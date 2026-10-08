import sys; sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/vid/v2')
from eng import *
PN="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pn/src/"
def vign(fr,s=0.3):
    h,w=fr.shape[:2]; yy,xx=np.mgrid[0:h,0:w]; d=np.sqrt(((xx-w/2)/(w/2))**2+((yy-h/2)/(h/2))**2); v=(1-s*np.clip(d-0.5,0,1)**1.3)[:,:,None]
    g=np.random.default_rng(3).normal(0,2.2,(h,w,1)); return np.clip(fr*v+g,0,255).astype(np.uint8)
def grade(fr,c=1.1,sat=1.15):
    f=fr.astype(np.float32); f=(f-128)*c+128+4; g=f.mean(2,keepdims=True); f=g+(f-g)*sat; return np.clip(f,0,255).astype(np.uint8)
def save(fr,name): cv2.imwrite(name,cv2.cvtColor(fr,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,95])
class Canvas:
    def __init__(s,fr): s.fr=fr; s.tl=np.zeros(fr.shape[:2],np.uint8); s.subj=np.zeros(fr.shape[:2],np.uint8); s.rects=[]
    def T(s,text,font,fill,cx,cy,glow=None,sw=9):
        sp=sprite(text,font,fill,sw=sw,glow=glow); paste(s.fr,sp,cx,cy,1.0); s._m(sp,cx,cy)
    def P(s,text,cx,cy,**k):
        # pill: draw then measure by diff
        before=s.fr.copy(); pill(s.fr,text,cx,cy,1.0,**k); d=(np.abs(s.fr.astype(np.int16)-before.astype(np.int16)).sum(2)>10).astype(np.uint8); s.tl|=d
    def _m(s,sp,cx,cy):
        h,w=sp.shape[:2]; x=int(round(cx-w/2)); y=int(round(cy-h/2)); x0=max(x,0); y0=max(y,0); x1=min(x+w,s.fr.shape[1]); y1=min(y+h,s.fr.shape[0])
        if x1>x0 and y1>y0: s.tl[y0:y1,x0:x1]|=(sp[y0-y:y1-y,x0-x:x1-x,3]>25).astype(np.uint8)
    def subject(s,k,ybot,hs,cx=None,cut=None):
        c=cut if cut is not None else cutout(k); a=c[:,:,3]; ys,xs=np.where(a>40); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
        sub=c[y0:y1+1,x0:x1+1]; sc=hs/sub.shape[0]; sub=cv2.resize(sub,(int(sub.shape[1]*sc),hs),interpolation=cv2.INTER_AREA)
        cx=s.fr.shape[1]//2 if cx is None else cx; X=int(cx-sub.shape[1]/2); Y=int(ybot-hs)
        # soft dark halo behind
        al=sub[:,:,3].astype(np.float32)/255; halo=np.zeros(s.fr.shape[:2],np.float32); halo[Y:Y+hs,X:X+sub.shape[1]]=al
        halo=cv2.GaussianBlur(halo,(0,0),38)[:,:,None]; s.fr[:]=(s.fr*(1-halo*0.45)).astype(np.uint8)
        reg=s.fr[Y:Y+hs,X:X+sub.shape[1]].astype(np.float32); s.fr[Y:Y+hs,X:X+sub.shape[1]]=(reg*(1-al[:,:,None])+sub[:,:,:3].astype(np.float32)*al[:,:,None]*1.04).clip(0,255).astype(np.uint8)
        s.subj[Y:Y+hs,X:X+sub.shape[1]]|=(al>0.15).astype(np.uint8); return (X,Y,sub.shape[1],hs)
    def rect(s,x0,y0,x1,y1): s.rects.append((x0,y0,x1,y1)); s.subj[y0:y1,x0:x1]=1
    def check(s,name):
        sd=cv2.dilate(s.subj,np.ones((9,9),np.uint8)); ov=int(((s.tl>0)&(sd>0)).sum()); print(name,"text/subject overlap px:",ov); return ov
def blurbg(k,dim=0.5,sig=22,cx=0.5,cy=0.5,wf=0.9):
    return (cv2.GaussianBlur(pwin(k,cx,cy,wf,W,H,1.0),(0,0),sig)*dim).astype(np.uint8)
