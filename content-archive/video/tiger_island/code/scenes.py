import sys; sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/island')
from core import *
import json, os
# beat marks (seconds). Retimed to VO later via marks.json if present
M=dict(hook=0.0,swim=5.0,sing=14.5,idea=24.5,bali=37.0,isl=51.0,punch=60.5,cta=69.5,end=76.0)
if os.path.exists(SP+"island/marks.json"): M.update(json.load(open(SP+"island/marks.json")))
TOTAL=M['end']
rng=np.random.default_rng(11)
VIG=None; GR=None
def finish(fr,t):
    global VIG,GR
    if VIG is None:
        yy,xx=np.mgrid[0:H,0:W]; d=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2); VIG=(1-0.32*np.clip(d-0.45,0,1)**1.3).astype(np.float32)[:,:,None]
        GR=np.random.default_rng(3).normal(0,4.0,(H+64,W+64,1)).astype(np.float32)
    ox=int((t*977)%64); oy=int((t*613)%64)
    return np.clip(fr*VIG+GR[oy:oy+H,ox:ox+W],0,255).astype(np.uint8)
def brand(o,a=1.0): o.text((W/2,78),"THE NATURAL ANGLE",bcs(30),CREAM,a*0.6,shadow=False)
def maptag(o,a=1.0,s="MAP: NATURAL EARTH. ILLUSTRATIVE."): o.text((W/2,1590),s,bcm(26),GREY,a*0.85)
def lt(t,a,b): return seg(t,a,b)
# ---------------- HOOK
def S_hook(t):
    p=t/(M['swim']); fr=pwin("260a7220",0.36,0.52,lerp(0.37,0.30,ease(p))).astype(np.float32)
    # water shimmer
    sh=np.clip(TEXL[1100:,:,None]*np.sin(t*2.0+np.arange(H-1100)[:,None,None]*0.03),0,1)*18; fr[1100:]+=sh
    fr=fr.astype(np.uint8); gradv(fr,0,560,0.65,0.0); gradv(fr,1250,H,0.0,0.75)
    o=Ov(); brand(o)
    a0=eo3(lt(t,0.2,0.7))*(1-lt(t,1.9,2.2))
    o.text((W/2,300),"TIGERS ARE STRONG SWIMMERS",anton(78),CREAM,a0,rise=30)
    a=eo3(lt(t,2.1,2.6)); o.text((W/2,270),"SO WHY AREN'T THEY",anton(90),CREAM,a,rise=30)
    a2=eo3(lt(t,2.5,3.0)); o.text((W/2,395),"ON EVERY ISLAND?",anton(116),GOLD,a2,rise=30)
    return o.apply(fr)
# ---------------- SUNDARBANS
SW_PATH=[(88.70,21.92),(88.95,21.80),(89.20,21.88),(89.45,22.02),(89.62,22.08)]
def S_swim(t):
    lt_=t-M['swim']; p=ease(seg(lt_,0,2.6))
    cam=Cam(lerp(85.5,89.15,p),lerp(19.5,22.0,p),lerp(34,300,p**1.3)); fr=map_img(cam)
    gradv(fr,0,520,0.7,0.0); gradv(fr,1350,H,0.0,0.7)
    o=Ov(); brand(o); maptag(o,eo3(seg(lt_,2.0,2.5)))
    a=eo3(seg(lt_,0.3,0.8)); o.text((W/2,250),"SUNDARBANS",anton(118),GOLD,a,rise=30); o.text((W/2,315),"INDIA  ·  BANGLADESH",bcs(40),CREAM,a)
    if lt_>2.4:
        x,y=cam.px(88.85,21.95); 
        for kk in range(2):
            r=((lt_*0.7+kk/2)%1); o.ring(x,y,12+r*60,GOLD,(1-r)*0.8)
    a1=eo3(seg(lt_,2.6,3.0))*(1-0.4*seg(lt_,4.4,4.8))
    o.card((70,420,W-70,580),a1); o.text((W/2,500),"~5 WATER CHANNELS A DAY",anton(62),CREAM,a1); o.text((W/2,555),"each wider than 30 m  ·  radio-collar study",bcm(32),GREY,a1)
    pa=seg(lt_,4.5,6.3)
    if pa>0:
        pts=[cam.px(*q) for q in SW_PATH]; o.dash(pts,GOLD,1.0,prog=ease(pa),w=6)
        n=len(pts)-1; f=ease(pa)*n; i=min(int(f),n-1); u=f-i; tx=lerp(pts[i][0],pts[i+1][0],u); ty=lerp(pts[i][1],pts[i+1][1],u)
        o.dot(tx,ty,13,GOLD)
        if pa>=1: o.arrowhead(pts[-2],pts[-1],GOLD,1.0)
    a2=eo3(seg(lt_,5.0,5.4))
    o.pill((W/2,1240),"ONE TIGER: ~100 KM IN 4 MONTHS",bcs(44),a2); o.text((W/2,1310),"crossing rivers over 1 km wide",bcm(34),CREAM,a2)
    a3=eo3(seg(lt_,7.0,7.4)); o.pill((W/2,680),"BUT CHANNELS OVER 400 m? RARELY CROSSED",bcs(42),a3,fg=(255,236,230),bg=(120,36,28),sc=lerp(0.8,1,eob(seg(lt_,7.0,7.5))))
    return o.apply(fr)
