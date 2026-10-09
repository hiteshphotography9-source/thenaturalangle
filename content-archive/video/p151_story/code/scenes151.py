import sys, json, math
sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/pnv')
import scenes as B
from scenes import *
DUR=132.6
B.SUB[17]=(0.53,0.67,0.70,0.81)
def place(n,s,fx,fy,xf=0.5,yf=0.5,dim=0.95,blurbg=True):
    """sharp photo scaled s, focus (fx,fy normalised) at frame (xf*W,yf*H) over blurred cover bg. returns frame, subject rect"""
    im=ph(n); ih,iw=im.shape[:2]
    out=B._cover_bg(n).astype(np.float32)
    M=np.array([[s,0,xf*W-fx*iw*s],[0,s,yf*H-fy*ih*s]],np.float32)
    mid=cv2.warpAffine(im,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0))
    fa=cv2.warpAffine(B._feather(iw,ih,int(70/max(s,0.2))),M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=0)[:,:,None]
    out=out*(1-fa)+mid.astype(np.float32)*dim*fa
    x0,x1,y0,y1=B.SUB[n]; rect=(int(M[0,0]*x0*iw+M[0,2]),int(M[1,1]*y0*ih+M[1,2]),int(M[0,0]*x1*iw+M[0,2]),int(M[1,1]*y1*ih+M[1,2]))
    m=np.zeros((H,W),bool); m[max(rect[1],0):max(rect[3],0),max(rect[0],0):max(rect[2],0)]=True; B.LASTA=m
    return np.clip(out,0,255).astype(np.uint8)
def zoom_s(p,s0,s1): return s0*(s1/s0)**ease(p)
def pillnote(fr,t,a,b,text="ILLUSTRATIVE PHOTOS. NOT ALL FRAMES SHOW P-151.",y=1835):
    if a<=t<=b: pill(fr,text,W/2,y,min(ease(seg(t,a,a+0.4)),1-ease(seg(t,b-0.4,b))),size=27,fg=(225,225,225),bg=(14,24,30))
# ---------- scenes (times = final VO seconds)
def S1(t):  # 0 - 5.7  wide river, 2023 date
    p=seg(t,0,5.7); fr=place(17,zoom_s(p,0.50,0.62),0.5,0.62,yf=0.52)
    bands(fr,0.7,0.7,720,1250); motes(fr,t,0.3)
    kt(fr,"1 FEBRUARY 2023",anton(118),WHITE,W/2,330,t,0.85,hold_end=5.5,sw=8,glow=(255,150,0))
    kt(fr,"PANNA'S FIRST TIGRESS, T1",bcs(70),CREAM,W/2,1500,t,2.85,hold_end=5.5,sw=6)
    kt(fr,"HAS DIED.",anton(110),RED,W/2,1640,t,4.2,hold_end=5.5,sw=8,glow=(255,40,30)) if False else None
    return fr
def S2(t):  # 5.7 - 13.0 next day, P-151 with four cubs
    p=seg(t,5.7,13.0); fr=fit(24,p,hfrac=0.30,yfrac=0.50,push=0.08,dim=0.95,par=False,wmax=0.95)
    bands(fr,0.66,0.7,660,1250); motes(fr,t,0.3)
    kt(fr,"NEXT DAY",bcs(84),CREAM,W/2,300,t,6.0,hold_end=7.4,sw=6)
    kt(fr,"HER DAUGHTER",bcs(84),CREAM,W/2,300,t,7.55,hold_end=9.3,sw=6) if False else None
    kt(fr,"P-151",anton(220),GOLD,W/2,420,t,7.5,hold_end=12.5,sw=11,glow=(255,150,0))
    kt(fr,"WITH 4 CUBS",anton(120),WHITE,W/2,1580,t,9.7,hold_end=12.6,sw=8,glow=(0,0,0))
    pillnote(fr,t,6.3,12.6)
    return fr
def S3(t):  # 13.0 - 16.1
    p=seg(t,13.0,16.1); fr=fit(25,p,hfrac=0.30,yfrac=0.50,push=0.08,dim=0.95,par=False,wmax=0.88)
    bands(fr,0.6,0.65,660,1250); motes(fr,t,0.3); return fr
