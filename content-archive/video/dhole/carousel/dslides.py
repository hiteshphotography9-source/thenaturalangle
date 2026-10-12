import sys; sys.path.insert(0,'.')
from dcore import *
WK=ldarr('wiki_dhole.png'); PK=ldarr('pack_bandipur.png'); TR=ldarr('imphal_trap.png')
FBI=Image.open(ID+'fb_assam.png').convert('RGB').crop((0,0,1080,1130)); IMH=Image.open(ID+'imphal_head.png').convert('RGB')

def s1():
    base=jungle(21); d=ImageDraw.Draw(base,"RGBA")
    credit(d,"Photo: Wikimedia Commons",y=790,x=W-60,anchor="rs"); chrome(base,1)
    top=L(); txt(ImageDraw.Draw(top,"RGBA"),(W/2,900),"WRITTEN OFF FOR DECADES.",B(58),CREAM)
    big=glayer((W/2,1110),"IT'S BACK.",A(210)); bg=glow(big,RUST,26,0.7)
    sub=L(); txt(ImageDraw.Draw(sub,"RGBA"),(W/2,1200),"INDIA'S FORGOTTEN PACK HUNTER, THE DHOLE",B(42),GREY)
    rect=(60,118,960,638); face=(265,235,170,150)
    def fr(t):
        img=base.copy()
        fl=max(0,1-abs(t-0.62)/0.14)*1.0 if 0.45<t<0.8 else 0
        k=eo3(seg(t,0.75,1.7)); ds=1-eo3(seg(t,0.6,0.9))
        tm=pwin(img,WK,(0,0,984,654),rect,z=1+0.08*ease(t/6.5),spot=face,k=k,flash=fl,desat=ds*0.9)
        d=ImageDraw.Draw(img,"RGBA")
        b=eo3(seg(t,0.9,1.7)); fx,fy=tm(face[0],face[1])
        x0=lerp(rect[0]+20,fx-170,b); x1=lerp(rect[0]+rect[2]-20,fx+170,b); y0=lerp(rect[1]+20,fy-150,b); y1=lerp(rect[1]+rect[3]-20,fy+150,b)
        brackets(d,x0,y0,x1,y1,EMBER,min(1,seg(t,0.8,1.0))*(0.75+0.25*math.sin(t*5)))
        comp(img,top,eo3(seg(t,0.0,0.5)))
        p=seg(t,1.5,2.0); s=lerp(1.7,1.0,eob(p,1.4)); a=eo3(seg(t,1.5,1.7))
        sh=(math.sin(t*90)*10*(1-seg(t,2.0,2.3))) if 2.0<t<2.3 else 0
        comp(img,bg,a*(0.55+0.25*math.sin(t*3)),sc=s,dx=sh); comp(img,big,a,sc=s,dx=sh)
        shine(img,big,seg(t,3.0,4.0)); shine(img,big,seg(t,5.2,6.2))
        comp(img,sub,eo3(seg(t,2.2,2.7)),dy=(1-eo3(seg(t,2.2,2.7)))*20)
        return img
    return fr,6.5

