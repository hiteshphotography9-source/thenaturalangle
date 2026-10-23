import sys, json, math, os
SPD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/"
sys.path.insert(0,SPD+"hornbill")
import hscenes as H
from hscenes import *
GOLD=(255,190,70)
ENT=[("S1",7),("S2",10),("S3",10),("S4",14),("S5",9),("S6",9),("S7",8),("S8",8)]
DES={}; _c=0
for n,l in ENT: DES[n]=(_c,l); _c+=l
START={n:DES[n][0] for n,_ in ENT}; START["end"]=_c
if os.path.exists(SPD+"disp/marks.json"): START.update(json.load(open(SPD+"disp/marks.json")))
TOTAL=START["end"]; ORDER=[n for n,_ in ENT]+["end"]
def FAC(n):
    i=ORDER.index(n); return DES[n][1]/(START[ORDER[i+1]]-START[n])
def bgd(t): return T.fbg(t,(14,10,6),(44,30,14))
def chipd(img,s,lt,y=150): tchip(img,s,eo3(seg(lt,0.1,0.5)),y=y,col=GOLD)
def tag(d,s,a,y=1830): txt(d,(W/2,y),s,BM(26),GREY,200*a)
# S1 hook
def S1(lt,t):
    img=bgd(t); brand(img,CREAM,150); chipd(img,"A TIGER'S JOURNEY",lt)
    k=ease(seg(lt,0.3,7)); fwin(img,"d2",wbox("d2",0.55,0.55,0.8,(60,520,960,720)),(60,520,960,720),z=1.0+0.2*k,pan=(0.04*k,0),spot=(0.58,0.55,0.18,0.25),k=0.5*eo3(seg(lt,0.3,1.2)),border=GOLD)
    d=ImageDraw.Draw(img,"RGBA")
    a=eo3(seg(lt,0.3,0.8)); comp(img,glayer((W/2,330),"HE WALKED",A(100),top=(255,250,240),bot=(255,216,140)),a,dy=(1-a)*30)
    a=eo3(seg(lt,0.9,1.5)); comp(img,glayer((W/2,460),"ABOUT 3,000 KM",A(120),top=(255,236,200),bot=GOLD),a,sc=lerp(1.25,1,eob(seg(lt,0.9,1.6),1.3)))
    a=eo3(seg(lt,3.2,3.8)); comp(img,glayer((W/2,1450),"TO COVER",A(84),top=(255,250,240),bot=(255,216,140)),a)
    a=eo3(seg(lt,4.0,4.7)); comp(img,glayer((W/2,1580),"315 KM IN A",A(110),top=(255,250,240),bot=GOLD),a,sc=lerp(1.2,1,eob(seg(lt,4.0,4.8),1.3)))
    a=eo3(seg(lt,4.6,5.3)); comp(img,glayer((W/2,1700),"STRAIGHT LINE.",A(110),top=(255,236,200),bot=GOLD),a,sc=lerp(1.2,1,eob(seg(lt,4.6,5.4),1.3)))
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1810),"Tiger T1-C1. Photo shown: a different tiger.",BM(26),GREY,210*eo3(seg(lt,5.6,6.2)))
    return img
# S2 why leave
def S2(lt,t):
    img=bgd(t); brand(img,CREAM,150); chipd(img,"WHY LEAVE HOME?",lt)
    fwin(img,"d3",wbox("d3",0.5,0.55,0.85,(60,200,960,620)),(60,200,960,620),z=1.0+0.06*seg(lt,0,10),spot=(0.62,0.55,0.2,0.2),k=0.5*eo3(seg(lt,0.3,1.2)),border=GOLD)
    d=ImageDraw.Draw(img,"RGBA")
    a=eo3(seg(lt,0.6,1.2)); comp(img,glayer((W/2,910),"A YOUNG MALE",A(84),top=(255,250,240),bot=(255,216,140)),a); a=eo3(seg(lt,1.4,2.0)); comp(img,glayer((W/2,1010),"MUST FIND HIS OWN LAND.",A(70),top=(255,250,240),bot=GOLD),a,sc=lerp(1.2,1,eob(seg(lt,1.4,2.1),1.3)))
    a=eo3(seg(lt,3.2,3.8)); txt(d,(W/2,1110),"AVERAGE DISTANCE MOVED FROM BIRTH AREA",B(36),CREAM,255*a)
    for i,(lab,val,v,col,t0) in enumerate((("MALES","27 KM",27,GOLD,3.6),("FEMALES","5.7 KM",5.7,(150,200,150),5.4))):
        a=eo3(seg(lt,t0,t0+0.4)); y=1230+i*130
        if a<=0: continue
        txt(d,(90,y-30),lab,B(40),CREAM,255*a,"ls"); d.rounded_rectangle((90,y-14,990,y+44),radius=29,fill=(40,28,14,int(230*a))); p=ease(seg(lt,t0+0.3,t0+1.4)); d.rounded_rectangle((90,y-14,90+max(50,900*(v/30)*p),y+44),radius=29,fill=col+(int(255*a),)); txt(d,(970,y-30),val,A(44),col,255*a,"rs")
    a=eo3(seg(lt,7.4,8.0)); txt(d,(W/2,1560),"Males roam. Females stay near their mother.",B(42),GOLD,255*a)
    a=eo3(seg(lt,8.2,8.8)); txt(d,(W/2,1640),"Study of Bengal tigers in semi-arid western India.",BM(28),GREY,230*a)
    return img
