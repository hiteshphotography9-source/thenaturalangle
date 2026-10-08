import sys; sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/vid/v2')
from eng import *
import eng
PN="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pn/src/"
def vign(fr,s=0.35):
    h,w=fr.shape[:2]; yy,xx=np.mgrid[0:h,0:w]; d=np.sqrt(((xx-w/2)/(w/2))**2+((yy-h/2)/(h/2))**2); v=(1-s*np.clip(d-0.5,0,1)**1.3)[:,:,None]
    g=np.random.default_rng(3).normal(0,2.5,(h,w,1)); return np.clip(fr*v+g,0,255).astype(np.uint8)
def grade(fr,c=1.1,sat=1.15):
    f=fr.astype(np.float32); f=(f-128)*c+128+6; g=f.mean(2,keepdims=True); f=g+(f-g)*sat; return np.clip(f,0,255).astype(np.uint8)
def stext(fr,t,font,fill,cx,cy,glow=None,sw=9,anchor="c",rot=0,tex=None):
    sp=sprite(t,font,fill,sw=sw,glow=glow,tex=tex)
    if anchor=="l": cx=cx+sp.shape[1]/2-30
    paste(fr,sp,cx,cy,1.0,1.0,rot)
def gradH(fr,x0,x1,a0,a1,col=(6,10,14)):
    h,w=fr.shape[:2]; xs=np.arange(w)[None,:]; t=np.clip((xs-x0)/max(1,(x1-x0)),0,1); a=(a0+(a1-a0)*t)[:,:,None]; fr[:]=(fr*(1-a)+np.array(col,np.float32)*a).astype(np.uint8)
def gradV(fr,y0,y1,a0,a1,col=(6,10,14)):
    h,w=fr.shape[:2]; ys=np.arange(h)[:,None]; t=np.clip((ys-y0)/max(1,(y1-y0)),0,1); a=(a0+(a1-a0)*t)[:,:,None]; fr[:]=(fr*(1-a)+np.array(col,np.float32)*a).astype(np.uint8)
