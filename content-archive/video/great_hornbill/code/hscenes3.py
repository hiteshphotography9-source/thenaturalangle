import sys, json, math, os
SPD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/"
sys.path.insert(0,SPD+"hornbill")
import hscenes as H
from hscenes import *
OFFV=0.5
PHJ=json.load(open(SPD+"hornbill/vo2/phrases.json")); PV={int(k):(v[0]+OFFV,v[1]+OFFV) for k,v in PHJ.items()}
if 38 not in PV: PV[38]=(PV[37][1]+0.4,PV[37][1]+1.1)
ORDER=["S1","S2","S3","S4","S5","S6","S7","S8","S9","end"]
START={"S1":0.0,"S2":PV[3][0]-0.4,"S3":PV[7][0]-0.4,"S4":PV[13][0]-0.4,"S5":PV[17][0]-0.4,"S6":PV[20][0]-0.4,"S7":PV[26][0]-0.4,"S8":PV[29][0]-0.4,"S9":PV[35][0]-0.4,"end":PV[38][1]+0.7}
TOTAL=START["end"]
def P(n,i,o=0.0): return PV[i][0]+o-START[n]
def D(n): return START[ORDER[ORDER.index(n)+1]]-START[n]
# ---- S1
def S1(lt,t):
    n="S1"; Dn=D(n)
    img=bg(t); brand(img,CREAM,150); chip(img,"GREAT HORNBILL",lt)
    k=ease(seg(lt,0.3,Dn)); z=1.0+0.22*k; pan=(-0.06*k,0.02*k)
    fwin(img,"h1",wbox("h1",0.5,0.52,1.0,(60,520,960,720)),(60,520,960,720),z=z,pan=pan,spot=(0.4,0.6,0.3,0.28),k=0.5*eo3(seg(lt,0.3,1.2)),border=SUN)
    d=ImageDraw.Draw(img,"RGBA")
    for i,(s,o) in enumerate((("THIS BIRD CANNOT",P(n,0,0.0)),("BUILD ITS OWN HOME.",P(n,0,1.0)))):
        a=eo3(seg(lt,o,o+0.4)); comp(img,glayer((W/2,300+i*105),s,A(92),top=(255,250,240),bot=(255,208,120)),a,dy=(1-a)*30)
    o=P(n,1,0.0); a=eo3(seg(lt,o,o+0.4)); comp(img,glayer((W/2,1450),"IT CAN ONLY",A(104),top=(255,250,240),bot=(255,208,120)),a,sc=lerp(1.2,1,eob(seg(lt,o,o+0.5),1.3)))
    o=P(n,1,0.9); a=eo3(seg(lt,o,o+0.4)); comp(img,glayer((W/2,1565),"INHERIT ONE.",A(130),top=(255,236,200),bot=SUN),a,sc=lerp(1.3,1,eob(seg(lt,o,o+0.5),1.3)))
    o=P(n,2,0.0); d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1680),"GREAT HORNBILL  ·  INDIA",B(38),CREAM,230*eo3(seg(lt,o,o+0.4)))
    return img
# ---- S2
def S2(lt,t):
    n="S2"; Dn=D(n)
    img=bg(t); brand(img,CREAM,150); chip(img,"THE HOME",lt)
    zp=ease(seg(lt,P(n,5,0.0),P(n,5,2.2))); z=1.0+1.1*zp; pan=(0.0,0.25*zp)
    fwin(img,"h2",wbox("h2",0.5,0.5,1.0,(60,200,960,780)),(60,200,960,780),z=z,pan=pan,spot=(0.5,0.88,0.12,0.1),k=eo3(seg(lt,P(n,5,0.8),P(n,5,2.2))),border=SUN)
    d=ImageDraw.Draw(img,"RGBA")
    o=P(n,3,0.0); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1060),"NO DRILL. NO NEST BUILDING.",B(56),CREAM,255*a)
    o=P(n,4,0.0); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1130),"IT NEEDS A NATURAL HOLE IN A GIANT TREE.",B(38),SUN,255*a)
    for i,(lab,val,o,w_) in enumerate((("NEST TREES WERE TALLER BY","18.5 m",P(n,6,1.6),1.0),("AND WIDER (TRUNK) BY","0.85 m",P(n,6,4.4),0.5))):
        a=eo3(seg(lt,o,o+0.4)); y=1290+i*150
        if a<=0: continue
        row(d,60,y,960,120,SUN,a,lab,val); p=ease(seg(lt,o+0.2,o+1.1)); d.rounded_rectangle((90,y+50,90+780*p*w_,y+58),radius=4,fill=SUN+(int(255*a),))
    o=P(n,6,5.6); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1640),"Anaimalai Hills study: 24 nests vs unused forest sites",BM(28),GREY,230*a)
    o=P(n,6,6.0); a=eo3(seg(lt,o,o+0.4)); pill(img,(W/2,1730),"A HOME THAT TAKES DECADES TO GROW",B(40),a,fg=INK,bg=SUN,sc=lerp(0.85,1,eob(seg(lt,o,o+0.5))))
    return img
