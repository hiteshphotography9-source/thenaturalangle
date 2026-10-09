import sys, json, math
sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pnv')
import scenes as B
from scenes import *
HB="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/p151b/"
DUR=132.6
IMG={}
def im(n):
    if n not in IMG: IMG[n]=cv2.cvtColor(cv2.imread(HB+f"src/{n}.jpg"),cv2.COLOR_BGR2RGB)
    return IMG[n]
# subject rects (normalised x0,x1,y0,y1) for text-safety checks
SUBJ={"cub_pair":[(0.20,0.29,0.38,0.58),(0.48,0.77,0.32,0.72)],"three":[(0.26,0.76,0.33,0.83)],"walk":[(0.18,0.62,0.40,0.70)],"cubs_walk":[(0.37,0.88,0.33,0.80)],
      "water":[(0.39,0.94,0.55,0.77)],"shore":[(0.56,0.70,0.74,0.87)],"yawn":[(0.0,1.0,0.12,0.95)],"two_look":[(0.0,1.0,0.12,0.95)],"stretch":[(0.0,1.0,0.12,0.95)],"bts1":[],"bts2":[],"bts3":[]}
FADE={"yawn":0.22,"two_look":0.22,"stretch":0.22}
def lerpk(keys,t):
    if t<=keys[0][0]: return keys[0][1:]
    if t>=keys[-1][0]: return keys[-1][1:]
    for a,b in zip(keys[:-1],keys[1:]):
        if a[0]<=t<=b[0]:
            e=ease((t-a[0])/(b[0]-a[0])); return tuple(lerp(x,y,e) for x,y in zip(a[1:],b[1:]))
LASTR=None
def shot(name,t,keys,dim=1.0,grade=None,shake=1.0,pin='bottom'):
    """full-bleed 9:16 camera move. keys: (t,cx,cy,z). Portrait z<1 = image pinned bottom with top fading to black."""
    global LASTR
    src=im(name); ih,iw=src.shape[:2]; cx,cy,z=lerpk(keys,t)
    wh=ih/z; ww=wh*W/H; s=H/wh
    fade=FADE.get(name,0)
    if z>=1.0 or not fade:
        cx=min(max(cx,ww/2/iw),1-ww/2/iw) if ww<iw else 0.5
        cy=min(max(cy,wh/2/ih),1-wh/2/ih) if wh<ih else 0.5
    else:
        cx=min(max(cx,ww/2/iw),1-ww/2/iw) if ww<iw else 0.5
        cy=(ih-wh/2)/ih if pin=='bottom' else (wh/2)/ih
    jx=math.sin(t*1.7)*3*shake; jy=math.cos(t*1.3)*3*shake
    M=np.array([[s,0,W/2-cx*iw*s+jx],[0,s,H/2-cy*ih*s+jy]],np.float32)
    out=cv2.warpAffine(src,M,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0))
    if fade:
        r=np.clip(np.arange(ih)/(ih*fade),0,1)**1.5
        if pin!='bottom': r=r[::-1]
        m=np.repeat(r[:,None],iw,1).astype(np.float32)
        am=cv2.warpAffine(m,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=0)[:,:,None]
        out=(out.astype(np.float32)*am).astype(np.uint8)
    if name=='walk':
        lab=cv2.cvtColor(out,cv2.COLOR_RGB2LAB); lab[:,:,0]=cv2.createCLAHE(clipLimit=2.4,tileGridSize=(6,6)).apply(lab[:,:,0]); out=cv2.cvtColor(lab,cv2.COLOR_LAB2RGB)
    # unsharp to counter the upscale softness
    bl=cv2.GaussianBlur(out,(0,0),1.6); out=cv2.addWeighted(out,1.45,bl,-0.45,0)
    out=(out.astype(np.float32)*dim)
    if grade=="cold":
        g=out.mean(2,keepdims=True); out=g+(out-g)*0.45; out=out*np.array((0.92,0.98,1.08),np.float32)
    elif grade=="dusk":
        out=out*np.array((1.04,0.97,0.9),np.float32)
    out=np.clip(out,0,255).astype(np.uint8)
    m=np.zeros((H,W),bool)
    for (x0,x1,y0,y1) in SUBJ.get(name,[]):
        X0=int(M[0,0]*x0*iw+M[0,2]); X1=int(M[0,0]*x1*iw+M[0,2]); Y0=int(M[1,1]*y0*ih+M[1,2]); Y1=int(M[1,1]*y1*ih+M[1,2])
        m[max(Y0,0):max(Y1,0),max(X0,0):max(X1,0)]=True
    B.LASTA=m
    return out
