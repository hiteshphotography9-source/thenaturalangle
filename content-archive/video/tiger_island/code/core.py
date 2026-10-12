import numpy as np, cv2, pickle, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
SP="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/"
FD=SP+"fonts/"; U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
GOLD=(232,196,118); CREAM=(244,238,226); RED=(226,92,72); BLUEW=(120,190,214); GREY=(168,172,170); INK=(14,16,18); TEAL=(96,206,196)
def F(n,s): return ImageFont.truetype(FD+n,int(s))
anton=lambda s:F("Anton-Regular.ttf",s); bcs=lambda s:F("BarlowCondensed-SemiBold.ttf",s); bcm=lambda s:F("BarlowCondensed-Medium.ttf",s)
def ease(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def eo3(x): x=min(1,max(0,x)); return 1-(1-x)**3
def eob(x,k=1.7): x=min(1,max(0,x)); return 1+(k+1)*(x-1)**3+k*(x-1)**2
def seg(t,a,b): return min(1,max(0,(t-a)/(b-a)))
def lerp(a,b,x): return a+(b-a)*x
G=pickle.load(open(SP+"island/geo.pkl","rb"))
OCEAN=np.array((8,22,32),np.float32); SHELF=np.array((18,52,64),np.float32); EXPO=np.array((112,100,64),np.float32); LANDC=np.array((44,58,46),np.float32)
_rng=np.random.default_rng(7)
TEXN=cv2.GaussianBlur(_rng.normal(0,1,(H,W)).astype(np.float32),(0,0),2.2); TEXN/=np.abs(TEXN).max()
TEXL=cv2.GaussianBlur(_rng.normal(0,1,(H,W)).astype(np.float32),(0,0),40); TEXL/=np.abs(TEXL).max()
class Cam:
    def __init__(s,lonc,latc,k,w=W,h=H): s.lonc,s.latc,s.k,s.w,s.h=lonc,latc,k,w,h; s.c=math.cos(math.radians(latc))
    def px(s,lon,lat): return ((lon-s.lonc)*s.k*s.c+s.w/2,(s.latc-lat)*s.k+s.h/2)
    def view(s):
        dx=s.w/2/(s.k*s.c); dy=s.h/2/s.k; return (s.lonc-dx,s.latc-dy,s.lonc+dx,s.latc+dy)
def _fill(mask,polys,cam):
    v=cam.view()
    for bb,rings in polys:
        if bb[2]<v[0] or bb[0]>v[2] or bb[3]<v[1] or bb[1]>v[3]: continue
        for i,r in enumerate(rings):
            x=((r[:,0]-cam.lonc)*cam.k*cam.c+cam.w/2)*16; y=((cam.latc-r[:,1])*cam.k+cam.h/2)*16
            pts=np.stack([x,y],1).astype(np.int64)
            pts=np.clip(pts,-2**30,2**30).astype(np.int32)
            cv2.fillPoly(mask,[pts],255 if i==0 else 0,cv2.LINE_AA,shift=4)
def map_img(cam,level=0.0,coast=1.0):
    land=np.zeros((cam.h,cam.w),np.uint8); _fill(land,G['land'],cam)
    deep=np.zeros((cam.h,cam.w),np.uint8); _fill(deep,G['deep'],cam)
    L=land.astype(np.float32)[...,None]/255; D=deep.astype(np.float32)[...,None]/255
    D=np.maximum(D,0)*(1-L)
    sea=OCEAN*D+SHELF*(1-D)
    if level>0: sea=sea*(1-(1-D)*level)+EXPO*(1-D)*level
    img=sea*(1-L)+LANDC*L
    tn=TEXN[:cam.h,:cam.w,None]; tl=TEXL[:cam.h,:cam.w,None]
    img=img*(1+0.06*tn+0.10*tl)
    if coast>0:
        e=cv2.dilate(land,np.ones((3,3),np.uint8)).astype(np.float32)-land.astype(np.float32)
        g=cv2.GaussianBlur(land.astype(np.float32),(0,0),6)/255*(1-L[...,0])
        img+=np.clip(e/255,0,1)[...,None]*np.array((150,200,190))*0.55*coast+g[...,None]*np.array((20,60,60))*coast
        if level>0:
            sh=(1-D[...,0])*(1-L[...,0]); e2=cv2.dilate((sh*255).astype(np.uint8),np.ones((3,3),np.uint8)).astype(np.float32)/255-sh
            img+=np.clip(e2,0,1)[...,None]*np.array((220,190,120))*0.5*level
    return np.clip(img,0,255).astype(np.uint8)
# ---------- photos
PH={}
def photo(k):
    if k not in PH:
        im=Image.open(U+k+"-image.jpg").convert("RGB"); w,h=im.size; s=min(1.0,3600/max(w,h))
        PH[k]=np.array(im.resize((int(w*s),int(h*s)),Image.LANCZOS))
    return PH[k]
def pwin(k,cx,cy,wf,ow=W,oh=H):
    im=photo(k); ih,iw=im.shape[:2]; cw=wf*iw; ch=cw*oh/ow
    if ch>ih: ch=ih; cw=ch*ow/oh
    x0=min(max(cx*iw-cw/2,0),iw-cw); y0=min(max(cy*ih-ch/2,0),ih-ch)
    s=ow/cw; M=np.array([[s,0,-x0*s],[0,s,-y0*s]],np.float32)
    return cv2.warpAffine(im,M,(ow,oh),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
def gradv(fr,y0,y1,a0,a1,col=(4,8,10)):
    y0=int(y0);y1=int(y1); a=np.linspace(a0,a1,y1-y0,dtype=np.float32)[:,None,None]
    fr[y0:y1]=(fr[y0:y1]*(1-a)+np.array(col,np.float32)*a).astype(np.uint8)
# ---------- text/overlay layer helpers (PIL RGBA overlay per frame)
class Ov:
    def __init__(s): s.im=Image.new("RGBA",(W,H),(0,0,0,0)); s.d=ImageDraw.Draw(s.im,"RGBA")
    def text(s,xy,t,f,col,a=1.0,anchor="ms",shadow=True,rise=0,stroke=0):
        if a<=0.003: return
        x,y=xy; y=y+(1-a)*rise
        if shadow:
            sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).text((x+3,y+5),t,font=f,fill=(0,0,0,int(200*a)),anchor=anchor)
            s.im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
        s.d.text((x,y),t,font=f,fill=col+(int(255*a),),anchor=anchor,stroke_width=stroke,stroke_fill=(0,0,0,int(200*a)))
    def pill(s,xy,t,f,a=1.0,fg=INK,bg=GOLD,anchor="mm",pad=(24,12),outline=None,sc=1.0):
        if a<=0.003: return
        x,y=xy; tw=f.getlength(t); bb=f.getbbox("Ag"); th=bb[3]-bb[1]
        w=(tw+2*pad[0])*sc; h=(th+2*pad[1])*sc
        if anchor=="mm": x0=x-w/2
        elif anchor=="lm": x0=x
        else: x0=x-w
        s.d.rounded_rectangle((x0,y-h/2,x0+w,y+h/2),radius=h/2,fill=bg+(int(235*a),),outline=(outline+(int(255*a),)) if outline else None,width=3)
        if sc>0.6: s.d.text((x0+w/2,y+th*0.02),t,font=f,fill=fg+(int(255*a),),anchor="mm")
        return (x0,y-h/2,x0+w,y+h/2)
    def card(s,box,a=1.0,fill=(10,14,16),edge=GOLD,ea=0.6):
        if a<=0.003: return
        s.d.rounded_rectangle(box,radius=22,fill=fill+(int(215*a),),outline=edge+(int(255*ea*a),),width=3)
    def ring(s,x,y,r,col,a,w=3): 
        if a>0: s.d.ellipse((x-r,y-r,x+r,y+r),outline=col+(int(255*min(1,a)),),width=w)
    def dot(s,x,y,r,col,a=1.0,edge=CREAM):
        if a>0: s.d.ellipse((x-r,y-r,x+r,y+r),fill=col+(int(255*a),),outline=edge+(int(255*a),),width=3)
    def dash(s,pts,col,a,prog=1.0,dl=18,gap=12,w=5):
        if a<=0 or prog<=0: return
        seglen=[math.dist(pts[i],pts[i+1]) for i in range(len(pts)-1)]; tot=sum(seglen); lim=tot*prog; pos=0
        for i in range(len(pts)-1):
            (x0,y0),(x1,y1)=pts[i],pts[i+1]; L=seglen[i]
            if L==0: continue
            u=0
            while u<L and pos+u<lim:
                u1=min(L,u+dl,lim-pos); f0=u/L; f1=u1/L
                s.d.line((x0+(x1-x0)*f0,y0+(y1-y0)*f0,x0+(x1-x0)*f1,y0+(y1-y0)*f1),fill=col+(int(255*a),),width=w)
                u+=dl+gap
            pos+=L
        return
    def arrowhead(s,p0,p1,col,a,size=22):
        ang=math.atan2(p1[1]-p0[1],p1[0]-p0[0]); x,y=p1
        pts=[(x,y),(x-size*math.cos(ang-0.45),y-size*math.sin(ang-0.45)),(x-size*math.cos(ang+0.45),y-size*math.sin(ang+0.45))]
        s.d.polygon(pts,fill=col+(int(255*a),))
    def apply(s,fr):
        a=np.array(s.im).astype(np.float32); al=a[...,3:4]/255
        return np.clip(fr*(1-al)+a[...,:3]*al,0,255).astype(np.uint8)
def bez(p0,p1,p2,n=40): return [((1-u)**2*p0[0]+2*(1-u)*u*p1[0]+u*u*p2[0],(1-u)**2*p0[1]+2*(1-u)*u*p1[1]+u*u*p2[1]) for u in np.linspace(0,1,n)]
