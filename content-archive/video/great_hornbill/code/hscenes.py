import sys, json, math, os
SPD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/"
sys.path.insert(0,SPD+"s3tiger")
from tscenes import *          # helpers + fonts + palettes (also loads fscenes helpers)
import tscenes as T
ENT=[("S1",8),("S2",11),("S3",11),("S4",8),("S5",11),("S6",10),("S7",8),("S8",12),("S9",8)]
DES={}; _c=0
for n,l in ENT: DES[n]=(_c,l); _c+=l
START={n:DES[n][0] for n,_ in ENT}; START["end"]=_c
if os.path.exists(SPD+"hornbill/marks.json"): START.update(json.load(open(SPD+"hornbill/marks.json")))
TOTAL=START["end"]; ORDER=[n for n,_ in ENT]+["end"]
def FAC(n):
    i=ORDER.index(n); return DES[n][1]/(START[ORDER[i+1]]-START[n])
_txt0=txt
def txt(d,xy,s_,f,fill,a=255,anchor="ms"):
    if a>0.5: _txt0(d,xy,s_,f,fill,a,anchor)
SUN=(255,176,60); OR=(255,150,40); DEEP=(10,22,18)
def bg(t): return T.fbg(t,(8,20,16),(24,44,30))
def chip(img,s,lt,y=150): tchip(img,s,eo3(seg(lt,0.1,0.5)),y=y,col=SUN)
def row(d,x,y,w,h,col,a,lab,val,vcol=None):
    d.rounded_rectangle((x,y-h/2,x+w,y+h/2),radius=22,fill=(14,34,28,int(228*a)),outline=col+(int(210*a),),width=3)
    txt(d,(x+30,y-8),lab,BM(26),GREY,255*a,"ls"); txt(d,(x+30,y+38),val,B(46),vcol or col,255*a,"ls")
# ---------- S1 hook
def S1(lt,t):
    img=bg(t); brand(img,CREAM,150); chip(img,"GREAT HORNBILL",lt)
    z=1.0+0.22*ease(seg(lt,0.5,8)); pan=(-0.06*ease(seg(lt,0.5,8)),0.02*ease(seg(lt,0.5,8)))
    fwin(img,"h1",wbox("h1",0.5,0.52,1.0,(60,520,960,720)),(60,520,960,720),z=z,pan=pan,spot=(0.4,0.6,0.3,0.28),k=0.5*eo3(seg(lt,0.6,1.6)),border=SUN)
    d=ImageDraw.Draw(img,"RGBA")
    for i,(s,t0) in enumerate((("THIS BIRD CANNOT",0.3),("BUILD ITS OWN HOME.",1.2))):
        a=eo3(seg(lt,t0,t0+0.5)); comp(img,glayer((W/2,300+i*105),s,A(92),top=(255,250,240),bot=(255,208,120)),a,dy=(1-a)*30)
    a=eo3(seg(lt,3.6,4.2)); comp(img,glayer((W/2,1450),"IT CAN ONLY",A(104),top=(255,250,240),bot=(255,208,120)),a,sc=lerp(1.2,1,eob(seg(lt,3.6,4.3),1.3)))
    a=eo3(seg(lt,4.6,5.2)); comp(img,glayer((W/2,1565),"INHERIT ONE.",A(130),top=(255,236,200),bot=SUN),a,sc=lerp(1.3,1,eob(seg(lt,4.6,5.3),1.3)))
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1680),"A STORY OF TREES, SEEDS AND SECOND CHANCES",B(34),CREAM,230*eo3(seg(lt,6.2,6.8)))
    return img
