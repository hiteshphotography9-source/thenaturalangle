import sys; sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pil')
from eng import *
import pickle
R=pickle.load(open(HERE+"region.pkl","rb")); RELIEF=R["relief"]; BORD=R["lines"]; RB=R["box"]
RPPD=240.0  # relief px per degree
_hsv=cv2.cvtColor(RELIEF,cv2.COLOR_RGB2HSV).astype(np.float32)
_sat=_hsv[:,:,1]/255; _lum=cv2.cvtColor(RELIEF,cv2.COLOR_RGB2GRAY).astype(np.float32)/255
_mount=np.clip(1-(_sat-0.06)/0.22,0,1); _mount=cv2.GaussianBlur(_mount,(0,0),3)
_det=_lum-cv2.GaussianBlur(_lum,(0,0),10)
STYLE=None
def style():
    global STYLE
    if STYLE is None:
        m=cv2.GaussianBlur(_mount,(0,0),40)[:,:,None]
        plains=np.array((10,40,34),np.float32); mount=np.array((46,70,86),np.float32)
        base=plains*(1-m)+mount*m
        lb=cv2.GaussianBlur(_lum,(0,0),14); band=(np.abs(np.sin((lb+m[:,:,0]*0.6)*55))<0.09).astype(np.float32)
        band=cv2.GaussianBlur(band,(0,0),1.2)[:,:,None]
        out=base+band*np.array((40,90,80),np.float32)*(0.5+0.8*m)
        STYLE=np.clip(out,0,255).astype(np.uint8)
    return STYLE
PIL_LL=(79.80,28.62)
def rmap(lonc,latc,k,w,h,t):
    s=k/RPPD; ox=(lonc-RB[0])*RPPD; oy=(RB[3]-latc)*RPPD
    M=np.array([[s,0,w/2-ox*s],[0,s,h/2-oy*s]],np.float32)
    img=cv2.warpAffine(style(),M,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT).astype(np.float32)
    # sparkle grain scaled
    img*= (1+0.02*scrolled(N3,w,h,1.0,0,0)[:,:,None])
    img=np.clip(img,0,255).astype(np.uint8)
    def P(lo,la): return ((lo-lonc)*k+w/2,(latc-la)*k+h/2)
    # border line gold
    for l in BORD:
        pts=np.array([P(a,b) for a,b in l],np.int32)
        if len(pts)>1: cv2.polylines(img,[pts],False,(255,210,90),max(2,int(k/90)),cv2.LINE_AA)
    return img,P
def drawchart(fr,rect,xr,upto,labels_t=None):
    x0,y0,x1,y1=rect; ymax=70
    def X(yr): return x0+(yr-xr[0])/(xr[1]-xr[0])*(x1-x0)
    def Y(v): return y1-(v/ymax)*(y1-y0)
    ov=fr.copy(); cv2.rectangle(ov,(x0-40,y0-50),(x1+40,y1+90),(8,16,22),-1); fr[:]=(fr*0.25+ov*0.75).astype(np.uint8)
    for v in (0,20,40,60): cv2.line(fr,(x0,int(Y(v))),(x1,int(Y(v))),(60,80,90),2); paste(fr,sprite(str(v),bcs(46),(170,200,210),sw=0,shadow=False),x0-40,Y(v),1.0)
    for yr in range(int(math.ceil(xr[0])),int(xr[1])+1,1 if False else 2):
        paste(fr,sprite(str(yr),bcs(46),(190,210,220),sw=0,shadow=False),X(yr),y1+40,1.0)
    return X,Y
