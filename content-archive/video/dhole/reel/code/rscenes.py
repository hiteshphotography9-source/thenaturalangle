import sys, json, math
SPD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/"
sys.path.insert(0,SPD+"dhreel"); sys.path.insert(0,SPD+"island")
from dcore_r import *
import core as IC
BEATS={float(k):v for k,v in json.load(open(SPD+"dhreel/vo/beats.json")).items()}
def T(src,end=False):
    k=min(BEATS,key=lambda q:abs(q-src)); return BEATS[k][1 if end else 0]
TOTAL=84.0
WK=ldarr('wiki_dhole.png'); PK=ldarr('pack_bandipur.png'); TR=ldarr('imphal_trap.png')
FBI=Image.open(ID+'fb_assam.png').convert('RGB'); IMH=Image.open(ID+'imphal_head.png').convert('RGB')
FBTOP=np.array(FBI.crop((0,0,1080,1000))).astype(np.float32)
def PH(k): return IC.photo(k).astype(np.float32)
def bgfill(arr,cx,cy,wf):
    h,w=arr.shape[:2]; cw=wf*w; ch=cw*H/W
    if ch>h: ch=h; cw=ch*W/H
    x0=min(max(cx*w-cw/2,0),w-cw); y0=min(max(cy*h-ch/2,0),h-ch); s=W/cw
    return cv2.warpAffine(arr,np.array([[s,0,-x0*s],[0,s,-y0*s]],np.float32),(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
def to_img(a): return Image.fromarray(np.clip(a,0,255).astype(np.uint8)).convert("RGBA")
def brand(img):
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,78),"THE NATURAL ANGLE",B(30),CREAM,150)
def gradv_arr(a,y0,y1,a0,a1):
    g=np.linspace(a0,a1,y1-y0,dtype=np.float32)[:,None,None]; a[y0:y1]=a[y0:y1]*(1-g)+np.array((4,6,4),np.float32)*g
def pulse(t,t0,sp=4.0): return 0.6+0.4*math.sin((t-t0)*sp)
def dotsxy(n,cx,cy,rx,ry,seed=3):
    r=np.random.default_rng(seed); out=[]
    for i in range(n):
        a=r.uniform(0,6.283); rr=math.sqrt(r.uniform(0.05,1)); out.append((cx+rx*rr*math.cos(a),cy+ry*rr*math.sin(a),r.uniform(0,6.28)))
    return out
# ================= S1 HOOK
S1END=T(9.8)-0.25
def S1(t):
    rev=T(7.1)-0.45
    if t<rev:
        a=bgfill(PH("a4bcbe52"),0.5,0.5,1.0); z=1+0.05*seg(t,0,rev)
        M=np.array([[z,0,W/2*(1-z)],[0,z,H/2*(1-z)]],np.float32); a=cv2.warpAffine(a,M,(W,H),borderMode=cv2.BORDER_REFLECT)
        gry=a.mean(2,keepdims=True); k=0.55*ease(seg(t,0.4,rev)); a=a*(1-k)+gry*k; a*=1-0.35*ease(seg(t,0.4,rev))
        gradv_arr(a,0,300,0.5,0.0); gradv_arr(a,1150,H,0.0,0.78)
        img=to_img(a); brand(img)
        o=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(o,"RGBA")
        a1=eo3(seg(t,0.15,0.55)); a2=eo3(seg(t,0.9,1.3)); a3=eo3(seg(t,T(3.0,True)-0.9,T(3.0,True)-0.5))
        
        # separate alphas
        img2=img.copy(); lay1=L(); grad_text(lay1,(W/2,1330),"TIGER.",A(150),top=(255,250,240),bot=(214,205,190)); lay2=L(); grad_text(lay2,(W/2,1470),"LEOPARD.",A(150),top=(255,250,240),bot=(214,205,190))
        comp(img2,lay1,a1,dy=(1-a1)*28); comp(img2,lay2,a2,dy=(1-a2)*28)
        l3=L(); d3=ImageDraw.Draw(l3,"RGBA"); txt(d3,(W/2,1575),"GET ALL THE ATTENTION.",B(58),CREAM); comp(img2,l3,a3)
        return img2
    k=t-rev; img=jungle(31); brand(img)
    fl=max(0,1-k/0.18)
    tm=pwin(img,WK,(0,0,984,654),(60,560,960,640),z=1+0.06*ease(k/4),spot=(265,235,170,150),k=eo3(seg(k,0.3,1.4)),flash=fl*0.6,desat=0.85*(1-eo3(seg(k,0.15,0.5))))
    d=ImageDraw.Draw(img,"RGBA"); fx,fy=tm(265,235); b=eo3(seg(k,0.4,1.3))
    brackets(d,lerp(80,fx-190,b),lerp(580,fy-165,b),lerp(1000,fx+190,b),lerp(1180,fy+165,b),EMBER,seg(k,0.3,0.6)*(0.75+0.25*math.sin(t*5)))
    l1=glayer((W/2,330),"THE PREDATOR",A(112)); l2=glayer((W/2,455),"PEOPLE FORGET",A(112))
    comp(img,glow(l1,RUST,24,0.6),eo3(seg(k,0.2,0.6))*0.8); comp(img,l1,eo3(seg(k,0.2,0.6)),sc=lerp(1.5,1,eob(seg(k,0.2,0.8),1.3)))
    comp(img,l2,eo3(seg(k,0.5,0.9)),sc=lerp(1.5,1,eob(seg(k,0.5,1.1),1.3)))
    shine(img,l1,seg(k,1.6,2.6)); shine(img,l2,seg(k,2.0,3.0))
    l3=L(); d3=ImageDraw.Draw(l3,"RGBA"); txt(d3,(W/2,1290),"INDIA'S WILD DOG  ·  THE DHOLE",B(46),SAGE); txt(d3,(W/2,1360),"UNDERESTIMATE IT AT YOUR PERIL",B(36),GREY)
    comp(img,l3,eo3(seg(t,T(7.1),T(7.1)+0.5)))
    credit(d,"Photo: Wikimedia Commons",y=1226,x=W-60,anchor="rs")
    return img
