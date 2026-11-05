import sys; sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/delhi')
from ds import *
from ds2 import multi, pill, zoomf, punch, chapter
import cv2, numpy as np, math
TOTAL3=63.0
PH={}
def ph(k):
    if k not in PH:
        im=cv2.cvtColor(cv2.imread(f'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/delhi/ph/p{k}.jpg'),cv2.COLOR_BGR2RGB)
        h,w=im.shape[:2]; r=2400/max(h,w)
        if r<1: im=cv2.resize(im,(int(w*r),int(h*r)),interpolation=cv2.INTER_AREA)
        PH[k]=im
    return PH[k]
def kb(k,t,t0,t1,a,b):
    u=ease(seg(t,t0,t1)); cx=lerp(a[0],b[0],u); cy=lerp(a[1],b[1],u); z=lerp(a[2],b[2],u)
    im=ph(k); h,w=im.shape[:2]; s=max(W/w,H/h)*z
    cxp=min(max(cx*w,W/(2*s)),w-W/(2*s)); cyp=min(max(cy*h,H/(2*s)),h-H/(2*s))
    M=np.array([[s,0,W/2-s*cxp],[0,s,H/2-s*cyp]],np.float32)
    return cv2.warpAffine(im,M,(W,H),flags=cv2.INTER_AREA if s<1 else cv2.INTER_LINEAR).astype(np.float32)
def grade(fr,h,t):
    if h<=0.01: return fr
    g=fr.mean(2,keepdims=True); fr=fr*(1-0.55*h)+g*0.55*h
    ox=int(t*20)%300; oy=int(t*9)%300
    hz=HZ1[oy:oy+H,ox:ox+W]*0.6+HZ2[oy+60:oy+60+H,ox+40:ox+40+W]*0.4; ha=np.clip((hz-0.2)*1.4,0,1)*h*0.55
    col=np.array((172,142,98),np.float32)
    fr=fr*(1-h*0.38)+col*h*0.38; fr=fr*(1-ha[...,None])+col*ha[...,None]
    pt=particles(t,int(40+160*h),5,0.8*h,None); fr=fr*(1-pt[...,None]*0.5)+np.array((210,175,120),np.float32)*pt[...,None]*0.5
    return fr
def vg(fr,top=0.0,bot=0.0,th=0.35,bh=0.35):
    y=np.linspace(0,1,H,dtype=np.float32)[:,None,None]; k=1-top*np.clip(1-y/th,0,1)-bot*np.clip((y-(1-bh))/bh,0,1); return fr*k
def blurdark(fr,k=0.4,bl=22): return cv2.GaussianBlur(fr,(0,0),bl)*k
# ---- beats
def B0(t):
    fr=kb(9,t,0,3.0,(0.22,0.52,1.0),(0.74,0.52,1.08)); fr=vg(fr,0.0,0.7,bh=0.3); lay=L()
    lay.t((60,1380),"EVERY WINTER,",AN(112),CREAM,eo3(seg(t,0.2,0.5)),sw=10); lay.t((60,1505),"THEY COME TO DELHI.",AN(112),ACC,eo3(seg(t,0.5,0.85)),sw=10)
    return composite(fr,lay)