def lightleak(fr,t,t0,dur=0.9,col=(255,170,70),a=0.28):
    p=(t-t0)/dur
    if not (0<=p<=1): return
    cx=lerp(-0.2,1.2,p)*W; yy,xx=np.mgrid[0:H,0:W]; g=np.exp(-(((xx-cx)/380)**2+((yy-H*0.35)/900)**2)).astype(np.float32)[:,:,None]
    add(fr,g*np.array(col,np.float32),a*math.sin(math.pi*p))
def chroma(fr,amt):
    if amt<0.5: return fr
    a=int(amt); out=fr.copy(); out[:,:,0]=np.roll(fr[:,:,0],a,1); out[:,:,2]=np.roll(fr[:,:,2],-a,1); return out
def motionblur_h(fr,L):
    if L<2: return fr
    k=np.zeros((1,L),np.float32); k[0,:]=1.0/L; return cv2.filter2D(fr,-1,k)
def txtfade(fr,t,a,b): pass
# ------------------- scenes
def S1(t):
    fr=shot("shore",t,[(0,0.62,0.62,1.0),(5.7,0.63,0.66,1.35)],dim=0.9,grade="dusk"); gradv(fr,0,760,0.62,0.0); gradv(fr,1500,H,0.0,0.4); motes(fr,t,0.35)
    kt(fr,"1 FEBRUARY 2023",anton(116),WHITE,W/2,300,t,0.85,hold_end=5.5,sw=8,glow=(255,150,0))
    kt(fr,"PANNA'S FIRST TIGRESS, T1,",bcs(66),CREAM,W/2,440,t,2.85,hold_end=5.5,sw=6); kt(fr,"HAS DIED.",anton(100),RED,W/2,545,t,3.9,hold_end=5.5,sw=8,glow=(255,40,30))
    return fr
def S2(t):
    fr=shot("cub_pair",t,[(5.7,0.245,0.5,1.0),(8.4,0.25,0.5,1.0),(11.2,0.64,0.5,1.12),(13.0,0.64,0.5,1.2)]); gradv(fr,0,640,0.6,0.0); gradv(fr,1450,H,0.0,0.55); motes(fr,t,0.4)
    kt(fr,"NEXT DAY",bcs(84),CREAM,W/2,270,t,6.0,hold_end=7.4,sw=6)
    kt(fr,"P-151",anton(210),GOLD,W/2,400,t,7.5,hold_end=12.6,sw=11,glow=(255,150,0))
    kt(fr,"WITH 4 CUBS",anton(110),WHITE,W/2,1600,t,9.8,hold_end=12.6,sw=8,glow=(0,0,0))
    return fr
def S3(t):
    fr=shot("walk",t,[(13.0,0.44,0.55,1.0),(16.1,0.50,0.55,1.05)]); gradv(fr,0,500,0.45,0.0); gradv(fr,1500,H,0.0,0.45); motes(fr,t,0.4); return fr
