import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
IMG="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/images/"
OUT="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/raptor/"
W,H=1080,1440
F="/usr/share/fonts/truetype/liberation/"
serif=lambda s:ImageFont.truetype(F+"LiberationSerif-Bold.ttf",s)
serifi=lambda s:ImageFont.truetype(F+"LiberationSerif-Italic.ttf",s)
sans=lambda s:ImageFont.truetype(F+"LiberationSans-Regular.ttf",s)
sansb=lambda s:ImageFont.truetype(F+"LiberationSans-Bold.ttf",s)
CREAM=(244,238,226); ACC=(226,138,52); BG=(12,14,11)

def load(n): return Image.open(IMG+f"{n}.jpg").convert("RGB")
def cover(im,box=None):
    if box: im=im.crop(box)
    s=max(W/im.width,H/im.height)
    im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    l=(im.width-W)//2; t=(im.height-H)//2
    return im.crop((l,t,l+W,t+H))
def grad(canvas,y0,y1,a0,a1):
    arr=np.array(canvas).astype(float)
    ys=np.arange(H)[:,None]
    t=np.clip((ys-y0)/(y1-y0),0,1)
    a=(a0+(a1-a0)*t)[:,:,None]
    arr=arr*(1-a)+np.array(BG)*a
    return Image.fromarray(arr.astype("uint8"))
def vignette(im,strength=0.28):
    arr=np.array(im).astype(float)
    y,x=np.mgrid[0:H,0:W]
    d=np.sqrt(((x-W/2)/(W/2))**2+((y-H/2)/(H/2))**2)
    m=1-strength*np.clip(d-0.5,0,1)**1.5
    return Image.fromarray((arr*m[:,:,None]).clip(0,255).astype("uint8"))
def grain(im,amt=7):
    arr=np.array(im).astype(float)
    n=np.random.default_rng(3).normal(0,amt,(H,W,1))
    return Image.fromarray((arr+n).clip(0,255).astype("uint8"))
def wrap(d,text,font,maxw):
    words=text.split();lines=[];cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur);cur=w
    lines.append(cur);return lines
def text(d,xy,t,font,fill=CREAM,maxw=900,lh=1.16,shadow=True):
    x,y=xy
    for ln in wrap(d,t,font,maxw):
        if shadow: d.text((x+2,y+2),ln,font=font,fill=(0,0,0))
        d.text((x,y),ln,font=font,fill=fill); y+=int(font.size*lh)
    return y
def label(d,xy,t,fill=ACC,size=24):
    f=sansb(size);x,y=xy
    for ch in t:
        d.text((x,y),ch,font=f,fill=fill); x+=d.textlength(ch,font=f)+4
def letter(n,y,box=None):
    im=load(n)
    if box: im=im.crop(box)
    r=W/im.width; im=im.resize((W,round(im.height*r)),Image.LANCZOS)
    c=Image.new("RGB",(W,H),BG); c.paste(im,(0,y)); return c,im.height
def footer(d,i,total=6,swipe=True):
    label(d,(70,H-82),"THE NATURAL ANGLE",CREAM,20)
    d.text((W-70-d.textlength(f"{i} / {total}",font=sans(22)),H-84),f"{i} / {total}",font=sans(22),fill=(170,165,150))
    if swipe and i<total:
        d.line([(W-190,H-120),(W-70,H-120)],fill=ACC,width=3)
        d.polygon([(W-70,H-120),(W-84,H-128),(W-84,H-112)],fill=ACC)
def finish(c,name):
    c=grain(vignette(c)); c.save(OUT+name,quality=95)


U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
FILES=["fe41241e","5c52c0a4","ae33de49","01df9a6b","0afbf1bc","0e105c61"]
CENT=[(.38,.55),(.5,.5),(.5,.48),(.5,.55),(.66,.55),(.5,.45)]
TOT=8
def bird(i): return Image.open(U+FILES[i]+"-image.jpg").convert("RGB")
def crop_to(im,w,h,cx,cy,zoom=1.0):
    r=w/h
    cw=min(im.width,im.height*r)/zoom; ch=cw/r
    x0=min(max(cx*im.width-cw/2,0),im.width-cw); y0=min(max(cy*im.height-ch/2,0),im.height-ch)
    return im.crop((int(x0),int(y0),int(x0+cw),int(y0+ch))).resize((w,h),Image.LANCZOS)