def s2():
    base=jungle(22); base.alpha_composite(glayer((W/2,196),"MEET THE DHOLE",A(112)))
    d=ImageDraw.Draw(base,"RGBA"); credit(d,"Photo: Bandipur NP, as published by Scroll.in",y=790,x=W-60,anchor="rs")
    txt(d,(60,790),"ASIATIC WILD DOG · CUON ALPINUS",B(30),SAGE,230,"ls"); chrome(base,2)
    chips=[("ENDANGERED","IUCN RED LIST"),("10-20 KG","LIGHTER THAN A LEOPARD CUB"),("5 TO 12","PER PACK, SOMETIMES 30+"),("WHISTLES","TO TALK IN THICK FOREST")]
    chips[1]=("10-20 KG","SIZE OF A MID-SIZE DOG")
    pos=[(300,930),(780,930),(300,1150),(780,1150)]
    lays=[]
    for (v,l),(cx,cy) in zip(chips,pos):
        lay=L(); dl=ImageDraw.Draw(lay,"RGBA"); dl.rounded_rectangle((cx-225,cy-95,cx+225,cy+95),radius=26,fill=(10,12,8,215),outline=CREAM+(70,),width=2)
        txt(dl,(cx,cy+8),v,A(66),CREAM); txt(dl,(cx,cy+58),l,B(28),GREY); lays.append(lay)
    hl=[]
    for (v,l),(cx,cy) in zip(chips,pos):
        lay=L(); dl=ImageDraw.Draw(lay,"RGBA"); dl.rounded_rectangle((cx-225,cy-95,cx+225,cy+95),radius=26,fill=(48,22,8,235),outline=RUST+(255,),width=4)
        txt(dl,(cx,cy+8),v,A(66),EMBER); txt(dl,(cx,cy+58),l,B(28),CREAM); hl.append(lay)
    T0=[0.9,1.6,2.3,3.0]; spot=(470,300,330,260)
    def fr(t):
        img=base.copy()
        pwin(img,PK,(0,0,1080,565),(60,250,960,502),z=1+0.07*ease(t/6),spot=spot,k=eo3(seg(t,0.2,1.0)))
        for i in range(4):
            a=eo3(seg(t,T0[i],T0[i]+0.3)); s=lerp(0.75,1,eob(seg(t,T0[i],T0[i]+0.5)))
            act=seg(t,T0[i],T0[i]+0.15)*(1-seg(t,T0[i]+0.6,T0[i]+0.9)) if i<3 else seg(t,T0[i],T0[i]+0.15)
            if i==3 and t>3.6: act=0.65+0.35*math.sin((t-3.6)*3)
            comp(img,lays[i],a,sc=s); 
            if act>0: comp(img,glow(hl[i],RUST,20,0.5),act*0.6,sc=s); comp(img,hl[i],act,sc=s)
        if t>3.2:
            d=ImageDraw.Draw(img,"RGBA"); cx,cy=780,1150; pts=[]
            for x in range(-150,151,4):
                env=math.exp(-(x/110)**2); pts.append((cx+x,cy-62+math.sin(x*0.09-t*9)*16*env*seg(t,3.2,3.6)))
            d.line(pts,fill=EMBER+(230,),width=3)
        return img
    return fr,6.0

def s3():
    base=jungle(23); base.alpha_composite(glayer((W/2,196),"HOW CLOSE IT CAME",A(108))); chrome(base,3)
    cx,cy,R=540,500,215
    lab=L(); txt(ImageDraw.Draw(lab,"RGBA"),(cx,cy+R+80),"OF ITS HISTORIC RANGE: GONE",B(46),CREAM)
    box2=L(); d2=ImageDraw.Draw(box2,"RGBA"); d2.rounded_rectangle((70,890,W-70,1080),radius=26,fill=(10,12,8,215),outline=RUST+(150,),width=3)
    txt(d2,(W/2,1050),"BREEDING ADULTS LEFT ON EARTH (2015 ESTIMATE)",B(34),GREY)
    box3=L(); d3=ImageDraw.Draw(box3,"RGBA"); d3.rounded_rectangle((70,1120,W-70,1320),radius=26,fill=(10,12,8,215),outline=RED+(150,),width=3)
    txt(d3,(W/2,1190),"IN INDIA IT WAS HUNTED AS \"VERMIN\" FOR BOUNTY",B(40),CREAM)
    l3=glayer((W/2,1282),"PROTECTED ONLY IN 1972",A(66),top=(255,150,130),bot=(222,60,46))
    cache={}
    def fr(t):
        img=base.copy(); d=ImageDraw.Draw(img,"RGBA")
        f1=1-0.35*seg(t,2.2,2.6)
        d.ellipse((cx-R,cy-R,cx+R,cy+R),outline=(255,255,255,int(28)),width=44)
        p=ease(seg(t,0.4,2.0))*0.75
        if p>0: d.arc((cx-R,cy-R,cx+R,cy+R),start=-90,end=-90+360*p,fill=tuple(int(c*f1) for c in RUST)+(255,),width=44)
        n=int(round(75*p/0.75)); key=('p',n)
        if key not in cache: cache[key]=glayer((cx,cy+34),f"{n}%+",A(96))
        comp(img,cache[key],f1)
        comp(img,lab,eo3(seg(t,1.6,2.0))*f1)
        a=eo3(seg(t,2.2,2.5)); comp(img,box2,a,sc=lerp(0.9,1,eob(seg(t,2.2,2.7))))
        if a>0:
            q=ease(seg(t,2.3,3.4)); lo=int(949*q); hi=int(2215*q); key=('c',lo)
            if key not in cache: cache[key]=glayer((W/2,1000),f"{lo:,} TO {hi:,}",A(96))
            comp(img,cache[key],a*(1-0.35*seg(t,3.6,4.0)))
        a3=eo3(seg(t,3.6,3.9)); comp(img,box3,a3,dy=(1-a3)*30)
        img.alpha_composite(wipe(l3,eo3(seg(t,3.9,4.7))))
        shine(img,l3,seg(t,4.9,5.8))
        return img
    return fr,6.0

