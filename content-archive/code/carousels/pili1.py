import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
import ref2
from ref2 import anton,bc,bcs,bar,barm,corm,TEX,CREAM,GOLD,BG,wrap_text
W,H=1080,1350
T=TEX[:H]
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
_f={13:"c31da8f7",11:"f9c98082",17:"5aa8c4c4",10:"3b5f4f8a",16:"56ba1637",3:"9f1b458b",4:"7c0877ae",7:"271a9e6f"}
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
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save("pili1/"+name,quality=95)
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


DD={13:(2000,1333),11:(1333,2000),17:(1600,2000),10:(1600,2000),16:(2000,1345),3:(1600,2000),4:(1600,2000),7:(2000,1428)}
def pcd(k,box,w,h,dim=1.0):
    sx=P[k].width/DD[k][0]; sy=P[k].height/DD[k][1]
    return pc(k,(box[0]*sx,box[1]*sy,box[2]*sx,box[3]*sy),w,h,dim)
def ext2(k,dbox,y,ph,dim=0.95):
    im=pcd(k,dbox,W,ph,dim); pa=np.array(im); top,bot=y,H-y-ph
    pad=cv2.copyMakeBorder(pa,top,bot,0,0,cv2.BORDER_REPLICATE)
    bl=cv2.GaussianBlur(pad,(0,0),sigmaX=60,sigmaY=14); bl=cv2.GaussianBlur(bl,(0,0),20).astype(np.float32)*0.6
    mk=np.zeros((H,W),np.float32); mk[y:y+ph]=1; fe=70
    for i in range(fe): mk[y+i]=np.minimum(mk[y+i],i/fe); mk[y+ph-1-i]=np.minimum(mk[y+ph-1-i],i/fe)
    out=pad.astype(np.float32)*mk[:,:,None]+bl*(1-mk[:,:,None])
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8))
def two(c,l1,l2,y=134,cap=86):
    s_=min(fit(l1,950,cap),fit(l2,950,cap)); c=gold_text(c,(60,y),l1,anton(s_)); return gold_text(c,(60,y+int(s_*1.1)),l2,anton(s_))

# ---- S1 cover
c=pcd(13,(307,0,1373,1333),W,H,0.95); c=grad(c,0,430,0.7,0.0); c=grad(c,1150,H,0.0,0.5)
lead(c,(66,92),"Pilibhit Tiger Reserve. Part 1.",46)
c=two(c,"WHO LIVES ALONG","THIS ROAD?",134,104)
pill(c,64,1240,"8 FRAMES FROM THE TERAI",fg=(244,238,226),size=28); swipe(c,1262)
c=motes(c,45,3,0.4); c=leak(c,0.18); fin(c,1,"slide1.jpg")

