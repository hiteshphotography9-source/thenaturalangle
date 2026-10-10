import numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont
FD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/fonts/"
HD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/tvl/"
W,H=1080,1920; TOTAL=54.1
GOLD=(255,200,70); CYAN=(80,225,235); RED=(255,84,70); CREAM=(250,246,236); GREY=(170,176,182)
def F(n,s): return ImageFont.truetype(FD+n,int(s))
def ease(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def eo3(x): x=min(1,max(0,x)); return 1-(1-x)**3
def seg(t,a,b): return min(1,max(0,(t-a)/(b-a)))
def lerp(a,b,x): return a+(b-a)*x
WX,WY,WW,WH=162,300,756,1344
_fc={}
def src(i):
    i=max(1,min(1624,i))
    if i not in _fc:
        if len(_fc)>40: _fc.pop(next(iter(_fc)))
        _fc[i]=cv2.cvtColor(cv2.imread(HD+f"f/f_{i:04d}.jpg"),cv2.COLOR_BGR2RGB)
    return _fc[i]
MASK=np.zeros((WH,WW),np.uint8); cv2.rectangle(MASK,(28,0),(WW-29,WH-1),255,-1); cv2.rectangle(MASK,(0,28),(WW-1,WH-29),255,-1)
for cx,cy in ((28,28),(WW-29,28),(28,WH-29),(WW-29,WH-29)): cv2.circle(MASK,(cx,cy),28,255,-1,cv2.LINE_AA)
MASKF=(cv2.GaussianBlur(MASK,(0,0),0.8).astype(np.float32)/255)[...,None]
yy,xx=np.mgrid[0:H,0:W]; VIG=(1-0.42*(((xx-W/2)/(W/2))**2*0.6+((yy-H/2)/(H/2))**2*0.9)).clip(0.5,1)[...,None].astype(np.float32)
rng=np.random.default_rng(11); GR=[rng.normal(0,1,(H//2,W//2)).astype(np.float32) for _ in range(6)]
# beats: t0,t1,kicker,headline(list lines)
BEATS=[(0,8.3,"ROUND 4  ·  BEHAVIOUR",["TIGER: GROUND LEVEL"]),
       (8.3,13.2,"01  THE FRAME",["LIMITED ANGLES.","NOT THE SAME FRAME."]),
       (13.2,26.2,"02  RARE BEHAVIOUR",["MATING. FIGHTS.","SEEN VERY RARELY."]),
       (26.2,35.2,"03  THE LEOPARD",["THEN THE GAME CHANGES"]),
       (35.2,45.9,"04  UP IN THE TREE",["A DIFFERENT KIND OF FRAME"]),
       (45.9,TOTAL+1,"05  THE PAYOFF",["THE NEXT LEVEL SHOT"])]
HITS=[b[0] for b in BEATS]+[17.1,35.23,47.23]
def beat_of(t):
    for i,b in enumerate(BEATS):
        if b[0]<=t<b[1]: return i
    return len(BEATS)-1
def fit(d,text,fn,size,maxw):
    while True:
        f=F(fn,size)
        if d.textlength(text,font=f)<=maxw or size<30: return f
        size-=3
def spaced(d,xy,text,font,fill,sp=6):
    ws=[d.textlength(c,font=font) for c in text]; tot=sum(ws)+sp*(len(text)-1); x=xy[0]-tot/2
    for c,w in zip(text,ws): d.text((x,xy[1]),c,font=font,fill=fill,anchor="ls"); x+=w+sp
def orig_frame(t):
    fr=src(int(t*30)+1)
    if t>=51.5:
        fr=fr.copy(); x0,x1,y0,y1=40,690,845,1010
        up=fr[y0-250:y1-250,x0:x1].astype(np.float32); reg=fr[y0:y1,x0:x1].astype(np.float32)
        bl=cv2.GaussianBlur(up,(0,0),20)*0.5
        mk=np.zeros((y1-y0,x1-x0),np.float32); cv2.rectangle(mk,(20,14),(x1-x0-20,y1-y0-14),1,-1); mk=cv2.GaussianBlur(mk,(0,0),8)[...,None]
        fr[y0:y1,x0:x1]=(reg*(1-mk)+bl*mk).astype(np.uint8)
    return fr
def rbar(d,x0,x1,y,lo,hi,mx,col,A,p,hh=16):
    d.rounded_rectangle((x0,y,x1,y+hh),radius=hh//2,fill=(255,255,255,int(40*A)))
    a=x0+(x1-x0)*lo/mx; b=x0+(x1-x0)*hi/mx; b2=a+(b-a)*p
    if b2>a+2: d.rounded_rectangle((a,y,b2,y+hh),radius=hh//2,fill=col+(int(255*A),))
def frame(t):
    fr=orig_frame(t); win=cv2.resize(fr,(WW,WH),interpolation=cv2.INTER_CUBIC)
    bi=beat_of(t); b=BEATS[bi]; lt=t-b[0]; pk=0.0
    for h in HITS:
        dd=t-h
        if 0<=dd<0.5: pk=max(pk,(1-dd/0.5)**2)
    bg=cv2.GaussianBlur(cv2.resize(fr,(W,H),interpolation=cv2.INTER_LINEAR),(0,0),38); base=bg.astype(np.float32)*0.30
    w=win.astype(np.float32); w=(w-128)*1.05+128; g=w.mean(2,keepdims=True); w=g+(w-g)*1.08
    sc=1+0.012*pk
    if sc>1.0005:
        M=np.array([[sc,0,(1-sc)*WW/2],[0,sc,(1-sc)*WH/2]],np.float32); w=cv2.warpAffine(w,M,(WW,WH),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    sh=np.zeros((H,W),np.float32); sh[WY:WY+WH,WX:WX+WW]=1; sh=cv2.GaussianBlur(sh,(0,0),26)[...,None]; base=base*(1-0.5*sh)
    reg=base[WY:WY+WH,WX:WX+WW]; base[WY:WY+WH,WX:WX+WW]=reg*(1-MASKF)+w*MASKF
    img=Image.fromarray(np.clip(base,0,255).astype(np.uint8)); d=ImageDraw.Draw(img,"RGBA")
    d.rounded_rectangle((WX-2,WY-2,WX+WW+1,WY+WH+1),radius=30,outline=GOLD+(150,),width=2)
    nB=len(BEATS)-1+1; sw=(W-140-10*(nB-1))/nB
    d.text((W/2,42),"THE NATURAL ANGLE",font=F("BarlowCondensed-Medium.ttf",30),fill=(255,255,255,170),anchor="ms")
    for i in range(nB):
        x0=70+i*(sw+10); d.rounded_rectangle((x0,60,x0+sw,66),radius=3,fill=(255,255,255,50))
        p=seg(t,BEATS[i][0],BEATS[i][1] if i<nB-1 else TOTAL)
        if p>0: d.rounded_rectangle((x0,60,x0+sw*p,66),radius=3,fill=GOLD+(255,))
    a=eo3(seg(lt,0.05,0.4)); fo=1-seg(t,b[1]-0.18,b[1]) if bi<len(BEATS)-1 else 1; al=int(255*a*fo)
    spaced(d,(W/2,128+int((1-a)*18)),b[2],F("BarlowCondensed-SemiBold.ttf",38),GOLD+(al,),sp=9)
    lines=b[3]; dy=int((1-eo3(seg(lt,0.05,0.5)))*40)
    if len(lines)==1:
        hf=fit(d,lines[0],"Anton-Regular.ttf",100,W-110); ys=[238]
    else:
        sz=min(76,int(min(fit(d,l,"Anton-Regular.ttf",76,W-110).size for l in lines))); hf=F("Anton-Regular.ttf",sz); ys=[212,282]
    for l,yv in zip(lines,ys):
        d.text((W/2+3,yv+dy+4),l,font=hf,fill=(0,0,0,int(160*a*fo)),anchor="ms"); d.text((W/2,yv+dy),l,font=hf,fill=CREAM+(al,),anchor="ms")
    by=WY+WH+14
    def panel(y,h,A,col=GOLD): d.rounded_rectangle((60,y,W-60,y+h),radius=22,fill=(14,16,20,int(224*A)),outline=col+(int(220*A),),width=3)
    # tiger size card
    if 1.2<=t<8.1:
        A=eo3(seg(t,1.2,1.7))*(1-seg(t,7.8,8.1)); y=by+4+int((1-eo3(seg(t,1.2,1.8)))*50); panel(y,236,A)
        d.text((90,y+40),"TYPICAL ADULT MALE BENGAL TIGER",font=F("BarlowCondensed-SemiBold.ttf",34),fill=GOLD+(int(255*A),),anchor="ls")
        d.text((W-90,y+40),"APPROXIMATE",font=F("BarlowCondensed-Medium.ttf",26),fill=GREY+(int(230*A),),anchor="rs")
        cols=[("2.8-3.1","M","LENGTH, HEAD TO TAIL",3.2),("0.9-1.1","M","HEIGHT AT SHOULDER",1.2),("190-260","KG","WEIGHT",270)]
        lo_hi=[(2.8,3.1),(0.9,1.1),(190,260)]
        for i,(num,unit,lab,mx) in enumerate(cols):
            q=eo3(seg(t,1.7+i*0.55,2.3+i*0.55)); cx=90+i*312
            d.text((cx,y+118),num,font=F("Anton-Regular.ttf",66),fill=CREAM+(int(255*q),),anchor="ls")
            d.text((cx+d.textlength(num,font=F("Anton-Regular.ttf",66))+8,y+118),unit,font=F("BarlowCondensed-SemiBold.ttf",34),fill=GOLD+(int(255*q),),anchor="ls")
            d.text((cx,y+150),lab,font=F("BarlowCondensed-Medium.ttf",25),fill=GREY+(int(240*q),),anchor="ls")
            rbar(d,cx,cx+270,y+166,lo_hi[i][0],lo_hi[i][1],mx,GOLD,A*q,eo3(seg(t,2.0+i*0.55,3.2+i*0.55)),hh=14)
        d.text((W/2,y+216),"Source: Wikipedia (Bengal tiger). Varies by region and animal.",font=F("BarlowCondensed-Medium.ttf",23),fill=GREY+(int(220*A),),anchor="ms")
    # rare behaviour chips (13.4-18.9) + territory marking fact (19.4-26)
    if 13.6<=t<19.2:
        A=eo3(seg(t,13.6,14.1))*(1-seg(t,18.9,19.2)); y=by+30
        d.text((W/2,y+36),"RARE TO CATCH ON CAMERA",font=F("BarlowCondensed-SemiBold.ttf",40),fill=GOLD+(int(240*A),),anchor="ms")
        for i,lab in enumerate(("MATING","TERRITORIAL FIGHTS")):
            wd=[280,520][i]; x0=60+(960-800-20)/2+sum([280,520][:i])+i*20; q=eo3(seg(t,14.3+i*0.35,14.8+i*0.35)); yy_=y+70+int((1-q)*40)
            d.rounded_rectangle((x0,yy_,x0+wd,yy_+104),radius=52,outline=GOLD+(int(255*q),),width=4,fill=(14,16,20,int(210*q)))
            d.text((x0+wd/2,yy_+70),lab,font=F("BarlowCondensed-SemiBold.ttf",52),fill=CREAM+(int(255*q),),anchor="ms")
        d.text((W/2,y+226),"Moments you wait years for.",font=F("BarlowCondensed-Medium.ttf",30),fill=GREY+(int(235*A),),anchor="ms")
    if 19.5<=t<26.0:
        A=eo3(seg(t,19.5,20.0))*(1-seg(t,25.7,26.0)); y=by+14+int((1-eo3(seg(t,19.5,20.1)))*50); panel(y,226,A,CYAN)
        d.text((90,y+54),"TERRITORY MARKING",font=F("BarlowCondensed-SemiBold.ttf",40),fill=CYAN+(int(255*A),),anchor="ls")
        ff=F("Barlow-Medium.ttf",33)
        for j,l in enumerate(("Tigers mark their territory by spraying scent","on trees and bushes. It tells rivals who lives here.")): d.text((90,y+108+j*44),l,font=ff,fill=CREAM+(int(245*A),),anchor="ls")
        d.text((90,y+200),"General behaviour, not specific to this tiger.",font=F("BarlowCondensed-Medium.ttf",26),fill=GREY+(int(230*A),),anchor="ls")
    # leopard comparison card (26.6-30.3)
    if 26.7<=t<30.3:
        A=eo3(seg(t,26.7,27.2))*(1-seg(t,29.9,30.3)); y=by+4+int((1-eo3(seg(t,26.7,27.3)))*50); panel(y,238,A)
        d.text((90,y+36),"SIZE CHECK",font=F("BarlowCondensed-SemiBold.ttf",32),fill=CREAM+(int(255*A),),anchor="ls")
        d.ellipse((260,y+18,276,y+34),fill=GOLD+(int(255*A),)); d.text((286,y+35),"TIGER",font=F("BarlowCondensed-SemiBold.ttf",28),fill=GOLD+(int(255*A),),anchor="ls")
        d.ellipse((400,y+18,416,y+34),fill=CYAN+(int(255*A),)); d.text((426,y+35),"LEOPARD",font=F("BarlowCondensed-SemiBold.ttf",28),fill=CYAN+(int(255*A),),anchor="ls")
        d.text((W-90,y+35),"ADULT MALES, APPROX. WIKIPEDIA, WWF INDIA",font=F("BarlowCondensed-Medium.ttf",24),fill=GREY+(int(230*A),),anchor="rs")
        rows=[("LENGTH","HEAD TO TAIL",(2.8,3.1),(2.0,2.3),3.2,"2.8-3.1 M","2.0-2.3 M"),("HEIGHT","AT SHOULDER",(0.9,1.1),(0.45,0.8),1.2,"0.9-1.1 M","0.45-0.8 M"),("WEIGHT","",(190,260),(50,75),270,"190-260 KG","50-75 KG")]
        for i,(lb,sb,tg,lp,mx,tt_,lt_) in enumerate(rows):
            yy_=y+50+i*58; q=eo3(seg(t,27.1+i*0.4,27.6+i*0.4)); pp=eo3(seg(t,27.3+i*0.4,28.3+i*0.4))
            d.text((90,yy_+22),lb,font=F("BarlowCondensed-SemiBold.ttf",30),fill=CREAM+(int(255*q),),anchor="ls")
            if sb: d.text((90,yy_+46),sb,font=F("BarlowCondensed-Medium.ttf",20),fill=GREY+(int(230*q),),anchor="ls")
            rbar(d,260,700,yy_+3,tg[0],tg[1],mx,GOLD,A*q,pp,hh=14); rbar(d,260,700,yy_+27,lp[0],lp[1],mx,CYAN,A*q,pp,hh=14)
            d.text((W-90,yy_+20),tt_,font=F("BarlowCondensed-SemiBold.ttf",28),fill=GOLD+(int(255*q),),anchor="rs"); d.text((W-90,yy_+46),lt_,font=F("BarlowCondensed-SemiBold.ttf",28),fill=CYAN+(int(255*q),),anchor="rs")
    # three chips (30.4-35.0)
    if 30.5<=t<35.1:
        A=eo3(seg(t,30.5,31.0))*(1-seg(t,34.8,35.1)); y=by+22
        d.text((W/2,y+40),"WHAT A TREE GIVES YOU",font=F("BarlowCondensed-SemiBold.ttf",40),fill=GOLD+(int(240*A),),anchor="ms")
        labs=["CLEAN BACKGROUND","MULTIPLE ANGLES","CREATIVE COMPOSITION"]; ws=[330,300,380]; tot=sum(ws)+2*14; x0=(W-tot)/2
        for i,lab in enumerate(labs):
            q=eo3(seg(t,31.2+i*0.7,31.7+i*0.7)); yy_=y+78+int((1-q)*40)
            d.rounded_rectangle((x0,yy_,x0+ws[i],yy_+96),radius=48,outline=CYAN+(int(255*q),),width=4,fill=(14,16,20,int(210*q)))
            d.text((x0+ws[i]/2,yy_+62),lab,font=F("BarlowCondensed-SemiBold.ttf",36),fill=CREAM+(int(255*q),),anchor="ms"); x0+=ws[i]+14
        d.text((W/2,y+226),"The leopard's frames: higher, cleaner, different.",font=F("BarlowCondensed-Medium.ttf",30),fill=GREY+(int(235*A),),anchor="ms")
    # tree life (36-45.5)
    if 36.0<=t<45.6:
        A=eo3(seg(t,36.0,36.5))*(1-seg(t,45.2,45.6)); y=by+14+int((1-eo3(seg(t,36.0,36.6)))*50); panel(y,226,A,CYAN)
        d.text((90,y+54),"LEOPARD: TREE LIFE",font=F("BarlowCondensed-SemiBold.ttf",40),fill=CYAN+(int(255*A),),anchor="ls")
        ff=F("Barlow-Medium.ttf",33)
        for j,l in enumerate(("Leopards often rest and feed up in trees,","out of sight and out of reach of larger predators.")): d.text((90,y+108+j*44),l,font=ff,fill=CREAM+(int(245*A),),anchor="ls")
        d.text((90,y+200),"General behaviour, not specific to this leopard.",font=F("BarlowCondensed-Medium.ttf",26),fill=GREY+(int(230*A),),anchor="ls")
    # payoff
    if t>=47.4:
        A=eo3(seg(t,47.4,47.9)); y=by+40
        d.text((W/2,y+50),"TIGER OR LEOPARD?",font=F("Anton-Regular.ttf",72),fill=CREAM+(int(250*A),),anchor="ms")
        for i,(lab,col) in enumerate((("TIGER",GOLD),("LEOPARD",CYAN))):
            wd=[290,360][i]; x0=W/2-330+sum([290,360][:i])+i*30; q=eo3(seg(t,47.9+i*0.2,48.4+i*0.2)); yy_=y+96+int((1-q)*40)
            d.rounded_rectangle((x0,yy_,x0+wd,yy_+90),radius=45,outline=col+(int(255*q),),width=4,fill=(14,16,20,int(210*q)))
            d.text((x0+wd/2,yy_+62),lab,font=F("BarlowCondensed-SemiBold.ttf",48),fill=col+(int(255*q),),anchor="ms")
        d.text((W/2,y+236),"COMMENT YOUR WINNER",font=F("BarlowCondensed-Medium.ttf",32),fill=GREY+(int(240*A),),anchor="ms")
    if t>=51.5:
        A=eo3(seg(t,51.6,52.0)); cy=WY+int(930*WH/1280)
        d.text((W/2,cy-8),"WHO WON?",font=F("Anton-Regular.ttf",64),fill=RED+(int(255*A),),anchor="ms")
        d.text((W/2,cy+48),"COMMENT YOUR ANSWER",font=F("BarlowCondensed-SemiBold.ttf",44),fill=CREAM+(int(255*A),),anchor="ms")
    out=np.array(img).astype(np.float32)*VIG
    out+=cv2.resize(GR[int(t*30)%6],(W,H))[...,None]*5.0
    for h in HITS:
        dd=t-h
        if 0<=dd<0.16 and h>0: out+=(1-dd/0.16)*26
    f=min(1,t/0.2)*min(1,(TOTAL-t)/0.35); out*=f
    return np.clip(out,0,255).astype(np.uint8)
