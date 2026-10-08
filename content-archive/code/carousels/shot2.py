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
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save("shot2/"+name,quality=95)
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
D="shot/"
# --- clean frames (deer avatar + caption removed, ibis untouched above caption)
d0=cv2.imread(D+"deer_a.png"); m=np.zeros(d0.shape[:2],np.uint8); m[1386:1494,284:796]=255; m[170:460,770:1045]=255
dc=cv2.inpaint(d0,m,7,cv2.INPAINT_TELEA); DEER=Image.fromarray(cv2.cvtColor(dc,cv2.COLOR_BGR2RGB))
IB=Image.open(D+"ibis_a.png").convert("RGB")
def ibis_win(y0=35): return IB.crop((0,y0,1080,y0+1350))
def deer_win(y0=500): return DEER.crop((0,y0,1080,y0+1350))
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

# ---- S1 hook
c=ibis_win(35); c=Image.fromarray((np.array(c).astype(np.float32)*0.92).clip(0,255).astype(np.uint8)); c=grad(c,0,520,0.62,0.0); c=grad(c,1180,H,0.0,0.45)
lead(c,(66,92),"Did you know?",54)
s_=fit("THIS SHOT WAS",950,150); c=gold_text(c,(60,150),"THIS SHOT WAS",anton(s_)); c=gold_text(c,(60,150+int(s_*1.14)),"PLANNED.",anton(s_))
d=ImageDraw.Draw(c); pill(c,64,1240,"YOU CAN PLAN YOUR IMAGE.",fg=(244,238,226),size=30)
swipe(c,1262); c=motes(c,40,3,0.4); done(c,1,"slide1.jpg")

# ---- S2 deer
c=deer_win(430); c=Image.fromarray((np.array(c).astype(np.float32)*0.92).clip(0,255).astype(np.uint8)); c=grad(c,0,520,0.55,0.0); c=grad(c,780,1000,0.0,0.93)
lead(c,(66,92),"I already had",56)
c=gold_text(c,(60,150),"THESE SHOTS.",anton(fit("THESE SHOTS.",950,150)))
y=330
for t_ in ["BACKLIT SHOTS","MORNING SHOTS","SPOTTED DEER SHOTS"]:
    pill(c,64,y,t_,fg=(200,236,140),size=30); y+=74
d=ImageDraw.Draw(c); d.text((64,1150),"I wanted something new.",font=corm(60),fill=(244,238,226)); d.text((64,1226),"Something creative. Unique.",font=bar(30),fill=(235,230,218))
done(c,2,"slide2.jpg")

# ---- S3 diagram: picked a spot
c=topo(dark(),0.2,41)
lead(c,(66,92),"Before sunrise,",54); c=gold_text(c,(60,150),"I PICKED",anton(140)); c=gold_text(c,(60,290),"A SPOT.",anton(140))
panel(c,64,470,1016,1010); d=ImageDraw.Draw(c)
gy=900; d.line([(90,gy),(990,gy)],fill=(150,144,124),width=3)
camera(d,110,gy-70,1.0); d.text((140,gy+22),"ME",font=bcs(20),fill=CREAM,anchor="mm")
for k,(x,sp) in enumerate([(470,False),(540,False),(610,True),(680,True)]): egret(d,x,gy-40,1.25,col=(244,176,188) if sp else (244,240,230),spoon=sp)
d.text((505,gy+24),"EGRETS",font=bcs(20),fill=(190,184,168),anchor="mm"); d.text((645,gy+24),"SPOONBILLS",font=bcs(20),fill=(190,184,168),anchor="mm")
y=wtext(c,(64,1060),"Egrets and spoonbills were feeding in front of me.",bar(32),940)
wtext(c,(64,y+10),"Where the birds are, and where you stand, decides the shot.",bar(26),940,fill=(200,196,184))
done(c,3,"slide3.jpg")

# ---- S4 diagram: sun behind
c=topo(dark(),0.2,43)
lead(c,(66,92),"Morning light.",54); c=gold_text(c,(60,150),"SUN BEHIND",anton(130)); c=gold_text(c,(60,282),"THE BIRDS.",anton(130))
panel(c,64,470,1016,1010); c=sun(c,880,600,34); d=ImageDraw.Draw(c)
gy=900; d.line([(90,gy),(990,gy)],fill=(150,144,124),width=3)
camera(d,110,gy-70,1.0); d.text((140,gy+22),"ME",font=bcs(20),fill=CREAM,anchor="mm")
for k,(x,sp) in enumerate([(470,False),(540,False),(610,True),(680,True)]): egret(d,x,gy-40,1.25,col=(244,176,188) if sp else (244,240,230),spoon=sp)
d.text((880,650),"SUN BEHIND",font=bcs(20),fill=(250,196,120),anchor="mm")
# alignment line me -> birds -> sun
pts=[(175,gy-48),(560,gy-62),(880,632)]
for a1,b1 in zip(pts[:-1],pts[1:]):
    n=int(math.hypot(b1[0]-a1[0],b1[1]-a1[1])/16)
    for k in range(n):
        if k%2==0: d.line([(a1[0]+(b1[0]-a1[0])*k/n,a1[1]+(b1[1]-a1[1])*k/n),(a1[0]+(b1[0]-a1[0])*(k+0.6)/n,a1[1]+(b1[1]-a1[1])*(k+0.6)/n)],fill=(250,196,120),width=3)