# ---- S2 map
c=topo(dark(),0.18,71); c=leak(c,0.1)
lead(c,(66,92),"Where is it?",46); c=two(c,"A TERAI FOREST","ON THE NEPAL BORDER.",134,90)
ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
# terai belt
d.ellipse([60,590,1020,800],fill=(138,160,92,50)); 
ov=ov.filter(ImageFilter.GaussianBlur(14)); c=Image.alpha_composite(c.convert("RGBA"),ov).convert("RGB"); d=ImageDraw.Draw(c,"RGBA")
# foothills
pts=[(64,470),(150,410),(215,450),(310,380),(400,445),(500,395),(580,450),(690,385),(770,445),(870,400),(960,450),(1016,420)]
d.line(pts,fill=GOLD+(255,),width=3,joint="curve")
d.text((64,490),"HIMALAYAN FOOTHILLS",font=bcs(22),fill=(190,184,168))
for x in range(64,980,34): d.line([(x,560),(x+18,560)],fill=(200,196,184,200),width=2)
d.text((1016,520),"NEPAL",font=bcs(22),fill=(190,184,168),anchor="ra"); d.text((1016,578),"INDIA",font=bcs(22),fill=(190,184,168),anchor="ra")
d.text((64,620),"TERAI: WET GRASSLAND AND SAL FOREST",font=bcs(22),fill=(170,196,120))
# rivers
RIV=(110,170,196,255)
sh=[(960,600),(905,650),(880,720),(850,790),(800,860),(720,930)]; d.line(sh,fill=RIV,width=4,joint="curve"); d.text((930,720),"SHARDA",font=bcs(22),fill=RIV)
gm=[(540,700),(520,760),(535,820),(500,880),(470,940),(420,990)]; d.line(gm,fill=RIV,width=3,joint="curve"); d.text((350,860),"GOMTI BEGINS HERE",font=bcs(22),fill=RIV,anchor="ra")
# marker pulse
for r,a in [(110,30),(80,55),(52,90)]: d.ellipse([540-r,700-r,540+r,700+r],outline=GOLD+(a,),width=3)
d.ellipse([524,684,556,716],fill=GOLD+(255,)); d.text((540,745),"PILIBHIT",font=bcs(30),fill=CREAM,anchor="mt")
d.text((64,1010),"GANGETIC PLAIN",font=bcs(22),fill=(190,184,168))
facts(c,[("AREA","730 sq km"),("NOTIFIED","June 2014"),("HABITAT","Sal forest, tall grass, swamp")],1085)
tinylabel(c,"Schematic, not to scale. Figures: NTCA, WII.",1290)
c=motes(c,25,4,0.3); fin(c,2,"slide2.jpg")

# ---- S3 peacock
c=pcd(11,(0,334,1333,2000),W,H,0.97); c=grad(c,0,520,0.62,0.0); c=grad(c,1150,H,0.0,0.35)
lead(c,(66,92),"Before the jeeps.",46); c=gold_text(c,(60,134),"THE ROAD WAKES FIRST.",anton(fit("THE ROAD WAKES FIRST.",950,92)))
d=ImageDraw.Draw(c); d.text((66,250),"A peacock crosses a misty road.",font=bar(32),fill=(244,240,230)); d.text((66,296),"Small subject, big space. Let the forest frame it.",font=bar(32),fill=(244,240,230))
pill(c,64,350,"INDIAN PEAFOWL, INDIA'S NATIONAL BIRD",fg=(200,236,140),size=24)
c=motes(c,30,5,0.3); fin(c,3,"slide3.jpg")

# ---- S4 deer
c=pcd(17,(0,0,1600,2000),W,H,0.97); c=grad(c,0,520,0.6,0.0); c=grad(c,1100,H,0.0,0.5)
lead(c,(66,92),"Five deer species share this forest.",46); c=two(c,"EVERY TIGER","NEEDS A MENU.",134,92)
y=640
for t_ in ["SWAMP DEER (BARASINGHA)","SPOTTED DEER (CHITAL)","HOG DEER","SAMBAR","BARKING DEER"]:
    pill(c,64,y,t_,fg=(200,236,140),size=26); y+=64
d=ImageDraw.Draw(c); 
for k,l in enumerate(["Prey decides how many","tigers a forest can hold."]): d.text((64,1160+k*48),l,font=corm(46),fill=(244,238,226))
tinylabel(c,"A spotted deer (chital) stag, photographed in Pilibhit.",1296)
c=motes(c,20,6,0.25); fin(c,4,"slide4.jpg")

# ---- S5 wet side
c=bgblur(10,0.5)
A=pcd(10,(350,0,1379,2000),540,1050,0.95); B=pcd(16,(445,0,1137,1345),540,1050,0.95)
c=paste(c,A,0,300); c=paste(c,B,540,300)
d=ImageDraw.Draw(c); d.line([(540,300),(540,1350)],fill=GOLD,width=2); d.line([(0,300),(1080,300)],fill=GOLD,width=2)
lead(c,(66,92),"Rivers feed this forest.",46); c=gold_text(c,(60,134),"THE WET SIDE.",anton(80))
d=ImageDraw.Draw(c); d.text((66,232),"Sharda, Chuka, Mala Khannot. The Gomti begins here.",font=bar(28),fill=(235,230,218))
pill(c,32,322,"OTTER WITH ITS CATCH",fg=(244,238,226),size=24); pill(c,572,322,"CROCODILE",fg=(200,236,140),size=24)
c=motes(c,18,7,0.25); fin(c,5,"slide5.jpg")

