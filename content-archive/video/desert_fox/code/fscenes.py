import sys, json, math, os
SPD="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/"
sys.path.insert(0,SPD+"dhreel"); sys.path.insert(0,SPD+"island")
from dcore_r import *
import core as IC
W,H=1080,1920
AMB=(255,170,60); SAND=(240,200,140); TERRA=(214,106,58); NIGHT=(14,18,44); COOL=(120,190,220); LEAF=(110,170,90)
# ---------- timeline
ENT=[("S1",9),("S2",12),("S3a",6),("S3b",6),("S4a",4.0),("S4b",9.0),("S5",12),("S6a",7),("S6b",6),("S7",12),("S8",15)]
DES={}; _c=0
for n,l in ENT: DES[n]=(_c,l); _c+=l
DTOT=_c
START={n:DES[n][0] for n,_ in ENT}; START["end"]=DTOT
if os.path.exists(SPD+"fox/marks.json"): START.update(json.load(open(SPD+"fox/marks.json")))
TOTAL=START["end"]
ORDER=[n for n,_ in ENT]+["end"]
def FAC(n):  # design seconds per real second
    i=ORDER.index(n); return DES[n][1]/(START[ORDER[i+1]]-START[n])
# ---------- images
FW={}; PYR={}
def load(name):
    if name not in FW:
        im=Image.open(SPD+f"fox/img/{name}.png").convert("RGB"); FW[name]=im.size
        a=np.array(im); lv={}
        for L_ in (3000,1800,1100):
            s=L_/max(a.shape[:2])
            if s<1: lv[L_]=cv2.resize(a,(int(a.shape[1]*s),int(a.shape[0]*s)),interpolation=cv2.INTER_AREA)
        lv[max(a.shape[:2])]=a if max(a.shape[:2])<=3000 else lv[3000]
        PYR[name]=sorted(((v.shape[1]/FW[name][0],v) for v in lv.values()),key=lambda p:p[0])
    return PYR[name]