# S3 meet
ROWD=[("NAME","T1-C1  ·  SUB-ADULT MALE",GOLD),("HOME","TIPESHWAR WILDLIFE SANCTUARY, YAVATMAL",GOLD),("COLLARED","FEBRUARY 2019 (WII + MAHARASHTRA FOREST DEPT)",GOLD),("LEFT HOME","JUNE 2019",GOLD)]
def S3(lt,t):
    img=bgd(t); brand(img,CREAM,150); chipd(img,"MEET T1-C1",lt)
    fwin(img,"d1",wbox("d1",0.5,0.5,0.9,(60,200,960,560)),(60,200,960,560),z=1.0+0.06*seg(lt,0,10),spot=(0.55,0.45,0.2,0.25),k=0.5*eo3(seg(lt,0.3,1.2)),border=GOLD)
    d=ImageDraw.Draw(img,"RGBA")
    for i,(lab,val,col) in enumerate(ROWD):
        t0=1.2+i*1.7; a=eo3(seg(lt,t0,t0+0.45)); y=880+i*140
        if a<=0: continue
        x0=60+(1-a)*60; d.rounded_rectangle((x0,y-56,x0+960,y+56),radius=22,fill=(40,28,14,int(228*a)),outline=col+(int(210*a),),width=3); txt(d,(x0+34,y-10),lab,BM(28),GREY,255*a,"ls"); f=B(46) if len(val)<30 else B(36); txt(d,(x0+34,y+38),val,f,col,255*a,"ls")
    a=eo3(seg(lt,8.0,8.6)); pill(img,(W/2,1520),"GPS COLLAR: EVERY STEP RECORDED",B(42),a,fg=INK,bg=GOLD,sc=lerp(0.85,1,eob(seg(lt,8.0,8.7))))
    a=eo3(seg(lt,8.8,9.4)); txt(d,(W/2,1620),"Photos here show other young tigers, not T1-C1.",BM(30),GREY,255*a)
    return img
# S4 map journey
_MC={}
def dmap():
    if "m" not in _MC:
        cam=IC.Cam(77.6,19.6,95,w=960,h=1000); m=IC.map_img(cam,coast=0.8).astype(np.float32); lm=np.clip((m[...,0]/(m[...,2]+1)-0.5)*4,0,1)[...,None]
        tex=IC.TEXN[:cam.h,:cam.w,None]*16+IC.TEXL[:cam.h,:cam.w,None]*46; m=m*(1-lm)*1.4+(np.array((82,104,68),np.float32)+tex)*lm
        g=np.zeros((cam.h,cam.w),np.uint8)
        for lo in range(70,90,1): x=int(cam.px(lo,cam.latc)[0]); cv2.line(g,(x,0),(x,cam.h),255,1)
        for la in range(8,30,1): y=int(cam.px(cam.lonc,la)[1]); cv2.line(g,(0,y),(cam.w,y),255,1)
        m=m+(g[...,None]/255.0)*16; _MC["m"]=(cam,np.clip(m,0,255).astype(np.uint8))
    return _MC["m"]
WAY=[(78.6,20.0),(78.9,19.7),(79.5,19.3),(79.9,19.8),(79.3,20.3),(78.4,20.5),(77.7,20.2),(77.0,19.7),(76.4,19.5),(76.2,20.0),(76.65,20.55)]
def smooth(pts,n=14):
    out=[]; P=[pts[0]]+pts+[pts[-1]]
    for i in range(1,len(P)-2):
        p0,p1,p2,p3=P[i-1],P[i],P[i+1],P[i+2]
        for k in range(n):
            u=k/n; out.append(tuple(0.5*((2*p1[j])+(-p0[j]+p2[j])*u+(2*p0[j]-5*p1[j]+4*p2[j]-p3[j])*u*u+(-p0[j]+3*p1[j]-3*p2[j]+p3[j])*u**3) for j in (0,1)))
    out.append(pts[-1]); return out