def S4(t): return B_map(t)
def B_map(t):
    keys=[(15.9,80.6,24.3,420,0.10,0.0),(23.4,80.55,24.2,520,0.12,-0.8)]
    lonc,latc,k,tilt,roll=camk(t,keys); fr,pr=mapview(lonc,latc,k,tilt,roll,t)
    px,py=pr(*PANNA); bx,by=pr(*BAND)
    q=eo3(seg(t,17.0,19.2)); polyline(fr,pr,[BAND,PANNA],(255,200,70),7,1.0,q,dash=24); dotp(fr,bx,by,15,(255,200,70)); dotp(fr,lerp(bx,px,q),lerp(by,py,q),13,(255,255,255))
    dotp(fr,px,py,20,(255,240,170))
    for j in range(3):
        qq=((t-16.4)*0.7+j/3)%1; ring(fr,px,py,18+qq*110,(255,220,120),(1-qq)*0.7,5)
    pill(fr,"PANNA",px+120,py,ease(seg(t,16.3,16.7)),size=50); pill(fr,"BANDHAVGARH",bx+160,by,ease(seg(t,16.6,17.0)),size=44)
    kt(fr,"2009",anton(150),GOLD,W/2,300,t,16.4,hold_end=19.7,sw=8,glow=(255,150,0))
    kt(fr,"T1 BROUGHT TO PANNA",bcs(70),WHITE,W/2,450,t,17.0,hold_end=19.7,sw=6)
    kt(fr,"ZERO TIGERS",anton(120),RED,W/2,320,t,19.95,hold_end=23.0,sw=9,glow=(255,40,30)); kt(fr,"IN THE RESERVE",bcs(70),CREAM,W/2,450,t,20.6,hold_end=23.0,sw=6)
    pill(fr,"SCHEMATIC MAP. NOT TO SCALE.",W/2,1790,0.85,size=30,fg=(225,225,225),bg=(14,24,30))
    vscan(fr,t); hud_corners(fr,50,200,W-50,H-250,CYAN,0.6); B.LASTA=None; return fr
def S5(t):
    fr=shot("cubs_walk",t,[(23.5,0.44,0.55,1.0),(33.0,0.78,0.55,1.08)]); gradv(fr,0,640,0.65,0.0); gradv(fr,1500,H,0.0,0.7); motes(fr,t,0.4)
    kt(fr,"IN HER LIFE, T1 HAD",bcs(64),CREAM,W/2,260,t,23.9,hold_end=29.2,sw=5)
    v=count(t,24.6,26.6,13)
    if t>=24.4: kt(fr,f"{v} CUBS",anton(190),GOLD,W/2,410,t,24.4,hold_end=33.0,sw=10,glow=(255,150,0),glitch=False)
    x0=W/2-6*66
    for i in range(13):
        ti=25.2+i*0.12
        if t<ti: continue
        a=ease(seg(t,ti,ti+0.2)); col=(255,200,70)
        if i==12 and t>=30.5: col=(80,235,240); r=26+int(8*math.sin((t-30.5)*6))
        else: r=22
        ov=fr.copy(); cv2.circle(ov,(int(x0+i*66),1650),r,col,-1,cv2.LINE_AA); cv2.circle(ov,(int(x0+i*66),1650),r,(255,255,255),3,cv2.LINE_AA); fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
    if t>=30.5: paste(fr,sprite("ONE OF THEM: P-151",bcs(60),(80,235,240),sw=5,glow=(0,160,200)),W/2,1755,ease(seg(t,30.5,30.9)))
    return fr
