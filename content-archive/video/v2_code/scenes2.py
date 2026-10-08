from eng import *
OVER=1.16
def camk(t,keys):
    if t<=keys[0][0]: return keys[0][1:]
    for a,b in zip(keys[:-1],keys[1:]):
        if a[0]<=t<=b[0]:
            e=ease((t-a[0])/(b[0]-a[0])); return tuple(lerp(x,y,e) for x,y in zip(a[1:],b[1:]))
    return keys[-1][1:]
def mapframe(t,keys,level=0.0,deco=None,glow=1.0):
    lonc,latc,k,tilt,roll=camk(t,keys); w=int(W*OVER); h=int(H*OVER)
    img=map_img(lonc,latc,k,w,h,t,level,glow)
    if deco: deco(img,lambda lo,la: ll(lo,la,lonc,latc,k,w,h))
    cx,cy=w/2,h/2; src=np.float32([[cx-W/2,cy-H/2],[cx+W/2,cy-H/2],[cx+W/2,cy+H/2],[cx-W/2,cy+H/2]]); sh=tilt*W*0.5
    dst=np.float32([[sh,0],[W-sh,0],[W,H],[0,H]]); P=cv2.getPerspectiveTransform(src,dst)
    R=np.vstack([cv2.getRotationMatrix2D((W/2,H/2),roll,1.0),[0,0,1]]); Mt=R@P
    fr=cv2.warpPerspective(img,Mt,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    def proj(lo,la):
        x,y=ll(lo,la,lonc,latc,k,w,h); p=cv2.perspectiveTransform(np.float32([[[x,y]]]),Mt.astype(np.float32))[0,0]; return float(p[0]),float(p[1])
    return fr,proj
def coords_hud(fr,t,keys,a=1.0):
    lonc,latc,k,_,_=camk(t,keys); la=abs(latc); lo=lonc
    s=f"{int(la)}°{int((la%1)*60):02d}'{'N' if latc>=0 else 'S'}   {int(lo)}°{int((lo%1)*60):02d}'E"
    paste(fr,sprite(s,bcs(34),(150,245,240),sw=2,shadow=False),W/2,196,a*0.9)
def vscan(fr,t,a=0.12):
    y=int((t*260)%(H+200)-100); ov=np.zeros((H,W,3),np.float32); cv2.line(ov,(0,y),(W,y),(120,255,250),3); ov=cv2.GaussianBlur(ov,(0,0),12)*2.5; add(fr,ov,a)
def worldlabel(img,p,txt,f=None,col=(255,255,255),size=44,dy=-60,glow=(0,160,190)):
    x,y=p; sp=sprite(txt,bcs(size),col,sw=4,glow=glow,glow_r=9); paste(img,sp,x,y+dy,1.0)
# ---------------- icons / badges
def icon_foot(fr,cx,cy,s,col):
    cv2.ellipse(fr,(int(cx),int(cy+10*s)),(int(30*s),int(38*s)),0,0,360,col,-1,cv2.LINE_AA)
    for i,dx in enumerate((-34,-17,0,17,34)): cv2.ellipse(fr,(int(cx+dx*s),int(cy-34*s-abs(dx)*0.18*s)),(int(8*s),int(11*s)),0,0,360,col,-1,cv2.LINE_AA)
def icon_claw(fr,cx,cy,s,col):
    for dx in (-26,0,26):
        pts=np.array([[cx+dx*s-14*s,cy-42*s],[cx+dx*s-4*s,cy-10*s],[cx+dx*s+6*s,cy+14*s],[cx+dx*s+14*s,cy+42*s]],np.int32)
        cv2.polylines(fr,[pts],False,col,int(9*s),cv2.LINE_AA)
def icon_rosette(fr,cx,cy,s,col):
    for dx,dy,r in ((0,0,30),(-34,-28,17),(34,-24,18),(-30,32,16),(32,30,19)):
        cv2.ellipse(fr,(int(cx+dx*s),int(cy+dy*s)),(int(r*s),int(r*0.85*s)),20,0,360,col,int(6*s),cv2.LINE_AA)
def badge(fr,cx,cy,t,t0,label,icon,col=GOLD,s=1.0):
    if t<t0: return
    p=seg(t,t0,t0+0.3); sc=lerp(0.2,1.0,eob(p,2.0))*s; a=min(1,p*3)
    ov=fr.copy(); r=int(96*sc)
    cv2.circle(ov,(int(cx),int(cy)),r,(10,22,30),-1,cv2.LINE_AA); cv2.circle(ov,(int(cx),int(cy)),r,col,int(6*sc),cv2.LINE_AA)
    icon(ov,cx,cy,sc*1.05,col); fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
    q=(t-t0)/0.8
    if 0<q<1: ring(fr,cx,cy,r+q*150,col,(1-q)*0.8,5)
    paste(fr,sprite(label,bcs(52),WHITE,sw=5,glow=(0,0,0),glow_r=6),cx,cy+r+46,min(1,(t-t0)/0.25)*a,1.0)
# ---------------- scenes
def S_eye(t):
    p=t/0.55; fr=pwin("454eb397",0.592,0.470,lerp(0.18,0.13,p),W,H,0.95).copy(); fade(fr,1-ease(seg(t,0.0,0.18))); return fr
def S_tiger_hero(t):
    p=seg(t,0.5,2.3)
    fr=para("a4bcbe52",0.5,0.36,lerp(0.98,0.92,p),lerp(0.94,0.70,eo3(p)),W,H,0,0.0,blur=10,dim=1.04)
    gradv(fr,0,700,0.55,0.0); gradv(fr,1300,H,0.0,0.55)
    # light rays
    ov=np.zeros((H,W,3),np.float32)
    for i in range(5): x0=200+i*190+math.sin(t*0.8+i)*30; cv2.line(ov,(int(x0),0),(int(x0-380),H),(255,220,150),60,cv2.LINE_AA)
    ov=cv2.GaussianBlur(ov,(0,0),40); add(fr,ov,0.10)
    motes(fr,t,0.9); 
    kt(fr,"INDIA",anton(250),GOLD,W/2,330,t,0.55,hold_end=2.28,glow=(255,150,30),sw=9)
    kt(fr,"HAS TIGERS",anton(150),WHITE,W/2,510,t,1.15,hold_end=2.28,glow=(255,150,30),sw=8)
    return fr
K_HOOK=[(2.3,80.2,12.6,60,0.0,0.0),(3.3,79.8,10.6,120,0.10,-1.5),(4.6,79.65,9.1,330,0.12,1.5)]
def S_hook(t):
    def deco(img,pr):
        a=ease(seg(t,3.5,4.4)); p0=pr(79.42,9.18); p1=pr(79.72,9.09)
        if a>0:
            for i in range(16):
                f0=i/16; f1=(i+0.55)/16
                if f1<=a+0.001: cv2.line(img,(int(lerp(p0[0],p1[0],f0)),int(lerp(p0[1],p1[1],f0))),(int(lerp(p0[0],p1[0],f1)),int(lerp(p0[1],p1[1],f1))),(255,236,150),max(3,int(k_now*0.03)),cv2.LINE_AA)
            ring(img,p0[0],p0[1],24+8*math.sin(t*8),GOLD,a,4); ring(img,p1[0],p1[1],24+8*math.sin(t*8+1),GOLD,a,4)
    k_now=camk(t,K_HOOK)[2]
    fr,proj=mapframe(t,K_HOOK,0,deco)
    pi=proj(78.0,12.0)
    pill(fr,"INDIA",W/2-210,400,ease(seg(t,2.45,2.75)),size=58,s=lerp(1.5,1.0,eob(seg(t,2.45,2.75))))
    if t>3.6:
        pm=proj(79.57,9.13); kt(fr,"UNDER 50 KM",anton(110),WHITE,W/2,1000,t,3.7,hold_end=4.58,glow=(255,200,40),sw=7)
    coords_hud(fr,t,K_HOOK,ease(seg(t,2.4,2.8))); vscan(fr,t); hud_corners(fr,50,260,W-50,H-420,CYAN,0.8)
    gradv(fr,0,300,0.5,0.0); return fr
K_LK=[(4.6,80.7,7.9,215,0.0,0.0),(6.0,80.7,7.9,240,0.10,1.5)]
def S_none(t):
    def deco(img,pr):
        for (lo,la) in [(80.7,7.8)]:
            x,y=pr(lo,la)
            for i in range(3):
                q=((t-4.65)*0.9+i/3)%1; ring(img,x,y,40+q*420,RED,(1-q)*0.7,6)
    fr,proj=mapframe(t,K_LK,0,deco)
    # red tint on island region via overall slight red vignette
    gradv(fr,H-700,H,0.0,0.45,(40,0,0))
    kt(fr,"SRI LANKA",anton(130),WHITE,W/2,420,t,4.65,hold_end=5.95,glow=(0,200,220),sw=7)
    n=int(min(1,seg(t,5.15,5.6))*9); 
    kt(fr,"WILD TIGERS:",bcs(78),CREAM,W/2-200,760,t,5.15,hold_end=5.95,sw=5)
    kt(fr,"0",anton(300),RED,W/2+210,760,t,5.4,hold_end=5.95,glow=(255,40,30),sw=9)
    vscan(fr,t,0.10); hud_corners(fr,50,260,W-50,H-420,RED,0.9); return fr
def S_why(t):
    fr,proj=mapframe(t,[(6.0,80.7,7.9,240,0.10,1.5),(7.35,80.7,7.9,260,0.12,-1.0)],0)
    fr=(fr*lerp(0.9,0.35,ease(seg(t,6.0,6.2)))).astype(np.uint8)
    kt(fr,"WHY?",anton(520),GOLD,W/2,820,t,6.02,dur=0.2,glow=(255,150,0),sw=14,glitch=True)
    flare(fr,820,0.9*seg(t,6.9,7.3)); return fr
K_SP=[(7.35,80.7,7.9,200,0.10,-1.0),(12.1,80.7,7.7,235,0.12,1.5)]
SPECIES=[("SLOTH BEARS",(80.05,8.42),7.45,icon_claw,(250,640)),("ELEPHANTS",(80.90,6.43),8.75,icon_foot,(250,1060)),("LEOPARDS",(81.40,6.37),9.95,icon_rosette,(830,1060))]
def S_species(t):
    fr,proj=mapframe(t,K_SP,0)
    kt(fr,"SRI LANKA HAS",bcs(70),CREAM,W/2,330,t,7.4,hold_end=12.0,sw=5,glow=(0,0,0))
    for (lab,(lo,la),t0,ic,(bx,by)) in SPECIES:
        x,y=proj(lo,la)
        if t>=t0:
            cv2.circle(fr,(int(x),int(y)),11,(255,236,160),-1,cv2.LINE_AA); cv2.line(fr,(int(x),int(y)),(int(bx),int(by)),(255,236,160),3,cv2.LINE_AA)
            badge(fr,bx,by,t,t0,lab,ic,GOLD,1.0)
    if t>=10.95:
        cx,cy=proj(80.7,7.55)
        for i in range(24):
            if i%2==0:
                a0=i*math.pi/12+t*0.8; a1=a0+math.pi/12; pts=np.array([(int(cx+150*math.cos(a)),int(cy+150*math.sin(a))) for a in np.linspace(a0,a1,6)])
                cv2.polylines(fr,[pts],False,RED,6,cv2.LINE_AA)
        kt(fr,"TIGER?",anton(190),WHITE,W/2,1380,t,10.95,hold_end=12.05,glow=(255,40,30),sw=9,rot=-3)
    vscan(fr,t,0.08); hud_corners(fr,50,260,W-50,H-420,CYAN,0.7); return fr
def ripples(fr,cx,cy,t,t0,n=4,col=(220,245,255),maxr=520,dur=1.4,w=3):
    for i in range(n):
        q=(t-t0-i*0.28)/dur
        if 0<q<1: ring(fr,cx,cy,30+maxr*eo3(q),col,(1-q)*0.7,w)
def S_water1(t):
    p=seg(t,12.83,15.9)
    fr=para("260a7220",0.37,0.46,lerp(0.62,0.52,p),lerp(0.52,0.40,eo3(p)),W,H,0,0,blur=7,dim=1.02)
    gradv(fr,0,520,0.55,0.0); gradv(fr,1250,H,0.0,0.5)
    ripples(fr,W*0.42,1230,t,12.9,5,maxr=700); motes(fr,t,0.6,(200,235,255))
    if t<14.2:
        kt(fr,"STOPPED BY",anton(110),WHITE,W/2,330,t,12.88,hold_end=14.15,sw=7,glow=(0,160,200)); kt(fr,"THE SEA?",anton(190),CYAN,W/2,500,t,13.25,hold_end=14.15,sw=8,glow=(0,160,200))
    else:
        kt(fr,"TIGERS",anton(190),WHITE,W/2,330,t,14.22,hold_end=15.85,sw=8,glow=(0,160,200)); kt(fr,"SWIM.",anton(230),GOLD,W/2,520,t,14.6,hold_end=15.85,sw=8,glow=(255,150,0))
        for i in range(10):
            q=((t-14.22)*1.4+i*0.13)%1; x=W*0.42+math.sin(i*2.1)*260*q; y=1030-q*340*(0.6+0.4*math.cos(i)); cv2.circle(fr,(int(x),int(y)),int(3+5*(1-q)),(235,250,255),-1,cv2.LINE_AA)
    return fr
K_ST=[(15.9,79.6,9.05,420,0.10,-1.5),(18.25,79.58,9.1,640,0.16,1.5)]
def S_strait(t):
    def deco(img,pr):
        x,y=pr(79.55,9.15)
        for i in range(4):
            q=((t-16.2)*0.8+i*0.25)
            if q>0: q=q%1; ring(img,x,y,50+q*600,(255,255,255),(1-q)*0.6,6)
    fr,proj=mapframe(t,K_ST,0,deco)
    v=int(35*eo3(seg(t,16.3,17.5)))
    kt(fr,"PALK STRAIT",bcs(86),CREAM,W/2,330,t,15.95,hold_end=18.2,sw=6,glow=(0,160,200))
    kt(fr,"UNDER",anton(120),WHITE,W/2,620,t,16.4,hold_end=18.2,sw=7,glow=(0,160,200)); 
    paste(fr,sprite(f"{v} M",anton(260),GOLD,sw=10,glow=(255,150,0)),W/2,860,min(1,seg(t,16.4,16.7)))
    kt(fr,"DEEP",anton(120),WHITE,W/2,1060,t,17.0,hold_end=18.2,sw=7,glow=(0,160,200))
    vscan(fr,t,0.12); hud_corners(fr,50,260,W-50,H-420,CYAN,0.9); coords_hud(fr,t,K_ST); return fr
K_DR=[(18.75,79.9,8.7,170,0.10,-1.0),(23.9,79.9,8.7,200,0.14,1.5),(26.2,79.8,8.6,215,0.10,-1.0)]
def S_drain(t):
    level=-120*ease(seg(t,19.0,23.9))
    def deco(img,pr):
        if level<-30:
            a=ease(seg(t,21.2,22.0)); p0=pr(79.42,9.18); p1=pr(79.72,9.09)
            for i in range(18):
                f=(i/18+t*0.5)%1; x=lerp(p0[0],p1[0],f); y=lerp(p0[1],p1[1],f); cv2.circle(img,(int(x),int(y)),int(7*a),(255,240,170),-1,cv2.LINE_AA)
            cv2.line(img,(int(p0[0]),int(p0[1])),(int(p1[0]),int(p1[1])),(255,226,120),max(2,int(8*a)),cv2.LINE_AA)
    fr,proj=mapframe(t,K_DR,level,deco)
    # level HUD
    paste(fr,sprite("SEA LEVEL",bcs(44),CREAM,sw=3),160,330,ease(seg(t,18.8,19.2)))
    paste(fr,sprite(f"{int(round(level))} M" if level<-0.5 else "0 M",anton(190),GOLD,sw=8,glow=(255,150,0)),250,470,ease(seg(t,18.8,19.2)))
    # gauge
    gx=W-90; ov=fr.copy(); cv2.rectangle(ov,(gx-16,330),(gx+16,1130),(10,22,30),-1); cv2.rectangle(ov,(gx-16,330),(gx+16,1130),CYAN,3)
    fy=int(330+800*(abs(level)/120)); cv2.rectangle(ov,(gx-12,fy-4),(gx+12,fy+4),WHITE,-1); fr[:]=(fr*0.0+ov).astype(np.uint8) if False else (fr*0.4+ov*0.6).astype(np.uint8)
    if t>=21.2: kt(fr,"LAND BRIDGE",anton(130),GOLD,W/2,1010,t,21.25,hold_end=23.2,sw=8,glow=(255,150,0))
    if t>=18.8: kt(fr,"LAST ICE AGE",bcs(64),CREAM,W/2,260,t,18.8,hold_end=21.0,sw=5)
    # timeline
    a=ease(seg(t,23.3,23.8))
    if a>0:
        paste(fr,sprite("THE LAST 500,000 YEARS",bcs(60),CREAM,sw=4),W/2,1100,a)
        ov=fr.copy(); cv2.rectangle(ov,(90,1170),(W-90,1230),(14,24,30),-1); cv2.rectangle(ov,(90,1170),(W-90,1230),CYAN,3)
        wf=int((W-180)*0.58*ease(seg(t,23.8,25.2))); 
        if wf>3: cv2.rectangle(ov,(90,1170),(90+wf,1230),GOLD,-1)
        fr[:]=(fr*(1-a)+ov*a).astype(np.uint8)
        kt(fr,"MORE THAN HALF",anton(100),WHITE,W/2,1330,t,24.9,hold_end=26.1,sw=7,glow=(255,150,0))
    vscan(fr,t,0.10); hud_corners(fr,50,260,W-50,H-420,CYAN,0.8)
    flare(fr,1010,0.8*ease(seg(t,26.0,26.12))*0+0); return fr
def S_eyes(t):
    p=seg(t,27.0,30.65); strip=pwin("a4bcbe52",0.5,0.372,lerp(0.46,0.36,p),W,760,1.0)
    bg=cv2.resize(cv2.GaussianBlur(strip,(0,0),18),(W,H)); fr=(bg*0.45).astype(np.uint8)
    m=np.ones((760,1),np.float32); 
    for i in range(60): m[i]=i/60; m[759-i]=min(m[759-i],i/60)
    y0=620; reg=fr[y0:y0+760].astype(np.float32); fr[y0:y0+760]=(reg*(1-m[:,:,None])+strip.astype(np.float32)*m[:,:,None]).astype(np.uint8)
    flare(fr,y0+380,0.5*math.sin(p*math.pi)); motes(fr,t,0.6)
    kt(fr,"COULD HAVE",anton(150),WHITE,W/2,370,t,27.2,hold_end=30.6,sw=8,glow=(0,0,0)); kt(fr,"WALKED ACROSS.",anton(130),GOLD,W/2,520,t,28.2,hold_end=30.6,sw=8,glow=(255,150,0))
    hud_corners(fr,60,y0-10,W-60,y0+770,GOLD,0.9,50,4)
    return fr
def S_black(t):
    fr=np.zeros((H,W,3),np.uint8); 
    q=seg(t,30.8,31.9); 
    cv2.line(fr,(int(W/2-W*0.4*q),H//2),(int(W/2+W*0.4*q),H//2),GOLD,4,cv2.LINE_AA)
    ov=np.zeros((H,W,3),np.float32); cv2.line(ov,(int(W/2-W*0.4*q),H//2),(int(W/2+W*0.4*q),H//2),(255,200,80),6); add(fr,cv2.GaussianBlur(ov,(0,0),18),1.4)
    motes(fr,t,0.5); return fr
K_FO=[(32.1,80.7,7.9,210,0.10,-1.5),(35.6,80.45,7.0,420,0.16,1.5),(41.5,80.45,6.95,520,0.12,-1.0),(44.8,80.45,6.95,560,0.10,0)]
def S_fossil(t):
    def deco(img,pr):
        for (lo,la,ph) in ((80.40,6.78,1),(80.42,6.68,2)):
            x,y=pr(lo,la)
            if t>=32.5+(ph-1)*4.2:
                q=((t-32.5)*0.9)%1; ring(img,x,y,16+q*140,GOLD,(1-q)*0.9,5); cv2.circle(img,(int(x),int(y)),11,(255,246,190),-1,cv2.LINE_AA)
    fr,proj=mapframe(t,K_FO,0,deco)
    def card(x,y,w,title,sub,t0,hold,num=None):
        if t<t0 or t>hold+0.15: return
        p=seg(t,t0,t0+0.3); a=min(1,p*3)*(1-seg(t,hold,hold+0.15)); xx=x-(1-eo3(p))*220
        ov=fr.copy(); cv2.rectangle(ov,(int(xx),y),(int(xx+w),y+330),(8,18,26),-1); cv2.rectangle(ov,(int(xx),y),(int(xx+w),y+330),GOLD,4); cv2.rectangle(ov,(int(xx),y),(int(xx+10),y+330),GOLD,-1)
        fr[:]=(fr*(1-a*0.88)+ov*a*0.88).astype(np.uint8)
        paste(fr,sprite(title,anton(96),WHITE,sw=5),xx+w/2+10,y+80,a); 
        if num is not None: paste(fr,sprite(num,anton(110),GOLD,sw=6,glow=(255,150,0)),xx+w/2+10,y+190,a)
        paste(fr,sprite(sub,bcs(46),(180,245,240),sw=3,shadow=False),xx+w/2+10,y+275,a)
    yrs=int(16500*eo3(seg(t,33.1,34.6)))
    card(40,340,W-80,"TOE BONE","BATADOMBA CAVE, KURUWITA",32.7,36.6,f"~{yrs:,} YEARS OLD" if yrs<16500 else "~16,500 YEARS OLD")
    card(40,340,W-80,"TOOTH","NEAR RATNAPURA",36.9,41.4,"LOWER CARNASSIAL")
    if t>=41.6:
        p=seg(t,41.6,41.9); s_=lerp(2.2,1.0,eob(p,1.2)); a=min(1,p*3)
        ov=fr.copy(); cv2.rectangle(ov,(60,640),(W-60,1260),(8,16,22),-1); cv2.rectangle(ov,(60,640),(W-60,1260),RED,10); fr[:]=(fr*(1-a*0.9)+ov*a*0.9).astype(np.uint8)
        paste(fr,sprite("TENTATIVE ID",bcs(84),CREAM,sw=4),W/2,740,a,s_)
        paste(fr,sprite("TIGER?",anton(330),WHITE,sw=12,glow=(255,40,30)),W/2,960,a,s_,-3)
        paste(fr,sprite("Manamendra-Arachchi et al., 2005",bar(40),(235,235,235),sw=3,shadow=False),W/2,1190,a)
    vscan(fr,t,0.08); hud_corners(fr,50,260,W-50,H-420,CYAN,0.7); return fr
def leafwipe(t,t0):
    p=ease(seg(t,t0,t0+0.7)); r=np.random.default_rng(2); n=cv2.resize(r.normal(0,1,(24,14)).astype(np.float32),(W,H),interpolation=cv2.INTER_CUBIC)
    yy,xx=np.mgrid[0:H,0:W]; diag=(xx/W*0.55+(1-yy/H)*0.75); return np.clip((p*1.7-diag)*6+n*0.5,0,1)[:,:,None]
def S_peek(t):
    p=seg(t,44.8,48.9); ph=pwin("454eb397",0.49,0.46,lerp(0.395,0.35,p),W,H,1.0).astype(np.float32)
    base=S_fossil(44.79).astype(np.float32); m=leafwipe(t,44.8); fr=(base*(1-m)+ph*m).astype(np.uint8)
    gradv(fr,0,560,0.65,0.0); gradv(fr,1300,H,0.0,0.4)
    
    kt(fr,"HYPOTHESIS",anton(160),GOLD,W/2,380,t,45.5,hold_end=47.35,sw=8,glow=(255,150,0))
    kt(fr,"STILL DEBATED",anton(120),WHITE,W/2,380,t,47.4,hold_end=48.85,sw=8,glow=(0,0,0))
    motes(fr,t,0.5); return fr
K_RS=[(48.9,80.0,8.7,225,0.10,1.0),(54.3,80.0,8.6,260,0.12,-1.0),(58.9,80.5,7.8,290,0.08,0)]
POP=[(80.7,7.9),(80.5,7.5),(80.9,7.4),(80.3,8.2),(81.1,8.0),(80.6,7.0),(81.0,6.8),(80.2,7.6),(80.8,8.5),(81.3,7.6),(80.4,6.9),(80.95,7.9)]
def S_rise(t):
    level=-120*(1-ease(seg(t,49.4,54.3)))
    def deco(img,pr):
        for i,(lo,la) in enumerate(POP):
            keep=i<3; a0=ease(seg(t,54.3+i*0.04,54.8+i*0.04)); a1=1.0 if keep else 1-ease(seg(t,55.4+i*0.18,55.9+i*0.18)); a=a0*a1
            if a>0.02: x,y=pr(lo,la); cv2.circle(img,(int(x),int(y)),13,(255,226,120),-1,cv2.LINE_AA); ring(img,x,y,26,GOLD,a*0.6,3)
    fr,proj=mapframe(t,K_RS,level,deco)
    fade(fr,1-ease(seg(t,48.9,49.4)),(255,255,255))
    paste(fr,sprite("SEA LEVEL",bcs(44),CREAM,sw=3),160,330,1.0); paste(fr,sprite(f"{int(round(level))} M" if level<-0.5 else "0 M",anton(190),GOLD,sw=8,glow=(255,150,0)),250,470,1.0)
    if t>=52.4: kt(fr,"BRIDGE",anton(150),WHITE,W/2,1000,t,52.45,hold_end=57.0,sw=8,glow=(0,120,200)); kt(fr,"FLOODED",anton(150),CYAN,W/2,1150,t,52.7,hold_end=57.0,sw=8,glow=(0,120,200))
    if t>=54.4:
        a=ease(seg(t,54.4,54.8)); pop=1.0-0.78*ease(seg(t,55.5,57.8)); gx=W-100
        ov=fr.copy(); cv2.rectangle(ov,(gx-18,500),(gx+18,1100),(10,22,30),-1); cv2.rectangle(ov,(gx-18,500),(gx+18,1100),RED,4); cv2.rectangle(ov,(gx-14,int(1100-596*pop)),(gx+14,1096),RED,-1); fr[:]=(fr*(1-a*0.8)+ov*a*0.8).astype(np.uint8)
        paste(fr,sprite("TIGERS",bcs(46),CREAM,sw=3),gx-6,470,a)
    if t>=56.2: kt(fr,"SMALL. ISOLATED.",anton(96),WHITE,W/2,1400,t,56.25,hold_end=58.85,sw=7,glow=(255,40,30))
    vscan(fr,t,0.10); hud_corners(fr,50,260,W-50,H-420,CYAN,0.7); return fr
def S_lion(t):
    fr,proj=mapframe(t,[(58.9,80.7,7.9,205,0.08,0),(67.3,80.7,7.9,225,0.10,1)],0); fr=(fr*0.28).astype(np.uint8)
    fade(fr,1-ease(seg(t,58.9,59.3)),(255,255,255))
    fl=1-0.8*ease(seg(t,63.0,63.7))
    kt(fr,"LION",anton(380),WHITE,W/2,520,t,59.3,tex='lion',sw=10,glow=(255,170,60),sy=0) if False else None
    if t>=59.3:
        p=seg(t,59.3,59.55); sp=sprite("LION",anton(400),WHITE,sw=10,glow=(255,170,60),tex='lion'); paste(fr,sp,W/2,540,min(1,p*3)*fl,lerp(1.5,1.0,eob(p,1.4)))
        paste(fr,sprite("GONE BEFORE ~37,000 YEARS AGO",bcs(54),CREAM,sw=4),W/2,800,seg(t,59.7,60.0)*fl)
    sl=ease(seg(t,63.0,63.5))
    if sl>0: cv2.line(fr,(int(W/2-300),600),(int(W/2-300+600*sl),470),RED,12,cv2.LINE_AA)
    if t>=64.8:
        p=seg(t,64.8,65.05); sp=sprite("LEOPARD",anton(262),WHITE,sw=7,glow=(255,190,60),tex='rosette'); paste(fr,sp,W/2,1130,min(1,p*3),lerp(1.5,1.0,eob(p,1.4)))
        paste(fr,sprite("STILL THERE",bcs(70),GOLD,sw=5,glow=(255,150,0)),W/2,1330,seg(t,65.5,65.8))
        for i in range(3): q=((t-64.8)*0.9+i/3)%1; ring(fr,W/2,1130,100+q*500,GOLD,(1-q)*0.5,5)
    motes(fr,t,0.6); return fr
MONT=[("4d5819bf",0.53,0.44,0.74,0.58,"para"),("260a7220",0.37,0.47,0.62,0.46,"para"),("0a195c9b",0.60,0.52,0.60,0.44,"para"),("ce145a99",0.56,0.66,0.98,0.88,"plain"),("a4bcbe52",0.5,0.38,0.98,0.74,"para")]
def S_mont(t):
    i=min(4,int((t-67.3)/1.1)); k,cx,cy,w0,w1,mode=MONT[i]; p=((t-67.3)-i*1.1)/1.1
    if mode=="para": fr=para(k,cx,cy,min(1.0,lerp(w0+0.14,w0+0.04,p)),lerp(w0,w1,eo3(p)),W,H,0,0,blur=8,dim=1.03,rot=lerp(-1.5,1.5,p)*(1 if i%2 else -1))
    else: fr=pext(k,570,lerp(1.0,1.08,p))
    gradv(fr,0,640,0.62,0.0); gradv(fr,1400,H,0.0,0.4); motes(fr,t,0.7)
    if t<70.0:
        kt(fr,"THE SEA DIDN'T",anton(120),WHITE,W/2,330,t,67.35,hold_end=69.95,sw=7); kt(fr,"KEEP THEM OUT.",anton(120),GOLD,W/2,460,t,67.65,hold_end=69.95,sw=7,glow=(255,150,0))
    else:
        kt(fr,"THE ISLAND MAY NOT",anton(104),WHITE,W/2,320,t,70.02,sw=7); kt(fr,"HAVE KEPT THEM IN.",anton(104),GOLD,W/2,436,t,70.3,sw=7,glow=(255,150,0))
        pill(fr,"BEST-SUPPORTED EXPLANATION, NOT PROVEN",W/2,540,ease(seg(t,70.8,71.1)),size=36)
    return fr
def S_hero(t):
    p=seg(t,72.8,79.0); fr=para("a4bcbe52",0.5,lerp(0.30,0.36,p),min(1.0,lerp(0.80,1.0,eo3(p))),lerp(0.62,0.95,eo3(p)),W,H,0,0,blur=10,dim=1.04)
    gradv(fr,0,620,0.7,0.0); motes(fr,t,0.8)
    kt(fr,"THE NATURAL ANGLE",anton(100),GOLD,W/2,340,t,77.3,sw=7,glow=(255,150,0)); 
    paste(fr,sprite("Photos: Hitesh Chawla",bar(42),CREAM,sw=3),W/2,450,ease(seg(t,77.7,78.2)))
    fade(fr,ease(seg(t,79.0,80.0))); return fr
SC=[(0,0.5,S_eye),(0.5,2.3,S_tiger_hero),(2.3,4.6,S_hook),(4.6,6.0,S_none),(6.0,7.35,S_why),(7.35,12.83,S_species),(12.83,15.9,S_water1),(15.9,18.75,S_strait),(18.75,27.0,S_drain),(27.0,30.65,S_eyes),(30.65,32.1,S_black),(32.1,44.8,S_fossil),(44.8,48.9,S_peek),(48.9,58.9,S_rise),(58.9,67.3,S_lion),(67.3,72.8,S_mont),(72.8,80.01,S_hero)]
HITS=[(0.53,1.2),(1.15,0.8),(2.3,1.0),(3.7,0.9),(4.65,0.9),(5.4,1.0),(6.02,1.4),(7.45,0.6),(8.75,0.6),(9.95,0.6),(10.95,0.9),(12.88,0.8),(14.22,0.9),(15.95,0.7),(18.75,0.9),(21.25,0.9),(24.9,0.9),(27.1,0.7),(30.65,1.5),(32.1,0.7),(36.9,0.6),(41.6,1.5),(44.8,0.9),(45.5,0.8),(47.4,0.8),(48.9,1.2),(52.45,0.9),(54.4,0.6),(56.25,0.8),(59.3,1.0),(63.0,0.8),(64.8,1.2),(67.3,1.5),(68.4,0.7),(69.5,0.7),(70.02,0.9),(77.3,0.7)]
def frame(t):
    for (a,b,fn) in SC:
        if a<=t<b: break
    fr=fn(t)
    # transitions: whip between SC boundaries flagged
    for tb,kind,dur in TR:
        if tb<=t<tb+dur:
            q=(t-tb)/dur
            if kind=="whip":
                pb=[s for s in SC if s[1]<=tb+1e-6][-1][2] if False else None
                prev=None
                for (a,b,fn2) in SC:
                    if abs(b-tb)<1e-6: prev=fn2(min(tb-1/FPS,t))
                if prev is not None:
                    sh=int(W*eo3(q)); ker=np.zeros((1,81),np.float32); ker[0,:]=1/81
                    p1=np.roll(prev,-sh,1); n1=np.roll(fr,W-sh,1); m=np.clip((q-0.35)/0.3,0,1)
                    mix=(p1*(1-m)+n1*m).astype(np.uint8); fr=cv2.filter2D(mix,-1,ker) if 0.05<q<0.95 else mix
            elif kind=="flash":
                fr=np.clip(fr.astype(np.float32)+255*(1-q)**2*0.9,0,255).astype(np.uint8)
    fr=punch(fr,t,HITS)
    return look(fr,t,HITS)
TR=[(2.3,"whip",0.22),(12.83,"flash",0.2),(18.75,"flash",0.2),(32.1,"flash",0.15),(44.8,"flash",0.12),(67.3,"flash",0.2)]
if __name__=="__main__":
    ts=[float(x) for x in sys.argv[1:]]
    for t in ts: cv2.imwrite(f"{HERE}t_{t:05.1f}.jpg",cv2.cvtColor(frame(t),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,88])
