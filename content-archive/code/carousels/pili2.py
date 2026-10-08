import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
import ref2
from ref2 import anton,bc,bcs,bar,barm,corm,TEX,CREAM,GOLD,BG,wrap_text
W,H=1080,1350
T=TEX[:H]
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
_f={5:"aeee4a0a",14:"454eb397",8:"a4bcbe52",9:"4d5819bf",2:"05008004",12:"3977faf4",18:"bc299d50",19:"0584b356"}
P={k:Image.open(U+v+"-image.jpg").convert("RGB") for k,v in _f.items()}
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
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save("pili2/"+name,quality=95)
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

N=9
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


def fb(k,f): w,h=P[k].size; return (f[0]*w,f[1]*h,f[2]*w,f[3]*h)
def pcf(k,f,w,h,dim=1.0): return pc(k,fb(k,f),w,h,dim)
def c45(k,fy=0.5,dim=0.97):
    w,h=P[k].size; ch=min(h,w/0.8); cw=ch*0.8; y0=(h-ch)*fy; x0=(w-cw)/2
    return pc(k,(x0,y0,x0+cw,y0+ch),W,H,dim)
def ext3(k,f,y,ph,dim=0.97):
    im=pcf(k,f,W,ph,dim); pa=np.array(im); top,bot=y,H-y-ph
    pad=cv2.copyMakeBorder(pa,top,bot,0,0,cv2.BORDER_REPLICATE)
    bl=cv2.GaussianBlur(pad,(0,0),sigmaX=60,sigmaY=14); bl=cv2.GaussianBlur(bl,(0,0),20).astype(np.float32)*0.6
    mk=np.zeros((H,W),np.float32); mk[y:y+ph]=1; fe=70
    for i in range(fe): mk[y+i]=np.minimum(mk[y+i],i/fe)
    if bot>0:
        for i in range(fe): mk[y+ph-1-i]=np.minimum(mk[y+ph-1-i],i/fe)
    out=pad.astype(np.float32)*mk[:,:,None]+bl*(1-mk[:,:,None])
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))
def two(c,l1,l2,y=134,cap=86):
    s_=min(fit(l1,950,cap),fit(l2,950,cap)); c=gold_text(c,(60,y),l1,anton(s_)); return gold_text(c,(60,y+int(s_*1.1)),l2,anton(s_))
def lines(c,x,y,ls,font=None,fill=(244,240,230),gap=42):
    d=ImageDraw.Draw(c); font=font or bar(30)
    for k,l in enumerate(ls): d.text((x,y+k*gap),l,font=font,fill=fill)

# S1 hook
c=c45(5,1.0); c=grad(c,0,430,0.7,0.0); c=grad(c,1200,H,0.0,0.4)
lead(c,(66,92),"Part 2. The road was empty.",46); c=gold_text(c,(60,134),"THEN SOMETHING MOVED.",anton(fit("THEN SOMETHING MOVED.",950,96)))
pill(c,64,1240,"A SIGHTING IN 9 FRAMES",fg=(244,238,226),size=28); swipe(c,1262)
c=motes(c,35,3,0.35); fin(c,1,"slide1.jpg")

# S2 it saw us first
c=ext3(14,(0.26,0.0997,0.822,0.8416),300,1000)
lead(c,(66,92),"We were scanning for stripes.",46); c=gold_text(c,(60,134),"IT SAW US FIRST.",anton(fit("IT SAW US FIRST.",950,92)))
lines(c,66,244,["Stripes vanish in leaves. Look for the eyes."],bar(28),(235,230,218))
c=motes(c,25,4,0.3); fin(c,2,"slide2.jpg")

# S3 road is its path
c=ext3(8,(0,0,1,0.704),400,950)
lead(c,(66,92),"Then it chose the road.",46); c=gold_text(c,(60,134),"THE ROAD IS ITS PATH.",anton(fit("THE ROAD IS ITS PATH.",950,92)))
lines(c,66,254,["Roads are easy walking.","In lynx and wolves, roads are also scent-marking routes.","Tigers may use them the same way."],bar(28),(244,240,230),38)
tinylabel(c,"From studies of lynx (Krofel 2017) and wolves (Bojarska 2020).",376,66)
c=motes(c,20,5,0.25); fin(c,3,"slide3.jpg")

