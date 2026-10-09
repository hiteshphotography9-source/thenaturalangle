import sys, math, json
sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pil')
from eng import *
HP="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pitta/"
FPS_S=30000/1001.0
TOTAL=34.0
_C={}
def src(clip,i):
    n={"A":435,"B":447}[clip]; i=max(1,min(n,int(i))); k=(clip,i)
    if k not in _C:
        if len(_C)>80: _C.pop(next(iter(_C)))
        _C[k]=cv2.cvtColor(cv2.imread(HP+f"{clip}/{clip.lower()}_{i:04d}.jpg"),cv2.COLOR_BGR2RGB)
    return _C[k]
def srcf(clip,ts):
    f=ts*FPS_S+1; a=int(math.floor(f)); u=f-a; Fa=src(clip,a)
    if u<0.03: return Fa
    return cv2.addWeighted(Fa,1-u,src(clip,a+1),u,0)
# segments: new0,new1,clip,src0,src1 ; crop keys per segment (cx,cy in source px, zoom over 640x800 base)
SEG=[(0.0,3.0,"A",9.55,10.95,[(0,330,560,1.0),(3,340,560,1.12)]),
     (3.0,9.0,"A",0.3,6.3,[(0,330,560,1.0),(6,320,540,1.1)]),
     (9.0,15.0,"B",1.0,5.0,[(0,300,540,1.3),(6,300,540,1.18)]),
     (15.0,21.0,"B",5.3,8.8,[(0,380,600,1.1),(2.2,420,560,1.3),(3.4,430,550,1.35),(6,380,580,1.15)]),
     (27.5,34.0,"A",11.0,14.5,[(0,320,560,1.0),(6.5,320,540,1.2)])]
WY,WH=330,1350
def segof(t):
    for s in SEG:
        if s[0]<=t<s[1]+1e-6: return s
    return None
def ckeys(keys,t):
    if t<=keys[0][0]: return keys[0][1:]
    for a,b in zip(keys[:-1],keys[1:]):
        if a[0]<=t<=b[0]:
            e=ease((t-a[0])/(b[0]-a[0])); return tuple(lerp(x,y,e) for x,y in zip(a[1:],b[1:]))
    return keys[-1][1:]