# ================= S2 WHO
S2END=T(19.45)-0.3
def S2(t):
    t0=S1END; k=t-t0; img=jungle(32); brand(img)
    tm=pwin(img,WK,(0,0,984,654),(60,300,960,640),z=1+0.06*ease(k/8),spot=(265,235,200,160),k=eo3(seg(k,0.3,1.2)),border=RUST)
    d=ImageDraw.Draw(img,"RGBA"); credit(d,"Photo: Wikimedia Commons",y=976,x=W-60,anchor="rs")
    comp(img,glayer((W/2,230),"MEET THE DHOLE",A(100)),eo3(seg(k,0.15,0.55)),dy=(1-eo3(seg(k,0.15,0.55)))*24)
    txt(d,(60,976),"ASIATIC WILD DOG · CUON ALPINUS",B(30),SAGE,230,"ls")
    # chips
    kgt=T(14.75)-0.1; alt=T(16.35)-0.1
    def chip(y,main,sub,t1,col=CREAM,hot=False,w=900):
        a=eo3(seg(t,t1,t1+0.35)); 
        if a<=0: return
        s=lerp(0.8,1,eob(seg(t,t1,t1+0.5)))
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); x0=W/2-w/2
        dl.rounded_rectangle((x0,y-90,x0+w,y+90),radius=28,fill=((54,24,8,235) if hot else (10,14,10,225)),outline=(RUST if hot else CREAM)+((255,) if hot else (70,)),width=(4 if hot else 2))
        txt(dl,(W/2,y+22),main,A(84),EMBER if hot else CREAM); txt(dl,(W/2,y+70),sub,B(32),CREAM if hot else GREY)
        comp(img,l,a,sc=s)
    chip(1130,"ENDANGERED","IUCN RED LIST",T(9.8)+0.9)
    chip(1340,"10 TO 20 KG","ABOUT THE WEIGHT OF A LARGE DOG",kgt,hot=(t>kgt and t<alt))
    # alone -> pack: dots
    a=eo3(seg(t,alt,alt+0.4))
    if a>0:
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((90,1470,990,1650),radius=28,fill=(54,24,8,235),outline=RUST+(255,),width=4)
        txt(dl,(W/2,1550),"NEVER HUNTS ALONE",A(72),EMBER); 
        comp(img,l,a,sc=lerp(0.8,1,eob(seg(t,alt,alt+0.5))))
        d=ImageDraw.Draw(img,"RGBA"); n=1+int(8*ease(seg(t,alt+0.5,alt+2.2)))
        for i in range(n):
            x=W/2-(n-1)*34+i*68; d.ellipse((x-13,1618-13,x+13,1618+13),fill=EMBER+(int(255*a),),outline=CREAM+(int(220*a),),width=2)
    return img
# ================= S3 PACK
S3END=T(27.35)-0.25
def S3(t):
    t0=S2END; k=t-t0; img=jungle(33); brand(img)
    comp(img,glayer((W/2,225),"THE PACK",A(112)),eo3(seg(k,0.1,0.5)),dy=(1-eo3(seg(k,0.1,0.5)))*24)
    tm=pwin(img,PK,(0,0,1080,565),(60,290,960,502),z=1+0.06*ease(k/7),spot=(660,230,360,260),k=eo3(seg(k,0.3,1.1)),border=RUST)
    d=ImageDraw.Draw(img,"RGBA"); credit(d,"Photo: Bandipur NP, as published by Scroll.in",y=826,x=W-60,anchor="rs")
    t5=T(19.45); t30=T(20.9); tw=T(22.85)
    # counter
    if t<t30-0.1:
        a=eo3(seg(t,t5,t5+0.35)); l=glayer((W/2,1010),"5 TO 12",A(190)); comp(img,glow(l,RUST,24,0.5),a*0.7); comp(img,l,a,sc=lerp(1.4,1,eob(seg(t,t5,t5+0.5),1.3)))
        txt(d,(W/2,1090),"DOGS IN A TYPICAL PACK",B(40),CREAM,255*a)
    else:
        a=eo3(seg(t,t30-0.1,t30+0.3)); l=glayer((W/2,1010),"SOMETIMES 30+",A(140)); comp(img,glow(l,RUST,24,0.5),a*0.7); comp(img,l,a,sc=lerp(1.4,1,eob(seg(t,t30-0.1,t30+0.4),1.3)))
        txt(d,(W/2,1090),"WHEN PACKS MERGE",B(40),CREAM,255*a)
    n=0
    if t>t5: n=5+int(7*ease(seg(t,t5+0.4,t5+1.2)))
    if t>t30: n=12+int(20*ease(seg(t,t30,t30+1.0)))
    P=dotsxy(32,540,1240,430,110,seed=5)
    for i in range(min(n,32)):
        x,y,ph=P[i]; x+=6*math.sin(t*1.7+ph); y+=4*math.cos(t*1.3+ph); ap=eo3(seg(t,t5+0.05*i,t5+0.05*i+0.3)) if i<12 else eo3(seg(t,t30+0.02*(i-12),t30+0.02*(i-12)+0.3))
        d.ellipse((x-11,y-11,x+11,y+11),fill=EMBER+(int(255*ap),),outline=CREAM+(int(200*ap),),width=2)
    # whistle
    a=eo3(seg(t,tw,tw+0.4))
    if a>0:
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((90,1400,990,1620),radius=28,fill=(10,14,10,230),outline=SAGE+(150,),width=3); comp(img,l,a)
        d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1490),"THEY WHISTLE",A(78),SAGE,255*a)
        txt(d,(W/2,1550),"to talk in thick forest",B(36),CREAM,255*a)
        for kk in range(3):
            r=((t-tw)*0.9+kk/3)%1; pts=[]
            for x in range(-230,231,6):
                env=math.exp(-(x/160)**2); pts.append((W/2+x,1595+math.sin(x*0.08-(t-tw)*14)*16*env))
            d.line(pts,fill=SAGE+(int(200*a),),width=3)
            break
    return img