def view(name,box,size,z=1.0,pan=(0,0)):
    pyr=load(name); w,h=size; FWi,FHi=FW[name]; x0,y0,x1,y1=box
    cx,cy=(x0+x1)/2+pan[0],(y0+y1)/2+pan[1]; bw,bh=(x1-x0)/z,(y1-y0)/z
    disp=w/(bw*FWi); arr=pyr[-1][1]
    for r,a in pyr:
        if r>=disp: arr=a; break
    Hh,Ww=arr.shape[:2]; sx=w/(bw*Ww); sy=h/(bh*Hh)
    M=np.array([[sx,0,-(cx-bw/2)*Ww*sx],[0,sy,-(cy-bh/2)*Hh*sy]],np.float32)
    return cv2.warpAffine(arr,M,(w,h),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
def fbox(name,cx,bw,cy=0.5):
    load(name); FWi,FHi=FW[name]; bh=bw*FWi*H/(W*FHi)
    if bh>1: bh=1; bw=bh*W*FHi/(H*FWi)
    cx=min(max(cx,bw/2),1-bw/2); cy=min(max(cy,bh/2),1-bh/2); return (cx-bw/2,cy-bh/2,cx+bw/2,cy+bh/2)
def fb(name,cx,bw,z=1.0,pan=(0,0),cy=0.5): return view(name,fbox(name,cx,bw,cy),(W,H),z,pan)
def arr2img(a): return Image.fromarray(np.clip(a,0,255).astype(np.uint8)).convert("RGBA")
def fwin(img,name,box,rect,z=1.0,pan=(0,0),spot=None,k=0.0,border=AMB,rad=28,flash=0.0,desat=0.0,warm=None,shim=0.0,t=0.0):
    wx,wy,ww,wh=rect; a=view(name,box,(ww,wh),z,pan)
    if shim>0: a=shimmer(a,t,shim)
    if desat>0: g=a.mean(2,keepdims=True); a=a*(1-desat)+g*desat
    if warm is not None: a=a*np.array(warm,np.float32)
    if spot is not None and k>0:
        sx_,sy_,rx_,ry_=spot; bx0,by0,bx1,by1=box; bw_,bh_=(bx1-bx0)/z,(by1-by0)/z; cx_,cy_=(bx0+bx1)/2+pan[0],(by0+by1)/2+pan[1]
        px=((sx_-(cx_-bw_/2))/bw_)*ww; py=((sy_-(cy_-bh_/2))/bh_)*wh; a=grade_spot(a,px,py,rx_/bw_*ww,ry_/bh_*wh,k)
    if flash>0: a=np.clip(a+flash*200,0,255)
    mk=Image.new("L",(ww,wh),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,ww-1,wh-1),radius=rad,fill=255)
    sh=Image.new("RGBA",(ww,wh),(0,0,0,0)); sh.putalpha(mk.point(lambda v:v*150//255)); img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)),(wx+8,wy+14))
    p=arr2img(a); p.putalpha(mk); img.alpha_composite(p,(wx,wy))
    ImageDraw.Draw(img,"RGBA").rounded_rectangle((wx-2,wy-2,wx+ww+1,wy+wh+1),radius=rad,outline=border+(200,),width=3)
def shimmer(a,t,amp):
    h,w=a.shape[:2]; yy,xx=np.mgrid[0:h,0:w].astype(np.float32)
    dx=amp*np.sin(yy*0.045+t*5.0)*np.sin(yy*0.013-t*2.0); return cv2.remap(a,xx+dx,yy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
# ---------- backgrounds
_G={}
def grad(c0,c1,key):
    if key not in _G:
        y=np.linspace(0,1,H,dtype=np.float32)[:,None,None]; _G[key]=np.broadcast_to(np.array(c0,np.float32)*(1-y)+np.array(c1,np.float32)*y,(H,W,3)).copy()
    return _G[key]
_ST=np.random.default_rng(9); STARS=[(_ST.uniform(0,W),_ST.uniform(60,1500),_ST.uniform(1,3),_ST.uniform(0,6.28)) for _ in range(120)]
def night_bg(t,c0=(8,10,30),c1=(30,28,60)):
    a=grad(c0,c1,("n",c0,c1)).copy(); img=arr2img(a); d=ImageDraw.Draw(img,"RGBA")
    for x,y,r,ph in STARS:
        al=int(120+110*math.sin(t*1.5+ph)); d.ellipse((x-r,y-r,x+r,y+r),fill=(255,244,220,max(0,min(255,al))))
    return img
def hot_bg(t):
    a=grad((255,232,176),(238,140,64),"hot").copy(); yy,xx=np.mgrid[0:H,0:W]
    g=np.exp(-(((xx-820)/380)**2+((yy-300)/380)**2))[...,None]; a=a+g*np.array((60,40,0),np.float32)
    return arr2img(a)
def scrim(img,y0,y1,a0,a1,col=(8,8,20)):
    l=Image.new("RGBA",(W,H),(0,0,0,0)); a=np.zeros((H,W),np.uint8); ramp=np.linspace(a0,a1,y1-y0); a[y0:y1]=(ramp[:,None]*255).astype(np.uint8)
    if y1<H and a1>0: a[y1:]=int(a1*255)
    l=Image.new("RGBA",(W,H),col+(0,)); l.putalpha(Image.fromarray(a)); img.alpha_composite(l)
def brand(img,col=CREAM,a=150):
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,78),"THE NATURAL ANGLE",B(30),col,a)
def tchip(img,s,a=1.0,y=150,col=AMB,dark=True):
    if a<=0.01: return
    d=ImageDraw.Draw(img,"RGBA"); f=B(40); w=f.getlength(s)+64
    d.rounded_rectangle((W/2-w/2,y-34,W/2+w/2,y+34),radius=34,fill=((12,14,30,int(215*a)) if dark else (255,255,255,int(200*a))),outline=col+(int(255*a),),width=3)
    txt(d,(W/2,y+13),s,f,col,255*a)
def tlay(xy,s,f,col,anchor="ms"):
    l=L(); txt(ImageDraw.Draw(l,"RGBA"),xy,s,f,col,255,anchor); return l
def pill(img,xy,s,f,a,fg=INK,bg=AMB,sc=1.0,outline=None,pad=(30,14)):
    if a<=0.01: return
    l=L(); d=ImageDraw.Draw(l,"RGBA"); x,y=xy; w=f.getlength(s)+2*pad[0]; h=f.size*1.0+2*pad[1]
    d.rounded_rectangle((x-w/2,y-h/2,x+w/2,y+h/2),radius=h/2,fill=bg+(245,),outline=(outline+(255,)) if outline else None,width=3); txt(d,(x,y+f.size*0.34),s,f,fg)
    comp(img,l,a,sc=sc)
def fox_icon(d,x,y,s,col,a=255):
    d.ellipse((x-s,y-s*0.7,x+s,y+s*0.9),fill=col+(a,)); d.polygon([(x-s*0.9,y-s*0.4),(x-s*0.55,y-s*1.5),(x-s*0.1,y-s*0.6)],fill=col+(a,)); d.polygon([(x+s*0.9,y-s*0.4),(x+s*0.55,y-s*1.5),(x+s*0.1,y-s*0.6)],fill=col+(a,))
    d.ellipse((x-s*0.45,y-s*0.1,x-s*0.2,y+s*0.15),fill=(20,16,12,a)); d.ellipse((x+s*0.2,y-s*0.1,x+s*0.45,y+s*0.15),fill=(20,16,12,a)); d.ellipse((x-s*0.14,y+s*0.38,x+s*0.14,y+s*0.62),fill=(20,16,12,a))
# ---------- icons for the menu
def ic_insect(d,x,y,s,c,a):
    d.ellipse((x-s*0.35,y-s*0.5,x+s*0.35,y+s*0.6),fill=c+(a,))
    for i in (-1,0,1):
        d.line((x-s*0.3,y+i*s*0.25,x-s*0.85,y+i*s*0.45),fill=c+(a,),width=4); d.line((x+s*0.3,y+i*s*0.25,x+s*0.85,y+i*s*0.45),fill=c+(a,),width=4)
    d.line((x-s*0.15,y-s*0.5,x-s*0.4,y-s*0.9),fill=c+(a,),width=3); d.line((x+s*0.15,y-s*0.5,x+s*0.4,y-s*0.9),fill=c+(a,),width=3)
def ic_fruit(d,x,y,s,c,a):
    d.ellipse((x-s*0.6,y-s*0.5,x+s*0.6,y+s*0.7),fill=c+(a,)); d.line((x,y-s*0.5,x+s*0.1,y-s*0.9),fill=(120,200,100,a),width=5); d.ellipse((x+s*0.1,y-s*0.95,x+s*0.6,y-s*0.65),fill=(120,200,100,a))
def ic_mammal(d,x,y,s,c,a):
    d.ellipse((x-s*0.7,y-s*0.35,x+s*0.5,y+s*0.45),fill=c+(a,)); d.ellipse((x+s*0.2,y-s*0.55,x+s*0.75,y+s*0.05),fill=c+(a,)); d.ellipse((x+s*0.25,y-s*0.8,x+s*0.5,y-s*0.5),fill=c+(a,))
    d.line((x-s*0.7,y+s*0.1,x-s*1.1,y-s*0.3),fill=c+(a,),width=4)
def ic_reptile(d,x,y,s,c,a):
    pts=[(x-s*1.0,y+s*0.3),(x-s*0.5,y-s*0.1),(x,y+s*0.2),(x+s*0.5,y-s*0.1),(x+s*0.95,y+s*0.1)]; d.line(pts,fill=c+(a,),width=int(s*0.38),joint="curve"); d.ellipse((x+s*0.8,y-s*0.1,x+s*1.2,y+s*0.3),fill=c+(a,))
    for px,py in ((x-s*0.4,y),(x+s*0.4,y)): d.line((px,py,px-s*0.1,py+s*0.5),fill=c+(a,),width=4)
def ic_bird(d,x,y,s,c,a):
    d.ellipse((x-s*0.6,y-s*0.3,x+s*0.5,y+s*0.4),fill=c+(a,)); d.ellipse((x+s*0.3,y-s*0.55,x+s*0.7,y-s*0.15),fill=c+(a,)); d.polygon([(x+s*0.65,y-s*0.4),(x+s*1.0,y-s*0.3),(x+s*0.65,y-s*0.25)],fill=c+(a,)); d.polygon([(x-s*0.2,y-s*0.2),(x-s*0.6,y-s*0.9),(x+s*0.1,y-s*0.3)],fill=c+(a,))
# ================== SCENES (lt = design seconds)
def S1(lt,t):
    img=hot_bg(t); brand(img,INK,170); d=ImageDraw.Draw(img,"RGBA")
    # sun disk
    d.ellipse((820-120,300-120,820+120,300+120),fill=(255,250,230,230))
    # counter
    q=ease(seg(lt,0.2,2.6)); v=int(30+20*q)
    l=glayer((W/2,420),f"{v}°C",A(230),top=(120,34,10),bot=(70,18,8)); comp(img,l,eo3(seg(lt,0.1,0.5)))
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,500),"THAR DESERT  ·  MAY AND JUNE",B(44),INK,255*eo3(seg(lt,0.6,1.1)))
    # photo
    a=eo3(seg(lt,0.9,1.6)); 
    if a>0:
        tmp=Image.new("RGBA",(W,H),(0,0,0,0)); fwin(tmp,"f1",(0.02,0.18,0.98,0.95),(60,600,960,560),z=1.0+0.05*seg(lt,0,9),desat=0.55,warm=(1.18,1.08,0.92),shim=7+4*seg(lt,0,4),t=t,border=(120,34,10))
        comp(img,tmp,a)
    l1=glayer((W/2,1330),"WHERE DOES A FOX",A(100),top=(255,250,240),bot=(255,214,160)); l2=glayer((W/2,1440),"HIDE FROM THIS?",A(100),top=(255,250,240),bot=(255,214,160))
    for l,t0 in ((l1,4.4),(l2,4.9)):
        aa=eo3(seg(lt,t0,t0+0.5)); comp(img,glow(l,(110,30,10),22,0.9),aa*0.7); comp(img,l,aa,dy=(1-aa)*30)
    pa=eo3(seg(lt,6.6,7.1)); pill(img,(W/2,1565),"THE ANSWER IS UNDER YOUR FEET",B(46),pa,fg=CREAM,bg=(110,30,10),sc=lerp(0.8,1,eob(seg(lt,6.6,7.2))))
    if lt>7.2:
        d=ImageDraw.Draw(img,"RGBA"); by=1655+10*math.sin((lt-7.2)*6); d.polygon([(W/2-34,by-14),(W/2+34,by-14),(W/2,by+30)],fill=(110,30,10,255))
    return img
