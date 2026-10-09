import sys, json, math
sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pil')
import eng
from eng import *
import sc as S0
from sc import rmap, camk, vscan, RB, RPPD
HEREP="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pnv/"
TL={r[0]:(r[1],r[2]) for r in json.load(open(HEREP+"tl.json"))}
DUR=89.8; FPS=30
# ---------------- paste recorder (text/pill overlap check)
REC=None
_paste0=eng.paste
def _rec_paste(fr,sp,cx,cy,a=1.0,s=1.0,rot=0.0):
    if REC is not None and a>0.3:
        h,w=sp.shape[:2]; m=(sp[:,:,3]>40)
        if s!=1.0: m=cv2.resize(m.astype(np.uint8),(int(w*s),int(h*s)))>0
        hh,ww=m.shape; x=int(round(cx-ww/2)); y=int(round(cy-hh/2))
        x0=max(x,0); y0=max(y,0); x1=min(x+ww,W); y1=min(y+hh,H)
        if x1>x0 and y1>y0: REC[y0:y1,x0:x1]|=m[y0-y:y1-y,x0-x:x1-x]
    _paste0(fr,sp,cx,cy,a,s,rot)
eng.paste=_rec_paste; paste=_rec_paste
# ---------------- photos
PHD={}; PCUT={}
def ph(n):
    if n not in PHD: PHD[n]=cv2.cvtColor(cv2.imread(HEREP+f"ph/{n}.jpg"),cv2.COLOR_BGR2RGB)
    return PHD[n]
def pcut(n):
    if n not in PCUT:
        c=np.array(Image.open(HEREP+f"ph/c{n}.png")); a=c[:,:,3]
        a=cv2.GaussianBlur(cv2.erode(a,np.ones((3,3),np.uint8)),(0,0),1.2); c[:,:,3]=a; PCUT[n]=c
    return PCUT[n]
# subject bbox (x0,x1,y0,y1) normalised, from cutouts
SUB={16:(0.0,0.97,0.19,0.89),23:(0.16,0.50,0.47,0.79),24:(0.26,0.78,0.33,0.72),25:(0.18,0.62,0.40,0.70),26:(0.20,0.77,0.32,0.72),27:(0.44,0.92,0.41,0.66),
     28:(0.38,0.88,0.33,0.80),29:(0.41,0.92,0.55,0.75),30:(0.36,0.61,0.46,0.91),"17e":(0.05,0.95,0.25,0.85)}
LASTA=None
def vm(n,cx,cy,wf):
    im=ph(n); ih,iw=im.shape[:2]; cw=wf*iw; ch=cw*H/W
    if ch>ih: ch=ih; cw=ch*W/H
    s=W/cw; xc=min(max(cx*iw,cw/2),iw-cw/2); yc=min(max(cy*ih,ch/2),ih-ch/2)
    return np.array([[s,0,W/2-xc*s],[0,s,H/2-yc*s]],np.float32)