def tig_cover(subj_key,bg_key,variant,headline,sub=None,pillt=None,big=None,name="x",bgmap=False,yb=None):
    if bgmap: fr=grade(map_img(80.45,8.3,200,W,H,1.0,0.0),1.1,1.2)
    else: fr=blurbg(bg_key,0.6)
    gradv(fr,0,760,0.55,0.0); gradv(fr,1450,H,0.0,0.5)
    cv=Canvas(fr)
    if variant=="ig":
        ytop=640; ybot=1660
    else:
        ytop=600; ybot=1620
    if yb: ybot=yb
    X,Y,w,h=cv.subject(subj_key,ybot,ybot-ytop)
    return cv
def finish(cv,name):
    cv.check(name); save(vign(grade(cv.fr,1.06,1.1),0.28),name)
# ---------- Sri Lanka
def sri(variant):
    cv=tig_cover("4d5819bf",None,variant,None,bgmap=True)
    if variant=="ig":
        cv.T("WHY NO TIGERS",anton(128),WHITE,W/2,320,glow=(0,0,0)); cv.T("IN SRI LANKA?",anton(150),GOLD,W/2,460,glow=(255,150,0)); cv.T("India has them. Sri Lanka doesn't.",bar(44),CREAM,W/2,570,sw=4)
    else:
        cv.T("WHY NO",anton(160),WHITE,W/2,170,glow=(0,0,0)); cv.T("TIGERS IN",anton(160),WHITE,W/2,325,glow=(0,0,0)); cv.T("SRI LANKA?",anton(180),GOLD,W/2,490,glow=(255,150,0))
    finish(cv,f"{variant.upper()}_SriLanka_v2.jpg")
def pili(variant):
    cv=tig_cover("a4bcbe52","c31da8f7",variant,None,yb=(1540 if variant=="ig" else None))
    if variant=="ig":
        cv.T("25 → 65",anton(210),GOLD,W/2,340,glow=(255,150,0),sw=11); cv.T("HOW DID THIS FOREST",bcs(72),WHITE,W/2,505,sw=6); cv.T("DOUBLE ITS TIGERS?",bcs(72),WHITE,W/2,585,sw=6)
        cv.P("PILIBHIT TIGER RESERVE",W/2,1625,fg=(20,16,8),bg=GOLD,size=40)
    else:
        cv.T("25 → 65",anton(240),GOLD,W/2,230,glow=(255,150,0),sw=12); cv.T("IN 4 YEARS?",anton(120),WHITE,W/2,395,glow=(0,0,0),sw=9); cv.P("PILIBHIT TIGER RESERVE",W/2,505,fg=(20,16,8),bg=GOLD,size=44)
    finish(cv,f"{variant.upper()}_Pilibhit_v2.jpg")
def panna(variant):
    A=cv2.cvtColor(cv2.imread(PN+"s_%04d.jpg"%(int(22.0*30)+1)),cv2.COLOR_BGR2RGB)[900:1400]; B=cv2.cvtColor(cv2.imread(PN+"s_%04d.jpg"%(int(34.5*30)+1)),cv2.COLOR_BGR2RGB)[600:1100]
    fr=np.zeros((H,W,3),np.uint8); fr[:]=(12,14,12); fr=(cv2.GaussianBlur(cv2.resize(B,(W,H)),(0,0),40)*0.35).astype(np.uint8)
    cv=Canvas(fr)
    if variant=="ig": ya,yb=560,1080; ty=(330,480); 
    else: ya,yb=520,1080; ty=(190,350)
    ph=500 if variant=="ig" else 540
    A2=cv2.resize(A,(W,ph)); B2=cv2.resize(B,(W,ph))
    if variant!="ig": ya=520; yb=520+ph+30
    cv.fr[ya:ya+ph]=grade(A2,1.1,1.2); cv.fr[yb:yb+ph]=grade(B2,1.1,1.2)
    cv.rect(0,ya,W,ya+ph); cv.rect(0,yb,W,yb+ph)
    for y in (ya,ya+ph,yb,yb+ph): cv2.line(cv.fr,(0,y),(W,y),GOLD,8)
    cv.T("TOURIST",anton(150 if variant=="ig" else 190),WHITE,W/2,ty[0],glow=(0,0,0)); cv.T("vs PHOTOGRAPHER",anton(104 if variant=="ig" else 120),GOLD,W/2,ty[1],glow=(255,150,0))
    if variant=="ig": cv.P("PANNA TIGER RESERVE",W/2,1625,fg=(20,16,8),bg=GOLD,size=40)
    else: cv.P("PANNA TIGER RESERVE",W/2,yb+ph+60,fg=(20,16,8),bg=GOLD,size=44) if False else None
    finish(cv,f"{variant.upper()}_Panna_v2.jpg")
if __name__=="__main__":
    for v in ("ig","yt"): sri(v); pili(v); panna(v)
