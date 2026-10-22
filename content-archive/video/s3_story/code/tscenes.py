import sys, json, math, os
SPD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/"
sys.path.insert(0,SPD+"fox")
from fscenes import *   # helpers: view, fb, fwin, grad, scrim, brand, tchip, pill, shimmer, txt, glayer, comp ...
import fscenes as FS
GRN=(110,205,125); RED2=(240,104,84); GOLD2=(255,190,60); FOR=(10,26,20)
ENT=[("S1",8),("S2",14),("S3",11),("S4",8),("S5",11),("S6",9),("S7",13),("S8",7),("S9",13)]
DES={}; _c=0
for n,l in ENT: DES[n]=(_c,l); _c+=l
START={n:DES[n][0] for n,_ in ENT}; START["end"]=_c
if os.path.exists(SPD+"s3tiger/marks.json"): START.update(json.load(open(SPD+"s3tiger/marks.json")))
TOTAL=START["end"]; ORDER=[n for n,_ in ENT]+["end"]
def FAC(n):
    i=ORDER.index(n); return DES[n][1]/(START[ORDER[i+1]]-START[n])
def fbg(t,c0=(6,18,15),c1=(20,40,32)):
    a=grad(c0,c1,("f",c0,c1)).copy(); img=arr2img(a); d=ImageDraw.Draw(img,"RGBA")
    for i in range(26):  # drifting fireflies
        x=(i*173+t*(9+i%5))%W; y=(i*331+math.sin(t*0.7+i)*40)%1500+120; al=int(60+60*math.sin(t*1.6+i)); d.ellipse((x-2,y-2,x+2,y+2),fill=(255,226,150,max(0,al)))
    return img
def wbox(name,cx,cy,bw,rect):
    FS.load(name); FWi,FHi=FS.FW[name]; ww,wh=rect[2],rect[3]; bh=bw*FWi*wh/(FHi*ww)
    if bh>1: bh=1; bw=bh*FHi*ww/(FWi*wh)
    cx=min(max(cx,bw/2),1-bw/2); cy=min(max(cy,bh/2),1-bh/2); return (cx-bw/2,cy-bh/2,cx+bw/2,cy+bh/2)
def head(img,s,lt,y=150): tchip(img,s,eo3(seg(lt,0.1,0.5)),y=y,col=GOLD2)
def rowtxt(d,x,y,s,f,col,a): txt(d,(x,y),s,f,col,a,"ls")
# ---------------- S1
def S1(lt,t):
    a=fb("t5",0.5,0.9,z=1.0+0.06*seg(lt,0,8),pan=(0,0.01*seg(lt,0,8))); a=a*np.array((1.05,1.0,0.92),np.float32)
    img=arr2img(a); scrim(img,1280,1920,0.0,0.86,(4,10,8)); scrim(img,0,330,0.7,0.0,(4,10,8)); brand(img,CREAM,170); head(img,"PILIBHIT TIGER RESERVE",lt)
    ia=eo3(seg(lt,0.5,1.1)); comp(img,glayer((W/2,1590),"THE TIGER CALLED S3",A(104),top=(255,250,240),bot=(255,208,120)),ia,sc=lerp(1.25,1,eob(seg(lt,0.5,1.2),1.3)))
    d=ImageDraw.Draw(img,"RGBA"); a2=eo3(seg(lt,2.6,3.2)); txt(d,(W/2,1670),"ONE OF PILIBHIT'S BIGGEST TIGERS",B(50),CREAM,255*a2)
    ak=eo3(seg(lt,1.2,1.8)); txt(d,(W/2,238),"ALSO KNOWN AS  SURAI 3  ·  MANAG",B(38),GOLD2,255*ak)
    pa=eo3(seg(lt,5.0,5.5)); pill(img,(W/2,1780),"HOW BIG IS HE? HOW DID HE SURVIVE?",B(44),pa,fg=INK,bg=GOLD2,sc=lerp(0.8,1,eob(seg(lt,5.0,5.6))))
    return img
