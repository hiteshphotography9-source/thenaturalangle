import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
IMG="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/images/"
OUT="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/sil/"
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


TOT=8
def framed(n,y=300,w=720,h=900,box=None):
    im=load(n)
    if box: im=im.crop(box)
    s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    l=(im.width-w)//2;t=(im.height-h)//2; im=im.crop((l,t,l+w,t+h))
    c=Image.new("RGB",(W,H),BG); c.paste(im,((W-w)//2,y)); return c
def thumb(c,n,x,y,w,h):
    im=load(n); s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    l=(im.width-w)//2;t=(im.height-h)//2; c.paste(im.crop((l,t,l+w,t+h)),(x,y))

# S1 hook
c=cover(load(15)); c=grad(c,0,720,0.62,0.0); c=grad(c,1250,H,0.0,0.7)
d=ImageDraw.Draw(c)
label(d,(70,80),"WILDLIFE SILHOUETTES  ·  5 RULES",CREAM,22)
y=text(d,(70,135),"Stop exposing for the bird.",serif(88),maxw=940,lh=1.1)
text(d,(70,y+20),"How to shoot a clean silhouette.",serifi(44),fill=(244,200,140),maxw=900)
footer(d,1,TOT); finish(c,"slide1.jpg")

# S2 rule 1
c=framed(11); d=ImageDraw.Draw(c)
label(d,(70,80),"RULE 1")
text(d,(70,120),"Expose for the sky, not the bird.",serif(58),maxw=940)
label(d,(70,1228),"SPOT METERING  ·  -1 TO -3 EV",ACC,24)
text(d,(70,1272),"Meter the bright sky beside the sun. The bird goes black.",sans(26),fill=(215,208,192),maxw=940,shadow=False)
footer(d,2,TOT); finish(c,"slide2.jpg")

# S3 rule 2
c,h=letter(11,330,(20,860,820,1460)); d=ImageDraw.Draw(c)
label(d,(70,80),"RULE 2")
text(d,(70,120),"Wait for the profile.",serif(66),maxw=940)
text(d,(70,330+h+40),"Beak, crest, tail and legs should read as one clean shape.",sans(30),fill=(215,208,192),maxw=940,shadow=False)
footer(d,3,TOT); finish(c,"slide3.jpg")

# S4 rule 3
c=framed(13); d=ImageDraw.Draw(c)
label(d,(70,80),"RULE 3")
text(d,(70,120),"Give every bird its own space.",serif(60),maxw=940)
text(d,(70,1235),"Overlap turns two birds into one blob.",serifi(40),fill=ACC,maxw=940,shadow=False)
footer(d,4,TOT); finish(c,"slide4.jpg")

# S5 sun placement 3-up
c=Image.new("RGB",(W,H),BG)
for i,n in enumerate([11,13,15]): thumb(c,n,40+i*342,360,330,560)
d=ImageDraw.Draw(c)
label(d,(70,80),"RULE 4")
text(d,(70,120),"Place the sun on purpose.",serif(60),maxw=940)
for i,t in enumerate(["Sun to the side.\nSoft gradient.","Sun half behind.\nGlowing edge.","Sun behind the bird.\nThe hero shot."]):
    for j,ln in enumerate(t.split("\n")):
        d.text((40+i*342,950+j*36),ln,font=sansb(24) if j==0 else sans(24),fill=CREAM if j==0 else (190,184,168))
text(d,(70,1130),"Move your feet until the sun sits where you want it.",serifi(40),fill=ACC,maxw=940,shadow=False)
footer(d,5,TOT); finish(c,"slide5.jpg")

# S6 shutter
c=framed(14); d=ImageDraw.Draw(c)
label(d,(70,80),"RULE 5")
text(d,(70,120),"Match shutter speed to the bird.",serif(58),maxw=940)
label(d,(70,1228),"PERCHED 1/250  ·  IN FLIGHT 1/1000+",ACC,24)
text(d,(70,1272),"See the blurred bird? Silhouettes show every bit of motion.",sans(26),fill=(215,208,192),maxw=940,shadow=False)
footer(d,6,TOT); finish(c,"slide6.jpg")

# S7 bonus rim light
c=framed(12); d=ImageDraw.Draw(c)
label(d,(70,80),"BONUS")
text(d,(70,120),"Not every golden hour is a silhouette.",serif(56),maxw=940)
text(d,(70,1228),"For rim light, keep the exposure on the bird. Shoot RAW. Lens hood on.",sans(26),fill=(215,208,192),maxw=940,shadow=False)
footer(d,7,TOT); finish(c,"slide7.jpg")

# S8 cheat sheet
c=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(c)
label(d,(70,90),"THE SILHOUETTE CHEAT SHEET")
text(d,(70,135),"Save this for golden hour.",serif(66),maxw=940,shadow=False)
rows=[("Mode","Aperture priority or Manual"),("Metering","Spot, on the bright sky"),("Exposure comp.","-1 to -3 EV"),("ISO","100 to 200"),("Aperture","f/5.6 to f/8"),("Shutter, perched","1/250 or faster"),("Shutter, flight","1/1000 or faster"),("File","RAW")]
y=330
for k,v in rows:
    d.line([(70,y),(W-70,y)],fill=(60,58,50),width=2)
    d.text((70,y+22),k,font=sans(28),fill=(190,184,168)); d.text((W-70-d.textlength(v,font=serif(32)),y+18),v,font=serif(32),fill=ACC)
    y+=84
d.line([(70,y),(W-70,y)],fill=(60,58,50),width=2)
d.text((70,y+22),"Starting points. Raise ISO if the shutter speed drops.",font=sans(22),fill=(130,126,112))
d.text((70,y+90),"Photographs by Hitesh Chawla  ·  The Natural Angle",font=sans(26),fill=(215,208,192))
text(d,(70,y+135),"Follow The Natural Angle for practical wildlife photography.",sans(26),fill=ACC,maxw=940,shadow=False)
footer(d,8,TOT,swipe=False); finish(c,"slide8.jpg")
print("ok")