def s4():
    base=jungle(24); d=ImageDraw.Draw(base,"RGBA")
    txt(d,(W/2,160),"COMEBACK #1 · KAZIRANGA-KARBI ANGLONG, ASSAM",B(38),SAGE)
    base.alpha_composite(glayer((W/2,280),"ONE NIGHT. SIX PHOTOS.",A(104)))
    d=ImageDraw.Draw(base,"RGBA"); credit(d,"Image: India Today NE",y=H-46); chrome(base,4)
    stats=[("83","CAMERA TRAPS"),("2 YRS","OF WATCHING"),("1","LONE DHOLE"),("6","PHOTOS")]
    info=L(); di=ImageDraw.Draw(info,"RGBA"); di.rounded_rectangle((60,1040,W-60,1320),radius=26,fill=(10,12,8,215),outline=RUST+(120,),width=2)
    txt(di,(W/2,1105),"31 OCT 2022 · AMGURI CORRIDOR, NEAR A HIGHWAY",B(40),EMBER)
    txt(di,(W/2,1170),"First proof of a dhole in this landscape",B(40),CREAM); txt(di,(W/2,1220),"in about 30 years (as reported).",B(40),CREAM)
    txt(di,(W/2,1285),"Wildlife Institute of India study, published June 2025",BM(30),GREY)
    def fr(t):
        img=base.copy()
        p=eob(seg(t,0.2,0.9),1.2); fl=max(0,1-abs(t-0.85)/0.12) if 0.7<t<1.0 else 0
        cimg=FBI if fl<=0 else Image.fromarray(np.clip(np.array(FBI).astype(np.float32)+fl*170,0,255).astype(np.uint8))
        card(img,cimg,lerp(-300,330,p),700,0.5,lerp(8,-2.5,eo3(seg(t,0.2,0.9))),a=eo3(seg(t,0.2,0.4)))
        d=ImageDraw.Draw(img,"RGBA")
        for i,(v,l) in enumerate(stats):
            t0=1.1+i*0.45; a=eo3(seg(t,t0,t0+0.3)); y=450+i*150
            if a<=0: continue
            hot=(i==2)
            col=EMBER if hot else CREAM
            if hot:
                g=0.6+0.4*math.sin((t-t0)*4) if t>t0+0.3 else a
                d.rounded_rectangle((640,y-92,1030,y+38),radius=20,fill=(60,24,8,int(220*a)),outline=RUST+(int(255*g),),width=4)
            xo=(1-a)*60
            txt(d,(670+xo,y),v,A(84),col,255*a,"ls"); txt(d,(670+xo,y+30),l,B(30),GREY if not hot else CREAM,255*a,"ls")
        comp(img,info,eo3(seg(t,3.0,3.4)),dy=(1-eo3(seg(t,3.0,3.5)))*30)
        return img
    return fr,6.0