TUN=[(540,880),(540,1000),(520,1090),(600,1170),(560,1260),(500,1320),(540,1380)]
def S2(lt,t):
    img=Image.new("RGBA",(W,H),(0,0,0,0)); top=grad((255,226,170),(240,150,70),"hot2").copy(); a=top.copy()
    gnd=grad((70,48,34),(22,16,22),"gnd"); a[860:]=gnd[860:]; img=arr2img(a); brand(img,CREAM,150)
    d=ImageDraw.Draw(img,"RGBA"); tchip(img,"12:30 PM  ·  ABOUT 50°C",eo3(seg(lt,0.1,0.5)),y=150,col=(255,170,60))
    fwin(img,"f9",(0.30,0.22,0.98,0.78),(110,215,860,640),z=1.0+0.04*seg(lt,0,12),desat=0.25,warm=(1.12,1.05,0.95),shim=5,t=t,border=(120,34,10))
    d=ImageDraw.Draw(img,"RGBA"); d.rectangle((0,846,W,862),fill=(150,100,60,255)); d.rectangle((0,846,W,850),fill=(210,160,100,255))
    # tunnels
    pr=ease(seg(lt,1.0,5.5)); segs=[]
    main=TUN; side1=[(520,1090),(380,1110),(260,1070),(190,900),(180,866)]; side2=[(600,1170),(760,1190),(860,1120),(900,940),(890,866)]; side3=[(500,1320),(380,1380),(300,1350)]
    for pts,t0,t1 in ((main,1.0,3.5),(side1,3.2,4.6),(side2,3.6,5.0),(side3,4.4,5.5)):
        p=ease(seg(lt,t0,t1))
        if p<=0: continue
        n=len(pts)-1; f=p*n; i=min(int(f),n-1); u=f-i
        for j in range(i): d.line(pts[j:j+2],fill=SAND+(235,),width=22); d.line(pts[j:j+2],fill=(30,22,26,255),width=14)
        x=lerp(pts[i][0],pts[i+1][0],u); y=lerp(pts[i][1],pts[i+1][1],u); d.line((pts[i],(x,y)),fill=SAND+(235,),width=22); d.line((pts[i],(x,y)),fill=(30,22,26,255),width=14)
    for (ex,ey,tx) in ((540,866,"ENTRANCE"),(180,866,"EXIT"),(890,866,"EXIT")):
        ea=eo3(seg(lt,4.8,5.3)) if ex!=540 else eo3(seg(lt,1.0,1.4)); d.ellipse((ex-18,ey-8,ex+18,ey+16),fill=(20,14,18,int(255*ea)))
    # chamber
    ca=eo3(seg(lt,3.3,3.8)); d.ellipse((540-70,1380-44,540+70,1380+44),fill=(30,22,26,int(255*ca)),outline=SAND+(int(235*ca),),width=6)
    # fox walks in
    fp=ease(seg(lt,1.4,3.6)); n=len(main)-1; f=fp*n; i=min(int(f),n-1); u=f-i; fx=lerp(main[i][0],main[i+1][0],u); fy=lerp(main[i][1],main[i+1][1],u)
    if fp>0: fox_icon(d,fx,fy,17,AMB,int(255*min(1,fp*5)))
    if lt>3.8:
        zz=(lt-3.8); 
        for k in range(3): 
            aa=eo3(seg(zz,k*0.5,k*0.5+0.4))*(1-0.5*((zz-k*0.5)%2.0)/2.0); txt(d,(600+k*28,1330-k*34),"z",A(36+k*8),COOL,255*aa)
    # chips
    rows=[(6.0,"MANY TUNNELS. MANY EXITS."),(7.6,"OLD PORCUPINE + HEDGEHOG BURROWS"),(9.2,"LITTLE RANN: OLD SALT-PAN MOUNDS")]
    for i,(t0,s) in enumerate(rows):
        aa=eo3(seg(lt,t0,t0+0.4)); yy=1500+i*62; d.ellipse((90,yy-9,108,yy+9),fill=AMB+(int(255*aa),)); txt(d,(130+(1-aa)*40,yy+13),s,B(40),CREAM,255*aa,"ls")
    kk=eo3(seg(lt,10.6,11.0)); 
    if kk>0: pill(img,(W/2,1000),"IN EXTREME HEAT, IT STAYS BELOW",B(38),kk,fg=INK,bg=COOL,sc=lerp(0.85,1,eob(seg(lt,10.6,11.2))))
    return img