# ---------- S2 the tree
def S2(lt,t):
    img=bg(t); brand(img,CREAM,150); chip(img,"THE HOME",lt)
    zp=ease(seg(lt,3.0,7.0)); z=1.0+1.1*zp; pan=(0.0,0.25*zp)
    fwin(img,"h2",wbox("h2",0.5,0.5,1.0,(60,200,960,780)),(60,200,960,780),z=z,pan=pan,spot=(0.5,0.88,0.12,0.1),k=eo3(seg(lt,3.6,5.0)),border=SUN)
    d=ImageDraw.Draw(img,"RGBA")
    a=eo3(seg(lt,0.3,0.9)); txt(d,(W/2,1060),"NO DRILL. NO NEST BUILDING.",B(56),CREAM,255*a)
    a=eo3(seg(lt,1.4,2.0)); txt(d,(W/2,1130),"IT NEEDS A NATURAL HOLE IN A GIANT TREE.",B(38),SUN,255*a)
    for i,(lab,val,v,t0) in enumerate((("NEST TREES WERE TALLER BY","18.5 m",18.5,5.2),("AND WIDER (TRUNK) BY","0.85 m",0.85,6.6))):
        a=eo3(seg(lt,t0,t0+0.4)); y=1290+i*150
        if a<=0: continue
        row(d,60,y,960,120,SUN,a,lab,val)
        p=ease(seg(lt,t0+0.2,t0+1.2)); d.rounded_rectangle((60+30,y+50,60+30+(780*p*(1.0 if i==0 else 0.5)),y+58),radius=4,fill=SUN+(int(255*a),))
    a=eo3(seg(lt,8.4,9.0)); txt(d,(W/2,1640),"Anaimalai Hills study: 24 nests vs unused forest sites",BM(28),GREY,230*a)
    a=eo3(seg(lt,9.4,10.0)); pill(img,(W/2,1730),"A HOME THAT TAKES DECADES TO GROW",B(40),a,fg=INK,bg=SUN,sc=lerp(0.85,1,eob(seg(lt,9.4,10.0))))
    return img
# ---------- S3 meet the tenant
def waves3(d,cx,cy,t,a):
    for k in range(3):
        u=((t/1.2)+k/3)%1; r=lerp(40,230,u); d.arc((cx-r,cy-r,cx+r,cy+r),start=-50,end=50,fill=SUN+(int(a*255*(1-u)),),width=6)
def S3(lt,t):
    img=bg(t); brand(img,CREAM,150); chip(img,"THE TENANT",lt)
    fwin(img,"h3",wbox("h3",0.5,0.45,0.95,(60,200,960,900)),(60,200,960,900),z=1.0+0.06*seg(lt,0,11),spot=(0.45,0.38,0.3,0.25),k=eo3(seg(lt,0.2,1.0)),border=SUN)
    d=ImageDraw.Draw(img,"RGBA")
    items=[(1.2,"2 TO 4 KG  ·  WINGSPAN ABOUT 1.5 M"),(4.2,"WINGBEATS HEARD FROM FAR: A STEAM-ENGINE CHUFF"),(7.4,"THE YELLOW? PREEN-GLAND OIL, WIPED ON")]
    for i,(t0,s) in enumerate(items):
        a=eo3(seg(lt,t0,t0+0.4)); y=1190+i*120
        if a<=0: continue
        d.rounded_rectangle((60+(1-a)*60,y-48,1020+(1-a)*60,y+48),radius=24,fill=(14,34,28,int(228*a)),outline=SUN+(int(210*a),),width=3); txt(d,(100+(1-a)*60,y+14),s,B(38 if len(s)<42 else 33),CREAM,255*a,"ls")
    wa=eo3(seg(lt,4.2,4.6))*(1-seg(lt,7.0,7.4)); 
    if wa>0: waves3(d,900,420,lt,wa*0.9)
    a=eo3(seg(lt,9.2,9.8)); txt(d,(W/2,1620),"Source: standard field accounts; oil colour per Wikipedia and zoo sources.",BM(26),GREY,200*a)
    return img
