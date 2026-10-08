import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
import ref2
from ref2 import anton,bc,bcs,bar,barm,corm,TEX,CREAM,GOLD,BG,wrap_text
W,H=1080,1350
T=TEX[:H]
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
P={1:Image.open(U+"39abed35-image.jpg").convert("RGB"),2:Image.open(U+"088198af-image.jpg").convert("RGB"),3:Image.open(U+"84a2e37d-image.jpg").convert("RGB")}
def crop(k,box,w,h,dim=1.0):
    im=P[k]; SW,SH=im.size
    im=im.crop((int(box[0]*SW),int(box[1]*SH),int(box[2]*SW),int(box[3]*SH)))
    s=max(w/im.width,h/im.height); im=im.resize((max(w,round(im.width*s)),max(h,round(im.height*s))),Image.LANCZOS)
    l=(im.width-w)//2;t=(im.height-h)//2; im=im.crop((l,t,l+w,t+h))
    if dim!=1.0: im=Image.fromarray((np.array(im).astype(np.float32)*dim).clip(0,255).astype(np.uint8))
    return im
def canvas(): return Image.fromarray(np.full((H,W,3),(14,15,13),np.uint8))
def gold_text(c,xy,t,font):
    m=Image.new("L",(W,H),0); ImageDraw.Draw(m).text(xy,t,font=font,fill=255,anchor="la")
    mn=np.array(m).astype(np.float32)/255; a=np.array(c).astype(np.float32)
    sh=cv2.GaussianBlur(mn,(0,0),12)*0.5; a=a*(1-sh[:,:,None]); a=a*(1-mn[:,:,None])+T*mn[:,:,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def header(c,i):
    d=ImageDraw.Draw(c); d.text((64,48),"THE NATURAL ANGLE",font=bcs(26),fill=(220,214,200))
    cnt=f"{i}/6"; tw=d.textlength(cnt,font=bcs(26))+44
    d.rounded_rectangle([W-64-tw,34,W-64,82],radius=24,fill=(20,20,18)); d.text((W-64-tw+22,44),cnt,font=bcs(26),fill=CREAM)
def lead(c,xy,t,size=70): ImageDraw.Draw(c).text(xy,t,font=corm(size),fill=(236,230,214),anchor="la")
def grad(c,y0,y1,a0,a1):
    a=np.array(c).astype(np.float32); yy=np.arange(H)[:,None]
    t=np.clip((yy-y0)/max(1,(y1-y0)),0,1); al=(a0+(a1-a0)*t)[:,:,None]
    return Image.fromarray((a*(1-al)+np.array(BG,np.float32)*al).astype(np.uint8))
def finish(c,name,vig=0.26):
    a=np.array(c).astype(np.float32); yy,xx=np.mgrid[0:H,0:W]; d=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
    a*=(1-vig*np.clip(d-0.5,0,1)**1.4)[:,:,None]; a+=np.random.default_rng(7).normal(0,5.0,(H,W,1))
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save("shot3/"+name,quality=95)
def wrapd(d,t,f,mw): return wrap_text(d,t,f,mw)

def extend(k,box,y,ph,dim=0.82):
    im=crop(k,box,W,ph,dim=dim); pa=np.array(im)
    top,bot=y,H-y-ph
    pad=cv2.copyMakeBorder(pa,top,bot,0,0,cv2.BORDER_REPLICATE)
    bl=cv2.GaussianBlur(pad,(0,0),sigmaX=70,sigmaY=14)
    bl=cv2.GaussianBlur(bl,(0,0),25)
    mk=np.zeros((H,W),np.float32); mk[y:y+ph]=1
    fe=90
    for i in range(fe):
        mk[y+i]=np.minimum(mk[y+i],i/fe); mk[y+ph-1-i]=np.minimum(mk[y+ph-1-i],i/fe)
    out=pad*mk[:,:,None]+bl*(1-mk[:,:,None])
    out=out*0.78
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))
def facts(c,items,y,n=None):
    d=ImageDraw.Draw(c); n=len(items); gap=36; cw=(W-128-gap*(n-1))/n
    for k,(lab,tx) in enumerate(items):
        x=64+k*(cw+gap); d.line([(x,y),(x,y+128)],fill=(150,146,134),width=2); d.text((x+22,y-2),lab,font=bcs(22),fill=GOLD)
        for j,l in enumerate(wrapd(d,tx,bar(25),cw-30)[:4]): d.text((x+22,y+30+j*32),l,font=bar(25),fill=CREAM)