def S3a(lt,t):
    a=fb("f4",0.40,0.72,z=1.0+0.07*seg(lt,0,6),pan=(0.01*seg(lt,0,6),0)); a=a*np.array((1.12,0.98,0.82),np.float32)
    k=seg(lt,0,6); a=a*(1-0.25*k)+np.array((40,20,50),np.float32)*0.25*k
    img=arr2img(a); scrim(img,0,720,0.62,0.0,(40,16,30)); brand(img,CREAM,170); tchip(img,"6:40 PM  ·  COOLING OFF",eo3(seg(lt,0.1,0.5)),y=150)
    comp(img,glayer((W/2,440),"DUSK",A(190)),eo3(seg(lt,0.3,0.9)),sc=lerp(1.4,1,eob(seg(lt,0.3,1.0),1.3)))
    d=ImageDraw.Draw(img,"RGBA"); aa=eo3(seg(lt,1.6,2.2)); txt(d,(W/2,580),"THE HEAT BREAKS.",B(60),CREAM,255*aa); aa=eo3(seg(lt,2.6,3.2)); txt(d,(W/2,655),"THE FOX COMES OUT.",B(60),AMB,255*aa)
    # temp falling
    tv=int(lerp(50,26,ease(seg(lt,1.0,5.0)))); aa=eo3(seg(lt,3.6,4.2)); txt(d,(W/2,740),f"{tv}°C  and falling",B(44),SAND,255*aa)
    return img