# ---------- S4 casque duel
def S4(lt,t):
    img=bg(t); brand(img,CREAM,150); chip(img,"THE HELMET",lt)
    fl=max(0,1-abs(lt-3.2)/0.25) if 3.0<lt<3.5 else 0
    fwin(img,"h1",wbox("h1",0.42,0.5,0.8,(60,220,960,800)),(60,220,960,800),z=1.0+0.1*seg(lt,0,8),spot=(0.52,0.4,0.2,0.2),k=0.5*eo3(seg(lt,0.3,1.2)),border=SUN,flash=fl*0.35)
    d=ImageDraw.Draw(img,"RGBA")
    a=eo3(seg(lt,0.6,1.2)); comp(img,glayer((W/2,1130),"HOLLOW CASQUE",A(100),top=(255,250,240),bot=(255,208,120)),a,sc=lerp(1.25,1,eob(seg(lt,0.6,1.3),1.3)))
    a=eo3(seg(lt,2.0,2.6)); txt(d,(W/2,1230),"MALES ARE KNOWN TO BUTT CASQUES IN MID-AIR",B(40),CREAM,255*a)
    a=eo3(seg(lt,4.0,4.6)); txt(d,(W/2,1310),"What is the casque for? Not fully known.",B(42),SUN,255*a)
    a=eo3(seg(lt,5.0,5.6)); txt(d,(W/2,1370),"Likely a status signal, say researchers.",BM(32),GREY,255*a)
    a=eo3(seg(lt,6.0,6.6)); pill(img,(W/2,1500),"A BIRD THAT WEARS ITS RANK",B(44),a,fg=INK,bg=SUN,sc=lerp(0.85,1,eob(seg(lt,6.0,6.7))))
    return img
# ---------- S5 range map
RANGES={"foot":[(78.3,30.2),(80.5,29.2),(83.0,28.2),(85.6,27.6),(88.3,27.3),(88.3,26.6),(85.6,26.9),(83.0,27.6),(80.5,28.5),(78.3,29.6)],
        "ne":[(91.6,28.2),(93.6,28.6),(95.8,29.2),(97.2,28.2),(96.3,26.8),(94.8,25.2),(93.6,23.6),(92.4,22.6),(91.6,24.0),(90.5,25.5),(91.0,27.2)],
        "wg":[(73.7,16.5),(74.3,15.5),(74.9,13.5),(75.7,12.0),(76.6,10.9),(77.4,9.6),(77.6,8.5),(76.9,8.4),(76.2,9.8),(75.4,11.5),(74.6,13.0),(74.0,14.8),(73.5,15.8)]}
_MP={}
def imap():
    if "m" not in _MP:
        cam=IC.Cam(82.0,21.5,29,w=960,h=1000); m=IC.map_img(cam,coast=0.8).astype(np.float32); lm=np.clip((m[...,0]/(m[...,2]+1)-0.5)*4,0,1)[...,None]
        tex=IC.TEXN[:cam.h,:cam.w,None]*14+IC.TEXL[:cam.h,:cam.w,None]*18; m=m*(1-lm)*1.4+(np.array((78,104,70),np.float32)+tex)*lm
        _MP["m"]=(cam,np.clip(m,0,255).astype(np.uint8))
    return _MP["m"]
