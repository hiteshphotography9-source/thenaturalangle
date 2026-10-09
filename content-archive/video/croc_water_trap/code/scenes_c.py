import sys, math
sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pil')
from eng import *
HERE_C="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/croc/"
NF=667; TOTAL=26.6
_C={}
def src(i):
    i=max(1,min(NF,int(i)))
    if i not in _C:
        if len(_C)>60: _C.pop(next(iter(_C)))
        _C[i]=cv2.cvtColor(cv2.imread(HERE_C+f"crop/c_{i:04d}.jpg"),cv2.COLOR_BGR2RGB)
    return _C[i]
def srcf(ts):
    """frame at fractional source time (seconds), blended between neighbours"""
    f=ts*30+1; a=int(math.floor(f)); u=f-a
    A=src(a)
    if u<0.02: return A
    B=src(a+1); return cv2.addWeighted(A,1-u,B,u,0)
# clips: (new_start,new_end, src_start, src_end)
CL=[(0.0,2.2,16.9,18.3),(2.2,6.7,0.3,4.8),(6.7,12.7,6.0,12.0),(12.7,17.2,12.0,14.5),(17.2,22.2,15.0,20.0),(22.2,TOTAL,20.4,21.7)]
def n2s(t):
    for a,b,s0,s1 in CL:
        if a<=t<b+1e-6: return s0+(t-a)/(b-a)*(s1-s0),(a,b)
    return CL[-1][3],(CL[-1][0],CL[-1][1])
WY0,WH=450,1000   # window y, height
def keyz(t):
    # zoom keys on crop coords: (t, zoom, cx, cy)
    K=[(0,1.0,540,500),(2.2,1.0,540,500),(6.7,1.0,540,500),(8.4,1.35,400,430),(12.6,1.45,380,430),(13.0,1.2,520,450),(16.8,1.1,540,470),(17.4,1.0,540,500),(22.0,1.0,540,500),(TOTAL,1.12,540,500)]
    if t<=K[0][0]: return K[0][1:]
    for a,b in zip(K[:-1],K[1:]):
        if a[0]<=t<=b[0]:
            e=ease((t-a[0])/(b[0]-a[0])); return tuple(lerp(x,y,e) for x,y in zip(a[1:],b[1:]))
    return K[-1][1:]