# ================= S4 HUNT
S4END=T(38.1)-0.3
def S4(t):
    t0=S3END; k=t-t0; img=jungle(34); brand(img); d=ImageDraw.Draw(img,"RGBA")
    ta=T(28.4); tt_=T(32.55)
    if t<tt_-0.25:
        comp(img,glayer((W/2,225),"TEAMWORK",A(120)),eo3(seg(k,0.1,0.5)),dy=(1-eo3(seg(k,0.1,0.5)))*24)
        cx,cy=540,850
        pa=eo3(seg(t,ta-0.2,ta+0.2))
        # prey
        R=110
        d.ellipse((cx-R,cy-R,cx+R,cy+R),fill=(110,84,52,int(255*pa)),outline=CREAM+(int(160*pa),),width=3); txt(d,(cx,cy+12),"SAMBAR",B(36),CREAM,255*pa)
        n=12; prog=ease(seg(t,ta,ta+2.4)); rad=lerp(430,190,prog)
        for i in range(n):
            ang=i/n*6.283+t*0.6*(1-prog*0.7); x=cx+rad*math.cos(ang); y=cy+rad*0.8*math.sin(ang)
            ap=eo3(seg(t,ta-0.4+i*0.04,ta+0.1+i*0.04))
            if prog>0.05 and prog<0.98:
                x0_=cx+(rad+60)*math.cos(ang); y0_=cy+(rad+60)*0.8*math.sin(ang); d.line((x0_,y0_,x,y),fill=EMBER+(int(120*ap),),width=2)
            d.ellipse((x-14,y-14,x+14,y+14),fill=EMBER+(int(255*ap),),outline=CREAM+(int(220*ap),),width=2)
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((70,1230,1010,1480),radius=28,fill=(10,14,10,225),outline=RUST+(150,),width=3)
        txt(dl,(W/2,1330),"TOGETHER THEY BRING DOWN",B(42),CREAM); txt(dl,(W/2,1420),"PREY MANY TIMES THEIR SIZE",A(66),EMBER)
        comp(img,l,eo3(seg(t,ta+0.8,ta+1.3)),dy=(1-eo3(seg(t,ta+0.8,ta+1.4)))*30)
        txt(d,(W/2,1560),"sambar, chital",B(34),GREY,255*eo3(seg(t,ta+1.2,ta+1.6)))
    else:
        j=t-(tt_-0.25); fl=max(0,1-j/0.2)
        a=PH("5b5b6505")
        tm=pwin(img,a,(0,0,a.shape[1],a.shape[0]),(60,330,960,820),z=1+0.05*ease(j/4),spot=(a.shape[1]*0.5,a.shape[0]*0.45,a.shape[1]*0.28,a.shape[0]*0.3),k=eo3(seg(j,0.3,1.0)),flash=fl*0.5,desat=0.8*(1-eo3(seg(j,0.1,0.4))),border=RED)
        d=ImageDraw.Draw(img,"RGBA")
        comp(img,glayer((W/2,225),"EVEN TIGERS?",A(112),top=(255,150,130),bot=(222,60,46)),eo3(seg(j,0.1,0.5)),dy=(1-eo3(seg(j,0.1,0.5)))*24)
        credit(d,"Tiger photo: Hitesh Chawla",y=1176,x=W-60,anchor="rs")
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((70,1230,1010,1520),radius=28,fill=(40,12,10,230),outline=RED+(200,),width=3)
        txt(dl,(W/2,1320),"PACKS HAVE BEEN RECORDED",B(44),CREAM); txt(dl,(W/2,1405),"CHASING TIGERS OFF KILLS",A(64),(255,150,130)); txt(dl,(W/2,1480),"rare, but documented by researchers",B(32),GREY)
        comp(img,l,eo3(seg(j,0.7,1.1)),dy=(1-eo3(seg(j,0.7,1.2)))*30)
        # dots closing in on tiger (left & right edges)
        for i in range(6):
            side=-1 if i%2==0 else 1; prog=ease(seg(j,1.0+i*0.15,3.2))
            x=lerp(540+side*520,540+side*300,prog); y=1000+((i//2)-1)*70
            d.ellipse((x-13,y-13,x+13,y+13),fill=EMBER+(int(255*eo3(seg(j,1.0+i*0.15,1.3+i*0.15))),),outline=CREAM+(200,),width=2)
    return img
# ================= S5 FALL (range loss, vermin, numbers)
S5END=T(57.05)-0.3
RMAP=None
def rmap():
    global RMAP
    if RMAP is None:
        cam=IC.Cam(96,24,16.0,w=960,h=1060); m=IC.map_img(cam,coast=0.7).astype(np.float32)
        RMAP=(cam,np.clip(m*np.array((1.0,0.93,0.80))*1.7,0,255).astype(np.uint8))
    return RMAP
FORMER=[(68,33),(70,38),(77,42),(85,48),(95,51),(108,52),(120,50),(131,48),(134,43),(128,38),(122,31),(121,25),(117,22),(110,18),(108,11),(105,8),(103,2),(104,-3),(110,-7.5),(106,-6),(101,-3),(98,3),(98,10),(94,16),(92,22),(86,20),(80,14),(78,8),(76,9),(73,17),(72,21),(67,25)]
TODAY=[(74.6,16.5,2.2),(76.6,11,1.4),(80.5,22.3,2.4),(85,21,1.2),(92.5,25.5,1.7),(84,28,1.0),(95.5,20,1.5),(99,16,1.6),(101,13.5,1.4),(104,13,1.5),(106,15.5,1.3),(101.5,3.5,1.2),(104.5,-7.5,0.8),(100,0,0.9)]
def S5(t):
    t0=S4END; img=jungle(35); brand(img); d=ImageDraw.Draw(img,"RGBA")
    tA=T(38.1); tB=T(46.55); tC=T(50.65)
    if t<tB-0.3:
        k=t-t0; cam,m=rmap()
        mk=Image.new("L",(960,1060),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,959,1059),radius=26,fill=255)
        mp=Image.fromarray(m).convert("RGBA"); mp.putalpha(mk)
        # overlays on the map
        ov=Image.new("RGBA",(960,1060),(0,0,0,0)); do=ImageDraw.Draw(ov,"RGBA")
        pts=[cam.px(*p) for p in FORMER]
        fa=eo3(seg(t,tA+0.2,tA+1.4)); shrink=ease(seg(t,T(40.55)+1.4,T(44.15)+0.4))
        do.polygon(pts,fill=RUST+(int((110*(1-shrink)+0)*fa),),outline=EMBER+(int(220*fa*(1-0.4*shrink)),))
        do.line(pts+[pts[0]],fill=EMBER+(int(230*fa),),width=3)
        ta_=ease(seg(t,T(40.55)+1.0,T(44.15)+0.2))
        ov2=Image.new("RGBA",(960,1060),(0,0,0,0)); do2=ImageDraw.Draw(ov2,"RGBA")
        if ta_>0.02:
            for (lo,la,r) in TODAY:
                x,y=cam.px(lo,la); rr=r*cam.k*0.7
                do2.ellipse((x-rr,y-rr*0.8,x+rr,y+rr*0.8),fill=EMBER+(int(220*ta_),),outline=CREAM+(int(200*ta_),),width=2)
        mp.alpha_composite(ov); mp.alpha_composite(ov2); 
        img.alpha_composite(mp,(60,330)); d=ImageDraw.Draw(img,"RGBA"); d.rounded_rectangle((58,328,1022,1392),radius=26,outline=RUST+(160,),width=3)
        comp(img,glayer((W/2,225),"HOW MUCH IS LEFT?",A(100)),eo3(seg(k,0.1,0.5)),dy=(1-eo3(seg(k,0.1,0.5)))*24)
        txt(d,(W/2,1432),"MAP IS ILLUSTRATIVE AND APPROXIMATE, NOT AN IUCN MAP",BM(26),GREY,230)
        l=L(); dl=ImageDraw.Draw(dl_:=l,"RGBA") if False else None
        la=eo3(seg(t,tA+0.3,tA+0.7))
        txt(d,(100,380),"FORMER RANGE",B(36),EMBER,255*la*(1-0.5*shrink),"ls")
        lb=eo3(seg(t,T(44.15),T(44.15)+0.5)); txt(d,(960,1330),"TODAY: SCATTERED PATCHES",B(34),CREAM,255*lb,"rs")
        # 75% ring counter
        pa=ease(seg(t,T(40.55)+0.4,T(40.55)+1.8))
        cx,cy,R=860,500,98
        if pa>0:
            d.ellipse((cx-R,cy-R,cx+R,cy+R),fill=(10,14,10,220)); d.ellipse((cx-R,cy-R,cx+R,cy+R),outline=(255,255,255,40),width=26)
            d.arc((cx-R,cy-R,cx+R,cy+R),start=-90,end=-90+360*0.75*pa,fill=RUST+(255,),width=26)
            txt(d,(cx,cy+22),f"{int(75*pa)}%+",A(64),CREAM); 
        lc=eo3(seg(t,T(44.15),T(44.15)+0.5))
        l2=L(); dl2=ImageDraw.Draw(l2,"RGBA"); dl2.rounded_rectangle((70,1480,1010,1640),radius=26,fill=(40,12,10,225),outline=RED+(190,),width=3)
        txt(dl2,(W/2,1565),"GONE FROM 75%+ OF ITS RANGE",A(62),(255,150,130)); txt(dl2,(W/2,1615),"IUCN: Endangered",B(32),GREY)
        comp(img,l2,lc,dy=(1-lc)*30)
    elif t<tC-0.3:
        k=t-(tB-0.3)
        tm=pwin(img,WK,(0,0,984,654),(60,300,960,520),z=1+0.04*ease(k/4),desat=0.7,border=RED)
        d=ImageDraw.Draw(img,"RGBA")
        comp(img,glayer((W/2,225),"IN INDIA",A(112),top=(255,150,130),bot=(222,60,46)),eo3(seg(k,0.1,0.5)))
        # stamp
        st=L(); ds=ImageDraw.Draw(st,"RGBA"); f=A(200); 
        ds.rounded_rectangle((120,990,960,1230),radius=14,outline=RED+(255,),width=14); txt(ds,(W/2,1170),"VERMIN",f,RED)
        stt=T(46.55)+0.9; sa=eo3(seg(t,stt,stt+0.12)); sc=lerp(2.2,1.0,eo3(seg(t,stt,stt+0.15)))
        comp(img,st,sa,sc=sc,rot=-7)
        if 0<t-stt<0.35: 
            kk=1-(t-stt)/0.35; a=np.array(img).astype(np.float32); a[...,:3]*=1-0.0; img=Image.fromarray(np.clip(a+kk*28,0,255).astype(np.uint8))
        d=ImageDraw.Draw(img,"RGBA")
        txt(d,(W/2,1300),"HUNTED FOR BOUNTY",B(52),CREAM,255*eo3(seg(t,stt+0.4,stt+0.8)))
        p=eo3(seg(t,T(46.55)+2.4,T(46.55)+3.1))
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((70,1370,1010,1610),radius=26,fill=(14,28,16,230),outline=SAGE+(200,),width=3)
        txt(dl,(W/2,1448),"PROTECTED ONLY IN",B(40),CREAM); txt(dl,(W/2,1580),"1972",A(100),SAGE)
        comp(img,l,p,sc=lerp(0.85,1,eob(seg(t,T(46.55)+2.4,T(46.55)+3.2))))
    else:
        k=t-(tC-0.3)
        comp(img,glayer((W/2,225),"WORLDWIDE TODAY",A(100)),eo3(seg(k,0.1,0.5)))
        q=ease(seg(t,T(52.25)+0.3,T(52.25)+2.4)); lo=int(949*q); hi=int(2215*q)
        l=glayer((W/2,720),f"{lo:,}",A(230)); l2=glayer((W/2,980),f"TO {hi:,}",A(170)); 
        a=eo3(seg(t,tC-0.1,tC+0.3)); comp(img,glow(l,RUST,26,0.5),a*0.6); comp(img,l,a); comp(img,l2,a)
        txt(d,(W/2,1090),"BREEDING ADULTS",B(64),CREAM,255*a); txt(d,(W/2,1150),"2015 ESTIMATE  ·  IUCN",B(34),GREY,255*a)
        # dot grid: 1 dot = about 50 adults (approx)
        nd=int(44*q); 
        for i in range(44):
            x=130+(i%11)*82; y=1260+(i//11)*88; on=i<nd
            d.ellipse((x-22,y-22,x+22,y+22),fill=(EMBER+(255,)) if on else (255,255,255,20),outline=(CREAM+(200,)) if on else None,width=2)
        txt(d,(W/2,1640),"1 dot is about 50 adults (approximate)",BM(28),GREY,230*a)
    return img
# ================= S6 COMEBACK
S6END=T(74.65)-0.3
IMAP=None
def imap():
    global IMAP
    if IMAP is None:
        cam=IC.Cam(82.5,22.0,34.0,w=960,h=950); m=IC.map_img(cam,coast=0.7).astype(np.float32)
        IMAP=(cam,np.clip(m*np.array((1.0,0.93,0.80))*1.7,0,255).astype(np.uint8))
    return IMAP
def S6(t):
    t0=S5END; k=t-t0; img=jungle(36); brand(img); d=ImageDraw.Draw(img,"RGBA"); cam,m=imap()
    mk=Image.new("L",(960,950),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,959,949),radius=26,fill=255)
    mp=Image.fromarray(m).convert("RGBA"); mp.putalpha(mk)
    sl=Image.new("L",(960,950),0); ds=ImageDraw.Draw(sl)
    wg=[cam.px(73.6,19.8),cam.px(74.0,17.0),cam.px(74.6,14.5),cam.px(75.6,12.0),cam.px(76.6,10.0),cam.px(77.3,8.6)]; ds.line(wg,fill=255,width=34,joint="curve")
    for lo,la,r in ((80.6,22.4,2.6),(93.6,26.4,1.6)):
        x,y=cam.px(lo,la); rr=r*cam.k; ds.ellipse((x-rr,y-rr*0.75,x+rr,y+rr*0.75),fill=255)
    sl=sl.filter(ImageFilter.GaussianBlur(18)); st=Image.new("RGBA",(960,950),RUST+(0,)); st.putalpha(sl.point(lambda v:int(v*0.55*ease(seg(t,t0+0.3,t0+1.2)))))
    mp.alpha_composite(st); img.alpha_composite(mp,(60,300)); d=ImageDraw.Draw(img,"RGBA"); d.rounded_rectangle((58,298,1022,1252),radius=26,outline=RUST+(160,),width=3)
    comp(img,glayer((W/2,225),"BUT SOMETHING CHANGED",A(88)),eo3(seg(k,0.1,0.5)),dy=(1-eo3(seg(k,0.1,0.5)))*24)
    txt(d,(W/2,1288),"Shaded: where dholes still hold on. Locations approximate.",BM(26),GREY,230)
    P=lambda lo,la:(60+cam.px(lo,la)[0],300+cam.px(lo,la)[1])
    pins=[("assam",T(59.4)-0.1,93.4,26.55,"ASSAM","after ~30 years",(-20,-60),"rs"),("manip",T(67.4),94.47,25.12,"MANIPUR","first ever",(-20,55),"rs"),("mp",T(70.55),77.75,23.05,"RATAPANI","first record",(26,-58),"ls")]
    for key,tp,lo,la,l1,l2,(ox,oy),anc in pins:
        p=seg(t,tp,tp+0.45)
        if p<=0: continue
        x,y=P(lo,la); a=eo3(seg(t,tp,tp+0.15)); yy=y-(1-eob(p,1.5))*120 if p<1 else y
        for kk in range(2):
            r=((t-tp)*0.8+kk/2)%1; rr=10+r*46; d.ellipse((x-rr,y-rr,x+rr,y+rr),outline=EMBER+(int(200*(1-r)*a),),width=3)
        d.ellipse((x-13,yy-13,x+13,yy+13),fill=EMBER+(int(255*a),),outline=CREAM+(int(255*a),),width=3)
        la_=eo3(seg(t,tp+0.3,tp+0.6))
        if la_>0:
            f1=B(32); f2=BM(26); w_=max(f1.getlength(l1),f2.getlength(l2))+28; tx,ty=x+ox,y+oy; bx=tx-w_ if anc=="rs" else tx-14; bx=max(64,min(bx,W-64-w_))
            d.rounded_rectangle((bx,ty-34,bx+w_,ty+40),radius=12,fill=(10,14,10,int(225*la_)),outline=EMBER+(int(200*la_),),width=2)
            txt(d,(bx+14,ty-2),l1,f1,CREAM,255*la_,"ls"); txt(d,(bx+14,ty+30),l2,f2,GREY,255*la_,"ls")
    # bottom proof cards
    ab=T(59.4); mn=T(65.9); mpp=T(70.55)
    if t<mn-0.2:
        a=eo3(seg(t,ab+0.2,ab+0.7)); 
        if a>0:
            p=eob(seg(t,ab+0.2,ab+0.9),1.2); card(img,Image.fromarray(FBTOP.astype(np.uint8)).crop((0,0,1080,720)),290,1480,0.42,lerp(7,-2,eo3(seg(t,ab+0.2,ab+0.9))),a=a)
            txt(d,(540,1420),"1 LONE DHOLE",A(60),EMBER,255*a,"lm"); txt(d,(540,1480),"6 PHOTOS · 83 CAMERA TRAPS",B(32),CREAM,255*a,"lm"); txt(d,(540,1530),"31 Oct 2022 · WII study, 2025",BM(28),GREY,255*a,"lm")
            credit(d,"Image: India Today NE",y=1650,x=60)
    elif t<mpp-0.2:
        a=eo3(seg(t,mn,mn+0.5)); p=eob(seg(t,mn,mn+0.8),1.2)
        card(img,IMH,540,lerp(1750,1430,p),0.60,lerp(-5,1.2,eo3(seg(t,mn,mn+0.8))),a=a)
        txt(d,(W/2,1560),"Camera spot picked by a former hunter, now a conservationist",B(30),CREAM,255*eo3(seg(t,mn+0.8,mn+1.3)))
        credit(d,"Imphal Times, ENFOGAL camera trap",y=1650,x=60)
    else:
        a=eo3(seg(t,mpp,mpp+0.5)); l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((70,1350,1010,1610),radius=28,fill=(54,24,8,235),outline=RUST+(255,),width=4)
        txt(dl,(W/2,1450),"RATAPANI TIGER RESERVE",A(62),EMBER); txt(dl,(W/2,1520),"first recorded sighting · Jan 2026",B(42),CREAM); txt(dl,(W/2,1580),"Madhya Pradesh · camera trap (as reported)",BM(30),GREY)
        comp(img,l,a,sc=lerp(0.85,1,eob(seg(t,mpp,mpp+0.6))))
    return img
# ================= S7 BINOCULARS
S7END=T(95.15)-0.3
FOREST=PH("c31da8f7"); TGX,TGY=1501,1699
def S7(t):
    t0=S6END; k=t-t0; ta=T(74.65); tb=T(76.65); tc=T(79.75)
    a=bgfill(FOREST,0.417,0.5,0.34).astype(np.float32)
    ps=ease(seg(t,ta,ta+0.4)); a*=0.7
    gradv_arr(a,0,450,0.6,0.0); gradv_arr(a,1450,H,0.0,0.75)
    img=to_img(a); brand(img); d=ImageDraw.Draw(img,"RGBA")
    # location of the tiny tiger in this crop
    iw=FOREST.shape[1]; ih=FOREST.shape[0]; cw=0.34*iw; ch=cw*H/W; x0=min(max(0.417*iw-cw/2,0),iw-cw); y0=min(max(0.5*ih-ch/2,0),ih-ch); sc=W/cw
    tx=(TGX-x0)*sc; ty=(TGY-y0)*sc
    l1=eo3(seg(t,ta,ta+0.4)); comp(img,glayer((W/2,250),"HARD TO SPOT",A(120)),l1,dy=(1-l1)*24)
    gb=eo3(seg(t,tb,tb+0.4)); txt(d,(W/2,370),"they vanish in a blink",B(52),CREAM,255*gb)
    bp=ease(seg(t,tc,tc+0.9)); R=lerp(0,205,bp); cxs=(310,770); cy=830
    if bp>0.05:
        zz=lerp(1.0,1.9,ease(seg(t,tc+0.3,tc+2.4))); hw=330/zz; n=int(2*R)
        if n>=8:
            for cx in cxs:
                M=np.array([[n/(2*hw),0,-(TGX-hw)*n/(2*hw)],[0,n/(2*hw),-(TGY-hw)*n/(2*hw)]],np.float32)
                ph=cv2.warpAffine(FOREST,M,(n,n),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
                ph=np.clip((ph-60)*1.25+70,0,255)
                mk=Image.new("L",(n,n),0); ImageDraw.Draw(mk).ellipse((0,0,n-1,n-1),fill=255)
                p=Image.fromarray(ph.astype(np.uint8)).convert("RGBA"); p.putalpha(mk); img.alpha_composite(p,(int(cx-n/2),int(cy-n/2)))
            d=ImageDraw.Draw(img,"RGBA")
            for cx in cxs:
                d.ellipse((cx-R-6,cy-R-6,cx+R+6,cy+R+6),outline=(14,14,14,255),width=16); d.ellipse((cx-R,cy-R,cx+R,cy+R),outline=RUST+(255,),width=4)
                d.line((cx-R*0.5,cy,cx+R*0.5,cy),fill=EMBER+(130,),width=2); d.line((cx,cy-R*0.5,cx,cy+R*0.5),fill=EMBER+(130,),width=2)
            d.rounded_rectangle((cxs[0]+R*0.8,cy-26,cxs[1]-R*0.8,cy+26),radius=20,fill=(24,24,24,255),outline=RUST+(200,),width=3)
        # ring on the tiny tiger in the scene + link
        ra=eo3(seg(t,tc+0.9,tc+1.3))
        if ra>0:
            for kk in range(2):
                r=((t-tc)*0.7+kk/2)%1; d.ellipse((tx-30-r*50,ty-60-r*50,tx+30+r*50,ty+60+r*50),outline=EMBER+(int(220*(1-r)*ra),),width=3)
            d.ellipse((tx-34,ty-64,tx+34,ty+64),outline=EMBER+(int(255*ra),),width=4)
            txt(d,(tx,ty+110),"HERE",B(34),EMBER,255*ra)
        if t>tc+2.4:
            la=eo3(seg(t,tc+2.4,tc+2.8)); txt(d,(W/2,cy+R+95),"FOUND IT FIRST",A(78),EMBER,255*la)
            txt(d,(W/2,cy+R+150),"view through binoculars, from my own photo",BM(28),GREY,255*la)
    pl=eo3(seg(t,tc+1.6,tc+2.0))
    if pl>0:
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((170,1480,910,1572),radius=46,fill=RUST+(250,)); txt(dl,(W/2,1548),"MY BINOCULARS: LINK IN DESCRIPTION",B(40),INK); comp(img,l,pl,sc=lerp(0.7,1,eob(seg(t,tc+1.6,tc+2.2))))
    return img
# ================= S8 CTA
def S8(t):
    t0=S7END; k=t-t0; img=jungle(38); brand(img); d=ImageDraw.Draw(img,"RGBA")
    ta=T(95.15); tn=T(96.15); tr=T(97.0); tq=T(101.2); tw_=T(102.85); tcm=T(104.55)
    a1=eo3(seg(t,ta,ta+0.4)); comp(img,glayer((W/2,260),"A COMEBACK?",A(120)),a1,dy=(1-a1)*24)
    # NOT YET glitch
    if t>=tn-0.1:
        sh=(math.sin(t*90)*12*(1-seg(t,tn,tn+0.4))) if t<tn+0.4 else 0
        ny=glayer((W/2,420),"NOT YET.",A(170),top=(255,150,110),bot=(214,60,36)); a=eo3(seg(t,tn-0.1,tn+0.1))
        comp(img,glow(ny,RED,26,0.55),a*(0.5+0.2*math.sin(t*3)),sc=lerp(1.6,1,eob(seg(t,tn-0.1,tn+0.35),1.3)),dx=sh); comp(img,ny,a,sc=lerp(1.6,1,eob(seg(t,tn-0.1,tn+0.35),1.3)),dx=sh)
    pr=eo3(seg(t,tr,tr+0.5))
    l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((70,560,1010,760),radius=28,fill=(10,14,10,225),outline=EMBER+(170,),width=3)
    txt(dl,(W/2,650),"EVERY NEW RECORD IS",B(48),CREAM); txt(dl,(W/2,725),"A REASON TO PROTECT THAT FOREST",A(54),EMBER)
    comp(img,l,pr,dy=(1-pr)*30)
    # portrait circle
    r=250; cxp,cyp=265,250; mk=Image.new("L",(2*r,2*r),0); ImageDraw.Draw(mk).ellipse((0,0,2*r-1,2*r-1),fill=255)
    z=1+0.07*ease(k/10); hw=170/z; x0_,y0_=cxp-hw,cyp-hw*0.98
    M=np.array([[2*r/(2*hw),0,-x0_*2*r/(2*hw)],[0,2*r/(2*hw),-y0_*2*r/(2*hw)]],np.float32); ph=cv2.warpAffine(WK,M,(2*r,2*r),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
    ph=grade_spot(ph,r,r*0.95,r*0.75,r*0.75,eo3(seg(k,0.3,1.2))); p=Image.fromarray(ph.astype(np.uint8)).convert("RGBA"); p.putalpha(mk)
    ap=eo3(seg(t,tq-0.3,tq+0.3)); 
    if ap>0:
        img.alpha_composite(amul(p,ap),(W//2-r,830)); d=ImageDraw.Draw(img,"RGBA"); d.ellipse((W//2-r-4,826,W//2+r+4,830+2*r+4),outline=RUST+(int(255*ap),),width=5)
    qa=eo3(seg(t,tq,tq+0.4))
    comp(img,glayer((W/2,1440),"EVER SEEN A DHOLE?",A(92)),qa,dy=(1-qa)*24)
    btn=L(); ImageDraw.Draw(btn,"RGBA").rounded_rectangle((W/2-330,1480,W/2+330,1572),radius=46,fill=RUST+(250,))
    f=B(44); s1_="COMMENT \""; s2_="DHOLE"; s3_="\" + WHERE"; tw=f.getlength(s1_+s2_+s3_); x0=W/2-tw/2
    a1_=L(); txt(ImageDraw.Draw(a1_,"RGBA"),(x0,1543),s1_,f,INK,255,"ls"); x2=x0+f.getlength(s1_); w2=f.getlength(s2_)
    a3_=L(); txt(ImageDraw.Draw(a3_,"RGBA"),(x2+w2,1543),s3_,f,INK,255,"ls")
    ba=eo3(seg(t,tw_,tw_+0.4)); comp(img,btn,ba,sc=lerp(0.6,1,eob(seg(t,tw_,tw_+0.5)))); comp(img,a1_,eo3(seg(t,tw_+0.3,tw_+0.5))); comp(img,a3_,eo3(seg(t,tw_+0.3,tw_+0.5)))
    n=int(5*seg(t,tcm,tcm+0.8)+0.999) if t>tcm else 0
    if n>0:
        w=L(); txt(ImageDraw.Draw(w,"RGBA"),(x2,1543),s2_[:n],f,(255,246,230),255,"ls"); comp(img,w,1)
    cl=L(); dc=ImageDraw.Draw(cl,"RGBA")
    for i,s in enumerate(["Photos: Wikimedia Commons; Scroll.in (Bandipur); India Today NE; Imphal Times / ENFOGAL.","Images belong to their respective owners. DM for credit or removal."]): txt(dc,(W/2,1630+i*34),s,BM(24),GREY,235)
    comp(img,cl,eo3(seg(t,tw_+0.3,tw_+0.8)))
    return img
SC=[("S1",0.0,S1),("S2",S1END,S2),("S3",S2END,S3),("S4",S3END,S4),("S5",S4END,S5),("S6",S5END,S6),("S7",S6END,S7),("S8",S7END,S8)]
VIGN=None;GRN=None
def finish(fr,t):
    global VIGN,GRN
    if VIGN is None:
        yy,xx=np.mgrid[0:H,0:W]; dd=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2); VIGN=(1-0.30*np.clip(dd-0.45,0,1)**1.3).astype(np.float32)[:,:,None]
        GRN=np.random.default_rng(3).normal(0,3.5,(H+64,W+64,1)).astype(np.float32)
    ox=int((t*977)%64); oy=int((t*613)%64); return np.clip(fr*VIGN+GRN[oy:oy+H,ox:ox+W],0,255).astype(np.uint8)
def frame(t):
    i=max(j for j,(n,s,f) in enumerate(SC) if s<=t+1e-6)
    fr=np.array(SC[i][2](t))[...,:3].astype(np.float32)
    for n,s,f in SC[1:]:
        dd=t-s
        if 0<=dd<0.22: fr=fr+(1-dd/0.22)*50
        if -0.12<dd<0:
            sc=1+0.06*(1+dd/0.12); fr=cv2.warpAffine(fr,np.array([[sc,0,W/2*(1-sc)],[0,sc,H/2*(1-sc)]],np.float32),(W,H),borderMode=cv2.BORDER_REFLECT)
    fade=min(1,t/0.25)*min(1,(TOTAL-t)/0.6)
    return finish(np.clip(fr*fade,0,255),t)
if __name__=="__main__":
    for tt in [float(a) for a in sys.argv[1:]]: Image.fromarray(frame(tt)).save(f"q_{tt:05.1f}.jpg",quality=85)
