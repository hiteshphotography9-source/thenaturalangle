import numpy as np, cv2, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SP="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/"
FD=SP+"fonts/"; ID=SP+"dhole/img/"
W,H=1080,1440; FPS=30
RUST=(232,112,46); EMBER=(255,150,70); CREAM=(244,238,226); GREY=(170,176,166); SAGE=(150,196,150); INK=(14,16,12); RED=(232,70,56); TEAL=(96,206,196)
def F(n,s): return ImageFont.truetype(FD+n,int(s))
A=lambda s:F("Anton-Regular.ttf",s); B=lambda s:F("BarlowCondensed-SemiBold.ttf",s); BM=lambda s:F("BarlowCondensed-Medium.ttf",s)
def ease(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def eo3(x): x=min(1,max(0,x)); return 1-(1-x)**3
def eob(x,k=1.7): x=min(1,max(0,x)); return 1+(k+1)*(x-1)**3+k*(x-1)**2
def seg(t,a,b): return min(1,max(0,(t-a)/(b-a)))
def lerp(a,b,x): return a+(b-a)*x
def L(w=W,h=H): return Image.new("RGBA",(w,h),(0,0,0,0))
def jungle(seed,w=W,h=H):
    r=np.random.default_rng(seed)
    n1=cv2.GaussianBlur(r.normal(0,1,(h,w)).astype(np.float32),(0,0),70); n1/=np.abs(n1).max()
    n2=cv2.GaussianBlur(r.normal(0,1,(h,w)).astype(np.float32),(0,0),9); n2/=np.abs(n2).max()
    leaf=np.clip((n2*0.7+n1*0.5)-0.15,0,1)
    img=np.zeros((h,w,3),np.float32)+(12,17,12)
    img+=leaf[...,None]*np.array((18,32,18),np.float32)
    yy,xx=np.mgrid[0:h,0:w]
    warm=np.exp(-(((xx-w*0.8)/(w*0.7))**2+((yy-h*0.05)/(h*0.6))**2))[...,None]*np.array((40,18,4),np.float32)
    img+=warm
    vig=(1-0.6*(((xx-w/2)/(w/2))**2*0.5+((yy-h/2)/(h/2))**2*0.6)).clip(0.3,1)[...,None]
    img=img*vig+r.normal(0,1,(h,w,1))*3.5
    return Image.fromarray(np.clip(img,0,255).astype(np.uint8)).convert("RGBA")
def ldarr(p): return np.array(Image.open(ID+p).convert("RGB")).astype(np.float32)
def grade_spot(arr,cx,cy,rx,ry,k):
    """selective pop: outside desat+darker, inside warmer+contrast. k 0..1"""
    if k<=0: return arr
    h,w=arr.shape[:2]; yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    m=np.clip(1.25-np.sqrt(((xx-cx)/rx)**2+((yy-cy)/ry)**2),0,1); m=cv2.GaussianBlur(m,(0,0),max(6,rx*0.15))[...,None]
    g=arr.mean(2,keepdims=True)
    out=arr*(1-0.55*k)+g*0.55*k; out=out*(1-0.38*k)
    ins=np.clip((arr-128)*(1+0.18*k)+128,0,255); ins=ins*np.array((1+0.06*k,1.0,1-0.04*k))
    ins=ins*(1+0.08*k)
    return np.clip(out*(1-m)+ins*m,0,255)
def pwin(img,arr,box,rect,z=1.0,spot=None,k=0.0,flash=0.0,rad=26,border=RUST,desat=0.0):
    x0,y0,x1,y1=box; cx,cy=(x0+x1)/2,(y0+y1)/2; hw,hh=(x1-x0)/2/z,(y1-y0)/2/z
    wx,wy,ww,wh=rect
    M=np.array([[ww/(2*hw),0,-(cx-hw)*ww/(2*hw)],[0,wh/(2*hh),-(cy-hh)*wh/(2*hh)]],np.float32)
    ph=cv2.warpAffine(arr,M,(ww,wh),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
    bl=cv2.GaussianBlur(ph,(0,0),1.3); ph=np.clip(ph*1.4-bl*0.4,0,255)
    if desat>0: g=ph.mean(2,keepdims=True); ph=ph*(1-desat)+g*desat; ph*=1-0.3*desat
    if spot is not None and k>0:
        sx,sy,srx,sry=spot  # in source coords
        f=ww/(2*hw); ph=grade_spot(ph,(sx-(cx-hw))*f,(sy-(cy-hh))*f,srx*f,sry*f,k)
    if flash>0: ph=np.clip(ph+flash*200,0,255)
    mk=Image.new("L",(ww,wh),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,ww-1,wh-1),radius=rad,fill=255)
    sh=Image.new("RGBA",(ww,wh),(0,0,0,0)); sh.putalpha(mk.point(lambda v:v*140//255)); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)),(wx+8,wy+14))
    p=Image.fromarray(ph.astype(np.uint8)).convert("RGBA"); p.putalpha(mk); img.alpha_composite(p,(wx,wy))
    ImageDraw.Draw(img,"RGBA").rounded_rectangle((wx-2,wy-2,wx+ww+1,wy+wh+1),radius=rad,outline=border+(200,),width=3)
    def tomap(sx,sy): f=ww/(2*hw); return wx+(sx-(cx-hw))*f, wy+(sy-(cy-hh))*f
    return tomap
def card(img,src,cx,cy,sc,rot,a=1.0):
    p=src.convert("RGBA").resize((max(1,int(src.width*sc)),max(1,int(src.height*sc))),Image.LANCZOS).rotate(rot,expand=True,resample=Image.BICUBIC)
    al=p.split()[-1].point(lambda v:int(v*a)); p.putalpha(al)
    sh=Image.new("RGBA",p.size,(0,0,0,0)); sh.putalpha(al.point(lambda v:int(v*0.6))); sh=sh.filter(ImageFilter.GaussianBlur(10))
    img.alpha_composite(sh,(int(cx-p.width/2+14),int(cy-p.height/2+18))); img.alpha_composite(p,(int(cx-p.width/2),int(cy-p.height/2)))
def txt(d,xy,s,f,fill,a=255,anchor="ms"): d.text(xy,s,font=f,fill=fill+(int(a),),anchor=anchor)
def grad_text(img,xy,s,f,top=(255,190,120),bot=(214,92,36),anchor="ms",shadow=True):
    m=Image.new("L",img.size,0); ImageDraw.Draw(m).text(xy,s,font=f,fill=255,anchor=anchor)
    bb=m.getbbox()
    if not bb: return
    y=np.clip((np.arange(img.size[1])-bb[1])/max(1,bb[3]-bb[1]),0,1)[:,None,None]
    tex=(np.array(top)*(1-y)+np.array(bot)*y); tex=np.broadcast_to(tex,(img.size[1],img.size[0],3)).astype(np.uint8)
    if shadow:
        sh=Image.new("RGBA",img.size,(0,0,0,0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(7)).point(lambda v:int(v*0.85))); img.alpha_composite(sh,(4,7))
    t=Image.fromarray(tex).convert("RGBA"); t.putalpha(m); img.alpha_composite(t)
def glayer(xy,s,f,**k): l=L(); grad_text(l,xy,s,f,**k); return l
def amul(lay,a):
    if a>=0.999: return lay
    l=lay.copy(); l.putalpha(l.split()[-1].point(lambda v:int(v*max(0,a)))); return l
def comp(img,lay,a=1.0,dx=0,dy=0,sc=1.0,rot=0.0):
    if a<=0.003: return
    bb=lay.getbbox()
    if not bb: return
    if sc==1 and rot==0:
        l=amul(lay,a)
        if dx or dy: l=l.transform(l.size,Image.AFFINE,(1,0,-dx,0,1,-dy))
        img.alpha_composite(l); return
    pad=40; bb=(max(0,bb[0]-pad),max(0,bb[1]-pad),min(W,bb[2]+pad),min(H,bb[3]+pad))
    c=lay.crop(bb); cx=(bb[0]+bb[2])/2+dx; cy=(bb[1]+bb[3])/2+dy
    c=c.resize((max(1,int(c.width*sc)),max(1,int(c.height*sc))),Image.BICUBIC)
    if rot: c=c.rotate(rot,expand=True,resample=Image.BICUBIC)
    c=amul(c,a); img.alpha_composite(c,(int(cx-c.width/2),int(cy-c.height/2)))
def wipe(lay,p,soft=60):
    if p>=1: return lay
    bb=lay.getbbox()
    if not bb or p<=0: return L()
    x=bb[0]+(bb[2]-bb[0]+soft)*p; m=np.clip((x-np.arange(W)[None,:])/soft,0,1)
    l=lay.copy(); a=np.array(l.split()[-1]).astype(np.float32)*m; l.putalpha(Image.fromarray(a.astype(np.uint8))); return l
def shine(img,lay,p,width=90,strength=170):
    if p<=0 or p>=1: return
    bb=lay.getbbox()
    if not bb: return
    x=bb[0]-200+(bb[2]-bb[0]+400)*p
    yy,xx=np.mgrid[0:H,0:W]; band=np.clip(1-np.abs((xx+(yy-bb[1])*0.35)-x)/width,0,1)
    a=np.array(lay.split()[-1]).astype(np.float32)/255*band*strength
    s=Image.new("RGBA",(W,H),(255,244,228,0)); s.putalpha(Image.fromarray(a.astype(np.uint8))); img.alpha_composite(s)
def dim(img,k):
    if k<=0: return img
    a=np.array(img).astype(np.float32); a[...,:3]*=1-k; return Image.fromarray(a.astype(np.uint8))
def glow(lay,col,r=18,s=1.0):
    a=lay.split()[-1].filter(ImageFilter.GaussianBlur(r)).point(lambda v:int(min(255,v*1.6*s)))
    g=Image.new("RGBA",lay.size,col+(0,)); g.putalpha(a); return g
def chrome(img,n,tot=8,swipe=True):
    d=ImageDraw.Draw(img,"RGBA")
    txt(d,(60,64),"THE NATURAL ANGLE",B(30),CREAM,170,"ls"); txt(d,(W-60,64),f"{n}/{tot}",B(30),RUST,230,"rs")
    d.line((60,82,W-60,82),fill=RUST+(80,),width=2)
    if swipe:
        txt(d,(W-96,H-46),"SWIPE",B(28),RUST,235,"rs"); x=W-84;y=H-56
        d.line((x,y,x+30,y),fill=RUST+(235,),width=4); d.polygon([(x+30,y-9),(x+44,y),(x+30,y+9)],fill=RUST+(235,))
def credit(d,s,y=H-46,x=60,anchor="ls"): txt(d,(x,y),s,BM(24),GREY,225,anchor)
def brackets(d,x0,y0,x1,y1,col,a,Lb=46,w=4):
    c=col+(int(255*a),)
    for (x,y,sx,sy) in ((x0,y0,1,1),(x1,y0,-1,1),(x0,y1,1,-1),(x1,y1,-1,-1)):
        d.line((x,y,x+sx*Lb,y),fill=c,width=w); d.line((x,y,x,y+sy*Lb),fill=c,width=w)
def render(name,fr,dur):
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
        "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","64k","-movflags","+faststart",name],stdin=subprocess.PIPE)
    for k in range(int(dur*FPS)): p.stdin.write(np.array(fr(k/FPS))[...,:3].tobytes())
    p.stdin.close(); p.wait()