# ---- S6 owl
c=pcd(3,(0,0,1600,2000),W,H,0.97); c=grad(c,0,300,0.55,0.0); c=grad(c,1080,H,0.0,0.7)
lead(c,(66,92),"Not every hunter is a cat.",46); c=gold_text(c,(60,134),"THE OWL THAT WINKED.",anton(fit("THE OWL THAT WINKED.",950,92)))
d=ImageDraw.Draw(c); d.text((64,1180),"Brown fish owl.",font=corm(58),fill=(244,238,226)); d.text((64,1252),"It lives near water and hunts fish, frogs and crabs.",font=bar(28),fill=(235,230,218))
c=motes(c,20,8,0.25); fin(c,6,"slide6.jpg")

# ---- S7 stripes
c=ext2(4,(0,0,1600,1407),250,950,0.97); c=grad(c,1150,H,0.0,0.55)
lead(c,(66,92),"Every tiger is different.",46); c=two(c,"NO TWO TIGERS WEAR","THE SAME STRIPES.",134,84)
d=ImageDraw.Draw(c)
for k,l in enumerate(["Researchers match stripe patterns in","camera-trap photos to tell tigers apart."]): d.text((64,1226+k*40),l,font=bar(28),fill=(244,240,230))
c=motes(c,20,9,0.25); fin(c,7,"slide7.jpg")

# ---- S8 numbers
c=topo(dark(),0.2,83); c=leak(c,0.1)
lead(c,(66,92),"Counted by their stripes.",46); c=gold_text(c,(60,134),"FROM 25 TO 65.",anton(fit("FROM 25 TO 65.",950,110)))
d=ImageDraw.Draw(c,"RGBA"); base=1000
d.rounded_rectangle([190,base-192,420,base],radius=10,fill=(150,130,80,255)); d.rounded_rectangle([560,base-500,790,base],radius=10,fill=GOLD+(255,))
d.text((305,base-192-18),"25",font=anton(120),fill=CREAM,anchor="ms"); d.text((675,base-500-18),"65",font=anton(120),fill=GOLD,anchor="ms")
d.text((305,base+34),"2014",font=bcs(34),fill=CREAM,anchor="mm"); d.text((675,base+34),"2018",font=bcs(34),fill=CREAM,anchor="mm")
arrow(d,(440,base-215),(540,base-330),col=(255,214,120,255),w=4,dash=True)
d.line([(120,base),(960,base)],fill=(200,196,184,200),width=2)
for k in range(5): paw(d,150+k*60,base+130-k*8,26,fill=(226,184,104,70-k*8))
d.text((64,1150),"Estimates reported for the reserve.",font=bar(30),fill=(244,240,230))
d.text((64,1196),"Pilibhit won the TX2 award in November 2020",font=bar(30),fill=(244,240,230)); d.text((64,1240),"for growing its tiger population.",font=bar(30),fill=(244,240,230))
tinylabel(c,"Estimates, not exact headcounts. Source: NTCA, Drishti IAS.",1296)
c=motes(c,25,10,0.3); fin(c,8,"slide8.jpg")

# ---- S9 close
c=pcd(7,(400,0,1542,1428),W,H,0.97); c=grad(c,0,430,0.62,0.0); c=grad(c,1150,H,0.0,0.7)
lead(c,(66,92),"That was part 1.",46); c=two(c,"MORE OF PILIBHIT","IN PART 2.",134,96)
pill(c,64,1250,"SAVE THIS FOR YOUR TRIP",fg=(244,238,226),size=26); pill(c,420,1250,"FOLLOW FOR PART 2",fg=(226,184,104),size=26)
c=motes(c,30,11,0.3); fin(c,9,"slide9.jpg")
print("done")