DATA=[(2010,42),(2013,23),(2014,25),(2018,65)]
def chartline(fr,X,Y,upto):
    pts=[(X(a),Y(b)) for a,b in DATA]
    for i in range(3):
        ya,yb=DATA[i][0],DATA[i+1][0]
        if upto<=ya: break
        f=min(1.0,(upto-ya)/(yb-ya)); a=pts[i]; b=pts[i+1]; e=(a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f)
        col=(255,95,80) if i==0 else ((190,190,190) if i==1 else (255,200,70))
        if i<2:
            n=int(max(2,math.hypot(e[0]-a[0],e[1]-a[1])/26))
            for j in range(n):
                p0=(a[0]+(e[0]-a[0])*j/n,a[1]+(e[1]-a[1])*j/n); p1=(a[0]+(e[0]-a[0])*(j+0.55)/n,a[1]+(e[1]-a[1])*(j+0.55)/n); cv2.line(fr,(int(p0[0]),int(p0[1])),(int(p1[0]),int(p1[1])),col,8,cv2.LINE_AA)
        else: cv2.line(fr,(int(a[0]),int(a[1])),(int(e[0]),int(e[1])),col,12,cv2.LINE_AA)
    for (yr,v),(px,py) in zip(DATA,pts):
        if upto>=yr: cv2.circle(fr,(int(px),int(py)),15,(255,255,255),-1,cv2.LINE_AA)
    return pts
# --------------- scenes
def S1(t):
    p=seg(t,0,1.6); fr=para("a4bcbe52",0.5,0.36,lerp(0.98,0.9,p),lerp(0.94,0.72,eo3(p)),W,H,0,0,blur=10,dim=1.04)
    gradv(fr,0,700,0.55,0.0); gradv(fr,1300,H,0.0,0.55); motes(fr,t,0.9)
    kt(fr,"PILIBHIT",anton(210),GOLD,W/2,330,t,0.12,hold_end=1.58,sw=9,glow=(255,150,30)); kt(fr,"TIGER RESERVE",bcs(84),WHITE,W/2,490,t,0.5,hold_end=1.58,sw=6,glow=(0,0,0)); return fr
def bgphoto(k,t,t0,cx=0.5,cy=0.5,w0=0.9,w1=0.8,blur=0,dim=0.45):
    p=seg(t,t0,t0+10); fr=pwin(k,cx,cy,lerp(w0,w1,p),W,H,dim)
    return cv2.GaussianBlur(fr,(0,0),blur) if blur else fr
def S2(t):
    fr=bgphoto("c31da8f7",t,1.6,0.5,0.5,0.7,0.55,14,0.5).copy()
    X,Y=drawchart(fr,(150,560,940,1180),(2009.5,2018.5),0)
    kt(fr,"4 YEARS",anton(130),WHITE,W/2,300,t,1.7,hold_end=9.9,sw=7,glow=(0,0,0))
    upto=2014+4*eo3(seg(t,3.6,7.6)) if t>=3.0 else 2013.9
    # chart limited view 2014-2018 only: reuse full axis but start at 2014
    DATA2=[(2014,25),(2018,65)]
    px0=(X(2014),Y(25)); 
    if t>=2.6:
        a=ease(seg(t,2.6,3.0)); cv2.circle(fr,(int(px0[0]),int(px0[1])),15,(255,255,255),-1,cv2.LINE_AA)
        paste(fr,sprite("25",anton(150),WHITE,sw=7,glow=(0,0,0)),px0[0]+10,px0[1]+110,a)
    if t>=3.6:
        q=eo3(seg(t,3.6,7.6)); e=(lerp(px0[0],X(2018),q),lerp(px0[1],Y(65),q)); cv2.line(fr,(int(px0[0]),int(px0[1])),(int(e[0]),int(e[1])),(255,200,70),12,cv2.LINE_AA)
        if q>=0.999: 
            cv2.circle(fr,(int(X(2018)),int(Y(65))),15,(255,255,255),-1,cv2.LINE_AA)
        v=int(25+40*q); paste(fr,sprite(str(v),anton(210),GOLD,sw=9,glow=(255,150,0)),e[0]-60,e[1]-130,1.0)
    kt(fr,"HOW?",anton(300),RED,W/2,1480,t,8.7,hold_end=9.9,sw=12,glow=(255,40,30))
    kt(fr,"TIGERS DON'T BREED THAT FAST",bcs(60),CREAM,W/2,1650,t,9.0,hold_end=9.9,sw=5) if False else None
    return fr
