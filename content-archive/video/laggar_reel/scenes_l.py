import numpy as np, cv2, math, os
from PIL import Image, ImageDraw, ImageFont
SP="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/"
FD=SP+"fonts/"; U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"; HD=SP+"lag/"
FL=["64a42d44","b1208e85","26726f42","dc158818","f02d75ca","4dec5138","35021122"]
W,H=1080,1920; CW,CH=1188,2112; TOTAL=49.5
GOLD=(226,184,104); CREAM=(244,238,226); GREY=(190,186,176); CYAN=(80,225,235)
def F(n,s): return ImageFont.truetype(FD+n,int(s))
def corm(s):
    f=ImageFont.truetype(FD+"CormorantGaramond-Italic[wght].ttf",int(s))
    try: f.set_variation_by_axes([500])
    except Exception: pass
    return f
def ease(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def eo3(x): x=min(1,max(0,x)); return 1-(1-x)**3
def seg(t,a,b): return min(1,max(0,(t-a)/(b-a)))
def lerp(a,b,x): return a+(b-a)*x
# gold texture
def gold_tex():
    rng=np.random.default_rng(1)
    yy=np.linspace(0,1,H)[:,None]; xx=np.linspace(0,1,W)[None,:]
    top=np.array([252,232,170],np.float32); bot=np.array([206,160,84],np.float32)
    base=top[None,None,:]*(1-yy[:,:,None])+bot[None,None,:]*yy[:,:,None]; base=base*(0.96+0.08*xx[:,:,None])
    def nz(s): return cv2.GaussianBlur(rng.normal(0,1,(H,W)).astype(np.float32),(0,0),s)
    n1=nz(40); n1/=np.abs(n1).max(); n2=nz(10); n2/=np.abs(n2).max(); ridge=np.abs(nz(5)-nz(12)); ridge/=ridge.max()
    tex=base*(1+0.12*n1[:,:,None]+0.07*n2[:,:,None])+(ridge[:,:,None]**2)*34-8+rng.normal(0,1,(H,W)).astype(np.float32)[:,:,None]*5
    return np.clip(tex,0,255)
TEX=gold_tex()
yy,xx=np.mgrid[0:H,0:W]; VIG=(1-0.38*(((xx-W/2)/(W/2))**2*0.6+((yy-H/2)/(H/2))**2*0.9)).clip(0.5,1)[...,None].astype(np.float32)
rng=np.random.default_rng(3); GR=[rng.normal(0,1,(H//2,W//2)).astype(np.float32) for _ in range(6)]
# placement: (img index, source anchor (sx,sy), canvas anchor (cx,cy), scale)
PL={0:((818,968),(594,1250),1.2),6:((1000,760),(800,1400),1.0),2:((585,840),(594,1190),1.0),5:((1337,760),(594,1150),0.55),
    4:((1650,1132),(594,1250),1.12),3:((746,1202),(640,1400),0.8),1:((1898,1546),(594,1150),0.62),"0b":((818,968),(594,1400),1.3)}
_cache={}
def layers(key):
    if key in _cache: return _cache[key]
    i=0 if key=="0b" else key
    (sx,sy),(cx,cy),s=PL[key]
    src=cv2.cvtColor(cv2.imread(U+FL[i]+"-image.jpg"),cv2.COLOR_BGR2RGB)
    a=np.array(Image.open(HD+f"{i}.png").split()[-1]).astype(np.float32)/255
    h,w=src.shape[:2]
    # background: heavy blur of cover version
    sc=max(CW/w,CH/h)*1.2; bgw,bgh=int(w*sc),int(h*sc); bg=cv2.resize(src,(bgw,bgh),interpolation=cv2.INTER_AREA)
    ox=(bgw-CW)//2; oy=(bgh-CH)//2; bg=bg[oy:oy+CH,ox:ox+CW]; bg=cv2.GaussianBlur(bg,(0,0),48).astype(np.float32)*0.85
    M=np.array([[s,0,cx-sx*s],[0,s,cy-sy*s]],np.float32)
    ph=cv2.warpAffine(src,M,(CW,CH),flags=cv2.INTER_AREA if s<1 else cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=0).astype(np.float32)
    cov=cv2.warpAffine(np.ones((h,w),np.float32),M,(CW,CH),flags=cv2.INTER_LINEAR,borderValue=0)
    cov=cv2.erode(cov,np.ones((3,3),np.uint8),iterations=2); cov=cv2.GaussianBlur(cov,(0,0),28)[...,None]; cov=np.clip((cov-0.2)/0.8,0,1)
    base=bg*(1-cov)+ph*cov
    al=cv2.warpAffine(a,M,(CW,CH),flags=cv2.INTER_LINEAR,borderValue=0)
    _cache.clear(); _cache[key]=(base.astype(np.float32),al); return _cache[key]
B=[ # t0,t1,img,lead,lines,sub,facts,special,sub_xy,kb
 (0,5.5,0,"Falcons hunt birds.",["BIRDS","ONLY?"],["NOT QUITE."],[("THE USUAL STORY","Fast aerial chases after doves and small birds."),("ALSO ON THE MENU","Bats, small mammals, lizards and large insects.")],None,None),
 (5.5,11.5,6,"In one falcon nest,",["79%","LIZARD"],["NOT BIRDS."],[("THE STUDY","One breeding pair, watched for a full season in 2019."),("THE PREY","Spiny-tailed lizards were 79% of what the chicks were fed.")],"bar",None),
 (11.5,17.5,2,"In that same nest,",["16"],["KINDS OF PREY","FED TO FOUR CHICKS"],[("THE MIX","Includes 4 reptile, 5 mammal and 3 bird species in total."),("THE NEST","One breeding pair, one season, 2019.")],"dots",None),
 (17.5,23.5,5,"It hunts",["LOW","AND FAST"],["FROM A PERCH.","OR AT GROUND LEVEL."],[("HOW","From an exposed perch, or in fast, low flight over open ground."),("WHEN IT STOOPS","When the target is a bird.")],None,None),
 (23.5,29.5,3,"It does not build one.",["BORROWED","NEST"],["OLD NESTS OF","CROWS AND VULTURES."],[("THE NEST","Takes over old stick nests, even Egyptian Vulture nests, and adds no material."),("THE SEASON","Eggs are laid from January to April.")],None,None),
 (29.5,36.0,4,"Once recorded at",["4,360 M"],["IN LADAKH."],[("USUAL RANGE","Mostly below 1,000 m. A resident, not a mountain bird."),("USUAL HOME","Dry, open country, farmland, villages and cities.")],"alt",None),
 (36.0,42.5,1,"A suspected fall of",["20-29%"],["IN ABOUT TEN YEARS."],[("WHAT IS LEFT","10,000 to 19,999 mature birds worldwide."),("WHY","Pesticides, habitat loss, and capture as bait for larger falcons.")],"fall",None),
 (42.5,49.5,"0b","Next time a falcon sits on a pole,",["LOOK","TWICE"],["IT MIGHT BE","A LAGGAR."],[("PROTECTED","Schedule I of India's Wildlife Protection Act."),("YOUR TURN","Where have you seen one? Tell me below.")],"end",None)]
HITS=[b[0] for b in B]
def beat_of(t):
    for i,b in enumerate(B):
        if b[0]<=t<b[1]: return i
    return len(B)-1
def title_mask(lines,t_rel,beat):
    probe=ImageDraw.Draw(Image.new("L",(10,10)))
    full=list(lines)
    f100=F("Anton-Regular.ttf",100); wmax=max(probe.textlength(l,font=f100) for l in full)
    cap=380 if len(full)==1 else 300
    size=min(930/wmax*100,cap); f=F("Anton-Regular.ttf",size)
    capH=f.getbbox("H")[3]-f.getbbox("H")[1]; lh=capH*1.14
    return f,size,capH,lh
def draw_title(beat,t):
    idx=beat; b=B[idx]; lines=list(b[4]); lt=t-b[0]
    f,size,capH,lh=title_mask(lines,lt,idx)
    shown=list(lines)
    p=ease(seg(lt,0.2,1.6))
    if idx==1: shown[0]=f"{int(round(79*p))}%"
    if idx==2: shown[0]=f"{int(round(16*p))}"
    if idx==5: shown[0]=f"{int(round(4360*p)):,} M"
    m=Image.new("L",(W,H),0); d=ImageDraw.Draw(m); y0=262
    for k,l in enumerate(shown):
        ap=eo3(seg(lt,0.1+0.18*k,0.55+0.18*k))
        y=y0+k*lh+int((1-ap)*50)
        d.text((70,y-f.getbbox("H")[1]),l,font=f,fill=int(255*ap))
    tb=y0+len(lines)*lh
    return np.array(m).astype(np.float32)/255,tb
def textwrap_lines(d,text,font,maxw):
    out=[];cur=""
    for w in text.split():
        c=(cur+" "+w).strip()
        if d.textlength(c,font=font)<=maxw: cur=c
        else: out.append(cur);cur=w
    out.append(cur); return out
def frame(t):
    bi=beat_of(t); b=B[bi]; lt=t-b[0]; dur=b[1]-b[0]
    base,al=layers(b[2])
    z=1.0+0.07*ease(lt/dur)+0.03*(1-seg(lt,0,0.45))**2
    vcx=594+lerp(-10,16,lt/dur)*(1 if bi%2==0 else -1); vcy=1056+lerp(0,-26,lt/dur)
    M=np.array([[z,0,540-z*vcx],[0,z,960-z*vcy]],np.float32)
    ph=cv2.warpAffine(base,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    a=cv2.warpAffine(al,M,(W,H),flags=cv2.INTER_LINEAR,borderValue=0)[...,None]
    # grade: top/bottom darken
    g=np.ones((H,1,1),np.float32); g[:900]=np.linspace(0.62,1.0,900)[:,None,None]; g[1380:]=np.linspace(1.0,0.30,H-1380)[:,None,None]
    bgl=ph*g
    tm,tb=draw_title(bi,t); tm=tm*eo3(seg(lt,0.0,0.3))
    sh=cv2.GaussianBlur(np.roll(np.roll(tm,10,0),6,1),(0,0),9)[...,None]
    sweep=np.clip(1-np.abs((xx+yy*0.5-(lt*900-300))/160.0),0,1)[...,None]*0.45*(seg(lt,0.6,1.2)>0)
    gold=np.clip(TEX+sweep*70,0,255)
    comp=bgl*(1-sh*0.6)
    comp=comp*(1-tm[...,None])+gold*tm[...,None]
    comp=comp*(1-a)+(ph*np.where(g<1,0.0+g,1))*a if False else comp*(1-a)+(ph*np.clip(g,0,1.0))*a
    img=Image.fromarray(np.clip(comp,0,255).astype(np.uint8)); d=ImageDraw.Draw(img,"RGBA")
    # brand + progress
    d.text((60,64),"THE NATURAL ANGLE",font=F("BarlowCondensed-SemiBold.ttf",30),fill=(240,236,226,200),anchor="ls")
    for i in range(8):
        x0=60+i*((W-120)/8); ww=(W-120)/8-8; p=seg(t,B[i][0],B[i][1]); d.rounded_rectangle((x0,84,x0+ww,89),radius=2,fill=(255,255,255,50))
        if p>0: d.rounded_rectangle((x0,84,x0+ww*p,89),radius=2,fill=GOLD+(255,))
    # lead
    ap=eo3(seg(lt,0.0,0.45)); lf=corm(58)
    d.text((70,190+int((1-ap)*20)),b[3],font=lf,fill=CREAM+(int(255*ap),),anchor="ls")
    # sub
    sy=int(tb+70)
    for k,s in enumerate(b[5]):
        sp=eo3(seg(lt,0.9+0.12*k,1.4+0.12*k))
        d.text((70,sy+k*58+int((1-sp)*24)),s,font=F("BarlowCondensed-Medium.ttf",50),fill=(236,232,222,int(235*sp)),anchor="ls")
    # specials
    sp=b[7]; y=1470
    if sp=="bar":
        p=ease(seg(lt,0.8,2.4)); x0,x1=70,W-70; wl=int((x1-x0)*0.79*p)
        d.rounded_rectangle((x0-12,y-70,x1+12,y+78),radius=18,fill=(10,12,10,150))
        d.text((x0,y-24),"SHARE OF PREY FED TO FOUR CHICKS, ONE NEST, 2019",font=F("BarlowCondensed-Medium.ttf",24),fill=GOLD+(255,),anchor="ls")
        d.rectangle((x0,y,x0+wl,y+44),fill=(226,184,104,255)); d.rectangle((x0+int((x1-x0)*0.79),y,x0+int((x1-x0)*0.79)+int((x1-x0)*0.21*p),y+44),fill=(92,90,84,255))
        if p>0.6: d.text((x0+12,y+34),"SPINY-TAILED LIZARD",font=F("BarlowCondensed-SemiBold.ttf",28),fill=(20,16,8,255),anchor="ls")
    if sp=="dots":
        d.rounded_rectangle((58,y-62,W-58,y+96),radius=18,fill=(10,12,10,150))
        d.text((70,y-24),"16 KINDS OF PREY. 12 NAMED: 4 REPTILE, 5 MAMMAL, 3 BIRD",font=F("BarlowCondensed-Medium.ttf",24),fill=GOLD+(255,),anchor="ls")
        cols=[(226,184,104)]*4+[(160,200,120)]*5+[(120,170,230)]*3+[(150,150,146)]*4
        for i in range(16):
            q=eo3(seg(lt,0.9+i*0.1,1.1+i*0.1)); cx=100+i*58.5; r=int(20*q)
            if r>0: d.ellipse((cx-r,y+44-r,cx+r,y+44+r),fill=cols[i]+(255,))
    if sp=="alt":
        p=ease(seg(lt,0.8,3.0)); x0,x1=90,W-90
        d.rounded_rectangle((58,y-72,W-58,y+90),radius=18,fill=(10,12,10,170))
        d.line((x0,y+10,x1,y+10),fill=(150,146,134,255),width=4)
        marks=[(0,"SEA LEVEL"),(1000,"1,000 M"),(1980,"1,980 M NEPAL"),(4360,"4,360 M LADAKH")]
        d.line((x0,y+10,x0+(x1-x0)*p*(4360/4360),y+10),fill=GOLD+(255,),width=8)
        for m,lab in marks:
            xm=x0+(x1-x0)*m/4360; on=p*4360>=m; hi=m==4360
            d.ellipse((xm-9,y+1,xm+9,y+19),fill=(GOLD if (hi or on) else (210,205,194))+(255,))
            if on: d.text((min(xm,x1-10),y-22),lab,font=F("BarlowCondensed-SemiBold.ttf" if hi else "BarlowCondensed-Medium.ttf",24),fill=(GOLD if hi else (225,220,208))+(255,),anchor="rs" if m>=1980 else "ls")
    if sp=="fall":
        p=ease(seg(lt,0.8,3.0)); x0,x1=90,W-90
        d.rounded_rectangle((58,y-72,W-58,y+96),radius=18,fill=(10,12,10,150))
        d.text((70,y-30),"SUSPECTED DECLINE OVER ABOUT TEN YEARS",font=F("BarlowCondensed-Medium.ttf",24),fill=GOLD+(255,),anchor="ls")
        pts=[(x0+(x1-x0)*u,y+12+ (60*u*0.25 if True else 0)+ (45*(u**2.2))) for u in np.linspace(0,p,40)]
        for u in np.linspace(0,p,40)[:0]: pass
        if len(pts)>1: d.line(pts,fill=(255,120,90,255),width=7)
        d.text((x0,y+66),"NOW",font=F("BarlowCondensed-SemiBold.ttf",24),fill=CREAM+(255,),anchor="ls")
        d.text((x1,y+66),"10 YEARS",font=F("BarlowCondensed-SemiBold.ttf",24),fill=CREAM+(255,),anchor="rs")
        if p>0.95: d.text((x1,y-30),"-20 TO -29%",font=F("Anton-Regular.ttf",40),fill=(255,140,110,255),anchor="rs")
    if sp=="end":
        q=eo3(seg(lt,1.8,2.4)); d.rounded_rectangle((70,1470,W-70,1550),radius=40,fill=GOLD+(int(240*q),))
        d.text((W/2,1526),"WHERE HAVE YOU SEEN ONE?",font=F("BarlowCondensed-SemiBold.ttf",46),fill=(20,16,8,int(255*q)),anchor="ms")
    # facts
    fa=eo3(seg(lt,1.4,2.0)); y=1612
    for k,(hd,tx) in enumerate(b[6]):
        x=70+k*500; d.line((x,y-6,x,y+170),fill=(255,255,255,int(90*fa)),width=2)
        d.text((x+22,y+22),hd,font=F("BarlowCondensed-SemiBold.ttf",26),fill=GOLD+(int(255*fa),),anchor="ls")
        ff=F("Barlow-Medium.ttf",28)
        for j,l in enumerate(textwrap_lines(d,tx,ff,420)[:4]): d.text((x+22,y+62+j*36),l,font=ff,fill=CREAM+(int(245*fa),),anchor="ls")
    out=np.array(img).astype(np.float32)*VIG
    out+=cv2.resize(GR[int(t*30)%6],(W,H))[...,None]*5.0
    for h in HITS:
        dd=t-h
        if 0<=dd<0.16: out+=(1-dd/0.16)*40
    f=min(1,t/0.25)*min(1,(TOTAL-t)/0.4); out*=f
    return np.clip(out,0,255).astype(np.uint8)