# ---------------- S2
AMBR=(255,196,70)
ROWS=[("NAME","S3  ·  SURAI 3  ·  MANAG",GRN,"ok"),("PLACE","PILIBHIT TIGER RESERVE, UP",GRN,"ok"),("WEIGHT","280 TO 300 KG  (REPORTED)",AMBR,"rep"),("LENGTH","ABOUT 10 FEET  (REPORTED)",AMBR,"rep"),("AGE","NOT PUBLISHED",RED2,"no"),("MOTHER","NOT PUBLISHED",RED2,"no")]
def S2(lt,t):
    img=fbg(t); brand(img,CREAM,150); head(img,"THE ID CARD",lt)
    fwin(img,"t2",wbox("t2",0.52,0.48,0.52,(60,200,960,620)),(60,200,960,620),z=1.0+0.04*seg(lt,0,14),spot=(0.52,0.45,0.2,0.28),k=eo3(seg(lt,0.3,1.2)),border=GOLD2)
    d=ImageDraw.Draw(img,"RGBA")
    for i,(lab,val,col,kind) in enumerate(ROWS):
        t0=1.2+i*1.7; a=eo3(seg(lt,t0,t0+0.45)); y=905+i*125
        if a<=0: continue
        x0=60+(1-a)*60
        d.rounded_rectangle((x0,y-52,x0+960,y+52),radius=22,fill=(14,34,28,int(225*a)),outline=col+(int(200*a),),width=3)
        txt(d,(x0+34,y-8),lab,BM(28),GREY,255*a,"ls")
        f=B(54) if len(val)<20 else (B(46) if len(val)<26 else B(42)); txt(d,(x0+34,y+36),val,f,col,255*a,"ls")
        cx,cy=x0+900,y
        if kind=="ok": d.ellipse((cx-24,cy-24,cx+24,cy+24),fill=GRN+(int(255*a),)); d.line((cx-11,cy,cx-3,cy+9,cx+13,cy-10),fill=(10,26,20,int(255*a)),width=6,joint="curve")
        elif kind=="rep": d.ellipse((cx-24,cy-24,cx+24,cy+24),outline=col+(int(255*a),),width=4); txt(d,(cx,cy+14),"i",B(40),col,255*a)
        else: d.ellipse((cx-24,cy-24,cx+24,cy+24),outline=RED2+(int(255*a),),width=4); txt(d,(cx,cy+14),"?",B(40),RED2,255*a)
    ka=eo3(seg(lt,11.6,12.2)); txt(d,(W/2,1790),"Weight and length: local safari sources. Not officially measured.",BM(30),GREY,255*ka)
    return img
# ---------------- S3 map
def _tmap(key,lon,lat,k):
    if key not in _MC:
        cam=IC.Cam(lon,lat,k,w=960,h=1000); m=IC.map_img(cam,coast=0.8).astype(np.float32); lm=np.clip((m[...,0]/(m[...,2]+1)-0.5)*4,0,1)[...,None]
        tex=(IC.TEXN[:cam.h,:cam.w,None]*14+IC.TEXL[:cam.h,:cam.w,None]*18); land=np.array((78,104,70),np.float32)+tex
        m=m*(1-lm)*1.4+land*lm
        if key=="te":
            mk=np.zeros((cam.h,cam.w),np.uint8); pts=[cam.px(*p) for p in NEPB]+[(cam.w+50,-50)]; cv2.fillPoly(mk,[np.array(pts,np.int32)],255); mk=cv2.GaussianBlur(mk,(0,0),2)[...,None]/255.0
            m=m*(1-0.55*mk)+np.array((120,96,70),np.float32)*0.55*mk*lm
        g=np.zeros((cam.h,cam.w),np.uint8); step=10 if key=="in" else 2
        for lo in range(60,100,step):
            x=int(cam.px(lo,cam.latc)[0]); cv2.line(g,(x,0),(x,cam.h),255,1)
        for la in range(0,40,step):
            y=int(cam.px(cam.lonc,la)[1]); cv2.line(g,(0,y),(cam.w,y),255,1)
        m=m+(g[...,None]/255.0)*18
        _MC[key]=(cam,np.clip(m,0,255).astype(np.uint8))
    return _MC[key]