def S5(lt,t):
    img=bg(t); brand(img,CREAM,150); chip(img,"WHERE DOES IT LIVE?",lt)
    cam,m=imap(); mk=Image.new("L",(960,1000),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,959,999),radius=26,fill=255); mp=Image.fromarray(m).convert("RGBA"); mp.putalpha(mk)
    ov=Image.new("RGBA",(960,1000),(0,0,0,0)); do=ImageDraw.Draw(ov,"RGBA")
    for key,t0 in (("foot",1.0),("ne",2.6),("wg",4.2)):
        fa=ease(seg(lt,t0,t0+1.0)); pts=[cam.px(*p) for p in RANGES[key]]; do.polygon(pts,fill=SUN+(int(150*fa),),outline=SUN+(int(255*fa),)); do.line(pts+[pts[0]],fill=SUN+(int(255*fa),),width=3)
    for nm,lo,la,t0,(ox,oy) in (("PAKKE",92.99,27.1,6.0,(-20,-50)),("ANAIMALAI",77.0,10.4,6.6,(70,10))):
        a_=eo3(seg(lt,t0,t0+0.4))
        if a_<=0: continue
        x,y=cam.px(lo,la); r=((lt-t0)*0.9)%1; do.ellipse((x-9-r*34,y-9-r*34,x+9+r*34,y+9+r*34),outline=CREAM+(int(200*(1-r)*a_),),width=3); do.ellipse((x-10,y-10,x+10,y+10),fill=CREAM+(int(255*a_),))
        f=B(32); w=f.getlength(nm)+26; bx=min(max(x+ox-w/2,12),960-12-w); do.rounded_rectangle((bx,y+oy-30,bx+w,y+oy+22),radius=12,fill=(8,22,18,int(230*a_)),outline=SUN+(int(200*a_),),width=2); txt(do,(bx+13,y+oy+8),nm,f,CREAM,255*a_,"ls")
    for s,lo,la,t0 in (("HIMALAYAN FOOTHILLS",83.5,29.6,1.4),("NORTH-EAST",93.5,30.6,3.0),("WESTERN GHATS",72.2,12.8,4.6)):
        a_=eo3(seg(lt,t0,t0+0.5)); x,y=cam.px(lo,la); txt(do,(min(max(x,170),790),y),s,B(32),CREAM,255*a_)
    mp.alpha_composite(ov); img.alpha_composite(mp,(60,230)); d=ImageDraw.Draw(img,"RGBA"); d.rounded_rectangle((58,228,1022,1232),radius=26,outline=SUN+(170,),width=3)
    a=eo3(seg(lt,7.0,7.6)); txt(d,(W/2,1320),"ALSO: NEPAL, BHUTAN, SOUTH CHINA,",B(40),CREAM,255*a); txt(d,(W/2,1372),"SOUTH-EAST ASIA, SUMATRA",B(40),CREAM,255*a)
    a=eo3(seg(lt,8.2,8.8)); pill(img,(W/2,1500),"IUCN STATUS: VULNERABLE",B(48),a,fg=INK,bg=RED2,sc=lerp(0.85,1,eob(seg(lt,8.2,8.9))))
    a=eo3(seg(lt,9.4,10.0)); txt(d,(W/2,1600),"It needs big, undisturbed forest. Those are shrinking.",B(36),SUN,255*a)
    txt(d,(W/2,1700),"Ranges illustrative. Map: Natural Earth. Status: IUCN Red List (2020).",BM(26),GREY,200)
    return img
# ---------- S6 gardener
def tree(d,x,y,h,a,col=(60,40,28),lc=(60,130,70)):
    d.rectangle((x-h*0.05,y-h*0.5,x+h*0.05,y),fill=col+(int(255*a),)); 
    for dx,dy,r in ((0,-0.62,0.28),(-0.2,-0.5,0.2),(0.2,-0.5,0.2),(0,-0.8,0.2)): d.ellipse((x+dx*h-r*h,y+dy*h-r*h,x+dx*h+r*h,y+dy*h+r*h),fill=lc+(int(255*a),))
def bird_icon(d,x,y,s,a,flap=0):
    d.ellipse((x-s*0.7,y-s*0.25,x+s*0.5,y+s*0.35),fill=(20,20,24,int(255*a))); d.ellipse((x+s*0.35,y-s*0.4,x+s*0.8,y),fill=(20,20,24,int(255*a)))
    d.polygon([(x+s*0.7,y-s*0.3),(x+s*1.6,y-s*0.05),(x+s*0.8,y-s*0.05)],fill=SUN+(int(255*a),)); d.polygon([(x-s*0.1,y-s*0.2),(x-s*0.6,y-s*(0.8+0.4*flap)),(x+s*0.3,y-s*0.3)],fill=(30,30,36,int(255*a)))
