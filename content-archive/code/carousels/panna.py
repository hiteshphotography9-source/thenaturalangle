import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
IMG="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/images/"
OUT="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/panna/"
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


TOT=6
def framed(n,y=310,w=720,h=900):
    im=load(n); 
    s=max(w/im.width,h/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    l=(im.width-w)//2;t=(im.height-h)//2; im=im.crop((l,t,l+w,t+h))
    c=Image.new("RGB",(W,H),BG); c.paste(im,((W-w)//2,y)); return c
def lbox(n,y,box=None):
    c,h=letter(n,y,box) if False else (None,None)
    im=load(n); r=W/im.width; im=im.resize((W,round(im.height*r)),Image.LANCZOS)
    c=Image.new("RGB",(W,H),BG); c.paste(im,(0,y)); return c,im.height

# S1 hook
c=framed(6); d=ImageDraw.Draw(c)
label(d,(70,80),"PANNA TIGER RESERVE  ·  MADHYA PRADESH")
text(d,(70,125),"In 2009, Panna had no tigers.",serif(66),maxw=940)
text(d,(70,1245),"Now look.",serifi(50),fill=ACC)
footer(d,1,TOT); finish(c,"slide1.jpg")

# S2 map / zero graphic
c=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(c)
label(d,(70,90),"2009  ·  THE COUNT")
d.text((66,120),"0",font=serif(330),fill=ACC)
text(d,(70,480),"tigers left in Panna.",sans(36),fill=(215,208,192),shadow=False)
text(d,(70,545),"Poachers had wiped out every tiger in the reserve.",serif(52),maxw=940,shadow=False)
cx,cy=W//2,1020
for r in (210,155,100,50):
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(70,68,60),width=2)
d.line([(cx-240,cy),(cx+240,cy)],fill=(70,68,60),width=2); d.line([(cx,cy-240),(cx,cy+240)],fill=(70,68,60),width=2)
d.ellipse([cx-13,cy-13,cx+13,cy+13],fill=ACC)
d.ellipse([cx-26,cy-26,cx+26,cy+26],outline=ACC,width=3)
label(d,(cx+40,cy-70),"PANNA",CREAM,22)
d.text((cx-210,cy+235),"MADHYA PRADESH  ·  KEN RIVER  ·  VINDHYAS",font=sans(22),fill=(150,146,132))
d.text((cx+60,cy+30),"24.7°N  80.0°E (approx.)",font=sans(20),fill=(150,146,132))
footer(d,2,TOT); finish(c,"slide2.jpg")

# S3 reintroduction
c,h=lbox(10,380); d=ImageDraw.Draw(c)
label(d,(70,100),"2009  ·  THE RESTART")
text(d,(70,150),"Two tigresses were brought in to start again.",serif(56),maxw=940)
text(d,(70,380+h+40),"T1 from Bandhavgarh. T2 from Kanha.",sans(32),fill=(215,208,192),shadow=False)
ty=H-210
d.line([(70,ty),(W-70,ty)],fill=(90,88,78),width=2)
for x,t in [(70,"2009: T1 and T2 relocated"),(560,"Dec 2024: P-151 with three cubs")]:
    d.ellipse([x,ty-9,x+18,ty+9],fill=ACC); d.text((x,ty-48),t,font=sans(21),fill=(190,184,168))
footer(d,3,TOT); finish(c,"slide3.jpg")

# S4 Panna-born
c,h=lbox(8,400); d=ImageDraw.Draw(c)
label(d,(70,100),"TODAY")
text(d,(70,150),"Tigers born in Panna now raise cubs of their own.",serif(56),maxw=940)
text(d,(70,400+h+50),"P-151 is one of them.",serifi(54),fill=ACC)
footer(d,4,TOT); finish(c,"slide4.jpg")

# S5 the eyes
c=framed(7); d=ImageDraw.Draw(c)
label(d,(70,80),"PANNA  ·  P-151'S CUBS")
text(d,(70,125),"A new generation, looking back.",serif(66),maxw=940)
footer(d,5,TOT); finish(c,"slide5.jpg")

# S6 close
c=framed(9); d=ImageDraw.Draw(c)
label(d,(70,80),"PANNA TIGER RESERVE")
text(d,(70,125),"Zero tigers in 2009. Cubs in the grass today.",serif(60),maxw=940)
text(d,(70,1245),"Follow The Natural Angle for practical wildlife photography.",sans(26),fill=ACC,maxw=940,shadow=False)
footer(d,6,TOT,swipe=False); finish(c,"slide6.jpg")
print("ok")