_MC={}
NEPB=[(79.9,29.9),(80.06,28.83),(80.58,28.62),(81.0,28.3),(81.4,28.15),(82.0,27.85),(82.8,27.55),(83.4,27.42),(84.0,27.35),(85.0,26.9),(86.0,26.6),(88.1,26.4),(88.1,31.0),(79.9,31.0)]
TERAI=[(78.1,30.0),(78.9,29.5),(79.8,28.85),(80.6,28.45),(81.3,28.25),(82.3,27.85),(83.2,27.5),(84.1,27.3)]
PINS=[("Corbett",78.9,29.53,(0,-70),0.0),("Pilibhit",79.8,28.78,(0,60),0.0),("Dudhwa",80.65,28.5,(30,64),0.0),("Valmiki",84.0,27.42,(-10,-60),0.0)]
def S3(lt,t):
    img=fbg(t); brand(img,CREAM,150); head(img,"WHERE IS PILIBHIT?",lt)
    d=ImageDraw.Draw(img,"RGBA")
    caI,mI=_tmap("in",81.0,23.0,28); caT,mT=_tmap("te",81.4,28.7,120)
    z=ease(seg(lt,3.2,5.0))
    mk=Image.new("L",(960,1000),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,959,999),radius=26,fill=255)
    # base india map, zooming into pilibhit before crossfade
    cx,cy=caI.px(79.8,28.7); s=lerp(1.0,3.3,z); cpx=lerp(480,cx,z); cpy=lerp(500,cy,z); M=np.array([[s,0,480-cpx*s],[0,s,500-cpy*s]],np.float32)
    base=cv2.warpAffine(mI,M,(960,1000),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    tx=cv2.warpAffine(mT,np.array([[1,0,0],[0,1,0]],np.float32),(960,1000)); cf=ease(seg(lt,4.0,5.0))
    # terai map is centred at 81.4E; shift so pilibhit sits like the zoomed india view
    m=(base*(1-cf)+tx*cf).astype(np.uint8)
    mp=Image.fromarray(m).convert("RGBA"); mp.putalpha(mk); ov=Image.new("RGBA",(960,1000),(0,0,0,0)); do=ImageDraw.Draw(ov,"RGBA")
    # India stage overlay
    ia=1-cf
    if ia>0:
        x,y=cx,cy; x=(x*s+M[0,2]); y=(y*s+M[1,2]); r=((lt*0.8)%1)
        do.ellipse((x-14-r*60,y-14-r*60,x+14+r*60,y+14+r*60),outline=GOLD2+(int(220*(1-r)*ia),),width=4); do.ellipse((x-13,y-13,x+13,y+13),fill=GOLD2+(int(255*ia),),outline=CREAM+(int(255*ia),),width=3)
        a_=eo3(seg(lt,0.6,1.2))*ia
        for s_,lo,la,f in (("INDIA",78.0,21.0,B(70)),):
            px,py=caI.px(lo,la); px=px*s+M[0,2]; py=py*s+M[1,2]; txt(do,(px,py),s_,f,CREAM,200*a_)
    # Terai stage
    if cf>0:
        pts=[caT.px(*p) for p in TERAI]; pa=eo3(seg(lt,5.0,6.8))*cf
        n=len(pts)-1; f=min(1,seg(lt,5.0,7.0))*n; i=min(int(f),n-1); u=f-i
        vis=pts[:i+1]+[(lerp(pts[i][0],pts[i+1][0],u),lerp(pts[i][1],pts[i+1][1],u))]
        if len(vis)>1: do.line(vis,fill=GRN+(int(120*cf),),width=46,joint="curve"); do.line(vis,fill=GRN+(int(255*cf),),width=5,joint="curve")
        for (nm,lo,la,(ox,oy),_) in PINS:
            t0={"Corbett":6.6,"Pilibhit":5.4,"Dudhwa":7.4,"Valmiki":8.0}[nm]; a_=eo3(seg(lt,t0,t0+0.4))*cf
            if a_<=0: continue
            x,y=caT.px(lo,la); big=(nm=="Pilibhit"); rr=14 if big else 9; col=GOLD2 if big else CREAM
            do.ellipse((x-rr,y-rr,x+rr,y+rr),fill=col+(int(255*a_),),outline=(10,26,20,int(255*a_)),width=3)
            f=B(40 if big else 32); w=f.getlength(nm.upper())+26; bx=min(max(x+ox-w/2,12),960-12-w)
            do.rounded_rectangle((bx,y+oy-30,bx+w,y+oy+22),radius=12,fill=(8,22,18,int(230*a_)),outline=col+(int(200*a_),),width=2); txt(do,(bx+13,y+oy+8),nm.upper(),f,col,255*a_,"ls")
        ha=eo3(seg(lt,5.6,6.2))*cf; txt(do,(480,70),"HIMALAYAN FOOTHILLS  ▲",B(34),CREAM,190*ha); txt(do,(700,330),"NEPAL",B(52),CREAM,170*ha)
        txt(do,(480,950),"TERAI ARC (ILLUSTRATIVE)",BM(26),GRN,230*ha)
    mp.alpha_composite(ov); img.alpha_composite(mp,(60,250)); d=ImageDraw.Draw(img,"RGBA"); d.rounded_rectangle((58,248,1022,1252),radius=26,outline=GOLD2+(170,),width=3)
    c1=eo3(seg(lt,7.6,8.2)); comp(img,glayer((W/2,1400),"730 SQ KM",A(110),top=(255,250,240),bot=(255,208,120)),c1,dy=(1-c1)*24)
    d=ImageDraw.Draw(img,"RGBA"); a2=eo3(seg(lt,8.4,9.0)); txt(d,(W/2,1485),"TIGER RESERVE SINCE JUNE 2014",B(48),CREAM,255*a2)
    a3=eo3(seg(lt,9.8,10.4)); txt(d,(W/2,1560),"Linked to Dudhwa: one connected tiger population",B(36),GOLD2,255*a3); txt(d,(W/2,1608),"Wildlife Institute of India study",BM(28),GREY,255*a3)
    txt(d,(W/2,1700),"Map: Natural Earth. Terai band and pins are illustrative.",BM(26),GREY,200)
    return img
# ---------------- S4 counts
def S4(lt,t):
    img=fbg(t); brand(img,CREAM,150); head(img,"A COMEBACK STORY",lt)
    fwin(img,"t3",wbox("t3",0.5,0.52,0.95,(60,200,960,640)),(60,200,960,640),z=1.0+0.05*seg(lt,0,9),spot=(0.5,0.55,0.18,0.22),k=eo3(seg(lt,0.3,1.2)),border=GOLD2)
    d=ImageDraw.Draw(img,"RGBA")
    # bars
    def bar(y,label,sub,v0,v1,t0,col,lab):
        a=eo3(seg(lt,t0,t0+0.4)); 
        if a<=0: return
        txt(d,(90,y-44),label,B(40),CREAM,255*a,"ls"); txt(d,(990,y-44),sub,BM(28),GREY,255*a,"rs")
        d.rounded_rectangle((90,y-20,990,y+40),radius=30,fill=(20,44,36,int(230*a)))
        p=ease(seg(lt,t0+0.3,t0+2.0)); w=max(60,(lerp(0,v1,p)/90)*900); d.rounded_rectangle((90,y-20,90+w,y+40),radius=30,fill=col+(int(255*a),))
        txt(d,(90+w-24 if w>260 else 90+w+20,y+24),lab(lerp(v0,v1,p)),A(40),INK if w>260 else CREAM,255*a,"rs" if w>260 else "ls")
    bar(990,"WHEN IT BECAME A TIGER RESERVE (2014)","about 25 to 30",25,30,1.4,(150,170,150),lambda v:f"{int(v)}")
    bar(1170,"LATER ESTIMATES","65 to 79+  (sources vary)",30,79,3.4,GOLD2,lambda v:f"{int(v)}+")
    ba=eo3(seg(lt,6.4,7.0)); 
    if ba>0:
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((70,1300,1010,1560),radius=28,fill=(10,26,20,240),outline=GOLD2+(255,),width=4); comp(img,l,ba,sc=lerp(0.92,1,eob(seg(lt,6.4,7.2))))
        d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1400),"2020: TX2 AWARD",A(72),GOLD2,255*ba); txt(d,(W/2,1465),"For doubling its tigers (Wikipedia)",B(38),CREAM,255*ba)
        txt(d,(W/2,1520),"S3 is one of those tigers.",B(34),GRN,255*ba)
    txt(d,(W/2,1680),"Counts differ between sources. Official: NTCA / Reserve.",BM(28),GREY,230*eo3(seg(lt,3.6,4.2)))
    return img