# ---- S3
def S3(lt,t):
    n="S3"; Dn=D(n)
    img=bg(t); brand(img,CREAM,150); chip(img,"THE TENANT",lt)
    fwin(img,"h3",wbox("h3",0.5,0.45,0.95,(60,200,960,900)),(60,200,960,900),z=1.0+0.06*seg(lt,0,Dn),spot=(0.45,0.38,0.3,0.25),k=eo3(seg(lt,0.2,1.0)),border=SUN)
    d=ImageDraw.Draw(img,"RGBA")
    items=[(P(n,7,0.0),"2 TO 4 KG  ·  WINGSPAN ABOUT 1.5 M"),(P(n,8,0.0),"WINGBEATS HEARD FROM FAR: A STEAM-ENGINE CHUFF"),(P(n,11,-0.2),"THE YELLOW? PREEN-GLAND OIL, WIPED ON")]
    for i,(o,s) in enumerate(items):
        a=eo3(seg(lt,o,o+0.35)); y=1190+i*120
        if a<=0: continue
        d.rounded_rectangle((60+(1-a)*60,y-48,1020+(1-a)*60,y+48),radius=24,fill=(14,34,28,int(228*a)),outline=SUN+(int(210*a),),width=3); txt(d,(100+(1-a)*60,y+14),s,B(38 if len(s)<42 else 33),CREAM,255*a,"ls")
    wa=eo3(seg(lt,P(n,8,0.0),P(n,8,0.4)))*(1-seg(lt,P(n,10,0.0),P(n,10,0.4)))
    if wa>0: waves3(d,900,420,lt,wa*0.9)
    o=P(n,12,0.0); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1620),"Colour source: preen-gland oil, per field and zoo accounts.",BM(26),GREY,200*a)
    return img
# ---- S4
def S4(lt,t):
    n="S4"; Dn=D(n); hit=P(n,15,1.8)
    img=bg(t); brand(img,CREAM,150); chip(img,"THE HELMET",lt)
    fl=max(0,1-abs(lt-hit)/0.25) if abs(lt-hit)<0.25 else 0
    fwin(img,"h1",wbox("h1",0.42,0.5,0.8,(60,220,960,800)),(60,220,960,800),z=1.0+0.1*seg(lt,0,Dn),spot=(0.52,0.4,0.2,0.2),k=0.5*eo3(seg(lt,0.3,1.2)),border=SUN,flash=fl*0.35)
    d=ImageDraw.Draw(img,"RGBA")
    o=P(n,13,0.0); a=eo3(seg(lt,o,o+0.4)); comp(img,glayer((W/2,1130),"HOLLOW CASQUE",A(100),top=(255,250,240),bot=(255,208,120)),a,sc=lerp(1.25,1,eob(seg(lt,o,o+0.5),1.3)))
    o=P(n,15,0.0); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1230),"MALES ARE KNOWN TO BUTT CASQUES IN MID-AIR",B(40),CREAM,255*a)
    o=P(n,16,0.0); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1310),"What is the casque for? Not fully known.",B(42),SUN,255*a)
    o=P(n,16,1.0); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1370),"Likely a status signal, say researchers.",BM(32),GREY,255*a)
    o=P(n,16,1.5); a=eo3(seg(lt,o,o+0.4)); pill(img,(W/2,1500),"A BIRD THAT WEARS ITS RANK",B(44),a,fg=INK,bg=SUN,sc=lerp(0.85,1,eob(seg(lt,o,o+0.5))))
    return img
