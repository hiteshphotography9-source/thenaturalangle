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
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save("dubri/"+name,quality=95)
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

# ---- S1: P1 growl, title in the grass above the ears
c=crop(1,(0,0,1,1),W,H,dim=0.8); c=grad(c,0,430,0.62,0.0); c=grad(c,1150,H,0.0,0.7)
lead(c,(66,84),"This forest changed the history of",58)
s=fit("WHITE TIGERS.",950,200); c=gold_text(c,(60,150),"WHITE TIGERS.",anton(s)); d=ImageDraw.Draw(c)
d.text((66,1248),"And the story begins in 1951.",font=corm(60),fill=(244,238,226))
tinylabel(c,"SANJAY-DUBRI TIGER RESERVE, MADHYA PRADESH",1322)
header(c,1); finish(c,"slide1.jpg")

# ---- S2: P9 forest path, 1951 above the canopy
im=P[9]; sc=1080/im.width; ph=im.resize((1080,round(im.height*sc)),Image.LANCZOS)
off=270; c=ph.crop((0,off,1080,off+H)); c=Image.fromarray((np.array(c).astype(np.float32)*0.86).clip(0,255).astype(np.uint8))
c=grad(c,0,560,0.78,0.0)
c=gold_text(c,(58,96),"1951.",anton(250)); d=ImageDraw.Draw(c)
for i,l in enumerate(wrapd(d,"A white tiger cub was found in the forests of this landscape, and captured by the Maharaja of Rewa.",bar(30),900)): d.text((64,430+i*40),l,font=bar(30),fill=(244,240,230))
tinylabel(c,"PHOTOGRAPHED IN SANJAY-DUBRI TODAY",1322)
header(c,2); finish(c,"slide2.jpg")

# ---- S3: P7 peek, text on the trunk
c=crop(7,(0,0,1,1),W,H,dim=0.9); c=hgrad(c,0,560,0.66,0.0); c=grad(c,1150,H,0.0,0.6)
lead(c,(66,120),"The tiger was a white cub.",54)
c=gold_text(c,(60,196),"HIS NAME",anton(112)); c=gold_text(c,(60,312),"WAS",anton(112)); c=gold_text(c,(60,428),"MOHAN.",anton(150)); d=ImageDraw.Draw(c)
for i,l in enumerate(wrapd(d,"Captured in 1951. He became the ancestor of most white tigers in zoos worldwide.",bar(27),400)): d.text((64,640+i*36),l,font=bar(27),fill=(244,240,230))
tinylabel(c,"PHOTOGRAPHED IN SANJAY-DUBRI. THIS IS NOT MOHAN.",1322)
header(c,3); finish(c,"slide3.jpg")

# ---- S4: P5 path, lineage chain in the canopy
c=crop(5,(0,0,1,1),W,H,dim=0.8); c=grad(c,0,610,0.84,0.0); c=grad(c,1100,H,0.0,0.72)
d=ImageDraw.Draw(c)
nodes=[("MOHAN","Captured 1951"),("RADHA","First white tigers born in captivity"),("WHITE TIGERS WORLDWIDE","Most in zoos descend from this pair")]
y=92
for k,(a,b) in enumerate(nodes):
    if k==2:
        c=gold_text(c,(60,y),a,anton(fit(a,940,58)))
    else:
        c=gold_text(c,(60,y),a,anton(84))
    d=ImageDraw.Draw(c); d.text((64,y+(112 if k<2 else 80)),b,font=bar(25),fill=(235,230,218))
    if k<2:
        ax=84; ay=y+148
        d.line([(ax,ay),(ax,ay+34)],fill=GOLD,width=4); d.polygon([(ax,ay+48),(ax-11,ay+30),(ax+11,ay+30)],fill=GOLD)
    y+=186
d.text((64,1226),"A white coat is a recessive mutation in a single gene.",font=bcs(32),fill=GOLD)
tinylabel(c,"SOURCE: MP FOREST DEPARTMENT, LUO ET AL. 2013 (SLC45A2)",1322)
header(c,4); finish(c,"slide4.jpg")

# ---- S5: P4 forest, landscape line
im=P[4]; sc=1080/im.width; ph=im.resize((1080,round(im.height*sc)),Image.LANCZOS)
off=150; c=ph.crop((0,off,1080,off+H)); c=Image.fromarray((np.array(c).astype(np.float32)*0.82).clip(0,255).astype(np.uint8))
c=grad(c,0,520,0.74,0.0); c=grad(c,1090,H,0.0,0.82)
lead(c,(66,84),"Now zoom out.",60)
c=gold_text(c,(60,152),"BIGGER THAN",anton(138)); c=gold_text(c,(60,290),"ONE TIGER.",anton(138)); d=ImageDraw.Draw(c)
d.text((64,1122),"Sanjay-Dubri is part of one tiger landscape.",font=bcs(32),fill=GOLD)
names=["BANDHAVGARH","SANJAY-DUBRI","GURU GHASIDAS","PALAMAU"]; xs=[120,400,690,960]; ly=1214
d.line([(xs[0],ly),(xs[-1],ly)],fill=(150,146,134),width=3)
for k,(n,x) in enumerate(zip(names,xs)):
    hi=(k==1); r=13 if hi else 8
    d.ellipse([x-r,ly-r,x+r,ly+r],fill=GOLD if hi else (210,205,194))
    f=bcs(24) if hi else bc(23); w_=d.textlength(n,font=f)
    d.text((x-w_/2,ly+24),n,font=f,fill=GOLD if hi else (225,220,208))
d.text((64,1290),"Tigers cross from Bandhavgarh into Sanjay-Dubri through a forest corridor. (NTCA)",font=bar(22),fill=(215,210,198))
header(c,5); finish(c,"slide5.jpg")

# ---- S6: P6 hero
im=P[6]; sc=1080/im.width; ph=im.resize((1080,round(im.height*sc)),Image.LANCZOS)
off=min(270,ph.height-H); c=ph.crop((0,off,1080,off+H))
c=grad(c,0,330,0.5,0.0); c=grad(c,1130,H,0.0,0.78); d=ImageDraw.Draw(c)
d.text((64,100),"SANJAY-DUBRI TIGER RESERVE",font=bcs(30),fill=GOLD)
d.text((64,1160),"One forest. One extraordinary tiger.",font=corm(50),fill=(244,238,226))
d.text((64,1222),"A story that travelled far beyond this landscape.",font=corm(50),fill=(244,238,226))
d.text((64,1296),"HAD YOU HEARD OF MOHAN BEFORE?",font=bcs(28),fill=GOLD)
d.text((W-64-d.textlength("THE NATURAL ANGLE",font=bcs(22)),1300),"THE NATURAL ANGLE",font=bcs(22),fill=(200,196,184))
finish(c,"slide6.jpg",vig=0.12)
print("done")
