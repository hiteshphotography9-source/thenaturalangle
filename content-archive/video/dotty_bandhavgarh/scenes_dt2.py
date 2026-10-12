import numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont
SP="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/"
FD=SP+"fonts/"; HD=SP+"dotty/"
W,H=1080,1920; TOTAL=58.6
GOLD=(255,196,92); AMB=(255,150,50); CREAM=(246,238,224); GREY=(176,170,160); CYAN=(90,215,230); RED=(235,80,60); INK=(24,20,16)
def F(n,s): return ImageFont.truetype(FD+n,int(s))
def ease(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def eo3(x): x=min(1,max(0,x)); return 1-(1-x)**3
def eob(x,k=1.6): x=min(1,max(0,x)); return 1+(k+1)*(x-1)**3+k*(x-1)**2
def seg(t,a,b): return min(1,max(0,(t-a)/(b-a)))
def lerp(a,b,x): return a+(b-a)*x
rng=np.random.default_rng(4)
# ---- stripe texture (procedural, original) ----
def make_stripes(w,h):
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    n1=cv2.GaussianBlur(rng.normal(0,1,(h,w)).astype(np.float32),(0,0),60); n1/=np.abs(n1).max()
    n2=cv2.GaussianBlur(rng.normal(0,1,(h,w)).astype(np.float32),(0,0),18); n2/=np.abs(n2).max()
    ph=yy*0.030+n1*9+n2*1.6+np.sin(xx*0.004)*2
    s=np.sin(ph); th=0.55+0.25*np.sin(xx*0.012+n1*3)
    stripe=np.clip((s-th)*6,0,1)*np.clip(np.abs(np.sin(xx*0.0045+n1*2))*1.6,0,1)
    base=np.zeros((h,w,3),np.float32); base[...]=(46,26,12)
    glow=np.clip(0.5+0.5*n1,0,1)[...,None]*np.array((40,22,6),np.float32)
    img=base+glow
    img=img*(1-stripe[...,None]*0.85)
    return np.clip(img,0,255)
STR=make_stripes(1200,2200)
yy,xx=np.mgrid[0:H,0:W]; VIG=(1-0.55*(((xx-W/2)/(W/2))**2*0.5+((yy-H/2)/(H/2))**2*0.7)).clip(0.35,1)[...,None].astype(np.float32)
GR=[rng.normal(0,1,(H//2,W//2)).astype(np.float32) for _ in range(6)]
def gold_tex():
    r=np.random.default_rng(1); y=np.linspace(0,1,H)[:,None]; x=np.linspace(0,1,W)[None,:]
    top=np.array([255,226,160],np.float32); bot=np.array([214,150,70],np.float32)
    base=top[None,None,:]*(1-y[:,:,None])+bot[None,None,:]*y[:,:,None]
    n=cv2.GaussianBlur(r.normal(0,1,(H,W)).astype(np.float32),(0,0),30); n/=np.abs(n).max()
    return np.clip(base*(1+0.1*n[...,None]),0,255)
TEX=gold_tex()
_ind=cv2.cvtColor(cv2.imread(HD+"india.png"),cv2.COLOR_BGR2RGB); IND=cv2.resize(_ind,(600,600),interpolation=cv2.INTER_AREA)
CM=np.zeros((600,600),np.uint8); cv2.circle(CM,(300,300),298,255,-1,cv2.LINE_AA); CMF=(cv2.GaussianBlur(CM,(0,0),1).astype(np.float32)/255)
DOT=(350*600/700,339.2*600/700)
# paper texture
PAP=np.clip(np.array((236,226,204),np.float32)[None,None,:]*(0.94+0.06*cv2.GaussianBlur(rng.normal(0,1,(520,900)).astype(np.float32),(0,0),3)[...,None]),0,255).astype(np.uint8)
def _ld(p): return cv2.cvtColor(cv2.imread(HD+p),cv2.COLOR_BGR2RGB)
P34=_ld('img/s34.png'); P31=_ld('img/p31.png'); S31=_ld('img/s31.png'); S33=_ld('img/s33.png')
def photo_win(img,src,box,rect,a,rad=26,border=GOLD):
    if a<=0.01: return img
    x0,y0,x1,y1=box; wx,wy,ww,wh=rect
    M=np.array([[ww/(x1-x0),0,-x0*ww/(x1-x0)],[0,wh/(y1-y0),-y0*wh/(y1-y0)]],np.float32)
    ph=cv2.warpAffine(src,M,(int(ww),int(wh)),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
    bl=cv2.GaussianBlur(ph,(0,0),1.2); ph=cv2.addWeighted(ph,1.35,bl,-0.35,0)
    mk=Image.new("L",(int(ww),int(wh)),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,int(ww)-1,int(wh)-1),radius=rad,fill=int(255*a))
    sh=Image.new("RGBA",(int(ww),int(wh)),(0,0,0,int(150*a))); img.alpha_composite(sh,(int(wx)+10,int(wy)+14))
    pim=Image.fromarray(ph).convert("RGBA"); pim.putalpha(mk); img.alpha_composite(pim,(int(wx),int(wy)))
    ImageDraw.Draw(img,"RGBA").rounded_rectangle((wx-2,wy-2,wx+ww+1,wy+wh+1),radius=rad,outline=border+(int(170*a),),width=3)
    return img
def shot(img,src,cx,cy,sc,rot,a):
    if a<=0.01: return img
    h,w=src.shape[:2]; pim=Image.fromarray(src).convert("RGBA").resize((int(w*sc),int(h*sc)),Image.LANCZOS).rotate(rot,expand=True,resample=Image.BICUBIC)
    al=pim.split()[-1].point(lambda v:int(v*a)); pim.putalpha(al)
    sh=Image.new("RGBA",pim.size,(0,0,0,0)); sh.putalpha(al.point(lambda v:int(v*0.55)))
    img.alpha_composite(sh,(int(cx-pim.width/2+12),int(cy-pim.height/2+16))); img.alpha_composite(pim,(int(cx-pim.width/2),int(cy-pim.height/2)))
    return img
EMB=[(rng.uniform(0,W),rng.uniform(0,H),rng.uniform(1.5,4),rng.uniform(10,40),rng.uniform(0,6.28)) for _ in range(70)]
OFF=0.6
M={'hook':0.2,'dotty':3.56,'origin':4.208,'y2012':6.858,'magadhi':8.506,'spotty':9.804,'sukhi':11.754,'home':12.832,'kids':14.32,'d1':17.248,'son':19.148,'push':20.336,'daughters':22.484,'out':24.282,'tala':27.14,'mother':28.758,'twocubs':30.458,'oct':31.696,'manpur':32.804,'patrol':35.242,'age':38.31,'natural':39.568,'left':42.106,'months':43.806,'watch':45.794,'mom':48.272,'legacy':49.01,'seen':51.908,'comment':53.776,'end':55.076}
T={k:v+OFF for k,v in M.items()}
SC=[0,6.9,13.3,T['oct'],T['left']-0.1,T['mom']-0.1,TOTAL]
def scene(t):
    for i in range(len(SC)-1):
        if SC[i]<=t<SC[i+1]: return i
    return len(SC)-2
def ctext(d,xy,s,f,fill,anchor="ms"): d.text(xy,s,font=f,fill=fill,anchor=anchor)
def shadowtext(d,xy,s,f,fill,a,anchor="ms",off=4):
    d.text((xy[0]+off,xy[1]+off),s,font=f,fill=(0,0,0,int(170*a)),anchor=anchor); d.text(xy,s,font=f,fill=fill[:3]+(int(255*a),),anchor=anchor)
def paw(d,cx,cy,r,col,a):
    if a<=0.01: return
    c=col+(int(255*a),)
    d.ellipse((cx-r,cy-r*0.55,cx+r,cy+r*0.95),fill=c)
    for dx,dy in ((-0.95,-1.05),(-0.33,-1.5),(0.33,-1.5),(0.95,-1.05)):
        rr=r*0.36; d.ellipse((cx+dx*r-rr,cy+dy*r-rr*1.2,cx+dx*r+rr,cy+dy*r+rr*1.2),fill=c)
def node(d,cx,cy,label,sub,a,col=GOLD,w=300,h=96,glow=0):
    if a<=0.01: return
    d.rounded_rectangle((cx-w/2,cy-h/2,cx+w/2,cy+h/2),radius=22,fill=(16,12,8,int(225*a)),outline=col+(int(255*a),),width=3+int(3*glow))
    d.text((cx,cy+(-4 if sub else 14)),label,font=F("Anton-Regular.ttf",42),fill=CREAM+(int(255*a),),anchor="ms")
    if sub: d.text((cx,cy+34),sub,font=F("BarlowCondensed-SemiBold.ttf",26),fill=col+(int(240*a),),anchor="ms")
def dline(d,p0,p1,a,col=GOLD,dash=16,w=4,prog=1.0):
    if a<=0.01: return
    x0,y0=p0; x1,y1=p1; L=math.hypot(x1-x0,y1-y0); n=int(L*prog/dash)
    for i in range(0,n,2):
        u0=i*dash/L; u1=min((i+1)*dash/L,prog)
        d.line((lerp(x0,x1,u0),lerp(y0,y1,u0),lerp(x0,x1,u1),lerp(y0,y1,u1)),fill=col+(int(230*a),),width=w)
def news(img,x,y,rot,outlet,date,head,a,s=1.0):
    if a<=0.01: return img
    cw,ch=860,330
    card=Image.fromarray(PAP[:ch,:cw]).convert("RGBA"); d=ImageDraw.Draw(card)
    d.rectangle((0,0,cw,52),fill=INK+(255,)); d.text((24,38),outlet,font=F("Anton-Regular.ttf",30),fill=(240,232,214,255),anchor="ls")
    d.text((cw-24,38),date,font=F("BarlowCondensed-SemiBold.ttf",26),fill=(210,200,180,255),anchor="rs")
    f=F("Anton-Regular.ttf",52); words=head.split(); lines=[];cur=""
    for wd in words:
        tr=(cur+" "+wd).strip()
        if d.textlength(tr,font=f)<=cw-60: cur=tr
        else: lines.append(cur);cur=wd
    lines.append(cur)
    for i,l in enumerate(lines[:3]): d.text((30,118+i*62),l,font=f,fill=INK+(255,),anchor="ls")
    for i in range(3): d.line((30,ch-70+i*16,cw-30-i*120,ch-70+i*16),fill=(150,140,120,255),width=6)
    d.text((cw-24,ch-14),"HEADLINE AS PUBLISHED. LAYOUT RECREATED.",font=F("BarlowCondensed-Medium.ttf",18),fill=(120,110,95,255),anchor="rs")
    card=card.resize((int(cw*s),int(ch*s)),Image.LANCZOS).rotate(rot,expand=True,resample=Image.BICUBIC)
    al=card.split()[-1].point(lambda v:int(v*a)); card.putalpha(al)
    sh=Image.new("RGBA",card.size,(0,0,0,0)); sh.putalpha(al.point(lambda v:int(v*0.55)))
    img.alpha_composite(sh,(int(x-card.width/2+12),int(y-card.height/2+16))); img.alpha_composite(card,(int(x-card.width/2),int(y-card.height/2)))
    return img
def frame(t):
    si=scene(t); lt=t-SC[si]
    # bg
    oy=int(60+t*7)%180; ox=int(40+math.sin(t*0.1)*30)
    bg=STR[oy:oy+H,ox:ox+W].copy()
    dim=[1.0,0.55,0.45,0.4,0.55,0.75][si]
    bg*=dim
    if si==0:   # warm reveal light on stripes
        g=np.exp(-(((xx-540)/420.0)**2+((yy-820)/520.0)**2))[...,None]*(0.6+0.4*ease(seg(t,0.2,3.5)))
        bg=bg*(1+g*1.1)
    img=Image.fromarray(np.clip(bg,0,255).astype(np.uint8)).convert("RGBA"); d=ImageDraw.Draw(img,"RGBA")
    # embers
    for (ex,ey,er,ev,ep) in EMB:
        y=(ey-t*ev)%H; x=ex+math.sin(t*0.6+ep)*20; a=0.25+0.25*math.sin(t*1.3+ep)
        d.ellipse((x-er,y-er,x+er,y+er),fill=AMB+(int(120*a),))
    # brand + progress
    d.text((W/2,48),"THE NATURAL ANGLE",font=F("BarlowCondensed-SemiBold.ttf",30),fill=(255,255,255,150),anchor="ms")
    d.rounded_rectangle((70,66,W-70,70),radius=2,fill=(255,255,255,40)); d.rounded_rectangle((70,66,70+(W-140)*t/TOTAL,70),radius=2,fill=GOLD+(220,))
    if si==0:
        k=eo3(seg(t,0.1,0.7)); d.text((W/2,230+int((1-k)*20)),"BANDHAVGARH TIGER RESERVE",font=F("BarlowCondensed-SemiBold.ttf",42),fill=GOLD+(int(255*k),),anchor="ms")
        # Ken Burns from full tiger to forehead, then ease back
        DX,DY=488,338
        full=(330,178,820,804); tight=(DX-150,180,DX+150,550)
        z=ease(seg(t,0.3,3.2))-0.45*ease(seg(t,T['dotty']-0.2,T['dotty']+1.6))
        box=tuple(lerp(f_,t_,z) for f_,t_ in zip(full,tight))
        rect=(70,290,940,1160)
        img=photo_win(img,P34,box,rect,eo3(seg(t,0.0,0.5)))
        d=ImageDraw.Draw(img,"RGBA")
        sx=rect[0]+(DX-box[0])/(box[2]-box[0])*rect[2]; sy=rect[1]+(DY-box[1])/(box[3]-box[1])*rect[3]
        ra=eo3(seg(t,2.4,2.9))*(1-seg(t,T['dotty']+0.8,T['dotty']+1.4)); rr=40*rect[2]/(box[2]-box[0])
        if ra>0:
            pul=1+0.06*math.sin(t*6)
            for k_,wid in ((1.25,10),(1.0,5)):
                d.ellipse((sx-rr*pul*k_,sy-rr*pul*k_,sx+rr*pul*k_,sy+rr*pul*k_),outline=AMB+(int((120 if wid==10 else 255)*ra),),width=wid)
            lx=sx-160; ly=max(rect[1]+70,sy-rr*1.35-20)
            d.rounded_rectangle((lx-10,ly-48,lx+330,ly+14),radius=16,fill=(16,12,8,int(220*ra)),outline=AMB+(int(255*ra),),width=3)
            d.text((lx+160,ly-6),"HER \"D\" MARK (APPROX.)",font=F("Anton-Regular.ttf",40),fill=CREAM+(int(255*ra),),anchor="ms")
        d.text((rect[0]+rect[2],rect[1]+rect[3]+34),"Photo: \u00a9 Ashish Tirkey / Pugdundee Safaris",font=F("BarlowCondensed-Medium.ttf",26),fill=GREY+(int(230*eo3(seg(t,0.5,1.0))),),anchor="rs")
        ta=eo3(seg(t,T['dotty']-0.05,T['dotty']+0.45))
        if ta>0:
            m=Image.new("L",(W,H),0); dm=ImageDraw.Draw(m); f=F("Anton-Regular.ttf",210)
            dm.text((W/2,1690+int((1-ta)*50)),"DOTTY",font=f,fill=int(255*ta),anchor="ms")
            mm=np.array(m).astype(np.float32)[...,None]/255; arr=np.array(img).astype(np.float32)
            shd=cv2.GaussianBlur(np.roll(np.roll(mm[...,0],10,0),8,1),(0,0),10)[...,None]
            sweep=np.clip(1-np.abs((xx+yy*0.4-((t-T['dotty'])*1400-200))/120.0),0,1)[...,None]*60
            arr[...,:3]=arr[...,:3]*(1-shd*0.6); arr[...,:3]=arr[...,:3]*(1-mm)+np.clip(TEX+sweep,0,255)*mm
            img=Image.fromarray(np.clip(arr,0,255).astype(np.uint8)); d=ImageDraw.Draw(img,"RGBA")
            sa=eo3(seg(t,T['origin']+0.2,T['origin']+0.8))
            d.text((W/2,1770),"c. 2012  \u00b7  2026",font=F("BarlowCondensed-SemiBold.ttf",46),fill=CREAM+(int(240*ta),),anchor="ms")
            d.text((W/2,1840),"ONE OF BANDHAVGARH'S MOST FAMOUS TIGRESSES",font=F("BarlowCondensed-Medium.ttf",34),fill=GREY+(int(240*sa),),anchor="ms")
    if si==1:
        a=eo3(seg(lt,0,0.6)); s=0.85+0.15*eo3(seg(lt,0,0.9))
        m=IND.copy(); cx,cy=540,600
        sz=int(600*s); mm=cv2.resize(m,(sz,sz)); mk=cv2.resize(CMF,(sz,sz))
        arr=np.array(img).astype(np.float32); x0,y0=cx-sz//2,cy-sz//2
        reg=arr[y0:y0+sz,x0:x0+sz,:3]; arr[y0:y0+sz,x0:x0+sz,:3]=reg*(1-mk[...,None]*a)+mm*mk[...,None]*a
        img=Image.fromarray(arr.astype(np.uint8)); d=ImageDraw.Draw(img,"RGBA")
        d.ellipse((x0,y0,x0+sz,y0+sz),outline=GOLD+(int(200*a),),width=3)
        px,py=x0+DOT[0]*sz/600,y0+DOT[1]*sz/600; pr=(lt*1.2)%1
        d.ellipse((px-9,py-9,px+9,py+9),fill=RED+(int(255*a),)); d.ellipse((px-12-pr*50,py-12-pr*50,px+12+pr*50,py+12+pr*50),outline=RED+(int(220*(1-pr)*a),),width=4)
        d.text((W/2,y0-30),"BANDHAVGARH  ·  MADHYA PRADESH",font=F("BarlowCondensed-SemiBold.ttf",40),fill=CREAM+(int(240*a),),anchor="ms")
        ya=eob(seg(t,T['y2012'],T['y2012']+0.5))
        if ya>0: d.rounded_rectangle((px+30,py-60,px+290,py+20),radius=18,fill=(16,12,8,int(220*min(1,ya))),outline=GOLD+(int(255*min(1,ya)),),width=3); d.text((px+160,py-6),"BORN c. 2012",font=F("Anton-Regular.ttf",40),fill=GOLD+(int(255*min(1,ya)),),anchor="ms")
        ma=eob(seg(t,T['magadhi'],T['magadhi']+0.5))
        if ma>0: d.rounded_rectangle((px-330,py+40,px-40,py+110),radius=18,fill=(16,12,8,int(220*min(1,ma))),outline=CYAN+(int(255*min(1,ma)),),width=3); d.text((px-185,py+88),"MAGADHI ZONE",font=F("Anton-Regular.ttf",38),fill=CYAN+(int(255*min(1,ma)),),anchor="ms")
        # family tree
        fa=eo3(seg(t,T['spotty']-0.4,T['spotty']+0.2)); ya_=1080
        sa=eo3(seg(t,T['sukhi'],T['sukhi']+0.5))
        node(d,540,ya_+120,"SUKHI PATIHA","MOTHER",sa,GOLD,360)
        dline(d,(540,ya_+170),(300,ya_+330),sa,GOLD,prog=sa); dline(d,(540,ya_+170),(780,ya_+330),sa,GOLD,prog=sa)
        node(d,300,ya_+380,"DOTTY","",eo3(seg(t,T['magadhi']+0.3,T['magadhi']+0.9)),AMB,300,96,1)
        node(d,780,ya_+380,"SPOTTY","SISTER",fa,GOLD,300)
        d.text((W/2,ya_+520),"Family details from safari records, not official.",font=F("BarlowCondensed-Medium.ttf",26),fill=GREY+(int(220*fa),),anchor="ms")
    if si==2:
        a=eo3(seg(lt,0,0.6))
        d.text((W/2,170),"HER STORY, ZONE BY ZONE",font=F("Anton-Regular.ttf",64),fill=CREAM+(int(255*a),),anchor="ms")
        d.text((W/2,215),"ZONE DIAGRAM, NOT A MAP",font=F("BarlowCondensed-Medium.ttf",28),fill=GREY+(int(220*a),),anchor="ms")
        MG=(300,860); TL=(760,1300); KH=(780,560)
        # edges
        ka=eo3(seg(t,T['d1'],T['d1']+0.6)); dline(d,MG,KH,ka,GOLD,prog=ka)
        ta_=eo3(seg(t,T['tala']+0.0,T['tala']+1.4)); dline(d,MG,TL,max(ta_,0),AMB,prog=ta_,w=6)
        node(d,*MG,"MAGADHI","HER HOME",a,CYAN,300,96,glow=1 if t<T['out'] else 0)
        node(d,*KH,"KHITAULI","",ka,GOLD,300)
        tna=eo3(seg(t,T['tala']+0.9,T['tala']+1.4)); node(d,*TL,"TALA","NEW HOME",tna,AMB,300,96,1)
        # Dotty marker
        pos=MG
        if t>=T['out']: 
            q=ease(seg(t,T['out'],T['out']+1.0)); pos=(lerp(MG[0],MG[0]+10,q),lerp(MG[1],MG[1]+300,q))
        if t>=T['tala']: q=ease(seg(t,T['tala'],T['tala']+1.4)); pos=(lerp(MG[0]+10,TL[0],q),lerp(MG[1]+300,TL[1]-230,q))
        mx,my=pos[0],pos[1]+110
        d.ellipse((mx-34,my-34,mx+34,my+34),fill=AMB+(int(255*a),),outline=(255,240,210,int(255*a)),width=4); d.text((mx,my+14),"D",font=F("Anton-Regular.ttf",42),fill=INK+(int(255*a),),anchor="ms")
        # cubs at magadhi
        ca=eo3(seg(t,T['kids'],T['kids']+0.6))*(1-seg(t,T['push'],T['push']+0.6))
        for i,(dx,dy) in enumerate(((-120,230),(0,265),(120,230))): paw(d,MG[0]+dx,MG[1]+dy,20,GOLD,ca*eo3(seg(t,T['kids']+i*0.2,T['kids']+i*0.2+0.4)))
        if ca>0: d.text((MG[0],MG[1]+330),"LITTERS RAISED HERE",font=F("BarlowCondensed-SemiBold.ttf",30),fill=GOLD+(int(240*ca),),anchor="ms")
        # D1 chip
        if ka>0:
            d.rounded_rectangle((KH[0]-190,KH[1]-190,KH[0]+190,KH[1]-80),radius=24,fill=(16,12,8,int(225*ka)),outline=GOLD+(int(255*ka),),width=3)
            d.text((KH[0],KH[1]-136),"D1",font=F("Anton-Regular.ttf",54),fill=GOLD+(int(255*ka),),anchor="ms")
            sa=eo3(seg(t,T['son'],T['son']+0.5)); d.text((KH[0],KH[1]-96),"KING OF KHITAULI  ·  REPORTED SON",font=F("BarlowCondensed-SemiBold.ttf",24),fill=CREAM+(int(240*max(ka*0.6,sa)),),anchor="ms")
        # daughters push
        da=eo3(seg(t,T['daughters'],T['daughters']+0.6))*(1-seg(t,T['tala'],T['tala']+0.8))
        for i,(dx,dy) in enumerate(((-140,110),(140,110),(0,230))): paw(d,MG[0]+dx,MG[1]+dy,22,CYAN,da)
        if da>0: d.text((MG[0],MG[1]-90),"HER DAUGHTERS",font=F("BarlowCondensed-SemiBold.ttf",32),fill=CYAN+(int(255*da),),anchor="ms")
        oa=eo3(seg(t,T['out'],T['out']+0.4))*(1-seg(t,T['tala']-0.3,T['tala']+0.3))
        if oa>0: d.text((MG[0]+10,MG[1]+530),"PUSHED OUT",font=F("Anton-Regular.ttf",64),fill=RED+(int(255*oa),),anchor="ms")
        if t>=T['push'] and t<T['out']+0.5:
            d.text((W/2,1640),"THE JUNGLE'S OLDEST RULE",font=F("BarlowCondensed-SemiBold.ttf",40),fill=GREY+(int(230*eo3(seg(t,T['push'],T['push']+0.5))*(1-seg(t,T['out'],T['out']+0.5))),),anchor="ms")
        mo=eo3(seg(t,T['mother'],T['mother']+0.5))
        if mo>0: d.text((TL[0],TL[1]+120),"A MOTHER AGAIN",font=F("Anton-Regular.ttf",54),fill=CREAM+(int(255*mo),),anchor="ms")
        cb=[eo3(seg(t,T['twocubs']+i*0.25,T['twocubs']+i*0.25+0.4)) for i in range(2)]
        for i in range(2): paw(d,TL[0]-60+i*120,TL[1]+230,24,GOLD,cb[i])
        if cb[1]>0: d.text((TL[0],TL[1]+320),"+2 CUBS",font=F("Anton-Regular.ttf",46),fill=GOLD+(int(255*cb[1]),),anchor="ms")
    if si==3:
        a=eo3(seg(lt,0,0.4))
        st=eob(seg(t,T['oct'],T['oct']+0.35),2.2); sc=lerp(1.6,1.0,min(1,st))
        f=F("Anton-Regular.ttf",int(120*sc))
        d.text((W/2,330),"9 OCTOBER 2026",font=f,fill=CREAM+(int(255*a),),anchor="ms")
        la=eo3(seg(t,T['manpur'],T['manpur']+0.5))
        if la>0:
            d.rounded_rectangle((90,400,W-90,530),radius=26,fill=(16,12,8,int(225*la)),outline=RED+(int(255*la),),width=3)
            d.ellipse((130,447,166,483),fill=RED+(int(255*la),))
            d.text((190,452),"MANPUR BUFFER RANGE",font=F("Anton-Regular.ttf",46),fill=CREAM+(int(255*la),),anchor="ls")
            d.text((190,500),"MAJHKHETA BEAT",font=F("BarlowCondensed-SemiBold.ttf",34),fill=GREY+(int(240*la),),anchor="ls")
        pa=eo3(seg(t,T['patrol'],T['patrol']+0.5))
        if pa>0: d.text((W/2,610),"FOUND DURING AN ELEPHANT PATROL",font=F("BarlowCondensed-SemiBold.ttf",44),fill=CREAM+(int(255*pa),),anchor="ms")
        aa=seg(t,T['age'],T['age']+0.9)
        if aa>0:
            n=int(round(14*ease(aa))); d.text((W/2,790),f"{n}",font=F("Anton-Regular.ttf",170),fill=GOLD+(int(255*min(1,aa*3)),),anchor="ms")
            d.text((W/2,850),"YEARS, ABOUT",font=F("BarlowCondensed-SemiBold.ttf",40),fill=GOLD+(int(240*min(1,aa*3)),),anchor="ms")
        na=eo3(seg(t,T['natural'],T['natural']+0.5))
        if na>0:
            d.rounded_rectangle((90,900,W-90,1010),radius=24,fill=(16,12,8,int(225*na)),outline=GOLD+(int(255*na),),width=3)
            d.text((W/2,950),"PRELIMINARY EXAMINATION: NATURAL CAUSES",font=F("BarlowCondensed-SemiBold.ttf",38),fill=CREAM+(int(255*na),),anchor="ms")
            d.text((W/2,990),"Field Director, Bandhavgarh TR, as reported",font=F("BarlowCondensed-Medium.ttf",26),fill=GREY+(int(230*na),),anchor="ms")
        n1=eo3(seg(t,T['manpur']+0.6,T['manpur']+1.2)); n2=eo3(seg(t,T['patrol']+0.4,T['patrol']+1.0)); n3=eo3(seg(t,T['natural']+0.6,T['natural']+1.2))
        img=shot(img,S31,560+int((1-n1)*700),1250,0.6,-2.5,n1)
        img=shot(img,S33,520-int((1-n3)*700),1660,0.6,2.0,n3)
        dd_=ImageDraw.Draw(img,"RGBA")
        if n3>0: dd_.text((W-60,1905),"Screenshots: The Hans India (11 Oct 2026), Hindi news report (10 Oct 2026)",font=F("BarlowCondensed-Medium.ttf",22),fill=GREY+(int(220*n3),),anchor="rs")
        d=ImageDraw.Draw(img,"RGBA")
    if si==4:
        a=eo3(seg(lt,0,0.5))
        for i in range(2): paw(d,400+i*280,760,95,GOLD,eo3(seg(lt,0.1+i*0.3,0.6+i*0.3)))
        d.text((W/2,330),"TWO CUBS",font=F("Anton-Regular.ttf",150),fill=CREAM+(int(255*a),),anchor="ms")
        d.text((W/2,410),"LEFT BEHIND",font=F("BarlowCondensed-SemiBold.ttf",56),fill=GOLD+(int(255*a),),anchor="ms")
        ma=eo3(seg(t,T['months'],T['months']+0.5))
        if ma>0: d.text((W/2,1080),"15 TO 16 MONTHS OLD",font=F("Anton-Regular.ttf",86),fill=CREAM+(int(255*ma),),anchor="ms")
        wa=eo3(seg(t,T['watch'],T['watch']+0.5))
        if wa>0:
            for k in range(3):
                r=((t*0.6+k/3)%1); rr=120+r*360
                d.ellipse((540-rr,760-rr,540+rr,760+rr),outline=CYAN+(int(160*(1-r)*wa),),width=3)
            d.text((W/2,1230),"FOREST DEPARTMENT IS MONITORING THEM",font=F("BarlowCondensed-SemiBold.ttf",44),fill=CYAN+(int(255*wa),),anchor="ms")
    if si==5:
        a=eo3(seg(t,T['mom'],T['mom']+0.6))
        d.text((W/2,560),"A MOTHER",font=F("Anton-Regular.ttf",150),fill=CREAM+(int(255*a),),anchor="ms")
        la=eo3(seg(t,T['legacy'],T['legacy']+0.7))
        d.text((W/2,650),"WHO FILLED BANDHAVGARH",font=F("BarlowCondensed-SemiBold.ttf",58),fill=GOLD+(int(255*la),),anchor="ms")
        d.text((W/2,715),"WITH HER LINE",font=F("BarlowCondensed-SemiBold.ttf",58),fill=GOLD+(int(255*la),),anchor="ms")
        pa=eo3(seg(t,T['mom']-0.1,T['mom']+0.6))
        z=ease(seg(t,T['mom'],TOTAL))*0.08
        img=photo_win(img,P31,(0+820*z/2,0+490*z/2,820-820*z/2,490-490*z/2),(60,780,960,574),pa,border=AMB)
        d=ImageDraw.Draw(img,"RGBA")
        d.text((W-60,1384),"Photo: NBT, as published by The Hans India",font=F("BarlowCondensed-Medium.ttf",24),fill=GREY+(int(220*pa),),anchor="rs")
        sa=eo3(seg(t,T['seen'],T['seen']+0.6))
        if sa>0: d.text((W/2,1490),"DID YOU EVER SEE DOTTY?",font=F("Anton-Regular.ttf",78),fill=CREAM+(int(255*sa),),anchor="ms")
        ca=eo3(seg(t,T['comment'],T['comment']+0.5))
        if ca>0:
            d.rounded_rectangle((W/2-260,1530,W/2+260,1616),radius=43,fill=GOLD+(int(240*ca),)); d.text((W/2,1588),"TELL ME IN THE COMMENTS",font=F("BarlowCondensed-SemiBold.ttf",42),fill=INK+(int(255*ca),),anchor="ms")
        ea=eo3(seg(t,T['end']+0.3,T['end']+1.2))
        if ea>0:
            d.text((W/2,1745),"DOTTY  \u00b7  c. 2012 TO 2026",font=F("Anton-Regular.ttf",64),fill=AMB+(int(255*ea),),anchor="ms")
        d.text((W/2,1880),"Images belong to their respective owners. DM for credit or removal.",font=F("BarlowCondensed-Medium.ttf",26),fill=GREY+(int(220*pa),),anchor="ms")
    out=np.array(img)[...,:3].astype(np.float32)*VIG
    out+=cv2.resize(GR[int(t*30)%6],(W,H))[...,None]*5.5
    for h in SC[1:-1]:
        dd=t-h
        if 0<=dd<0.18: out+=(1-dd/0.18)*30
    f=min(1,t/0.3)*min(1,(TOTAL-t)/0.6); out*=f
    return np.clip(out,0,255).astype(np.uint8)