def _cover_bg(n,blur=28,dim=0.66,p=0.0):
    im=ph(n); ih,iw=im.shape[:2]; sc=max(W/iw,H/ih)*(1.06+0.03*p)
    M=np.array([[sc,0,W/2-iw/2*sc],[0,sc,H/2-ih/2*sc]],np.float32)
    bg=cv2.warpAffine(im,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    return (cv2.GaussianBlur(bg,(0,0),blur)*dim).astype(np.uint8)
def _feather(w,h,f=70):
    a=np.ones((h,w),np.float32); r=np.linspace(0,1,f)
    a[:f,:]*=r[:,None]; a[-f:,:]*=r[::-1][:,None]; a[:,:f]*=r[None,:]; a[:,-f:]*=r[::-1][None,:]; return a
def fit(n,p,hfrac=0.40,yfrac=0.5,push=0.08,dim=0.92,par=True,blur=10,wmax=0.9,xfrac=0.5,dx=0.0):
    """sharp photo (scaled so subject height~hfrac*H) centred at (xfrac,yfrac), over blurred cover bg"""
    global LASTA
    x0,x1,y0,y1=SUB[n]; im=ph(n); ih,iw=im.shape[:2]
    sw=(x1-x0)*iw; sh=(y1-y0)*ih; s=min(hfrac*H/sh, wmax*W/sw)*(1+push*p)
    cx=(x0+x1)/2; cy=(y0+y1)/2
    M=np.array([[s,0,xfrac*W-cx*iw*s],[0,s,yfrac*H-cy*ih*s]],np.float32)
    out=_cover_bg(n,p=p).astype(np.float32)
    mid=cv2.warpAffine(im,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0))
    fa=cv2.warpAffine(_feather(iw,ih,int(70/max(s,0.2))),M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=0)[:,:,None]
    if par and n in PCUTOK:
        mid=cv2.GaussianBlur(mid,(0,0),4)
        out=out*(1-fa)+mid.astype(np.float32)*dim*fa
        c=pcut(n); s2=s*1.07
        M2=np.array([[s2,0,xfrac*W-cx*iw*s2],[0,s2,yfrac*H-cy*ih*s2]],np.float32)
        fg=cv2.warpAffine(c,M2,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
        a=fg[:,:,3:4].astype(np.float32)/255; LASTA=fg[:,:,3]>110
        out=out*(1-a)+fg[:,:,:3].astype(np.float32)*dim*a
    else:
        out=out*(1-fa)+mid.astype(np.float32)*dim*fa
        m=np.zeros((H,W),bool); xa=int(xfrac*W-sw*s/2*0+0); 
        bx0=int(xfrac*W-(x1-x0)*iw*s/2); bx1=int(xfrac*W+(x1-x0)*iw*s/2); by0=int(yfrac*H-sh*s/2); by1=int(yfrac*H+sh*s/2)
        m[max(by0,0):max(by1,0),max(bx0,0):max(bx1,0)]=True; LASTA=m
    return np.clip(out,0,255).astype(np.uint8)
PCUTOK={16,23,28,29,30}
def coverfit(n,p,cx=0.2,push=0.08,dim=0.9):
    global LASTA
    im=ph(n); ih,iw=im.shape[:2]; s=H/ih*(1+push*p); xc=cx*iw
    M=np.array([[s,0,W/2-xc*s],[0,s,H/2-ih/2*s]],np.float32)
    LASTA=None
    return (cv2.warpAffine(im,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)*dim).astype(np.uint8)
def bands(fr,top=0.62,bot=0.62,ty=640,by=1300):
    gradv(fr,0,ty,top,0.0); gradv(fr,by,H,0.0,bot)
def count(t,t0,t1,v): return int(round(v*eo3(seg(t,t0,t1))))
def dots(fr,t,t0,n,keep,y,col=(255,200,70),dim_col=(120,120,120),fade_t=None,step=120,r=30):
    x0=W/2-(n-1)*step/2
    for i in range(n):
        ti=t0+i*0.22
        if t<ti: continue
        a=ease(seg(t,ti,ti+0.18)); c=col
        if fade_t is not None and i>=keep:
            f=ease(seg(t,fade_t+(i-keep)*0.25,fade_t+(i-keep)*0.25+0.5)); c=lerp_col(col,(90,90,95),f); a=a*(1-0.55*f)
        ov=fr.copy(); cv2.circle(ov,(int(x0+i*step),int(y)),r,c,-1,cv2.LINE_AA); cv2.circle(ov,(int(x0+i*step),int(y)),r,(255,255,255),3,cv2.LINE_AA)
        fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
def lerp_col(a,b,x): return tuple(int(lerp(u,v,x)) for u,v in zip(a,b))
# ---------------- map helpers
PANNA=(80.00,24.75); BAND=(81.03,23.72); KANHA=(80.62,22.30); PENCH=(79.30,21.72)
import json as _j
_rv=_j.load(open("/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pil/ne_10m_rivers_lake_centerlines.json"))
def _lines(name):
    out=[]
    for f in _rv['features']:
        if f['properties'].get('name')==name:
            g=f['geometry']; ls=g['coordinates'] if g['type']=='MultiLineString' else [g['coordinates']]
            out+= [[(p[0],p[1]) for p in l] for l in ls]
    return out
BETWA=_lines("Betwa"); YAMUNA=_lines("Yamuna")
KEN=[(80.40,23.75),(80.22,24.20),(80.06,24.60),(80.00,24.85),(80.12,25.20),(80.34,25.48),(80.50,25.80)]
DAM=(80.02,24.86)
BUND=(79.35,25.45)
def nearest_betwa(pt):
    best=None
    for l in BETWA:
        for q in l:
            d=(q[0]-pt[0])**2+(q[1]-pt[1])**2
            if best is None or d<best[0]: best=(d,q)
    return best[1]
BTW=nearest_betwa((79.3,25.0))
def mapview(lonc,latc,k,tilt,roll,t):
    w=int(W*1.16); h=int(H*1.16); img,P=rmap(lonc,latc,k,w,h,t)
    cx,cy=w/2,h/2; src=np.float32([[cx-W/2,cy-H/2],[cx+W/2,cy-H/2],[cx+W/2,cy+H/2],[cx-W/2,cy+H/2]]); sh=tilt*W*0.5
    dst=np.float32([[sh,0],[W-sh,0],[W,H],[0,H]]); Pm=cv2.getPerspectiveTransform(src,dst); Rm=np.vstack([cv2.getRotationMatrix2D((W/2,H/2),roll,1.0),[0,0,1]])
    Mt=(Rm@Pm).astype(np.float32)
    fr=cv2.warpPerspective(img,Mt,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    def proj(lo,la):
        x,y=P(lo,la); q=cv2.perspectiveTransform(np.float32([[[x,y]]]),Mt)[0,0]; return float(q[0]),float(q[1])
    return fr,proj
def polyline(fr,proj,pts,col,wd,a=1.0,upto=1.0,dash=0):
    pp=[proj(*p) for p in pts]; L=[0]
    for i in range(1,len(pp)): L.append(L[-1]+math.hypot(pp[i][0]-pp[i-1][0],pp[i][1]-pp[i-1][1]))
    tot=L[-1]*upto; ov=fr.copy()
    for i in range(1,len(pp)):
        if L[i-1]>=tot: break
        e=min(1.0,(tot-L[i-1])/max(1e-6,L[i]-L[i-1])); a_=pp[i-1]; b_=(a_[0]+(pp[i][0]-a_[0])*e,a_[1]+(pp[i][1]-a_[1])*e)
        if dash:
            n=int(max(2,math.hypot(b_[0]-a_[0],b_[1]-a_[1])/dash))
            for j in range(n):
                p0=(a_[0]+(b_[0]-a_[0])*j/n,a_[1]+(b_[1]-a_[1])*j/n); p1=(a_[0]+(b_[0]-a_[0])*(j+0.55)/n,a_[1]+(b_[1]-a_[1])*(j+0.55)/n)
                cv2.line(ov,(int(p0[0]),int(p0[1])),(int(p1[0]),int(p1[1])),col,wd,cv2.LINE_AA)
        else: cv2.line(ov,(int(a_[0]),int(a_[1])),(int(b_[0]),int(b_[1])),col,wd,cv2.LINE_AA)
    fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
def dotp(fr,x,y,r,col,ring_t=None):
    cv2.circle(fr,(int(x),int(y)),r,col,-1,cv2.LINE_AA); cv2.circle(fr,(int(x),int(y)),r,(255,255,255),3,cv2.LINE_AA)
def ellipse_pts(c,a,b,n=60,rot=0.0):
    out=[]
    for i in range(n+1):
        th=2*math.pi*i/n; x=a*math.cos(th); y=b*math.sin(th); out.append((c[0]+x*math.cos(rot)-y*math.sin(rot),c[1]+x*math.sin(rot)+y*math.cos(rot)))
    return out
# reserve schematic: ~1,598 sq km ellipse (28 km x 18 km semi-axes)
RA=0.277; RBb=0.162
def reserve_outline(fr,proj,a=1.0,col=(255,215,110),wd=5):
    polyline(fr,proj,ellipse_pts(PANNA,RA,RBb),col,wd,a,1.0,dash=22)
# ---------------- scenes
def tstart(l,lead=0.0): return TL[l][0]-lead
def S_open(t):
    # A+B : empty frame, lone silhouette sky
    p=seg(t,0,4.75); fr=fit("17e",p,hfrac=0.5,yfrac=0.5,push=0.05,dim=0.85,par=False,wmax=0.95)
    g=ease(seg(t,TL['B'][0]-0.05,TL['B'][0]+0.5))
    gray=fr.mean(2,keepdims=True); fr=(fr*(1-0.65*g)+gray*0.65*g).astype(np.uint8)
    gradv(fr,0,760,0.55,0.0); gradv(fr,1450,H,0.0,0.45)
    motes(fr,t,0.35)
    kt(fr,"2009",anton(280),WHITE,W/2,300,t,TL['A'][0],hold_end=4.6,sw=10,glow=(255,150,30))
    kt(fr,"NO TIGERS",anton(170),RED,W/2,600,t,TL['B'][0]+0.35,hold_end=4.6,sw=9,glow=(255,40,30))
    kt(fr,"LEFT.",anton(170),RED,W/2,780,t,TL['B'][0]+0.95,hold_end=4.6,sw=9,glow=(255,40,30))
    return fr
def S_c(t):
    a=TL['C'][0]-0.15; p=seg(t,a,TL['D'][0]-0.15); fr=fit(24,p,hfrac=0.30,yfrac=0.51,push=0.08,dim=0.95,par=False,wmax=0.9)
    bands(fr); motes(fr,t,0.4)
    kt(fr,"6 YEARS EARLIER",bcs(86),CREAM,W/2,340,t,TL['C'][0]+0.05,hold_end=TL['D'][0]-0.2,sw=6)
    v=count(t,TL['C'][0]+1.1,TL['C'][0]+2.4,40)
    if t>=TL['C'][0]+1.0:
        kt(fr,f"{v}+",anton(300),GOLD,W/2,1560,t,TL['C'][0]+1.0,hold_end=TL['D'][0]-0.2,sw=11,glow=(255,150,0),glitch=False)
        paste(fr,sprite("TIGERS IN PANNA",bcs(66),WHITE,sw=5),W/2,1735,ease(seg(t,TL['C'][0]+1.5,TL['C'][0]+1.9)))
    pill(fr,"REPORTED ESTIMATE",W/2,200,ease(seg(t,TL['C'][0]+2.0,TL['C'][0]+2.4)),size=34,fg=(230,230,230),bg=(14,24,30))
    return fr
def S_d(t):
    a=TL['D'][0]-0.15; p=seg(t,a,TL['G'][0]-0.2); fr=fit(30,p,hfrac=0.34,yfrac=0.51,push=0.08,dim=0.9,par=True,xfrac=0.5)
    g=ease(seg(t,a,a+1.5)); gray=fr.mean(2,keepdims=True); fr=(fr*(1-0.5*g)+gray*0.5*g).astype(np.uint8)
    ov=np.zeros_like(fr,np.float32); ov[:,:,0]=255*0.10*g; add(fr,ov,1.0)
    bands(fr,0.7,0.7,700,1250)
    kt(fr,"POACHING.",anton(180),RED,W/2,330,t,TL['D'][0]+0.1,hold_end=TL['G'][0]-0.25,sw=9,glow=(255,40,30))
    kt(fr,"NEGLECT.",anton(180),CREAM,W/2,1560,t,TL['D'][0]+1.2,hold_end=TL['G'][0]-0.25,sw=9,glow=(0,0,0))
    return fr
def S_map1(t):
    # G + I + J : translocation, T3 walks out, brought back
    g0=TL['G'][0]; i0=TL['I'][0]; j0=TL['J'][0]; j1=TL['J'][1]
    keys=[(g0-0.4,80.3,23.35,215,0.10,0.0),(g0+4.0,80.2,23.4,225,0.12,-1.0),(i0,80.1,23.3,225,0.12,0.8),(j1+0.6,80.1,23.3,235,0.10,-0.8)]
    lonc,latc,k,tilt,roll=camk(t,keys); fr,pr=mapview(lonc,latc,k,tilt,roll,t)
    # arrivals
    seg_t=[(g0+0.1,g0+2.0,BAND,"TIGRESS",(255,200,70)),(g0+2.0,g0+4.0,KANHA,"TIGRESS",(255,200,70)),(g0+4.1,g0+6.0,PENCH,"MALE",(80,235,240))]
    for (a,b,src,lab,col) in seg_t:
        if t<a: continue
        q=eo3(seg(t,a,b+0.2)); sx,sy=pr(*src); px,py=pr(*PANNA)
        polyline(fr,pr,[src,PANNA],col,5,0.9,q,dash=26)
        dotp(fr,sx,sy,15,col)
        dx,dy=lerp(sx,px,q),lerp(sy,py,q); dotp(fr,dx,dy,13,(255,255,255))
        nm={BAND:"BANDHAVGARH",KANHA:"KANHA",PENCH:"PENCH"}[src]
        pill(fr,nm,sx+(150 if src!=PENCH else 130),sy,ease(seg(t,a,a+0.35)),size=44)
    px,py=pr(*PANNA); dotp(fr,px,py,20,(255,240,170))
    for jj in range(3):
        q=((t-g0)*0.7+jj/3)%1; ring(fr,px,py,18+q*110,(255,220,120),(1-q)*0.7,5)
    pill(fr,"PANNA",px+120,py-4,ease(seg(t,g0-0.2,g0+0.2)),size=52)
    kt(fr,"2009",anton(150),GOLD,W/2,300,t,g0+0.05,hold_end=i0-0.1,sw=8,glow=(255,150,0))
    kt(fr,"TIGERS BROUGHT IN",bcs(76),WHITE,W/2,450,t,g0+0.5,hold_end=i0-0.1,sw=6,glow=(0,0,0))
    # T3 walks out toward Pench, then comes back
    if t>=i0-0.1:
        a_=ease(seg(t,i0-0.1,i0+0.3)); T3=(PANNA[0]-0.34,PANNA[1]-1.55)   # schematic direction toward Pench
        out_q=eo3(seg(t,i0+0.2,i0+2.4)); back_q=ease(seg(t,j0+0.3,j1-0.1)); q=out_q*(1-back_q)
        polyline(fr,pr,[PANNA,T3],(80,235,240),5,0.8*a_,out_q,dash=24)
        tx,ty=lerp(px,pr(*T3)[0],q),lerp(py,pr(*T3)[1],q); dotp(fr,tx,ty,17,(80,235,240))
        kt(fr,"T3 WALKS OUT",anton(110),(80,235,240),W/2,300,t,i0+0.05,hold_end=j0-0.15,sw=7,glow=(0,160,200)) if t<j0-0.1 else None
        kt(fr,"TRACKED. BROUGHT BACK.",anton(88),WHITE,W/2,300,t,j0+0.05,hold_end=j1+0.3,sw=7,glow=(0,0,0))
    pill(fr,"SCHEMATIC MAP. ROUTES NOT TO SCALE.",W/2,1640,0.9,size=32,fg=(225,225,225),bg=(14,24,30))
    vscan(fr,t); hud_corners(fr,50,200,W-50,H-320,CYAN,0.6)
    return fr
def S_cubs(t):
    l0=TL['L'][0]; m0=TL['M'][0]; n0=TL['N'][0]; n1=TL['N'][1]
    if t<n0-0.2: n=28; p=seg(t,l0-0.2,n0-0.2)
    else: n=26; p=seg(t,n0-0.2,n1+0.4)
    fr=fit(n,p,hfrac=0.30 if n==28 else 0.34,yfrac=0.49,push=0.08,dim=0.95,par=(n==28))
    bands(fr,0.66,0.7,620,1200); motes(fr,t,0.35)
    if t<n0-0.15:
        kt(fr,"APRIL 2010",bcs(80),CREAM,W/2,260,t,l0+0.05,hold_end=n0-0.25,sw=6)
        kt(fr,"T1",anton(190),GOLD,W/2,420,t,l0+0.2,hold_end=n0-0.25,sw=9,glow=(255,150,0))
        dots(fr,t,l0+1.0,4,2,1580,fade_t=m0-0.1)
        if t>=l0+1.2: paste(fr,sprite("4 CUBS",bcs(70),WHITE,sw=5),W/2-0,1720,ease(seg(t,l0+1.2,l0+1.5))*(1 if t<m0-0.1 else 0))
        if t>=m0-0.05: paste(fr,sprite("2 SURVIVED",bcs(70),(255,200,70),sw=5),W/2,1720,ease(seg(t,m0-0.05,m0+0.3)))
    else:
        kt(fr,"T2",anton(190),(80,235,240),W/2,380,t,n0+0.0,hold_end=n1+0.5,sw=9,glow=(0,160,200))
        kt(fr,"4 CUBS",bcs(80),CREAM,W/2,520,t,n0+0.15,hold_end=n1+0.5,sw=6)
        dots(fr,t,n0+0.8,4,4,1580,col=(80,235,240))
        paste(fr,sprite("ALL 4 SURVIVED",bcs(70),(80,235,240),sw=5),W/2,1720,ease(seg(t,n0+1.7,n0+2.1)))
    pill(fr,"ILLUSTRATIVE PHOTOS. NOT THE TIGERS NAMED.",W/2,1830,0.85,size=28,fg=(225,225,225),bg=(14,24,30))
    return fr
def S_2021(t):
    o0=TL['O'][0]; p0=TL['P'][0]; p1=TL['P'][1]
    p=seg(t,o0-0.2,p1+0.3); fr=fit(23,p,hfrac=0.30,yfrac=0.50,push=0.08,dim=0.95,wmax=0.95)
    bands(fr,0.68,0.72,680,1230); motes(fr,t,0.35)
    kt(fr,"2021",anton(190),WHITE,W/2,330,t,o0+0.0,hold_end=p1+0.3,sw=9,glow=(255,150,0))
    if t>=p0:
        v=count(t,p0+0.2,p0+1.6,59)
        kt(fr,str(v),anton(330),GOLD,W/2,1540,t,p0,hold_end=p0+2.9,sw=12,glow=(255,150,0),glitch=False)
        paste(fr,sprite("TIGERS",bcs(76),WHITE,sw=5),W/2,1730,ease(seg(t,p0+1.4,p0+1.8))*(1 if t<p0+2.9 else 0))
    if t>=p0+2.9:
        a=ease(seg(t,p0+2.9,p0+3.3)); paste(fr,sprite("18 FEMALES",bcs(84),CREAM,sw=6),W/2,1480,a)
        v=count(t,p0+3.8,p0+4.9,120); paste(fr,sprite(f"{v} CUBS",anton(230),GOLD,sw=10,glow=(255,150,0)),W/2,1640,ease(seg(t,p0+3.5,p0+3.9)))
    return fr
def S_leave(t):
    r0=TL['R'][0]; r1=TL['R'][1]
    keys=[(r0-0.3,80.0,24.75,1250,0.10,0.0),(r1,80.0,24.78,900,0.12,-1.0)]
    lonc,latc,k,tilt,roll=camk(t,keys); fr,pr=mapview(lonc,latc,k,tilt,roll,t)
    reserve_outline(fr,pr,0.95)
    px,py=pr(*PANNA); pill(fr,"PANNA TIGER RESERVE",px,py+int(0.162*k*0.9)+90,ease(seg(t,r0,r0+0.4)),size=44)
    rng=np.random.default_rng(5)
    angs=[0.3,1.1,1.9,2.7,3.6,4.3,5.1,5.8]
    for i,an in enumerate(angs):
        t0=r0+0.6+i*0.28
        if t<t0: continue
        q=eo3(seg(t,t0,t0+2.4)); r_=lerp(0.05,1.0,q)
        x0=px+math.cos(an)*0.02*k; y0=py+math.sin(an)*0.02*k
        x1=px+math.cos(an)*(RA*k*1.0+q*0.9*k*0.55); y1=py+math.sin(an)*(RBb*k*1.0+q*0.9*k*0.55)
        cv2.line(fr,(int(x0),int(y0)),(int(x1),int(y1)),(80,235,240),4,cv2.LINE_AA); dotp(fr,x1,y1,12,(80,235,240))
    kt(fr,"TIGERS ARE",bcs(84),CREAM,W/2,300,t,r0+0.05,hold_end=r1+0.1,sw=6)
    kt(fr,"LEAVING.",anton(190),(80,235,240),W/2,460,t,r0+0.55,hold_end=r1+0.1,sw=9,glow=(0,160,200))
    if t>=r0+3.4:
        a=ease(seg(t,r0+3.4,r0+3.8)); paste(fr,sprite("35+ HAVE DISPERSED",anton(96),WHITE,sw=7,glow=(0,160,200)),W/2,1560,a)
        paste(fr,sprite("RESERVE REVIEW, 2021",bar(36),(220,230,235),sw=3,shadow=False),W/2,1660,a)
    pill(fr,"SCHEMATIC",W/2,1780,0.8,size=30,fg=(225,225,225),bg=(14,24,30))
    vscan(fr,t); hud_corners(fr,50,200,W-50,H-300,CYAN,0.6); return fr
def S_99(t):
    s0=TL['S'][0]; s1=TL['S'][1]
    p=seg(t,s0-0.2,s1+0.4); fr=fit(25,p,hfrac=0.30,yfrac=0.50,push=0.08,dim=0.95,par=False,wmax=0.88)
    bands(fr,0.7,0.74,660,1200); motes(fr,t,0.3)
    kt(fr,"ONE YOUNG TIGRESS",bcs(80),CREAM,W/2,300,t,s0+0.05,hold_end=s1+0.4,sw=6)
    kt(fr,"SEARCHING FOR LAND",bcs(66),(215,225,230),W/2,400,t,s0+0.5,hold_end=s1+0.4,sw=5)
    if t>=s0+2.6:
        v=count(t,s0+2.7,s0+3.6,99)
        kt(fr,f"{v} KM",anton(320),GOLD,W/2,1560,t,s0+2.6,hold_end=s1+0.4,sw=12,glow=(255,150,0),glitch=False)
        paste(fr,sprite("PANNA TIGRESS P213-22, 2021",bar(36),(225,230,235),sw=3,shadow=False),W/2,1730,ease(seg(t,s0+3.4,s0+3.8)))
    return fr
def S_enough(t):
    a0=TL['T'][0]; a1=TL['T'][1]
    p=seg(t,a0-0.2,a1+0.3)
    fr=fit(16,p,hfrac=0.34,yfrac=0.51,push=0.08,dim=0.95) if t<a0+3.3 else coverfit(22,p,0.24,0.06,0.95)
    bands(fr,0.66,0.7,640,1250); motes(fr,t,0.3)
    kt(fr,"A BIG WIN.",anton(150),GOLD,W/2,330,t,a0+0.05,hold_end=a0+3.3,sw=9,glow=(255,150,0))
    kt(fr,"BUT IS THERE",bcs(84),CREAM,W/2,1500,t,a0+3.55,hold_end=a1+0.3,sw=6)
    kt(fr,"ENOUGH FOREST?",anton(150),RED,W/2,1660,t,a0+4.05,hold_end=a1+0.3,sw=9,glow=(255,40,30))
    return fr
def S_kb(t):
    u0=TL['U'][0]; v0=TL['V'][0]; v1=TL['V'][1]
    keys=[(u0-0.3,79.95,25.0,330,0.10,0.0),(v0,79.75,25.1,450,0.12,0.8),(v1,79.8,25.0,470,0.12,-0.6)]
    lonc,latc,k,tilt,roll=camk(t,keys); fr,pr=mapview(lonc,latc,k,tilt,roll,t)
    polyline(fr,pr,KEN,(110,225,255),9,1.0,eo3(seg(t,u0+0.2,u0+1.4)))
    for l in BETWA: polyline(fr,pr,l,(120,235,150),7,1.0,eo3(seg(t,u0+0.9,u0+2.2)))
    kx,ky=pr(*KEN[2]); bx,by=pr(*BTW)
    pill(fr,"KEN RIVER",kx+30,ky+205,ease(seg(t,u0+1.0,u0+1.4)),size=46,bg=(110,225,255))
    bxx,byy=pr(*BETWA[0][len(BETWA[0])//2]); pill(fr,"BETWA RIVER",min(max(bxx+120,230),W-230),byy-190,ease(seg(t,u0+2.0,u0+2.4)),size=46,bg=(120,235,150))
    reserve_outline(fr,pr,0.8,wd=4)
    if t>=v0+0.2:
        q=eo3(seg(t,v0+0.3,v0+2.8)); dx,dy=pr(*DAM)
        polyline(fr,pr,[DAM,BTW],(255,200,70),8,1.0,q,dash=24)
        ex,ey=lerp(dx,pr(*BTW)[0],q),lerp(dy,pr(*BTW)[1],q); dotp(fr,ex,ey,14,(255,230,150))
        dotp(fr,dx,dy,14,(255,200,70))
        mx,my=pr(*BUND); pill(fr,"BUNDELKHAND",min(mx+180,W-190),my+20,ease(seg(t,v0+1.4,v0+1.8)),size=48,fg=(255,255,255),bg=(20,90,140))
    kt(fr,"KEN-BETWA",anton(150),WHITE,W/2,290,t,u0+0.05,hold_end=v0-0.1,sw=8,glow=(0,160,200))
    kt(fr,"RIVER LINK",anton(150),(110,225,255),W/2,445,t,u0+0.45,hold_end=v0-0.1,sw=8,glow=(0,160,200))
    kt(fr,"WATER FOR A DRY REGION",anton(92),WHITE,W/2,320,t,v0+0.1,hold_end=v1+0.5,sw=7,glow=(0,160,200))
    pill(fr,"SCHEMATIC. NOT TO SCALE.",W/2,1790,0.85,size=30,fg=(225,225,225),bg=(14,24,30))
    vscan(fr,t); hud_corners(fr,50,200,W-50,H-250,CYAN,0.6); return fr
def S_cost(t):
    x0=TL['X'][0]; x1=TL['X'][1]
    keys=[(x0-0.3,79.95,24.85,520,0.10,0.0),(x0+3.0,80.0,24.85,1500,0.12,-0.8),(x1,80.02,24.86,2300,0.12,0.5)]
    lonc,latc,k,tilt,roll=camk(t,keys); fr,pr=mapview(lonc,latc,k,tilt,roll,t)
    reserve_outline(fr,pr,0.95,wd=6)
    polyline(fr,pr,KEN,(110,225,255),9,1.0,1.0)
    px,py=pr(*PANNA); dx,dy=pr(*DAM)
    # submergence blob (schematic, ~57 sq km = 3.6% of reserve ellipse), grows along the river
    q=eo3(seg(t,x0+5.3,x0+7.0))
    if q>0:
        area_frac=57/1598.0; ea=RA*0.55; eb=2.4*(area_frac*RA*RBb)/ea
        pts=ellipse_pts((DAM[0]+0.01,DAM[1]-0.12),ea*q,eb*q*1.0,40,rot=math.radians(80))
        P_=np.array([pr(*p) for p in pts],np.int32); ov=fr.copy(); cv2.fillPoly(ov,[P_],(80,170,255)); fr[:]=(fr*(1-0.55)+ov*0.55).astype(np.uint8)
        cv2.polylines(fr,[P_],True,(190,230,255),4,cv2.LINE_AA)
    dotp(fr,dx,dy,14,(255,200,70))
    pill(fr,"DAM SITE (APPROX.)",dx-190,dy-60,ease(seg(t,x0+3.4,x0+3.8)),size=40,bg=(255,200,70))
    kt(fr,"ENVIRONMENTAL",anton(120),WHITE,W/2,290,t,x0+0.05,hold_end=x0+3.0,sw=8,glow=(0,160,200))
    kt(fr,"COST.",anton(190),RED,W/2,450,t,x0+0.5,hold_end=x0+3.0,sw=9,glow=(255,40,30))
    kt(fr,"ONE STUDY'S ESTIMATE",bcs(70),CREAM,W/2,300,t,x0+3.75,hold_end=x1+0.3,sw=6)
    if t>=x0+5.7:
        v=count(t,x0+5.8,x0+6.9,57)
        kt(fr,f"~{v} SQ KM",anton(250),(150,215,255),W/2,1500,t,x0+5.7,hold_end=x1+0.3,sw=11,glow=(0,160,255),glitch=False)
        paste(fr,sprite("OF THE RESERVE COULD BE SUBMERGED",bcs(58),WHITE,sw=5),W/2,1655,ease(seg(t,x0+6.5,x0+6.9)))
        pill(fr,"ESTIMATES VARY BY STUDY",W/2,1760,ease(seg(t,x0+7.2,x0+7.6)),size=34,fg=(225,225,225),bg=(14,24,30))
    vscan(fr,t); hud_corners(fr,50,200,W-50,H-250,CYAN,0.6); return fr
def S_home(t):
    h0=TL['AB'][0]; h1=TL['AB'][1]
    p=seg(t,h0-0.2,h1+0.4); fr=fit(29,p,hfrac=0.28,yfrac=0.50,push=0.08,dim=0.95,wmax=0.95)
    bands(fr,0.7,0.72,680,1250); motes(fr,t,0.3)
    kt(fr,"CAN WE SAVE",bcs(86),CREAM,W/2,330,t,h0+0.1,hold_end=h1+0.2,sw=6)
    kt(fr,"THEIR HOME TOO?",anton(140),GOLD,W/2,1560,t,h0+0.7,hold_end=h1+0.2,sw=9,glow=(255,150,0))
    return fr
def S_end(t):
    a0=TL['AC'][0]; a1=TL['AC'][1]
    p=seg(t,a0-0.2,DUR); fr=fit(27,p,hfrac=0.24,yfrac=0.53,push=0.06,dim=0.9,par=False,wmax=0.95)
    bands(fr,0.72,0.8,680,1150); motes(fr,t,0.3)
    kt(fr,"A WAY FOR",bcs(86),CREAM,W/2,300,t,a0+0.1,hold_end=88.0,sw=6)
    kt(fr,"BOTH?",anton(210),GOLD,W/2,470,t,a0+0.6,hold_end=88.0,sw=9,glow=(255,150,0))
    # end card
    a=ease(seg(t,88.0,88.4))
    if a>0:
        paste(fr,sprite("FULL PANNA STORY",anton(120),WHITE,sw=8,glow=(255,150,0)),W/2,1450,a)
        paste(fr,sprite("ON MY CHANNEL, LINK BELOW",bcs(64),CREAM,sw=5),W/2,1570,a)
        paste(fr,sprite("THE NATURAL ANGLE",anton(84),GOLD,sw=7,glow=(255,150,0)),W/2,1700,a)
        paste(fr,sprite("Photos: Hitesh Chawla. Illustrative, not the tigers named.",bar(34),CREAM,sw=3),W/2,1800,a)
    fade(fr,ease(seg(t,89.3,DUR)))
    return fr
SC=[(0,TL['C'][0]-0.15,S_open),(TL['C'][0]-0.15,TL['D'][0]-0.15,S_c),(TL['D'][0]-0.15,TL['G'][0]-0.4,S_d),
    (TL['G'][0]-0.4,TL['L'][0]-0.2,S_map1),(TL['L'][0]-0.2,TL['O'][0]-0.2,S_cubs),(TL['O'][0]-0.2,TL['R'][0]-0.3,S_2021),
    (TL['R'][0]-0.3,TL['S'][0]-0.2,S_leave),(TL['S'][0]-0.2,TL['T'][0]-0.2,S_99),(TL['T'][0]-0.2,TL['U'][0]-0.3,S_enough),
    (TL['U'][0]-0.3,TL['X'][0]-0.3,S_kb),(TL['X'][0]-0.3,TL['AB'][0]-0.2,S_cost),(TL['AB'][0]-0.2,TL['AC'][0]-0.2,S_home),(TL['AC'][0]-0.2,DUR+1,S_end)]
TR=[s[0] for s in SC[1:]]
HITS=[(TL['A'][0]+0.0,1.0),(TL['B'][0]+0.35,0.9),(TL['C'][0]+1.0,0.6),(TL['D'][0]+0.1,0.7),(TL['G'][0]+0.05,0.5),(TL['L'][0]+0.2,0.5),(TL['O'][0],0.7),
      (TL['P'][0]+0.2,0.6),(TL['S'][0]+2.6,0.6),(TL['T'][0]+0.05,0.6),(TL['T'][0]+4.05,0.7),(TL['U'][0]+0.05,0.7),(TL['X'][0]+0.5,0.8),(TL['X'][0]+5.7,0.7),(TL['AC'][0]+0.6,0.7),(88.0,0.4)]
def frame(t):
    for i,(a,b,fn) in enumerate(SC):
        if a<=t<b: break
    fr=fn(t)
    if i>0 and t-a<0.28:   # dissolve from previous scene
        pa,pb,pf=SC[i-1]; prev=pf(min(t,pb-0.001)); k=ease((t-a)/0.28); fr=(prev.astype(np.float32)*(1-k)+fr.astype(np.float32)*k).astype(np.uint8)
    fr=punch(fr,t,HITS); return look(fr,t,HITS)
if __name__=="__main__":
    ts=[float(x) for x in sys.argv[1:]]
    for t in ts: cv2.imwrite(HEREP+f"f_{t:05.1f}.jpg",cv2.cvtColor(frame(t),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,88])
