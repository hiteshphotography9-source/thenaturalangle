import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
import ref2
from ref2 import anton,bc,bcs,bar,barm,corm,TEX,CREAM,GOLD,BG,wrap_text
W,H=1080,1350
T=TEX[:H]
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
P={k:Image.open(U+f+"-image.jpg").convert("RGB") for k,f in zip(range(1,10),["5f01d554","0a195c9b","e10bf14f","9fdad865","2584e54f","a35362e9","00927760","611de240","5dfbe20e"])}
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
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save("mausi/"+name,quality=95)
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


MOSS=(138,160,92); RUST=(196,84,64)
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
def progress(c,i,n=6):
    d=ImageDraw.Draw(c); gw=(W-128-5*10)/6
    for k in range(n): d.rounded_rectangle([64+k*(gw+10),1336,64+k*(gw+10)+gw,1341],radius=2,fill=GOLD if k<i else (70,68,60))
def chip(c,x,y,t,fill,fg=(20,16,8),size=24):
    d=ImageDraw.Draw(c); f=bcs(size); w_=d.textlength(t,font=f)+34
    d.rounded_rectangle([x,y,x+w_,y+size+20],radius=(size+20)//2,fill=fill); d.text((x+17,y+9),t,font=f,fill=fg); return w_
def swipe(c,y=1262):
    d=ImageDraw.Draw(c); d.text((W-64-d.textlength("SWIPE",font=bcs(24))-46,y),"SWIPE",font=bcs(24),fill=GOLD)
    x=W-64-30; d.line([(x,y+14),(x+26,y+14)],fill=GOLD,width=3); d.polygon([(x+36,y+14),(x+24,y+6),(x+24,y+22)],fill=GOLD)
NOTE="PHOTOGRAPH OF A SANJAY-DUBRI TIGER. NOT THE ANIMALS IN THIS STORY."
def base_finish(c,i,name,vig=0.26):
    progress(c,i); header(c,i); finish(c,name,vig=vig)

# ---- S1
c=crop(3,(0,0,1,1),W,H,dim=0.78); c=grad(c,0,560,0.74,0.0); c=grad(c,1120,H,0.0,0.7); c=topo(c,0.07,3)
lead(c,(66,92),"In March 2022,",60)
c=gold_text(c,(60,158),"FOUR CUBS",anton(150)); c=gold_text(c,(60,330),"LOST THEIR MOTHER.",anton(fit("LOST THEIR MOTHER.",950,110)))
d=ImageDraw.Draw(c)
d.text((66,1180),"Then an aunt stepped in.",font=corm(64),fill=(244,238,226))
swipe(c,1262); tinylabel(c,NOTE,1304)
c=motes(c,60,5,0.5); c=leak(c,0.16)
base_finish(c,1,"slide1.jpg")

# ---- S2: P8 night grade, photo pushed down for text room
c=extend(8,(0.38,0.12,1.0,1.0),560,790,dim=1.15)
a=np.array(c).astype(np.float32); g=a.mean(2,keepdims=True); a=g*0.35+a*0.65; a*=np.array([0.78,0.9,1.12],np.float32)
c=Image.fromarray(np.clip(a,0,255).astype(np.uint8)); c=grad(c,0,420,0.5,0.0); c=grad(c,1170,H,0.0,0.82); c=topo(c,0.06,7,(150,180,230))
c=gold_text(c,(60,92),"16 MARCH",anton(124)); c=gold_text(c,(60,214),"2022.",anton(124)); d=ImageDraw.Draw(c)
chip(c,64,372,"T18",(226,184,104))
for i,l in enumerate(wrapd(d,"A tigress was found injured beside a railway track in the reserve's core area.",bar(27),940)): d.text((64,444+i*36),l,font=bar(27),fill=(244,240,230))
d.text((64,1190),"She died the next evening.",font=corm(50),fill=(244,238,226))
d.text((64,1252),"Four cubs, 8 to 9 months old, were left behind.",font=bar(26),fill=(235,230,218))
tinylabel(c,"PHOTOGRAPH OF A SANJAY-DUBRI TIGER, GRADED DARK FOR MOOD. NOT T18.",1304)
base_finish(c,2,"slide2.jpg")

# ---- S3: graphic slide
c=Image.fromarray(np.full((H,W,3),(14,15,13),np.uint8)); c=topo(c,0.2,11)
lead(c,(66,92),"After their mother died,",54)
c=gold_text(c,(60,160),"THEN THERE",anton(120)); c=gold_text(c,(60,282),"WERE 3.",anton(250)); d=ImageDraw.Draw(c)
for k in range(4):
    cx=140+k*220; cy=760
    if k<3: paw(d,cx,cy,86,fill=GOLD)
    else:
        paw(d,cx,cy,86,fill=(60,40,34)); d.line([(cx-70,cy-90),(cx+70,cy+90)],fill=RUST,width=9); d.line([(cx-70,cy+90),(cx+70,cy-90)],fill=RUST,width=9)
chip(c,64,930,"ONE CUB WAS KILLED BY AN ADULT TIGER",RUST,fg=(255,244,238),size=26)
for i,l in enumerate(wrapd(d,"The three survivors were left without their mother. Forest teams began monitoring them.",bar(30),940)): d.text((64,1040+i*42),l,font=bar(30),fill=(240,236,226))
d.text((64,1296),"SOURCE: PTI / DECCAN HERALD, AUG 2022",font=bc(21),fill=(150,146,134))
base_finish(c,3,"slide3.jpg")

# ---- S4: P3 tight crop
c=crop(3,(450/1600,430/2000,1150/1600,1305/2000),W,H,dim=0.82); c=grad(c,0,470,0.78,0.0); c=grad(c,1130,H,0.0,0.6); c=topo(c,0.06,13)
c=gold_text(c,(60,92),"10 DAYS",anton(150)); c=gold_text(c,(60,242),"LATER.",anton(150)); d=ImageDraw.Draw(c)
for i,l in enumerate(wrapd(d,"The orphans were found with T28, their mother's sister.",bar(29),420)): d.text((64,440+i*38),l,font=bar(29),fill=(244,240,230))
xx=64; xx+=chip(c,xx,540,"T18",(70,68,60),fg=(230,226,214))+14
d=ImageDraw.Draw(c); d.line([(xx,562),(xx+40,562)],fill=GOLD,width=3); d.text((xx+52,548),"SISTERS",font=bcs(22),fill=GOLD); xx+=52+d.textlength("SISTERS",font=bcs(22))+14
d.line([(xx,562),(xx+40,562)],fill=GOLD,width=3); xx+=54; chip(c,xx,540,"T28 MAUSI",(226,184,104))
tinylabel(c,NOTE,1304)
base_finish(c,4,"slide4.jpg")

# ---- S5: P8 extend, 4+3
c=extend(8,(0.38,0.12,1.0,1.0),520,830,dim=0.84); c=grad(c,0,520,0.4,0.0); c=grad(c,1190,H,0.0,0.7)
c=gold_text(c,(60,92),"SEVEN CUBS.",anton(132)); c=gold_text(c,(60,222),"ONE TIGRESS.",anton(132)); d=ImageDraw.Draw(c)
for k in range(7):
    paw(d,100+k*92,420,34,fill=GOLD if k<4 else None,outline=None if k<4 else MOSS,w=4) if k<4 else None
    if k>=4: paw(d,100+k*92,420,34,fill=MOSS)
d.text((64,468),"HER OWN FOUR  +  THREE ORPHANS",font=bcs(24),fill=GOLD)
d.text((64,1210),"By August 2022 the orphans hunted on their own.",font=bar(27),fill=(244,240,230))
d.text((64,1248),"Forest staff watched over them on elephant-back and provided prey.",font=bar(23),fill=(215,210,198))
tinylabel(c,NOTE,1304)
base_finish(c,5,"slide5.jpg")

# ---- S6: P8 hero, photo block on top, calm text band below
c=extend(8,(0.30,0.0,1.0,1.0),0,1100,dim=1.0); c=grad(c,0,300,0.45,0.0); c=grad(c,1110,H,0.0,0.78); c=motes(c,45,21,0.45); c=leak(c,0.1)
d=ImageDraw.Draw(c)
d.text((64,100),"SANJAY-DUBRI TIGER RESERVE",font=bcs(30),fill=GOLD)
d.text((64,1180),"Tigers are famously solitary.",font=corm(54),fill=(244,238,226))
d.text((64,1240),"This family was not.",font=corm(54),fill=(244,238,226))
d.text((64,1306),"HAD YOU HEARD OF MAUSI BEFORE?",font=bcs(28),fill=GOLD)
progress(c,6); d=ImageDraw.Draw(c); d.text((W-64-d.textlength("THE NATURAL ANGLE",font=bcs(22)),1308),"THE NATURAL ANGLE",font=bcs(22),fill=(200,196,184))
finish(c,"slide6.jpg",vig=0.12)
print("done")
