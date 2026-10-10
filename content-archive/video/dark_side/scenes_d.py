import numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont
FD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/fonts/"
HD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/dark/"
W,H=1080,1920; TOTAL=29.95
GOLD=(255,200,70); CYAN=(80,225,235); RED=(255,84,70); CREAM=(250,246,236); GREY=(170,176,182)
def F(n,s): return ImageFont.truetype(FD+n,s)
def ease(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def eo3(x): x=min(1,max(0,x)); return 1-(1-x)**3
def seg(t,a,b): return min(1,max(0,(t-a)/(b-a)))
def lerp(a,b,x): return a+(b-a)*x
WX,WY,WW,WH=162,300,756,1344
_fc={}
def src(i):
    i=max(1,min(899,i))
    if i not in _fc:
        if len(_fc)>40: _fc.pop(next(iter(_fc)))
        _fc[i]=cv2.cvtColor(cv2.imread(HD+f"f/f_{i:04d}.jpg"),cv2.COLOR_BGR2RGB)
    return _fc[i]
# rounded mask
MASK=np.zeros((WH,WW),np.uint8); cv2.rectangle(MASK,(28,0),(WW-29,WH-1),255,-1); cv2.rectangle(MASK,(0,28),(WW-1,WH-29),255,-1)
for cx,cy in ((28,28),(WW-29,28),(28,WH-29),(WW-29,WH-29)): cv2.circle(MASK,(cx,cy),28,255,-1,cv2.LINE_AA)
MASKF=(cv2.GaussianBlur(MASK,(0,0),0.8).astype(np.float32)/255)[...,None]
yy,xx=np.mgrid[0:H,0:W]; VIG=(1-0.42*(((xx-W/2)/(W/2))**2*0.6+((yy-H/2)/(H/2))**2*0.9)).clip(0.5,1)[...,None].astype(np.float32)
rng=np.random.default_rng(5)
GR=[rng.normal(0,1,(H//2,W//2)).astype(np.float32) for _ in range(6)]
# beats: t0,t1,kicker,headline
BEATS=[(0,3.0,"THE DARK SIDE OF","WILDLIFE TOURISM"),
       (3.0,10.2,"01  THE SHOT","ALL YOU SEE IS THE FRAME"),
       (10.2,17.3,"02  THE CROWD","ONE SIGHTING. MANY VEHICLES."),
       (17.3,23.0,"03  THE MOMENT","THEN YOU LOOK UP"),
       (23.0,28.6,"04  THE REALISATION","WE KNOW WHERE THE LINE IS"),
       (28.6,TOTAL+1,"05  YOUR TURN","WHERE IS YOUR LINE?")]
HITS=[b[0] for b in BEATS]+[28.85]
def beat_of(t):
    for i,b in enumerate(BEATS):
        if b[0]<=t<b[1]: return i
    return len(BEATS)-1
def fit(draw,text,fontname,size,maxw):
    while True:
        f=F(fontname,size)
        w=draw.textlength(text,font=f)
        if w<=maxw or size<30: return f,w
        size-=3
def spaced(draw,xy,text,font,fill,sp=6,anchor_c=True):
    ws=[draw.textlength(c,font=font) for c in text]; tot=sum(ws)+sp*(len(text)-1); x=xy[0]-tot/2 if anchor_c else xy[0]
    for c,w in zip(text,ws): draw.text((x,xy[1]),c,font=font,fill=fill,anchor="ls"); x+=w+sp
    return tot
def wrap(draw,text,font,maxw):
    out=[];cur=""
    for w in text.split():
        tr=(cur+" "+w).strip()
        if draw.textlength(tr,font=font)<=maxw: cur=tr
        else: out.append(cur);cur=w
    out.append(cur); return out
CARDS=[(10.3,13.7,"TADOBA ANDHARI  ·  MAY 2024","10 guides and 10 safari vehicles suspended for a month after a tiger's movement was blocked.","REPORTED BY DECCAN HERALD"),
       (13.7,17.2,"UMRED-PAUNI-KARHANDLA  ·  DEC 2024","Vehicles crowded a tigress with her cubs. Drivers and guides suspended for 3 months, tourists banned.","REPORTED BY THE HITAVADA")]
def frame(t):
    n=int(t*30)+1; fr=src(n)
    win=cv2.resize(fr,(WW,WH),interpolation=cv2.INTER_CUBIC)
    bi=beat_of(t); b=BEATS[bi]; lt=t-b[0]
    # beat punch (window scale)
    pk=0.0
    for h in HITS:
        d=t-h
        if 0<=d<0.5: pk=max(pk,(1-d/0.5)**2)
    # bg
    bg=cv2.resize(fr,(W,H),interpolation=cv2.INTER_LINEAR); bg=cv2.GaussianBlur(bg,(0,0),38)
    base=(bg.astype(np.float32)*0.30)
    # gold tint wash per beat color
    # window grade
    w=win.astype(np.float32); w=(w-128)*1.06+128; g=w.mean(2,keepdims=True); w=g+(w-g)*1.08
    sc=1+0.012*pk
    if sc>1.0005:
        M=np.array([[sc,0,(1-sc)*WW/2],[0,sc,(1-sc)*WH/2]],np.float32); w=cv2.warpAffine(w,M,(WW,WH),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    # shadow
    sh=np.zeros((H,W),np.float32); sh[WY:WY+WH,WX:WX+WW]=1; sh=cv2.GaussianBlur(sh,(0,0),26)[...,None]; base=base*(1-0.5*sh)
    reg=base[WY:WY+WH,WX:WX+WW]; base[WY:WY+WH,WX:WX+WW]=reg*(1-MASKF)+w*MASKF
    img=Image.fromarray(np.clip(base,0,255).astype(np.uint8)); d=ImageDraw.Draw(img,"RGBA")
    # window border
    d.rounded_rectangle((WX-2,WY-2,WX+WW+1,WY+WH+1),radius=30,outline=GOLD+(150,),width=2)
    # chapter ticks
    sx=70; ex=W-70; nseg=5; gap=10; sw=(ex-sx-gap*(nseg-1))/nseg
    for i in range(nseg):
        x0=sx+i*(sw+gap); b0=BEATS[i+1][0] if i+1<len(BEATS) else 0
        d.rounded_rectangle((x0,60,x0+sw,66),radius=3,fill=(255,255,255,50))
        s0=BEATS[i][0]; s1=BEATS[i][1] if i<4 else TOTAL
        p=seg(t,s0,s1)
        if p>0: d.rounded_rectangle((x0,60,x0+sw*p,66),radius=3,fill=GOLD+(255,))
    # top text
    a=eo3(seg(lt,0.05,0.4)); ex_=1-seg(b[1]-t,0,0.0) if False else 1
    fo=1-seg(t,b[1]-0.18,b[1]) if bi<len(BEATS)-1 else 1
    al=int(255*a*fo)
    kf=F("BarlowCondensed-SemiBold.ttf",38); spaced(d,(W/2,130+int((1-a)*18)),b[2],kf,GOLD+(al,),sp=9)
    hf,hw=fit(d,b[3],"Anton-Regular.ttf",104,W-110)
    # slight slide-in
    dy=int((1-eo3(seg(lt,0.05,0.5)))*40)
    tx=W/2-hw/2
    d.text((W/2+3,238+dy+4),b[3],font=hf,fill=(0,0,0,int(160*a*fo)),anchor="ms")
    d.text((W/2,238+dy),b[3],font=hf,fill=CREAM+(al,),anchor="ms")
    # bottom graphics
    by=WY+WH+16   # 1660
    brand=F("BarlowCondensed-Medium.ttf",30)
    # focus / awareness bars  (3-10.2 and 17.3-23)
    if (3.0<=t<10.4) or (17.3<=t<23.3):
        ap=eo3(seg(t,3.2,3.7)) if t<12 else 1
        if t>=17.3: ap=eo3(seg(t,17.3,17.8))
        fade_out=1-seg(t,10.0,10.4) if t<12 else 1-seg(t,23.0,23.3)
        A=ap*fade_out
        focus=lerp(0.18,0.96,eo3(seg(t,3.2,9.5))) if t<12 else 0.96-0.0*seg(t,17,23)
        aware=0.14+0.04*math.sin(t*2) if t<12 else lerp(0.14,0.9,ease(seg(t,18.55,22.4)))
        if t>=17.3 and t<=18.5: aware=0.14
        y0=by+40
        for k,(lab,val,col) in enumerate((("FOCUS ON THE SHOT",focus,GOLD),("AWARENESS OF THE ANIMAL",aware,CYAN))):
            yy_=y0+k*86
            d.text((90,yy_),lab,font=F("BarlowCondensed-SemiBold.ttf",34),fill=CREAM+(int(235*A),),anchor="ls")
            d.text((W-90,yy_),f"{int(val*100)}%",font=F("BarlowCondensed-SemiBold.ttf",34),fill=col+(int(235*A),),anchor="rs")
            d.rounded_rectangle((90,yy_+14,W-90,yy_+30),radius=8,fill=(255,255,255,int(40*A)))
            d.rounded_rectangle((90,yy_+14,90+(W-180)*val,yy_+30),radius=8,fill=col+(int(255*A),))
        d.text((W/2,by+208),"ILLUSTRATION OF THE STORY, NOT MEASURED DATA",font=F("BarlowCondensed-Medium.ttf",24),fill=GREY+(int(200*A),),anchor="ms")
    # case cards
    for (c0,c1,hd,body,srcn) in CARDS:
        if c0<=t<c1:
            p=eo3(seg(t,c0,c0+0.45)); q=1-seg(t,c1-0.25,c1); A=p*q; dy=int((1-p)*50)
            y=by+24+dy
            d.rounded_rectangle((70,y,W-70,y+196),radius=22,fill=(14,16,20,int(215*A)),outline=RED+(int(220*A),),width=3)
            d.rectangle((70,y+22,78,y+174),fill=RED+(int(255*A),))
            d.text((104,y+46),hd,font=F("BarlowCondensed-SemiBold.ttf",34),fill=RED+(int(255*A),),anchor="ls")
            bf=F("Barlow-Medium.ttf",33)
            for i,l in enumerate(wrap(d,body,bf,W-104-100)[:3]): d.text((104,y+92+i*38),l,font=bf,fill=CREAM+(int(245*A),),anchor="ls")
            d.text((W-100,y+46),srcn,font=F("BarlowCondensed-Medium.ttf",24),fill=GREY+(int(230*A),),anchor="rs")
    if 10.3<=t<17.2:
        A=eo3(seg(t,10.3,10.8))*(1-seg(t,16.9,17.2))
        d.text((W/2,by+14),"RECENT CASES, NOT FROM THIS FOOTAGE",font=F("BarlowCondensed-SemiBold.ttf",26),fill=GOLD+(int(230*A),),anchor="ms")
    # line gauge 23.3-29.95
    if t>=23.0:
        A=eo3(seg(t,23.0,23.6)); xL,xR=120,W-120; yc=by+78; mid=W/2
        d.rounded_rectangle((xL,yc-6,mid,yc+6),radius=6,fill=CYAN+(int(110*A),))
        d.rounded_rectangle((mid,yc-6,xR,yc+6),radius=6,fill=RED+(int(110*A),))
        d.text((xL,yc-40),"OBSERVE",font=F("BarlowCondensed-SemiBold.ttf",34),fill=CYAN+(int(240*A),),anchor="ls")
        d.text((xR,yc-40),"DISTURB",font=F("BarlowCondensed-SemiBold.ttf",34),fill=RED+(int(240*A),),anchor="rs")
        for yy_ in range(int(yc-46),int(yc+48),14): d.line((mid,yy_,mid,yy_+7),fill=CREAM+(int(230*A),),width=4)
        d.text((mid,yc+80),"THE LINE",font=F("BarlowCondensed-SemiBold.ttf",30),fill=CREAM+(int(230*A),),anchor="ms")
        # marker
        cross=seg(t,28.85,29.15)
        mx=lerp(xL+40,mid-26,ease(seg(t,23.4,28.7)))
        mx=lerp(mx,mid+150,ease(cross)) if t>=28.85 else mx+2.5*math.sin(t*5)*seg(t,25,28.7)
        col=RED if t>=28.95 else CREAM
        r=20+int(6*math.sin(t*6)) if t<28.85 else 24
        if t>=28.85:
            ring=seg(t,28.85,29.6)
            d.ellipse((mx-30-ring*80,yc-30-ring*80,mx+30+ring*80,yc+30+ring*80),outline=RED+(int(220*(1-ring)),),width=4)
            d.text((W/2,yc+134),"LINE CROSSED",font=F("Anton-Regular.ttf",44),fill=RED+(int(255*eo3(seg(t,28.95,29.25))),),anchor="ms")
        d.ellipse((mx-r,yc-r,mx+r,yc+r),fill=col+(255,),outline=(0,0,0,200),width=3)
    # brand
    if t<3.0 or t>=29.0:
        pass
    sp=spaced(d,(W-70-0,H-34),"",brand,GOLD+(0,)) if False else 0
    d.text((W/2,42),"THE NATURAL ANGLE",font=brand,fill=(255,255,255,170),anchor="ms")
    # first beat chip
    if t<3.3:
        A=eo3(seg(t,0.4,0.9))*(1-seg(t,3.0,3.3)); y=by+60
        d.rounded_rectangle((W/2-250,y,W/2+250,y+78),radius=39,fill=GOLD+(int(235*A),))
        d.text((W/2,y+53),"A FIRST-PERSON ACCOUNT",font=F("BarlowCondensed-SemiBold.ttf",42),fill=(20,16,8,int(255*A)),anchor="ms")
    out=np.array(img).astype(np.float32)
    # vignette + grain + dust
    out*=VIG
    gi=GR[n%6]; gi=cv2.resize(gi,(W,H),interpolation=cv2.INTER_LINEAR); out+=gi[...,None]*5.0
    # transition flash
    for h in HITS:
        dd=t-h
        if 0<=dd<0.18: out+=(1-dd/0.18)*28
    # crossing: red pulse
    if 28.85<=t<29.6: out[...,0]+=(1-(t-28.85)/0.75)*40*(1-(t-28.85)/0.75)
    # fade in/out
    f=min(1,t/0.25)*min(1,(TOTAL-t)/0.3)
    out*=f
    return np.clip(out,0,255).astype(np.uint8)
