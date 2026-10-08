import numpy as np, cv2, pickle, math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
HERE=os.path.dirname(os.path.abspath(__file__))+"/"
FD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/fonts/"
UP="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
GOLD=(255,200,70); CREAM=(250,246,236); RED=(255,72,60); CYAN=(70,225,235); WHITE=(255,255,255)
def F(n,s): return ImageFont.truetype(FD+n,s)
anton=lambda s:F("Anton-Regular.ttf",s); bcs=lambda s:F("BarlowCondensed-SemiBold.ttf",s); bar=lambda s:F("Barlow-Medium.ttf",s)
def ease(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def eo3(x): x=min(1,max(0,x)); return 1-(1-x)**3
def eob(x,k=1.7): x=min(1,max(0,x)); return 1+(k+1)*(x-1)**3+k*(x-1)**2
def seg(t,a,b): return min(1,max(0,(t-a)/(b-a)))
def lerp(a,b,x): return a+(b-a)*x
A=pickle.load(open(HERE+"assets.pkl","rb")); LAND=A["land"]; DEPTH=A["D"]; LANDRGB=A["land_rgb"]; SEAD=A["sea_detail"]
PPD=60; C85=math.cos(math.radians(8.5)); LON0,LAT1=60.0,30.0
# ---------------- noise tiles
def tile(seed,sig,size=512):
    r=np.random.default_rng(seed).normal(0,1,(size,size)).astype(np.float32)
    r=cv2.GaussianBlur(np.tile(r,(3,3)),(0,0),sig)[size:2*size,size:2*size]; return (r-r.mean())/(r.std()+1e-6)
N1=tile(1,3.0); N2=tile(2,6.0); N3=tile(3,1.5)
def scrolled(tilearr,w,h,scale,ox,oy):
    M=np.array([[1/scale,0,ox],[0,1/scale,oy]],np.float32)
    big=cv2.warpAffine(tilearr,M,(w,h),flags=cv2.INTER_LINEAR|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_WRAP)
    return big
# ---------------- map
def aff(lonc,latc,k,w,h): s=k/PPD; return np.array([[s,0,(LON0-lonc)*k*C85+w/2],[0,s,(latc-LAT1)*k+h/2]],np.float32)
def ll(lon,lat,lonc,latc,k,w,h,over=1.0):
    return ((lon-lonc)*k*C85+w/2,(latc-lat)*k+h/2)
def map_img(lonc,latc,k,w,h,t,level=0.0,glow=1.0):
    M=aff(lonc,latc,k,w,h)
    Dw=cv2.warpAffine(DEPTH,M,(w,h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=999)
    Dw=cv2.GaussianBlur(Dw,(0,0),1.2) if k>200 else Dw
    sd=cv2.warpAffine(SEAD,M,(w,h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    lr=cv2.warpAffine(LANDRGB,M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
    # land mask crisp
    vl0=lonc-w/2/(k*C85); vl1=lonc+w/2/(k*C85); vt1=latc+h/2/k; vb=latc-h/2/k
    mask=np.zeros((h,w),np.uint8); pts=[]
    for r in LAND:
        if r[:,0].max()<vl0 or r[:,0].min()>vl1 or r[:,1].max()<vb or r[:,1].min()>vt1: continue
        pts.append(np.stack([(r[:,0]-lonc)*k*C85+w/2,(latc-r[:,1])*k+h/2],1).astype(np.int32))
    if pts: cv2.fillPoly(mask,pts,255,lineType=cv2.LINE_AA)
    m=(mask.astype(np.float32)/255)[:,:,None]
    # ocean colour by depth
    d=Dw[:,:,None]; deep=np.array((4,34,84),np.float32); mid=np.array((10,112,170),np.float32); shal=np.array((40,214,210),np.float32)
    a1=np.clip(d/70,0,1); a2=np.clip((d-70)/130,0,1)
    oc=shal*(1-a1)+mid*a1; oc=oc*(1-a2)+deep*a2
    oc=oc*(1+sd[:,:,None]*1.6)
    # caustic shimmer in shallows
    sh=np.clip(1-d/110,0,1)
    c1=scrolled(N1,w,h,max(1.2,k/180),t*22,t*14); c2=scrolled(N2,w,h,max(2.0,k/120),-t*17,t*9)
    caus=np.clip((c1*c2)*0.35,0,1)[:,:,None]*sh*(110)
    oc=oc+caus*np.array((0.8,1.0,1.0),np.float32)
    # sparkle on deep water
    sp=np.clip(scrolled(N3,w,h,max(1.0,k/300),t*40,-t*30)-1.9,0,1)[:,:,None]*60
    oc=oc+sp*(1-sh)
    img=oc
    if level<-0.5:
        e=np.clip((abs(level)-d)/7,0,1)*(d<900)
        sand=np.array((222,190,112),np.float32)*(0.88+0.12*scrolled(N3,w,h,max(1,k/150),0,0)[:,:,None]*0.6)
        rim=np.clip(e*(1-e)*4,0,1)
        img=img*(1-e*0.95)+sand*e*0.95; img=img*(1-rim*0.5)+np.array((120,96,60),np.float32)*rim*0.5
    # land colour
    lc=lr.astype(np.float32)*np.array((0.72,0.98,0.62),np.float32)
    lc=lc*(0.92+0.16*scrolled(N3,w,h,max(1,k/120),0,0)[:,:,None]*0.5)
    img=img*(1-m)+lc*m
    # coast light
    if glow>0:
        gb=cv2.GaussianBlur(mask.astype(np.float32)/255,(0,0),max(3,k/45))
        outer=np.clip(gb*(1-mask.astype(np.float32)/255)*1.4,0,1)[:,:,None]
        img=img+outer*np.array((30,170,170),np.float32)*glow
        edge=np.clip(cv2.GaussianBlur(mask.astype(np.float32),(0,0),1.1)/255,0,1); ed=(mask.astype(np.float32)/255-cv2.erode(mask,np.ones((3,3),np.uint8)).astype(np.float32)/255)
        edge2=cv2.dilate(mask,np.ones((3,3),np.uint8)).astype(np.float32)/255-mask.astype(np.float32)/255
        img=img+np.clip(edge2,0,1)[:,:,None]*np.array((190,255,250),np.float32)*0.55*glow
    return np.clip(img,0,255).astype(np.uint8)
def tilt_warp(img,amt,W_=W,H_=H):
    """img rendered oversize; return W_xH_ with perspective tilt amt 0..0.3"""
    h,w=img.shape[:2]; cx,cy=w/2,h/2
    src=np.float32([[cx-W_/2,cy-H_/2],[cx+W_/2,cy-H_/2],[cx+W_/2,cy+H_/2],[cx-W_/2,cy+H_/2]])
    sh=amt*W_*0.5
    dst=np.float32([[sh,0],[W_-sh,0],[W_,H_],[0,H_]])
    # source slightly larger at top to compensate
    M=cv2.getPerspectiveTransform(src,dst); return cv2.warpPerspective(img,M,(W_,H_),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
# ---------------- text
_SP={}
FURTEX=None
def fur():
    global FURTEX
    if FURTEX is None:
        im=Image.open(UP+"a4bcbe52-image.jpg").convert("RGB"); w,h=im.size
        FURTEX=np.array(im.crop((int(w*.3),int(h*.38),int(w*.72),int(h*.62))).resize((900,420)))
        FURTEX=np.clip(FURTEX.astype(np.float32)*1.15,0,255).astype(np.uint8)
    return FURTEX
def sprite(text,font,fill,stroke=(0,0,0),sw=7,glow=None,glow_r=14,furfill=False,shadow=True,tex=None):
    key=(text,id(font),fill,stroke,sw,glow,furfill,tex)
    if key in _SP: return _SP[key]
    pad=int(glow_r*2.2+sw+10); d=ImageDraw.Draw(Image.new("L",(4,4))); bb=d.textbbox((0,0),text,font=font,stroke_width=sw)
    w=bb[2]-bb[0]+2*pad; h=bb[3]-bb[1]+2*pad; ox,oy=pad-bb[0],pad-bb[1]
    m=Image.new("L",(w,h),0); ImageDraw.Draw(m).text((ox,oy),text,font=font,fill=255); mf=np.array(m).astype(np.float32)/255
    ms=Image.new("L",(w,h),0); ImageDraw.Draw(ms).text((ox,oy),text,font=font,fill=255,stroke_width=sw,stroke_fill=255); msf=np.array(ms).astype(np.float32)/255
    out=np.zeros((h,w,4),np.float32)
    if glow is not None:
        g=cv2.GaussianBlur(msf,(0,0),glow_r)*1.6; g=np.clip(g,0,1)
        out[:,:,:3]+=np.array(glow,np.float32)*g[:,:,None]; out[:,:,3]=np.maximum(out[:,:,3],g*0.9)
    if shadow:
        sh=cv2.GaussianBlur(msf,(0,0),6); sh=np.roll(sh,(5,3),(0,1)); a=sh*0.6
        out[:,:,:3]=out[:,:,:3]*(1-a[:,:,None]); out[:,:,3]=np.maximum(out[:,:,3],a)
    # stroke
    a=msf[:,:,None]; out[:,:,:3]=out[:,:,:3]*(1-a)+np.array(stroke,np.float32)*a; out[:,:,3]=np.maximum(out[:,:,3],msf)
    # fill
    if furfill or tex:
        ft=cv2.resize(TEX[tex or 'tiger'](),(w,h)).astype(np.float32); col=ft
        yy=np.linspace(1.15,0.85,h)[:,None,None]; col=np.clip(col*yy,0,255)
    else:
        yy=np.linspace(1.0,0.82,h)[:,None,None]; col=np.array(fill,np.float32)*yy
    a=mf[:,:,None]; out[:,:,:3]=out[:,:,:3]*(1-a)+col*a; out[:,:,3]=np.maximum(out[:,:,3],mf)
    out[:,:,3]*=255; sp=np.clip(out,0,255).astype(np.uint8); _SP[key]=sp; return sp
def paste(fr,sp,cx,cy,a=1.0,s=1.0,rot=0.0):
    if a<=0.004: return
    if s!=1.0 or rot!=0.0:
        h,w=sp.shape[:2]; M=cv2.getRotationMatrix2D((w/2,h/2),rot,s); nw=int(w*s*1.15+abs(rot)*4+4); nh=int(h*s*1.15+abs(rot)*4+4)
        M[0,2]+=nw/2-w/2; M[1,2]+=nh/2-h/2; sp=cv2.warpAffine(sp,M,(nw,nh),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
    h,w=sp.shape[:2]; x=int(round(cx-w/2)); y=int(round(cy-h/2))
    x0=max(x,0); y0=max(y,0); x1=min(x+w,fr.shape[1]); y1=min(y+h,fr.shape[0])
    if x1<=x0 or y1<=y0: return
    s_=sp[y0-y:y1-y,x0-x:x1-x]; al=(s_[:,:,3:4].astype(np.float32)/255)*a
    fr[y0:y1,x0:x1]=(fr[y0:y1,x0:x1]*(1-al)+s_[:,:,:3]*al).astype(np.uint8)
def kt(fr,text,font,fill,cx,cy,t,t0,hold_end=None,dur=0.22,glow=None,furfill=False,sw=7,rot=0,glitch=True,fadeout=0.15,sy=0,tex=None):
    """kinetic pop text"""
    if t<t0: return
    if hold_end is not None and t>hold_end+fadeout: return
    p=seg(t,t0,t0+dur); s=lerp(1.5,1.0,eob(p,1.4)); a=min(1,p*3)
    if hold_end is not None and t>hold_end: a*=1-(t-hold_end)/fadeout
    sp=sprite(text,font,fill,sw=sw,glow=glow,furfill=furfill,tex=tex)
    if glitch and t-t0<0.14:
        for dx,col in ((-9,(255,0,60)),(9,(0,230,255))):
            g=sp.copy(); g[:,:,:3]=col; paste(fr,g,cx+dx,cy+sy,0.55*a,s,rot)
    paste(fr,sp,cx,cy+sy,a,s,rot)
def pill(fr,t_,cx,cy,a=1.0,fg=(20,16,8),bg=GOLD,size=40,s=1.0,outline=None):
    f=bcs(size); d=ImageDraw.Draw(Image.new("L",(4,4))); tw=d.textlength(t_,font=f); w=int(tw+56); h=size+30
    sp=np.zeros((h+20,w+20,4),np.uint8); pil=Image.fromarray(sp); dr=ImageDraw.Draw(pil)
    dr.rounded_rectangle([10,10,w+10,h+10],radius=h//2,fill=bg+(255,),outline=(outline+(255,)) if outline else None,width=3)
    dr.text((10+28,10+14),t_,font=f,fill=fg+(255,)); sp=np.array(pil)
    paste(fr,sp,cx,cy,a,s)
def ring(fr,cx,cy,r,col,a,w=3):
    if a<=0.01 or r<2: return
    ov=fr.copy(); cv2.circle(ov,(int(cx),int(cy)),int(r),col[::-1] if False else col,w,cv2.LINE_AA); fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
def gradv(fr,y0,y1,a0,a1,col=(6,10,14)):
    ys=np.arange(fr.shape[0])[:,None]; t=np.clip((ys-y0)/max(1,(y1-y0)),0,1); a=(a0+(a1-a0)*t)[:,:,None]
    fr[:]=(fr*(1-a)+np.array(col,np.float32)*a).astype(np.uint8)
def fade(fr,a,col=(0,0,0)):
    if a>0: fr[:]=(fr*(1-a)+np.array(col,np.float32)*a).astype(np.uint8)
def add(fr,layer,k=1.0): fr[:]=np.clip(fr.astype(np.float32)+layer*k,0,255).astype(np.uint8)
# ---------------- particles
_R=np.random.default_rng(21); PN=90
PX=_R.uniform(0,W,PN); PY=_R.uniform(0,H,PN); PS=_R.uniform(1.5,6.5,PN); PV=_R.uniform(8,40,PN); PD=_R.uniform(0.3,1.0,PN); PP=_R.uniform(0,6.28,PN)
def motes(fr,t,strength=1.0,col=(255,235,190)):
    ov=np.zeros((H,W,3),np.float32)
    for i in range(PN):
        x=(PX[i]+math.sin(t*0.7+PP[i])*24+t*PV[i]*0.3)%W; y=(PY[i]-t*PV[i]*PD[i]*1.2)%H
        r=PS[i]; a=PD[i]*(0.6+0.4*math.sin(t*2+PP[i]))
        cv2.circle(ov,(int(x),int(y)),int(r),tuple(float(c)*a for c in col),-1,cv2.LINE_AA)
    ov=cv2.GaussianBlur(ov,(0,0),2.0); add(fr,ov,strength*0.9)
# ---------------- photo parallax
_PH={}; _CUT={}
def photo(k):
    if k not in _PH:
        im=Image.open(UP+k+"-image.jpg").convert("RGB"); w,h=im.size; s=min(1.0,3600/max(w,h)); _PH[k]=np.array(im.resize((int(w*s),int(h*s)),Image.LANCZOS))
    return _PH[k]
def cutout(k):
    if k not in _CUT:
        c=np.array(Image.open(HERE+f"cut_{k}.png")); a=c[:,:,3].astype(np.float32)/255
        a=cv2.GaussianBlur(cv2.erode((a*255).astype(np.uint8),np.ones((3,3),np.uint8)).astype(np.float32)/255,(0,0),1.3)
        c[:,:,3]=(a*255).astype(np.uint8); _CUT[k]=c
    return _CUT[k]
def pwin(k,cx,cy,wf,ow,oh,dim=1.0,rot=0.0):
    im=photo(k); ih,iw=im.shape[:2]; cw=wf*iw; ch=cw*oh/ow
    if ch>ih: ch=ih; cw=ch*ow/oh
    s=ow/cw*(1.035 if rot else 1.0); cw2=ow/s; ch2=oh/s; xc=min(max(cx*iw,cw2/2),iw-cw2/2); yc=min(max(cy*ih,ch2/2),ih-ch2/2)
    M=cv2.getRotationMatrix2D((xc,yc),rot,s); M[0,2]+=ow/2-xc; M[1,2]+=oh/2-yc
    out=cv2.warpAffine(im,M,(ow,oh),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    return out if dim==1.0 else (out*dim).astype(np.uint8)
def para(k,cx,cy,wf_bg,wf_fg,ow,oh,dxfg=0.0,dyfg=0.0,blur=9,dim=1.0,rot=0.0):
    """2.5D: blurred bg (wider) + sharp cutout fg (tighter), fg covers bg subject"""
    bg=pwin(k,cx,cy,wf_bg,ow,oh,dim,rot); 
    if blur>0: bg=cv2.GaussianBlur(bg,(0,0),blur)
    cut=cutout(k); ih,iw=cut.shape[:2]; cw=wf_fg*iw; ch=cw*oh/ow
    if ch>ih: ch=ih; cw=ch*ow/oh
    s=ow/cw*(1.035 if rot else 1.0); cw2=ow/s; ch2=oh/s; xc=min(max((cx+dxfg)*iw,cw2/2),iw-cw2/2); yc=min(max((cy+dyfg)*ih,ch2/2),ih-ch2/2)
    M=cv2.getRotationMatrix2D((xc,yc),rot,s); M[0,2]+=ow/2-xc; M[1,2]+=oh/2-yc
    fg=cv2.warpAffine(cut,M,(ow,oh),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
    a=fg[:,:,3:4].astype(np.float32)/255; out=bg.astype(np.float32)*(1-a)+(fg[:,:,:3].astype(np.float32)*dim)*a
    return np.clip(out,0,255).astype(np.uint8)
# ---------------- global look
VIG=None; GR=None; LUT=None
def look(fr,t,hits):
    global VIG,GR,LUT
    if VIG is None:
        yy,xx=np.mgrid[0:H,0:W]; d=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2); VIG=(1-0.32*np.clip(d-0.5,0,1)**1.3).astype(np.float32)[:,:,None]
        GR=np.random.default_rng(3).normal(0,3.2,(H+64,W+64,1)).astype(np.float32)
        x=np.arange(256)/255.0; s=x+0.16*(x-0.5)*(1-np.abs(2*x-1)); LUT=(np.clip(s,0,1)*255).astype(np.uint8)
    f=cv2.LUT(fr,LUT).astype(np.float32)
    # slight teal shadows / warm highlights
    lum=f.mean(2,keepdims=True)/255
    f=f+(1-lum)*np.array((-6,3,8),np.float32)+lum*np.array((8,3,-6),np.float32)
    # saturation
    g=f.mean(2,keepdims=True); f=g+(f-g)*1.14
    ox=int((t*977)%64); oy=int((t*613)%64)
    return np.clip(f*VIG+GR[oy:oy+H,ox:ox+W],0,255).astype(np.uint8)
def punch(fr,t,hits):
    """zoom pulse + flash from hit list [(time,strength)]"""
    z=0.0; fl=0.0; shx=0.0; shy=0.0
    for (th,s) in hits:
        dt=t-th
        if 0<=dt<0.35:
            e=math.exp(-dt*11); z+=0.035*s*e; fl+=0.16*s*e*(dt<0.12)
            if s>=1.2: shx+=math.sin(dt*90)*10*s*e; shy+=math.cos(dt*80)*8*s*e
    if z>0.001 or shx!=0 or shy!=0:
        sc=1+z; M=np.array([[sc,0,(1-sc)*W/2+shx],[0,sc,(1-sc)*H/2+shy]],np.float32); fr=cv2.warpAffine(fr,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    if fl>0.01: fr=np.clip(fr.astype(np.float32)+255*fl,0,255).astype(np.uint8)
    return fr
def flare(fr,y,a,col=(255,230,180)):
    if a<=0.01: return
    ov=np.zeros((H,W,3),np.float32); cv2.line(ov,(0,int(y)),(W,int(y)),tuple(float(c) for c in col),3,cv2.LINE_AA); ov=cv2.GaussianBlur(ov,(0,0),14)*3.0; add(fr,ov,a)
def hud_corners(fr,x0,y0,x1,y1,col=CYAN,a=1.0,L=60,w=4):
    ov=fr.copy()
    for (x,y,sx,sy) in ((x0,y0,1,1),(x1,y0,-1,1),(x0,y1,1,-1),(x1,y1,-1,-1)):
        cv2.line(ov,(x,y),(x+sx*L,y),col,w,cv2.LINE_AA); cv2.line(ov,(x,y),(x,y+sy*L),col,w,cv2.LINE_AA)
    fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)

# ---------------- procedural textures
def _rosette():
    r=np.random.default_rng(8); w,h=900,420; img=np.zeros((h,w,3),np.float32); img[:]=(214,164,72)
    n=cv2.resize(r.normal(0,1,(21,45)).astype(np.float32),(w,h),interpolation=cv2.INTER_CUBIC); img+=n[:,:,None]*14
    for _ in range(34):
        x=r.uniform(0,w); y=r.uniform(0,h); a=r.uniform(40,64); b=a*r.uniform(0.75,1.0); ang=r.uniform(0,180)
        cv2.ellipse(img,(int(x),int(y)),(int(a),int(b)),ang,0,360,(70,42,14),int(r.uniform(9,13)),cv2.LINE_AA)
        cv2.ellipse(img,(int(x),int(y)),(int(a*0.55),int(b*0.55)),ang,0,360,(190,132,50),-1,cv2.LINE_AA)
    return np.clip(img,0,255).astype(np.uint8)
def _lion():
    r=np.random.default_rng(9); w,h=900,420; base=np.zeros((h,w,3),np.float32); g=np.linspace(0,1,h)[:,None]
    base[:]=(236,182,96); base=base*(1-g[:,:,None]*0.45)+np.array((120,66,28),np.float32)*(g[:,:,None]*0.45)
    n=cv2.GaussianBlur(r.normal(0,1,(h,w)).astype(np.float32),(0,0),sigmaX=1.2,sigmaY=14); n=n/n.std()
    base+=n[:,:,None]*30; return np.clip(base,0,255).astype(np.uint8)
_T={}
def _tx(name,fn):
    if name not in _T: _T[name]=fn()
    return _T[name]
TEX={'tiger':fur,'rosette':lambda:_tx('rosette',_rosette),'lion':lambda:_tx('lion',_lion)}

def pext(k,y0,zoom=1.0):
    """photo scaled to full width, placed at bottom (top band extended with blur)"""
    im=photo(k); ih,iw=im.shape[:2]; ph=int(W*ih/iw); big=cv2.resize(im,(int(W*zoom),int(ph*zoom)),interpolation=cv2.INTER_AREA if zoom<1 else cv2.INTER_LINEAR)
    # place with bottom aligned
    canvas=cv2.GaussianBlur(cv2.resize(im,(W,H)),(0,0),30); canvas=(canvas*0.6).astype(np.uint8)
    top=H-big.shape[0]; xo=(big.shape[1]-W)//2
    sharp=big[:,xo:xo+W]; m=np.ones((sharp.shape[0],1,1),np.float32)
    for i in range(140): m[i]=i/140
    reg=canvas[top:H].astype(np.float32); canvas[top:H]=(reg*(1-m)+sharp.astype(np.float32)*m).astype(np.uint8)
    return canvas