def B1(t):
    st=t-3.0; h=0.05+0.80*ease(seg(t,3.2,5.8)); fr=kb(2,t,3.0,7.0,(0.58,0.50,1.0),(0.58,0.50,1.12)); fr=grade(fr,h,t); fr=vg(fr,0.55,0.55,th=0.4,bh=0.3); lay=L()
    ta=seg(t,3.2,3.6); v=int(lerp(62,367,ease(seg(t,3.3,5.3)))); col=aqi_col(v)
    lay.t((W//2,250),"DELHI AQI  |  5 NOV 2026, 9 AM",BC(54),CREAM,eo3(ta),anchor='mm',sw=6)
    sc2=1+0.05*math.sin(t*14)*seg(t,5.3,5.6)*(1-seg(t,5.6,6.2))
    lay.t((W//2,470),str(v),AN(330*sc2),col,eo3(ta),anchor='mm',sw=12)
    bx0,bx1,by=110,970,660
    for i,c in enumerate([(120,220,90),(240,210,60),(255,140,30),(235,60,50),(160,20,60)]):
        x0=bx0+(bx1-bx0)*i/5; lay.d.rectangle((x0,by,x0+(bx1-bx0)/5-4,by+22),fill=c+(int(230*eo3(ta)),))
    mx=bx0+(bx1-bx0)*cl(v/500); lay.d.polygon([(mx,by-6),(mx-16,by-38),(mx+16,by-38)],fill=WHT+(int(255*eo3(ta)),))
    lay.t((W//2,1440),"SOME AREAS CROSSED 400: SEVERE",BC(60),RED,eo3(seg(t,5.6,6.1)),anchor='mm',sw=8)
    lay.t((W//2,1550),"NOW LOOK AT THE COUNTS.",AN(80),WHT,eo3(seg(t,6.0,6.5)),anchor='mm',sw=9)
    return composite(fr,lay)
def count(t,t0,key,a_,b_,name,a,b,yrs,focus):
    st=t-t0; fr=kb(key,t,t0,t0+4.5,focus[0],focus[1]); fr=grade(fr,0.15,t); fr=vg(fr,0.75,0.55,th=0.36,bh=0.2); lay=L()
    lay.t((W//2,200),name,AN(104),CREAM,eo3(seg(st,0.0,0.35)),anchor='mm',sw=10)
    lay.t((W//2,290),"ASIAN WATERBIRD CENSUS",BC(46),ACC,eo3(seg(st,0.1,0.4)),anchor='mm',sw=6)
    k1=eob(seg(st,0.25,0.65),2.0); lay.t((270,450),f"{a:,}",AN(int(140*max(0.05,k1))),CREAM,min(1,k1*1.5),anchor='mm',sw=11)
    lay.t((270,572),yrs[0],BC(46),(225,225,225),eo3(seg(st,0.4,0.7)),anchor='mm',sw=5)
    kb_=eo3(seg(st,0.9,1.2)); vb=int(a-(a-b)*ease(seg(st,1.0,2.2)))
    lay.t((540,450),"→",AN(110),ACC,kb_,anchor='mm',sw=9)
    lay.t((810,450),f"{vb:,}",AN(140),RED,kb_,anchor='mm',sw=11); lay.t((810,572),yrs[1],BC(46),(225,225,225),kb_,anchor='mm',sw=5)
    pc=int(round((1-b/a)*100)); kp=eob(seg(st,2.3,2.8),2.2)
    lay.t((W//2,1470),f"-{pc}%",AN(int(260*max(0.05,min(1,kp)))),RED,min(1,kp*1.5),anchor='mm',sw=14)
    lay.t((W//2,1600),"Counts change with year, rain and method.",BM(32),(225,225,225),eo3(seg(st,3.0,3.4)),anchor='mm',sw=0,shadow=False)
    return composite(fr,lay)
def B2(t): return count(t,7.0,4,0,0,"NAJAFGARH JHEEL",27673,10592,("2021","2022"),((0.58,0.50,1.0),(0.58,0.50,1.12)))
def B3(t): return count(t,11.5,8,0,0,"SULTANPUR",9026,2686,("2023","2024"),((0.52,0.55,1.0),(0.55,0.52,1.1)))
def B4(t):
    fr=kb(6,t,15.5,21.0,(0.45,0.62,1.0),(0.45,0.58,1.18)); fr=grade(fr,0.25,t); return np.clip(fr,0,255)
def B5(t):
    st=t-22.3; fr=kb(3,t,22.3,26,(0.60,0.52,1.0),(0.60,0.52,1.12)); fr=grade(fr,0.1+0.5*ease(seg(t,22.5,25.5)),t); fr=vg(fr,0.55,0.6,th=0.34,bh=0.3); lay=L()
    lay.t((W//2,260),"WHAT SMOG DOES TO BIRDS",BC(56),ACC,eo3(seg(st,0.0,0.3)),anchor='mm',sw=6)
    multi(lay,380,[("FINE PARTICLES CAN ",WHT)],AN(78),eo3(seg(st,0.3,0.7)),9); multi(lay,480,[("INFLAME",ACC),(" BIRD LUNGS",WHT)],AN(96),eo3(seg(st,0.6,1.0)),10)
    pill(lay,1520,"RESEARCH REVIEW, 2025",ORG,eo3(seg(st,1.1,1.5)))
    return composite(fr,lay)
def B6(t):
    st=t-26.0; fr=kb(5,t,26,30,(0.55,0.60,1.0),(0.55,0.60,1.15)); fr=grade(fr,0.6,t); fr=vg(fr,0.6,0.6,th=0.4,bh=0.3); lay=L()
    k=eob(seg(st,0.1,0.5),2.2); lay.t((W//2,380),"~25",AN(int(320*max(0.05,k))),ORG,min(1,k*1.5),anchor='mm',sw=14)
    multi(lay,580,[("BIRDS WITH ",WHT),("WATERY EYES",ACC)],AN(80),eo3(seg(st,0.5,0.9)),9)
    pill(lay,1490,"ONE EAST DELHI CLINIC, DEC 2025. NOT A CENSUS.",ORG,eo3(seg(st,1.2,1.6)),BC(36))
    return composite(fr,lay)
def B7(t):
    st=t-31.3; fr=kb(1,t,31.3,35.3,(0.50,0.58,1.0),(0.50,0.52,1.1)); fr=grade(fr,0.12,t)
    # foam on the water (lower part)
    r=np.random.default_rng(9); f=np.zeros((H,W),np.float32)
    for i in range(int(40+260*ease(seg(st,0.5,3.5)))): cv2.circle(f,(int((r.random()*W+t*r.uniform(10,40))%W),int(1300+(r.random()*620+t*r.uniform(10,50))%620)),int(r.uniform(4,16)),1.0,-1,cv2.LINE_AA)
    f=cv2.GaussianBlur(f,(0,0),2)*0.7; fr=fr*(1-f[...,None])+np.array((240,240,236),np.float32)*f[...,None]
    fr=vg(fr,0.6,0.15,th=0.36,bh=0.2); lay=L()
    lay.t((W//2,260),"YAMUNA, DELHI",BC(56),TEAL,eo3(seg(st,0.0,0.3)),anchor='mm',sw=6)
    k=eob(seg(st,0.1,0.5),2.2); lay.t((W//2,380),"22 KM",AN(int(270*max(0.05,k))),TEAL,min(1,k*1.5),anchor='mm',sw=14)
    multi(lay,540,[("MOST POLLUTED OF ",WHT),("INDIA'S 311",ACC)],BC(58),eo3(seg(st,0.5,0.9)),7); multi(lay,600,[("POLLUTED RIVER STRETCHES",WHT)],BC(58),eo3(seg(st,0.7,1.1)),7)
    pill(lay,1560,"CEEW",TEAL,eo3(seg(st,1.2,1.6)))
    return composite(fr,lay)
def B8(t):
    st=t-35.3; fr=blurdark(kb(9,t,35.3,40,(0.5,0.55,1.0),(0.55,0.55,1.1)),0.45,8); lay=L()
    lay.t((W//2,300),"CPCB TEST, 2018",BC(54),ACC,eo3(seg(st,0.0,0.3)),anchor='mm',sw=6)
    n=int(17*ease(seg(st,0.3,1.6)))
    for i in range(17):
        cx=110+(i%6)*170; cy=500+(i//6)*170; on=i<13
        if i<n: lay.d.ellipse((cx-52,cy-52,cx+52,cy+52),fill=((235,60,50) if on else (90,110,100))+(255,),outline=WHT+(255,),width=5)
    k=eob(seg(st,1.6,2.1),2.0); lay.t((W//2,1090),"13 OF 17",AN(int(230*max(0.05,k))),RED,min(1,k*1.5),anchor='mm',sw=12)
    multi(lay,1260,[("SPOTS: AMMONIA ABOVE THE ",WHT),("SAFE LIMIT",ACC)],BC(58),eo3(seg(st,2.0,2.4)),7)
    pill(lay,1370,"HARYANA TO DELHI",TEAL,eo3(seg(st,2.4,2.8)))
    return composite(fr,lay)
def B9(t):
    st=t-41.3; fr=blurdark(kb(8,t,41.3,47,(0.5,0.5,1.1),(0.55,0.5,1.2)),0.4,18); lay=L()
    lay.t((60,230),"BUT IT IS NOT",AN(110),CREAM,eo3(seg(st,0.1,0.5)),sw=9); lay.t((60,355),"ONLY THE AIR.",AN(135),ORG,eo3(seg(st,0.3,0.7)),sw=10)
    chips=[("DRYING WETLANDS",TEAL),("DIRTY WATER",(120,220,90)),("DUST AND BUILDING",AMB),("LATE, WARMER WINTERS",(235,110,110))]
    for i,(c,col) in enumerate(chips):
        k=eob(seg(st,1.0+i*1.1,1.4+i*1.1))
        if k>0: lay.chip((60,700+i*170),c,BC(64),col,min(1,k),pad=34)
    return composite(fr,lay)
def B10(t):
    st=t-47.0; fr=kb(6,t,47,51,(0.40,0.70,1.1),(0.40,0.66,1.22)); fr=grade(fr,0.3,t); fr=vg(fr,0.65,0.6,th=0.4,bh=0.3); lay=L()
    lay.t((W//2,330),"EXPERTS STILL DEBATE",BC(70),CREAM,eo3(seg(st,0.2,0.6)),anchor='mm',sw=7); lay.t((W//2,430),"HOW MUCH IS THE AIR ALONE.",BC(70),ACC,eo3(seg(st,0.6,1.0)),anchor='mm',sw=7)
    pill(lay,1520,"HABITAT, WATER, CLIMATE ALL MATTER",ORG,eo3(seg(st,1.6,2.0)),BC(38))
    return composite(fr,lay)
def B11(t):
    st=t-51.0; h=0.6*(1-ease(seg(st,0.5,5.0))); fr=kb(1,t,51,57,(0.50,0.52,1.0),(0.50,0.48,1.12)); fr=grade(fr,h,t); fr=vg(fr,0.55,0.6,th=0.36,bh=0.3); lay=L()
    lay.t((60,270),"PROTECT",AN(150),CREAM,eo3(seg(st,0.2,0.6)),sw=11); lay.t((60,440),"THE WETLANDS.",AN(150),ACC,eo3(seg(st,0.5,0.9)),sw=11)
    lay.t((60,1380),"DELHI'S AIR",AN(88),CREAM,eo3(seg(st,2.2,2.6)),sw=9); lay.t((60,1480),"PART 1 OF 3",AN(88),ORG,eo3(seg(st,2.5,2.9)),sw=9)
    lay.t((60,1610),"Photos: Hitesh Chawla  |  @thenaturalangle",BM(36),(235,235,235),eo3(seg(st,3.4,3.9)),sw=0,shadow=False)
    return composite(fr,lay)
def B12(t):
    fr=kb(7,t,57,63,(0.50,0.52,1.0),(0.50,0.50,1.12)); return np.clip(grade(fr,0.0,t),0,255)
BEATS3=[(0,3,B0,[0.05]),(3,7,B1,[3.3,5.3,5.9]),(7,11.5,B2,[7.3,8.3,9.6]),(11.5,15.5,B3,[11.8,12.8,14.1]),(15.5,21,B4,[]),
 (21,22.3,lambda t:chapter(t,21,"01","THE AIR"),[]),(22.3,26,B5,[22.4,23.0]),(26,30,B6,[26.1]),
 (30,31.3,lambda t:chapter(t,30,"02","THE WATER",TEAL),[]),(31.3,35.3,B7,[31.4]),(35.3,40,B8,[37.4]),
 (40,41.3,lambda t:chapter(t,40,"03","NOT ONLY AIR",ORG),[]),(41.3,47,B9,[42.3,43.4,44.5,45.6]),(47,51,B10,[47.1]),(51,57,B11,[51.2]),(57,63,B12,[])]
WHIPS3=[21,30,40]
def frame3(i):
    t=min(i/FPS,TOTAL3-1e-3)
    for a,b,f,pk in BEATS3:
        if a<=t<b:
            fr=f(t).astype(np.float32); s=punch(t,pk)*(1+0.02*(t-a)/(b-a)); bl=0
            for w in WHIPS3:
                if w<=t<w+0.22: u=1-(t-w)/0.22; s*=1+0.5*u*u; bl=max(bl,45*u*u)
                if w+1.3-0.2<=t<w+1.3: u=(t-(w+1.3-0.2))/0.2; s*=1+0.5*u*u; bl=max(bl,45*u*u)
                if w+1.3<=t<w+1.5: u=1-(t-(w+1.3))/0.2; s*=1+0.25*u*u; bl=max(bl,25*u*u)
            return np.clip(zoomf(fr,s,bl),0,255).astype(np.uint8)
    return np.zeros((H,W,3),np.uint8)