PTHAR=[(69.9,24.6),(70.1,26.0),(70.5,28.0),(71.7,29.4),(73.6,30.0),(75.0,29.2),(75.1,27.0),(74.1,25.5),(72.5,24.4)]
PGRR=[(68.3,23.6),(69.2,24.4),(70.6,24.5),(70.9,23.8),(69.5,23.2)]
PLRR=[(70.7,23.6),(71.9,23.8),(72.3,23.1),(71.3,22.7)]
_MP=None
def wmap():
    global _MP
    if _MP is None:
        cam=IC.Cam(72.0,26.0,92.0,w=960,h=1000); m=IC.map_img(cam,coast=0.7).astype(np.float32); _MP=(cam,np.clip(m*np.array((1.05,0.95,0.82))*1.7,0,255).astype(np.uint8))
    return _MP
def S3b(lt,t):
    img=night_bg(t); brand(img,CREAM,150); tchip(img,"WHERE IN INDIA?",eo3(seg(lt,0.1,0.5)),y=150)
    cam,m=wmap(); mk=Image.new("L",(960,1000),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,959,999),radius=26,fill=255); mp=Image.fromarray(m).convert("RGBA"); mp.putalpha(mk)
    ov=Image.new("RGBA",(960,1000),(0,0,0,0)); do=ImageDraw.Draw(ov,"RGBA"); fa=ease(seg(lt,0.6,2.0))
    for poly,c in ((PTHAR,AMB),(PGRR,AMB),(PLRR,AMB)):
        pts=[cam.px(*p) for p in poly]; do.polygon(pts,fill=c+(int(120*fa),),outline=c+(int(255*fa),)); do.line(pts+[pts[0]],fill=c+(int(255*fa),),width=3)
    mp.alpha_composite(ov); img.alpha_composite(mp,(60,250)); d=ImageDraw.Draw(img,"RGBA"); d.rounded_rectangle((58,248,1022,1252),radius=26,outline=AMB+(160,),width=3)
    P=lambda lo,la:(60+cam.px(lo,la)[0],250+cam.px(lo,la)[1])
    labs=[("THAR DESERT",72.2,28.4,(0,-6),"ms",B(48),2.0),("GREAT RANN",69.3,24.0,(0,30),"ms",B(36),2.6),("LITTLE RANN",71.6,23.0,(10,50),"ms",B(36),3.0)]
    for s,lo,la,(ox,oy),anc,f,t0 in labs:
        x,y=P(lo,la); a_=eo3(seg(lt,t0,t0+0.5)); txt(d,(x+ox,y+oy),s,f,CREAM,255*a_)
    pins=[(3.6,"Desert National Park",70.5,26.5,(18,-22),"ls"),(4.2,"Tal Chhapar",74.43,27.8,(-18,-22),"rs"),(4.8,"Wild Ass Sanctuary",71.5,23.3,(-16,-26),"rs")]
    for t0,s,lo,la,(ox,oy),anc in pins:
        p=seg(lt,t0,t0+0.4)
        if p<=0: continue
        x,y=P(lo,la); aa=eo3(seg(lt,t0,t0+0.15)); r=((lt-t0)*0.8)%1; d.ellipse((x-10-r*40,y-10-r*40,x+10+r*40,y+10+r*40),outline=AMB+(int(200*(1-r)*aa),),width=3); d.ellipse((x-12,y-12,x+12,y+12),fill=AMB+(int(255*aa),),outline=CREAM+(int(255*aa),),width=3)
        f=B(30); w=f.getlength(s)+26; tx=x+ox; bx=tx if anc=="ls" else tx-w; bx=max(64,min(bx,W-64-w)); d.rounded_rectangle((bx,y+oy-30,bx+w,y+oy+22),radius=12,fill=(10,12,30,int(225*aa)),outline=AMB+(int(180*aa),),width=2); txt(d,(bx+13,y+oy+8),s,f,CREAM,255*aa,"ls")
    txt(d,(W/2,1290),"Regions are approximate and illustrative.",BM(26),GREY,230)
    comp(img,glayer((W/2,1440),"THE WHITE-FOOTED FOX",A(76)),eo3(seg(lt,3.2,3.8)),dy=(1-eo3(seg(lt,3.2,3.8)))*20)
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1510),"India's dry west: Rajasthan and Gujarat",B(40),SAND,255*eo3(seg(lt,4.0,4.6)))
    return img
def waves(d,cx,cy,t,col,a,n=3,r0=190,r1=26,per=1.4):
    for k in range(n):
        u=((t/per)+k/n)%1; r=lerp(r0,r1,u); al=int(a*255*math.sin(math.pi*u)); d.arc((cx-r,cy-r,cx+r,cy+r),start=200,end=340,fill=col+(al,),width=5)
def S4a(lt,t):
    img=night_bg(t); brand(img,CREAM,150); tchip(img,"9:15 PM  ·  LISTENING",eo3(seg(lt,0.1,0.5)),y=150)
    fwin(img,"f6",(0.0,0.0,1.0,1.0),(60,330,960,900),z=1.0+0.07*seg(lt,0,4.0),spot=(0.5,0.52,0.45,0.5),k=eo3(seg(lt,0.4,1.4)),border=AMB)
    d=ImageDraw.Draw(img,"RGBA"); tp=[(60+0.30*960,330+0.22*900),(60+0.74*960,330+0.24*900)]
    wa=eo3(seg(lt,0.9,1.4))
    for (cx,cy) in tp: waves(d,cx,cy-10,lt,AMB,wa)
    comp(img,glayer((W/2,290),"BIG EARS",A(120)),eo3(seg(lt,0.2,0.8)),sc=lerp(1.3,1,eob(seg(lt,0.2,0.9),1.3)))
    comp(img,glayer((W/2,1470),"A RADAR FOR",A(84)),eo3(seg(lt,1.6,2.1)),dy=(1-eo3(seg(lt,1.6,2.1)))*24); comp(img,glayer((W/2,1570),"ANYTHING UNDERGROUND",A(84)),eo3(seg(lt,2.4,2.9)),dy=(1-eo3(seg(lt,2.4,2.9)))*24)
    return img
