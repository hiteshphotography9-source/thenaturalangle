import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
import ref2
from ref2 import anton,bc,bcs,bar,barm,corm,TEX,CREAM,GOLD,BG,wrap_text
W,H=1080,1350
T=TEX[:H]
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
P={k:Image.open(U+f+"-image.jpg").convert("RGB") for k,f in zip(range(1,7),["364811ee","0563f8ac","260a7220","ce145a99","13adec9a","5b5b6505"])}
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
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save("tiger/"+name,quality=95)
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

# ---- S1 (title kept clear of the face)
c=crop(1,(0,0,1,1),W,H,dim=0.74); c=grad(c,0,520,0.6,0.0); c=grad(c,1090,H,0.0,0.8)
lead(c,(66,84),"Kishanpur, April.",66)
c=gold_text(c,(60,150),"SHE WAS",anton(168)); c=gold_text(c,(60,320),"ALONE.",anton(168))
d=ImageDraw.Draw(c)
d.text((66,1148),"Then something changed.",font=corm(70),fill=(244,238,226))
d.text((66,1262),"WHAT THESE PHOTOGRAPHS REVEAL ABOUT TIGER FAMILY LIFE.",font=bcs(25),fill=GOLD)
header(c,1); finish(c,"slide1.jpg")

# ---- S2
c=extend(3,(0,0.0,1,1.0),500,720); lead(c,(66,92),"Later, at the water,",64)
c=gold_text(c,(60,150),"THE CUBS",anton(130)); c=gold_text(c,(60,280),"WERE THERE.",anton(130))
c=grad(c,1190,H,0.0,0.55)
d=ImageDraw.Draw(c)
f=bcs(26); ta=d.textlength("ALONE",font=f); tb=d.textlength("WITH CUBS",font=f); tw=ta+tb+96; yy=1130
d.rounded_rectangle([64,yy,64+tw,yy+44],radius=4,fill=(14,15,13)); d.text((81,yy+7),"ALONE",font=f,fill=GOLD); xa=81+ta+16
d.line([(xa,yy+22),(xa+40,yy+22)],fill=GOLD,width=3); d.polygon([(xa+52,yy+22),(xa+38,yy+14),(xa+38,yy+30)],fill=GOLD); d.text((xa+66,yy+7),"WITH CUBS",font=f,fill=GOLD)
for i,l in enumerate(wrapd(d,"A tigress may spend much of her time alone. But raising cubs changes her social world completely.",bar(26),940)): d.text((64,1204+i*34),l,font=bar(26),fill=(240,236,226))
header(c,2); finish(c,"slide2.jpg")

# ---- S3
c=extend(5,(0,0.0,1,1.0),400,720); lead(c,(66,92),"This isn't just",64)
c=gold_text(c,(60,150),"A FAMILY MOMENT.",anton(104))
c=grad(c,1100,H,0.0,0.7)
d=ImageDraw.Draw(c)
d.text((64,1130),"Tiger cubs depend heavily on their mother while they are young.",font=bcs(30),fill=GOLD)
facts(c,[("FOOD","A tigress must raise her kill rate by about 50% to feed her cubs."),("PROTECTION","Young cubs are vulnerable. Other tigers can be a threat."),("LEARNING","Play, watching and practice build their skills.")],1190)
header(c,3); finish(c,"slide3.jpg")

# ---- S4
c=crop(2,(0.30,0.0,0.8325,1.0),W,H,dim=0.8); c=grad(c,0,330,0.6,0.0); c=grad(c,1060,H,0.0,0.82)
lead(c,(66,84),"The cubs are",56)
c=gold_text(c,(60,134),"LEARNING",anton(112)); c=gold_text(c,(60,242),"TO SURVIVE.",anton(112)); d=ImageDraw.Draw(c)
d.text((64,1120),"Growing up isn't just about getting bigger.",font=bcs(34),fill=GOLD)
steps=["WATCH","FOLLOW","PRACTISE","LEARN"]; sx=64; sy=1190
for k,s_ in enumerate(steps):
    w_=d.textlength(s_,font=bcs(28))+36
    d.rectangle([sx,sy,sx+w_,sy+46],outline=GOLD,width=2); d.text((sx+18,sy+8),s_,font=bcs(28),fill=CREAM); sx+=w_
    if k<3: d.line([(sx+8,sy+23),(sx+34,sy+23)],fill=GOLD,width=3); d.polygon([(sx+42,sy+23),(sx+30,sy+15),(sx+30,sy+31)],fill=GOLD); sx+=50
d.text((64,1262),"TIGERS TOGETHER IN THE WATER. WHAT SCIENCE SAYS ABOUT CUBS, NOT WHAT THIS FRAME PROVES.",font=bc(20),fill=(190,186,176))
header(c,4); finish(c,"slide4.jpg")

# ---- S5
c=crop(4,(0,0,1,1),W,H,dim=0.62); c=grad(c,0,420,0.62,0.0); c=grad(c,1020,H,0.0,0.88)
lead(c,(66,78),"But this",60)
c=gold_text(c,(60,142),"WON'T LAST",anton(112)); c=gold_text(c,(60,262),"FOREVER.",anton(112)); d=ImageDraw.Draw(c)
d.text((64,1052),"Cubs eventually become independent and leave to establish their own lives.",font=bar(26),fill=(240,236,226))
steps=[("DEPENDENT","Rely on their mother"),("LEARNING","About 18 to 24 months with her"),("INDEPENDENT","Disperse at about 2 to 3 years")]
cw=(W-128-2*40)/3
for k,(a,b) in enumerate(steps):
    x=64+k*(cw+40); y=1130
    d.line([(x,y),(x+cw,y)],fill=GOLD if k==2 else (150,146,134),width=4)
    d.text((x,y+14),a,font=anton(36),fill=GOLD if k==2 else CREAM)
    d.text((x,y+66),b,font=bar(22),fill=(215,210,198))
    if k<2: d.polygon([(x+cw+30,y+2),(x+cw+14,y-8),(x+cw+14,y+12)],fill=GOLD)
header(c,5); finish(c,"slide5.jpg")

# ---- S6
c=crop(6,(0,0,1,1),W,H); c=grad(c,0,330,0.55,0.0); c=grad(c,1060,H,0.0,0.85)
c=gold_text(c,(60,62),"THIS IS HOW A",anton(84)); c=gold_text(c,(60,150),"TIGER LEARNS",anton(84)); c=gold_text(c,(60,238),"TO BE A TIGER.",anton(84)); d=ImageDraw.Draw(c)
d.text((64,1100),"For a young tiger, growing up isn't just about surviving.",font=corm(40),fill=(244,238,226))
d.text((64,1150),"It's about learning how to survive.",font=corm(40),fill=(244,238,226))
d.text((64,1222),"Wildlife isn't just about what you see. It's about understanding what you're watching.",font=bar(23),fill=(225,220,208))
d.text((64,1288),"SAVE THIS FOR YOUR NEXT SAFARI",font=bcs(26),fill=GOLD)
d.text((W-64-d.textlength("THE NATURAL ANGLE",font=bcs(22)),1292),"THE NATURAL ANGLE",font=bcs(22),fill=(200,196,184))
finish(c,"slide6.jpg",vig=0.12)
print("done")
