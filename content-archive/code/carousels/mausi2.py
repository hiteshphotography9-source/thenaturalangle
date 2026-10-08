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
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save("mausi2/"+name,quality=95)
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
def progress(c,i,n=10):
    d=ImageDraw.Draw(c); gw=(W-128-(n-1)*10)/n
    for k in range(n): d.rounded_rectangle([64+k*(gw+10),1336,64+k*(gw+10)+gw,1341],radius=2,fill=GOLD if k<i else (70,68,60))
def chip(c,x,y,t,fill,fg=(20,16,8),size=24):
    d=ImageDraw.Draw(c); f=bcs(size); w_=d.textlength(t,font=f)+34
    d.rounded_rectangle([x,y,x+w_,y+size+20],radius=(size+20)//2,fill=fill); d.text((x+17,y+9),t,font=f,fill=fg); return w_
def swipe(c,y=1262):
    d=ImageDraw.Draw(c); d.text((W-64-d.textlength("SWIPE",font=bcs(24))-46,y),"SWIPE",font=bcs(24),fill=GOLD)
    x=W-64-30; d.line([(x,y+14),(x+26,y+14)],fill=GOLD,width=3); d.polygon([(x+36,y+14),(x+24,y+6),(x+24,y+22)],fill=GOLD)

def header(c,i,n=10):
    d=ImageDraw.Draw(c); d.text((64,48),"THE NATURAL ANGLE",font=bcs(26),fill=(220,214,200))
    cnt=f"{i}/{n}"; tw=d.textlength(cnt,font=bcs(26))+44
    d.rounded_rectangle([W-64-tw,34,W-64,82],radius=24,fill=(20,20,18)); d.text((W-64-tw+22,44),cnt,font=bcs(26),fill=CREAM)
def base_finish(c,i,name,vig=0.26):
    progress(c,i); header(c,i); finish(c,name,vig=vig)
NOTE="PHOTOGRAPH OF ANOTHER SANJAY-DUBRI TIGER. NOT T18, T28 OR THE CUBS."
def wtext(c,xy,t,font,mw,fill=(244,240,230),lh=1.3):
    d=ImageDraw.Draw(c); y=xy[1]
    for l in wrapd(d,t,font,mw): d.text((xy[0],y),l,font=font,fill=fill); y+=int(font.size*lh)
    return y
def dark(): return Image.fromarray(np.full((H,W,3),(14,15,13),np.uint8))

# ---- S1
c=crop(3,(0,0,1,1),W,H,dim=0.78); c=grad(c,0,560,0.78,0.0); c=grad(c,1060,H,0.0,0.8); c=topo(c,0.07,3)
lead(c,(66,88),"Sanjay-Dubri, 2022. A true story.",52)
for k,l in enumerate(["A TIGRESS RAISED","HER DEAD SISTER'S","CUBS."]):
    c=gold_text(c,(60,150+k*118),l,anton(fit(l,950,108)))
d=ImageDraw.Draw(c)
chip(c,64,1110,"READ THE STORY",(226,184,104))
wtext(c,(64,1190),"The tigers in these photographs are other tigers from the same reserve. They are not T18, T28 or the cubs.",bar(24),700,fill=(235,230,218),lh=1.28)
swipe(c,1262); c=motes(c,55,5,0.5); c=leak(c,0.14)
base_finish(c,1,"slide1.jpg")

# ---- S2: family tree
c=topo(dark(),0.2,15)
lead(c,(66,92),"First, who is who.",56)
c=gold_text(c,(60,150),"MEET THE",anton(120)); c=gold_text(c,(60,270),"FAMILY.",anton(120)); d=ImageDraw.Draw(c)
lx,rx=270,810; ty=540
for x,lab,sub,col in [(lx,"T18","THE MOTHER",(70,68,60)),(rx,"T28","MAUSI",(226,184,104))]:
    d.ellipse([x-78,ty-78,x+78,ty+78],fill=col); fg=(230,226,214) if col[0]<100 else (20,16,8)
    d.text((x,ty-8),lab,font=anton(54),fill=fg,anchor="mm"); d.text((x,ty+36),sub,font=bcs(21),fill=fg,anchor="mm")
d.line([(lx+84,ty),(rx-84,ty)],fill=GOLD,width=3); d.text(((lx+rx)/2,ty-30),"SISTERS",font=bcs(24),fill=GOLD,anchor="mm")
d.text((lx,ty+112),"Died March 2022",font=bar(24),fill=(215,210,198),anchor="mm")
d.text((rx,ty+112),"Maternal aunt (mausi)",font=bar(24),fill=(215,210,198),anchor="mm")
d.text((rx,ty+146),"Resident tigress of the range",font=bar(22),fill=(190,186,176),anchor="mm")
cy=930
for k in range(4):
    cx=lx-135+k*90
    if k<3: paw(d,cx,cy,34,fill=MOSS)
    else:
        paw(d,cx,cy,34,fill=(60,40,34)); d.line([(cx-34,cy-34),(cx+34,cy+34)],fill=RUST,width=6); d.line([(cx-34,cy+34),(cx+34,cy-34)],fill=RUST,width=6)
for k in range(4):
    cx=rx-135+k*90
    if k<3: paw(d,cx,cy,34,fill=GOLD)
    else: paw(d,cx,cy,34,fill=None,outline=GOLD,w=3)
d.line([(lx,ty+82),(lx,cy-70)],fill=(110,106,96),width=2); d.line([(rx,ty+182),(rx,cy-70)],fill=(110,106,96),width=2)
d.text((lx,cy+66),"4 CUBS, ABOUT 9 MONTHS",font=bcs(23),fill=GOLD,anchor="mm"); d.text((lx,cy+98),"1 killed. 3 survived.",font=bar(23),fill=(215,210,198),anchor="mm")
d.text((rx,cy+66),"HER OWN, YOUNGER",font=bcs(23),fill=GOLD,anchor="mm"); d.text((rx,cy+98),"Reports say 3 or 4 cubs",font=bar(23),fill=(215,210,198),anchor="mm")
chip(c,64,1120,"THE 3 SURVIVORS WERE RAISED BY MAUSI",MOSS,fg=(16,22,8),size=26)
d=ImageDraw.Draw(c); d.text((64,1204),"Mausi means maternal aunt in Hindi. Cub counts differ between reports.",font=bar(24),fill=(190,186,176))
d.text((64,1296),"SOURCES: PTI, DOWN TO EARTH, ETV BHARAT",font=bc(21),fill=(150,146,134))
base_finish(c,2,"slide2.jpg")

# ---- S3: the night
c=extend(8,(0.38,0.12,1.0,1.0),600,750,dim=1.15)
a=np.array(c).astype(np.float32); g=a.mean(2,keepdims=True); a=g*0.35+a*0.65; a*=np.array([0.78,0.9,1.12],np.float32)
c=Image.fromarray(np.clip(a,0,255).astype(np.uint8)); c=grad(c,0,470,0.5,0.0); c=grad(c,1190,H,0.0,0.85); c=topo(c,0.06,7,(150,180,230))
c=gold_text(c,(60,92),"16 MARCH",anton(124)); c=gold_text(c,(60,214),"2022.",anton(124)); d=ImageDraw.Draw(c)
y=wtext(c,(64,372),"At night, forest staff were told a tigress was lying beside the railway track in the Dubri range, deep inside the core area.",bar(28),940)
wtext(c,(64,y+6),"The team identified her as T18. She was rescued and treated, but died within a day.",bar(28),940)
d.text((64,1210),"She left four cubs, about nine months old.",font=corm(46),fill=(244,238,226))
tinylabel(c,"PHOTOGRAPH OF ANOTHER SANJAY-DUBRI TIGER, GRADED DARK FOR MOOD. NOT T18.",1304)
base_finish(c,3,"slide3.jpg")

# ---- S4: hardest weeks
c=crop(3,(450/1600,400/2000,1150/1600,1275/2000),W,H,dim=0.82); c=grad(c,0,720,0.85,0.0); c=grad(c,1140,H,0.0,0.6)
lead(c,(66,90),"Four cubs. No mother.",56)
c=gold_text(c,(60,150),"ALONE FOR",anton(132)); c=gold_text(c,(60,282),"10 DAYS.",anton(132)); d=ImageDraw.Draw(c)
for k in range(4):
    cx=96+k*80
    if k<3: paw(d,cx,500,30,fill=GOLD)
    else: paw(d,cx,500,30,fill=(60,40,34)); d.line([(cx-30,470),(cx+30,530)],fill=RUST,width=6); d.line([(cx-30,530),(cx+30,470)],fill=RUST,width=6)
y=wtext(c,(64,556),"Elephant-mounted teams monitored the cubs and provided prey.",bar(25),560,lh=1.25)
wtext(c,(64,y+4),"An adult tiger killed one cub.",bar(25),560,lh=1.25)
tinylabel(c,NOTE,1304)
base_finish(c,4,"slide4.jpg")

# ---- S5: found with T28
c=extend(8,(0.38,0.12,1.0,1.0),560,790,dim=0.95); c=grad(c,0,420,0.4,0.0); c=grad(c,1150,H,0.0,0.82)
lead(c,(66,88),"About 10 days later, the cubs were found with",48)
c=gold_text(c,(60,150),"MAUSI.",anton(170)); d=ImageDraw.Draw(c)
xx=64; xx+=chip(c,xx,356,"T18",(70,68,60),fg=(230,226,214))+14
d=ImageDraw.Draw(c); d.line([(xx,378),(xx+40,378)],fill=GOLD,width=3); d.text((xx+52,364),"SISTERS",font=bcs(22),fill=GOLD); xx+=52+d.textlength("SISTERS",font=bcs(22))+14
d.line([(xx,378),(xx+40,378)],fill=GOLD,width=3); xx+=54; chip(c,xx,356,"T28",(226,184,104))
y=wtext(c,(64,430),"T28 was a resident tigress of the range. Officials identified her from their records.",bar(26),940)
wtext(c,(64,y+4),"Reports say another nursing tigress had refused to mother the cubs. T28 did not.",bar(26),940)
d=ImageDraw.Draw(c); d.text((64,1200),"She took them in alongside her own.",font=corm(50),fill=(244,238,226))
tinylabel(c,NOTE,1304)
base_finish(c,5,"slide5.jpg")

# ---- S6: two litters graphic
c=topo(dark(),0.2,19)
lead(c,(66,92),"Officials found a tigress with six cubs,",50)
c=gold_text(c,(60,150),"TWO LITTERS.",anton(130)); c=gold_text(c,(60,282),"ONE TIGRESS.",anton(130)); d=ImageDraw.Draw(c)
rows=[("ABOUT 9 MONTHS","T18's orphans",3,MOSS),("SLIGHTLY YOUNGER, 6-7 MONTHS","T28's own cubs",3,GOLD)]
y0=520
for r,(a1,b1,n,col) in enumerate(rows):
    y=y0+r*250
    d.rounded_rectangle([64,y,W-64,y+210],radius=18,outline=(80,78,70),width=2)
    for k in range(n): paw(d,150+k*100,y+84,40,fill=col)
    d.text((500,y+44),a1,font=bcs(26),fill=col); d.text((500,y+90),b1,font=anton(44),fill=CREAM); d.text((500,y+150),"Together as one family",font=bar(22),fill=(190,186,176)) if r==0 else d.text((500,y+150),"Reports differ: 3 or 4 cubs",font=bar(22),fill=(190,186,176))
y=wtext(c,(64,1040),"They lived around a marshy lake ringed by grass 6 to 7 feet tall, a safer place for cubs.",bar(27),940)
wtext(c,(64,y+6),"About five months after the orphaning, monitoring showed the cubs had mixed well and lived like a family.",bar(27),940)
d.text((64,1296),"SOURCES: DOWN TO EARTH, PTI",font=bc(21),fill=(150,146,134))
base_finish(c,6,"slide6.jpg")

# ---- S7: training
c=crop(3,(0.12,0.10,0.88,0.90),W,H,dim=0.84); c=grad(c,0,560,0.84,0.0); c=grad(c,1170,H,0.0,0.6)
lead(c,(66,88),"Reports say Mausi gave the orphans",50)
c=gold_text(c,(60,150),"PRIORITY.",anton(150)); d=ImageDraw.Draw(c)
y=wtext(c,(64,352),"In hunting training, the orphans came first, ahead of her own cubs.",bar(28),520)
wtext(c,(64,y+8),"Field Director YP Singh said the orphans can now hunt independently and share prey with their siblings.",bar(28),520)
tinylabel(c,NOTE,1304)
base_finish(c,7,"slide7.jpg")

# ---- S8: timeline
c=topo(dark(),0.18,23)
lead(c,(66,92),"Save this.",56)
c=gold_text(c,(60,150),"THE TIMELINE.",anton(130)); d=ImageDraw.Draw(c)
ev=[("16 MAR 2022","Staff alerted: injured T18 beside the railway track."),("17 MAR","T18 dies after rescue and treatment. Four cubs, ~9 months old."),("ABOUT 10 DAYS LATER","The three survivors are found with T28, her sister."),("AUG 2022","Orphans hunt on their own and share prey, officials say."),("ABOUT A YEAR ON","Officials had monitored the family before going public.")]
x=108; y=380
d.line([(x,y+10),(x,y+4*190+10)],fill=(110,106,96),width=3)
for k,(a1,b1) in enumerate(ev):
    yy=y+k*190; hi=(k==2)
    d.ellipse([x-14,yy-4,x+14,yy+24],fill=GOLD if hi else (210,205,194))
    d.text((x+44,yy-6),a1,font=bcs(30),fill=GOLD if hi else CREAM)
    wtext(c,(x+44,yy+36),b1,bar(26),820,fill=(215,210,198),lh=1.25)
d=ImageDraw.Draw(c); d.text((64,1296),"SOURCES: PTI, DECCAN HERALD, ETV BHARAT, DOWN TO EARTH. I FOUND NO CONFIRMED UPDATE AFTER 2023.",font=bc(20),fill=(150,146,134))
base_finish(c,8,"slide8.jpg")

# ---- S9: not the first
c=topo(dark(),0.2,27)
lead(c,(66,92),"Is it unheard of?",56)
c=gold_text(c,(60,150),"RARE.",anton(150)); c=gold_text(c,(60,300),"NOT UNHEARD OF.",anton(110)); d=ImageDraw.Draw(c)
rows=[("RANTHAMBHORE, 2011","After their mother T-5 died, male tiger T-25 took over her twin cubs."),("PANNA, 2021","A male tiger was reported caring for cubs after their mother's death."),("SANJAY-DUBRI, 2022","A tigress, T28, raised her sister's cubs alongside her own.")]
for k,(a1,b1) in enumerate(rows):
    y=520+k*210; hi=(k==2)
    d.line([(64,y),(64,y+150)],fill=GOLD if hi else (150,146,134),width=4)
    d.text((92,y-4),a1,font=bcs(32),fill=GOLD if hi else CREAM)
    wtext(c,(92,y+46),b1,bar(27),880,fill=(225,220,208),lh=1.28)
wtext(c,(64,1180),"Each case was reported as unusual. Tigers are generally solitary, and I found no global count of such cases.",bar(25),940,fill=(190,186,176))
d=ImageDraw.Draw(c); d.text((64,1296),"SOURCES: OPEN MAGAZINE, HT, MONGABAY INDIA, PTI",font=bc(21),fill=(150,146,134))
base_finish(c,9,"slide9.jpg")

# ---- S10: hero
c=extend(8,(0.30,0.0,1.0,1.0),0,1060,dim=1.0); c=grad(c,0,300,0.45,0.0); c=grad(c,1070,H,0.0,0.82); c=motes(c,45,21,0.45); c=leak(c,0.1)
d=ImageDraw.Draw(c); d.text((64,100),"SANJAY-DUBRI TIGER RESERVE",font=bcs(30),fill=GOLD)
d.text((64,1124),"Tigers are famously solitary.",font=corm(54),fill=(244,238,226)); d.text((64,1184),"This family was not.",font=corm(54),fill=(244,238,226))
d.text((64,1250),"Photograph by Hitesh Chawla: another tiger of this reserve, not Mausi.",font=bar(22),fill=(205,200,188))
d.text((64,1296),"HAD YOU HEARD OF MAUSI BEFORE?",font=bcs(28),fill=GOLD)
progress(c,10); d=ImageDraw.Draw(c); d.text((W-64-d.textlength("THE NATURAL ANGLE",font=bcs(22)),1300),"THE NATURAL ANGLE",font=bcs(22),fill=(200,196,184))
finish(c,"slide10.jpg",vig=0.12)
print("done")