# ---- S5
def S5(lt,t):
    n="S5"
    img=bg(t); brand(img,CREAM,150); chip(img,"WHERE DOES IT LIVE?",lt)
    cam,m=imap(); mk=Image.new("L",(960,1000),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,959,999),radius=26,fill=255); mp=Image.fromarray(m).convert("RGBA"); mp.putalpha(mk)
    ov=Image.new("RGBA",(960,1000),(0,0,0,0)); do=ImageDraw.Draw(ov,"RGBA"); o18=P(n,18,0.0)
    tms={"foot":o18+0.2,"ne":o18+1.9,"wg":o18+3.3}
    for key in ("foot","ne","wg"):
        t0=tms[key]; fa=ease(seg(lt,t0,t0+0.9)); pts=[cam.px(*p) for p in RANGES[key]]; do.polygon(pts,fill=SUN+(int(150*fa),),outline=SUN+(int(255*fa),)); do.line(pts+[pts[0]],fill=SUN+(int(255*fa),),width=3)
    for nm,lo,la,t0,(ox,oy) in (("PAKKE",92.99,27.1,o18+2.4,(-20,-50)),("ANAIMALAI",77.0,10.4,o18+3.6,(70,10))):
        a_=eo3(seg(lt,t0,t0+0.4))
        if a_<=0: continue
        x,y=cam.px(lo,la); r=((lt-t0)*0.9)%1; do.ellipse((x-9-r*34,y-9-r*34,x+9+r*34,y+9+r*34),outline=CREAM+(int(200*(1-r)*a_),),width=3); do.ellipse((x-10,y-10,x+10,y+10),fill=CREAM+(int(255*a_),))
        f=B(32); w=f.getlength(nm)+26; bx=min(max(x+ox-w/2,12),960-12-w); do.rounded_rectangle((bx,y+oy-30,bx+w,y+oy+22),radius=12,fill=(8,22,18,int(230*a_)),outline=SUN+(int(200*a_),),width=2); txt(do,(bx+13,y+oy+8),nm,f,CREAM,255*a_,"ls")
    for s,lo,la,t0 in (("HIMALAYAN FOOTHILLS",83.5,29.6,tms["foot"]),("NORTH-EAST",93.5,30.6,tms["ne"]),("WESTERN GHATS",72.2,12.8,tms["wg"])):
        a_=eo3(seg(lt,t0+0.2,t0+0.7)); x,y=cam.px(lo,la); txt(do,(min(max(x,170),790),y),s,B(32),CREAM,255*a_)
    mp.alpha_composite(ov); img.alpha_composite(mp,(60,230)); d=ImageDraw.Draw(img,"RGBA"); d.rounded_rectangle((58,228,1022,1232),radius=26,outline=SUN+(170,),width=3)
    o=P(n,19,0.0); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1320),"ALSO: NEPAL, BHUTAN, SOUTH CHINA,",B(40),CREAM,255*a); txt(d,(W/2,1372),"SOUTH-EAST ASIA, SUMATRA",B(40),CREAM,255*a)
    o=P(n,19,1.3); a=eo3(seg(lt,o,o+0.4)); pill(img,(W/2,1500),"IUCN STATUS: VULNERABLE",B(48),a,fg=INK,bg=RED2,sc=lerp(0.85,1,eob(seg(lt,o,o+0.5))))
    o=P(n,19,2.0); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1600),"It needs big, undisturbed forest. Those are shrinking.",B(36),SUN,255*a)
    txt(d,(W/2,1700),"Ranges illustrative. Map: Natural Earth. Status: IUCN Red List (2020).",BM(26),GREY,200)
    return img
# ---- S6
def S6(lt,t):
    n="S6"
    img=bg(t); brand(img,CREAM,150); chip(img,"THE GARDENER",lt)
    d=ImageDraw.Draw(img,"RGBA"); gy=900
    d.rectangle((60,gy,1020,1100),fill=(50,36,26,255)); d.rectangle((60,gy,1020,gy+8),fill=(90,140,70,255))
    ta=eo3(seg(lt,P(n,20,0.2),P(n,20,0.8))); tree(d,230,gy,520,ta)
    fa=eo3(seg(lt,P(n,22,-0.2),P(n,22,0.3)))
    for i in range(5): d.ellipse((150+i*35-9,gy-460-(i%2)*30-9,150+i*35+9,gy-460-(i%2)*30+9),fill=(230,80,60,int(255*fa)))
    f0=P(n,22,0.6); f1=P(n,23,1.0); p=ease(seg(lt,f0,f1))
    if f0<lt<f1+0.3: bird_icon(d,lerp(300,820,p),gy-340-math.sin(math.pi*p)*180,60,1,flap=math.sin(lt*14))
    dp=ease(seg(lt,P(n,23,0.7),P(n,23,1.3)))
    if dp>0:
        sy=lerp(gy-340,gy-6,dp); d.ellipse((820-12,sy-12,820+12,sy+12),fill=(230,80,60,255))
    sg=ease(seg(lt,P(n,24,0.0),P(n,24,2.6)))
    if sg>0: tree(d,820,gy,420*sg,min(1,sg*3),lc=(110,190,100))
    o=P(n,20,0.0); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,260),"IT DOES NOT JUST LIVE IN THE FOREST.",B(46),CREAM,255*a)
    o=P(n,21,0.0); comp(img,glayer((W/2,400),"IT GROWS IT.",A(110),top=(255,250,240),bot=(255,208,120)),eo3(seg(lt,o,o+0.4)),sc=lerp(1.2,1,eob(seg(lt,o,o+0.5),1.3)))
    d=ImageDraw.Draw(img,"RGBA")
    o=P(n,22,0.0); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1230),"SWALLOWS LARGE FRUIT, DROPS THE SEEDS FAR AWAY",B(38),CREAM,255*a)
    o=P(n,24,0.8); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1330),"69 TO 100%  of seeds landed away from the parent tree",B(40),SUN,255*a); txt(d,(W/2,1376),"(5 hornbill + tree pairs, Arunachal study)",BM(28),GREY,255*a)
    o=P(n,24,2.8); a=eo3(seg(lt,o,o+0.4)); pill(img,(W/2,1520),"HORNBILLS HELP GROW THE FOREST",B(42),a,fg=INK,bg=SUN,sc=lerp(0.85,1,eob(seg(lt,o,o+0.5))))
    return img