def S3(t):
    # chart revealing the earlier fall
    if t<16.2:
        fr=bgphoto("454eb397",t,10,0.5,0.45,0.9,0.78,10,0.38).copy()
        X,Y=drawchart(fr,(150,560,940,1180),(2009.5,2018.5),0)
        upto=2010+ (2014-2010)*eo3(seg(t,10.6,14.2)); pts=chartline(fr,X,Y,2018)  if False else None
        # draw full chart base: 2014->2018 gold (already known), earlier dashed progressively
        pts=[(X(a),Y(b)) for a,b in DATA]
        cv2.line(fr,(int(pts[2][0]),int(pts[2][1])),(int(pts[3][0]),int(pts[3][1])),(255,200,70),12,cv2.LINE_AA)
        for p_ in pts[2:]: cv2.circle(fr,(int(p_[0]),int(p_[1])),15,(255,255,255),-1,cv2.LINE_AA)
        chartline(fr,X,Y,min(2014,upto))
        if t>=10.6: kt(fr,"BEFORE THIS,",bcs(80),CREAM,W/2,300,t,10.1,hold_end=16.1,sw=6); kt(fr,"TIGERS WERE FALLING.",anton(110),RED,W/2,430,t,10.6,hold_end=16.1,sw=8,glow=(255,40,30))
        a1=ease(seg(t,11.4,11.8)); paste(fr,sprite("40+",anton(120),(255,150,140),sw=7,glow=(0,0,0)),X(2010)+40,Y(42)-80,a1)
        a2=ease(seg(t,13.8,14.2)); paste(fr,sprite("~23",anton(120),(230,230,230),sw=7,glow=(0,0,0)),X(2013)-10,Y(23)+100,a2)
        paste(fr,sprite("REPORTED ESTIMATES. SOURCES DIFFER.",bar(36),(220,230,235),sw=3,shadow=False),W/2,1330,ease(seg(t,12.0,12.5)))
        return fr
    fr=pwin("454eb397",0.49,0.46,lerp(0.40,0.34,seg(t,16.2,22.5)),W,H,1.0).copy()
    gradv(fr,0,620,0.65,0.0); gradv(fr,1250,H,0.0,0.6); motes(fr,t,0.5)
    ov=np.zeros_like(fr,np.float32); ov[:,:,0]=255*0.06*(1+math.sin(t*6)); add(fr,ov,1.0)
    kt(fr,"QUESTIONS ABOUT",bcs(70),CREAM,W/2,340,t,16.3,hold_end=22.4,sw=5); kt(fr,"POACHING",anton(190),RED,W/2,500,t,16.7,hold_end=22.4,sw=9,glow=(255,40,30))
    kt(fr,"CAUSE NEVER CONFIRMED",bcs(64),WHITE,W/2,1400,t,19.0,hold_end=22.4,sw=5,glow=(0,0,0))
    return fr