def s5():
    base=jungle(25); d=ImageDraw.Draw(base,"RGBA")
    txt(d,(W/2,160),"COMEBACK #2 · SHIRUI HILLS, MANIPUR",B(38),SAGE)
    base.alpha_composite(glayer((W/2,280),"A FIRST FOR MANIPUR",A(108)))
    d=ImageDraw.Draw(base,"RGBA"); credit(d,"Camera trap: ENFOGAL, as published by Imphal Times",y=834,x=W-60,anchor="rs"); chrome(base,5)
    l1=L(); txt(ImageDraw.Draw(l1,"RGBA"),(W/2,1190),"July 2026: first camera-trap record of a dhole in Manipur.",B(38),CREAM)
    l2=L(); txt(ImageDraw.Draw(l2,"RGBA"),(W/2,1245),"Locals believed dholes never lived in these hills.",B(38),GREY)
    f=B(38); s_a="Camera spot picked by a "; s_b="former hunter"; s_c=", now a conservationist."
    tw=f.getlength(s_a+s_b+s_c); x0=W/2-tw/2; xb=x0+f.getlength(s_a); wb=f.getlength(s_b)
    l3=L(); d3=ImageDraw.Draw(l3,"RGBA"); txt(d3,(x0,1318),s_a,f,CREAM,255,"ls"); txt(d3,(xb+wb,1318),s_c,f,CREAM,255,"ls")
    l3b=L(); txt(ImageDraw.Draw(l3b,"RGBA"),(xb,1318),s_b,f,EMBER,255,"ls")
    rect=(60,330,960,476); dog=(446,210,170,130)
    def fr(t):
        img=base.copy()
        fl=max(0,1-abs(t-0.5)/0.12) if 0.35<t<0.65 else 0
        tm=pwin(img,TR,(0,0,800,397),rect,z=1+0.06*ease(t/6),spot=dog,k=eo3(seg(t,0.6,1.4)),flash=fl,desat=0.9*(1-eo3(seg(t,0.45,0.7))),border=EMBER)
        d=ImageDraw.Draw(img,"RGBA"); fx,fy=tm(dog[0],dog[1]); b=eo3(seg(t,0.7,1.4))
        brackets(d,lerp(rect[0]+20,fx-180,b),lerp(rect[1]+20,fy-150,b),lerp(rect[0]+rect[2]-20,fx+180,b),lerp(rect[1]+rect[3]-20,fy+150,b),EMBER,seg(t,0.6,0.8)*(0.75+0.25*math.sin(t*5)))
        p=eob(seg(t,1.3,2.0),1.2); card(img,IMH,W/2,lerp(780,1000,p),0.86,lerp(-6,1.2,eo3(seg(t,1.3,2.0))),a=eo3(seg(t,1.3,1.5)))
        comp(img,l1,eo3(seg(t,2.2,2.6))); comp(img,l2,eo3(seg(t,2.6,3.0)))
        a3=eo3(seg(t,3.1,3.5)); comp(img,l3,a3); comp(img,l3b,a3)
        if t>3.6:
            u=eo3(seg(t,3.6,4.1)); d=ImageDraw.Draw(img,"RGBA"); d.line((xb,1330,xb+wb*u,1330),fill=RUST+(255,),width=5)
            gl=glow(l3b,RUST,14,0.6); comp(img,gl,(0.4+0.4*math.sin((t-3.6)*4))*u)
        return img
    return fr,6.0

