from vid import *
rng=np.random.default_rng(5)
DHANU=(79.42,9.18); TALAI=(79.72,9.09)
VIG=None; GRAIN=None
def finish(fr,t):
    global VIG,GRAIN
    if VIG is None:
        yy,xx=np.mgrid[0:H,0:W]; d=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2); VIG=(1-0.30*np.clip(d-0.45,0,1)**1.3).astype(np.float32)[:,:,None]
        GRAIN=np.random.default_rng(3).normal(0,4.0,(H+64,W+64,1)).astype(np.float32)
    ox=int((t*977)%64); oy=int((t*613)%64)
    return np.clip(fr*VIG+GRAIN[oy:oy+H,ox:ox+W],0,255).astype(np.uint8)
def tag_ill(fr,y,a=1.0): text(fr,"ILLUSTRATIVE MAP. DEPTHS APPROXIMATE.",bar(24),(170,170,160),64,y,a)
# ---------------- scenes
def S_eye(t):
    p=t/1.9; fr=pwin("454eb397",0.592,0.470,lerp(0.17,0.14,p),W,H,0.92).copy()
    gradv(fr,1300,H,0.0,0.5); return fr
def S_hook(t):
    p=ease(seg(t,1.9,5.6)); k=lerp(52,265,p**1.1); lonc=lerp(80.0,79.65,p); latc=lerp(16.0,8.75,p)
    fr=map_img(lonc,latc,k,W,H)
    # dotted line
    a=ease(seg(t,4.1,5.0)); (x0,y0)=ll2px(*DHANU,lonc,latc,k,W,H); (x1,y1)=ll2px(*TALAI,lonc,latc,k,W,H)
    if a>0:
        n=14
        for i in range(n):
            f0=i/n; f1=(i+0.55)/n
            if f1<=a+0.001:
                cv2.line(fr,(int(lerp(x0,x1,f0)),int(lerp(y0,y1,f0))),(int(lerp(x0,x1,f1)),int(lerp(y0,y1,f1))),(255,230,160),5,cv2.LINE_AA)
        ring(fr,x0,y0,18+10*math.sin(t*6),GOLD,a*0.9,3); ring(fr,x1,y1,18+10*math.sin(t*6+1),GOLD,a*0.9,3)
        pill(fr,"UNDER 50 KM",(x0+x1)/2,y0-130,ease(seg(t,4.6,5.2)),fg=(20,16,8),bg=GOLD,size=40,anchor="c")
    a1=ease(seg(t,2.3,2.8)); pill(fr,"INDIA: WILD TIGERS",70,600,a1,fg=(20,16,8),bg=GOLD,size=40)
    a2=ease(seg(t,4.5,5.0)); pill(fr,"SRI LANKA: NONE",70,1180,a2,fg=(255,230,224),bg=(120,34,28),size=40)
    gradv(fr,1500,H,0.0,0.55); return fr