def S4(t):  # 16.1 - 23.5 map: T1 from Bandhavgarh, no tigers
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
    vscan(fr,t); hud_corners(fr,50,200,W-50,H-250,CYAN,0.6); return fr
def S5(t):  # 23.5 - 33.0  13 cubs, one of them P-151
    p=seg(t,23.5,33.2); fr=fit(28,p,hfrac=0.30,yfrac=0.46,push=0.08,dim=0.9,par=True)
    bands(fr,0.7,0.75,640,1180); motes(fr,t,0.3)
    kt(fr,"IN HER LIFE, T1 HAD",bcs(66),CREAM,W/2,270,t,23.9,hold_end=29.2,sw=5)
    v=count(t,24.6,26.6,13); 
    if t>=24.4: kt(fr,f"{v} CUBS",anton(200),GOLD,W/2,430,t,24.4,hold_end=33.0,sw=10,glow=(255,150,0),glitch=False)
    # 13 dots, one highlighted P-151
    x0=W/2-6*66
    for i in range(13):
        ti=25.2+i*0.12
        if t<ti: continue
        a=ease(seg(t,ti,ti+0.2)); col=(255,200,70)
        if i==12 and t>=30.5: col=(80,235,240); r=26+int(8*math.sin((t-30.5)*6))
        else: r=22
        ov=fr.copy(); cv2.circle(ov,(int(x0+i*66),1640),r,col,-1,cv2.LINE_AA); cv2.circle(ov,(int(x0+i*66),1640),r,(255,255,255),3,cv2.LINE_AA); fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
    if t>=30.5: paste(fr,sprite("ONE OF THEM: P-151",bcs(62),(80,235,240),sw=5,glow=(0,160,200)),W/2,1745,ease(seg(t,30.5,30.9)))
    return fr
def S6(t):  # 33.0 - 44.2  Ken river, both banks
    p=seg(t,33.0,44.2); fr=fit(29,p,hfrac=0.28,yfrac=0.50,push=0.08,dim=0.95,wmax=0.95)
    bands(fr,0.66,0.7,660,1250); motes(fr,t,0.3)
    kt(fr,"KEN RIVER",anton(150),(110,225,255),W/2,300,t,33.5,hold_end=37.2,sw=9,glow=(0,160,200)); kt(fr,"MADLA FOREST",bcs(76),WHITE,W/2,450,t,34.4,hold_end=37.2,sw=6)
    kt(fr,"TERRITORY ON",bcs(76),CREAM,W/2,300,t,37.5,hold_end=43.8,sw=6); kt(fr,"BOTH BANKS",anton(150),GOLD,W/2,450,t,38.0,hold_end=43.8,sw=9,glow=(255,150,0))
    return fr
def S7(t):  # 44.2 - 54.7 (mother's duty) visuals only
    p=seg(t,44.2,54.7); 
    fr=fit(26,p,hfrac=0.34,yfrac=0.50,push=0.08,dim=0.95,par=False,wmax=0.95) if t<49.5 else fit(28,seg(t,49.5,54.7),hfrac=0.30,yfrac=0.50,push=0.08,dim=0.95,par=True)
    bands(fr,0.6,0.66,660,1250); motes(fr,t,0.3); return fr
def S8(t):  # 54.7 - 58.9  one, two, four
    p=seg(t,54.7,58.9); fr=fit(24,p,hfrac=0.28,yfrac=0.46,push=0.06,dim=0.92,par=False,wmax=0.95)
    bands(fr,0.66,0.72,650,1220); motes(fr,t,0.3)
    for val,t0,t1,lab in ((1,55.15,56.5,"CUB"),(2,56.55,57.4,"CUBS"),(4,57.45,58.9,"CUBS")):
        if t0<=t<t1+0.15: kt(fr,str(val),anton(380),GOLD,W/2,1520,t,t0,hold_end=t1,sw=14,glow=(255,150,0),glitch=False); paste(fr,sprite(lab,bcs(70),WHITE,sw=5),W/2,1725,ease(seg(t,t0,t0+0.25))*(1 if t<t1 else 0))
    kt(fr,"HER LITTERS",bcs(80),CREAM,W/2,300,t,54.9,hold_end=58.6,sw=6)
    return fr