# ---------------- SINGAPORE
def S_sing(t):
    lt_=t-M['sing']; p=ease(seg(lt_,0,3.2))
    cam=Cam(lerp(102.2,103.80,p),lerp(3.2,1.45,p),lerp(110,2300,p**2.2)); fr=map_img(cam)
    gradv(fr,0,560,0.75,0.0); gradv(fr,1300,H,0.0,0.75)
    o=Ov(); brand(o); maptag(o,eo3(seg(lt_,1,1.5)))
    a=eo3(seg(lt_,0.2,0.7)); o.text((W/2,250),"AND THE SEA?",anton(110),GOLD,a,rise=30)
    if lt_<2.6:
        x,y=cam.px(102.3,3.6); o.text((x,y),"MALAY PENINSULA",bcs(44),CREAM,a*(1-seg(lt_,2.0,2.6)))
    if lt_>2.8:
        a1=eo3(seg(lt_,2.8,3.3)); x,y=cam.px(103.82,1.36); o.text((x,y),"SINGAPORE",anton(64),CREAM,a1)
        x2,y2=cam.px(103.70,1.52); o.text((x2,y2-20),"JOHOR (MALAYA)",bcs(40),CREAM,a1)
        pa=seg(lt_,3.4,4.6)
        p0=cam.px(103.76,1.475); p2=cam.px(103.79,1.415); p1=((p0[0]+p2[0])/2+60,(p0[1]+p2[1])/2)
        pts=bez(p0,p1,p2,30); o.dash(pts,GOLD,1.0,prog=ease(pa),w=6)
        if pa>=1: o.arrowhead(pts[-3],pts[-1],GOLD,1.0)
        a2=eo3(seg(lt_,3.8,4.3)); o.card((70,380,W-70,560),a2); o.text((W/2,460),"1800s: TIGERS SWAM ACROSS",anton(58),CREAM,a2); o.text((W/2,525),"the narrow Johor Strait",bcs(38),GOLD,a2)
    a3=eo3(seg(lt_,5.6,6.0))
    if a3>0:
        o.card((70,1230,W-70,1500),a3,edge=RED); y=1330
        o.d.line((180,y,900,y),fill=GOLD+(int(200*a3),),width=4)
        pr=ease(seg(lt_,6.0,7.6)); o.d.line((180,y,180+720*pr,y),fill=RED+(int(255*a3),),width=8)
        o.dot(180,y,14,GOLD,a3); o.text((180,y-30),"1831",anton(52),GOLD,a3); o.text((180,y+60),"first reported victim",bcm(30),CREAM,a3)
        a4=eo3(seg(lt_,7.4,7.8)); o.dot(900,y,14,RED,a4); o.text((900,y-30),"1930",anton(52),RED,a4); o.text((900,y+60),"last wild tiger shot",bcm(30),CREAM,a4)
        a5=eo3(seg(lt_,8.2,8.6)); o.text((W/2,1460),"THEY ARRIVED. THEY DIDN'T LAST.",bcs(40),CREAM,a5)
    return o.apply(fr)