def S4b(lt,t):
    img=night_bg(t); brand(img,CREAM,150); tchip(img,"11:00 PM  ·  THE POUNCE",eo3(seg(lt,0.1,0.5)),y=150)
    fwin(img,"f8",(0.06,0.24,0.60,0.82),(60,340,960,560),z=1.0+0.05*seg(lt,0,9),spot=(0.29,0.60,0.15,0.11),k=eo3(seg(lt,0.3,1.2)),border=AMB)
    d=ImageDraw.Draw(img,"RGBA"); sy=1050; g=grad((86,60,40),(30,22,24),"gnd2"); 
    d.rectangle((60,sy,1020,1480),fill=(60,42,32,255)); d.rectangle((60,sy,1020,sy+8),fill=SAND+(255,)); d.rectangle((60,sy+8,1020,1480),fill=(48,34,30,255))
    rx,ry=360,1290; fx0,fy0=760,sy-8
    # rodent
    ra=eo3(seg(lt,0.8,1.3)); d.ellipse((rx-26,ry-16,rx+26,ry+18),fill=SAND+(int(255*ra),)); d.ellipse((rx+14,ry-26,rx+30,ry-10),fill=SAND+(int(255*ra),)); d.line((rx-26,ry,rx-56,ry-12),fill=SAND+(int(255*ra),),width=3)
    txt(d,(rx,ry+60),"RODENT UNDERGROUND",B(30),SAND,255*ra)
    # fox on surface
    fa=eo3(seg(lt,0.8,1.3)); 
    leap=ease(seg(lt,3.6,4.8))
    if leap<=0: fox_icon(d,fx0,fy0-18,20,AMB,int(255*fa))
    else:
        x=lerp(fx0,rx,leap); y=fy0-18-math.sin(math.pi*leap)*260
        if leap<0.97: fox_icon(d,x,y,20,AMB,255)
        else: 
            fl=seg(lt,4.8,5.3); d.ellipse((rx-60-fl*40,sy-40-fl*20,rx+60+fl*40,sy+30+fl*10),outline=AMB+(int(255*(1-fl)),),width=5)
        # dashed arc
        pts=[(lerp(fx0,rx,u/20),fy0-18-math.sin(math.pi*u/20)*260) for u in range(21)]
        for i in range(0,20,2): d.line((pts[i],pts[i+1]),fill=AMB+(200,),width=4)
    # sound rings rising
    sa=eo3(seg(lt,1.0,1.4))*(1-seg(lt,3.5,3.8))
    if sa>0:
        for k in range(4):
            u=((lt-1.0)/1.2+k/4)%1; r=lerp(20,330,u); d.arc((rx-r,ry-r,rx+r,ry+r),start=235,end=305,fill=COOL+(int(230*sa*(1-u)),),width=5)
    txt(d,(W/2,1700),"",B(10),CREAM)
    comp(img,glayer((W/2,290),"LISTEN. LOCK. LEAP.",A(88)),eo3(seg(lt,0.2,0.8)),dy=(1-eo3(seg(lt,0.2,0.8)))*20)
    d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1560),"Foxes locate prey by sound, then pounce",B(34),CREAM,255*eo3(seg(lt,2.4,3.0))*(1-seg(lt,5.8,6.2))); txt(d,(W/2,1605),"Red fox family behaviour",BM(28),GREY,255*eo3(seg(lt,2.4,3.0))*(1-seg(lt,5.8,6.2)))
    ka=eo3(seg(lt,6.4,7.0)); comp(img,glayer((W/2,1540),"THE RED FOX FAMILY'S",A(70)),ka,dy=(1-ka)*20); kb=eo3(seg(lt,6.9,7.5)); comp(img,glayer((W/2,1625),"SIGNATURE MOVE",A(84)),kb,dy=(1-kb)*20)
    return img
