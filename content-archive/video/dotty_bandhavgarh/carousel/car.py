import numpy as np, cv2, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SP="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/"
FD=SP+"fonts/"; ID=SP+"dotty/img/"
W,H=1080,1440
GOLD=(255,196,92); AMB=(255,150,50); CREAM=(246,238,224); GREY=(186,178,166); CYAN=(90,215,230); RED=(235,80,60); INK=(24,20,16)
def F(n,s): return ImageFont.truetype(FD+n,int(s))
A=lambda s:F("Anton-Regular.ttf",s); B=lambda s:F("BarlowCondensed-SemiBold.ttf",s); BM=lambda s:F("BarlowCondensed-Medium.ttf",s)
rng=np.random.default_rng(4)
def stripes(w,h,seed):
    r=np.random.default_rng(seed)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    n1=cv2.GaussianBlur(r.normal(0,1,(h,w)).astype(np.float32),(0,0),60); n1/=np.abs(n1).max()
    n2=cv2.GaussianBlur(r.normal(0,1,(h,w)).astype(np.float32),(0,0),18); n2/=np.abs(n2).max()
    ph=yy*0.030+n1*9+n2*1.6+np.sin(xx*0.004)*2
    s=np.sin(ph); th=0.55+0.25*np.sin(xx*0.012+n1*3)
    st=np.clip((s-th)*6,0,1)*np.clip(np.abs(np.sin(xx*0.0045+n1*2))*1.6,0,1)
    img=np.zeros((h,w,3),np.float32)+(46,26,12)
    img+=np.clip(0.5+0.5*n1,0,1)[...,None]*np.array((40,22,6),np.float32)
    img=img*(1-st[...,None]*0.85)
    yy2,xx2=np.mgrid[0:h,0:w]
    vig=(1-0.55*(((xx2-w/2)/(w/2))**2*0.5+((yy2-h/2)/(h/2))**2*0.7)).clip(0.35,1)[...,None]
    img=img*vig+r.normal(0,1,(h,w,1))*4
    return Image.fromarray(np.clip(img,0,255).astype(np.uint8)).convert("RGBA")
def ld(p): return Image.open(ID+p).convert("RGB")
def photo(img,src,box,rect,rad=26,border=GOLD,sharpen=True):
    wx,wy,ww,wh=rect
    ph=src.crop(box).resize((ww,wh),Image.LANCZOS)
    if sharpen: ph=ph.filter(ImageFilter.UnsharpMask(2,80,2))
    mk=Image.new("L",(ww,wh),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,ww-1,wh-1),radius=rad,fill=255)
    sh=Image.new("RGBA",(ww,wh),(0,0,0,150)); sh.putalpha(mk.point(lambda v:v*150//255)); img.alpha_composite(sh,(wx+10,wy+14))
    p=ph.convert("RGBA"); p.putalpha(mk); img.alpha_composite(p,(wx,wy))
    ImageDraw.Draw(img,"RGBA").rounded_rectangle((wx-2,wy-2,wx+ww+1,wy+wh+1),radius=rad,outline=border+(200,),width=3)
def card(img,src,cx,cy,sc,rot):
    p=src.convert("RGBA").resize((int(src.width*sc),int(src.height*sc)),Image.LANCZOS).rotate(rot,expand=True,resample=Image.BICUBIC)
    al=p.split()[-1]; sh=Image.new("RGBA",p.size,(0,0,0,0)); sh.putalpha(al.point(lambda v:int(v*0.55)))
    sh=sh.filter(ImageFilter.GaussianBlur(8))
    img.alpha_composite(sh,(int(cx-p.width/2+14),int(cy-p.height/2+18))); img.alpha_composite(p,(int(cx-p.width/2),int(cy-p.height/2)))
def gold_text(img,xy,s,f,anchor="ms"):
    m=Image.new("L",img.size,0); ImageDraw.Draw(m).text(xy,s,font=f,fill=255,anchor=anchor)
    y=np.linspace(0,1,H)[:,None,None]; tex=np.array([255,226,160])*(1-y)+np.array([214,150,70])*y
    tex=np.broadcast_to(tex,(H,W,3)).astype(np.uint8)
    sh=Image.new("RGBA",img.size,(0,0,0,0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(6)).point(lambda v:int(v*0.8)))
    img.alpha_composite(sh,(4,6))
    t=Image.fromarray(tex).convert("RGBA"); t.putalpha(m); img.alpha_composite(t)
def txt(d,xy,s,f,fill,a=255,anchor="ms"): d.text(xy,s,font=f,fill=fill+(a,),anchor=anchor)
def chrome(img,n,tot=8,swipe=True):
    d=ImageDraw.Draw(img,"RGBA")
    txt(d,(60,64),"THE NATURAL ANGLE",B(30),CREAM,170,"ls")
    txt(d,(W-60,64),f"{n}/{tot}",B(30),GOLD,220,"rs")
    d.line((60,82,W-60,82),fill=GOLD+(70,),width=2)
    if swipe:
        txt(d,(W-96,H-46),"SWIPE",B(28),GOLD,230,"rs")
        x=W-84;y=H-56
        d.line((x,y,x+30,y),fill=GOLD+(230,),width=4); d.polygon([(x+30,y-9),(x+44,y),(x+30,y+9)],fill=GOLD+(230,))
def credit(d,s,y=H-46,x=60,anchor="ls"): txt(d,(x,y),s,BM(24),GREY,220,anchor)
def glow_ellipse(img,cx,cy,rx,ry):
    L=Image.new("L",img.size,0); ImageDraw.Draw(L).ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=255)
    g=np.array(L.filter(ImageFilter.GaussianBlur(max(4,rx*0.35)))).astype(np.float32)/255
    a=np.array(img).astype(np.float32); a[...,:3]=np.clip(a[...,:3]*(1+g[...,None]*0.35)+g[...,None]*np.array((60,30,0)),0,255)
    img.paste(Image.fromarray(a.astype(np.uint8)))
    ImageDraw.Draw(img,"RGBA").ellipse((cx-rx*1.08,cy-ry*1.12,cx+rx*1.08,cy+ry*1.12),outline=AMB+(255,),width=4)
def wrap(s,f,maxw):
    words=s.split(); lines=[]; cur=""
    for w_ in words:
        t=(cur+" "+w_).strip()
        if f.getlength(t)<=maxw: cur=t
        else: lines.append(cur); cur=w_
    lines.append(cur); return lines