def fit(t,mw,cap):
    pr=ImageDraw.Draw(Image.new("L",(5,5))); s=cap
    while pr.textlength(t,font=anton(s))>mw and s>30: s-=2
    return s
def hgrad(c,x0,x1,a0,a1):
    a=np.array(c).astype(np.float32); xx=np.arange(W)[None,:]
    t=np.clip((xx-x0)/max(1,(x1-x0)),0,1); al=(a0+(a1-a0)*t)[:,:,None]
    return Image.fromarray((a*(1-al)+np.array(BG,np.float32)*al).astype(np.uint8))
def tinylabel(c,t,y=1318,x=64):
    d=ImageDraw.Draw(c); d.text((x,y),t,font=bc(21),fill=(200,196,184))


def wtext(c,xy,t,font,mw,fill=(244,240,230),lh=1.3):
    d=ImageDraw.Draw(c); y=xy[1]
    for l in wrapd(d,t,font,mw): d.text((xy[0],y),l,font=font,fill=fill); y+=int(font.size*lh)
    return y
def dark(): return Image.fromarray(np.full((H,W,3),(14,15,13),np.uint8))
def paw(d,cx,cy,s,fill=None,outline=None,w=3):
    sh=[(cx,cy+0.28*s,0.55*s,0.42*s)]+[(cx+dx*s,cy+dy*s,0.17*s,0.23*s) for dx,dy in [(-0.62,-0.14),(-0.22,-0.52),(0.22,-0.52),(0.62,-0.14)]]
    for (x,y,rx,ry) in sh: d.ellipse([x-rx,y-ry,x+rx,y+ry],fill=fill,outline=outline,width=w)