# ---------------- IDEA
ang=np.linspace(0,2*np.pi,90,endpoint=False); rr=1+0.10*np.sin(ang*3+1)+0.06*np.sin(ang*5+2)+0.04*np.sin(ang*9)
ISL=[(540+300*r*math.cos(a),1060+230*r*math.sin(a)) for a,r in zip(ang,rr)]
PREY=[(540+rng.uniform(-220,220),1060+rng.uniform(-150,150)) for _ in range(14)]
def S_idea(t):
    lt_=t-M['idea']
    base=np.zeros((H,W,3),np.float32)+OCEAN*1.6; base*=1+0.12*TEXL[...,None]+0.05*np.sin(TEXN[...,None]*3+t)
    fr=np.clip(base,0,255).astype(np.uint8)
    o=Ov(); brand(o)
    o.d.polygon(ISL,fill=tuple(int(c) for c in LANDC*1.3)+(255,),outline=(150,200,190,200))
    o.text((W/2,250),"SWIMMING IS NOT SETTLING",anton(84),GOLD,eo3(seg(lt_,0.2,0.7)),rise=30)
    # tiger arrives
    pa=ease(seg(lt_,0.6,2.4)); sx,sy=lerp(120,470,pa),lerp(1600,1080,pa)
    for i in range(10):
        q=max(0,pa-i*0.03); wx,wy=lerp(120,470,q),lerp(1600,1080,q); o.ring(wx,wy,6+i*3,BLUEW,0.25*(1-i/10)*(pa<1 or True))
    o.dot(sx,sy,18,GOLD); o.text((sx,sy+8),"M",bcs(24),INK,1.0,shadow=False)
    o.text((W/2,1420),"ONE TIGER ARRIVES",anton(64),CREAM,eo3(seg(lt_,2.0,2.4))*(1-seg(lt_,3.3,3.6)))
    items=[(3.5,"1. A MALE AND A FEMALE"),(5.5,"2. A TIGRESS NEEDS 16 TO 180 SQ KM"),(7.5,"3. ENOUGH DEER AND PIGS TO EAT")]
    for i,(t0,s) in enumerate(items):
        a=eo3(seg(lt_,t0,t0+0.4)); act=1-0.4*seg(lt_,t0+1.6,t0+2.0)
        o.text((90,400+i*70),s,bcs(46),GOLD if act>0.9 else CREAM,a*act,anchor="ls",rise=0)
    fa=eo3(seg(lt_,3.6,4.2)); fx,fy=620,1040
    if fa>0: o.dot(fx,fy,18,TEAL,fa); o.text((fx,fy+8),"F",bcs(24),INK,fa,shadow=False)
    ra=ease(seg(lt_,5.7,7.2))
    if ra>0:
        for (cx,cy),col in (((470,1080),GOLD),((620,1040),TEAL)):
            R=lerp(30,330,ra); o.ring(cx,cy,R,col,0.7,4)
    pr=eo3(seg(lt_,7.7,8.4))
    for i,(x,y) in enumerate(PREY):
        a=eo3(seg(lt_,7.7+i*0.05,8.1+i*0.05)); o.d.ellipse((x-6,y-6,x+6,y+6),fill=CREAM+(int(200*a),))
    a=eo3(seg(lt_,9.2,9.7)); o.card((70,1360,W-70,1560),a,edge=RED)
    o.text((W/2,1440),"TO LAST: HUNDREDS OF TIGERS",anton(64),CREAM,a); o.text((W/2,1510),"long-term viable population, rough estimate",bcm(32),GREY,a)
    if lt_>10.4:
        k=eo3(seg(lt_,10.4,10.8)); o.text((W/2,660),"SMALL ISLAND = DEAD END",anton(70),RED,k)
    return o.apply(fr)