def cutpaste(fr,k,cx,cy,wf,dx=0,dy=0,dim=1.0,rot=0):
    """paste cutout of photo k so that window of width wf (image fraction) maps to full frame width"""
    h,w=fr.shape[:2]; cut=cutout(k); ih,iw=cut.shape[:2]; cw=wf*iw; s=w/cw; xc=cx*iw; yc=cy*ih
    M=cv2.getRotationMatrix2D((xc,yc),rot,s); M[0,2]+=w/2-xc+dx; M[1,2]+=h/2-yc+dy
    fg=cv2.warpAffine(cut,M,(w,h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
    a=fg[:,:,3:4].astype(np.float32)/255; fr[:]=np.clip(fr.astype(np.float32)*(1-a)+fg[:,:,:3].astype(np.float32)*dim*a,0,255).astype(np.uint8)
def save(fr,name,q=95): cv2.imwrite(name,cv2.cvtColor(fr,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,q])
# ================= THUMBNAILS 1280x720
TW,TH=1280,720
def thumb_srilanka():
    img=map_img(80.35,8.4,330,TW,TH,1.3,0.0)           # Sri Lanka + strait
    img=grade(img,1.12,1.2); fr=img.copy()
    gradH(fr,300,900,0.0,0.0)
    # tiger right
    bg=pwin("a4bcbe52",0.5,0.4,0.9,TW,TH,0.5); 
    mask=np.zeros((TH,TW),np.float32); mask[:,640:]=1; mask=cv2.GaussianBlur(mask,(0,0),60)[:,:,None]
    fr=(fr*(1-mask*0.9)+bg*(mask*0.9)).astype(np.uint8)
    cutpaste(fr,"a4bcbe52",0.5,0.40,0.80,dx=330,dy=60,dim=1.06)
    gradH(fr,0,760,0.45,0.0)
    stext(fr,"NO TIGERS",anton(150),WHITE,370,190,glow=(0,0,0),sw=10)
    stext(fr,"IN SRI LANKA?",anton(124),GOLD,420,340,glow=(255,150,0),sw=10)
    # red zero badge
    cv2.circle(fr,(160,560),92,(10,16,20),-1,cv2.LINE_AA); cv2.circle(fr,(160,560),92,RED,12,cv2.LINE_AA)
    stext(fr,"0",anton(130),WHITE,160,560,glow=(255,40,30),sw=6)
    pill(fr,"WILD TIGERS",330,590,1.0,fg=WHITE,bg=RED,size=44) if False else None
    stext(fr,"WILD TIGERS",bcs(70),WHITE,420,595,glow=None,sw=6)
    return vign(fr,0.3)
def thumb_panna():
    L=cv2.cvtColor(cv2.imread(PN+"s_%04d.jpg"%(int(21.0*30)+1)),cv2.COLOR_BGR2RGB); R=cv2.cvtColor(cv2.imread(PN+"s_%04d.jpg"%(int(31.0*30)+1)),cv2.COLOR_BGR2RGB)
    def crop(im,cx,cy,w_):
        h,w=im.shape[:2]; cw=w_; ch=cw*TH/ (TW/2+160); x0=int(cx*w-cw/2); y0=int(cy*h-ch/2); x0=max(0,min(w-int(cw),x0)); y0=max(0,min(h-int(ch),y0))
        return cv2.resize(im[y0:y0+int(ch),x0:x0+int(cw)],(TW//2+160,TH),interpolation=cv2.INTER_CUBIC)
    a=crop(L,0.52,0.60,1000); b=crop(R,0.32,0.58,900)
    fr=np.zeros((TH,TW,3),np.uint8); fr[:,:TW//2+160]=a
    m=np.zeros((TH,TW),np.uint8); poly=np.array([[TW//2-80,0],[TW,0],[TW,TH],[TW//2-170,TH]],np.int32); cv2.fillPoly(m,[poly],255,cv2.LINE_AA)
    full_b=np.zeros_like(fr); full_b[:,TW-(TW//2+160):]=b
    mm=(cv2.GaussianBlur(m,(0,0),1.2).astype(np.float32)/255)[:,:,None]; fr=(fr*(1-mm)+full_b*mm).astype(np.uint8)
    fr=grade(fr,1.18,1.3)
    cv2.line(fr,(TW//2-80,0),(TW//2-170,TH),(255,210,80),10,cv2.LINE_AA)
    gradV(fr,0,200,0.55,0.0); gradV(fr,420,TH,0.0,0.82)
    stext(fr,"TOURIST",anton(120),WHITE,300,590,glow=(0,0,0),sw=9)
    stext(fr,"vs",bcs(80),GOLD,TW//2-20,640,glow=None,sw=6)
    stext(fr,"PHOTOGRAPHER",anton(96),GOLD,930,590,glow=(255,150,0),sw=9)
    pill(fr,"PANNA TIGER RESERVE",TW//2,60,1.0,fg=(20,16,8),bg=GOLD,size=40)
    return vign(fr,0.3)
def thumb_pilibhit():
    bg=pwin("c31da8f7",0.5,0.5,0.8,TW,TH,0.55); bg=cv2.GaussianBlur(bg,(0,0),9); fr=(bg*1.0).astype(np.uint8)
    cutpaste(fr,"4d5819bf",0.5,0.46,0.62,dx=330,dy=30,dim=1.06)
    gradH(fr,0,780,0.7,0.0)
    stext(fr,"25",anton(260),WHITE,200,250,glow=(0,0,0),sw=12)
    cv2.arrowedLine(fr,(330,250),(500,250),GOLD,16,cv2.LINE_AA,tipLength=0.45)
    stext(fr,"65",anton(300),GOLD,640,235,glow=(255,150,0),sw=12)
    stext(fr,"IN 4 YEARS?",anton(110),WHITE,360,490,glow=(0,0,0),sw=9)
    pill(fr,"PILIBHIT TIGER RESERVE",330,620,1.0,fg=(20,16,8),bg=GOLD,size=46)
    return vign(fr,0.3)
# ================= COVERS 1080x1920 (safe area: centre 1080x1440 for grid)
def cover_srilanka():
    fr=para("a4bcbe52",0.5,0.38,0.98,0.84,W,H,0,0,blur=10,dim=1.04)
    m=map_img(80.35,8.4,260,W,H,1.0,0.0); m=grade(m,1.1,1.2)
    # map as top band behind text
    gradv(fr,0,640,0.78,0.0); gradv(fr,1450,H,0.0,0.7)
    fr=grade(fr,1.1,1.15)
    stext(fr,"WHY NO",anton(170),WHITE,W/2,380,glow=(0,0,0),sw=10)
    stext(fr,"TIGERS IN",anton(170),WHITE,W/2,540,glow=(0,0,0),sw=10)
    stext(fr,"SRI LANKA?",anton(190),GOLD,W/2,720,glow=(255,150,0),sw=11)
    stext(fr,"India has them. Sri Lanka doesn't.",bar(48),CREAM,W/2,1560,glow=None,sw=4)
    return vign(fr,0.28)
def cover_panna():
    L=cv2.cvtColor(cv2.imread(PN+"s_%04d.jpg"%(int(34.5*30)+1)),cv2.COLOR_BGR2RGB); c_=L[470:1500,:]
    bgp=cv2.GaussianBlur(cv2.resize(L[200:1500,:],(1080,1920)),(0,0),28); fr=(bgp*0.55).astype(np.uint8)
    mk=np.ones((c_.shape[0],1,1),np.float32)
    for i in range(90): mk[i]=i/90; mk[-1-i]=min(mk[-1-i],i/90)
    y0=450; reg=fr[y0:y0+c_.shape[0]].astype(np.float32); fr[y0:y0+c_.shape[0]]=(reg*(1-mk)+c_.astype(np.float32)*mk).astype(np.uint8)
    fr=grade(fr,1.15,1.25)
    stext(fr,"TOURIST",anton(190),WHITE,W/2,360,glow=(0,0,0),sw=10)
    stext(fr,"vs",bcs(90),GOLD,W/2,500,glow=None,sw=6)
    stext(fr,"PHOTOGRAPHER",anton(130),GOLD,W/2,640,glow=(255,150,0),sw=10)
    pill(fr,"PANNA TIGER RESERVE",W/2,1500,1.0,fg=(20,16,8),bg=GOLD,size=44)
    return vign(fr,0.28)
def cover_pilibhit():
    fr=para("a4bcbe52",0.5,0.40,0.92,0.78,W,H,0,0,blur=10,dim=1.0)
    gradv(fr,0,760,0.78,0.0); gradv(fr,1400,H,0.0,0.75); fr=grade(fr,1.1,1.2)
    stext(fr,"25 → 65",anton(230),GOLD,W/2,380,glow=(255,150,0),sw=12)
    stext(fr,"HOW DID THIS FOREST",bcs(80),WHITE,W/2,590,glow=None,sw=6)
    stext(fr,"DOUBLE ITS TIGERS?",bcs(80),WHITE,W/2,680,glow=None,sw=6)
    pill(fr,"PILIBHIT TIGER RESERVE",W/2,1500,1.0,fg=(20,16,8),bg=GOLD,size=44)
    return vign(fr,0.28)
if __name__=="__main__":
    save(thumb_srilanka(),"YT_thumb_SriLanka.jpg"); save(thumb_panna(),"YT_thumb_Panna.jpg"); save(thumb_pilibhit(),"YT_thumb_Pilibhit.jpg")
    save(cover_srilanka(),"IG_cover_SriLanka.jpg"); save(cover_panna(),"IG_cover_Panna.jpg"); save(cover_pilibhit(),"IG_cover_Pilibhit.jpg")
    print("ok")