SPECIES=[("ELEPHANTS",(80.90,6.43),8.1,"l"),("SLOTH BEARS",(80.02,8.45),9.1,"l"),("LEOPARDS",(81.42,6.37),10.1,"r")]
def S_species(t):
    p=seg(t,7.35,12.83); k=lerp(188,212,p); lonc,latc=80.7,7.9
    fr=map_img(lonc,latc,k,W,H); text(fr,"SRI LANKA",anton(110),GOLD,64,260,ease(seg(t,7.4,7.9)))
    for name,(lo,la),ts,side in SPECIES:
        a=ease(seg(t,ts,ts+0.35)); 
        if a<=0: continue
        x,y=ll2px(lo,la,lonc,latc,k,W,H); ring(fr,x,y,16+8*((t-ts)%1.2)*3,GOLD,a*(1-((t-ts)%1.2)/1.2)*0.8,3); cv2.circle(fr,(int(x),int(y)),9,(255,230,160),-1,cv2.LINE_AA)
        w=pill(fr,name,0,-200,0,size=38) if False else None
        f=bcs(38); d=ImageDraw.Draw(Image.new("L",(4,4))); tw=d.textlength(name,font=f)+44
        px=x+60 if side=="r" else x-60-tw; py=y-30
        cv2.line(fr,(int(x),int(y)),(int(px+(0 if side=="r" else tw)),int(py+32)),(255,230,160),2,cv2.LINE_AA)
        pill(fr,name,px,py,a,size=38)
    a=ease(seg(t,11.0,11.5))
    if a>0:
        cx,cy=ll2px(80.7,7.65,lonc,latc,k,W,H)
        for i in range(24):
            if i%2==0:
                a0=i*math.pi/12; a1=(i+1)*math.pi/12; pts=[(int(cx+210*math.cos(a)),int(cy+210*math.sin(a))) for a in np.linspace(a0,a1,6)]
                cv2.polylines(fr,[np.array(pts)],False,RED,5,cv2.LINE_AA)
        text(fr,"?",anton(260),(255,214,200),cx,cy-150,a,anchor="c")
    gradv(fr,1500,H,0.0,0.55); return fr
def S_water(t):
    if t<15.8:
        p=(t-12.83)/3.0; fr=pwin("260a7220",0.34,0.52,lerp(0.40,0.34,p),W,H,0.95).copy()
        gradv(fr,0,420,0.5,0.0); gradv(fr,1250,H,0.0,0.6)
        text(fr,"TIGERS SWIM",anton(120),GOLD,64,300,ease(seg(t,13.2,13.7)),rise=30)
        return fr
    k=lerp(470,560,seg(t,15.8,18.75)); lonc,latc=79.62,9.10
    fr=map_img(lonc,latc,k,W,H)
    text(fr,"PALK STRAIT",anton(90),GOLD,64,260,ease(seg(t,15.9,16.4)))
    x,y=ll2px(79.55,9.15,lonc,latc,k,W,H)
    for s0 in (16.3,17.1,17.9):
        q=(t-s0)/1.4
        if 0<q<1: ring(fr,x,y,40+520*q,(255,230,160),(1-q)*0.8,4)
    text(fr,"UNDER 35 M DEEP",anton(100),(255,236,180),W/2,1260,ease(seg(t,16.6,17.1)),anchor="c",rise=30)
    tag_ill(fr,1440,ease(seg(t,16.6,17.1))); gradv(fr,1500,H,0.0,0.5); return fr
def S_drain(t):
    MH=1130; k=205; lonc,latc=79.9,8.7
    level=-120*ease(seg(t,19.0,23.9))
    m=map_img(lonc,latc,k,W,MH,level); fr=np.zeros((H,W,3),np.uint8); fr[:MH]=m
    p=seg(t,18.75,27.0); ph=pwin("a4bcbe52",0.5,0.30,lerp(0.92,0.84,p),W,H-MH,0.95); fr[MH:]=ph
    cv2.line(fr,(0,MH),(W,MH),GOLD,3)
    gradv(fr,MH,MH+70,0.5,0.0)
    text(fr,"SEA LEVEL",bcs(34),(200,196,184),64,170,ease(seg(t,18.9,19.3)))
    text(fr,f"{int(round(level))} M" if level<-0.5 else "0 M",anton(150),GOLD,60,196,ease(seg(t,18.9,19.3)))
    if level<-35:
        a=ease(seg(t,21.2,22.0)); (x0,y0)=ll2px(*DHANU,lonc,latc,k,W,MH); (x1,y1)=ll2px(*TALAI,lonc,latc,k,W,MH)
        cv2.line(fr,(int(x0),int(y0)),(int(x1),int(y1)),(255,236,170),max(2,int(7*a)),cv2.LINE_AA)
        ring(fr,(x0+x1)/2,(y0+y1)/2,30+20*math.sin(t*5),GOLD,a*0.8,3)
        text(fr,"LAND BRIDGE",anton(64),(255,236,180),(x0+x1)/2-250,y0-150,ease(seg(t,22.0,22.6)),anchor="l")
    a=ease(seg(t,23.5,24.2))
    if a>0:
        text(fr,"MORE THAN HALF OF THE LAST 500,000 YEARS",bcs(34),CREAM,64,935,a)
        rrect(fr,64,985,1016,1030,fill=(20,24,22),outline=GOLD,a=a,r=8,w=2)
        wfill=int(952*0.58*ease(seg(t,24.0,25.4))); 
        if wfill>2: rrect(fr,64,985,64+wfill,1030,fill=GOLD,a=1.0,r=8,w=1)
        text(fr,"LAND-CONNECTED",bcs(30),(20,16,8),80,990,a*ease(seg(t,25.0,25.6)))
    tag_ill(fr,1088,0.9); return fr