# S1 collage hook
c=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(c)
tw,th,gap=320,420,20; x0=(W-(3*tw+2*gap))//2
for i in range(6):
    t=crop_to(bird(i),tw,th,CENT[i][0],CENT[i][1],1.6 if i in (0,3,4) else 1.5)
    c.paste(t,(x0+(i%3)*(tw+gap),380+(i//3)*(th+gap)))
d=ImageDraw.Draw(c)
label(d,(70,80),"FIELD GUIDE  ·  RAPTORS OF OPEN COUNTRY")
text(d,(70,125),"6 raptors. 6 habitats. Can you tell them apart?",serif(60),maxw=940,shadow=False)
text(d,(70,1290),"Swipe to meet them.",serifi(36),fill=ACC,shadow=False)
footer(d,1,TOT); finish(c,"slide1.jpg")

DATA=[
 (0,"Black-winged Kite","Elanus caeruleus","Open grassland, farmland and scrub with scattered trees.","Hovering over fields, then a sudden plunge. Rodents are the main prey."),
 (1,"Montagu's Harrier","Circus pygargus  ·  female","Grasslands, crop fields, marshes and open country.","Low, gliding flight over grass and crops. A winter migrant to India from Central Asia and Russia."),
 (2,"Common Kestrel","Falco tinnunculus","Open country: fields, grassland and farmland.","A hover 10 to 20 m above the ground. Winter visitor and local resident in India."),
 (3,"Long-legged Buzzard","Buteo rufinus","Arid, open, uncultivated land: steppe, semi-desert and stony hills.","Pale body, rufous tail. A winter migrant in the arid northwest."),
 (4,"Laggar Falcon","Falco jugger  ·  female","Dry open plains, arid scrub and open woodland with scattered trees.","A dark moustachial streak and rufous crown. A resident across India that mainly hunts birds."),
 (5,"Short-toed Snake Eagle","Circaetus gallicus","Open plains, arid stony scrub, foothills and semi-desert, with trees for nesting.","Big round head, bright yellow eyes, pale underside. Snakes are most of its diet."),
]
for k,(i,name,sci,hab,look) in enumerate(DATA):
    c=Image.new("RGB",(W,H),BG)
    im=crop_to(bird(i),720,800,CENT[i][0],CENT[i][1],1.0 if i!=4 else 1.0)
    c.paste(im,((W-720)//2,270)); d=ImageDraw.Draw(c)
    label(d,(70,76),f"RAPTOR {k+1} OF 6")
    d.text((70,112),name,font=serif(60),fill=CREAM)
    d.text((70,190),sci,font=serifi(30),fill=(244,200,140))
    label(d,(70,1092),"HABITAT",ACC,22)
    y=text(d,(70,1126),hab,sans(28),fill=CREAM,maxw=940,lh=1.2,shadow=False)
    label(d,(70,y+14),"LOOK FOR",ACC,22)
    text(d,(70,y+48),look,sans(26),fill=(215,208,192),maxw=940,lh=1.2,shadow=False)
    footer(d,k+2,TOT); finish(c,f"slide{k+2}.jpg")

# S8 summary + CTA
c=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(c)
label(d,(70,90),"WHERE TO LOOK")
text(d,(70,135),"Know the habitat, find the bird.",serif(60),maxw=940,shadow=False)
rows=[("Black-winged Kite","Grassland, farmland"),("Montagu's Harrier","Grassland, marsh"),("Common Kestrel","Open fields"),("Long-legged Buzzard","Arid steppe, semi-desert"),("Laggar Falcon","Dry plains, scrub"),("Short-toed Snake Eagle","Arid scrub, open plains")]
y=360
for k,v in rows:
    d.line([(70,y),(W-70,y)],fill=(60,58,50),width=2)
    d.text((70,y+24),k,font=sans(28),fill=CREAM); d.text((W-70-d.textlength(v,font=serif(30)),y+22),v,font=serif(30),fill=ACC)
    y+=90
d.line([(70,y),(W-70,y)],fill=(60,58,50),width=2)
text(d,(70,y+60),"Save this for your next field trip.",serif(46),maxw=940,shadow=False)
d.text((70,y+135),"Photographs by Hitesh Chawla  ·  The Natural Angle",font=sans(26),fill=(215,208,192))
footer(d,8,TOT,swipe=False); finish(c,"slide8.jpg")
print("ok")