# ---- S7
def S7(lt,t):
    n="S7"; Dn=D(n)
    img=bg(t); brand(img,CREAM,150); chip(img,"THE PRICE",lt)
    fwin(img,"h3",wbox("h3",0.55,0.38,0.7,(60,200,960,800)),(60,200,960,800),z=1.0+0.1*seg(lt,0,Dn),spot=(0.5,0.28,0.25,0.18),k=eo3(seg(lt,0.2,1.0)),border=RED2)
    d=ImageDraw.Draw(img,"RGBA")
    o=P(n,26,0.0); a=eo3(seg(lt,o,o+0.4)); comp(img,glayer((W/2,1120),"A TROPHY ON ITS HEAD",A(96),top=(255,200,180),bot=RED2),a,sc=lerp(1.25,1,eob(seg(lt,o,o+0.5),1.3)))
    o=P(n,27,0.0); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1210),"The casque went into traditional headgear.",B(42),CREAM,255*a)
    for i,(o,s) in enumerate(((P(n,28,0.0),"HUNTING: MEAT, CASQUE, FEATHERS"),(P(n,28,1.0),"LOGGING: GIANT NEST TREES CUT"))):
        a=eo3(seg(lt,o,o+0.4)); y=1330+i*110
        if a<=0: continue
        d.rounded_rectangle((90,y-46,990,y+46),radius=22,fill=(40,16,14,int(230*a)),outline=RED2+(int(220*a),),width=3); d.ellipse((120,y-16,152,y+16),fill=RED2+(int(255*a),)); txt(d,(180,y+14),s,B(44),CREAM,255*a,"ls")
    o=P(n,28,1.8); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1620),"Even as the state bird of Arunachal Pradesh.",B(36),SUN,255*a)
    return img
# ---- S8
def S8(lt,t):
    n="S8"; Dn=D(n)
    img=bg(t); brand(img,CREAM,150); chip(img,"THE TURN",lt)
    fwin(img,"h2",wbox("h2",0.62,0.5,0.7,(60,200,960,640)),(60,200,960,640),z=1.0+0.06*seg(lt,0,Dn),spot=(0.66,0.45,0.2,0.3),k=eo3(seg(lt,0.2,1.0)),border=GRN)
    d=ImageDraw.Draw(img,"RGBA")
    o=P(n,30,0.0); comp(img,glayer((W/2,920),"HUNTERS BECAME GUARDIANS",A(80),top=(255,250,240),bot=(150,235,160)),eo3(seg(lt,o,o+0.4)),sc=lerp(1.2,1,eob(seg(lt,o,o+0.5),1.3)))
    o=P(n,31,0.0); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,990),"Hornbill Nest Adoption Program, Pakke, Arunachal Pradesh",B(34),CREAM,255*a)
    n1=int(10*ease(seg(lt,P(n,32,0.0),P(n,32,0.9)))); n2=int(119*ease(seg(lt,P(n,33,1.0),P(n,33,2.6))))
    for i,(o,lab,val) in enumerate(((P(n,32,0.0),"NYISHI NEST PROTECTORS",f"{n1}"),(P(n,33,0.0),"CHICKS FLEDGED, 2012 TO 2018",f"{n2}"))):
        a=eo3(seg(lt,o,o+0.4)); y=1130+i*150
        if a<=0: continue
        d.rounded_rectangle((90,y-62,990,y+62),radius=26,fill=(14,34,28,int(235*a)),outline=GRN+(int(230*a),),width=3); txt(d,(130,y+16),lab,B(40),CREAM,255*a,"ls"); txt(d,(950,y+30),val,A(84),GRN,255*a,"rs")
    o=P(n,34,0.0); a=eo3(seg(lt,o,o+0.4))
    if a>0: d.rounded_rectangle((90,1385,990,1485),radius=26,fill=(14,34,28,int(235*a)),outline=GRN+(int(230*a),),width=3); txt(d,(W/2,1448),"FIBREGLASS BEAKS NOW REPLACE REAL ONES IN HEADGEAR",B(34),CREAM,255*a)
    o=P(n,34,1.2); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1580),"Programme figures (NCF). Some protectors were hunters before.",B(32),SUN,255*a)
    o=P(n,34,1.8); a=eo3(seg(lt,o,o+0.4)); txt(d,(W/2,1650),"Pakke won the India Biodiversity Award 2016 for this work.",BM(30),GREY,255*a)
    return img