# ---------------- BALI vs LOMBOK
def S_bali(t):
    lt_=t-M['bali']; p=ease(seg(lt_,0,2.0))
    lev=ease(seg(lt_,2.4,4.6))*(1-ease(seg(lt_,11.6,13.2)))
    cam=Cam(lerp(113.0,115.55,p),lerp(-6.0,-8.45,p),lerp(110,420,p**1.5)); fr=map_img(cam,level=lev)
    gradv(fr,0,560,0.75,0.0); gradv(fr,1380,H,0.0,0.7)
    o=Ov(); brand(o); maptag(o,eo3(seg(lt_,1,1.5)),"SHELF SHOWN: SEA SHALLOWER THAN 200 m. ILLUSTRATIVE.")
    o.text((W/2,250),"BALI VS LOMBOK",anton(110),GOLD,eo3(seg(lt_,0.2,0.7)),rise=30)
    la=eo3(seg(lt_,1.8,2.3))
    for nm,lo,la_ in (("JAVA",114.55,-7.72),("BALI",115.15,-8.0),("LOMBOK",116.3,-8.25)):
        x,y=cam.px(lo,la_); o.text((x,y),nm,anton(50),CREAM,la)
    a=eo3(seg(lt_,2.6,3.0))*(1-seg(lt_,11.4,11.8)); o.pill((W/2,400),"ICE AGE: SEA ABOUT 120 m LOWER",bcs(44),a)
    pa=seg(lt_,4.8,6.6)
    if pa>0:
        pts=[cam.px(*q) for q in ((114.1,-7.9),(114.5,-8.05),(114.9,-8.25),(115.3,-8.35))]
        o.dash(pts,GOLD,1-seg(lt_,12.0,12.5),prog=ease(pa),w=6)
        o.text((W/2,1270),"TIGERS WALKED INTO BALI",anton(62),GOLD,eo3(seg(lt_,5.0,5.4))*(1-seg(lt_,7.2,7.5)))
    wa=seg(lt_,7.0,8.0)
    if wa>0:
        top=cam.px(115.73,-7.7); bot=cam.px(115.73,-9.1)
        o.dash([top,bot],RED,1.0,prog=ease(wa),w=6,dl=14,gap=10)
        o.text((top[0],top[1]-20),"WALLACE LINE",bcs(40),RED,eo3(seg(lt_,7.4,7.8)))
        a1=eo3(seg(lt_,7.6,8.0))*(1-seg(lt_,11.4,11.8)); o.card((70,1180,W-70,1360),a1,edge=RED)
        o.text((W/2,1255),"LOMBOK STRAIT: 250 m+ DEEP",anton(58),CREAM,a1); o.text((W/2,1320),"never dry, even in the Ice Ages  ·  about 20 to 35 km wide",bcm(32),GREY,a1)
    ba=seg(lt_,9.0,10.0)
    if ba>0:
        s=cam.px(115.3,-8.35); e=cam.px(115.62,-8.42); bk=1-max(0,(ba-0.7)/0.3)*0.3
        x=lerp(s[0],e[0],min(1,ba/0.7)*bk); y=lerp(s[1],e[1],min(1,ba/0.7)*bk); o.dot(x,y,13,GOLD,1-seg(lt_,12.0,12.5))
        if ba>0.7:
            xa=eo3(seg(lt_,9.7,10.0)); cx,cy=e
            o.d.line((cx-26,cy-26,cx+26,cy+26),fill=RED+(int(255*xa),),width=8); o.d.line((cx-26,cy+26,cx+26,cy-26),fill=RED+(int(255*xa),),width=8)
            o.pill((W/2,520),"TIGERS NEVER REACHED LOMBOK",bcs(46),xa,fg=(255,236,230),bg=(120,36,28))
    a5=eo3(seg(lt_,12.4,12.8)); x,y=cam.px(115.15,-8.0)
    o.pill((W/2,1270),"AND BALI'S OWN TIGERS: LAST CONFIRMED 1937",bcs(42),a5)
    return o.apply(fr)
# ---------------- ISLANDS
PINS=[(0.9,"ANDAMANS",92.75,11.6,"NO TIGER RECORD",GREY,(28,-40),"ls"),
      (2.3,"SRI LANKA",80.75,7.7,"FOSSIL? DEBATED",GOLD,(30,60),"ls"),
      (3.7,"BORNEO",114.2,0.6,"FOSSILS",GOLD,(-30,70),"rs"),
      (5.1,"PALAWAN",118.6,9.7,"BONES ~20,000 YRS OLD",GOLD,(-30,-46),"rs")]
def S_isl(t):
    lt_=t-M['isl']; p=ease(seg(lt_,0,1.2))
    cam=Cam(lerp(105,99.3,p),lerp(2,6.5,p),lerp(32,23.6,p)); fr=map_img(cam,level=0.55*ease(seg(lt_,0.3,1.2)))
    gradv(fr,0,560,0.75,0.0); gradv(fr,1380,H,0.0,0.7)
    o=Ov(); brand(o); maptag(o,eo3(seg(lt_,1,1.5)),"SHELF SHOWN: SEA SHALLOWER THAN 200 m. ILLUSTRATIVE.")
    o.text((W/2,240),"THEY CAME.",anton(100),CREAM,eo3(seg(lt_,0.2,0.6)),rise=30)
    o.text((W/2,350),"THEY DIDN'T STAY.",anton(100),GOLD,eo3(seg(lt_,0.8,1.2)),rise=30)
    for (t0,nm,lo,la,sub,col,(ox,oy),anc) in PINS:
        a=eo3(seg(lt_,t0,t0+0.35))
        if a<=0: continue
        x,y=cam.px(lo,la)
        r=((lt_-t0)*0.8)%1; o.ring(x,y,10+r*40,col,(1-r)*a)
        o.dot(x,y,11,col,a)
        f1=bcs(38); f2=bcm(30); w=max(f1.getlength(nm),f2.getlength(sub))+30; bx=x+ox if anc=="ls" else x+ox-w
        bx=max(40,min(bx,W-40-w)); by=y+oy
        o.d.rounded_rectangle((bx,by-38,bx+w,by+44),radius=14,fill=(10,14,16,int(215*a)),outline=col+(int(200*a),),width=2)
        o.text((bx+15,by-2),nm,f1,CREAM,a,anchor="ls",shadow=False); o.text((bx+15,by+34),sub,f2,col,a,anchor="ls",shadow=False)
    a=eo3(seg(lt_,6.6,7.0)); o.pill((W/2,1300),"WILD TIGERS THERE TODAY: 0",anton(60),a,fg=(255,236,230),bg=(120,36,28),sc=lerp(0.8,1,eob(seg(lt_,6.6,7.2))))
    return o.apply(fr)
