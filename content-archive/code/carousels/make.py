import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
IMG="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/images/"
OUT="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/beldanda/"
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

# S1
c,h=letter(2,430)
c=grad(c,0,430,0.0,0.0)
d=ImageDraw.Draw(c)
label(d,(70,86),"KISHANPUR  ·  DUDHWA TIGER RESERVE")
text(d,(70,150),"A forest road was closed for six months to protect one tigress's cubs.",serif(58),maxw=940)
text(d,(70,H-250),"Why?",serifi(54),fill=ACC)
footer(d,1); finish(c,"slide1.jpg")

# S2 framed photo, text in clear band below
im=load(3).resize((800,1000),Image.LANCZOS)
c=Image.new("RGB",(W,H),BG); c.paste(im,(140,110))
d=ImageDraw.Draw(c)
label(d,(70,1150),"KISHANPUR")
text(d,(70,1190),"Her name is Beldanda.",serif(66),maxw=940)
text(d,(70,1280),"Named after the Beldanda beat where she is seen.",sans(28),fill=(215,208,192),maxw=940)
footer(d,2); finish(c,"slide2.jpg")

# S3 photo1 letterbox top
c,h=letter(1,90)
d=ImageDraw.Draw(c)
label(d,(70,90+h+60),"17 NOV 2019",ACC,30)
text(d,(70,90+h+110),"Five cubs on one road. One photograph that travelled the world.",serif(52),maxw=940)
d.line([(70,H-190),(W-70,H-190)],fill=(90,88,78),width=2)
for x,t in [(70,"17 Nov 2019: the photo"),(520,"Road closed for six months")]:
    d.ellipse([x,H-199,x+18,H-181],fill=ACC)
    d.text((x+28,H-230),t,font=sans(22),fill=(190,184,168))
footer(d,3); finish(c,"slide3.jpg")

# S4 photo4 full bleed
c=cover(load(4)); c=grad(c,0,520,0.85,0.0); c=grad(c,980,H,0.0,0.85)
d=ImageDraw.Draw(c)
text(d,(70,110),"Wild tiger cubs face long odds.",serif(66),maxw=900)
text(d,(70,1200),"Space, water and time are what give them a chance.",serifi(40),maxw=900)
footer(d,4); finish(c,"slide4.jpg")

# S5 photo5 letterbox
c,h=letter(5,200)
d=ImageDraw.Draw(c)
label(d,(70,110),"KISHANPUR  ·  BELDANDA AND HER CUBS")
y=text(d,(70,200+h+70),"Almost grown.",serif(78),maxw=940)
text(d,(70,y+6),"Still together.",serifi(78),fill=ACC,maxw=940)
footer(d,5); finish(c,"slide5.jpg")

# S6 letterboxed, text only in clean bands
c,h=letter(2,330,(650,434,1500,1000))
d=ImageDraw.Draw(c)
label(d,(70,120),"KISHANPUR  ·  THE NATURAL ANGLE")
text(d,(70,175),"Give a tiger space, and she does the rest.",serif(58),maxw=940)
label(d,(70,330+h+70),"FOLLOW FOR MORE FROM THE FIELD",ACC,24)
text(d,(70,330+h+120),"Photographed by Hitesh Chawla",sans(30),fill=(215,208,192))
footer(d,6,swipe=False); finish(c,"slide6.jpg")
print("ok")