def topo(c,alpha=0.16,seed=4,col=(226,184,104)):
    rng=np.random.default_rng(seed); n=rng.normal(0,1,(54,68)).astype(np.float32)
    n=cv2.resize(n,(W,H),interpolation=cv2.INTER_CUBIC); n=cv2.GaussianBlur(n,(0,0),90)
    n=(n-n.min())/(n.max()-n.min()); ov=np.zeros((H,W),np.uint8)
    for lv in np.linspace(0.12,0.9,22):
        m=(n>lv).astype(np.uint8)*255
        cs,_=cv2.findContours(m,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
        cv2.polylines(ov,cs,False,255,2,cv2.LINE_AA)
    ov=cv2.GaussianBlur(ov,(0,0),0.8).astype(np.float32)/255*alpha
    a=np.array(c).astype(np.float32); a=a*(1-ov[:,:,None])+np.array(col,np.float32)*ov[:,:,None]
    return Image.fromarray(a.astype(np.uint8))
def motes(c,n=70,seed=9,strength=0.5,ybias=None):
    rng=np.random.default_rng(seed); ov=np.zeros((H,W),np.float32)
    for _ in range(n):
        x=rng.uniform(0,W); y=rng.uniform(0,H) if ybias is None else rng.uniform(*ybias); r=rng.uniform(2,7)
        cv2.circle(ov,(int(x),int(y)),int(r),float(rng.uniform(0.3,1.0)),-1,cv2.LINE_AA)
    ov=cv2.GaussianBlur(ov,(0,0),2.2)*strength
    a=np.array(c).astype(np.float32)+ov[:,:,None]*np.array([255,225,160],np.float32)*0.55
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def leak(c,strength=0.28):
    yy,xx=np.mgrid[0:H,0:W]; d=np.sqrt((xx-W*0.95)**2+(yy-H*0.05)**2)/W
    ov=np.clip(1-d*1.5,0,1)**2*strength; a=np.array(c).astype(np.float32)
    a=a+ov[:,:,None]*np.array([255,170,70],np.float32); return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def progress(c,i,n=10):
    d=ImageDraw.Draw(c); gw=(W-128-(n-1)*10)/n
    for k in range(n): d.rounded_rectangle([64+k*(gw+10),1336,64+k*(gw+10)+gw,1341],radius=2,fill=GOLD if k<i else (70,68,60))
def chip(c,x,y,t,fill,fg=(20,16,8),size=24):
    d=ImageDraw.Draw(c); f=bcs(size); w_=d.textlength(t,font=f)+34
    d.rounded_rectangle([x,y,x+w_,y+size+20],radius=(size+20)//2,fill=fill); d.text((x+17,y+9),t,font=f,fill=fg); return w_
def swipe(c,y=1262):
    d=ImageDraw.Draw(c); d.text((W-64-d.textlength("SWIPE",font=bcs(24))-46,y),"SWIPE",font=bcs(24),fill=GOLD)
    x=W-64-30; d.line([(x,y+14),(x+26,y+14)],fill=GOLD,width=3); d.polygon([(x+36,y+14),(x+24,y+6),(x+24,y+22)],fill=GOLD)

import math
MOSS=(138,160,92); RUST=(196,84,64); SUN=(240,150,40)
def pill(c,x,y,t,fg=CREAM,hi=None,size=30,fill=(14,12,8),alpha=0.72):
    d=ImageDraw.Draw(c,"RGBA"); f=bcs(size); w_=d.textlength(t,font=f)+44
    d.rounded_rectangle([x,y,x+w_,y+size+26],radius=16,fill=fill+(int(255*alpha),),outline=(255,255,255,40),width=1)
    d.text((x+22,y+12),t,font=f,fill=fg); return w_
def progress8(c,i):
    d=ImageDraw.Draw(c); gw=(W-128-7*10)/8
    for k in range(8): d.rounded_rectangle([64+k*(gw+10),1336,64+k*(gw+10)+gw,1341],radius=2,fill=GOLD if k<i else (70,68,60))
def hdr(c,i,n=8):
    d=ImageDraw.Draw(c); d.text((64,48),"THE NATURAL ANGLE",font=bcs(26),fill=(220,214,200))
    cnt=f"{i}/{n}"; tw=d.textlength(cnt,font=bcs(26))+44
    d.rounded_rectangle([W-64-tw,34,W-64,82],radius=24,fill=(20,20,18)); d.text((W-64-tw+22,44),cnt,font=bcs(26),fill=CREAM)
def done(c,i,name,vig=0.24):
    progress8(c,i); hdr(c,i); finish(c,name,vig=vig)
def blurbg(img,dim=0.55,sig=22):
    a=cv2.GaussianBlur(np.array(img),(0,0),sig).astype(np.float32)*dim
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def camera(d,x,y,s=1.0,col=CREAM):
    d.rounded_rectangle([x,y,x+60*s,y+42*s],radius=7*s,outline=col,width=3); d.rectangle([x+16*s,y-8*s,x+34*s,y],outline=col,width=3)
    d.ellipse([x+20*s,y+9*s,x+42*s,y+31*s],outline=col,width=3)
def egret(d,x,y,s=1.0,col=(240,236,226),spoon=False):
    # body
    d.ellipse([x-20*s,y-10*s,x+20*s,y+10*s],fill=col)
    d.line([(x+14*s,y-6*s),(x+26*s,y-34*s),(x+22*s,y-52*s)],fill=col,width=int(5*s)+1)
    d.ellipse([x+16*s,y-60*s,x+30*s,y-46*s],fill=col)
    if spoon: d.line([(x+28*s,y-54*s),(x+48*s,y-48*s)],fill=col,width=int(4*s)); d.ellipse([x+44*s,y-54*s,x+58*s,y-44*s],fill=col)
    else: d.line([(x+28*s,y-54*s),(x+46*s,y-50*s)],fill=(236,200,90),width=int(3*s)+1)
    for dx in (-5,6): d.line([(x+dx*s,y+8*s),(x+(dx-1)*s,y+34*s)],fill=col,width=3)
def sun(c,cx,cy,r):
    a=np.array(c).astype(np.float32); yy,xx=np.mgrid[0:H,0:W]; dd=np.sqrt((xx-cx)**2+(yy-cy)**2)
    g=np.clip(1-dd/(r*3.2),0,1)**2*0.55; a=a+g[:,:,None]*np.array(SUN,np.float32)
    c=Image.fromarray(np.clip(a,0,255).astype(np.uint8)); d=ImageDraw.Draw(c); d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=SUN); return c
def panel(c,x0,y0,x1,y1):
    d=ImageDraw.Draw(c,"RGBA"); d.rounded_rectangle([x0,y0,x1,y1],radius=22,fill=(16,15,11,235),outline=(120,112,90,120),width=2)
    d.text(((x0+x1)/2,y0+22),"SIDE VIEW",font=bcs(20),fill=(190,184,168),anchor="mm")
    d.ellipse([x0+26,y0+44,x0+52,y0+70],outline=CREAM,width=3); d.line([(x0+39,y0+50),(x0+39,y0+58),(x0+45,y0+58)],fill=CREAM,width=3)
    d.text((x0+64,y0+47),"BEFORE SUNRISE",font=bcs(22),fill=CREAM)

N=7
def prog(c,i):
    d=ImageDraw.Draw(c); gw=(W-128-(N-1)*10)/N
    for k in range(N): d.rounded_rectangle([64+k*(gw+10),1336,64+k*(gw+10)+gw,1341],radius=2,fill=GOLD if k<i else (70,68,60))
def hd(c,i):
    d=ImageDraw.Draw(c); d.text((64,48),"THE NATURAL ANGLE",font=bcs(26),fill=(220,214,200))
    cnt=f"{i}/{N}"; tw=d.textlength(cnt,font=bcs(26))+44
    d.rounded_rectangle([W-64-tw,34,W-64,82],radius=24,fill=(20,20,18)); d.text((W-64-tw+22,44),cnt,font=bcs(26),fill=CREAM)
def fin(c,i,name,vig=0.24): prog(c,i); hd(c,i); finish(c,name,vig=vig)
def pc(k,box,w,h,dim=1.0):
    im=P[k].crop(tuple(int(v) for v in box)).resize((w,h),Image.LANCZOS)
    if dim!=1.0: im=Image.fromarray((np.array(im).astype(np.float32)*dim).clip(0,255).astype(np.uint8))
    return im
def bgblur(k,dim=0.45,sig=30):
    im=P[k].resize((W,H),Image.LANCZOS); a=cv2.GaussianBlur(np.array(im),(0,0),sig).astype(np.float32)*dim
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def paste(c,im,x,y,ftop=0,fbot=0):
    w,h=im.size; m=np.ones((h,w),np.float32)
    for i in range(ftop): m[i]=i/ftop
    for i in range(fbot): m[h-1-i]=np.minimum(m[h-1-i],i/fbot)
    a=np.array(c).astype(np.float32); reg=a[y:y+h,x:x+w]; a[y:y+h,x:x+w]=reg*(1-m[:,:,None])+np.array(im).astype(np.float32)*m[:,:,None]
    return Image.fromarray(a.astype(np.uint8))
def arrow(d,p0,p1,col=GOLD,w=4,dash=False):
    import math
    x0,y0=p0;x1,y1=p1; L=math.hypot(x1-x0,y1-y0); ux,uy=(x1-x0)/L,(y1-y0)/L
    if dash:
        t=0
        while t<L-30: d.line([(x0+ux*t,y0+uy*t),(x0+ux*min(t+18,L-30),y0+uy*min(t+18,L-30))],fill=col,width=w); t+=32
    else: d.line([(x0,y0),(x1-ux*20,y1-uy*20)],fill=col,width=w)
    d.polygon([(x1,y1),(x1-ux*30-uy*13,y1-uy*30+ux*13),(x1-ux*30+uy*13,y1-uy*30-ux*13)],fill=col)

# ---- S1 hook
c=pc(1,(0,0,2311,2889),W,H,0.95); c=grad(c,0,400,0.55,0.0); c=grad(c,1150,H,0.0,0.5)
lead(c,(66,92),"Black-headed ibis, just before landing.",46)
s_=fit("WHY DO THESE",900,96); c=gold_text(c,(60,134),"WHY DO THESE",anton(s_)); c=gold_text(c,(60,134+int(s_*1.1)),"WINGS GLOW?",anton(s_))
pill(c,64,1240,"SUNRISE. BACKLIGHT. ONE SECOND.",fg=(244,238,226),size=28); swipe(c,1262)
c=motes(c,35,3,0.35); fin(c,1,"slide1.jpg")

# ---- S2 ID: backlight hides colour
c=bgblur(1,0.5)
A=pc(1,(160,0,1735,2889),540,1010,0.95); B=pc(3,(400,0,2427,3716),540,1010,0.95)
c=paste(c,A,0,330,ftop=70); c=paste(c,B,540,330,ftop=70)
c=grad(c,1000,1340,0.0,0.85)
d=ImageDraw.Draw(c); d.line([(540,340),(540,1340)],fill=GOLD,width=2)
lead(c,(66,92),"Two ibises. One morning.",46)
c=gold_text(c,(60,134),"BACKLIGHT HIDES COLOUR.",anton(fit("BACKLIGHT HIDES COLOUR.",950,92)))
d=ImageDraw.Draw(c); d.text((66,248),"So tell them apart by head, bill and size.",font=bar(30),fill=(235,230,218))
pill(c,32,352,"BLACK-HEADED IBIS",fg=(244,238,226),size=24); pill(c,572,352,"GLOSSY IBIS",fg=(200,236,140),size=24)
for t_,x,y in [("White body.",40,1120),("Bare black head.",40,1160),("Thick, curved bill.",40,1200),("Dark chestnut body.",580,1120),("Green gloss in good light.",580,1160),("Slimmer bill.",580,1200)]:
    d.text((x,y),t_,font=bar(28),fill=(244,240,230))
c=motes(c,25,5,0.3); fin(c,2,"slide2.jpg")

# ---- S3 light through feathers
c=pc(2,(560,0,2269,2136),W,H,0.95); c=grad(c,0,330,0.5,0.0); c=grad(c,1080,H,0.0,0.72)
lead(c,(66,92),"Low sun behind the bird.",46)
c=gold_text(c,(60,134),"LIGHT THROUGH FEATHERS.",anton(fit("LIGHT THROUGH FEATHERS.",950,92)))
d=ImageDraw.Draw(c,"RGBA")
arrow(d,(985,205),(905,330),col=(255,214,120,255),w=4,dash=True)
pill(c,770,360,"SUN, OUT OF FRAME",fg=(255,226,150),size=24)
arrow(d,(905,640),(790,560),col=(244,238,226,255),w=3)
pill(c,712,660,"THIN EDGES LET LIGHT THROUGH",fg=(244,238,226),size=22)
d=ImageDraw.Draw(c); d.text((64,1150),"Feathers are thin, so they glow.",font=corm(56),fill=(244,238,226))
d.text((64,1226),"Shoot into the light. Keep the background dark.",font=bar(30),fill=(235,230,218))
c=motes(c,30,8,0.35); fin(c,3,"slide3.jpg")

# ---- S4 two frames
c=bgblur(2,0.45)
A=pc(2,(0,450,2952,1654),1080,440,0.95); B=pc(1,(0,640,2311,1945),1080,610,0.95)
c=paste(c,A,0,300,ftop=60); c=paste(c,B,0,740)
ImageDraw.Draw(c).line([(0,740),(1080,740)],fill=GOLD,width=2)
lead(c,(66,92),"Same landing sequence.",46)
c=gold_text(c,(60,134),"ONE LANDING. TWO FRAMES.",anton(fit("ONE LANDING. TWO FRAMES.",950,88)))
d=ImageDraw.Draw(c); d.text((66,244),"Wings change in a blink. Shoot a burst, then choose.",font=bar(28),fill=(235,230,218))
pill(c,870,318,"FRAME A",fg=(244,238,226),size=24); pill(c,870,762,"FRAME B",fg=(244,238,226),size=24)
c=motes(c,20,6,0.25); fin(c,4,"slide4.jpg")

# ---- S5 where to stand
c=topo(dark(),0.2,61); c=leak(c,0.12)
lead(c,(66,92),"A setup worth trying.",46)
c=gold_text(c,(60,134),"SUN IN FRONT. WIND BEHIND.",anton(fit("SUN IN FRONT. WIND BEHIND.",950,88)))
c=sun(c,560,350,46); d=ImageDraw.Draw(c,"RGBA")
d.text((560,426),"SUN",font=bcs(28),fill=(255,226,150),anchor="mm")
cut=Image.open("shot3/ibis_cut_full.png").convert("RGBA").crop((240,360,700,1000)); cut=cut.resize((int(cut.width*0.5),int(cut.height*0.5)),Image.LANCZOS)
sh=Image.new("RGBA",c.size,(0,0,0,0)); sh.paste(cut,(560-cut.width//2,490),cut); c=Image.alpha_composite(c.convert("RGBA"),sh).convert("RGB"); d=ImageDraw.Draw(c,"RGBA")
arrow(d,(560,850),(560,975),col=(255,214,120,255),w=5,dash=True)
d.text((596,915),"BIRD LANDS INTO THE WIND",font=bcs(28),fill=(255,226,150),anchor="lm")
camera(d,512,990,1.4)
d.text((560,1085),"YOU",font=bcs(28),fill=CREAM,anchor="mm")
for x in (140,230):
    arrow(d,(x,1020),(x,800),col=(138,160,92,255),w=5)
d.text((90,1040),"WIND FROM BEHIND YOU",font=bcs(24),fill=(170,196,120),anchor="la")
d.text((64,1160),"Birds usually land into the wind.",font=corm(54),fill=(244,238,226))
d.text((64,1232),"Stand so they come toward you, sun behind them.",font=bar(28),fill=(235,230,218))
d.text((64,1274),"Rule of thumb. Read the grass and water first.",font=bar(24),fill=(190,186,172))
c=motes(c,25,7,0.3); fin(c,5,"slide5.jpg")

# ---- S6 two ways to expose
c=bgblur(3,0.5)
A=pc(3,(670,0,2156,3716),540,1350,0.95); B=pc(1,(360,0,1515,2889),540,1350,0.95)
c=paste(c,A,0,0); c=paste(c,B,540,0)
c=grad(c,0,330,0.6,0.0); c=grad(c,1000,H,0.0,0.88)
d=ImageDraw.Draw(c); d.line([(540,0),(540,1350)],fill=GOLD,width=2)
lead(c,(66,92),"Same kind of light.",46)
c=gold_text(c,(60,134),"TWO WAYS TO",anton(80)); c=gold_text(c,(60,218),"EXPOSE BACKLIGHT.",anton(80))
pill(c,32,1010,"SILHOUETTE",fg=(244,238,226),size=24); pill(c,572,1010,"RIM + DETAIL",fg=(200,236,140),size=24)
d=ImageDraw.Draw(c)
for t_,x,y in [("Dial exposure down.",40,1090),("Let shadows go dark.",40,1128),("Add exposure (+EV).",580,1090),("Spot meter the bird.",580,1128)]:
    d.text((x,y),t_,font=bar(28),fill=(244,240,230))
d.text((64,1250),"Guides disagree, so test both and watch the histogram.",font=bar(26),fill=(235,230,218))
c=motes(c,20,9,0.25); fin(c,6,"slide6.jpg")

# ---- S7 close
c=pc(3,(0,0,2973,3716),W,H,0.92); c=grad(c,0,380,0.55,0.0); c=grad(c,880,1100,0.0,0.88)
lead(c,(66,92),"The light helps. The bird decides.",46)
c=gold_text(c,(60,134),"WATCH THE BEHAVIOUR.",anton(fit("WATCH THE BEHAVIOUR.",950,96)))
y=1000
for t_ in ["1/1000 s or faster for flight","Continuous AF (AF-C)","Check the histogram. Rim light clips first."]:
    pill(c,64,y,t_,fg=(244,238,226),size=28); y+=66
d=ImageDraw.Draw(c); d.text((64,1215),"Starting points, not rules.",font=corm(46),fill=(244,238,226))
d.text((64,1282),"SAVE THIS FOR YOUR NEXT SUNRISE",font=bcs(26),fill=GOLD)
c=motes(c,30,10,0.35); fin(c,7,"slide7.jpg")
print("done")