def footage(t):
    s=segof(t); n0,n1,clip,s0,s1,keys=s
    ts=s0+(t-n0)/(n1-n0)*(s1-s0); fr=srcf(clip,ts)
    cx,cy,z=ckeys(keys,t-n0)
    top,bot=(52,1084) if clip=="B" else (0,1136)
    cw=640/z; ch=cw*WH/1080
    x0=min(max(cx-cw/2,0),640-cw); y0=min(max(cy-ch/2,top),bot-ch)
    sc=1080/cw; M=np.array([[sc,0,-x0*sc],[0,sc,-y0*sc]],np.float32)
    out=cv2.warpAffine(fr,M,(1080,WH),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
    bl=cv2.GaussianBlur(out,(0,0),1.6); out=cv2.addWeighted(out,1.5,bl,-0.5,0)   # recover softness from 640 px source
    f=out.astype(np.float32); f=(f-128)*1.07+128; g=f.mean(2,keepdims=True); f=g+(f-g)*1.1
    return np.clip(f,0,255).astype(np.uint8),M,ts,clip
def bgfrom(win):
    b=cv2.resize(win,(int(1080*H/WH),H)); x0=(b.shape[1]-W)//2; b=b[:,x0:x0+W]; b=cv2.GaussianBlur(b,(0,0),42); return (b*0.30).astype(np.uint8)
SW=[("CROWN",(196,150,70)),("MASK",(22,24,30)),("THROAT",(240,244,248)),("BREAST",(214,165,70)),("VENT",(222,55,35)),("LEGS",(236,170,176)),("BACK",(28,110,78)),("RUMP",(60,200,235)),("WING",(86,160,70))]
SWT=[3.8,4.8,5.8,6.8,7.8,8.5,10.2,11.6,12.9]   # reveal times
def swatches(fr,t,y=1790,a=1.0,final=False):
    n=sum(1 for x in SWT if t>=x) if not final else 9
    for i,(nm,c) in enumerate(SW):
        x=W/2+(i-4)*100; r=34
        ti=SWT[i] if not final else 27.7+i*0.12
        if t<ti-0.3: 
            cv2.circle(fr,(int(x),y),r,(80,90,95),2,cv2.LINE_AA); continue
        p=ease(seg(t,ti-0.3,ti)); rr=int(r*(0.4+0.6*p))
        cv2.circle(fr,(int(x),y),rr,c[::-1] if False else c,-1,cv2.LINE_AA); cv2.circle(fr,(int(x),y),rr,(255,255,255),3,cv2.LINE_AA)
        q=(t-ti)/0.7
        if 0<q<1: ring(fr,x,y,r+q*40,(255,255,255),(1-q)*0.7,3)
    return n
def mouthring(fr,M,t_src,t):
    # beak-tip location in source px for clip B around the catch
    P=[(6.2,(560,470)),(6.8,(570,440)),(7.2,(575,436)),(7.6,(560,455)),(8.0,(520,470))]
    for (ta,pa),(tb,pb) in zip(P[:-1],P[1:]):
        if ta<=t_src<=tb: u=(t_src-ta)/(tb-ta); p=(lerp(pa[0],pb[0],u),lerp(pa[1],pb[1],u)); break
    else: return
    x=M[0,0]*p[0]+M[0,2]; y=M[1,1]*p[1]+M[1,2]+WY
    return x,y
def mapscene(t):
    lt=t-21.0
    lonc,latc,k=79.0,21.0,52.0
    mw,mh=int(W*1.0),int(H*1.0)
    img=map_img(lonc,latc,k,W,H,t,0.0,0.6)
    img=cv2.GaussianBlur(img,(0,0),0.6); img=(img*0.82).astype(np.uint8)
    def P(lo,la): return ll(lo,la,lonc,latc,k,W,H)
    ov=img.copy()
    # breeding zones (gold): Himalayan foothills curve, central hills, Western Ghats
    foot=[P(74.0,31.8),P(77,30.4),P(80,29.2),P(83,27.9),P(86,27.2),P(88.5,27.0)]
    cen=[(P(78.5+4.6*math.cos(a),22.4+1.8*math.sin(a))) for a in np.linspace(0,2*math.pi,40)]
    wg=[P(73.9,20.0),P(74.4,17.5),P(75.0,14.5),P(76.0,12.0)]
    a1=ease(seg(lt,1.0,2.4))
    o2=ov.copy()
    cv2.polylines(o2,[np.array(foot,np.int32)],False,(255,200,70),34,cv2.LINE_AA); cv2.fillPoly(o2,[np.array(cen,np.int32)],(255,200,70)); cv2.polylines(o2,[np.array(wg,np.int32)],False,(255,200,70),26,cv2.LINE_AA)
    ov=cv2.addWeighted(ov,1-0.32*a1,o2,0.32*a1,0)
    # winter zone (cyan): south peninsula + Sri Lanka
    a2=ease(seg(lt,3.2,4.6)); o3=ov.copy()
    south=[P(75.2,14.8),P(78.6,14.0),P(80.4,13.0),P(79.8,10.2),P(78.0,8.2),P(76.2,9.0),P(75.0,12.0)]
    cv2.fillPoly(o3,[np.array(south,np.int32)],(70,225,235)); sl=P(80.7,7.6); cv2.circle(o3,(int(sl[0]),int(sl[1])),26,(70,225,235),-1,cv2.LINE_AA)
    ov=cv2.addWeighted(ov,1-0.32*a2,o3,0.32*a2,0)
    fr=ov
    # migration arrows: north (summer) and south (Oct-Nov)
    def arrow(a,b,col,u0,u1):
        u=ease(seg(lt,u0,u1)); 
        if u<=0: return
        e=(lerp(a[0],b[0],u),lerp(a[1],b[1],u)); cv2.arrowedLine(fr,(int(a[0]),int(a[1])),(int(e[0]),int(e[1])),col,9,cv2.LINE_AA,tipLength=0.12)
    arrow(P(78.5,12.5),P(80.0,21.2),(255,230,140),1.5,3.0)
    arrow(P(82.0,28.0),P(79.5,13.5),(120,235,245),4.4,6.0)
    # labels
    pill(fr,"BREEDS: JUN TO AUG",P(81.5,26.4)[0]-0,P(81.5,26.4)[1]-70,ease(seg(lt,1.6,2.0)),size=40,fg=(20,16,8),bg=GOLD)
    pill(fr,"WINTER: SOUTH",P(77.0,9.2)[0]-150,P(77.0,9.2)[1]+70,ease(seg(lt,3.6,4.0)),size=40,fg=(10,24,28),bg=(70,225,235))
    gradv(fr,0,560,0.75,0.0); gradv(fr,1500,H,0.0,0.7)
    kt(fr,"A MONSOON BIRD",anton(100),WHITE,W/2,170,t,21.2,hold_end=26.9,sw=8,glow=(0,160,200)); 
    kt(fr,"Breeds in the rains. Heads south for winter.",bcs(54),CREAM,W/2,310,t,22.6,hold_end=26.9,sw=5)
    pill(fr,"SCHEMATIC. RANGE IS APPROXIMATE.",W/2,1790,0.9,size=30,fg=(225,225,225),bg=(14,24,30))
    vs=int((t*200)%(H+200)-100); o=np.zeros((H,W,3),np.float32); cv2.line(o,(0,vs),(W,vs),(120,255,250),3); o=cv2.GaussianBlur(o,(0,0),12)*2.2; add(fr,o,0.10)
    # rain streaks (monsoon)
    rng=np.random.default_rng(int(t*30)%97); 
    for _ in range(40):
        x=int(rng.uniform(0,W)); y=int(rng.uniform(0,H)); cv2.line(fr,(x,y),(x-6,y+34),(210,225,235),1,cv2.LINE_AA)
    hud_corners(fr,50,200,W-50,H-250,CYAN,0.55)
    return fr
def frame(t):
    if 21.0<=t<27.5:
        fr=mapscene(t)
    else:
        win,M,ts,clip=footage(t); fr=bgfrom(win); fr[WY:WY+WH]=win
        cv2.rectangle(fr,(0,WY-3),(W,WY),(255,200,70),3); cv2.rectangle(fr,(0,WY+WH),(W,WY+WH+3),(255,200,70),3)
        gradv(fr,0,WY,0.65,0.25); gradv(fr,WY+WH,H,0.25,0.7)
        # ---- text by beat
        kt(fr,"WHAT IS IT HIDING",anton(88),WHITE,W/2,150,t,0.15,hold_end=2.9,sw=8,glow=(0,0,0)); kt(fr,"UNDER THE FLUFF?",anton(100),GOLD,W/2,265,t,0.5,hold_end=2.9,sw=8,glow=(255,150,0))
        kt(fr,"FRONT VIEW",anton(100),WHITE,W/2,120,t,3.1,hold_end=8.8,sw=8,glow=(0,0,0)); kt(fr,"Looks simple. Count the colours.",bcs(54),CREAM,W/2,235,t,3.5,hold_end=8.8,sw=5)
        kt(fr,"NOW TURN IT AROUND",anton(90),GOLD,W/2,150,t,9.1,hold_end=14.8,sw=8,glow=(255,150,0)); kt(fr,"Emerald back. Electric-blue rump.",bcs(56),CREAM,W/2,265,t,9.8,hold_end=14.8,sw=5)
        kt(fr,"BUT IT HUNTS",anton(96),WHITE,W/2,140,t,15.1,hold_end=20.8,sw=8,glow=(0,0,0)); kt(fr,"ON THE GROUND",anton(96),(110,225,255),W/2,255,t,15.5,hold_end=20.8,sw=8,glow=(0,160,200))
        # beak-ring + caption in hunter beat
        if 15.0<=t<21.0:
            mp=mouthring(fr,M,ts,t)
            if mp and 18.3<=t<19.0:
                x,y=mp; q=(t*1.4)%1; ring(fr,x,y,30+q*60,(255,235,150),(1-q)*0.9,4); cv2.circle(fr,(int(x),int(y)),8,(255,240,170),-1,cv2.LINE_AA)
            kt(fr,"Flips leaf litter. Ants, termites, snails.",bcs(54),CREAM,W/2,1730,t,16.2,hold_end=20.8,sw=5)
        # swatches
        if t<27.0:
            a=ease(seg(t,3.3,3.8))*(1-ease(seg(t,20.8,21.0)))
            if a>0.02 and not (15.0<=t<21.0):
                n=swatches(fr,t)
                kt(fr,(f"{n} COLOUR" if n==1 else f"{n} COLOURS"),anton(66),GOLD,W/2,1700,t,3.8,hold_end=14.8,sw=6,glow=(255,150,0),glitch=False) if n>0 else None
        if t>=27.5:
            swatches(fr,t,final=True)
            kt(fr,"NAVRANG",anton(190),GOLD,W/2,150,t,27.7,hold_end=33.6,sw=11,glow=(255,150,0))
            kt(fr,"NINE COLOURS. ONE SMALL BIRD.",bcs(66),WHITE,W/2,290,t,28.5,hold_end=33.6,sw=6)
            kt(fr,"Which side surprised you more?",bcs(56),CREAM,W/2,1722,t,30.0,hold_end=33.6,sw=5)
            kt(fr,"THE NATURAL ANGLE",anton(52),GOLD,W/2,1870,t,31.2,hold_end=33.6,sw=5,glow=(255,150,0))
        if 9.0<=t<9.8: pass
    # transition polish
    for tb in (3.0,9.0,15.0,21.0,27.5):
        d=t-tb
        if 0<=d<0.35: fr=np.clip(fr.astype(np.float32)+255*(1-d/0.35)**2*0.35,0,255).astype(np.uint8)
    fade(fr,1-ease(seg(t,0,0.35))); fade(fr,ease(seg(t,TOTAL-0.7,TOTAL)))
    HITS=[(0.2,0.8),(3.1,0.5),(9.1,0.8),(15.1,0.5),(17.3,0.6),(21.2,0.6),(27.7,0.8)]
    fr=punch(fr,t,HITS); return look(fr,t,HITS)
if __name__=="__main__":
    ts=[float(x) for x in sys.argv[2:]]; tiles=[]
    for t in ts:
        f=cv2.resize(frame(t),(270,480)); cv2.putText(f,f"{t}",(6,24),0,0.7,(255,255,0),2); tiles.append(f)
    cols=8; rows=(len(tiles)+cols-1)//cols; img=np.zeros((rows*480,cols*270,3),np.uint8)
    for i,f in enumerate(tiles): img[(i//cols)*480:(i//cols+1)*480,(i%cols)*270:(i%cols+1)*270]=f
    cv2.imwrite(sys.argv[1],cv2.cvtColor(img,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,88])
