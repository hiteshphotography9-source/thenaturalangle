import sys, json, math, os
SPD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/"
sys.path.insert(0,SPD+"s3tiger")
from tscenes import *
import tscenes as T
OFFV=0.5
PH=[(a+OFFV,b+OFFV,l) for a,b,l in json.load(open(SPD+"s3tiger/vo/phrases.json"))]
ORDER=["S1","S2","S3","S4","S5","S6","end"]
START={"S1":0.0,"S2":PH[4][0]-0.35,"S3":PH[7][0]-0.35,"S4":PH[10][0]-0.35,"S5":PH[14][0]-0.45,"S6":PH[19][0]-0.35,"end":PH[23][1]+0.9}
TOTAL=START["end"]
def P0(n,i): return PH[i][0]-START[n]       # phrase i start in scene-local seconds
def P1(n,i): return PH[i][1]-START[n]
AMBR=(255,196,70)
# ---------------- S1 hook
def S1(lt,t):
    L1=START["S1"]; D=START["S2"]
    a=fb("t5",0.5,0.9,z=1.0+0.08*seg(lt,0,D),pan=(0,0.012*seg(lt,0,D))); a=a*np.array((1.05,1.0,0.92),np.float32)
    img=arr2img(a); scrim(img,1280,1920,0.0,0.86,(4,10,8)); scrim(img,0,330,0.7,0.0,(4,10,8)); brand(img,CREAM,170); head(img,"PILIBHIT TIGER RESERVE",lt)
    p=P0("S1",0); ia=eo3(seg(lt,p,p+0.35)); comp(img,glayer((W/2,1590),"THE TIGER CALLED S3",A(104),top=(255,250,240),bot=(255,208,120)),ia,sc=lerp(1.3,1,eob(seg(lt,p,p+0.4),1.3)))
    d=ImageDraw.Draw(img,"RGBA")
    p1=P0("S1",1); p2=P0("S1",2)
    txt(d,(W/2,214),"ALSO KNOWN AS",B(32),CREAM,230*eo3(seg(lt,p1-0.2,p1+0.1)))
    f=B(54); w1=f.getlength("SURAI 3"); w2=f.getlength("MONARCH"); gap=70; x1=W/2-(w1+w2+gap)/2+w1/2; x2=x1+w1/2+gap+w2/2
    a1=eo3(seg(lt,p1,p1+0.3)); a2=eo3(seg(lt,p2,p2+0.3))
    if a1>0: pill(img,(W/2-(w2+gap)/2-0,262),"SURAI 3",f,a1,fg=INK,bg=GOLD2,sc=lerp(0.8,1,eob(seg(lt,p1,p1+0.35))),pad=(26,10))
    if a2>0: pill(img,(W/2+(w1+gap)/2+0,262),"MONARCH",f,a2,fg=INK,bg=GOLD2,sc=lerp(0.8,1,eob(seg(lt,p2,p2+0.35))),pad=(26,10))
    p3=P0("S1",3); a3=eo3(seg(lt,p3+0.2,p3+0.6)); txt(d,(W/2,1670),"ONE OF PILIBHIT'S BIGGEST TIGERS",B(48),CREAM,255*a3)
    pa=eo3(seg(lt,p3+1.4,p3+1.8)); pill(img,(W/2,1780),"HOW BIG? AND HOW DID HE SURVIVE?",B(44),pa,fg=INK,bg=GOLD2,sc=lerp(0.8,1,eob(seg(lt,p3+1.4,p3+1.9))))
    return img