def S_eyes2(t):
    p=(t-27.0)/3.65; fr=pwin("a4bcbe52",0.5,0.365,lerp(0.50,0.40,p),W,H,0.95).copy(); gradv(fr,1300,H,0.0,0.4); return fr
def S_black(t): return np.zeros((H,W,3),np.uint8)
def card(fr,x,y,lines,a,w=520):
    h=36+sum(l[1]+10 for l in lines)
    rrect(fr,x,y,x+w,y+h,fill=(10,14,12),outline=GOLD,a=a,r=14,w=3); yy=y+20
    for txt,sz,fnt,col in lines: text(fr,txt,fnt(sz),col,x+24,yy,a); yy+=sz+10
def S_fossil(t):
    p=ease(seg(t,32.1,35.8)); k=lerp(190,400,p); lonc=lerp(80.7,80.25,p); latc=lerp(7.9,6.95,p)
    fr=map_img(lonc,latc,k,W,H); x,y=ll2px(80.39,6.74,lonc,latc,k,W,H)
    q=((t-32.5)%1.5)/1.5
    ring(fr,x,y,20+110*q,GOLD,(1-q)*0.9,4); cv2.circle(fr,(int(x),int(y)),11,(255,236,170),-1,cv2.LINE_AA)
    a1=ease(seg(t,32.9,33.4)); a2=ease(seg(t,36.9,37.4))
    if a1>0:
        cv2.line(fr,(int(x),int(y)),(int(x-60),int(y-300)),(255,230,160),2,cv2.LINE_AA)
        card(fr,60,int(y-300-250),[("TOE BONE",64,anton,CREAM),("~16,500 YEARS OLD",44,bcs,GOLD),("Batadomba Cave, near Kuruwita",30,bar,(220,216,204))],a1,w=560)
    if a2>0:
        cv2.line(fr,(int(x),int(y)),(int(x+80),int(y+260)),(255,230,160),2,cv2.LINE_AA)
        card(fr,int(x-120),int(y+260),[("TOOTH",64,anton,CREAM),("LOWER CARNASSIAL",40,bcs,GOLD),("Near Ratnapura",30,bar,(220,216,204))],a2,w=560)
    a3=ease(seg(t,41.6,42.1))
    if a3>0:
        rrect(fr,70,730,1010,1010,fill=(10,14,12),outline=GOLD,a=a3,r=10,w=4)
        text(fr,"TENTATIVE ID",bcs(40),GOLD,110,755,a3); text(fr,"TIGER?",anton(150),CREAM,106,795,a3)
        text(fr,"Manamendra-Arachchi et al., 2005",bar(30),(220,216,204),110,945,a3)
    gradv(fr,1500,H,0.0,0.4); return fr
def leaf_mask(t0,t,seed=2):
    p=ease(seg(t,t0,t0+0.7)); r=np.random.default_rng(seed); n=cv2.resize(r.normal(0,1,(24,14)).astype(np.float32),(W,H),interpolation=cv2.INTER_CUBIC)
    yy,xx=np.mgrid[0:H,0:W]; diag=(xx/W*0.55+(1-yy/H)*0.75)
    return np.clip((p*1.7-diag)*6+n*0.5,0,1)[:,:,None]
