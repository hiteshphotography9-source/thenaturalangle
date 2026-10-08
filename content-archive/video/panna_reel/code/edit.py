import sys; sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/vid/v2')
from eng import *
SRC="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pn/src/"
DUR=56.1667; NF=1685
_C={}
def src(t):
    n=min(NF,max(1,int(round(t*30))+1))
    if n not in _C:
        if len(_C)>40: _C.pop(next(iter(_C)))
        _C[n]=cv2.cvtColor(cv2.imread(SRC+f"s_{n:04d}.jpg"),cv2.COLOR_BGR2RGB)
    return _C[n]
def zoomcrop(fr,z,cx=0.5,cy=0.5,rot=0.0,sx=0,sy=0):
    if z==1.0 and rot==0 and sx==0 and sy==0: return fr
    xc=cx*W; yc=cy*H; M=cv2.getRotationMatrix2D((xc,yc),rot,z); M[0,2]+=sx; M[1,2]+=sy
    return cv2.warpAffine(fr,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
# ---------- shot plan: (t0,t1,srcmap,fn) ; zoom jumps
def jumpzoom(t,t0,t1,period=2.1,amts=(1.0,1.16,1.06,1.22),cxs=(0.5,0.35,0.6,0.45),cys=(0.5,0.62,0.45,0.58),creep=0.05):
    k=int((t-t0)/period); k=min(k,99); p=((t-t0)-k*period)/period
    return amts[k%len(amts)]*(1+creep*p), cxs[k%len(cxs)], cys[k%len(cys)], k, (t-t0)-k*period
CUTS=[3.8,9.6,14.75,16.87,24.2,27.27,33.17,36.0,38.03,39.4,42.03,48.77,52.9]
def base(t):
    """returns frame and zoom info for the source video with re-edit"""
    ts=t
    if 0<=t<0.8: ts=34.5+t*0.5     # cold open: tiger C face
    elif 0.8<=t<1.6: ts=21.0+(t-0.8)*0.4   # jeep chaos
    elif 1.6<=t<2.4: ts=1.2+(t-1.6)*0.4      # tiger A
    elif 2.4<=t<3.8: ts=t-0.0
    elif 44.3<=t<48.77: ts=0.3+(t-44.3)*0.72
    fr=src(ts)
    if t<2.4: z=1.08+0.06*((t%0.8)/0.8); fr=zoomcrop(fr,z,0.5,0.5)
    elif 3.8<=t<24.2:
        z,cx,cy,k,pp=jumpzoom(t,3.8,24.2,2.4,(1.0,1.2,1.08,1.28),(0.5,0.3,0.55,0.4),(0.5,0.5,0.45,0.5)); fr=zoomcrop(fr,z,cx,cy)
    elif 24.2<=t<39.4:
        z,cx,cy,k,pp=jumpzoom(t,24.2,39.4,2.2,(1.0,1.17,1.06,1.25),(0.4,0.3,0.45,0.35),(0.55,0.55,0.5,0.5)); fr=zoomcrop(fr,z,cx,cy)
    elif 39.4<=t<52.9:
        z,cx,cy,k,pp=jumpzoom(t,39.4,52.9,2.3,(1.0,1.15,1.05),(0.5,0.4,0.55),(0.5,0.5,0.6)); fr=zoomcrop(fr,z,cx,cy)
    elif t>=52.9:
        z=1.0+0.1*seg(t,52.9,56.2); fr=zoomcrop(fr,z,0.45,0.6)
    return fr
# ---------- text captions (own timeline)
CAPS=[(2.4,4.4,"TOURIST vs","PHOTOGRAPHER.",WHITE,GOLD),(4.4,9.55,"THREE","TIGERS.",WHITE,GOLD),(9.6,15.0,"TWO TOGETHER.","ONE ALONE.",WHITE,CYAN),(15.0,23.9,"THEN IT","GOT HARD.",WHITE,RED),(23.9,32.0,"EVERY ANGLE","WAS BLOCKED.",WHITE,RED),(32.0,39.3,"WORD SPREAD.","EVERY JEEP CAME RUNNING.",WHITE,GOLD),(39.4,42.0,"THE REAL","CHALLENGE BEGAN.",WHITE,GOLD),(42.0,48.7,"AUTOFOCUS KEPT","GRABBING THE BRANCHES.",WHITE,RED),(48.8,52.85,"IT'S NOT LUCK.","IT'S TECHNIQUE.",WHITE,(120,255,160))]
CHAP=[(0,15.0,"1  THE SIGHTING"),(15.0,39.4,"2  THE CROWD"),(39.4,56.2,"3  THE TECHNIQUE")]
def captions(fr,t):
    for (a,b,l1,l2,c1,c2) in CAPS:
        if a<=t<b+0.001:
            f1=anton(118 if len(l1)<12 else 96); f2=anton(150 if len(l2)<12 else (104 if len(l2)<20 else 84))
            kt(fr,l1,f1,c1,W/2,380,t,a,hold_end=b-0.05,sw=8,glow=(0,0,0)); 
            kt(fr,l2,f2,c2,W/2,530,t,a+0.16,hold_end=b-0.05,sw=8,glow=((255,170,30) if c2==GOLD else (0,0,0)))
def plate(fr,t):
    # cover original caption zone with blurred dark plate + HUD info
    y0=1370
    reg=fr[y0:H].copy(); bl=cv2.GaussianBlur(reg,(0,0),30); g=bl.mean(2,keepdims=True); bl=((g*0.6+bl*0.4)*0.22).astype(np.uint8)
    m=np.ones((H-y0,1,1),np.float32)
    for i in range(36): m[i]=i/36
    fr[y0:H]=(reg*(1-m)+bl*m).astype(np.uint8)
    # chapter chip
    ch=[c for c in CHAP if c[0]<=t<c[1]+0.01][0][2] if t<DUR else CHAP[-1][2]
    pill(fr,ch,W/2,1560,1.0,fg=(20,16,8),bg=GOLD,size=46)
    paste(fr,sprite("THE NATURAL ANGLE",bcs(46),CREAM,sw=3),W/2,1660,1.0)
    # progress bar
    p=t/DUR; cv2.rectangle(fr,(80,1730),(W-80,1738),(60,60,60),-1); cv2.rectangle(fr,(80,1730),(int(80+(W-160)*p),1738),GOLD,-1)
    for tb in (15.0,39.4): x=int(80+(W-160)*tb/DUR); cv2.rectangle(fr,(x-2,1722),(x+2,1746),WHITE,-1)
def afbox(fr,cx,cy,s,col,a=1.0,w=6):
    ov=fr.copy(); L=int(s*0.28)
    for (sx,sy) in ((-1,-1),(1,-1),(-1,1),(1,1)):
        x=int(cx+sx*s/2); y=int(cy+sy*s/2); cv2.line(ov,(x,y),(x-sx*L,y),col,w,cv2.LINE_AA); cv2.line(ov,(x,y),(x,y-sy*L),col,w,cv2.LINE_AA)
    cv2.circle(ov,(int(cx),int(cy)),5,col,-1,cv2.LINE_AA); fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
HUNT=[(0.18,0.20),(0.72,0.28),(0.35,0.42),(0.80,0.50),(0.22,0.58),(0.60,0.35),(0.45,0.22)]
def overlays(fr,t):
    if 2.4<=t<3.8: pass
    # 4.4-9.5 outline on visible tiger (tiger B stripes)
    if 4.5<=t<9.5:
        a=ease(seg(t,4.5,5.0)); cx,cy=W*0.28,H*0.43; pul=1+0.04*math.sin(t*6)
        ov=fr.copy(); cv2.ellipse(ov,(int(cx),int(cy)),(int(300*pul),int(130*pul)),-8,0,360,GOLD,6,cv2.LINE_AA); fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
        pill(fr,"TIGER",W*0.30,H*0.43+190,a,size=54)
    if 9.7<=t<15.0:
        a=ease(seg(t,9.7,10.1)); ov=fr.copy(); cv2.ellipse(ov,(int(W*0.32),int(H*0.40)),(int(340),int(150)),-8,0,360,CYAN,6,cv2.LINE_AA); fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
        pill(fr,"2 TOGETHER",W*0.34,H*0.40+200,a,size=54,bg=CYAN)
        a2=ease(seg(t,11.6,12.0)); pill(fr,"1 ALONE",W*0.70,1230,a2,size=54,bg=GOLD)
    # crowd: red pulses
    if 15.0<=t<23.9:
        a=0.25+0.15*math.sin(t*8); gradv(fr,0,H,0.0,0.0); ov=np.zeros_like(fr,np.float32); ov[:,:,0]=255*a*0.35; add(fr,ov,0.6*ease(seg(t,15.0,15.4)))
        n=int(min(1,seg(t,15.3,22.5))*9); 
        paste(fr,sprite("VIEW BLOCKED",bcs(54),(255,200,190),sw=4,glow=(255,40,30),glow_r=8),W/2,890,0.0)
    if 24.0<=t<32.0:
        a=ease(seg(t,24.0,24.5)); 
        for k in range(5):
            x=(k*0.23+0.1)*W; y0=(0.02+0.12*((k*3)%4)) * H; ov=fr.copy(); cv2.line(ov,(int(x),int(y0)),(int(x+60),int(y0+260)),RED,5,cv2.LINE_AA); fr[:]=(fr*(1-a*0.5)+ov*a*0.5).astype(np.uint8)
        afbox(fr,W*0.30,H*0.62,300,RED,a,6); pill(fr,"OBSTRUCTED",W*0.30,H*0.62-230,a,fg=WHITE,bg=RED,size=50)
    if 33.0<=t<39.3:
        n=int(min(1,seg(t,36.0,38.8))*14); a=ease(seg(t,36.1,36.5))
        if a>0:
            pill(fr,"JEEPS ARRIVING",W/2,900,a,size=58,fg=WHITE,bg=RED)
    # autofocus hunting
    if 44.4<=t<48.77:
        k=int((t-44.4)*5.5); p=((t-44.4)*5.5)%1; i0=HUNT[k%len(HUNT)]; i1=HUNT[(k+1)%len(HUNT)]; e=ease(p*1.6)
        cx=lerp(i0[0],i1[0],e)*W; cy=lerp(i0[1],i1[1],e)*(H*0.7); sz=300+40*math.sin(t*20)
        afbox(fr,cx,cy,sz,RED,1.0,7)
        if int(t*5.5)%2==0: pill(fr,"AF: BRANCH",cx,cy-sz/2-50,1.0,fg=WHITE,bg=RED,size=48)
        if (t*5.5)%1<0.12: fade(fr,0.0)
    if 48.8<=t<52.9:
        p=seg(t,48.8,49.3); cx=lerp(0.6*W,0.40*W,eo3(p)); cy=lerp(0.35*H,0.67*H,eo3(p)); sz=lerp(320,470,eo3(p))
        afbox(fr,cx,cy,sz,(60,255,130),1.0,8)
        pill(fr,"LOCKED",cx,cy-sz/2-56,ease(seg(t,49.1,49.4)),fg=(10,30,10),bg=(60,255,130),size=56)
        flare(fr,cy,0.7*math.exp(-(t-49.2)*5)*(t>=49.2))
    if t>=52.9:
        a=ease(seg(t,53.2,53.7)); gradv(fr,0,H,0.0,0.0)
        kt(fr,"MORE FIELDCRAFT ON",bcs(70),CREAM,W/2,330,t,53.2,sw=5,glow=(0,0,0)); kt(fr,"THE NATURAL",anton(150),GOLD,W/2,470,t,53.5,sw=8,glow=(255,150,0)); kt(fr,"ANGLE",anton(150),WHITE,W/2,620,t,53.7,sw=8,glow=(255,150,0),tex=None)
        pill(fr,"FOLLOW FOR MORE",W/2,780,ease(seg(t,54.3,54.7)),size=44)
def split_open(t):
    # 2.4-3.8 split screen: top jeeps, bottom tiger
    p=seg(t,2.4,2.7); h=int(H*0.5*eo3(p)) if False else None
def frame(t):
    fr=base(t).copy()
    if 2.4<=t<3.8:
        top=src(21.0+(t-2.4)*0.3); bot=src(33.0+(t-2.4)*0.3)
        z1=zoomcrop(top,1.12,0.5,0.5); z2=zoomcrop(bot,1.12,0.4,0.5)
        s=eo3(seg(t,2.4,2.65)); hh=int(H*0.5)
        fr=fr.copy(); fr[:hh]=cv2.resize(z1[int(H*0.15):int(H*0.15)+hh*1] if False else z1[::2][:hh] if False else cv2.resize(z1,(W,H))[int(H*0.25):int(H*0.75)],(W,hh)); fr[hh:]=cv2.resize(cv2.resize(z2,(W,H))[int(H*0.25):int(H*0.75)],(W,H-hh))
        cv2.rectangle(fr,(0,hh-4),(W,hh+4),GOLD,-1)
        paste(fr,sprite("TOURIST",anton(110),WHITE,sw=7,glow=(0,0,0)),W/2,hh-110,s); paste(fr,sprite("PHOTOGRAPHER",anton(110),GOLD,sw=7,glow=(255,150,0)),W/2,hh+110,s)
    elif t>=3.8 or t<2.4: pass
    # grade
    if t<2.4: 
        pass
    # shake in crowd
    if 15.0<=t<23.9: fr=zoomcrop(fr,1.0,0.5,0.5,0,int(3*math.sin(t*37)),int(3*math.cos(t*31)))
    # mild contrast boost for original footage
    fr=np.clip((fr.astype(np.float32)-128)*1.08+128+4,0,255).astype(np.uint8)
    gradv(fr,0,620,0.45,0.0)
    if t>=2.4 or t>=0: motes(fr,t,0.5)
    if t>=2.4 and not (2.4<=t<3.8): captions(fr,t)
    overlays(fr,t)
    plate(fr,t)
    if t<2.4:
        kt(fr,"TOURIST",anton(190),WHITE,W/2,420,t,1.0,hold_end=2.35,sw=9,glow=(0,0,0)) if t>=1.0 else None
        if t>=1.6: kt(fr,"vs PHOTOGRAPHER",anton(110),GOLD,W/2,590,t,1.6,hold_end=2.35,sw=8,glow=(255,150,0))
    # transitions at cuts
    for tb in (0.8,1.6,2.4,3.8,9.6,14.75,16.87,24.2,27.27,33.17,36.0,38.03,39.4,42.03,44.3,48.77,52.9):
        dt=t-tb
        if 0<=dt<0.16: fr=np.clip(fr.astype(np.float32)+255*(1-dt/0.16)**2*0.55,0,255).astype(np.uint8)
    fr=punch(fr,t,HITS)
    return look(fr,t,HITS)
HITS=[(0.0,1.0),(0.8,0.9),(1.6,0.9),(2.4,1.2),(3.8,1.2),(4.4,0.8),(9.6,0.8),(15.0,1.2),(16.87,0.8),(23.9,1.2),(24.2,0.8),(27.27,0.8),(32.0,0.9),(36.0,1.0),(39.4,1.2),(42.0,0.9),(44.4,0.9),(48.8,1.3),(52.9,1.4),(53.5,0.7)]
if __name__=="__main__":
    ts=[float(x) for x in sys.argv[1:]]
    for t in ts: cv2.imwrite(f"/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pn/e_{t:05.1f}.jpg",cv2.cvtColor(frame(t),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,88])