def s6():
    sys.path.insert(0,SP+'pil'); import eng
    MW,MH=960,860; lonc,latc,k=82.6,18.3,34.8
    m=eng.map_img(lonc,latc,k,MW,MH,0,glow=0.3).astype(np.float32)
    g=m.mean(2,keepdims=True); m=(m*0.45+g*0.55)*np.array((0.62,0.66,0.55)); m=np.clip(m*0.85,0,255)
    base=jungle(26); base.alpha_composite(glayer((W/2,180),"WHERE THEY'RE SHOWING UP",A(92)))
    d=ImageDraw.Draw(base,"RGBA"); chrome(base,6)
    mk=Image.new("L",(MW,MH),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,MW-1,MH-1),radius=26,fill=255)
    mp=Image.fromarray(m.astype(np.uint8)).convert("RGBA"); mp.putalpha(mk); base.alpha_composite(mp,(60,230))
    d.rounded_rectangle((58,228,60+MW+1,230+MH+1),radius=26,outline=RUST+(150,),width=3)
    P=lambda lo,la:(60+(lo-lonc)*k*eng.C85+MW/2,230+(latc-la)*k+MH/2)
    # strongholds layer
    sl=Image.new("L",(W,H),0); ds=ImageDraw.Draw(sl)
    wg=[P(73.6,19.8),P(74.0,17.0),P(74.6,14.5),P(75.6,12.0),P(76.6,10.0),P(77.3,8.6)]
    ds.line(wg,fill=255,width=44,joint="curve")
    for lo,la,r in ((80.6,22.4,2.6),(93.6,26.4,1.6)):
        x,y=P(lo,la); rr=r*k; ds.ellipse((x-rr,y-rr*0.75,x+rr,y+rr*0.75),fill=255)
    sl=sl.filter(ImageFilter.GaussianBlur(22))
    strong=Image.new("RGBA",(W,H),RUST+(0,)); strong.putalpha(sl.point(lambda v:int(v*0.8)))
    sl_lab=L(); dl=ImageDraw.Draw(sl_lab,"RGBA")
    x,y=P(74.6,14.5); txt(dl,(x-24,y),"WESTERN GHATS",B(30),CREAM,240,"rs")
    x,y=P(81.2,20.6); txt(dl,(x,y+8),"CENTRAL INDIA",B(30),CREAM,240,"ms")
    pass
    pins=[(93.4,26.55,"ASSAM · 2022","rec. published 2025",(-30,-40),"rs"),(94.47,25.12,"MANIPUR · 2026","first ever",(-30,40),"rs"),
          (77.75,23.05,"RATAPANI TR · JAN 2026","first record",(30,-42),"ls"),(76.8,22.55,"KHIVNI WLS · 2025","after 25+ yrs (reported)",(-30,52),"rs")]
    T0=[1.4,1.9,2.4,2.9]
    leg=L(); dg=ImageDraw.Draw(leg,"RGBA"); dg.rounded_rectangle((60,1110,W-60,1330),radius=24,fill=(10,12,8,215),outline=RUST+(110,),width=2)
    dg.ellipse((100,1150,136,1186),fill=RUST+(200,)); txt(dg,(156,1180),"STRONGHOLDS: Western Ghats, Central India, North-East",B(34),CREAM,255,"ls")
    dg.ellipse((106,1222,130,1246),fill=EMBER+(255,),outline=CREAM+(255,),width=3); txt(dg,(156,1246),"NEW OR RETURNING RECORDS, 2022 TO 2026",B(34),EMBER,255,"ls")
    txt(dg,(W/2,1305),"Approximate locations. Not to scale.",BM(28),GREY)
    def fr(t):
        img=base.copy(); a=eo3(seg(t,0.3,1.1))*(0.85+0.15*math.sin(t*2.5))
        comp(img,strong,a); comp(img,sl_lab,eo3(seg(t,0.8,1.2)))
        d=ImageDraw.Draw(img,"RGBA")
        for i,(lo,la,l1,l2,(ox,oy),anc) in enumerate(pins):
            p=seg(t,T0[i],T0[i]+0.45)
            if p<=0: continue
            x,y=P(lo,la); yy=y-(1-eob(p,1.5))*120 if p<1 else y; a=eo3(seg(t,T0[i],T0[i]+0.15))
            for kk in range(2):
                r=((t-T0[i])*0.8+kk/2)%1; rr=10+r*46; d.ellipse((x-rr,y-rr,x+rr,y+rr),outline=EMBER+(int(200*(1-r)*a),),width=3)
            d.ellipse((x-13,yy-13,x+13,yy+13),fill=EMBER+(int(255*a),),outline=CREAM+(int(255*a),),width=3)
            la_=eo3(seg(t,T0[i]+0.3,T0[i]+0.6))
            if la_>0:
                tx,ty=x+ox,y+oy; f1=B(32); f2=BM(26)
                w_=max(f1.getlength(l1),f2.getlength(l2))+28
                bx0=tx-w_ if anc=="rs" else tx-14; bx0=max(64,min(bx0,W-64-w_))
                d.rounded_rectangle((bx0,ty-34,bx0+w_,ty+40),radius=12,fill=(10,12,8,int(225*la_)),outline=EMBER+(int(200*la_),),width=2)
                txt(d,(bx0+14,ty-2),l1,f1,CREAM,255*la_,"ls"); txt(d,(bx0+14,ty+30),l2,f2,GREY,255*la_,"ls")
        comp(img,leg,eo3(seg(t,3.5,3.9)),dy=(1-eo3(seg(t,3.5,4.0)))*30)
        return img
    return fr,6.0