K_MAP=[(22.5,79.6,28.0,110,0.0,0.0),(26.0,79.8,28.6,260,0.12,1.5),(29.0,79.8,28.7,420,0.16,-1.0)]
def S4a(t):
    lonc,latc,k,tilt,roll=camk(t,K_MAP)
    w=int(W*1.16); h=int(H*1.16); img,P=rmap(lonc,latc,k,w,h,t)
    px,py=P(*PIL_LL); 
    for i in range(3):
        q=((t-23.0)*0.8+i/3)%1; ring(img,px,py,20+q*260*(k/260),(255,220,120),(1-q)*0.8,6)
    cv2.circle(img,(int(px),int(py)),16,(255,240,170),-1,cv2.LINE_AA)
    cx,cy=w/2,h/2; src=np.float32([[cx-W/2,cy-H/2],[cx+W/2,cy-H/2],[cx+W/2,cy+H/2],[cx-W/2,cy+H/2]]); sh=tilt*W*0.5
    dst=np.float32([[sh,0],[W-sh,0],[W,H],[0,H]]); Pm=cv2.getPerspectiveTransform(src,dst); Rm=np.vstack([cv2.getRotationMatrix2D((W/2,H/2),roll,1.0),[0,0,1]])
    fr=cv2.warpPerspective(img,Rm@Pm,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    pt=cv2.perspectiveTransform(np.float32([[[px,py]]]),(Rm@Pm).astype(np.float32))[0,0]
    kt(fr,"JUNE 2014",anton(150),GOLD,W/2,330,t,22.7,hold_end=28.9,sw=8,glow=(255,150,0)); kt(fr,"TIGER RESERVE",anton(110),WHITE,W/2,470,t,23.1,hold_end=28.9,sw=7,glow=(0,0,0))
    if t>=24.4: pill(fr,"PILIBHIT",pt[0],pt[1]+80,ease(seg(t,24.4,24.8)),size=58)
    if t>=26.5:
        v=int(730*eo3(seg(t,26.5,28.0))); paste(fr,sprite(f"~{v} SQ KM",anton(130),WHITE,sw=8,glow=(0,160,200)),W/2,1250,ease(seg(t,26.5,26.9)))
    if t>=27.6: paste(fr,sprite("INDIA-NEPAL BORDER",bcs(56),(255,215,110),sw=4),W/2,1400,ease(seg(t,27.6,28.0)))
    pill(fr,"SCHEMATIC MAP",W/2,1560,0.9,size=34,fg=(230,230,230),bg=(14,24,30)) if False else None
    vscan(fr,t); hud_corners(fr,50,260,W-50,H-420,CYAN,0.7); return fr
def camk(t,keys):
    if t<=keys[0][0]: return keys[0][1:]
    for a,b in zip(keys[:-1],keys[1:]):
        if a[0]<=t<=b[0]:
            e=ease((t-a[0])/(b[0]-a[0])); return tuple(lerp(x,y,e) for x,y in zip(a[1:],b[1:]))
    return keys[-1][1:]
def vscan(fr,t,a=0.12):
    y=int((t*260)%(H+200)-100); ov=np.zeros((H,W,3),np.float32); cv2.line(ov,(0,y),(W,y),(120,255,250),3); ov=cv2.GaussianBlur(ov,(0,0),12)*2.5; add(fr,ov,a)
def icon_target(fr,cx,cy,s,col):
    cv2.circle(fr,(int(cx),int(cy)),int(34*s),col,int(6*s),cv2.LINE_AA); cv2.circle(fr,(int(cx),int(cy)),int(12*s),col,-1,cv2.LINE_AA)
    for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)): cv2.line(fr,(int(cx+dx*26*s),int(cy+dy*26*s)),(int(cx+dx*52*s),int(cy+dy*52*s)),col,int(6*s),cv2.LINE_AA)
def icon_grass(fr,cx,cy,s,col):
    for i,dx in enumerate((-30,-15,0,15,30)):
        h_=(48-abs(dx)*0.6)*s; pts=np.array([[cx+dx*s,cy+30*s],[cx+dx*s+(dx*0.25)*s,cy+30*s-h_]],np.int32); cv2.polylines(fr,[pts],False,col,int(7*s),cv2.LINE_AA)
def icon_shield(fr,cx,cy,s,col):
    pts=np.array([[cx,cy-46*s],[cx+38*s,cy-30*s],[cx+34*s,cy+14*s],[cx,cy+46*s],[cx-34*s,cy+14*s],[cx-38*s,cy-30*s]],np.int32); cv2.polylines(fr,[pts],True,col,int(7*s),cv2.LINE_AA)
    cv2.line(fr,(int(cx-14*s),int(cy)),(int(cx-3*s),int(cy+12*s)),col,int(7*s),cv2.LINE_AA); cv2.line(fr,(int(cx-3*s),int(cy+12*s)),(int(cx+16*s),int(cy-14*s)),col,int(7*s),cv2.LINE_AA)
def badge(fr,cx,cy,t,t0,label,icon,col=GOLD,s=1.0):
    if t<t0: return
    p=seg(t,t0,t0+0.3); sc=lerp(0.2,1.0,eob(p,2.0))*s; a=min(1,p*3); ov=fr.copy(); r=int(96*sc)
    cv2.circle(ov,(int(cx),int(cy)),r,(10,22,30),-1,cv2.LINE_AA); cv2.circle(ov,(int(cx),int(cy)),r,col,int(6*sc),cv2.LINE_AA); icon(ov,cx,cy,sc*1.05,col); fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
    q=(t-t0)/0.8
    if 0<q<1: ring(fr,cx,cy,r+q*150,col,(1-q)*0.8,5)
    paste(fr,sprite(label,bcs(50),WHITE,sw=5,glow=(0,0,0),glow_r=6),cx,cy+r+44,min(1,(t-t0)/0.25)*a,1.0)