# ---------------- S5 size
BARS=[("ADULT MALE RANGE","200 to 260 kg",200,260,(150,170,150)),("CENTRAL INDIA, AVERAGE (42 males)","190 kg",0,190,(150,170,150)),("CHITWAN, AVERAGE (7 males)","235 kg",0,235,(150,170,150)),("CHITWAN, HEAVIEST EVER REPORTED","270+ kg",0,270,GOLD2)]
def S5(lt,t):
    img=fbg(t); brand(img,CREAM,150); head(img,"HOW BIG IS BIG?",lt)
    fwin(img,"t4",wbox("t4",0.58,0.55,0.8,(60,200,960,520)),(60,200,960,520),z=1.0+0.05*seg(lt,0,12),spot=(0.57,0.62,0.18,0.3),k=eo3(seg(lt,0.3,1.2)),border=GOLD2)
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,800),"WEIGHT OF WILD BENGAL TIGER MALES",B(40),CREAM,255*eo3(seg(lt,0.8,1.4)))
    X0,X1=90,990
    for i,(lab,val,lo,hi,col) in enumerate(BARS):
        t0=1.6+i*1.7; a=eo3(seg(lt,t0,t0+0.4)); y=950+i*112
        if a<=0: continue
        txt(d,(X0,y-26),lab,BM(28),GREY,255*a,"ls"); d.rounded_rectangle((X0,y-8,X1,y+36),radius=22,fill=(20,44,36,int(230*a)))
        p=ease(seg(lt,t0+0.3,t0+1.4)); x0=X0+lo/300*(X1-X0); x1=X0+(lerp(lo,hi,p) if lo>0 else hi*p)/300*(X1-X0) 
        if lo>0: x1=X0+lerp(lo,hi,p)/300*(X1-X0)
        d.rounded_rectangle((x0,y-8,max(x0+30,x1),y+36),radius=22,fill=col+(int(255*a),)); txt(d,(X1,y-26),val,B(38),col if col!=(150,170,150) else CREAM,255*a,"rs")
    s0=1.6+4*1.7; sa=eo3(seg(lt,s0,s0+0.5)); y=950+4*112
    if sa>0:
        txt(d,(X0,y-26),"S3  (LOCAL REPORTS)",BM(28),AMBR,255*sa,"ls"); txt(d,(X1,y-26),"280 to 300 kg ?",B(38),AMBR,255*sa,"rs"); d.rounded_rectangle((X0,y-8,X1,y+36),radius=22,fill=(20,44,36,int(230*sa)))
        pp=ease(seg(lt,s0+0.3,s0+1.2)); xa=X0+280/300*(X1-X0); xb=X0+lerp(280,300,pp)/300*(X1-X0)
        for k_ in range(0,int(xb-xa)+1,14): d.rounded_rectangle((xa+k_,y-8,xa+k_+8,y+36),radius=3,fill=AMBR+(int(255*sa),))
        d.rounded_rectangle((X0,y-8,xa,y+36),radius=22,outline=AMBR+(int(200*sa),),width=3)
        pu=0.5+0.5*math.sin(lt*5); txt(d,(540,y+82),"UNVERIFIED. NEEDS A SCALE.",B(36),RED2,(150+100*pu)*sa)
    ka=eo3(seg(lt,9.4,10.0)); txt(d,(W/2,1640),"If true, he is heavier than every male above.",B(44),CREAM,255*ka); txt(d,(W/2,1700),"Studies via Wikipedia. S3 figure: local safari sources.",BM(28),GREY,230*ka)
    return img