ROUTE=smooth(WAY)
def S4(lt,t):
    img=bgd(t); brand(img,CREAM,150); chipd(img,"THE JOURNEY",lt)
    cam,m=dmap(); mk=Image.new("L",(960,1000),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,959,999),radius=26,fill=255); mp=Image.fromarray(m).convert("RGBA"); mp.putalpha(mk)
    ov=Image.new("RGBA",(960,1000),(0,0,0,0)); do=ImageDraw.Draw(ov,"RGBA")
    ma=eo3(seg(lt,0.4,1.0))
    for s_,lo,la in (("MAHARASHTRA",75.6,18.4),("TELANGANA",79.4,17.6)): x,y=cam.px(lo,la); txt(do,(x,y),s_,B(34),CREAM,150*ma)
    p=ease(seg(lt,2.0,10.5)); n=max(2,int(len(ROUTE)*p)); pts=[cam.px(*q) for q in ROUTE[:n]]
    if len(pts)>1: do.line(pts,fill=GOLD+(120,),width=11,joint="curve"); do.line(pts,fill=(255,236,170,255),width=4,joint="curve")
    for nm,lo,la,t0,(ox,oy) in (("TIPESHWAR",78.6,20.0,1.0,(0,-66)),("DNYANGANGA",76.65,20.55,10.6,(0,-66))):
        a_=eo3(seg(lt,t0,t0+0.4))
        if a_<=0: continue
        x,y=cam.px(lo,la); r=((lt-t0)*0.9)%1; do.ellipse((x-9-r*34,y-9-r*34,x+9+r*34,y+9+r*34),outline=CREAM+(int(200*(1-r)*a_),),width=3); do.ellipse((x-11,y-11,x+11,y+11),fill=GOLD+(int(255*a_),),outline=CREAM+(int(255*a_),),width=3)
        f=B(32); w=f.getlength(nm)+26; bx=min(max(x+ox-w/2,12),960-12-w); do.rounded_rectangle((bx,y+oy-30,bx+w,y+oy+22),radius=12,fill=(20,14,8,int(235*a_)),outline=GOLD+(int(200*a_),),width=2); txt(do,(bx+13,y+oy+8),nm,f,CREAM,255*a_,"ls")
    if p>0:
        x,y=cam.px(*ROUTE[n-1]); do.ellipse((x-10,y-10,x+10,y+10),fill=(255,255,255,255))
    mp.alpha_composite(ov); img.alpha_composite(mp,(60,230)); d=ImageDraw.Draw(img,"RGBA"); d.rounded_rectangle((58,228,1022,1232),radius=26,outline=GOLD+(170,),width=3)
    km=int(3000*p); dy=int(225*p)
    a=eo3(seg(lt,1.6,2.2)); txt(d,(300,1340),f"{km:,}",A(100),GOLD,255*a,"ms"); txt(d,(300,1390),"KM WALKED (TOTAL)",B(30),CREAM,255*a); txt(d,(780,1340),f"{dy}",A(100),GOLD,255*a,"ms"); txt(d,(780,1390),"DAYS",B(30),CREAM,255*a)
    a=eo3(seg(lt,11.0,11.6)); txt(d,(W/2,1500),"About 8.4 km a day, for 225 days.",B(44),CREAM,255*a)
    a=eo3(seg(lt,12.0,12.6)); txt(d,(W/2,1580),"He settled in Dnyanganga Wildlife Sanctuary, Buldhana.",B(34),GOLD,255*a)
    txt(d,(W/2,1700),"Route and state labels illustrative. Map: Natural Earth.",BM(26),GREY,200)
    return img