# ---------------- S2 ID card
ROWS2=[("NAME","S3  ·  SURAI 3  ·  MONARCH",GRN,"ok",None),("PLACE","PILIBHIT TIGER RESERVE, UP",GRN,"ok",None),("WEIGHT","280 TO 300 KG",AMBR,"rep",("S2",1.9)),("LENGTH","ABOUT 10 FEET",AMBR,"rep",("S2",3.9)),("AGE","ABOUT 6 TO 7 YEARS",GRN,"ok",("S2b",0.25))]
def S2(lt,t):
    D=START["S3"]-START["S2"]
    img=fbg(t); brand(img,CREAM,150); head(img,"THE ID CARD",lt)
    fwin(img,"t2",wbox("t2",0.52,0.48,0.52,(60,200,960,560)),(60,200,960,560),z=1.0+0.05*seg(lt,0,D),spot=(0.52,0.45,0.2,0.28),k=eo3(seg(lt,0.1,0.7)),border=GOLD2)
    d=ImageDraw.Draw(img,"RGBA")
    base=P0("S2",4)
    for i,(lab,val,col,kind,tm) in enumerate(ROWS2):
        if tm is None: t0=0.3+i*0.55
        elif tm[0]=="S2": t0=base+tm[1]
        else: t0=P0("S2",6)+tm[1]
        a=eo3(seg(lt,t0,t0+0.35)); y=860+i*135
        if a<=0: continue
        x0=60+(1-a)*60
        d.rounded_rectangle((x0,y-56,x0+960,y+56),radius=22,fill=(14,34,28,int(228*a)),outline=col+(int(210*a),),width=3)
        txt(d,(x0+34,y-10),lab,BM(28),GREY,255*a,"ls"); f=B(56) if len(val)<20 else B(46); txt(d,(x0+34,y+40),val,f,col,255*a,"ls")
        cx,cy=x0+900,y
        if kind=="ok": d.ellipse((cx-24,cy-24,cx+24,cy+24),fill=GRN+(int(255*a),)); d.line((cx-11,cy,cx-3,cy+9,cx+13,cy-10),fill=(10,26,20,int(255*a)),width=6,joint="curve")
        else: d.ellipse((cx-24,cy-24,cx+24,cy+24),outline=col+(int(255*a),),width=4); txt(d,(cx,cy+14),"i",B(40),col,255*a)
    pn=P0("S2",5); ka=eo3(seg(lt,pn,pn+0.4)); pill(img,(W/2,1600),"WEIGHT + LENGTH: NOT OFFICIAL",B(42),ka,fg=INK,bg=AMBR,sc=lerp(0.85,1,eob(seg(lt,pn,pn+0.45))))
    txt(d,(W/2,1670),"As told by local guides",BM(32),GREY,230*eo3(seg(lt,pn+0.5,pn+0.9)))
    return img
# ---------------- S3 rival
def S3(lt,t):
    D=START["S4"]-START["S3"]
    img=fbg(t); brand(img,CREAM,150); head(img,"THE RIVAL",lt)
    fwin(img,"t3",wbox("t3",0.5,0.55,0.95,(60,200,960,420)),(60,200,960,420),z=1.0+0.05*seg(lt,0,D),spot=(0.5,0.55,0.2,0.2),k=eo3(seg(lt,0.1,0.7)),border=GOLD2)
    cx,cy=540,930
    ta=eo3(seg(lt,0.2,0.7)); tl_=L(); dtl=ImageDraw.Draw(tl_,"RGBA"); dtl.ellipse((cx-310,cy-215,cx+310,cy+215),fill=(110,205,125,40),outline=GRN+(240,),width=4); comp(img,tl_,ta); d=ImageDraw.Draw(img,"RGBA")
    d.ellipse((cx-70-26,cy-18,cx-70+26,cy+34),fill=GOLD2+(int(255*ta),)); txt(d,(cx-70,cy+16),"S3",B(30),INK,255*ta)
    p7=P0("S3",7); ra=ease(seg(lt,p7+0.1,p7+1.1)); pulse=0.5+0.5*math.sin(lt*7)
    if ra>0:
        rx=lerp(980,cx+190,ra); ry=cy+lerp(120,10,ra); d.ellipse((rx-26,ry-18,rx+26,ry+34),fill=RED2+(255,)); txt(d,(rx,ry+16),"S2",B(30),INK,255)
        if ra>0.95:
            pc=P0("S3",9); k=eo3(seg(lt,pc,pc+0.4)); d.line((cx-40,cy+10,rx-30,ry+10),fill=RED2+(int((120+100*pulse)*k),),width=6)
    ka=eo3(seg(lt,p7+1.2,p7+1.7)); l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((70,1260,1010,1500),radius=28,fill=(10,26,20,240),outline=RED2+(255,),width=4); comp(img,l,ka,sc=lerp(0.92,1,eob(seg(lt,p7+1.2,p7+1.8))))
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1370),"S3'S BIGGEST RIVAL",B(52),CREAM,255*ka); comp(img,glayer((W/2,1465),"S2",A(110),top=(255,170,150),bot=RED2),ka)
    p8=P0("S3",8); k8=eo3(seg(lt,p8,p8+0.35)); txt(d,(W/2,1580),"As told by local guides",BM(34),GREY,255*k8)
    p9=P0("S3",9); k9=eo3(seg(lt,p9,p9+0.4)); txt(d,(W/2,1640),"Two big males. One territory.",B(44),CREAM,255*k9)
    return img