# ---------------- S6 rival
def S6(lt,t):
    img=fbg(t); brand(img,CREAM,150); head(img,"THE RIVAL",lt)
    fwin(img,"t3",wbox("t3",0.5,0.55,0.95,(60,200,960,400)),(60,200,960,400),z=1.0+0.04*seg(lt,0,9),spot=(0.5,0.55,0.2,0.2),k=eo3(seg(lt,0.3,1.2)),border=GOLD2)
    cx,cy=540,900
    ta=eo3(seg(lt,0.8,1.6)); tl_=L(); dtl=ImageDraw.Draw(tl_,"RGBA"); dtl.ellipse((cx-300,cy-210,cx+300,cy+210),fill=(110,205,125,40),outline=GRN+(240,),width=4); comp(img,tl_,ta); d=ImageDraw.Draw(img,"RGBA")
    txt(d,(cx,cy-250),"A MALE HOLDS A TERRITORY",B(36),GRN,255*ta)
    d.ellipse((cx-24,cy-16,cx+24,cy+30),fill=GOLD2+(int(255*ta),)); txt(d,(cx,cy+8+4),"S3",B(30),INK,255*ta); txt(d,(cx,cy+70),"S3",B(32),GOLD2,255*ta)
    ra=ease(seg(lt,2.6,4.2)); pulse=0.5+0.5*math.sin(lt*6)
    if ra>0:
        rx=lerp(960,cx+260,ra); ry=cy+lerp(110,50,ra); d.ellipse((rx-24,ry-16,rx+24,ry+30),fill=RED2+(255,)); txt(d,(rx,ry+12),"S2",B(30),INK,255); txt(d,(rx,ry+70),"RIVAL",B(30),RED2,255)
        if ra>0.95: d.line((cx+30,cy+10,rx-30,ry+10),fill=RED2+(int(120+100*pulse),),width=5)
    pa=eo3(seg(lt,4.6,5.2)); txt(d,(W/2,1250),"TWO BIG MALES. ONE TERRITORY.",B(46),CREAM,255*pa)
    ka=eo3(seg(lt,5.6,6.2)); l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((70,1370,1010,1640),radius=28,fill=(10,26,20,240),outline=RED2+(255,),width=4); comp(img,l,ka,sc=lerp(0.92,1,eob(seg(lt,5.6,6.4))))
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1470),"S3'S BIGGEST RIVAL: S2",A(68),RED2,255*ka); txt(d,(W/2,1540),"As told by local safari sources.",B(38),CREAM,255*eo3(seg(lt,6.6,7.2))); txt(d,(W/2,1592),"No public report on this rivalry found.",BM(30),GREY,255*eo3(seg(lt,7.2,7.8)))
    return img