def S9(t):  # 58.9 - 64.4
    p=seg(t,58.9,64.4); fr=fit(25,p,hfrac=0.30,yfrac=0.50,push=0.08,dim=0.95,par=False,wmax=0.88)
    bands(fr,0.6,0.66,660,1250); motes(fr,t,0.3); return fr
def S10(t): # 64.4 - 68.8 no guarantee
    p=seg(t,64.4,68.8); fr=fit(30,p,hfrac=0.34,yfrac=0.52,push=0.08,dim=0.85,par=True)
    gray=fr.mean(2,keepdims=True); fr=(fr*0.7+gray*0.3).astype(np.uint8)
    bands(fr,0.72,0.74,700,1250)
    kt(fr,"BUT THE JUNGLE",bcs(86),CREAM,W/2,300,t,64.6,hold_end=68.6,sw=6); kt(fr,"GIVES NO GUARANTEE",anton(112),RED,W/2,440,t,66.0,hold_end=68.6,sw=8,glow=(255,40,30))
    return fr
def S11(t): # 68.8 - 78.0 summer water, cubs play
    if t<73.4:
        p=seg(t,68.8,73.4); fr=place(17,zoom_s(p,0.55,1.9),0.60,0.76,yf=0.5)
        bands(fr,0.66,0.7,660,1250); motes(fr,t,0.3)
        kt(fr,"SUMMER",bcs(84),CREAM,W/2,300,t,69.0,hold_end=73.2,sw=6); kt(fr,"AT THE WATER",anton(130),(110,225,255),W/2,440,t,69.6,hold_end=73.2,sw=8,glow=(0,160,200))
        return fr
    p=seg(t,73.4,78.0); fr=fit(26,p,hfrac=0.34,yfrac=0.50,push=0.08,dim=0.95,par=False,wmax=0.95)
    bands(fr,0.6,0.66,660,1250); motes(fr,t,0.3)
    kt(fr,"THE CUBS PLAY",anton(130),GOLD,W/2,330,t,75.0,hold_end=77.8,sw=9,glow=(255,150,0))
    return fr
def S12(t): # 78.0 - 85.0
    p=seg(t,78.0,85.0); fr=fit(28,p,hfrac=0.30,yfrac=0.50,push=0.08,dim=0.95,par=True)
    bands(fr,0.66,0.7,660,1250); motes(fr,t,0.3)
    kt(fr,"FOR A MOMENT",bcs(84),CREAM,W/2,300,t,78.1,hold_end=80.1,sw=6); kt(fr,"ALL IS WELL",anton(130),GOLD,W/2,440,t,78.5,hold_end=80.1,sw=9,glow=(255,150,0))
    kt(fr,"BUT THE JUNGLE IS",bcs(80),CREAM,W/2,300,t,80.4,hold_end=84.8,sw=6); kt(fr,"NOT ALWAYS KIND",anton(130),RED,W/2,440,t,81.2,hold_end=84.8,sw=9,glow=(255,40,30))
    return fr
def S13(t): # 85.0 - 98.5  30 June 2026 (reported)
    p=seg(t,85.0,98.5); fr=fit(25,p,hfrac=0.28,yfrac=0.52,push=0.06,dim=0.7,par=False,wmax=0.85)
    gray=fr.mean(2,keepdims=True); fr=(fr*0.55+gray*0.45).astype(np.uint8)
    bands(fr,0.75,0.78,700,1250)
    kt(fr,"30 JUNE 2026",anton(150),WHITE,W/2,330,t,85.4,hold_end=91.8,sw=9,glow=(0,0,0))
    kt(fr,"AS REPORTED",bcs(78),CREAM,W/2,480,t,87.5,hold_end=91.8,sw=6)
    kt(fr,"A 17-MONTH-OLD CUB",bcs(86),CREAM,W/2,320,t,92.4,hold_end=98.3,sw=6); kt(fr,"OF P-151",anton(130),GOLD,W/2,460,t,93.4,hold_end=98.3,sw=9,glow=(255,150,0))
    pill(fr,"REPORTED. NOT OFFICIALLY CONFIRMED.",W/2,1760,ease(seg(t,87.4,87.9)),size=32,fg=(240,240,240),bg=(60,20,20))
    return fr