# S5 walked vs straight
def S5(lt,t):
    img=bgd(t); brand(img,CREAM,150); chipd(img,"THE MATH",lt)
    d=ImageDraw.Draw(img,"RGBA")
    a=eo3(seg(lt,0.4,1.0)); comp(img,glayer((W/2,380),"3,000 KM WALKED",A(100),top=(255,236,200),bot=GOLD),a,sc=lerp(1.2,1,eob(seg(lt,0.4,1.1),1.3)))
    # winding vs straight
    x0,x1,y=110,970,640
    p=ease(seg(lt,1.4,4.2)); pts=[]
    for i in range(0,int(300*p)+1): u=i/300; pts.append((lerp(x0,x1,u),y+70*math.sin(u*math.pi*9)*(0.5+0.5*math.sin(u*5))))
    if len(pts)>1: d.line(pts,fill=GOLD+(255,),width=8,joint="curve")
    d.ellipse((x0-12,y-12,x0+12,y+12),fill=CREAM+(255,))
    a=eo3(seg(lt,4.4,5.0)); d.line((x0,y+170,x1,y+170),fill=CREAM+(int(255*a),),width=8); d.ellipse((x0-12,y+158,x0+12,y+182),fill=CREAM+(int(255*a),)); d.ellipse((x1-12,y+158,x1+12,y+182),fill=CREAM+(int(255*a),))
    a2=eo3(seg(lt,5.0,5.6)); comp(img,glayer((W/2,1050),"315 KM IN A STRAIGHT LINE",A(70),top=(255,250,240),bot=(255,216,140)),a2)
    a=eo3(seg(lt,6.2,6.8)); pill(img,(W/2,1220),"NEARLY 10x THE STRAIGHT DISTANCE",B(46),a,fg=INK,bg=GOLD,sc=lerp(0.85,1,eob(seg(lt,6.2,6.9))))
    a=eo3(seg(lt,7.2,7.8)); txt(d,(W/2,1340),"Why? Farms, villages, roads and fences",B(42),CREAM,255*a); txt(d,(W/2,1400),"keep forcing detours.",B(42),CREAM,255*a)
    a=eo3(seg(lt,8.0,8.6)); txt(d,(W/2,1560),"Source: Hussain et al. 2022, Ecology and Evolution.",BM(28),GREY,230*a)
    return img
# S6 small forests
def S6(lt,t):
    img=bgd(t); brand(img,CREAM,150); chipd(img,"HOW HE SURVIVED",lt)
    fwin(img,"d4",wbox("d4",0.55,0.55,0.8,(60,200,960,560)),(60,200,960,560),z=1.0+0.06*seg(lt,0,9),spot=(0.72,0.6,0.2,0.2),k=0.5*eo3(seg(lt,0.3,1.2)),border=GOLD)
    d=ImageDraw.Draw(img,"RGBA")
    # patches diagram
    rng=np.random.default_rng(5); pts=[(150+i*70+rng.uniform(-18,18),960+rng.uniform(-70,70),rng.uniform(16,34)) for i in range(12)]
    a=eo3(seg(lt,1.2,1.8))
    for i,(x,y,r) in enumerate(pts): d.ellipse((x-r,y-r,x+r,y+r),fill=(70,130,70,int(255*a)))
    p=ease(seg(lt,2.4,6.0)); n=int(len(pts)*p)
    for i in range(min(n,len(pts))-1): d.line((pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1]),fill=GOLD+(255,),width=5)
    if n>0 and n<=len(pts): d.ellipse((pts[n-1][0]-11,pts[n-1][1]-11,pts[n-1][0]+11,pts[n-1][1]+11),fill=(255,255,255,255))
    a=eo3(seg(lt,0.6,1.2)); txt(d,(W/2,860),"HE HOPPED BETWEEN SMALL FOREST PATCHES",B(44),CREAM,255*a)
    a=eo3(seg(lt,6.2,6.8)); comp(img,glayer((W/2,1250),"SMALL FORESTS",A(96),top=(255,250,240),bot=GOLD),a,sc=lerp(1.2,1,eob(seg(lt,6.2,6.9),1.3)))
    a=eo3(seg(lt,6.8,7.4)); comp(img,glayer((W/2,1360),"KEEP TIGERS CONNECTED.",A(76),top=(255,250,240),bot=(255,216,140)),a)
    a=eo3(seg(lt,7.6,8.2)); txt(d,(W/2,1470),"89 resting and kill sites were identified from his track.",B(36),CREAM,255*a)
    a=eo3(seg(lt,8.2,8.8)); txt(d,(W/2,1540),"Finding of the study, not a guess.",BM(30),GREY,230*a)
    return img