def S4b(t):
    seq=[("c31da8f7",0.5,0.5),("f9c98082",0.5,0.65),("5aa8c4c4",0.6,0.7),("bc299d50",0.7,0.55)]
    i=min(3,int((t-29.0)/1.9)); k,cx,cy=seq[i]; p=((t-29.0)-i*1.9)/1.9
    fr=pwin(k,cx,cy,lerp(0.85,0.7,p),W,H,0.85).copy(); gradv(fr,0,H,0.38,0.38)
    kt(fr,"WHAT NTCA CREDITS",bcs(66),CREAM,W/2,300,t,29.0,hold_end=36.4,sw=5,glow=(0,0,0))
    badge(fr,W/2,640,t,29.5,"PATROLLING TECH (M-STrIPES)",icon_target,GOLD)
    badge(fr,W/2,1010,t,31.8,"BETTER GRASSLAND AND HABITAT",icon_grass,(120,255,160))
    badge(fr,W/2,1380,t,34.0,"ACTION AGAINST POACHERS",icon_shield,(255,120,100))
    return fr
def S5a(t):
    fr=bgphoto("c31da8f7",t,36.5,0.5,0.5,0.7,0.6,16,0.5).copy()
    cols=13; x0=120; y0=600; dx=70; dy=84
    n=int(65*eo3(seg(t,37.0,40.0)))
    sp=0 if t<41.5 else eo3(seg(t,41.5,43.5))
    for i in range(65):
        r_,c_=divmod(i,cols); x=x0+c_*dx; y=y0+r_*dy
        if i<n:
            tr=i>=57; col=(255,200,70) if not tr else lerp_col((255,200,70),(80,235,240),sp)
            cv2.circle(fr,(int(x),int(y)),30,col,-1,cv2.LINE_AA); cv2.circle(fr,(int(x),int(y)),30,(255,255,255),2,cv2.LINE_AA)
    if t<41.5: paste(fr,sprite(str(n),anton(260),WHITE,sw=10,glow=(255,150,0)),W/2,340,1.0)
    if t>=41.5:
        a=ease(seg(t,41.5,42.0)); paste(fr,sprite("57",anton(210),(255,200,70),sw=9,glow=(255,150,0)),W*0.27,1200,a); paste(fr,sprite("RESIDENT",bcs(64),CREAM,sw=4),W*0.27,1330,a)
        paste(fr,sprite("8",anton(210),(80,235,240),sw=9,glow=(0,160,200)),W*0.72,1200,a); paste(fr,sprite("TRANSIT",bcs(64),CREAM,sw=4),W*0.72,1330,a)
        kt(fr,"65 = 57 + 8",anton(150),WHITE,W/2,340,t,41.6,hold_end=44.4,sw=8,glow=(0,0,0))
    kt(fr,"NTCA 2018 ESTIMATE",bcs(60),(210,225,230),W/2,1520,t,38.0,hold_end=44.4,sw=4)
    return fr
