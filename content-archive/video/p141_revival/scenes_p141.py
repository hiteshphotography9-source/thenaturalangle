import numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont
FD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/fonts/"
HD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/p141/"
W,H=1080,1920; OFF=1.5; TOTAL=46.4
GOLD=(255,200,70); CYAN=(80,225,235); RED=(255,84,70); CREAM=(250,246,236); GREY=(170,176,182)
def F(n,s): return ImageFont.truetype(FD+n,s)
def ease(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def eo3(x): x=min(1,max(0,x)); return 1-(1-x)**3
def seg(t,a,b): return min(1,max(0,(t-a)/(b-a)))
def lerp(a,b,x): return a+(b-a)*x
WX,WY,WW,WH=162,300,756,1344
_fc={}
def src(i):
    i=max(1,min(1348,i))
    if i not in _fc:
        if len(_fc)>40: _fc.pop(next(iter(_fc)))
        _fc[i]=cv2.cvtColor(cv2.imread(HD+f"f/f_{i:04d}.jpg"),cv2.COLOR_BGR2RGB)
    return _fc[i]
MASK=np.zeros((WH,WW),np.uint8); cv2.rectangle(MASK,(28,0),(WW-29,WH-1),255,-1); cv2.rectangle(MASK,(0,28),(WW-1,WH-29),255,-1)
for cx,cy in ((28,28),(WW-29,28),(28,WH-29),(WW-29,WH-29)): cv2.circle(MASK,(cx,cy),28,255,-1,cv2.LINE_AA)
MASKF=(cv2.GaussianBlur(MASK,(0,0),0.8).astype(np.float32)/255)[...,None]
yy,xx=np.mgrid[0:H,0:W]; VIG=(1-0.42*(((xx-W/2)/(W/2))**2*0.6+((yy-H/2)/(H/2))**2*0.9)).clip(0.5,1)[...,None].astype(np.float32)
rng=np.random.default_rng(9); GR=[rng.normal(0,1,(H//2,W//2)).astype(np.float32) for _ in range(6)]
_m=cv2.imread(HD+"mapchip.png"); MAPC=cv2.cvtColor(cv2.resize(_m,(200,200),interpolation=cv2.INTER_AREA),cv2.COLOR_BGR2RGB)
CM=np.zeros((200,200),np.uint8); cv2.circle(CM,(100,100),98,255,-1,cv2.LINE_AA); CMF=(cv2.GaussianBlur(CM,(0,0),0.8).astype(np.float32)/255)[...,None]
DOT=(130.2*200/260,107.3*200/260)
BEATS=[(0,OFF,"PANNA TIGER RESERVE","15 FEET FROM P-141"),
       (OFF,11.7,"01  THE GLIMPSE","A FLASH OF STRIPES"),
       (11.7,30.5,"02  HIDDEN IN PLAIN SIGHT","SHE WAS RIGHT THERE"),
       (30.5,40.0,"03  THE WAIT","THEN, SILENCE"),
       (40.0,TOTAL+1,"04  THE PAYOFF","AND THEN SHE WALKED OUT")]
HITS=[b[0] for b in BEATS]
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
    if t<OFF:
        o=42.0+t; zoom=1.0+0.06*(t/OFF); fr=src(int(o*30)+1); h,w=fr.shape[:2]
        M=np.array([[zoom,0,(1-zoom)*w/2],[0,zoom,(1-zoom)*h/2]],np.float32)
        return cv2.warpAffine(fr,M,(w,h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT),o
    o=t-OFF; return src(int(o*30)+1),o
def card(d,img,y,A,head,lines,srcn,col=GOLD,h=226):
    d.rounded_rectangle((70,y,W-70,y+h),radius=22,fill=(14,16,20,int(220*A)),outline=col+(int(220*A),),width=3)
    d.rectangle((70,y+22,78,y+h-22),fill=col+(int(255*A),))
    d.text((104,y+50),head,font=F("BarlowCondensed-SemiBold.ttf",36),fill=col+(int(255*A),),anchor="ls")
    d.text((W-100,y+50),srcn,font=F("BarlowCondensed-Medium.ttf",24),fill=GREY+(int(230*A),),anchor="rs")
    bf=F("Barlow-Medium.ttf",33)
    for i,l in enumerate(lines): d.text((104,y+98+i*40),l,font=bf,fill=CREAM+(int(245*A),),anchor="ls")
def frame(t):
    fr,o=orig_frame(t); win=cv2.resize(fr,(WW,WH),interpolation=cv2.INTER_CUBIC)
    bi=beat_of(t); b=BEATS[bi]; lt=t-b[0]; pk=0.0
    for h in HITS+[OFF+0.0]:
        dd=t-h
        if 0<=dd<0.5: pk=max(pk,(1-dd/0.5)**2)
    bg=cv2.GaussianBlur(cv2.resize(fr,(W,H),interpolation=cv2.INTER_LINEAR),(0,0),38); base=bg.astype(np.float32)*0.30
    w=win.astype(np.float32); w=(w-128)*1.06+128; g=w.mean(2,keepdims=True); w=g+(w-g)*1.08
    sc=1+0.012*pk
    if sc>1.0005:
        M=np.array([[sc,0,(1-sc)*WW/2],[0,sc,(1-sc)*WH/2]],np.float32); w=cv2.warpAffine(w,M,(WW,WH),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    sh=np.zeros((H,W),np.float32); sh[WY:WY+WH,WX:WX+WW]=1; sh=cv2.GaussianBlur(sh,(0,0),26)[...,None]; base=base*(1-0.5*sh)
    reg=base[WY:WY+WH,WX:WX+WW]; base[WY:WY+WH,WX:WX+WW]=reg*(1-MASKF)+w*MASKF
    img=Image.fromarray(np.clip(base,0,255).astype(np.uint8)); d=ImageDraw.Draw(img,"RGBA")
    d.rounded_rectangle((WX-2,WY-2,WX+WW+1,WY+WH+1),radius=30,outline=GOLD+(150,),width=2)
    sx=70; ex=W-70; nseg=4; gap=10; sw=(ex-sx-gap*(nseg-1))/nseg
    d.text((W/2,42),"THE NATURAL ANGLE",font=F("BarlowCondensed-Medium.ttf",30),fill=(255,255,255,170),anchor="ms")
    for i in range(nseg):
        x0=sx+i*(sw+gap); d.rounded_rectangle((x0,60,x0+sw,66),radius=3,fill=(255,255,255,50))
        s0=BEATS[i+1][0]; s1=BEATS[i+2][0] if i+2<len(BEATS) else TOTAL
        p=seg(t,s0,s1)
        if p>0: d.rounded_rectangle((x0,60,x0+sw*p,66),radius=3,fill=GOLD+(255,))
    a=eo3(seg(lt,0.05,0.4)); fo=1-seg(t,b[1]-0.18,b[1]) if bi<len(BEATS)-1 else 1; al=int(255*a*fo)
    spaced(d,(W/2,130+int((1-a)*18)),b[2],F("BarlowCondensed-SemiBold.ttf",38),GOLD+(al,),sp=9)
    hf=fit(d,b[3],"Anton-Regular.ttf",104,W-110); dy=int((1-eo3(seg(lt,0.05,0.5)))*40)
    d.text((W/2+3,238+dy+4),b[3],font=hf,fill=(0,0,0,int(160*a*fo)),anchor="ms"); d.text((W/2,238+dy),b[3],font=hf,fill=CREAM+(al,),anchor="ms")
    by=WY+WH+16
    # B1 bottom: location chip
    if OFF+0.4<=t<OFF+9.9:
        A=eo3(seg(t,OFF+0.4,OFF+0.9))*(1-seg(t,OFF+9.6,OFF+9.9)); y=by+50
        d.rounded_rectangle((90,y,W-90,y+96),radius=48,fill=(14,16,20,int(220*A)),outline=GOLD+(int(200*A),),width=3)
        blink=0.5+0.5*math.sin(t*6); d.ellipse((130,y+36,154,y+60),fill=RED+(int(255*A*(0.4+0.6*blink)),))
        d.text((180,y+62),"PANNA TIGER RESERVE, MADHYA PRADESH",font=F("BarlowCondensed-SemiBold.ttf",44),fill=CREAM+(int(250*A),),anchor="ls")
        d.text((W/2,y+150),"FILMED FROM A SAFARI GYPSY",font=F("BarlowCondensed-Medium.ttf",32),fill=GREY+(int(230*A),),anchor="ms")
    # ID card (orig 12.4-19.4)
    c0,c1=12.4+OFF,19.6+OFF
    if c0<=t<c1:
        A=eo3(seg(t,c0,c0+0.5))*(1-seg(t,c1-0.3,c1)); dy2=int((1-eo3(seg(t,c0,c0+0.6)))*50); y=by+14+dy2
        d.rounded_rectangle((70,y,W-70,y+226),radius=22,fill=(14,16,20,int(220*A)),outline=GOLD+(int(220*A),),width=3)
        img.paste(Image.fromarray(MAPC),(96,y+13),Image.fromarray((CMF[...,0]*255*A).astype(np.uint8))); d=ImageDraw.Draw(img,"RGBA")
        px,py=96+DOT[0],y+13+DOT[1]; pr=int(7+5*math.sin(t*5)); ring=((t*1.4)%1)
        d.ellipse((px-pr*0.6,py-pr*0.6,px+pr*0.6,py+pr*0.6),fill=RED+(int(255*A),)); d.ellipse((px-10-ring*28,py-10-ring*28,px+10+ring*28,py+10+ring*28),outline=RED+(int(200*(1-ring)*A),),width=3)
        d.text((330,y+84),"P-141",font=F("Anton-Regular.ttf",90),fill=GOLD+(int(255*A),),anchor="ls")
        d.text((330,y+130),"TIGRESS  ·  PANNA TIGER RESERVE",font=F("BarlowCondensed-SemiBold.ttf",38),fill=CREAM+(int(250*A),),anchor="ls")
        d.text((330,y+170),"Daughter of T-1, a tigress from the",font=F("Barlow-Medium.ttf",30),fill=CREAM+(int(235*A),),anchor="ls")
        d.text((330,y+206),"reintroduction project (The Hitavada)",font=F("Barlow-Medium.ttf",30),fill=CREAM+(int(235*A),),anchor="ls")
    # litter card (orig 20.2-28.8)
    c0,c1=20.2+OFF,29.0+OFF
    if c0<=t<c1:
        A=eo3(seg(t,c0,c0+0.5))*(1-seg(t,c1-0.3,c1)); dy2=int((1-eo3(seg(t,c0,c0+0.6)))*50); y=by+14+dy2
        d.rounded_rectangle((70,y,W-70,y+226),radius=22,fill=(14,16,20,int(220*A)),outline=GOLD+(int(220*A),),width=3)
        d.text((104,y+50),"HER LITTERS  ·  REPORTED",font=F("BarlowCondensed-SemiBold.ttf",36),fill=GOLD+(int(255*A),),anchor="ls")
        d.text((W-100,y+50),"THE HITAVADA, OCT 2024",font=F("BarlowCondensed-Medium.ttf",24),fill=GREY+(int(230*A),),anchor="rs")
        for i in range(10):
            q=eo3(seg(t,c0+0.5+i*0.12,c0+0.8+i*0.12)); cx=124+i*60 if i<6 else 124+i*60+30; cy=y+110
            col=(150,156,162) if i<6 else GOLD
            d.ellipse((cx-22,cy-22,cx+22,cy+22),fill=col+(int(255*A*q),),outline=(0,0,0,int(160*A*q)),width=2)
        d.text((124+0,y+176),"6 CUBS, 3 LITTERS",font=F("BarlowCondensed-SemiBold.ttf",32),fill=GREY+(int(240*A),),anchor="ls")
        d.text((124+6*60+30,y+176),"4 CUBS, 4TH LITTER",font=F("BarlowCondensed-SemiBold.ttf",32),fill=GOLD+(int(250*A),),anchor="ls")
        d.text((104,y+212),"Four cubs born Oct 2024. Cubs shown are counts, not photos.",font=F("BarlowCondensed-Medium.ttf",26),fill=GREY+(int(220*A),),anchor="ls")
    # B3: listening flatline
    if 30.9+OFF-OFF*0<=t<39.6:
        A=eo3(seg(t,31.0,31.5))*(1-seg(t,39.2,39.6)); y=by+70
        d.text((W/2,y),"LISTENING",font=F("BarlowCondensed-SemiBold.ttf",42),fill=GOLD+(int(240*A),),anchor="ms")
        pts=[]
        for i in range(0,880,6):
            xx_=100+i; amp=2+ (24*math.exp(-((i-440+ (t*180)%900-450)**2)/2000.0) if False else 0)
            yy_=y+80+3*math.sin(i*0.05+t*3)*(0.4+0.6*(1 if (i/880) < seg(t,31,39) else 0))
            pts.append((xx_,yy_))
        d.line(pts,fill=CYAN+(int(210*A),),width=4)
        d.text((W/2,y+150),"WAITING FOR HER TO MOVE",font=F("BarlowCondensed-Medium.ttf",32),fill=GREY+(int(230*A),),anchor="ms")
    # B4 payoff chip
    if t>=40.2:
        A=eo3(seg(t,40.2,40.8)); y=by+36
        d.text((W/2,y+50),"WORTH THE WAIT?",font=F("Anton-Regular.ttf",70),fill=CREAM+(int(250*A),),anchor="ms")
        for i,(lab,col) in enumerate((("YES",GOLD),("OF COURSE",CYAN))):
            wd=[230,360][i]; x0=W/2-300+sum([230,360][:i])+i*20; q=eo3(seg(t,40.6+i*0.15,41.1+i*0.15)); yy_=y+90+int((1-q)*40)
            d.rounded_rectangle((x0,yy_,x0+wd,yy_+86),radius=43,outline=col+(int(255*q),),width=4,fill=(14,16,20,int(200*q)))
            d.text((x0+wd/2,yy_+58),lab,font=F("BarlowCondensed-SemiBold.ttf",44),fill=col+(int(255*q),),anchor="ms")
        d.text((W/2,y+228),"FOLLOW FOR MORE PANNA STORIES",font=F("BarlowCondensed-Medium.ttf",32),fill=GREY+(int(240*A),),anchor="ms")
    out=np.array(img).astype(np.float32)*VIG
    out+=cv2.resize(GR[int(t*30)%6],(W,H))[...,None]*5.0
    for h in HITS:
        dd=t-h
        if 0<=dd<0.18 and h>0: out+=(1-dd/0.18)*26
    f=min(1,t/0.2)*min(1,(TOTAL-t)/0.3); out*=f
    return np.clip(out,0,255).astype(np.uint8)