def window(t):
    s,_=n2s(t); fr=srcf(s); z,cx,cy=keyz(t)
    sw=1080/z; sh=1000/z; x0=min(max(cx-sw/2,0),1080-sw); y0=min(max(cy-sh/2,0),1000-sh)
    M=np.array([[z,0,-x0*z],[0,z,-y0*z]],np.float32)
    out=cv2.warpAffine(fr,M,(1080,1000),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
    # gentle grade: cooler shadows, slight contrast
    f=out.astype(np.float32); f=(f-128)*1.08+128; lum=f.mean(2,keepdims=True)/255; f=f+(1-lum)*np.array((-4,2,8),np.float32); f=np.clip(f,0,255).astype(np.uint8)
    return f,M,s
def mouth_win(M,s):
    # estimated mouth in crop coords (x,y) over source time
    P=[(5.0,(470,610)),(6.0,(300,430)),(8.0,(300,440)),(12.0,(300,445)),(14.5,(330,450)),(15.5,(470,400)),(17.5,(520,330)),(20.0,(380,430)),(21.0,(520,420))]
    for (ta,pa),(tb,pb) in zip(P[:-1],P[1:]):
        if ta<=s<=tb: u=(s-ta)/(tb-ta); p=(lerp(pa[0],pb[0],u),lerp(pa[1],pb[1],u)); break
    else: p=P[0][1] if s<P[0][0] else P[-1][1]
    return (M[0,0]*p[0]+M[0,2], M[1,1]*p[1]+M[1,2])
def bgfull(fr_win):
    big=cv2.resize(fr_win,(1080*2,1000*2)); H2=H; sc=H/1000.0
    b=cv2.resize(fr_win,(int(1080*sc),H)); x0=(b.shape[1]-W)//2; b=b[:,x0:x0+W]
    b=cv2.GaussianBlur(b,(0,0),38); return (b*0.28).astype(np.uint8)
# ---- illustration panel (bottom): flow carries fish into open jaws
PY0,PH=1500,290
def panel(fr,t,a):
    if a<=0.01: return
    ov=fr.copy()
    cv2.rectangle(ov,(40,PY0),(W-40,PY0+PH),(10,22,28),-1)
    # water flow lines
    for k in range(6):
        y=PY0+40+k*36
        pts=[]
        for x in range(60,W-60,14):
            pts.append((x,int(y+8*math.sin((x*0.02)-t*2.2+k))))
        cv2.polylines(ov,[np.array(pts,np.int32)],False,(70,140,160),2,cv2.LINE_AA)
    # jaws (side view, open) on right
    jx,jy=800,PY0+150
    up=np.array([[jx,jy-60],[jx+170,jy-34],[jx+250,jy-34],[jx+250,jy-12],[jx+170,jy-6],[jx,jy-6]],np.int32)
    lo=np.array([[jx,jy+6],[jx+170,jy+3],[jx+250,jy+16],[jx+250,jy+38],[jx+170,jy+30],[jx,jy+80]],np.int32)
    cv2.fillPoly(ov,[up],(40,56,48)); cv2.fillPoly(ov,[lo],(40,56,48)); cv2.polylines(ov,[up],True,(255,200,70),3,cv2.LINE_AA); cv2.polylines(ov,[lo],True,(255,200,70),3,cv2.LINE_AA)
    # fish drifting along current into jaws
    for i in range(4):
        q=((t*0.22)+i/4)%1.0
        x=lerp(90,jx+60,q); y=jy+30+20*math.sin(q*9+i*1.7)*(1-q)
        al=min(1,q*5)*min(1,(1-q)*6+0.2)
        body=np.array([[x-26,y],[x-8,y-12],[x+22,y-4],[x+22,y+4],[x-8,y+12]],np.int32); tail=np.array([[x-26,y],[x-44,y-12],[x-44,y+12]],np.int32)
        col=(235,215,90) if i%2==0 else (120,225,235)
        o2=ov.copy(); cv2.fillPoly(o2,[body],col); cv2.fillPoly(o2,[tail],col); ov=cv2.addWeighted(ov,1-al,o2,al,0)
    # arrows showing current
    for k in range(3):
        x=120+((t*60+k*220)%760); cv2.arrowedLine(ov,(int(x),PY0+PH-30),(int(x+70),PY0+PH-30),(130,230,250),4,cv2.LINE_AA,tipLength=0.4)
    fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
    paste(fr,sprite("CURRENT",bcs(32),(150,235,250),sw=3,shadow=False),150,PY0+PH-62,a)
    paste(fr,sprite("OPEN JAWS",bcs(32),GOLD,sw=3,shadow=False),jx+130,PY0+52,a)
    pill(fr,"ILLUSTRATION. NOT FROM THE FOOTAGE.",W/2,PY0-24,a,size=26,fg=(230,230,230),bg=(14,24,30))
def flow_arrows(fr,t,a):
    if a<=0.01: return
    for k in range(4):
        q=((t*0.6)+k/4)%1; sx=900-q*560; sy=WY0+170+q*290
        ov=fr.copy(); cv2.arrowedLine(ov,(int(sx+46),int(sy-46)),(int(sx),int(sy)),(130,230,250),5,cv2.LINE_AA,tipLength=0.35); fr[:]=(fr*(1-0.8*a)+ov*0.8*a).astype(np.uint8)
def tracker(fr,t,a):
    if a<=0.01: return
    labs=[("1  ARRIVES",2.2,6.7),("2  WAITS",6.7,12.7),("3  CURRENT DOES THE WORK",12.7,22.2)]
    xs=[150,420,800]
    for (lab,a0,a1),x in zip(labs,xs):
        on=a0<=t<a1
        pill(fr,lab,x,1850,a,size=34,fg=(20,16,8) if on else (190,200,205),bg=GOLD if on else (24,36,44))
def ring_arrows(fr,mp,t,a):
    if a<=0.01: return
    x,y=mp
    for j in range(3):
        q=((t*0.8)+j/3)%1; ring(fr,x,y,26+q*90,(110,230,250),(1-q)*0.8*a,4)
    cv2.circle(fr,(int(x),int(y)),9,(255,240,170),-1,cv2.LINE_AA)
    for k in range(4):   # flow arrows toward mouth, from upper right
        q=((t*0.7)+k/4)%1; sx=x+340-q*320; sy=y-340+q*320
        cv2.arrowedLine(fr,(int(sx+46),int(sy-46)),(int(sx),int(sy)),(130,230,250),5,cv2.LINE_AA,tipLength=0.35)
S_LAYER={}
def frame(t):
    win,M,s=window(t); fr=bgfull(win)
    # window with soft border
    fr[WY0:WY0+WH]=win
    cv2.rectangle(fr,(0,WY0-3),(W,WY0),(255,200,70),3); cv2.rectangle(fr,(0,WY0+WH),(W,WY0+WH+3),(255,200,70),3)
    gradv(fr,0,WY0,0.7,0.2); 
    mp=mouth_win(M,s); mp=(mp[0],mp[1]+WY0)
    flow_arrows(fr,t,ease(seg(t,7.0,7.6))*(1-ease(seg(t,21.6,22.2))))
    panel(fr,t,ease(seg(t,8.0,8.6))*(1-ease(seg(t,21.6,22.2))))
    tracker(fr,t,ease(seg(t,2.2,2.8))*(1-ease(seg(t,22.0,22.4))))
    # ---- text (top zone only, below top 450)
    kt(fr,"HAVE YOU SEEN",bcs(90),CREAM,W/2,170,t,0.15,hold_end=2.0,sw=6); kt(fr,"A CROCODILE HUNT LIKE THIS?",anton(88),GOLD,W/2,300,t,0.45,hold_end=2.0,sw=8,glow=(255,150,0))
    kt(fr,"IT DOES NOT CHASE.",anton(120),WHITE,W/2,215,t,2.4,hold_end=6.5,sw=8,glow=(0,0,0)); kt(fr,"It arrives at the water's edge.",bcs(58),CREAM,W/2,350,t,3.2,hold_end=6.5,sw=5)
    kt(fr,"IT WAITS.",anton(150),GOLD,W/2,200,t,6.9,hold_end=12.5,sw=9,glow=(255,150,0)); kt(fr,"Jaws in the fastest part of the flow.",bcs(58),CREAM,W/2,345,t,7.7,hold_end=12.5,sw=5)
    kt(fr,"THE WATER",anton(118),WHITE,W/2,165,t,12.9,hold_end=17.0,sw=8,glow=(0,0,0)); kt(fr,"IS THE TRAP.",anton(118),(110,225,255),W/2,300,t,13.4,hold_end=17.0,sw=8,glow=(0,160,200))
    kt(fr,"LET THE CURRENT",anton(100),WHITE,W/2,185,t,17.4,hold_end=22.0,sw=8,glow=(0,0,0)); kt(fr,"DO THE WORK.",anton(120),GOLD,W/2,325,t,17.9,hold_end=22.0,sw=8,glow=(255,150,0))
    kt(fr,"THE NATURAL ANGLE",anton(100),GOLD,W/2,220,t,22.5,sw=8,glow=(255,150,0)); 
    paste(fr,sprite("Full video on my channel",bcs(58),CREAM,sw=5),W/2,350,ease(seg(t,23.0,23.4)))
    if t>=22.4:
        pill(fr,"CROCODILE BEHAVIOUR: WATER TRAP",W/2,1560,ease(seg(t,22.6,23.0)),size=40,fg=(20,16,8),bg=GOLD)
    motes(fr,t,0.25)
    fade(fr,1-ease(seg(t,0,0.4))); fade(fr,ease(seg(t,TOTAL-0.8,TOTAL)))
    HITS=[(0.2,0.8),(2.4,0.5),(6.9,0.6),(12.9,0.6),(17.4,0.6),(17.5,0.5),(21.0,0.6),(22.5,0.5)]
    fr=punch(fr,t,HITS); return look(fr,t,HITS)
if __name__=="__main__":
    ts=[float(x) for x in sys.argv[2:]]; tiles=[]
    for t in ts:
        f=cv2.resize(frame(t),(270,480)); cv2.putText(f,f"{t}",(6,24),0,0.7,(255,255,0),2); tiles.append(f)
    cols=8; rows=(len(tiles)+cols-1)//cols; img=np.zeros((rows*480,cols*270,3),np.uint8)
    for i,f in enumerate(tiles): img[(i//cols)*480:(i//cols+1)*480,(i%cols)*270:(i%cols+1)*270]=f
    cv2.imwrite(sys.argv[1],cv2.cvtColor(img,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,88])