def lerp_col(a,b,x): return tuple(int(lerp(u,v,x)) for u,v in zip(a,b))
K_M2=[(44.4,79.9,28.9,300,0.10,-1.0),(51.0,80.1,29.0,420,0.12,1.0)]
def S5b(t):
    lonc,latc,k,tilt,roll=camk(t,K_M2); w=int(W*1.16); h=int(H*1.16); img,P=rmap(lonc,latc,k,w,h,t); px,py=P(*PIL_LL); ex,ey=P(80.15,29.15)
    cv2.circle(img,(int(px),int(py)),16,(255,240,170),-1,cv2.LINE_AA)
    for j in range(4):
        q=((t-45.4)*0.6+j*0.25)%1
        if t>=45.4:
            x=lerp(px,ex+60,q); y=lerp(py,ey-160,q); a=math.sin(q*math.pi); cv2.circle(img,(int(x),int(y)),int(14),(80,235,240),-1,cv2.LINE_AA)
            cv2.line(img,(int(x),int(y)),(int(x-(ex-px)*0.06),int(y-(ey-py)*0.0+14)),(80,235,240),4,cv2.LINE_AA)
    cx,cy=w/2,h/2; src=np.float32([[cx-W/2,cy-H/2],[cx+W/2,cy-H/2],[cx+W/2,cy+H/2],[cx-W/2,cy+H/2]]); sh=tilt*W*0.5
    dst=np.float32([[sh,0],[W-sh,0],[W,H],[0,H]]); Pm=cv2.getPerspectiveTransform(src,dst); Rm=np.vstack([cv2.getRotationMatrix2D((W/2,H/2),roll,1.0),[0,0,1]])
    fr=cv2.warpPerspective(img,Rm@Pm,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    fade(fr,1-ease(seg(t,44.4,44.8)),(255,255,255))
    kt(fr,"TIGERS CROSS",anton(130),WHITE,W/2,320,t,44.9,hold_end=50.9,sw=8,glow=(0,160,200)); kt(fr,"THE INDIA-NEPAL BORDER",anton(84),(80,235,240),W/2,455,t,45.3,hold_end=50.9,sw=7,glow=(0,160,200))
    pill(fr,"SURVEY DOCUMENTED (WII)",W/2,1380,ease(seg(t,47.5,47.9)),size=44)
    paste(fr,sprite("SCHEMATIC. NOT TRACKED PATHS.",bar(34),(220,230,235),sw=3,shadow=False),W/2,1500,0.9)
    vscan(fr,t); hud_corners(fr,50,260,W-50,H-420,CYAN,0.7); return fr
def S5c(t):
    p=seg(t,51.0,56.6); fr=para("4d5819bf",0.5,0.46,lerp(0.98,0.86,p),lerp(0.9,0.62,eo3(p)),W,H,0,0,blur=10,dim=1.03)
    gradv(fr,0,760,0.7,0.0); gradv(fr,1300,H,0.0,0.5); motes(fr,t,0.7)
    kt(fr,"BREEDING?",anton(150),GOLD,W/2,330,t,51.1,hold_end=56.5,sw=8,glow=(255,150,0)); kt(fr,"OR MOVEMENT?",anton(150),(80,235,240),W/2,490,t,52.4,hold_end=56.5,sw=8,glow=(0,160,200))
    kt(fr,"NOBODY CAN SAY EXACTLY.",bcs(70),WHITE,W/2,1430,t,54.0,hold_end=56.5,sw=5,glow=(0,0,0)); return fr
def laurel(fr,cx,cy,r,col,a):
    ov=fr.copy()
    for side in (-1,1):
        for i in range(9):
            ang=math.radians(110+i*17); x=cx+side*(r*math.cos(math.radians(i*17+10))*1.0); 
            xa=cx+side*r*math.sin(math.radians(20+i*19)); ya=cy+r*math.cos(math.radians(20+i*19))*0.95
            cv2.ellipse(ov,(int(xa),int(ya)),(30,12),side*(40+i*10),0,360,col,-1,cv2.LINE_AA)
    fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
def S6(t):
    p=seg(t,56.6,62); fr=para("a4bcbe52",0.5,0.40,lerp(0.9,0.82,p),lerp(0.8,0.66,eo3(p)),W,H,0,0,blur=10,dim=1.0)
    gradv(fr,0,560,0.7,0.0); gradv(fr,1150,H,0.0,0.75); motes(fr,t,0.9)
    laurel(fr,W/2,1370,200,(255,200,70),ease(seg(t,57.2,57.8)))
    kt(fr,"TX2",anton(260),GOLD,W/2,1360,t,57.2,hold_end=61.9,sw=10,glow=(255,150,0)); kt(fr,"FIRST EVER AWARD · 2020",bcs(60),WHITE,W/2,1560,t,57.8,hold_end=61.9,sw=5,glow=(0,0,0))
    kt(fr,"25 → 65",anton(130),WHITE,W/2,330,t,57.4,hold_end=61.9,sw=8,glow=(255,150,30))
    flare(fr,H*0.6,0.7*math.exp(-(t-57.2)*5)*(t>=57.2)); return fr
def S7(t):
    fr=np.zeros((H,W,3),np.uint8); fr[:]=(12,30,22)
    # narrow forest strip with sugarcane fields on both sides
    cx=W/2; sw_=lerp(300,300,0)
    for k_ in range(0,H,22):
        pass
    fr[:,:]=(120,104,44)
    yy,xx=np.mgrid[0:H,0:W]
    stripe=((xx//18)%2==0)
    fr[stripe]=(108,94,40)
    fr=cv2.GaussianBlur(fr,(0,0),2)
    # forest strip
    fx0,fx1=int(W*0.36),int(W*0.64); fr[:,fx0:fx1]=(18,70,42)
    nz=scrolled(N2,W,H,1.0,0,t*30)[:,fx0:fx1]; fr[:,fx0:fx1]=np.clip(fr[:,fx0:fx1].astype(np.float32)*(1+0.25*nz[:,:,None]),0,255).astype(np.uint8)
    cv2.line(fr,(fx0,0),(fx0,H),(255,230,150),4); cv2.line(fr,(fx1,0),(fx1,H),(255,230,150),4)
    paste(fr,sprite("FOREST",bcs(56),WHITE,sw=4),W/2,980,ease(seg(t,62.2,62.6))); paste(fr,sprite("SUGARCANE",bcs(56),(255,235,170),sw=4),W*0.17,980,ease(seg(t,62.4,62.8))); paste(fr,sprite("SUGARCANE",bcs(56),(255,235,170),sw=4),W*0.83,980,ease(seg(t,62.4,62.8)))
    # tigers dots crossing out
    if t>=63.5:
        for j in range(3):
            q=((t-63.5)*0.5+j*0.33)%1; x=lerp(W*0.5,W*(0.2 if j%2 else 0.8),q); y=560+j*110; cv2.circle(fr,(int(x),int(y)),16,(255,230,120),-1,cv2.LINE_AA); ring(fr,x,y,30,(255,230,120),0.5*(1-q),3)
    kt(fr,"NARROW FOREST.",anton(110),WHITE,W/2,300,t,62.1,hold_end=70.4,sw=8,glow=(0,0,0)); kt(fr,"SUGARCANE EDGE.",anton(110),GOLD,W/2,430,t,62.7,hold_end=70.4,sw=8,glow=(255,150,0))
    if t>=66.0:
        v=int(26*eo3(seg(t,66.0,67.0))); paste(fr,sprite(str(v),anton(300),WHITE,sw=12,glow=(255,40,30)),W*0.30,1230,1.0)
        paste(fr,sprite("BIG-CAT",bcs(56),CREAM,sw=4),W*0.30,1400,ease(seg(t,66.4,66.8))); paste(fr,sprite("CONFLICT CASES",bcs(56),CREAM,sw=4),W*0.30,1455,ease(seg(t,66.4,66.8)))
    if t>=67.8:
        paste(fr,sprite("18",anton(300),RED,sw=12,glow=(255,40,30)),W*0.72,1230,ease(seg(t,67.8,68.2))); paste(fr,sprite("INVOLVED TIGERS",bcs(56),CREAM,sw=4),W*0.72,1400,ease(seg(t,68.0,68.4)))
    paste(fr,sprite("2024 · PILIBHIT AREA · SOURCE: WTI",bar(34),(235,235,235),sw=3,shadow=False),W/2,1600,ease(seg(t,68.6,69.0)))
    return fr
def S8(t):
    seq=[("a4bcbe52",0.5,0.42,0.85,0.7,"para"),("05008004",0.5,0.55,0.6,0.45,"para"),("c31da8f7",0.5,0.5,0.7,0.55,"plain")]
    i=0 if t<73.2 else (1 if t<75.4 else 2)
    if i==0: p=seg(t,70.5,73.2); fr=para("a4bcbe52",0.5,0.40,lerp(0.9,0.84,p),lerp(0.8,0.66,eo3(p)),W,H,0,0,blur=10,dim=1.0)
    elif i==1: p=seg(t,73.2,75.4); fr=pext("05008004",570,lerp(1.0,1.08,p))
    else: p=seg(t,75.4,80); fr=pwin("c31da8f7",0.5,0.5,lerp(0.62,0.5,p),W,H,0.95).copy()
    gradv(fr,0,700,0.6,0.0); gradv(fr,1250,H,0.0,0.6); motes(fr,t,0.8)
    kt(fr,"TIGERS CAN",anton(150),WHITE,W/2,330,t,70.6,hold_end=73.1,sw=8,glow=(0,0,0)); kt(fr,"COME BACK.",anton(190),GOLD,W/2,500,t,71.1,hold_end=73.1,sw=9,glow=(255,150,0))
    kt(fr,"THE TEST NOW:",bcs(80),CREAM,W/2,330,t,73.3,hold_end=77.0,sw=6,glow=(0,0,0)); kt(fr,"SHARING THE EDGE.",anton(130),(120,255,160),W/2,470,t,73.7,hold_end=77.0,sw=8,glow=(0,120,60))
    kt(fr,"THE NATURAL ANGLE",anton(100),GOLD,W/2,1330,t,77.4,sw=8,glow=(255,150,0)); paste(fr,sprite("Photos: Hitesh Chawla",bar(42),CREAM,sw=3),W/2,1440,ease(seg(t,77.8,78.3)))
    fade(fr,ease(seg(t,79.2,80.0))); return fr
SC=[(0,1.6,S1),(1.6,10.0,S2),(10.0,22.5,S3),(22.5,29.0,S4a),(29.0,36.5,S4b),(36.5,44.4,S5a),(44.4,51.0,S5b),(51.0,56.6,S5c),(56.6,62.0,S6),(62.0,70.5,S7),(70.5,80.01,S8)]
HITS=[(0.12,1.4),(1.6,1.0),(2.7,0.7),(7.5,1.2),(8.7,1.3),(10.1,1.0),(11.4,0.7),(14.0,0.8),(16.3,1.2),(22.7,1.2),(24.4,0.8),(29.5,0.8),(31.8,0.8),(34.0,0.8),(36.5,1.0),(41.5,1.3),(44.9,1.1),(51.1,1.2),(52.4,0.8),(57.2,1.5),(62.1,1.2),(66.0,0.9),(67.8,1.1),(70.6,1.2),(73.3,0.9),(77.4,0.8)]
TR=[1.6,10.0,22.5,29.0,36.5,44.4,51.0,56.6,62.0,70.5]
NEWT=[0,1.9,3.0,4.4,6.6,8.0,9.93,13.3,15.4,17.0,18.3,20.5,20.55,22.9,23.4,24.0,24.3,25.9,27.1,28.7,31.4,31.5,33.6,34.0,37.6,37.9,38.35,40.5,42.3,44.5,46.4,48.7,48.8,50.0,52.0,52.05,54.2,55.8,58.6,60.55,60.6,60.8,62.7,63.05,64.8,68.2,68.4,70.2,71.0]
OLDT=[0,1.6,2.6,3.6,7.6,8.6,10.0,11.4,12.0,14.0,16.2,22.4,22.5,24.4,26.5,28.0,29.0,29.5,31.8,34.0,36.4,36.5,40.0,41.5,44.2,44.4,44.9,47.5,51.0,52.4,54.0,56.5,56.6,57.2,61.9,62.0,62.7,66.0,67.8,70.4,70.5,70.6,73.1,73.3,73.7,77.0,77.4,79.2,80.0]
def frame(t):
    return frame_old(float(np.interp(t,NEWT,OLDT)))
def frame_old(t):
    for (a,b,fn) in SC:
        if a<=t<b: break
    fr=fn(t)
    for tb in TR:
        dt=t-tb
        if 0<=dt<0.16: fr=np.clip(fr.astype(np.float32)+255*(1-dt/0.16)**2*0.7,0,255).astype(np.uint8)
    fr=punch(fr,t,HITS); return look(fr,t,HITS)
if __name__=="__main__":
    ts=[float(x) for x in sys.argv[1:]]
    for t in ts: cv2.imwrite(f"{HERE}t_{t:05.1f}.jpg",cv2.cvtColor(frame(t),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,88])