# ---------------- S7 the fight
def S7(lt,t):
    img=fbg(t); brand(img,CREAM,150); head(img,"THE NEAR-DEATH FIGHT",lt)
    hit=seg(lt,1.8,2.0)
    fwin(img,"t4",wbox("t4",0.58,0.55,0.8,(60,200,960,500)),(60,200,960,500),z=1.0+0.05*seg(lt,0,13),spot=(0.57,0.62,0.18,0.3),k=eo3(seg(lt,0.3,1.2)),border=RED2 if 1.8<lt<6.5 else GOLD2,desat=0.6*ease(seg(lt,2.0,3.6))*(1-ease(seg(lt,7.0,9.0))))
    d=ImageDraw.Draw(img,"RGBA")
    ev=eo3(seg(lt,0.8,1.4)); txt(d,(W/2,800),"S3'S HEALTH",B(40),CREAM,255*ev)
    # bar value: 1 -> 0.06 after attack, rescue, recover to 0.8
    v=1.0-0.94*ease(seg(lt,1.9,3.4)); v=v+0.0 if lt<7.0 else 0.06+0.74*ease(seg(lt,7.0,10.0))
    col=GRN if v>0.55 else (AMBR if v>0.25 else RED2)
    d.rounded_rectangle((90,840,990,920),radius=40,fill=(20,44,36,int(230*ev))); 
    if ev>0: d.rounded_rectangle((90,840,90+max(40,860*v+40),920),radius=40,fill=col+(255,))
    if 1.8<lt<2.4: txt(d,(W/2,1010),"S2 ATTACKS",A(90),RED2,255*(1-seg(lt,2.2,2.4)))
    na=eo3(seg(lt,3.6,4.2))*(1-eo3(seg(lt,6.2,6.8)))
    if na>0.01: pu=0.6+0.4*math.sin(lt*7); comp(img,glayer((W/2,1080),"NEARLY DIED",A(120),top=(255,170,150),bot=RED2),na*pu,sc=lerp(1.2,1,eob(seg(lt,3.6,4.3),1.3)))
    d=ImageDraw.Draw(img,"RGBA")
    ra=eo3(seg(lt,5.4,6.0))
    if ra>0:
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((90,1130,990,1330),radius=30,fill=(10,30,24,245),outline=GRN+(255,),width=4); comp(img,l,ra,sc=lerp(0.9,1,eob(seg(lt,5.4,6.1))))
        d=ImageDraw.Draw(img,"RGBA"); cx_,cy_=190,1230; d.ellipse((cx_-46,cy_-46,cx_+46,cy_+46),fill=GRN+(int(255*ra),)); d.rectangle((cx_-8,cy_-28,cx_+8,cy_+28),fill=(10,26,20,int(255*ra))); d.rectangle((cx_-28,cy_-8,cx_+28,cy_+8),fill=(10,26,20,int(255*ra)))
        txt(d,(260,1215),"FOREST OFFICIALS STEP IN",B(48),CREAM,255*ra,"ls"); txt(d,(260,1275),"And bring him back from the edge.",B(34),GRN,255*eo3(seg(lt,6.4,7.0)),"ls")
    sv=eo3(seg(lt,9.4,10.0)); comp(img,glayer((W/2,1520),"HE SURVIVED.",A(128),top=(255,250,240),bot=GOLD2),sv,sc=lerp(1.3,1,eob(seg(lt,9.4,10.1),1.3)))
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1610),"As told by local safari sources. No public report found.",BM(30),GREY,255*eo3(seg(lt,10.6,11.2)))
    return img
