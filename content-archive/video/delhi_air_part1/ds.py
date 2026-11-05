import numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920; FPS=25; TOTAL=90.0
FD='/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/fonts/'
def AN(s): return ImageFont.truetype(FD+'Anton-Regular.ttf',int(s))
def BC(s): return ImageFont.truetype(FD+'BarlowCondensed-SemiBold.ttf',int(s))
def BM(s): return ImageFont.truetype(FD+'Barlow-Medium.ttf',int(s))
ACC=(232,255,61); WHT=(255,255,255); CREAM=(250,243,228); ORG=(255,140,30); RED=(235,45,40); TEAL=(60,200,200); AMB=(255,190,70)
def cl(x): return min(1,max(0,x))
def seg(t,a,b): return cl((t-a)/(b-a)) if b>a else (1.0 if t>=a else 0.0)
def ease(x): x=cl(x); return x*x*(3-2*x)
def eo3(x): x=cl(x); return 1-(1-x)**3
def eob(x,k=1.7): x=cl(x); return 1+(k+1)*(x-1)**3+k*(x-1)**2
def lerp(a,b,x): return a+(b-a)*x
def lerpc(c0,c1,x): return tuple(lerp(a,b,x) for a,b in zip(c0,c1))
rng=np.random.default_rng(7)
# ---------------- precomputed
def noise_tex(h,w,sc,seed):
    r=np.random.default_rng(seed).random((max(2,h//sc),max(2,w//sc))).astype(np.float32)
    return cv2.resize(r,(w,h),interpolation=cv2.INTER_CUBIC)
HZ1=noise_tex(2600,1500,120,1); HZ2=noise_tex(2600,1500,60,2)
yy=np.linspace(0,1,H,dtype=np.float32)[:,None]
def grad(top,bot):
    t=np.array(top,np.float32)[None,None,:]; b=np.array(bot,np.float32)[None,None,:]
    return t+(b-t)*yy[...,None]*np.ones((1,W,1),np.float32)
R2=((np.arange(W)[None,:]-W/2)**2+(np.arange(H)[:,None]-H*0.55)**2).astype(np.float32)
SUNGLOW=np.exp(-R2/(2*260.0**2)); SUNDISC=(R2<150**2).astype(np.float32)
# skyline mask
def make_skyline():
    m=np.zeros((H,W),np.uint8); r=np.random.default_rng(11); x=0
    while x<W:
        w=int(r.integers(40,110)); h=int(r.integers(80,330)); cv2.rectangle(m,(x,1380-h),(x+w,1480),255,-1)
        if r.random()<0.25: cv2.rectangle(m,(x+w//2-6,1380-h-60),(x+w//2+6,1380-h),255,-1)
        x+=w-4
    # arch (India Gate like)
    cv2.rectangle(m,(430,1180),(650,1480),255,-1); cv2.rectangle(m,(480,1260),(600,1480),0,-1); cv2.ellipse(m,(540,1262),(60,50),0,180,360,255,-1)
    return m.astype(np.float32)/255
SKY=make_skyline()
REEDS=np.zeros((H,W),np.uint8)
for i in range(120):
    x=int(rng.integers(0,W)); h=int(rng.integers(180,520)); lean=int(rng.integers(-40,40))
    cv2.line(REEDS,(x,H),(x+lean,H-h),255,int(rng.integers(3,7)),cv2.LINE_AA)
    if rng.random()<0.4: cv2.ellipse(REEDS,(x+lean,H-h-20),(7,26),0,0,360,255,-1,cv2.LINE_AA)
REEDS=REEDS.astype(np.float32)/255
# ---------------- world (sky + skyline + water + reeds)
def world(t,haze,dusk=0.0):
    top=lerpc((40,85,130),(105,82,55),haze); hor=lerpc((245,185,125),(190,120,62),haze)
    sky=grad(top,hor)
    # sun
    sunc=lerpc((255,215,150),(215,80,45),haze); sa=lerp(1.0,0.55,haze)
    sky+=SUNGLOW[...,None]*np.array(sunc,np.float32)*0.55*sa
    sky=np.where(SUNDISC[...,None]>0,sky*(1-0.7*sa)+np.array(sunc,np.float32)*0.7*sa,sky)
    # drifting haze
    ox=int(t*14)%300; oy=int(t*6)%300
    hz=HZ1[oy:oy+H,ox:ox+W]*0.6+HZ2[oy+80:oy+80+H,ox+60:ox+60+W]*0.4
    ha=np.clip((hz-0.25)*1.6,0,1)*haze*0.85
    sky=sky*(1-ha[...,None])+np.array((170,140,95),np.float32)*ha[...,None]
    # skyline fades into haze
    sk=SKY*0.9; col=lerpc((25,30,40),(130,105,75),haze*0.8)
    sky=sky*(1-sk[...,None])+np.array(col,np.float32)*sk[...,None]
    # water
    wy=1480; wh=H-wy; ys=np.arange(wh,dtype=np.float32)[:,None]; xs=np.arange(W,dtype=np.float32)[None,:]
    rip=np.sin(xs*0.03+ys*0.12+t*1.4)*0.5+np.sin(xs*0.011-ys*0.09+t*0.9)*0.5
    base=sky[wy-300:wy-300+wh][::-1]*0.55 if False else None
    wcol=np.array(lerpc((35,80,95),(70,70,55),haze),np.float32)
    wat=wcol[None,None,:]*(0.75+0.25*(1-ys/wh))[...,None]+(rip[...,None]*12)+np.array(sunc,np.float32)*np.exp(-((xs-W/2)**2)/(2*110**2))[...,None]*(0.25+0.1*rip[...,None])*sa
    sky[wy:]=wat
    # reeds
    rr=REEDS[:,:,None]*np.array((10,14,12),np.float32)
    sky=sky*(1-REEDS[...,None]*0.92)+rr*0.92
    return sky
# ---------------- birds
def bird(mask,cx,cy,s,ph,thick=None):
    th=max(2,int(s*0.16)) if thick is None else thick
    f=math.sin(ph); wy=-s*0.55*f
    pts=[(cx-s,cy+wy*0.9+s*0.1),(cx-s*0.5,cy+wy*0.35-s*0.1),(cx,cy),(cx+s*0.5,cy+wy*0.35-s*0.1),(cx+s,cy+wy*0.9+s*0.1)]
    cv2.polylines(mask,[np.array(pts,np.int32)],False,255,th,cv2.LINE_AA)
    cv2.circle(mask,(int(cx),int(cy)),max(2,th//2+1),255,-1,cv2.LINE_AA)
def bigbird(mask,cx,cy,s,ph):
    f=math.sin(ph); 
    def wing(sg):
        lead=[(0,-0.02*s),(sg*0.45*s,(-0.22*f-0.12)*s),(sg*s,(-0.55*f+0.02)*s)]
        trail=[(sg*0.93*s,(-0.50*f+0.14)*s),(sg*0.5*s,(-0.12*f+0.16)*s),(0,0.10*s)]
        return np.array([(cx+x,cy+y) for x,y in lead+trail],np.int32)
    cv2.fillPoly(mask,[wing(1)],255,cv2.LINE_AA); cv2.fillPoly(mask,[wing(-1)],255,cv2.LINE_AA)
    cv2.ellipse(mask,(int(cx),int(cy+0.03*s)),(int(0.20*s),int(0.09*s)),0,0,360,255,-1,cv2.LINE_AA)
    cv2.circle(mask,(int(cx+0.22*s),int(cy-0.01*s)),int(0.06*s),255,-1,cv2.LINE_AA)
    cv2.fillPoly(mask,[np.array([(cx+0.27*s,cy-0.02*s),(cx+0.36*s,cy+0.01*s),(cx+0.26*s,cy+0.03*s)],np.int32)],255,cv2.LINE_AA)
    cv2.fillPoly(mask,[np.array([(cx-0.18*s,cy+0.04*s),(cx-0.40*s,cy+0.10*s),(cx-0.18*s,cy+0.10*s)],np.int32)],255,cv2.LINE_AA)
def flock(t,n,alpha,y0,spd,size,seed=3,scatter=0.0):
    m=np.zeros((H,W),np.uint8); r=np.random.default_rng(seed)
    for i in range(n):
        row=i//2+1; side=1 if i%2 else -1
        if i==0: row=0; side=0
        bx=-200+((t*spd)%(W+900))-row*55; by=y0+row*side*38+math.sin(t*0.8+i)*14
        ph=t*7.5+i*0.9
        if scatter>0:
            by-=scatter*140*(1+i%3)*seg(scatter,0,1); bx+=scatter*60*((i%5)-2)
        bird(m,bx,by,size*(0.85+0.3*r.random()),ph)
    return (m.astype(np.float32)/255)*alpha
def apply_mask(fr,m,col=(12,14,16)):
    return fr*(1-m[...,None])+np.array(col,np.float32)*m[...,None]
# ---------------- text helpers (PIL overlay)
class L:
    def __init__(s): s.im=Image.new('RGBA',(W,H),(0,0,0,0)); s.d=ImageDraw.Draw(s.im)
    def t(s,xy,txt,font,col=WHT,a=1.0,anchor='la',sw=7,shadow=True):
        if a<=0.01: return
        A=int(255*cl(a))
        if shadow: s.d.text((xy[0]+4,xy[1]+6),txt,font=font,fill=(0,0,0,int(150*cl(a))),anchor=anchor,stroke_width=sw,stroke_fill=(0,0,0,int(150*cl(a))))
        s.d.text(xy,txt,font=font,fill=tuple(int(c) for c in col)+(A,),anchor=anchor,stroke_width=sw,stroke_fill=(0,0,0,A))
    def chip(s,xy,txt,font,col=ACC,a=1.0,fill=(10,16,14),anchor='lm',pad=26):
        if a<=0.01: return
        w=font.getlength(txt)+pad*2; hh=font.size*1.15
        x,y=xy
        if anchor=='lm': x0=x; 
        else: x0=x-w/2
        A=int(255*cl(a))
        s.d.rounded_rectangle((x0,y-hh,x0+w,y+hh),radius=int(hh),fill=fill+(int(235*cl(a)),),outline=tuple(col)+(A,),width=4)
        s.d.text((x0+w/2,y),txt,font=font,fill=tuple(col)+(A,),anchor='mm')
def composite(base,layer):
    im=Image.fromarray(np.clip(base,0,255).astype(np.uint8)).convert('RGBA'); im.alpha_composite(layer.im); return np.array(im.convert('RGB'))
def aqi_col(v):
    if v<100: return (120,220,90)
    if v<200: return (240,210,60)
    if v<300: return (255,140,30)
    if v<400: return (235,60,50)
    return (160,20,60)
# ---------------- scenes
def s1(t):
    haze=0.05+0.85*ease(seg(t,2.6,5.8)); fr=world(t,haze)
    a=1.0-0.85*seg(t,5.0,8.0); sc=seg(t,5.2,8.4)
    fr=apply_mask(fr,flock(t+3.5,13,a,640+sc*-120,120,30,scatter=sc))
    lay=L()
    lay.t((60,360),"EVERY WINTER",AN(110),CREAM,eo3(seg(t,0.3,0.9))*(1-seg(t,3.0,3.4)),sw=9)
    lay.t((60,490),"THESE WETLANDS FILL WITH BIRDS",BC(64),ACC,eo3(seg(t,0.9,1.5))*(1-seg(t,3.0,3.4)),sw=7)
    ta=seg(t,3.2,3.6)
    if t>=3.2:
        v=int(lerp(62,367,ease(seg(t,3.3,5.3)))); col=aqi_col(v)
        lay.t((W//2,330),"DELHI AQI  |  5 NOV 2026, 9 AM",BC(54),CREAM,eo3(ta),anchor='mm',sw=6)
        sc2=1+0.05*math.sin(t*14)*seg(t,5.3,5.6)*(1-seg(t,5.6,6.2))
        lay.t((W//2,640),str(v),AN(430*sc2),col,eo3(ta),anchor='mm',sw=14)
        # scale bar
        bx0,bx1,by=110,970,860
        for i,c in enumerate([(120,220,90),(240,210,60),(255,140,30),(235,60,50),(160,20,60)]):
            x0=bx0+(bx1-bx0)*i/5; lay.d.rectangle((x0,by,x0+(bx1-bx0)/5-4,by+26),fill=c+(int(230*eo3(ta)),))
        mx=bx0+(bx1-bx0)*cl(v/500); lay.d.polygon([(mx,by-8),(mx-18,by-44),(mx+18,by-44)],fill=WHT+(int(255*eo3(ta)),))
    lay.t((W//2,980),"SOME AREAS CROSSED 400: SEVERE",BC(64),RED,eo3(seg(t,5.8,6.4)),anchor='mm',sw=8)
    lay.t((60,1120),"NOW THINK OF THE BIRDS.",AN(100),WHT,eo3(seg(t,7.2,7.9)),sw=9)
    return composite(fr,lay)
# map projection
LON0,LAT0,SCL=76.80,28.95,1250.0
def mp(lon,lat): return (60+(lon-LON0)*SCL*0.97, 400+(LAT0-lat)*SCL*1.05)
DELHI=[(76.84,28.55),(76.90,28.70),(77.00,28.83),(77.15,28.88),(77.25,28.86),(77.34,28.72),(77.35,28.60),(77.30,28.50),(77.15,28.45),(77.00,28.40),(76.88,28.45)]
YAM=[(77.20,28.95),(77.22,28.75),(77.25,28.65),(77.315,28.567),(77.35,28.46),(77.45,28.32),(77.52,28.2)]
PINS=[("OKHLA",77.315,28.567,10.6,(60,-75)),("NAJAFGARH JHEEL",76.95,28.50,11.7,(-20,-85)),("SULTANPUR",76.88,28.47,12.8,(-10,70)),("DHANAURI",77.50,28.35,13.9,(0,75))]
def s2(t):
    bg=np.zeros((H,W,3),np.float32)+np.array((14,24,28),np.float32)
    gx=np.arange(W)[None,:]; gy=np.arange(H)[:,None]
    g=(((gx%60)<2)|((gy%60)<2)).astype(np.float32)*10; bg+=g[...,None]
    lay=L(); st=t-9.0
    smog=ease(seg(t,15.5,21.0))
    if smog>0:
        ox=int(t*30)%300; oy=int(t*14)%300
        hz=HZ1[oy:oy+H,ox:ox+W]*0.55+HZ2[oy:oy+H,ox:ox+W]*0.45; hz=cv2.GaussianBlur(hz,(0,0),25); ha=np.clip(0.30+(hz-0.5)*0.8,0,1)*smog*0.78
        bgs=bg*(1-ha[...,None])+np.array((150,115,70),np.float32)*ha[...,None]
    else: bgs=bg
    # map layer
    mpl=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(mpl)
    pts=[mp(*p) for p in DELHI]; d.polygon(pts,fill=(255,255,255,26),outline=(250,243,228,230)); d.line(pts+[pts[0]],fill=(250,243,228,230),width=5)
    yp=[mp(*p) for p in YAM]; n=int(len(yp)*seg(t,9.6,11.0)*1.0+1)
    d.line(yp,fill=(60,200,200,230),width=9,joint='curve')
    for k in range(7):
        u=((t*0.35+k/7)%1)*(len(yp)-1); i=int(u); f=u-i; px=yp[i][0]*(1-f)+yp[min(i+1,len(yp)-1)][0]*f; py=yp[i][1]*(1-f)+yp[min(i+1,len(yp)-1)][1]*f
        d.ellipse((px-7,py-7,px+7,py+7),fill=(200,255,255,230))
    dc=mp(77.12,28.66); d.text(dc,"DELHI",font=BC(46),fill=(250,243,228,150),anchor='mm')
    d.text(mp(77.30,28.80),"YAMUNA",font=BC(34),fill=(60,200,200,235),anchor='lm')
    base=Image.fromarray(np.clip(bgs,0,255).astype(np.uint8)).convert('RGBA'); base.alpha_composite(mpl)
    hub=mp(77.12,28.66); sp=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sp)
    for name,lon,lat,tt,(dx,dy) in PINS:
        x,y=mp(lon,lat); pr=ease(seg(t,tt-0.4,tt+0.1)); sd.line([hub,(hub[0]+(x-hub[0])*pr,hub[1]+(y-hub[1])*pr)],fill=(232,255,61,150),width=5)
    base.alpha_composite(sp)
    for name,lon,lat,tt,(dx,dy) in PINS:
        x,y=mp(lon,lat); k=eob(seg(t,tt,tt+0.45))
        if k<=0: continue
        pl=Image.new('RGBA',(W,H),(0,0,0,0)); pd=ImageDraw.Draw(pl)
        for j in range(3):
            u=(((t-tt)*0.8+j/3)%1); r=14+u*70; pd.ellipse((x-r,y-r,x+r,y+r),outline=(232,255,61,int(220*(1-u))),width=4)
        rr=16*k; pd.ellipse((x-rr,y-rr,x+rr,y+rr),fill=(232,255,61,255),outline=(0,0,0,255),width=4)
        base.alpha_composite(pl)
    lay.im=Image.alpha_composite(base,lay.im); lay.d=ImageDraw.Draw(lay.im)
    for name,lon,lat,tt,(dx,dy) in PINS:
        x,y=mp(lon,lat); k=seg(t,tt+0.2,tt+0.7)
        if k>0: lay.t((x+dx,y+dy),name,BC(50),CREAM,k,anchor='mm',sw=6)
    lay.t((W//2,200),"DELHI-NCR WETLANDS",AN(96),CREAM,eo3(seg(st,0.2,0.8)),anchor='mm',sw=9)
    lay.t((W//2,290),"WINTER HOME FOR MIGRATORY BIRDS",BC(52),ACC,eo3(seg(st,0.9,1.5)),anchor='mm',sw=6)
    lay.t((W//2,1560),"SULTANPUR: A RAMSAR SITE SINCE 2021",BC(50),CREAM,eo3(seg(t,14.6,15.2))*(1-seg(t,17.5,18.0)),anchor='mm',sw=6)
    lay.t((W//2,1560),"THEN THE SMOG ARRIVES.",AN(88),ORG,eo3(seg(t,17.8,18.5)),anchor='mm',sw=9)
    lay.t((W//2,1640),"Schematic map. Positions approximate.",BM(32),(210,210,210),0.7,anchor='mm',sw=3,shadow=False)
    return np.array(lay.im.convert('RGB')).astype(np.float32)
def particles(t,n,seed,intensity,col):
    r=np.random.default_rng(seed); out=np.zeros((H,W),np.float32)
    px=(r.random(n)*W+t*r.uniform(40,160,n))%W; py=(r.random(n)*H+t*r.uniform(-30,70,n)+np.sin(t+r.random(n)*6)*30)%H
    for i in range(n):
        cv2.circle(out,(int(px[i]),int(py[i])),int(2+r.random()*5),1.0,-1,cv2.LINE_AA)
    return out*intensity
def s3(t):
    st=t-22.0; haze=0.95; fr=world(t,haze)*0.62
    fr=fr*(0.55+0.45*(1-0.0))
    pt=particles(t,260,5,0.9,None); fr=fr*(1-pt[...,None]*0.7)+np.array((205,170,110),np.float32)*pt[...,None]*0.7
    # big bird silhouette
    m=np.zeros((H,W),np.uint8); bigbird(m,W//2+int(math.sin(t*0.7)*30),640+int(math.sin(t*1.3)*14),380,t*5.0)
    cough=0.5+0.5*math.sin(t*9)
    fr=apply_mask(fr,m.astype(np.float32)/255*0.9)
    lay=L()
    lay.t((60,210),"WHAT SMOG",AN(110),CREAM,eo3(seg(st,0.2,0.8)),sw=9); lay.t((60,330),"DOES TO BIRDS",AN(110),ACC,eo3(seg(st,0.5,1.1)),sw=9)
    items=[(["FINE PARTICLES CAN","INFLAME BIRD LUNGS"],"Research review, 2025",2.2,ORG),
           (["DELHI VETS: ABOUT 25 BIRDS WITH","WATERY, IRRITATED EYES IN WEEKS"],"One east Delhi clinic, Dec 2025. Not a census.",5.6,ORG),
           (["HARYANA, 2019 TO 2022:","WORSE AIR, FEWER BIRD SPECIES"],"Fatehabad and Hisar. A link, not proof of cause.",9.4,ORG)]
    for i,(a_,b_,ts,c) in enumerate(items):
        y=860+i*270; k=eo3(seg(st,ts,ts+0.5))
        if k<=0: continue
        lay.d.rounded_rectangle((50,y-100,1030,y+150),radius=26,fill=(10,14,12,int(220*k)),outline=c+(int(255*k),),width=4)
        lay.t((80,y-70),a_[0],BC(50),WHT,k,sw=0,shadow=False); lay.t((80,y-10),a_[1],BC(50),WHT,k,sw=0,shadow=False)
        lay.t((80,y+75),b_,BM(32),(220,220,220),k,sw=0,shadow=False)
    return composite(fr,lay)
def s4(t):
    st=t-36.0
    bg=grad((24,30,34),(38,44,40)); fr=bg.copy()
    ys=np.arange(H,dtype=np.float32)[:,None]; xs=np.arange(W,dtype=np.float32)[None,:]
    wm=(ys>520).astype(np.float32)
    rip=np.sin(xs*0.02+ys*0.07-t*2.0)+np.sin(xs*0.05-ys*0.04+t*1.3)
    wcol=np.array((46,86,84),np.float32)*(0.7+0.12*rip[...,None])
    wat=wcol*(1-0.35*np.clip((ys-520)/1400,0,1)[...,None])
    fr=fr*(1-wm[...,None])+wat*wm[...,None]
    # foam particles
    r=np.random.default_rng(9); n=int(60+420*ease(seg(st,1.0,9.0))); f=np.zeros((H,W),np.float32)
    fx=(r.random(n)*W+np.sin(t*0.5+r.random(n)*6)*40)%W; fy=520+(r.random(n)*1400+t*r.uniform(40,120,n))%1400; fs=r.uniform(5,24,n)
    for i in range(n): cv2.circle(f,(int(fx[i]),int(fy[i])),int(fs[i]),1.0,-1,cv2.LINE_AA)
    f=cv2.GaussianBlur(f,(0,0),2)*0.8; fr=fr*(1-f[...,None])+np.array((240,240,236),np.float32)*f[...,None]
    lay=L()
    lay.t((60,210),"THEN THE",AN(110),CREAM,eo3(seg(st,0.2,0.8)),sw=9); lay.t((60,330),"WATER",AN(150),TEAL,eo3(seg(st,0.5,1.1)),sw=9)
    k1=eo3(seg(st,2.2,2.8))
    if k1>0:
        lay.d.rounded_rectangle((50,600,1030,810),radius=26,fill=(10,14,12,int(215*k1)),outline=TEAL+(int(255*k1),),width=4)
        lay.t((80,650),"YAMUNA, DELHI: 22 KM",BC(50),WHT,k1,sw=0,shadow=False); lay.t((80,715),"MOST POLLUTED OF INDIA'S 311 POLLUTED RIVER STRETCHES",BC(36),(230,230,230),k1,sw=0,shadow=False)
        lay.t((80,770),"CEEW",BM(30),TEAL,k1,sw=0,shadow=False)
    k2=eo3(seg(st,6.0,6.6))
    if k2>0:
        lay.d.rounded_rectangle((50,860,1030,1100),radius=26,fill=(10,14,12,int(215*k2)),outline=ORG+(int(255*k2),),width=4)
        lay.t((80,910),"AMMONIA ABOVE THE SAFE LIMIT",BC(52),WHT,k2,sw=0,shadow=False); lay.t((80,975),"AT 13 OF 17 SPOTS TESTED, HARYANA TO DELHI",BC(40),(230,230,230),k2,sw=0,shadow=False)
        lay.t((80,1040),"CPCB test, 2018",BM(30),ORG,k2,sw=0,shadow=False)
        # gauge
        gx,gy=870,1230
    k3=eo3(seg(st,9.5,10.1))
    if k3>0:
        lay.t((60,1250),"FOAM. DETERGENT. SEWAGE.",AN(78),WHT,k3,sw=9); lay.t((60,1350),"THE FOOD AND WATER BIRDS DEPEND ON.",BC(52),ACC,k3,sw=6)
    return composite(fr,lay)
def s5(t):
    st=t-50.0; fr=grad((12,16,20),(20,24,28)).copy()
    gx=np.arange(W)[None,:]; fr[:, :, :]+= ((gx%90)<2).astype(np.float32)[...,None]*8
    lay=L()
    lay.t((60,200),"THE COUNTS",AN(110),CREAM,eo3(seg(st,0.2,0.8)),sw=9)
    lay.t((60,320),"ASIAN WATERBIRD CENSUS",BC(54),ACC,eo3(seg(st,0.5,1.1)),sw=6)
    def bars(y0,name,a,al,b,bl,ts,note):
        k=eo3(seg(st,ts,ts+0.5)); 
        if k<=0: return
        lay.t((60,y0),name,BC(60),WHT,k,sw=6)
        m=max(a,b); sc=700/m
        va=a*ease(seg(st,ts+0.4,ts+1.6)); lay.d.rounded_rectangle((60,y0+80,60+max(8,va*sc),y0+160),radius=14,fill=(120,220,90,int(235*k)))
        lay.t((60+max(8,va*sc)+14,y0+120),f"{int(va):,}",AN(56),WHT,k,anchor='lm',sw=5); lay.t((70,y0+120),al,BC(38),(8,12,10),k,anchor='lm',sw=0,shadow=False)
        tb=ts+2.6
        kb=eo3(seg(st,tb,tb+0.4))
        if kb>0:
            vb=a-(a-b)*ease(seg(st,tb+0.2,tb+1.8)); lay.d.rounded_rectangle((60,y0+180,60+max(8,vb*sc),y0+260),radius=14,fill=(235,60,50,int(235*kb)))
            lay.t((60+max(8,vb*sc)+14,y0+220),f"{int(vb):,}",AN(56),RED if False else WHT,kb,anchor='lm',sw=5); lay.t((70,y0+220),bl,BC(38),WHT,kb,anchor='lm',sw=0,shadow=False)
        lay.t((60,y0+290),note,BM(32),(215,215,215),k,sw=0,shadow=False)
        pc=int(round((1-b/a)*100)); kp=eob(seg(st,tb+1.6,tb+2.1))
        if kp>0: lay.t((1020,y0+28),f"-{pc}%",AN(88*min(1,kp)+1),RED,min(1,kp),anchor='rm',sw=8)
    bars(520,"NAJAFGARH JHEEL",27673,"2021",10592,"2022",1.2,"Species: 81 to 71. Flamingos: 100 to 500 a day, to one.")
    bars(1010,"SULTANPUR",9026,"2023",2686,"2024",8.0,"Species: 51 to 43. (Haryana forest dept says its totals have risen.)")
    lay.t((60,1480),"Counts change with year, rain and method.",BM(34),(205,205,205),eo3(seg(st,14.5,15.1)),sw=0,shadow=False)
    return composite(fr,lay)
def s6(t):
    st=t-68.0; fr=world(t,0.8)*0.5
    r=np.random.default_rng(4); pt=particles(t,140,6,0.6,None); fr=fr*(1-pt[...,None]*0.5)+np.array((200,165,105),np.float32)*pt[...,None]*0.5
    lay=L()
    lay.t((60,200),"BUT IT IS NOT",AN(100),CREAM,eo3(seg(st,0.2,0.8)),sw=9); lay.t((60,315),"ONLY THE AIR.",AN(120),ORG,eo3(seg(st,0.5,1.1)),sw=9)
    chips=[("DRYING WETLANDS",TEAL),("DIRTY WATER",(120,220,90)),("DUST AND BUILDING",AMB),("LATE, WARMER WINTERS",(235,110,110))]
    for i,(c,col) in enumerate(chips):
        k=eob(seg(st,2.0+i*1.7,2.5+i*1.7)); 
        if k<=0: continue
        y=620+i*160; lay.chip((60,y),c,BC(60),col,min(1,k),pad=34)
    lay.t((60,1400),"EXPERTS STILL DEBATE",BC(60),CREAM,eo3(seg(st,9.4,10.0)),sw=6); lay.t((60,1470),"HOW MUCH IS THE AIR ALONE.",BC(60),ACC,eo3(seg(st,9.9,10.5)),sw=6)
    return composite(fr,lay)
def s7(t):
    st=t-80.0; haze=0.9-0.8*ease(seg(st,1.0,8.0)); fr=world(t,haze)
    fr=apply_mask(fr,flock(t,15,ease(seg(st,2.0,4.0)),560,110,28,seed=8))
    lay=L()
    lay.t((60,260),"PROTECT",AN(150),CREAM,eo3(seg(st,0.4,1.0)),sw=11); lay.t((60,430),"THE WETLANDS.",AN(150),ACC,eo3(seg(st,0.8,1.4)),sw=11)
    lay.t((60,640),"THEY CLEAN THE CITY TOO.",BC(66),WHT,eo3(seg(st,1.6,2.2)),sw=7)
    lay.t((60,1280),"DELHI'S AIR",AN(88),CREAM,eo3(seg(st,4.0,4.6)),sw=9); lay.t((60,1380),"PART 1 OF 3",AN(88),ORG,eo3(seg(st,4.4,5.0)),sw=9)
    lay.t((60,1500),"Sources in the caption.",BM(36),(230,230,230),eo3(seg(st,5.5,6.1)),sw=0,shadow=False)
    lay.t((60,1575),"@thenaturalangle",BC(54),WHT,eo3(seg(st,6.3,6.9)),sw=6)
    return composite(fr,lay)
SC=[(0,9,s1),(9,22,s2),(22,36,s3),(36,50,s4),(50,68,s5),(68,80,s6),(80,90,s7)]
def frame(i):
    t=min(i/FPS,TOTAL-1e-3)
    for a,b,f in SC:
        if a<=t<b:
            fr=f(t).astype(np.float32)
            d=seg(t,a,a+0.35); e=1-seg(t,b-0.12,b)
            return np.clip(fr*(0.15+0.85*d)*(0.5+0.5*e),0,255).astype(np.uint8)
    return f(TOTAL-1e-3).astype(np.uint8)