def S6(t):
    if t<37.4:
        fr=shot("bts2",t,[(33.0,0.50,0.5,1.0),(37.4,0.46,0.5,1.12)],grade="dusk"); gradv(fr,0,640,0.55,0.0); gradv(fr,1450,H,0.0,0.55); motes(fr,t,0.4)
        kt(fr,"KEN RIVER",anton(150),(110,225,255),W/2,280,t,33.5,hold_end=37.3,sw=9,glow=(0,160,200)); kt(fr,"MADLA FOREST",bcs(76),WHITE,W/2,430,t,34.4,hold_end=37.3,sw=6)
        pill(fr,"BEHIND THE SCENES",W/2,1790,ease(seg(t,33.6,34.0)),size=30,fg=(230,230,230),bg=(14,24,30)); return fr
    fr=shot("water",t,[(37.4,0.47,0.62,1.0),(44.2,0.80,0.62,1.1)]); gradv(fr,0,640,0.62,0.0); gradv(fr,1450,H,0.0,0.55); motes(fr,t,0.4)
    kt(fr,"TERRITORY ON",bcs(76),CREAM,W/2,280,t,37.6,hold_end=43.9,sw=6); kt(fr,"BOTH BANKS",anton(150),GOLD,W/2,430,t,38.1,hold_end=43.9,sw=9,glow=(255,150,0))
    return fr
def S7(t):
    if t<50.0:
        fr=shot("two_look",t,[(44.2,0.5,0.5,0.78),(50.0,0.5,0.5,0.9)]); gradv(fr,1500,H,0.0,0.5); motes(fr,t,0.4); return fr
    fr=shot("bts1",t,[(50.0,0.22,0.5,1.0),(54.7,0.30,0.5,1.12)]); gradv(fr,0,640,0.5,0.0); gradv(fr,1450,H,0.0,0.55); motes(fr,t,0.35)
    pill(fr,"BEHIND THE SCENES",W/2,1790,ease(seg(t,50.2,50.6)),size=30,fg=(230,230,230),bg=(14,24,30)); return fr
def S8(t):
    if t<56.5: fr=shot("cubs_walk",t,[(54.7,0.44,0.52,1.0),(56.5,0.50,0.52,1.1)])
    elif t<57.45: fr=shot("two_look",t,[(56.5,0.5,0.5,0.72),(57.45,0.5,0.5,0.76)])
    else: fr=shot("three",t,[(57.45,0.48,0.55,1.0),(58.9,0.56,0.55,1.0)])
    gradv(fr,0,600,0.6,0.0); gradv(fr,1500,H,0.0,0.6); motes(fr,t,0.4)
    kt(fr,"HER LITTERS",bcs(64),CREAM,W/2,160,t,54.9,hold_end=58.6,sw=6)
    for val,t0,t1,lab in ((1,55.15,56.5,"CUB"),(2,56.55,57.4,"CUBS"),(4,57.45,58.9,"CUBS")):
        if t0<=t<t1+0.1: kt(fr,str(val),anton(260),GOLD,W/2,340,t,t0,hold_end=t1,sw=13,glow=(255,150,0),glitch=False); paste(fr,sprite(lab,bcs(56),WHITE,sw=5),W/2,470,ease(seg(t,t0,t0+0.25))*(1 if t<t1 else 0))
    return fr
def S9(t):
    fr=shot("stretch",t,[(58.9,0.5,0.5,0.8),(64.4,0.5,0.5,0.92)]); gradv(fr,1500,H,0.0,0.5); motes(fr,t,0.4); return fr
def S10(t):
    fr=shot("walk",t,[(64.4,0.50,0.55,1.1),(68.8,0.42,0.55,1.2)],dim=0.95,grade="cold"); gradv(fr,0,640,0.62,0.0); gradv(fr,1500,H,0.0,0.45)
    kt(fr,"BUT THE JUNGLE",bcs(86),CREAM,W/2,270,t,64.6,hold_end=68.6,sw=6); kt(fr,"GIVES NO GUARANTEE",anton(108),RED,W/2,410,t,66.0,hold_end=68.6,sw=8,glow=(255,40,30))
    return fr