def S6(lt,t):
    img=bg(t); brand(img,CREAM,150); chip(img,"THE GARDENER",lt)
    d=ImageDraw.Draw(img,"RGBA"); gy=900
    d.rectangle((60,gy,1020,1100),fill=(50,36,26,255)); d.rectangle((60,gy,1020,gy+8),fill=(90,140,70,255))
    ta=eo3(seg(lt,0.4,1.0)); tree(d,230,gy,520,ta)
    fa=eo3(seg(lt,1.0,1.6))
    for i in range(5): d.ellipse((150+i*35-9,gy-460-(i%2)*30-9,150+i*35+9,gy-460-(i%2)*30+9),fill=(230,80,60,int(255*fa)))
    p=ease(seg(lt,2.0,4.6))
    if 1.8<lt<5.0:
        bx=lerp(300,820,p); by=gy-340-math.sin(math.pi*p)*180; bird_icon(d,bx,by,60,1,flap=math.sin(lt*14))
    # seed drop
    dp=ease(seg(lt,4.0,5.4)); 
    if dp>0:
        sx=820; sy=lerp(gy-340,gy-6,dp); d.ellipse((sx-12,sy-12,sx+12,sy+12),fill=(230,80,60,255))
    sg=ease(seg(lt,5.6,7.8))
    if sg>0: tree(d,820,gy,420*sg,min(1,sg*3),lc=(110,190,100))
    a=eo3(seg(lt,0.2,0.8)); txt(d,(W/2,260),"IT DOES NOT JUST LIVE IN THE FOREST.",B(46),CREAM,255*a); comp(img,glayer((W/2,400),"IT GROWS IT.",A(110),top=(255,250,240),bot=(255,208,120)),eo3(seg(lt,1.0,1.6)),sc=lerp(1.2,1,eob(seg(lt,1.0,1.7),1.3)))
    d=ImageDraw.Draw(img,"RGBA")
    a=eo3(seg(lt,3.0,3.6)); txt(d,(W/2,1230),"SWALLOWS LARGE FRUIT, DROPS THE SEEDS FAR AWAY",B(38),CREAM,255*a)
    a=eo3(seg(lt,5.0,5.6)); txt(d,(W/2,1310),"69 TO 100%  of seeds landed away from the parent tree",B(40),SUN,255*a); txt(d,(W/2,1356),"(5 hornbill + tree pairs, Arunachal study)",BM(28),GREY,255*a)
    a=eo3(seg(lt,7.0,7.6)); txt(d,(W/2,1450),"Namdapha: up to 12,000 large seeds per sq km per day",B(38),CREAM,255*a); txt(d,(W/2,1496),"(all hornbill species there)",BM(28),GREY,255*a)
    a=eo3(seg(lt,8.4,9.0)); pill(img,(W/2,1620),"MAYBE EVEN ITS OWN FUTURE HOMES",B(42),a,fg=INK,bg=SUN,sc=lerp(0.85,1,eob(seg(lt,8.4,9.0))))
    return img
# ---------- S7 the cost
def S7(lt,t):
    img=bg(t,) if False else bg(t); brand(img,CREAM,150); chip(img,"THE PRICE",lt)
    fwin(img,"h3",wbox("h3",0.55,0.38,0.7,(60,200,960,800)),(60,200,960,800),z=1.0+0.1*seg(lt,0,8),spot=(0.5,0.28,0.25,0.18),k=eo3(seg(lt,0.2,1.0)),border=RED2)
    d=ImageDraw.Draw(img,"RGBA")
    a=eo3(seg(lt,0.6,1.2)); comp(img,glayer((W/2,1120),"A TROPHY ON ITS HEAD",A(96),top=(255,200,180),bot=RED2),a,sc=lerp(1.25,1,eob(seg(lt,0.6,1.3),1.3)))
    a=eo3(seg(lt,2.0,2.6)); txt(d,(W/2,1210),"The casque went into traditional headgear.",B(42),CREAM,255*a)
    for i,(t0,s) in enumerate(((3.4,"HUNTING: MEAT, CASQUE, FEATHERS"),(4.6,"LOGGING: GIANT NEST TREES CUT"))):
        a=eo3(seg(lt,t0,t0+0.4)); y=1330+i*110
        if a<=0: continue
        d.rounded_rectangle((90,y-46,990,y+46),radius=22,fill=(40,16,14,int(230*a)),outline=RED2+(int(220*a),),width=3); d.ellipse((120,y-16,152,y+16),fill=RED2+(int(255*a),)); txt(d,(180,y+14),s,B(44),CREAM,255*a,"ls")
    a=eo3(seg(lt,6.0,6.6)); txt(d,(W/2,1620),"Even as the state bird of Arunachal Pradesh.",B(36),SUN,255*a)
    return img