# ---------------- S8 what the camera shows
def S8(lt,t):
    img=fbg(t); brand(img,CREAM,150); head(img,"WHAT THE PHOTO SHOWS",lt)
    p=seg(lt,0,8); fwin(img,"t5",wbox("t5",0.5,0.45,0.95,(60,200,960,880)),(60,200,960,880),z=1.0+0.18*ease(seg(lt,1.0,7.0)),pan=(0,0.12*ease(seg(lt,1.0,7.0))),spot=(0.5,0.45,0.28,0.28),k=eo3(seg(lt,0.3,1.2)),border=GOLD2)
    d=ImageDraw.Draw(img,"RGBA")
    items=[(1.4,"THICK, POWERFUL NECK"),(3.2,"HEAVY FOREARMS"),(5.0,"FULL, HEALTHY COAT")]
    for i,(t0,s) in enumerate(items):
        a=eo3(seg(lt,t0,t0+0.45)); y=1150+i*100
        if a<=0: continue
        d.rounded_rectangle((120,y-40,960,y+40),radius=24,fill=(14,34,28,int(230*a)),outline=GRN+(int(220*a),),width=3); d.ellipse((140,y-20,180,y+20),fill=GRN+(int(255*a),)); d.line((149,y,158,y+9,172,y-9),fill=(10,26,20,int(255*a)),width=5)
        txt(d,(206+(1-a)*40,y+14),s,B(46),CREAM,255*a,"ls")
    ka=eo3(seg(lt,6.2,6.8)); txt(d,(W/2,1560),"A SURVIVOR'S BUILD.",A(64),GOLD2,255*ka); txt(d,(W/2,1625),"What the photo shows. Not a measurement.",B(36),CREAM,255*ka)
    return img