ICONS=[("INSECTS",ic_insect),("FRUIT + PLANTS",ic_fruit),("SMALL MAMMALS",ic_mammal),("REPTILES",ic_reptile),("BIRDS",ic_bird)]
def S5(lt,t):
    img=night_bg(t,(14,12,30),(46,30,40)); brand(img,CREAM,150); tchip(img,"MIDNIGHT  ·  THE MENU",eo3(seg(lt,0.1,0.5)),y=150)
    fwin(img,"f3",(0.0,0.20,0.62,0.80),(60,230,960,480),z=1.0+0.05*seg(lt,0,12),spot=(0.30,0.55,0.20,0.12),k=eo3(seg(lt,0.3,1.2)),border=AMB)
    d=ImageDraw.Draw(img,"RGBA"); pos=[(240,990),(540,990),(840,990),(390,1260),(690,1260)]
    for i,((nm,fn),(cx,cy)) in enumerate(zip(ICONS,pos)):
        t0=1.6+i*1.5; a=eo3(seg(lt,t0,t0+0.4)); s=lerp(0.6,1,eob(seg(lt,t0,t0+0.5)))
        if a<=0: continue
        act=1 if lt<t0+1.3 else 0.55
        d.ellipse((cx-100*s,cy-100*s,cx+100*s,cy+100*s),fill=(14,16,34,int(230*a)),outline=AMB+(int(255*a*act),),width=4)
        fn(d,cx,cy-6,60*s,AMB if act>0.9 else SAND,int(255*a)); txt(d,(cx,cy+150),nm,B(36),CREAM,255*a)
    aa=eo3(seg(lt,9.2,9.8)); comp(img,glayer((W/2,1545),"NOT PICKY.",A(100)),aa,sc=lerp(1.3,1,eob(seg(lt,9.2,9.9),1.3))); txt(d,(W/2,1618),"THAT IS HOW IT SURVIVES THERE.",B(46),CREAM,255*eo3(seg(lt,10.0,10.6)))
    txt(d,(W/2,1662),"Diet studies: insects, plants, small mammals; also reptiles, birds",BM(26),GREY,230*eo3(seg(lt,10.0,10.6)))
    return img
def S6a(lt,t):
    a=fb("f7",0.60,0.70,z=1.0+0.06*seg(lt,0,7),pan=(0.0,0.0)); a=a*np.array((1.08,1.0,0.9),np.float32); img=arr2img(a)
    scrim(img,0,560,0.55,0.0,(10,8,20)); scrim(img,1180,1700,0.0,0.7,(10,8,20)); brand(img,CREAM,170); tchip(img,"BACK AT THE DEN",eo3(seg(lt,0.1,0.5)),y=150)
    comp(img,glayer((W/2,330),"BORN UNDERGROUND",A(100)),eo3(seg(lt,0.3,0.9)),dy=(1-eo3(seg(lt,0.3,0.9)))*24)
    d=ImageDraw.Draw(img,"RGBA"); n=min(5,int(seg(lt,1.8,4.2)*5+0.999)) if lt>1.8 else 0
    for i in range(n):
        x=W/2-(n-1)*70+i*140; aa=eo3(seg(lt,1.8+i*0.5,2.2+i*0.5)); fox_icon(d,x,1430,32*lerp(0.5,1,aa),AMB,int(255*aa))
    if lt>3.8: txt(d,(W/2,1545),"ABOUT 3 TO 5 PUPS A LITTER",A(58),CREAM,255*eo3(seg(lt,3.8,4.4))); txt(d,(W/2,1600),"sources vary",BM(30),GREY,255*eo3(seg(lt,4.2,4.8)))
    return img
def S6b(lt,t):
    a=fb("f10",0.40,0.74,z=1.0+0.06*seg(lt,0,6),pan=(0.0,0.0)); a=a*np.array((1.08,1.0,0.9),np.float32); img=arr2img(a)
    scrim(img,1180,1700,0.0,0.72,(10,8,20)); brand(img,CREAM,170)
    comp(img,glayer((W/2,1400),"3 TO 4 MONTHS OF CARE",A(70)),eo3(seg(lt,0.3,0.9)),dy=(1-eo3(seg(lt,0.3,0.9)))*24)
    d=ImageDraw.Draw(img,"RGBA"); bx0,bx1,by=140,940,1470; d.rounded_rectangle((bx0,by-14,bx1,by+14),radius=14,fill=(255,255,255,40)); p=ease(seg(lt,0.8,3.4)); d.rounded_rectangle((bx0,by-14,bx0+(bx1-bx0)*p,by+14),radius=14,fill=AMB+(240,))
    for m in range(5): txt(d,(bx0+(bx1-bx0)*m/4,by+54),f"{m}",B(30),GREY,230)
    txt(d,(W/2,by+96),"months of care",BM(28),GREY,230)
    comp(img,glayer((W/2,1625),"THEN, ONE NIGHT, THEY STEP OUT.",A(46)),eo3(seg(lt,3.8,4.4)))
    return img