# ---------- S8 hope
def S8(lt,t):
    img=bg(t); brand(img,CREAM,150); chip(img,"THE TURN",lt)
    fwin(img,"h2",wbox("h2",0.62,0.5,0.7,(60,200,960,640)),(60,200,960,640),z=1.0+0.06*seg(lt,0,12),spot=(0.66,0.45,0.2,0.3),k=eo3(seg(lt,0.2,1.0)),border=GRN)
    d=ImageDraw.Draw(img,"RGBA")
    a=eo3(seg(lt,0.6,1.2)); comp(img,glayer((W/2,920),"HUNTERS BECAME GUARDIANS",A(80),top=(255,250,240),bot=(150,235,160)),a,sc=lerp(1.2,1,eob(seg(lt,0.6,1.3),1.3)))
    a=eo3(seg(lt,1.8,2.4)); txt(d,(W/2,990),"Hornbill Nest Adoption Program, Pakke, Arunachal Pradesh",B(34),CREAM,255*a)
    n1=int(10*ease(seg(lt,3.0,4.0))); n2=int(119*ease(seg(lt,4.8,6.4)))
    for i,(t0,lab,val) in enumerate(((3.0,"NYISHI NEST PROTECTORS",f"{n1}"),(4.8,"CHICKS FLEDGED, 2012 TO 2018",f"{n2}"))):
        a=eo3(seg(lt,t0,t0+0.4)); y=1130+i*150
        if a<=0: continue
        d.rounded_rectangle((90,y-62,990,y+62),radius=26,fill=(14,34,28,int(235*a)),outline=GRN+(int(230*a),),width=3); txt(d,(130,y+16),lab,B(40),CREAM,255*a,"ls"); txt(d,(950,y+30),val,A(84),GRN,255*a,"rs")
    a=eo3(seg(lt,7.2,7.8)); d.rounded_rectangle((90,1385,990,1485),radius=26,fill=(14,34,28,int(235*a)),outline=GRN+(int(230*a),),width=3); txt(d,(W/2,1448),"FIBREGLASS BEAKS NOW REPLACE REAL ONES IN HEADGEAR",B(34),CREAM,255*a)
    a=eo3(seg(lt,9.0,9.6)); txt(d,(W/2,1580),"Programme figures (NCF). Some protectors were hunters before.",B(32),SUN,255*a)
    a=eo3(seg(lt,10.2,10.8)); txt(d,(W/2,1650),"Pakke won the India Biodiversity Award 2016 for this work.",BM(30),GREY,255*a)
    return img
# ---------- S9 close
def S9(lt,t):
    a=fb("h2",0.66,0.40,z=1.0+0.06*seg(lt,0,8),cy=0.45); a=a*np.array((1.04,1.0,0.94),np.float32)
    img=arr2img(a); scrim(img,1100,1920,0.0,0.92,(4,10,8)); scrim(img,0,320,0.7,0.0,(4,10,8)); brand(img,CREAM,170); chip(img,"THE GREAT HORNBILL",lt)
    d=ImageDraw.Draw(img,"RGBA")
    q=eo3(seg(lt,0.6,1.2)); txt(d,(W/2,1280),"NEXT TIME IN THE FOREST,",B(54),CREAM,255*q); q=eo3(seg(lt,1.6,2.2)); txt(d,(W/2,1350),"DO NOT JUST LOOK AT THE BIRD.",B(54),CREAM,255*q)
    w=eo3(seg(lt,3.0,3.6)); comp(img,glayer((W/2,1500),"LOOK AT THE TREE.",A(112),top=(255,250,240),bot=SUN),w,sc=lerp(1.3,1,eob(seg(lt,3.0,3.7),1.3)))
    btn=L(); ImageDraw.Draw(btn,"RGBA").rounded_rectangle((W/2-380,1590,W/2+380,1682),radius=46,fill=SUN+(250,)); ba=eo3(seg(lt,4.6,5.1)); comp(img,btn,ba,sc=lerp(0.6,1,eob(seg(lt,4.6,5.2))))
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1651),"FOLLOW THE NATURAL ANGLE",B(46),INK,255*eo3(seg(lt,5.0,5.4)))
    txt(d,(W/2,1745),"More forest stories every week",B(36),CREAM,255*eo3(seg(lt,5.8,6.4)))
    txt(d,(W/2,1840),"Photos: Hitesh Chawla. Sources: NCF, IUCN, Wikipedia, published studies.",BM(23),GREY,225*eo3(seg(lt,6.4,7.2)))
    return img
FN={"S1":S1,"S2":S2,"S3":S3,"S4":S4,"S5":S5,"S6":S6,"S7":S7,"S8":S8,"S9":S9}
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