def s7():
    base=jungle(27); d=ImageDraw.Draw(base,"RGBA")
    txt(d,(W/2,240),"COMEBACK?",A(120),CREAM); chrome(base,7)
    credit(d,"Photo: Wikimedia Commons",y=860,x=W-60,anchor="rs")
    ny=glayer((W/2,420),"NOT YET.",A(170),top=(255,150,110),bot=(214,60,36))
    pts=["Assam's record: one lone dog, on one night.","Most packs live in small, cut-off forests.","Threats: lost forest, lost prey, diseases from village dogs.","Every new record is a reason to protect that forest."]
    lays=[]
    for i,s in enumerate(pts):
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); y=950+i*96; last=(i==3)
        txt(dl,(110,y),s,B(40) if not last else A(42),EMBER if last else CREAM,255,"ls"); lays.append((l,y))
    def fr(t):
        img=base.copy()
        pwin(img,WK,(0,110,984,459),(60,480,960,340),z=1+0.06*ease(t/6),spot=(265,235,200,160),k=eo3(seg(t,1.0,1.8)),border=RUST)
        if 0.4<t<1.1:
            r=np.random.default_rng(int(t*30)); on=r.random()>0.35
            if on: comp(img,ny,0.9,dx=r.integers(-14,14))
        elif t>=1.1:
            comp(img,glow(ny,RED,22,0.5),0.5+0.2*math.sin(t*3)); comp(img,ny,1)
        d=ImageDraw.Draw(img,"RGBA")
        for i,(l,y) in enumerate(lays):
            t0=1.9+i*0.6; a=eo3(seg(t,t0,t0+0.35))
            if a<=0: continue
            act=1-seg(t,t0+0.5,t0+0.8) if i<3 else 1
            d.rounded_rectangle((70,y-36,80,y+6),radius=4,fill=(RUST if act>0.05 else (90,96,86))+(int(255*a),))
            comp(img,l,a*(1-0.35*(1-act)),dx=(1-a)*50)
        return img
    return fr,6.0