# ---------------- S4 fight
def S4(lt,t):
    D=START["S5"]-START["S4"]
    p10,p11,p12,p13=P0("S4",10),P0("S4",11),P0("S4",12),P0("S4",13)
    hit=p10+1.9
    img=fbg(t); brand(img,CREAM,150); head(img,"THE NEAR-DEATH FIGHT",lt)
    fwin(img,"t4",wbox("t4",0.58,0.55,0.8,(60,200,960,500)),(60,200,960,500),z=1.0+0.05*seg(lt,0,D),spot=(0.57,0.62,0.18,0.3),k=eo3(seg(lt,0.1,0.7)),border=RED2 if hit<lt<p12 else GOLD2,desat=0.6*ease(seg(lt,hit,hit+0.8))*(1-ease(seg(lt,p13,p13+1.2))))
    d=ImageDraw.Draw(img,"RGBA")
    ev=eo3(seg(lt,0.2,0.6)); txt(d,(W/2,800),"S3'S HEALTH",B(40),CREAM,255*ev)
    v=1.0-0.94*ease(seg(lt,hit,hit+0.9)); 
    if lt>=p13: v=0.06+0.80*ease(seg(lt,p13,p13+1.6))
    col=GRN if v>0.55 else (AMBR if v>0.25 else RED2)
    d.rounded_rectangle((90,840,990,920),radius=40,fill=(20,44,36,int(230*ev)))
    if ev>0: d.rounded_rectangle((90,840,90+max(40,860*v+40),920),radius=40,fill=col+(255,))
    if hit<lt<hit+0.7: txt(d,(W/2,1010),"S2 ATTACKS",A(96),RED2,255*(1-seg(lt,hit+0.45,hit+0.7)))
    na=eo3(seg(lt,p11+0.5,p11+0.9))*(1-eo3(seg(lt,p12+0.1,p12+0.5)))
    if na>0.01: pu=0.6+0.4*math.sin(lt*8); comp(img,glayer((W/2,1080),"NEARLY DIED",A(124),top=(255,170,150),bot=RED2),na*pu,sc=lerp(1.2,1,eob(seg(lt,p11+0.5,p11+1.0),1.3)))
    d=ImageDraw.Draw(img,"RGBA")
    ra=eo3(seg(lt,p12,p12+0.4))
    if ra>0:
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((90,1130,990,1330),radius=30,fill=(10,30,24,245),outline=GRN+(255,),width=4); comp(img,l,ra,sc=lerp(0.9,1,eob(seg(lt,p12,p12+0.5))))
        d=ImageDraw.Draw(img,"RGBA"); cx_,cy_=190,1230; d.ellipse((cx_-46,cy_-46,cx_+46,cy_+46),fill=GRN+(int(255*ra),)); d.rectangle((cx_-8,cy_-28,cx_+8,cy_+28),fill=(10,26,20,int(255*ra))); d.rectangle((cx_-28,cy_-8,cx_+28,cy_+8),fill=(10,26,20,int(255*ra)))
        txt(d,(260,1215),"FOREST OFFICIALS STEP IN",B(48),CREAM,255*ra,"ls"); txt(d,(260,1275),"And bring him back from the edge.",B(34),GRN,255*eo3(seg(lt,p12+0.5,p12+0.9)),"ls")
    sv=eo3(seg(lt,p13,p13+0.35)); comp(img,glayer((W/2,1520),"HE SURVIVED.",A(130),top=(255,250,240),bot=GOLD2),sv,sc=lerp(1.3,1,eob(seg(lt,p13,p13+0.45),1.3)))
    return img
