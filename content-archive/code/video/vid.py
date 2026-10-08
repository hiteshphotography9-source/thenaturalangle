import numpy as np, cv2, pickle, math, os, sys
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1080,1920,30
FD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/fonts/"
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
GOLD=(232,196,118); CREAM=(244,238,226); RED=(214,96,78); BLUEW=(120,176,196)
OCEAN=np.array((9,20,26),np.float32); SHELF=np.array((20,46,54),np.float32); EXPO=np.array((110,98,62),np.float32); LANDC=(38,50,41)
def F(name,s): return ImageFont.truetype(FD+name,s)
anton=lambda s:F("Anton-Regular.ttf",s); bcs=lambda s:F("BarlowCondensed-SemiBold.ttf",s); bar=lambda s:F("Barlow-Regular.ttf",s); barm=lambda s:F("Barlow-Medium.ttf",s)
def corm(s):
    f=F("CormorantGaramond-Italic[wght].ttf",s)
    try: f.set_variation_by_axes([500])
    except Exception: pass
    return f
GEO=pickle.load(open('/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/vid/geo.pkl','rb'))
LAND=GEO['land']; DEEP=GEO['D']; C85=math.cos(math.radians(8.5)); PPD=160; RLON0,RLAT1=76.0,12.0
def ease(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def seg(t,a,b): return min(1,max(0,(t-a)/(b-a)))
def lerp(a,b,x): return a+(b-a)*x
# ---------- photos
PH={}
def photo(k):
    if k not in PH:
        im=Image.open(U+k+"-image.jpg").convert("RGB"); w,h=im.size; s=min(1.0,4800/max(w,h))
        PH[k]=np.array(im.resize((int(w*s),int(h*s)),Image.LANCZOS))
    return PH[k]
def pwin(k,cx,cy,wf,ow,oh,dim=1.0):
    """window centered (cx,cy) in image fractions, width wf of image width, output ow x oh"""
    im=photo(k); ih,iw=im.shape[:2]; cw=wf*iw; ch=cw*oh/ow
    if ch>ih: ch=ih; cw=ch*ow/oh
    x0=min(max(cx*iw-cw/2,0),iw-cw); y0=min(max(cy*ih-ch/2,0),ih-ch)
    s=ow/cw; M=np.array([[s,0,-x0*s],[0,s,-y0*s]],np.float32)
    out=cv2.warpAffine(im,M,(ow,oh),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    return out if dim==1.0 else (out*dim).astype(np.uint8)
# ---------- map
def cam_M(lonc,latc,k,w,h):
    s=k/PPD; return np.array([[s,0,(RLON0-lonc)*k*C85+w/2],[0,s,(latc-RLAT1)*k+h/2]],np.float32)
def map_img(lonc,latc,k,w,h,level=0.0,grid=True):
    M=cam_M(lonc,latc,k,w,h)
    Dw=cv2.warpAffine(DEEP,M,(w,h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=999)
    shelf=np.clip(1-Dw/200,0,1)*0.55; base=OCEAN[None,None,:]*(1-shelf[:,:,None])+SHELF[None,None,:]*shelf[:,:,None]
    if level<0:
        a=np.clip((abs(level)-Dw)/10.0,0,1)*(Dw<900)
        base=base*(1-a[:,:,None]*0.92)+EXPO[None,None,:]*a[:,:,None]*0.92
    img=np.clip(base,0,255).astype(np.uint8)
    if grid:
        for lon in range(60,100,2):
            x=int((lon-lonc)*k*C85+w/2)
            if 0<=x<w: img[:,x]=np.clip(img[:,x].astype(np.int16)+7,0,255)
        for lat in range(-4,36,2):
            y=int((latc-lat)*k+h/2)
            if 0<=y<h: img[y,:]=np.clip(img[y,:].astype(np.int16)+7,0,255)
    vlon0=lonc-w/2/(k*C85); vlon1=lonc+w/2/(k*C85); vlat1=latc+h/2/k; vlat0=latc-h/2/k
    pts=[]
    for r in LAND:
        if r[:,0].max()<vlon0 or r[:,0].min()>vlon1 or r[:,1].max()<vlat0 or r[:,1].min()>vlat1: continue
        pts.append(np.stack([(r[:,0]-lonc)*k*C85+w/2,(latc-r[:,1])*k+h/2],1).astype(np.int32))
    if pts:
        cv2.fillPoly(img,pts,LANDC,lineType=cv2.LINE_AA)
        cv2.polylines(img,pts,True,GOLD,max(1,int(k/160)+1),lineType=cv2.LINE_AA)
    return img
def ll2px(lon,lat,lonc,latc,k,w,h): return ((lon-lonc)*k*C85+w/2,(latc-lat)*k+h/2)
# ---------- text sprites
_SP={}
def sprite(text,font,fill,shadow=True,pad=18):
    key=(text,id(font),fill)
    if key in _SP: return _SP[key]
    d=ImageDraw.Draw(Image.new("L",(4,4))); bb=d.textbbox((0,0),text,font=font); w=bb[2]-bb[0]+2*pad; h=bb[3]-bb[1]+2*pad
    im=Image.new("RGBA",(w,h),(0,0,0,0)); dd=ImageDraw.Draw(im)
    if shadow: dd.text((pad-bb[0]+2,pad-bb[1]+3),text,font=font,fill=(0,0,0,150))
    dd.text((pad-bb[0],pad-bb[1]),text,font=font,fill=fill+(255,)); _SP[key]=np.array(im); return _SP[key]
def blit(fr,sp,x,y,a=1.0):
    if a<=0.003: return
    x=int(round(x)); y=int(round(y)); h,w=sp.shape[:2]
    x0=max(x,0); y0=max(y,0); x1=min(x+w,fr.shape[1]); y1=min(y+h,fr.shape[0])
    if x1<=x0 or y1<=y0: return
    s=sp[y0-y:y1-y,x0-x:x1-x]; al=(s[:,:,3:4].astype(np.float32)/255)*a
    fr[y0:y1,x0:x1]=(fr[y0:y1,x0:x1]*(1-al)+s[:,:,:3]*al).astype(np.uint8)
def text(fr,t,font,fill,x,y,a=1.0,anchor="l",rise=0):
    sp=sprite(t,font,fill); h,w=sp.shape[:2]
    if anchor=="c": x=x-w/2
    elif anchor=="r": x=x-w
    blit(fr,sp,x-18,y-18+rise*(1-min(1,a)),a)
def rrect(fr,x0,y0,x1,y1,fill=None,outline=None,a=1.0,r=14,w=3):
    ov=fr.copy(); 
    pil=Image.fromarray(ov); d=ImageDraw.Draw(pil,"RGBA")
    d.rounded_rectangle([x0,y0,x1,y1],radius=r,fill=(fill+(int(215*a),)) if fill else None,outline=(outline+(int(255*a),)) if outline else None,width=w)
    fr[:]=np.array(pil)
def pill(fr,t,x,y,a=1.0,fg=CREAM,bg=(12,14,12),size=34,anchor="l",outline=None):
    f=bcs(size); d=ImageDraw.Draw(Image.new("L",(4,4))); tw=d.textlength(t,font=f); w=tw+44; h=size+26
    if anchor=="c": x=x-w/2
    rrect(fr,x,y,x+w,y+h,fill=bg,outline=outline,a=a,r=h//2 if outline is None else 10)
    text(fr,t,f,fg,x+22,y+9,a)
    return w
def ring(fr,cx,cy,r,col,a,w=3):
    if a<=0.01 or r<2: return
    ov=fr.copy(); cv2.circle(ov,(int(cx),int(cy)),int(r),col,w,cv2.LINE_AA); fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
def gradv(fr,y0,y1,a0,a1,col=(8,10,9)):
    ys=np.arange(fr.shape[0])[:,None]; t=np.clip((ys-y0)/max(1,(y1-y0)),0,1); a=(a0+(a1-a0)*t)[:,:,None]
    fr[:]=(fr*(1-a)+np.array(col,np.float32)*a).astype(np.uint8)
def fade(fr,a,col=(0,0,0)): 
    if a>0: fr[:]=(fr*(1-a)+np.array(col,np.float32)*a).astype(np.uint8)