def S11(t):
    if t<73.4:
        fr=shot("water",t,[(68.8,0.82,0.62,1.0),(73.4,0.48,0.62,1.12)]); gradv(fr,0,640,0.6,0.0); gradv(fr,1450,H,0.0,0.55); motes(fr,t,0.4)
        kt(fr,"SUMMER",bcs(84),CREAM,W/2,270,t,69.0,hold_end=73.2,sw=6); kt(fr,"AT THE WATER",anton(130),(110,225,255),W/2,415,t,69.6,hold_end=73.2,sw=8,glow=(0,160,200)); return fr
    fr=shot("yawn",t,[(73.4,0.5,0.5,0.8),(78.0,0.5,0.5,0.9)]); gradv(fr,1500,H,0.0,0.5); motes(fr,t,0.4)
    kt(fr,"THE CUBS PLAY",anton(130),GOLD,W/2,300,t,75.0,hold_end=77.8,sw=9,glow=(255,150,0)); return fr
def S12(t):
    fr=shot("three",t,[(78.0,0.52,0.58,1.0),(85.0,0.55,0.58,1.12)]); gradv(fr,0,640,0.6,0.0); gradv(fr,1500,H,0.0,0.55); motes(fr,t,0.4)
    kt(fr,"FOR A MOMENT",bcs(80),CREAM,W/2,260,t,78.1,hold_end=80.1,sw=6); kt(fr,"ALL IS WELL",anton(125),GOLD,W/2,395,t,78.5,hold_end=80.1,sw=9,glow=(255,150,0))
    kt(fr,"BUT THE JUNGLE IS",bcs(76),CREAM,W/2,260,t,80.4,hold_end=84.8,sw=6); kt(fr,"NOT ALWAYS KIND",anton(125),RED,W/2,395,t,81.2,hold_end=84.8,sw=9,glow=(255,40,30))
    return fr
def S13(t):
    fr=shot("walk",t,[(85.0,0.46,0.55,1.1),(98.5,0.50,0.55,1.22)],dim=0.9,grade="cold"); gradv(fr,0,640,0.68,0.0); gradv(fr,1450,H,0.0,0.6)
    kt(fr,"30 JUNE 2026",anton(150),WHITE,W/2,280,t,85.4,hold_end=91.8,sw=9,glow=(0,0,0)); kt(fr,"AS REPORTED",bcs(76),CREAM,W/2,420,t,87.5,hold_end=91.8,sw=6)
    kt(fr,"A 17-MONTH-OLD CUB",bcs(84),CREAM,W/2,270,t,92.4,hold_end=98.3,sw=6); kt(fr,"OF P-151",anton(125),GOLD,W/2,400,t,93.4,hold_end=98.3,sw=9,glow=(255,150,0))
    pill(fr,"REPORTED. NOT OFFICIALLY CONFIRMED.",W/2,1760,ease(seg(t,87.4,87.9)),size=32,fg=(240,240,240),bg=(60,20,20)); return fr
def S14(t):
    if t<108.0:
        fr=shot("bts3",t,[(98.5,0.22,0.5,1.0),(108.0,0.30,0.5,1.12)]); gradv(fr,0,600,0.5,0.0); gradv(fr,1450,H,0.0,0.55); motes(fr,t,0.35)
        pill(fr,"BEHIND THE SCENES",W/2,1790,ease(seg(t,98.7,99.1)),size=30,fg=(230,230,230),bg=(14,24,30)); return fr
    fr=shot("two_look",t,[(108.0,0.5,0.5,0.76),(118.7,0.5,0.5,0.82)],dim=0.85,grade="cold"); gradv(fr,1450,H,0.0,0.6); motes(fr,t,0.3)
    kt(fr,"LESS SPACE.",anton(130),WHITE,W/2,250,t,108.2,hold_end=118.5,sw=9,glow=(0,0,0)); kt(fr,"HARDER SURVIVAL.",anton(105),RED,W/2,380,t,109.4,hold_end=118.5,sw=9,glow=(255,40,30)); return fr