def S14(t): # 98.5 - 118.7 territory, less space
    p=seg(t,98.5,118.7); fr=fit(30,p,hfrac=0.32,yfrac=0.52,push=0.08,dim=0.9,par=True)
    bands(fr,0.7,0.74,700,1250)
    if t>=108.0:
        kt(fr,"LESS SPACE.",anton(140),WHITE,W/2,320,t,108.2,hold_end=118.5,sw=9,glow=(0,0,0)); kt(fr,"HARDER SURVIVAL.",anton(110),RED,W/2,470,t,109.4,hold_end=118.5,sw=9,glow=(255,40,30))
    return fr
def S15(t): # 118.7 - 124.2
    p=seg(t,118.7,124.2); fr=fit(24,p,hfrac=0.30,yfrac=0.50,push=0.08,dim=0.95,par=False,wmax=0.95)
    bands(fr,0.66,0.7,660,1250); motes(fr,t,0.3)
    kt(fr,"TIGERS CAME BACK.",anton(112),GOLD,W/2,300,t,119.2,hold_end=121.6,sw=8,glow=(255,150,0)); kt(fr,"IS THERE ROOM?",anton(120),WHITE,W/2,300,t,121.7,hold_end=123.9,sw=8,glow=(0,0,0))
    return fr
def S16(t): # 124.2 - end card
    p=seg(t,124.2,DUR); fr=fit(27,p,hfrac=0.24,yfrac=0.46,push=0.06,dim=0.9,par=False,wmax=0.95)
    bands(fr,0.72,0.82,680,1150); motes(fr,t,0.3)
    a=ease(seg(t,124.5,125.0))
    paste(fr,sprite("FULL PANNA STORY",anton(120),WHITE,sw=8,glow=(255,150,0)),W/2,1440,a); paste(fr,sprite("ON MY CHANNEL, LINK BELOW",bcs(64),CREAM,sw=5),W/2,1565,a)
    paste(fr,sprite("THE NATURAL ANGLE",anton(84),GOLD,sw=7,glow=(255,150,0)),W/2,1690,a); paste(fr,sprite("Photos: Hitesh Chawla. Not all frames show P-151.",bar(32),CREAM,sw=3),W/2,1795,a)
    fade(fr,ease(seg(t,131.4,DUR)))
    return fr
SC=[(0,5.7,S1),(5.7,13.0,S2),(13.0,16.1,S3),(16.1,23.5,S4),(23.5,33.0,S5),(33.0,44.2,S6),(44.2,54.7,S7),(54.7,58.9,S8),(58.9,64.4,S9),(64.4,68.8,S10),(68.8,78.0,S11),(78.0,85.0,S12),(85.0,98.5,S13),(98.5,118.7,S14),(118.7,124.2,S15),(124.2,DUR+1,S16)]
HITS=[(0.85,0.8),(7.5,0.6),(16.4,0.6),(24.4,0.5),(30.5,0.5),(55.15,0.5),(56.55,0.5),(57.45,0.6),(66.0,0.6),(85.4,0.7),(108.2,0.6),(119.2,0.5),(124.5,0.5)]
def frame(t):
    for i,(a,b,fn) in enumerate(SC):
        if a<=t<b: break
    fr=fn(t)
    if i>0 and t-a<0.35:
        pa,pb,pf=SC[i-1]; prev=pf(min(t,pb-0.001)); k=ease((t-a)/0.35); fr=(prev.astype(np.float32)*(1-k)+fr.astype(np.float32)*k).astype(np.uint8)
    fr=punch(fr,t,HITS); return look(fr,t,HITS)
if __name__=="__main__":
    ts=[float(x) for x in sys.argv[2:]]; tiles=[]
    for t in ts:
        f=frame(t); f=cv2.resize(f,(270,480)); cv2.putText(f,f"{t}",(6,24),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,0),2); tiles.append(f)
    cols=8; rows=(len(tiles)+cols-1)//cols; img=np.zeros((rows*480,cols*270,3),np.uint8)
    for i,f in enumerate(tiles): img[(i//cols)*480:(i//cols+1)*480,(i%cols)*270:(i%cols+1)*270]=f
    cv2.imwrite(sys.argv[1],cv2.cvtColor(img,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,85])