# S7 settled
def S7(lt,t):
    img=bgd(t); brand(img,CREAM,150); chipd(img,"WHERE HE STOPPED",lt)
    fwin(img,"d2",wbox("d2",0.55,0.55,0.8,(60,200,960,620)),(60,200,960,620),z=1.0+0.08*seg(lt,0,8),spot=(0.58,0.55,0.18,0.25),k=0.5*eo3(seg(lt,0.3,1.2)),border=GOLD)
    d=ImageDraw.Draw(img,"RGBA")
    a=eo3(seg(lt,0.6,1.2)); comp(img,glayer((W/2,950),"DNYANGANGA",A(110),top=(255,250,240),bot=GOLD),a,sc=lerp(1.2,1,eob(seg(lt,0.6,1.3),1.3)))
    a=eo3(seg(lt,1.8,2.4)); txt(d,(W/2,1040),"Wildlife Sanctuary, Buldhana, Maharashtra",B(40),CREAM,255*a)
    for i,(t0,lab,val) in enumerate(((3.0,"SANCTUARY AREA","about 205 km²"),(4.6,"HIS JOURNEY ENDED AFTER","225 days"))):
        a=eo3(seg(lt,t0,t0+0.45)); y=1200+i*140
        if a<=0: continue
        d.rounded_rectangle((90,y-56,990,y+56),radius=22,fill=(40,28,14,int(230*a)),outline=GOLD+(int(210*a),),width=3); txt(d,(124,y-10),lab,BM(28),GREY,255*a,"ls"); txt(d,(124,y+38),val,B(50),GOLD,255*a,"ls")
    a=eo3(seg(lt,6.2,6.8)); txt(d,(W/2,1520),"A tiger home he found by walking.",B(42),CREAM,255*a)
    return img
# S8 close
def S8(lt,t):
    img=bgd(t); brand(img,CREAM,150); chipd(img,"THE NATURAL ANGLE",lt)
    fwin(img,"d2",wbox("d2",0.55,0.55,0.8,(60,200,960,620)),(60,200,960,620),z=1.0+0.06*seg(lt,0,8),spot=(0.58,0.55,0.18,0.25),k=0.5*eo3(seg(lt,0.3,1.2)),border=GOLD)
    d=ImageDraw.Draw(img,"RGBA")
    a=eo3(seg(lt,0.4,1.0)); txt(d,(W/2,960),"A TIGER NEEDS MORE THAN A PARK.",B(52),CREAM,255*a)
    a=eo3(seg(lt,1.8,2.4)); comp(img,glayer((W/2,1110),"IT NEEDS A PATH.",A(130),top=(255,250,240),bot=GOLD),a,sc=lerp(1.3,1,eob(seg(lt,1.8,2.5),1.3)))
    btn=L(); ImageDraw.Draw(btn,"RGBA").rounded_rectangle((W/2-380,1290,W/2+380,1382),radius=46,fill=GOLD+(250,)); ba=eo3(seg(lt,3.6,4.1)); comp(img,btn,ba,sc=lerp(0.6,1,eob(seg(lt,3.6,4.2))))
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1351),"FOLLOW THE NATURAL ANGLE",B(46),INK,255*eo3(seg(lt,4.0,4.4)))
    txt(d,(W/2,1470),"More tiger stories every week",B(36),CREAM,255*eo3(seg(lt,4.8,5.4)))
    txt(d,(W/2,1640),"Photos: Hitesh Chawla (other tigers, not T1-C1).",BM(26),GREY,225*eo3(seg(lt,5.4,6.2)))
    txt(d,(W/2,1690),"Source: Hussain et al. 2022 (Ecology and Evolution); WII; Maharashtra Forest Dept.",BM(24),GREY,225*eo3(seg(lt,5.8,6.6)))
    return img
FN={"S1":S1,"S2":S2,"S3":S3,"S4":S4,"S5":S5,"S6":S6,"S7":S7,"S8":S8}
def frame(t):
    i=max(j for j,n in enumerate(ORDER[:-1]) if START[n]<=t+1e-6); n=ORDER[i]; lt=(t-START[n])*FAC(n)
    fr=np.array(FN[n](lt,t))[...,:3].astype(np.float32)
    for m in ORDER[1:-1]:
        dd=t-START[m]
        if 0<=dd<0.2: fr=fr+(1-dd/0.2)*45
        if -0.1<dd<0: sc=1+0.05*(1+dd/0.1); fr=cv2.warpAffine(fr,np.array([[sc,0,W/2*(1-sc)],[0,sc,H/2*(1-sc)]],np.float32),(W,H),borderMode=cv2.BORDER_REFLECT)
    fade=min(1,t/0.25)*min(1,(TOTAL-t)/0.7)
    return T.finish(np.clip(fr*fade,0,255),t)
if __name__=="__main__":
    for tt in [float(a) for a in sys.argv[1:]]: Image.fromarray(frame(tt)).save(f"q_{tt:05.1f}.jpg",quality=85)