def S15(t):
    fr=shot("cub_pair",t,[(118.7,0.64,0.5,1.1),(121.5,0.64,0.5,1.0),(124.2,0.245,0.5,1.0)]); gradv(fr,0,640,0.6,0.0); gradv(fr,1450,H,0.0,0.55); motes(fr,t,0.4)
    kt(fr,"TIGERS CAME BACK.",anton(108),GOLD,W/2,280,t,119.2,hold_end=121.6,sw=8,glow=(255,150,0)); kt(fr,"IS THERE ROOM?",anton(118),WHITE,W/2,280,t,121.7,hold_end=123.9,sw=8,glow=(0,0,0)); return fr
def S16(t):
    fr=shot("yawn",t,[(124.2,0.5,0.5,0.68),(DUR,0.5,0.5,0.72)],dim=0.95,pin="top"); gradv(fr,1250,H,0.0,0.7); motes(fr,t,0.35)
    a=ease(seg(t,124.5,125.0))
    paste(fr,sprite("FULL PANNA STORY",anton(118),WHITE,sw=8,glow=(255,150,0)),W/2,1450,a); paste(fr,sprite("ON MY CHANNEL, LINK BELOW",bcs(62),CREAM,sw=5),W/2,1570,a)
    paste(fr,sprite("THE NATURAL ANGLE",anton(82),GOLD,sw=7,glow=(255,150,0)),W/2,1690,a); paste(fr,sprite("Photos: Hitesh Chawla",bar(32),CREAM,sw=3),W/2,1795,a)
    fade(fr,ease(seg(t,131.4,DUR))); return fr
SC=[(0,5.7,S1),(5.7,13.0,S2),(13.0,16.1,S3),(16.1,23.5,S4),(23.5,33.0,S5),(33.0,44.2,S6),(44.2,54.7,S7),(54.7,58.9,S8),(58.9,64.4,S9),(64.4,68.8,S10),(68.8,78.0,S11),(78.0,85.0,S12),(85.0,98.5,S13),(98.5,118.7,S14),(118.7,124.2,S15),(124.2,DUR+1,S16)]
HITS=[(0.85,0.8),(7.5,0.6),(16.4,0.6),(19.95,0.7),(24.4,0.5),(30.5,0.5),(55.15,0.7),(56.55,0.7),(57.45,0.8),(66.0,0.6),(85.4,0.7),(108.2,0.6),(119.2,0.5),(124.5,0.5)]
LEAKS=[5.7,16.1,33.0,44.2,64.4+0.0,78.0,118.7]
def frame(t):
    for i,(a,b,fn) in enumerate(SC):
        if a<=t<b: break
    fr=fn(t)
    if i>0 and t-a<0.4:
        pa,pb,pf=SC[i-1]; prev=pf(min(t,pb-0.001)); k=(t-a)/0.4; e=ease(k)
        L=int(70*math.sin(math.pi*k)); 
        fr=(motionblur_h(prev,L).astype(np.float32)*(1-e)+motionblur_h(fr,L).astype(np.float32)*e).astype(np.uint8)
    for lt in LEAKS: lightleak(fr,t,lt-0.1)
    for th,s in HITS:
        dt=t-th
        if 0<=dt<0.22: fr=chroma(fr,6*s*(1-dt/0.22))
    fr=punch(fr,t,HITS); return look(fr,t,HITS)
if __name__=="__main__":
    ts=[float(x) for x in sys.argv[2:]]; tiles=[]
    for t in ts:
        f=frame(t); f=cv2.resize(f,(270,480)); cv2.putText(f,f"{t}",(6,24),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,0),2); tiles.append(f)
    cols=8; rows=(len(tiles)+cols-1)//cols; img=np.zeros((rows*480,cols*270,3),np.uint8)
    for i,f in enumerate(tiles): img[(i//cols)*480:(i//cols+1)*480,(i%cols)*270:(i%cols+1)*270]=f
    cv2.imwrite(sys.argv[1],cv2.cvtColor(img,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,88])