# ---------------- S9 CTA
def S9(lt,t):
    a=fb("t1",0.5,0.9,z=1.0+0.05*seg(lt,0,13)); a=a*np.array((1.05,1.0,0.92),np.float32)*(1-0.15*seg(lt,0,13))
    img=arr2img(a); scrim(img,1000,1920,0.0,0.93,(4,10,8)); scrim(img,0,330,0.7,0.0,(4,10,8)); brand(img,CREAM,170); head(img,"THE VERDICT",lt)
    d=ImageDraw.Draw(img,"RGBA")
    q=eo3(seg(lt,0.6,1.2)); txt(d,(W/2,1190),"ONE OF INDIA'S BIGGEST?",B(58),CREAM,255*q); w=eo3(seg(lt,1.8,2.4)); comp(img,glayer((W/2,1305),"CLAIMS SAY YES.",A(104),top=(255,250,240),bot=GOLD2),w,sc=lerp(1.3,1,eob(seg(lt,1.8,2.5),1.3)))
    q=eo3(seg(lt,4.2,4.8)); txt(d,(W/2,1405),"WANT TO SEE HIM IN PERSON?",B(54),CREAM,255*q); w=eo3(seg(lt,5.4,6.0)); comp(img,glayer((W/2,1515),"JOIN ME IN PILIBHIT",A(92),top=(255,250,240),bot=GOLD2),w,sc=lerp(1.3,1,eob(seg(lt,5.4,6.1),1.3)))
    btn=L(); ImageDraw.Draw(btn,"RGBA").rounded_rectangle((W/2-440,1570,W/2+440,1662),radius=46,fill=GOLD2+(250,)); ba=eo3(seg(lt,7.2,7.7)); comp(img,btn,ba,sc=lerp(0.6,1,eob(seg(lt,7.2,7.8))))
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1632),"DURING MY PILIBHIT SAFARIS",B(44),INK,255*eo3(seg(lt,7.6,8.0)))
    ka=eo3(seg(lt,9.0,9.6)); txt(d,(W/2,1730),"GET IN TOUCH ON INSTAGRAM",B(46),CREAM,255*ka); txt(d,(W/2,1790),"@thenaturalangle",A(54),GOLD2,255*eo3(seg(lt,9.6,10.2)))
    txt(d,(W/2,1850),"Photos: Hitesh Chawla. Sources: WII, Wikipedia, local safari sources.",BM(23),GREY,225*eo3(seg(lt,11.0,11.8)))
    return img
FN={"S1":S1,"S2":S2,"S3":S3,"S4":S4,"S5":S5,"S6":S6,"S7":S7,"S8":S8,"S9":S9}
VIGN=None;GRN_=None
def finish(fr,t):
    global VIGN,GRN_
    if VIGN is None:
        yy,xx=np.mgrid[0:H,0:W]; dd=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2); VIGN=(1-0.28*np.clip(dd-0.45,0,1)**1.3).astype(np.float32)[:,:,None]; GRN_=np.random.default_rng(3).normal(0,3.0,(H+64,W+64,1)).astype(np.float32)
    ox=int((t*977)%64); oy=int((t*613)%64); return np.clip(fr*VIGN+GRN_[oy:oy+H,ox:ox+W],0,255).astype(np.uint8)
def frame(t):
    i=max(j for j,n in enumerate(ORDER[:-1]) if START[n]<=t+1e-6); n=ORDER[i]; lt=(t-START[n])*FAC(n)
    fr=np.array(FN[n](lt,t))[...,:3].astype(np.float32)
    for m in ORDER[1:-1]:
        dd=t-START[m]
        if 0<=dd<0.2: fr=fr+(1-dd/0.2)*45
        if -0.1<dd<0: sc=1+0.05*(1+dd/0.1); fr=cv2.warpAffine(fr,np.array([[sc,0,W/2*(1-sc)],[0,sc,H/2*(1-sc)]],np.float32),(W,H),borderMode=cv2.BORDER_REFLECT)
    fade=min(1,t/0.25)*min(1,(TOTAL-t)/0.7)
    return finish(np.clip(fr*fade,0,255),t)
if __name__=="__main__":
    for tt in [float(a) for a in sys.argv[1:]]: Image.fromarray(frame(tt)).save(f"q_{tt:05.1f}.jpg",quality=85)