def s8():
    base=jungle(28); d=ImageDraw.Draw(base,"RGBA")
    base.alpha_composite(glayer((W/2,860),"EVER SEEN A DHOLE",A(100))); base.alpha_composite(glayer((W/2,968),"IN THE WILD?",A(100)))
    d=ImageDraw.Draw(base,"RGBA")
    cl=["Photos: Wikimedia Commons; Scroll.in (Bandipur); India Today NE;","Imphal Times / ENFOGAL camera trap.","Images belong to their respective owners. DM for credit or removal.","With respect to every photographer and field team."]
    y=1225
    for s in cl: txt(d,(W/2,y),s,BM(28),GREY,235); y+=38
    chrome(base,8,swipe=False)
    r=290; cxp,cyp=265,250
    mk=Image.new("L",(2*r,2*r),0); ImageDraw.Draw(mk).ellipse((0,0,2*r-1,2*r-1),fill=255)
    btn=L(); ImageDraw.Draw(btn,"RGBA").rounded_rectangle((W/2-320,1020,W/2+320,1112),radius=46,fill=RUST+(250,))
    f=B(44); s1_="COMMENT \""; s2_="DHOLE"; s3_="\" + WHERE"; tw=f.getlength(s1_+s2_+s3_); x0=W/2-tw/2
    a1=L(); txt(ImageDraw.Draw(a1,"RGBA"),(x0,1083),s1_,f,INK,255,"ls"); x2=x0+f.getlength(s1_); w2=f.getlength(s2_)
    a3=L(); txt(ImageDraw.Draw(a3,"RGBA"),(x2+w2,1083),s3_,f,INK,255,"ls")
    tip=L(); txt(ImageDraw.Draw(tip,"RGBA"),(W/2,1162),"Field tip: dholes vanish fast. Binoculars help you catch them first.",B(32),SAGE)
    def fr(t):
        img=base.copy(); z=1+0.08*ease(t/6); hw=175/z
        x0_,y0_=int(cxp-hw),int(cyp-hw); M=np.array([[2*r/(2*hw),0,-x0_*2*r/(2*hw)],[0,2*r/(2*hw),-y0_*2*r/(2*hw)]],np.float32)
        ph=cv2.warpAffine(WK,M,(2*r,2*r),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
        ph=grade_spot(ph,r,r*0.95,r*0.75,r*0.75,eo3(seg(t,0.2,1.0)))
        p=Image.fromarray(ph.astype(np.uint8)).convert("RGBA"); p.putalpha(mk); img.alpha_composite(p,(W//2-r,150))
        d=ImageDraw.Draw(img,"RGBA"); d.ellipse((W//2-r-4,146,W//2+r+4,150+2*r+4),outline=RUST+(255,),width=5)
        comp(img,btn,eo3(seg(t,0.4,0.7)),sc=lerp(0.5,1,eob(seg(t,0.4,1.0))))
        ta=eo3(seg(t,0.8,1.1)); comp(img,a1,ta); comp(img,a3,ta)
        n=int(5*seg(t,1.2,2.0)+0.999) if t>1.2 else 0
        if n>0:
            pul=1+0.05*max(0,math.sin((t-2.1)*3.2)) if t>2.1 else 1
            w=L(); txt(ImageDraw.Draw(w,"RGBA"),(x2,1083),s2_[:n],f,(255,246,230),255,"ls"); comp(img,w,1,sc=pul)
        comp(img,tip,eo3(seg(t,2.4,2.9)))
        return img
    return fr,6.0

SL=[s1,s2,s3,s4,s5,s6,s7,s8]
def job(i):
    fr,dur=SL[i](); render(f"Dhole_Motion_{i+1}.mp4",fr,dur)
    Image.fromarray(np.array(fr(dur-0.05))[...,:3]).save(f"Dhole_Carousel_{i+1}.jpg",quality=95); return i+1
if __name__=="__main__":
    from multiprocessing import Pool
    idx=[int(a)-1 for a in sys.argv[1:]] or list(range(8))
    with Pool(4) as pl: print(pl.map(job,idx))