# ---------------- S5 survivor
def S5(lt,t):
    D=START["S6"]-START["S5"]
    p14,p15,p16,p17,p18=[P0("S5",i) for i in range(14,19)]
    img=fbg(t); brand(img,CREAM,150); head(img,"AND TODAY?",lt)
    zz=1.0+0.2*ease(seg(lt,p15,p17+0.8)); pan=(0,0.12*ease(seg(lt,p15,p17+0.8)))
    fwin(img,"t5",wbox("t5",0.5,0.45,0.95,(60,200,960,880)),(60,200,960,880),z=zz,pan=pan,spot=(0.5,0.45,0.28,0.28),k=eo3(seg(lt,0.1,0.7)),border=GOLD2)
    d=ImageDraw.Draw(img,"RGBA")
    for i,(t0,s) in enumerate([(p15,"THICK, POWERFUL NECK"),(p16,"HEAVY FOREARMS"),(p17,"FULL, HEALTHY COAT")]):
        a=eo3(seg(lt,t0,t0+0.35)); y=1150+i*100
        if a<=0: continue
        d.rounded_rectangle((120,y-40,960,y+40),radius=24,fill=(14,34,28,int(230*a)),outline=GRN+(int(220*a),),width=3); d.ellipse((140,y-20,180,y+20),fill=GRN+(int(255*a),)); d.line((149,y,158,y+9,172,y-9),fill=(10,26,20,int(255*a)),width=5)
        txt(d,(206+(1-a)*40,y+14),s,B(46),CREAM,255*a,"ls")
    ka=eo3(seg(lt,p18,p18+0.4)); comp(img,glayer((W/2,1560),"A SURVIVOR'S BUILD.",A(70),top=(255,250,240),bot=GOLD2),ka,sc=lerp(1.2,1,eob(seg(lt,p18,p18+0.45),1.3)))
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1625),"What the photo shows. Not a measurement.",B(36),CREAM,255*eo3(seg(lt,p18+0.5,p18+0.9)))
    return img
# ---------------- S6 CTA
def S6(lt,t):
    D=START["end"]-START["S6"]
    p19,p20,p21,p22,p23=[P0("S6",i) for i in range(19,24)]
    a=fb("t1",0.5,0.9,z=1.0+0.05*seg(lt,0,D)); a=a*np.array((1.05,1.0,0.92),np.float32)*(1-0.12*seg(lt,0,D))
    img=arr2img(a); scrim(img,1000,1920,0.0,0.93,(4,10,8)); scrim(img,0,330,0.7,0.0,(4,10,8)); brand(img,CREAM,170); head(img,"SEE HIM IN PERSON",lt)
    d=ImageDraw.Draw(img,"RGBA")
    q=eo3(seg(lt,p19,p19+0.4)); txt(d,(W/2,1190),"WANT TO SEE HIM",B(58),CREAM,255*q); w=eo3(seg(lt,p19+1.0,p19+1.4)); comp(img,glayer((W/2,1300),"IN PERSON?",A(112),top=(255,250,240),bot=GOLD2),w,sc=lerp(1.3,1,eob(seg(lt,p19+1.0,p19+1.5),1.3)))
    w=eo3(seg(lt,p20,p20+0.4)); comp(img,glayer((W/2,1430),"JOIN ME IN PILIBHIT",A(92),top=(255,250,240),bot=GOLD2),w,sc=lerp(1.3,1,eob(seg(lt,p20,p20+0.5),1.3)))
    btn=L(); ImageDraw.Draw(btn,"RGBA").rounded_rectangle((W/2-440,1485,W/2+440,1577),radius=46,fill=GOLD2+(250,)); ba=eo3(seg(lt,p21,p21+0.4)); comp(img,btn,ba,sc=lerp(0.6,1,eob(seg(lt,p21,p21+0.5))))
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1547),"DURING MY PILIBHIT SAFARIS",B(44),INK,255*eo3(seg(lt,p21+0.2,p21+0.5)))
    ka=eo3(seg(lt,p22,p22+0.4)); txt(d,(W/2,1660),"GET IN TOUCH ON INSTAGRAM",B(48),CREAM,255*ka); txt(d,(W/2,1730),"@thenaturalangle",A(60),GOLD2,255*eo3(seg(lt,p22+0.5,p22+0.9)))
    pa=eo3(seg(lt,p23,p23+0.35)); pill(img,(W/2,1805),"LINK BELOW",B(36),pa,fg=INK,bg=CREAM,sc=lerp(0.8,1,eob(seg(lt,p23,p23+0.4))),pad=(24,8))
    txt(d,(W/2,1870),"Photos: Hitesh Chawla, The Natural Angle",BM(24),GREY,200*eo3(seg(lt,p23,p23+0.6)))
    return img
FN={"S1":S1,"S2":S2,"S3":S3,"S4":S4,"S5":S5,"S6":S6}
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
    print(START,TOTAL)
    for tt in [float(a) for a in sys.argv[1:]]: Image.fromarray(frame(tt)).save(f"q_{tt:05.1f}.jpg",quality=85)