def S_peek(t):
    base=S_fossil(44.79); p=(t-44.8)/4.1; ph=pwin("454eb397",0.49,0.46,lerp(0.395,0.36,p),W,H,0.95).astype(np.float32)
    m=leaf_mask(44.8,t); fr=(base*(1-m)+ph*m).astype(np.uint8)
    gradv(fr,1150,H,0.0,0.55)
    a=ease(seg(t,45.6,46.0)); pill(fr,"HYPOTHESIS",64,1200,a,fg=(20,16,8),bg=GOLD,size=46)
    a=ease(seg(t,47.4,47.8)); pill(fr,"STILL DEBATED",64,1310,a,fg=CREAM,bg=(12,14,12),size=46,outline=GOLD)
    return fr
POP=[(80.7,7.9),(80.5,7.5),(80.9,7.4),(80.3,8.2),(81.1,8.0),(80.6,7.0),(81.0,6.8),(80.2,7.6),(80.8,8.5),(81.3,7.6),(80.4,6.9),(80.95,7.9)]
def S_rise(t):
    k=290; lonc,latc=80.0,8.8
    level=-120*(1-ease(seg(t,49.5,54.3))); fr=map_img(lonc,latc,k,W,H,level)
    text(fr,"SEA LEVEL",bcs(34),(200,196,184),64,170); text(fr,f"{int(round(level))} M" if level<-0.5 else "0 M",anton(150),GOLD,60,196)
    a=ease(seg(t,52.4,53.0)); text(fr,"BRIDGE FLOODED",anton(80),CREAM,64,400,a,rise=30); text(fr,"~10,000 YEARS AGO",anton(80),GOLD,64,488,a,rise=30)
    # population dots
    for i,(lo,la) in enumerate(POP):
        keep=i<3; a0=ease(seg(t,54.3+i*0.04,54.8+i*0.04)); a1=1.0 if keep else 1-ease(seg(t,55.4+i*0.18,55.9+i*0.18))
        a=a0*a1
        if a>0.02:
            x,y=ll2px(lo,la,lonc,latc,k,W,H); cv2.circle(fr,(int(x),int(y)),11,(255,214,120),-1,cv2.LINE_AA); ring(fr,x,y,22,GOLD,a*0.5,2)
    a=ease(seg(t,56.4,57.0)); text(fr,"SMALL, ISOLATED POPULATION",bcs(52),(255,236,180),W/2,1420,a,anchor="c")
    tag_ill(fr,1488,0.9); gradv(fr,1560,H,0.0,0.5)
    # fade in from black
    fade(fr,1-ease(seg(t,48.9,49.5))); return fr
def S_lion(t):
    k=205; fr=map_img(80.7,7.9,k,W,H); fr=(fr*0.35).astype(np.uint8); gradv(fr,0,H,0.2,0.2)
    a=ease(seg(t,59.2,59.8)); fade_l=1-0.78*ease(seg(t,63.0,63.6))
    text(fr,"LION",anton(260),CREAM,W/2,430,a*fade_l,anchor="c",rise=40)
    text(fr,"GONE BEFORE ~37,000 YEARS AGO",bcs(46),GOLD,W/2,740,a*fade_l,anchor="c")
    sl=ease(seg(t,63.0,63.5))
    if sl>0:
        d=ImageDraw.Draw(Image.fromarray(fr)); 
        cv2.line(fr,(int(W/2-250),int(570)),(int(W/2-250+500*sl),int(570)),(214,96,78),9,cv2.LINE_AA)
    a=ease(seg(t,64.8,65.4)); 
    if a>0:
        ring(fr,W/2,1090,120+80*((t-64.8)%1.5)/1.5,GOLD,a*(1-((t-64.8)%1.5)/1.5)*0.7,4)
    text(fr,"LEOPARD",anton(260),GOLD,W/2,980,a,anchor="c",rise=40); text(fr,"STILL THERE",bcs(54),CREAM,W/2,1290,ease(seg(t,65.5,66.0)),anchor="c")
    fade(fr,1-ease(seg(t,58.9,59.3))); return fr
