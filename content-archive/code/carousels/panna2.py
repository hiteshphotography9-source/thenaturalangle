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


# S1 hook: zero + photo
c=framed(6,y=370,w=720,h=840); d=ImageDraw.Draw(c)
d.text((56,20),"0",font=serif(330),fill=ACC)
label(d,(300,110),"PANNA  ·  2009")
d.text((300,150),"tigers left.",font=sans(46),fill=CREAM)
d.text((300,215),"Not one.",font=serifi(64),fill=ACC)
text(d,(70,1235),"So how is this happening today?",serifi(46),fill=CREAM,shadow=False)
footer(d,1,TOT); finish(c,"slide1.jpg")

# S2 locator graphic
c=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(c)
label(d,(70,90),"PANNA TIGER RESERVE  ·  2008-09")
text(d,(70,140),"Poachers had wiped out every tiger in the reserve.",serif(62),maxw=940,shadow=False)
cx,cy=W//2,880
for r in (260,195,130,65):
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(70,68,60),width=2)
d.line([(cx-300,cy),(cx+300,cy)],fill=(70,68,60),width=2); d.line([(cx,cy-300),(cx,cy+300)],fill=(70,68,60),width=2)
d.ellipse([cx-15,cy-15,cx+15,cy+15],fill=ACC); d.ellipse([cx-30,cy-30,cx+30,cy+30],outline=ACC,width=3)
label(d,(cx+48,cy-78),"PANNA",CREAM,24)
d.text((cx+66,cy+34),"24.7°N  80.0°E (approx.)",font=sans(21),fill=(150,146,132))
d.text((70,1215),"Madhya Pradesh. Vindhya hills. The Ken River runs through it.",font=sans(26),fill=(190,184,168))
footer(d,2,TOT); finish(c,"slide2.jpg")

# S3 T1 arrives
c,h=lbox(10,400); d=ImageDraw.Draw(c)
label(d,(70,100),"MARCH 2009")
text(d,(70,150),"One tigress arrived from Bandhavgarh. Her name was T1.",serif(54),maxw=940)
text(d,(70,400+h+45),"T2 came from Kanha. A male, T3, from Pench.",sans(30),fill=(215,208,192),shadow=False)
footer(d,3,TOT); finish(c,"slide3.jpg")

# S4 13 cubs
c,h=lbox(8,400); d=ImageDraw.Draw(c)
label(d,(70,100),"THE MOTHER OF PANNA")
text(d,(70,150),"T1 gave birth to 13 cubs in her lifetime.",serif(58),maxw=940)
text(d,(70,400+h+45),"She died of old age in 2023, aged about 17.",serifi(40),fill=ACC,maxw=940)
footer(d,4,TOT); finish(c,"slide4.jpg")

# S5 growth graphic
c=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(c)
label(d,(70,90),"THE RECOVERY")
d.text((66,125),"0",font=serif(220),fill=CREAM)
d.text((250,185),"to",font=serifi(60),fill=(160,155,140))
d.text((360,125),"80+",font=serif(220),fill=ACC)
text(d,(70,400),"tigers, in about 14 years.",sans(38),fill=(215,208,192),shadow=False)
# chart
x0,x1,y0,y1=110,970,1160,720
d.line([(x0,y0),(x1,y0)],fill=(90,88,78),width=2); d.line([(x0,y0),(x0,y1-30)],fill=(90,88,78),width=2)
a=(x0+30,y0); b=(x1-40,y1+10)
for i in range(0,14,2):
    t0=i/14;t1=(i+1)/14
    d.line([(a[0]+(b[0]-a[0])*t0,a[1]+(b[1]-a[1])*t0),(a[0]+(b[0]-a[0])*t1,a[1]+(b[1]-a[1])*t1)],fill=ACC,width=4)
d.ellipse([a[0]-12,a[1]-12,a[0]+12,a[1]+12],fill=CREAM); d.ellipse([b[0]-14,b[1]-14,b[0]+14,b[1]+14],fill=ACC)
d.text((a[0]-20,y0+22),"2009",font=sans(26),fill=(190,184,168)); d.text((b[0]-90,y0+22),"2023-24",font=sans(26),fill=(190,184,168))
d.text((a[0]+14,a[1]-48),"0",font=sansb(26),fill=CREAM); d.text((b[0]-130,b[1]-12),"80+",font=sansb(28),fill=ACC)
d.text((70,1262),"Reported figures vary by source. The direction does not.",font=sans(24),fill=(150,146,132))
footer(d,5,TOT); finish(c,"slide5.jpg")

# S6 close
c=framed(7,y=330,w=720,h=860); d=ImageDraw.Draw(c)
label(d,(70,80),"PANNA TIGER RESERVE")
text(d,(70,120),"Panna proved it can be done. Keeping it is the next test.",serif(48),maxw=940)
text(d,(70,1230),"Follow The Natural Angle for practical wildlife photography.",sans(26),fill=ACC,maxw=940,shadow=False)
footer(d,6,TOT,swipe=False); finish(c,"slide6.jpg")
print("ok")