# S4 roar or yawn
c=c45(9,0.0); c=grad(c,0,520,0.65,0.0); c=grad(c,1200,H,0.0,0.3)
lead(c,(66,92),"A tiger opens its mouth.",46); c=gold_text(c,(60,134),"ROAR OR YAWN?",anton(fit("ROAR OR YAWN?",950,100)))
lines(c,66,262,["Look at the eyes.","Then tell me in the comments."],bar(30),(244,240,230),44)
c=motes(c,20,6,0.25); fin(c,4,"slide4.jpg")

# S5 focus on eyes
c=c45(2,1.0); c=grad(c,0,520,0.6,0.0); c=grad(c,1120,H,0.0,0.6)
lead(c,(66,92),"Then it looked straight at us.",46); c=gold_text(c,(60,134),"FOCUS ON THE EYES.",anton(fit("FOCUS ON THE EYES.",950,92)))
lines(c,66,1200,["Nearest eye sharp. Short burst."],corm(50),(244,238,226)); lines(c,66,1262,["Move less. Shoot more."],bar(28),(235,230,218))
c=motes(c,25,7,0.3); fin(c,5,"slide5.jpg")

# S6 crowd
c=c45(12,0.5); c=grad(c,0,600,0.78,0.0); c=grad(c,1250,H,0.0,0.3)
lead(c,(66,92),"Then the crowd arrived.",46); c=two(c,"GIVE THE TIGER","THE ROAD.",134,96)
y=800
for t_ in ["500 M BETWEEN VEHICLES","15 MIN MAX AT A SIGHTING","KEEP YOUR DISTANCE"]:
    w_=ImageDraw.Draw(c).textlength(t_,font=bcs(24))+44; pill(c,int(1030-w_),y,t_,fg=(200,236,140),size=24); y+=62
d=ImageDraw.Draw(c); d.text((1016,y+10),"NTCA guidance. Rules vary by reserve.",font=bc(21),fill=(220,214,200),anchor="ra")
c=motes(c,15,8,0.2); fin(c,6,"slide6.jpg")

# S7 deer
c=ext3(18,(0.40,0.2475,0.90,0.942),300,1000)
lead(c,(66,92),"And the forest was watching too.",46); c=gold_text(c,(60,134),"EVERY EYE WAS ON US.",anton(fit("EVERY EYE WAS ON US.",950,92)))
lines(c,66,244,["A deer behind the ferns. Big ears, wide eyes."],bar(28),(235,230,218))
c=motes(c,25,9,0.3); fin(c,7,"slide7.jpg")

# S8 find the owl
c=c45(19,0.5); c=grad(c,0,520,0.8,0.0); c=grad(c,1150,H,0.0,0.35)
lead(c,(66,92),"Quick game.",46); c=gold_text(c,(60,134),"FIND THE OWL.",anton(fit("FIND THE OWL.",950,100)))
lines(c,66,262,["It is asleep. Swipe for the answer."],bar(30),(244,240,230))
c=motes(c,15,10,0.2); fin(c,8,"slide8.jpg")

# S9 reveal + close
c=c45(19,0.5); c=grad(c,0,420,0.6,0.0); c=grad(c,1050,H,0.0,0.75)
ox,oy=int(0.4125*W),int(0.6*H)
# lens
zoom=pcf(19,(0.319,0.52,0.506,0.67),380,380,1.12)
msk=Image.new("L",(380,380),0); ImageDraw.Draw(msk).ellipse([0,0,379,379],fill=255)
lx,ly=800,520
d=ImageDraw.Draw(c,"RGBA"); d.line([(ox+30,oy-40),(lx-150,ly+150)],fill=GOLD+(255,),width=3)
d.ellipse([ox-70,oy-70,ox+70,oy+70],outline=GOLD+(255,),width=4)
c.paste(zoom,(lx-190,ly-190),msk); d=ImageDraw.Draw(c); d.ellipse([lx-190,ly-190,lx+190,ly+190],outline=GOLD,width=6)
lead(c,(66,92),"A small owl, asleep in a stump.",46); c=gold_text(c,(60,134),"THERE IT IS.",anton(fit("THERE IT IS.",950,100)))
d=ImageDraw.Draw(c); d.text((64,1110),"That was Part 2.",font=corm(54),fill=(244,238,226))
lines(c,64,1180,["The tiger photos are of different tigers,","ordered to tell one sighting."],bar(26),(235,230,218),34)
pill(c,64,1262,"SAVE THIS FOR YOUR NEXT SAFARI",fg=(244,238,226),size=22)
c=motes(c,15,11,0.2); fin(c,9,"slide9.jpg")
print("done")