# ---- S9
def S9(lt,t):
    n="S9"; Dn=D(n)
    a=fb("h2",0.66,0.40,z=1.0+0.06*seg(lt,0,Dn),cy=0.45); a=a*np.array((1.04,1.0,0.94),np.float32)
    img=arr2img(a); scrim(img,1100,1920,0.0,0.92,(4,10,8)); scrim(img,0,320,0.7,0.0,(4,10,8)); brand(img,CREAM,170); chip(img,"THE GREAT HORNBILL",lt)
    d=ImageDraw.Draw(img,"RGBA")
    o=P(n,35,0.0); txt(d,(W/2,1280),"NEXT TIME IN THE FOREST,",B(54),CREAM,255*eo3(seg(lt,o,o+0.4))); o=P(n,35,1.3); txt(d,(W/2,1350),"DO NOT JUST LOOK AT THE BIRD.",B(54),CREAM,255*eo3(seg(lt,o,o+0.4)))
    o=P(n,36,0.0); comp(img,glayer((W/2,1500),"LOOK AT THE TREE.",A(112),top=(255,250,240),bot=SUN),eo3(seg(lt,o,o+0.4)),sc=lerp(1.3,1,eob(seg(lt,o,o+0.5),1.3)))
    o=P(n,38,0.0); btn=L(); ImageDraw.Draw(btn,"RGBA").rounded_rectangle((W/2-380,1590,W/2+380,1682),radius=46,fill=SUN+(250,)); comp(img,btn,eo3(seg(lt,o,o+0.4)),sc=lerp(0.6,1,eob(seg(lt,o,o+0.5))))
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1651),"FOLLOW THE NATURAL ANGLE",B(46),INK,255*eo3(seg(lt,o+0.2,o+0.5)))
    txt(d,(W/2,1745),"More forest stories every week",B(36),CREAM,255*eo3(seg(lt,o+0.6,o+1.0)))
    txt(d,(W/2,1840),"Photos: Hitesh Chawla. Sources: NCF, IUCN, Wikipedia, published studies.",BM(23),GREY,225*eo3(seg(lt,o+0.8,o+1.3)))
    return img
FN={"S1":S1,"S2":S2,"S3":S3,"S4":S4,"S5":S5,"S6":S6,"S7":S7,"S8":S8,"S9":S9}
def frame(t):
    i=max(j for j,n in enumerate(ORDER[:-1]) if START[n]<=t+1e-6); n=ORDER[i]; lt=t-START[n]
    fr=np.array(FN[n](lt,t))[...,:3].astype(np.float32)
    for m in ORDER[1:-1]:
        dd=t-START[m]
        if 0<=dd<0.18: fr=fr+(1-dd/0.18)*45
        if -0.1<dd<0: sc=1+0.05*(1+dd/0.1); fr=cv2.warpAffine(fr,np.array([[sc,0,W/2*(1-sc)],[0,sc,H/2*(1-sc)]],np.float32),(W,H),borderMode=cv2.BORDER_REFLECT)
    fade=min(1,t/0.2)*min(1,(TOTAL-t)/0.6)
    return T.finish(np.clip(fr*fade,0,255),t)
if __name__=="__main__":
    print({k:round(v,2) for k,v in START.items()},TOTAL)
    for tt in [float(a) for a in sys.argv[1:]]: Image.fromarray(frame(tt)).save(f"q_{tt:05.1f}.jpg",quality=85)