def S7(lt,t):
    img=night_bg(t,(10,14,30),(28,34,44)); brand(img,CREAM,150); tchip(img,"THE LONG VIEW",eo3(seg(lt,0.1,0.5)),y=150)
    comp(img,glayer((W/2,290),"BUT THE DESERT",A(88)),eo3(seg(lt,0.2,0.7))); comp(img,glayer((W/2,390),"IS CHANGING",A(88)),eo3(seg(lt,0.5,1.0)))
    fwin(img,"f5",(0.0,0.20,1.0,0.88),(110,450,860,520),z=1.0+0.04*seg(lt,0,12),spot=(0.28,0.55,0.18,0.15),k=eo3(seg(lt,0.6,1.5)),border=LEAF)
    d=ImageDraw.Draw(img,"RGBA")
    rows=[(2.0,"VILAYATI BABOOL (PROSOPIS) CROWDS OUT OPEN LAND"),(4.2,"FREE-RANGING DOGS + THEIR DISEASES"),(6.0,"ROADS, FARMS AND TOWNS KEEP GROWING")]
    for i,(t0,s) in enumerate(rows):
        aa=eo3(seg(lt,t0,t0+0.4)); yy=[1075,1255,1330][i]; d.ellipse((80,yy-10,100,yy+10),fill=(235,90,70,int(255*aa))); 
        f=B(36); words=s.split(); 
        txt(d,(125+(1-aa)*30,yy+13),s,f,CREAM,255*aa,"ls")
    # shrinking open habitat bar
    ba=eo3(seg(lt,2.2,2.8))
    if ba>0:
        bx0,bx1,by=125,955,1110; d.rounded_rectangle((bx0,by,bx1,by+30),radius=15,fill=SAND+(int(230*ba),)); g=ease(seg(lt,2.8,6.0))
        d.rounded_rectangle((bx1-(bx1-bx0)*0.6*g,by,bx1,by+30),radius=15,fill=(70,120,60,int(255*ba))); txt(d,(bx0,by+58),"open land",BM(26),SAND,255*ba,"ls"); txt(d,(bx1,by+58),"invaded",BM(26),LEAF,255*ba,"rs")
    k=eo3(seg(lt,7.6,8.2))
    if k>0:
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); dl.rounded_rectangle((70,1400,1010,1650),radius=28,fill=(12,14,30,235),outline=AMB+(255,),width=4); comp(img,l,k,sc=lerp(0.9,1,eob(seg(lt,7.6,8.4))))
        d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1485),"NO ONE KNOWS HOW MANY",A(70),AMB,255*k)
        txt(d,(W/2,1552),"No count exists for this fox.",B(40),CREAM,255*eo3(seg(lt,8.6,9.2))); txt(d,(W/2,1605),"IUCN 'Least Concern' is for the red fox worldwide.",BM(30),GREY,255*eo3(seg(lt,9.2,9.8)))
    return img
def S8(lt,t):
    img=night_bg(t,(10,12,32),(40,30,60)); brand(img,CREAM,150)
    comp(img,glayer((W/2,300),"NEXT TIME,",A(100)),eo3(seg(lt,1.3,1.8))); comp(img,glayer((W/2,420),"AT DUSK, LOOK BACK.",A(100)),eo3(seg(lt,2.4,3.0)),sc=lerp(1.2,1,eob(seg(lt,2.4,3.1),1.3)))
    fwin(img,"f1",(0.03,0.22,0.98,0.95),(60,520,960,540),z=1.0+0.05*seg(lt,0,15),spot=(0.40,0.60,0.34,0.26),k=eo3(seg(lt,0.6,1.6)),warm=(0.85,0.92,1.12),border=AMB)
    d=ImageDraw.Draw(img,"RGBA")
    q=eo3(seg(lt,7.7,8.3)); comp(img,glayer((W/2,1210),"HAVE YOU SEEN A DESERT FOX?",A(66)),q,dy=(1-q)*24)
    btn=L(); ImageDraw.Draw(btn,"RGBA").rounded_rectangle((W/2-330,1260,W/2+330,1352),radius=46,fill=AMB+(250,))
    f=B(44); s1_="COMMENT \""; s2_="FOX"; s3_="\" + WHERE"; tw=f.getlength(s1_+s2_+s3_); x0=W/2-tw/2
    a1=L(); txt(ImageDraw.Draw(a1,"RGBA"),(x0,1323),s1_,f,INK,255,"ls"); x2=x0+f.getlength(s1_); w2=f.getlength(s2_); a3=L(); txt(ImageDraw.Draw(a3,"RGBA"),(x2+w2,1323),s3_,f,INK,255,"ls")
    ba=eo3(seg(lt,10.4,10.8)); comp(img,btn,ba,sc=lerp(0.6,1,eob(seg(lt,10.4,11.0)))); comp(img,a1,eo3(seg(lt,10.8,11.1))); comp(img,a3,eo3(seg(lt,10.8,11.1)))
    n=int(3*seg(lt,12.0,12.9)+0.999) if lt>12.0 else 0
    if n>0:
        w=L(); txt(ImageDraw.Draw(w,"RGBA"),(x2,1323),s2_[:n],f,(120,40,10),255,"ls"); comp(img,w,1)
    cl=L(); dc=ImageDraw.Draw(cl,"RGBA")
    for i,s in enumerate(["A typical night, based on field studies of desert foxes. Not one animal's story.","Photos: Hitesh Chawla. Different foxes shown. Maps: Natural Earth, illustrative."]): txt(dc,(W/2,1470+i*40),s,BM(27),GREY,235)
    comp(img,cl,eo3(seg(lt,13.2,14.0)))
    return img
FN={"S1":S1,"S2":S2,"S3a":S3a,"S3b":S3b,"S4a":S4a,"S4b":S4b,"S5":S5,"S6a":S6a,"S6b":S6b,"S7":S7,"S8":S8}
VIGN=None;GRN=None
def finish(fr,t):
    global VIGN,GRN
    if VIGN is None:
        yy,xx=np.mgrid[0:H,0:W]; dd=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2); VIGN=(1-0.28*np.clip(dd-0.45,0,1)**1.3).astype(np.float32)[:,:,None]; GRN=np.random.default_rng(3).normal(0,3.2,(H+64,W+64,1)).astype(np.float32)
    ox=int((t*977)%64); oy=int((t*613)%64); return np.clip(fr*VIGN+GRN[oy:oy+H,ox:ox+W],0,255).astype(np.uint8)
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