MONT=[("ce145a99",.56,.62,.92,.80),("4d5819bf",.54,.52,.62,.54),("0a195c9b",.62,.60,.40,.34),("05008004",.50,.66,.46,.38)]
def S_montage(t):
    i=min(3,int((t-67.3)/1.375)); k,cx,cy,w0,w1=MONT[i]; p=((t-67.3)-i*1.375)/1.375
    fr=pwin(k,cx,cy,lerp(w0,w1,p),W,H,0.95).copy()
    if (t-67.3)-i*1.375<0.1 and i>0: fade(fr,0.5*(1-((t-67.3)-i*1.375)/0.1),(255,255,255))
    gradv(fr,1000,1560,0.0,0.82)
    if t<70.0:
        a=ease(seg(t,67.35,67.7)); text(fr,"THE SEA DIDN'T",anton(88),CREAM,64,1230,a,rise=30); text(fr,"KEEP THEM OUT.",anton(88),GOLD,64,1320,a,rise=30)
    else:
        a=ease(seg(t,70.0,70.35)); text(fr,"THE ISLAND MAY NOT",anton(80),CREAM,64,1200,a,rise=30); text(fr,"HAVE KEPT THEM IN.",anton(80),GOLD,64,1285,a,rise=30)
        pill(fr,"BEST-SUPPORTED EXPLANATION, NOT PROVEN",64,1400,ease(seg(t,70.6,71.0)),size=30,fg=(20,16,8),bg=GOLD)
    return fr
def S_hero(t):
    p=ease(seg(t,72.8,79.0)); fr=pwin("a4bcbe52",0.5,lerp(0.42,0.50,p),lerp(0.40,0.70,p),W,H,0.95).copy()
    gradv(fr,950,1600,0.0,0.75)
    a=ease(seg(t,77.3,77.9)); text(fr,"THE NATURAL ANGLE",anton(76),GOLD,W/2,1190,a,anchor="c",rise=30); text(fr,"Photos: Hitesh Chawla",bar(34),CREAM,W/2,1290,ease(seg(t,77.6,78.2)),anchor="c")
    fade(fr,ease(seg(t,79.0,80.0))); return fr
SC=[(0,1.9,S_eye,0),(1.9,7.35,S_hook,0.18),(7.35,12.83,S_species,0.25),(12.83,18.75,S_water,0.2),(18.75,30.65,lambda t: S_drain(t) if t<27.0 else S_eyes2(t),0.25),(30.65,32.1,S_black,0.0),(32.1,44.8,S_fossil,0.0),(44.8,48.9,S_peek,0.0),(48.9,58.9,S_rise,0.0),(58.9,67.3,S_lion,0.0),(67.3,72.8,S_montage,0.0),(72.8,80.01,S_hero,0.25)]
def frame(t):
    for i,(a,b,fn,tr) in enumerate(SC):
        if a<=t<b: break
    fr=fn(t)
    if tr>0 and t<a+tr and i>0:
        pa,pb,pfn,_=SC[i-1]; prev=pfn(min(t,pb-1/FPS)); m=1-ease((t-a)/tr)
        fr=(prev*m+fr*(1-m)).astype(np.uint8)
    if t<1.9 and False: pass
    # flash at hook cut
    if 1.9<=t<2.05: fr=(fr*0.5+255*0.5*(1-(t-1.9)/0.15)).astype(np.uint8)
    return finish(fr.astype(np.float32),t)
if __name__=="__main__":
    ts=[float(x) for x in sys.argv[1:]] or [1,3,5,9,14,17,20,22,24,29,31,34,38,42,46,50,53,56,61,65,68,71,75,79]
    for t in ts:
        cv2.imwrite(f"test_{t:05.1f}.jpg",cv2.cvtColor(frame(t),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,88])