d.rectangle([420,640,730,930],outline=(200,236,140),width=3)
th=IB.crop((120,640,860,1385)).resize((304,300)); c.paste(th,(424,644)); d=ImageDraw.Draw(c)
pill(c,430,610,"THE SHOT I WANTED",fg=(200,236,140),size=20)
pill(c,64,1060,"BIRDS IN THE MIDDLE",fg=(244,238,226),size=28)
d.text((64,1240),"Backlight turns feathers into glowing edges.",font=bar(28),fill=(225,220,208))
done(c,4,"slide4.jpg")

# ---- S5 formula
c=blurbg(ibis_win(35),0.5,26); c=topo(c,0.08,47)
lead(c,(66,110),"But here is the catch.",56)
c=gold_text(c,(60,190),"PLAN",anton(210)); d=ImageDraw.Draw(c)
c=gold_text(c,(60,420),"+ BEHAVIOUR",anton(fit("+ BEHAVIOUR",950,170))); d=ImageDraw.Draw(c)
d.line([(64,670),(1016,670)],fill=GOLD,width=4)
c=gold_text(c,(60,700),"= THE SHOT",anton(fit("= THE SHOT",950,170))); d=ImageDraw.Draw(c)
pill(c,64,980,"NO BEHAVIOUR, NO SHOT.",fg=(255,236,226),fill=(120,34,28),alpha=0.9,size=30)
d.text((64,1090),"If you don't know how the bird behaves,",font=bar(30),fill=(244,240,230)); d.text((64,1134),"you won't get it. Trust me.",font=bar(30),fill=(244,240,230))
done(c,5,"slide5.jpg")

# ---- S6 waiting
c=blurbg(ibis_win(35),0.45,30); c=topo(c,0.1,51)
lead(c,(66,92),"Then comes the hard part.",54); c=gold_text(c,(60,150),"I WAITED.",anton(160)); d=ImageDraw.Draw(c)
cx,cy,r=540,720,230
d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(210,205,190),width=4)
for k in range(60):
    a=math.radians(k*6-90); l=22 if k%5==0 else 10
    d.line([(cx+(r-8)*math.cos(a),cy+(r-8)*math.sin(a)),(cx+(r-8-l)*math.cos(a),cy+(r-8-l)*math.sin(a))],fill=(210,205,190),width=3 if k%5==0 else 2)
d.pieslice([cx-r+30,cy-r+30,cx+r-30,cy+r-30],-90,-90+300,fill=(226,184,104,),outline=None)
d.ellipse([cx-r+54,cy-r+54,cx+r-54,cy+r-54],fill=(16,15,11))
d.text((cx,cy-14),"1 HOUR",font=anton(86),fill=GOLD,anchor="mm"); d.text((cx,cy+62),"OR MORE",font=bcs(34),fill=CREAM,anchor="mm")
wtext(c,(64,1010),"This ibis flew away.",bar(34),940,fill=(244,240,230)); d.text((64,1066),"It came back.",font=corm(70),fill=(244,238,226))
done(c,6,"slide6.jpg")

# ---- S7 payoff close crop
im=IB.crop((0,385,800,1385)).resize((1080,1350),Image.LANCZOS); c=Image.fromarray((np.array(im).astype(np.float32)*0.95).clip(0,255).astype(np.uint8))
c=grad(c,0,430,0.62,0.0); c=grad(c,1190,H,0.0,0.5)
lead(c,(66,92),"Just before landing,",54); c=gold_text(c,(60,150),"WINGS SPREAD.",anton(fit("WINGS SPREAD.",950,120))); d=ImageDraw.Draw(c)
pill(c,64,300,"FLAPPING",fg=(200,236,140),size=30)
d.text((64,1150),"5-10 SHOTS.",font=anton(70),fill=GOLD); d.text((64,1242),"This was the best one.",font=bar(28),fill=(244,240,230))
c=motes(c,35,8,0.4); done(c,7,"slide7.jpg")

# ---- S8 close
c=ibis_win(35); c=Image.fromarray((np.array(c).astype(np.float32)*0.8).clip(0,255).astype(np.uint8)); c=grad(c,0,560,0.78,0.0); c=grad(c,1200,H,0.0,0.5)
lead(c,(66,92),"All you need:",56)
c=gold_text(c,(60,150),"PLAN YOUR SHOT.",anton(fit("PLAN YOUR SHOT.",950,118))); c=gold_text(c,(60,290),"KNOW THE",anton(fit("KNOW THE BEHAVIOUR.",950,118))); c=gold_text(c,(60,404),"BEHAVIOUR.",anton(fit("KNOW THE BEHAVIOUR.",950,118)))
pill(c,64,1190,"FULL VIDEO: 8 CREATIVE IDEAS",fg=(244,238,226),size=28)
d=ImageDraw.Draw(c); d.text((64,1270),"SAVE THIS FOR YOUR NEXT SHOOT",font=bcs(26),fill=GOLD)
c=motes(c,40,12,0.4); done(c,8,"slide8.jpg")
print("done")