# ---------------- PUNCH
def S_punch(t):
    lt_=t-M['punch']; fr=pwin("a4bcbe52",0.5,0.5,lerp(1.0,0.86,ease(lt_/9))).astype(np.uint8)
    gradv(fr,0,700,0.8,0.0); gradv(fr,1300,H,0.0,0.6)
    o=Ov(); brand(o)
    a1=eo3(seg(lt_,0.4,0.9))*(1-seg(lt_,5.0,5.4)); a2=eo3(seg(lt_,2.6,3.1))*(1-seg(lt_,5.0,5.4))
    o.text((W/2,230),"A TIGER CAN SWIM",anton(96),CREAM,a1,rise=30); o.text((W/2,330),"TO AN ISLAND.",anton(96),CREAM,a1,rise=30)
    o.text((W/2,440),"A POPULATION CAN'T.",anton(110),GOLD,a2,rise=30)
    b1=eo3(seg(lt_,5.5,6.0)); b2=eo3(seg(lt_,6.6,7.1))
    o.text((W/2,280),"SWIMMING MOVES A TIGER.",anton(84),CREAM,b1,rise=30)
    o.text((W/2,390),"LAND MOVES A POPULATION.",anton(84),GOLD,b2,rise=30)
    return o.apply(fr)
# ---------------- CTA
def S_cta(t):
    lt_=t-M['cta']; fr=pwin("454eb397",0.62,0.45,lerp(0.36,0.31,ease(lt_/6.5))).astype(np.float32)*0.8
    fr=fr.astype(np.uint8); gradv(fr,0,700,0.85,0.0); gradv(fr,1250,H,0.0,0.8)
    o=Ov(); brand(o)
    o.text((W/2,280),"WHICH ISLAND SHOULD",anton(90),CREAM,eo3(seg(lt_,0.2,0.7)),rise=30)
    o.text((W/2,385),"HAVE HAD TIGERS?",anton(90),GOLD,eo3(seg(lt_,0.5,1.0)),rise=30)
    o.pill((W/2,500),"TELL ME IN THE COMMENTS",bcs(44),eo3(seg(lt_,1.2,1.6)),sc=lerp(0.7,1,eob(seg(lt_,1.2,1.8))))
    o.pill((W/2,1420),"WATCH NEXT: WHY NO TIGERS IN SRI LANKA",bcs(40),eo3(seg(lt_,2.2,2.6)),fg=CREAM,bg=(20,26,28),outline=GOLD)
    o.text((W/2,1530),"Tiger photos: Hitesh Chawla  ·  Maps: Natural Earth",bcm(28),GREY,eo3(seg(lt_,2.6,3.0)))
    return o.apply(fr)
SCN=[('hook',S_hook),('swim',S_swim),('sing',S_sing),('idea',S_idea),('bali',S_bali),('isl',S_isl),('punch',S_punch),('cta',S_cta)]
KEYS=[k for k,_ in SCN]
def frame(t):
    i=max(j for j,k in enumerate(KEYS) if M[k]<=t+1e-6)
    fr=SCN[i][1](t).astype(np.float32)
    for k in KEYS[1:]:
        d=t-M[k]
        if 0<=d<0.22: fr=fr+(1-d/0.22)*55
        if -0.12<d<0:
            s=1+0.06*(1+d/0.12); fr=cv2.warpAffine(fr,np.array([[s,0,W/2*(1-s)],[0,s,H/2*(1-s)]],np.float32),(W,H),borderMode=cv2.BORDER_REFLECT)
    fade=min(1,t/0.25)*min(1,(TOTAL-t)/0.6)
    return finish(np.clip(fr*fade,0,255),t)
if __name__=="__main__":
    import sys
    for tt in [float(a) for a in sys.argv[1:]]:
        Image.fromarray(frame(tt)).save(f"qc_{tt:05.1f}.jpg",quality=85)
