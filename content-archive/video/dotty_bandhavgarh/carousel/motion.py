import sys; sys.path.insert(0,'.')
from car import *
import subprocess
S34=ld('s34.png'); P31=ld('p31.png'); S31=ld('s31.png'); S33=ld('s33.png')
DX,DY=486,365; FPS=30; DUR=6.0
def ease(x): x=min(1,max(0,x)); return x*x*(3-2*x)
def eo3(x): x=min(1,max(0,x)); return 1-(1-x)**3
def eob(x,k=1.7): x=min(1,max(0,x)); return 1+(k+1)*(x-1)**3+k*(x-1)**2
def seg(t,a,b): return min(1,max(0,(t-a)/(b-a)))
def L(): return Image.new("RGBA",(W,H),(0,0,0,0))
TEXG=None
def gold_layer(xy,s,f,anchor="ms"):
    lay=L(); gold_text(lay,xy,s,f,anchor); return lay
def amul(lay,a):
    if a>=0.999: return lay
    l=lay.copy(); l.putalpha(l.split()[-1].point(lambda v:int(v*max(0,a)))); return l
def comp(img,lay,a=1.0,dx=0,dy=0,sc=1.0,rot=0.0):
    if a<=0.003: return
    if sc==1 and rot==0:
        l=amul(lay,a)
        if dx or dy: img.alpha_composite(l,(int(dx),int(dy))) if False else img.alpha_composite(l.transform(l.size,Image.AFFINE,(1,0,-dx,0,1,-dy)))
        else: img.alpha_composite(l)
        return
    bb=lay.getbbox(); 
    if not bb: return
    pad=40; bb=(max(0,bb[0]-pad),max(0,bb[1]-pad),min(W,bb[2]+pad),min(H,bb[3]+pad))
    c=lay.crop(bb); cx=(bb[0]+bb[2])/2+dx; cy=(bb[1]+bb[3])/2+dy
    nw,nh=max(1,int(c.width*sc)),max(1,int(c.height*sc)); c=c.resize((nw,nh),Image.BICUBIC)
    if rot: c=c.rotate(rot,expand=True,resample=Image.BICUBIC)
    c=amul(c,a); img.alpha_composite(c,(int(cx-c.width/2),int(cy-c.height/2)))
def wipe(lay,p,soft=60,vertical=False):
    if p>=1: return lay
    bb=lay.getbbox()
    if not bb or p<=0: return L()
    m=np.zeros((H,W),np.float32)
    if vertical:
        y=bb[1]+(bb[3]-bb[1]+soft)*p; yy=np.arange(H)[:,None]; m[:]=np.clip((y-yy)/soft,0,1)
    else:
        x=bb[0]+(bb[2]-bb[0]+soft)*p; xx=np.arange(W)[None,:]; m[:]=np.clip((x-xx)/soft,0,1)
    l=lay.copy(); a=np.array(l.split()[-1]).astype(np.float32)*m; l.putalpha(Image.fromarray(a.astype(np.uint8))); return l
def shine(img,lay,p,width=90,strength=170):
    if p<=0 or p>=1: return
    bb=lay.getbbox()
    if not bb: return
    x=bb[0]-200+(bb[2]-bb[0]+400)*p
    yy,xx=np.mgrid[0:H,0:W]; band=np.clip(1-np.abs((xx+(yy-bb[1])*0.35)-x)/width,0,1)
    a=np.array(lay.split()[-1]).astype(np.float32)/255*band*strength
    s=Image.new("RGBA",(W,H),(255,250,235,0)); s.putalpha(Image.fromarray(a.astype(np.uint8))); img.alpha_composite(s)
def photo_lay(src,box,rect,z,border=GOLD):
    x0,y0,x1,y1=box; cx,cy=(x0+x1)/2,(y0+y1)/2; hw,hh=(x1-x0)/2/z,(y1-y0)/2/z
    lay=L(); photo(lay,src,(int(cx-hw),int(cy-hh),int(cx+hw),int(cy+hh)),rect,border=border); return lay
def to_arr(img): return np.array(img)[...,:3]

# ---------------- SLIDE 1 ----------------
def s1():
    box=(336,178,636,560); rect=(230,118,620,789)
    sc=rect[2]/(box[2]-box[0]); sx=rect[0]+(DX-box[0])*sc; sy=rect[1]+(DY-box[1])*rect[3]/(box[3]-box[1]); rx,ry=40*sc,22*sc
    base=stripes(W,H,11); photo(base,S34,box,rect,border=AMB)
    glow=base.copy(); glow_ellipse(glow,sx,sy,rx,ry)   # includes ring; we only use for glow fill
    d=ImageDraw.Draw(base,"RGBA")
    credit(d,"Photo: © Ashish Tirkey / Pugdundee Safaris",y=rect[1]+rect[3]+32,x=rect[0]+rect[2],anchor="rs")
    txt(d,(W/2,1020),"SHE WAS BORN WITH A",B(54),CREAM)
    txt(d,(W/2,1250),"THE STORY OF DOTTY, BANDHAVGARH'S LEGEND",B(40),GREY); txt(d,(W/2,1310),"c. 2012 TO 2026",B(36),GOLD)
    chrome(base,1)
    # glow without ring: redo
    g2=base.copy(); 
    Lm=Image.new("L",(W,H),0); ImageDraw.Draw(Lm).ellipse((sx-rx,sy-ry,sx+rx,sy+ry),fill=255)
    g=np.array(Lm.filter(ImageFilter.GaussianBlur(max(4,rx*0.35)))).astype(np.float32)/255
    ga=np.array(base).astype(np.float32); ga[...,:3]=np.clip(ga[...,:3]*(1+g[...,None]*0.35)+g[...,None]*np.array((60,30,0)),0,255); g2=Image.fromarray(ga.astype(np.uint8))
    head=gold_layer((W/2,1180),"\"D\" ON HER HEAD",A(150))
    ly=rect[1]+78
    lab=L(); dl=ImageDraw.Draw(lab,"RGBA"); dl.rounded_rectangle((sx-160,ly-46,sx+160,ly+14),radius=16,fill=(16,12,8,225),outline=AMB+(255,),width=3); txt(dl,(sx,ly-6),"HER \"D\" MARK",A(38),CREAM)
    def fr(t):
        ga_=ease(seg(t,0.9,1.5))*(0.85+0.15*math.sin(t*4))
        img=Image.blend(base,g2,ga_) if ga_>0 else base.copy()
        d=ImageDraw.Draw(img,"RGBA"); p=eo3(seg(t,0.3,1.2))
        if p>0: d.arc((sx-rx*1.08,sy-ry*1.12,sx+rx*1.08,sy+ry*1.12),start=-90,end=-90+360*p,fill=AMB+(255,),width=5)
        lp=eo3(seg(t,1.1,1.5))
        if lp>0: y0=sy-ry*1.12; d.line((sx,y0,sx,y0+(ly+14-y0)*lp),fill=AMB+(230,),width=3)
        comp(img,lab,eo3(seg(t,1.4,1.7)),sc=lerp(0.6,1,eob(seg(t,1.4,1.9))))
        img.alpha_composite(wipe(head,eo3(seg(t,0.1,1.0))))
        shine(img,head,seg(t,2.2,3.2)); shine(img,head,seg(t,4.6,5.6))
        return img
    return fr
def lerp(a,b,x): return a+(b-a)*x

# ---------------- SLIDE 2 ----------------
def s2():
    base=stripes(W,H,12); title=gold_layer((W/2,206),"WHO WAS DOTTY?",A(112)); base.alpha_composite(title)
    d=ImageDraw.Draw(base,"RGBA"); credit(d,"Photo: © Ashish Tirkey / Pugdundee Safaris",y=884,x=W-60,anchor="rs")
    rows=[("BORN","c. 2012, Magadhi zone"),("MOTHER","Sukhi Patiha"),("SISTER","Spotty")]
    y=975
    for k,v in rows:
        d.rounded_rectangle((60,y-58,W-60,y+22),radius=18,fill=(16,12,8,170),outline=GOLD+(90,),width=2)
        txt(d,(96,y),k,B(36),GOLD,255,"ls"); txt(d,(W-96,y),v,A(44),CREAM,255,"rs"); y+=100
    txt(d,(W/2,1360),"Family details from safari records, not official.",BM(28),GREY,230); chrome(base,2)
    y4=1275
    box=L(); db=ImageDraw.Draw(box,"RGBA"); db.rounded_rectangle((60,y4-58,W-60,y4+22),radius=18,fill=(30,18,6,230),outline=AMB+(255,),width=3); txt(db,(96,y4),"NAMED FOR",B(36),GOLD,255,"ls")
    val=L(); dv=ImageDraw.Draw(val,"RGBA"); txt(dv,(W-96,y4),"The \"D\" on her forehead",A(46),CREAM,255,"rs")
    dbig=L(); txt(ImageDraw.Draw(dbig,"RGBA"),(W/2,y4-160),"",A(10),GOLD)
    def fr(t):
        img=base.copy(); img.alpha_composite(photo_lay(S34,(27,178,990,805),(60,262,960,586),1+0.06*ease(t/DUR)))
        p=eob(seg(t,0.4,1.1)); comp(img,box,eo3(seg(t,0.4,0.8)),dx=(1-p)*700)
        img.alpha_composite(wipe(val,eo3(seg(t,1.1,2.0))))
        shine(img,val,seg(t,2.4,3.3),strength=200)
        pa=ease(seg(t,2.0,2.4))*(0.5+0.5*math.sin((t-2)*3))
        if pa>0: ImageDraw.Draw(img,"RGBA").rounded_rectangle((54,y4-64,W-54,y4+28),radius=22,outline=AMB+(int(200*pa),),width=4)
        return img
    return fr

# ---------------- SLIDE 3 ----------------
def s3():
    base=stripes(W,H,13); d=ImageDraw.Draw(base,"RGBA")
    txt(d,(W/2,180),"PUSHED OUT BY",B(60),CREAM); base.alpha_composite(gold_layer((W/2,320),"HER OWN DAUGHTERS",A(118)))
    d=ImageDraw.Draw(base,"RGBA"); txt(d,(W/2,1360),"The jungle's oldest rule: territory goes to the strongest.",BM(30),GREY,230); chrome(base,3)
    steps=[("c. 2012","Born in Magadhi zone",GOLD),("MAGADHI","Raised her litters here",GOLD),("THE TWIST","Her grown daughters took over",RED),("TALA ZONE","She moved, and started again",CYAN),("c. 2025","A mother again: 2 cubs",AMB)]
    x0=200; y=470; dots=[]; texts=[]
    for k,(a,b,c) in enumerate(steps):
        yy=y+k*190
        dl=L(); ImageDraw.Draw(dl,"RGBA").ellipse((x0-24,yy-24,x0+24,yy+24),fill=c+(255,),outline=CREAM+(255,),width=4); dots.append(dl)
        tl=L(); dt=ImageDraw.Draw(tl,"RGBA"); txt(dt,(x0+60,yy-6),a,A(54),c,255,"ls"); txt(dt,(x0+60,yy+44),b,B(42),CREAM,255,"ls"); texts.append(tl)
    def fr(t):
        img=base.copy(); d=ImageDraw.Draw(img,"RGBA")
        p=ease(seg(t,0.3,3.3)); d.line((x0,y,x0,y+760*p),fill=GOLD+(140,),width=4)
        for k in range(5):
            tk=0.3+k*0.75
            comp(img,dots[k],eo3(seg(t,tk,tk+0.2)),sc=lerp(0.2,1,eob(seg(t,tk,tk+0.45))))
            comp(img,texts[k],eo3(seg(t,tk+0.1,tk+0.5)),dx=(1-eo3(seg(t,tk+0.1,tk+0.6)))*60)
        if t>3.6:
            k=2; pa=0.5+0.5*math.sin((t-3.6)*4); yy=y+k*190
            d=ImageDraw.Draw(img,"RGBA"); d.ellipse((x0-40,yy-40,x0+40,yy+40),outline=RED+(int(160*pa),),width=4)
        return img
    return fr

# ---------------- SLIDE 4 ----------------
def s4():
    base=stripes(W,H,14); d=ImageDraw.Draw(base,"RGBA")
    txt(d,(W/2,180),"HER BLOODLINE",B(60),CREAM); base.alpha_composite(gold_layer((W/2,320),"STILL RULES",A(140))); d=ImageDraw.Draw(base,"RGBA")
    def node(cx,cy,l,s,col=GOLD,w=320,h=110):
        d.rounded_rectangle((cx-w/2,cy-h/2,cx+w/2,cy+h/2),radius=22,fill=(16,12,8,225),outline=col+(255,),width=3)
        txt(d,(cx,cy),l,A(46),CREAM); txt(d,(cx,cy+40),s,B(28),col)
    def ln(a,b): d.line((a,b),fill=GOLD+(150,),width=4)
    node(540,450,"SUKHI PATIHA","MOTHER")
    ln((540,505),(540,600)); ln((300,600),(780,600)); ln((300,600),(300,640)); ln((780,600),(780,640))
    node(300,695,"DOTTY","THE \"D\" TIGRESS",AMB); node(780,695,"SPOTTY","HER SISTER")
    ln((300,750),(300,840)); ln((180,840),(900,840))
    for x in (180,540,900): ln((x,840),(x,890))
    node(180,950,"D1","REPORTED SON",GOLD,280); node(540,950,"DAUGHTERS","TOOK MAGADHI",CYAN,280); node(900,950,"2 CUBS","BORN c. 2025",AMB,280)
    txt(d,(W/2,1360),"Lineage as reported in safari records, not official.",BM(30),GREY,230); chrome(base,4)
    bx=L(); db=ImageDraw.Draw(bx,"RGBA"); db.rounded_rectangle((90,1090,W-90,1240),radius=24,fill=(16,12,8,215),outline=GOLD+(160,),width=3)
    l1=L(); txt(ImageDraw.Draw(l1,"RGBA"),(W/2,1150),"D1 IS NOW CALLED THE",B(40),GOLD)
    l2=gold_layer((W/2,1218),"KING OF KHITAULI",A(62))
    def fr(t):
        img=base.copy(); d=ImageDraw.Draw(img,"RGBA")
        p=ease(seg(t,0.2,0.7)); 
        if p>0: d.line((180,1005,180,1005+85*p),fill=GOLD+(200,),width=4)
        comp(img,bx,eo3(seg(t,0.6,0.9)),sc=lerp(0.85,1,eob(seg(t,0.6,1.1))))
        comp(img,l1,eo3(seg(t,1.0,1.4)),dy=(1-eo3(seg(t,1.0,1.4)))*20)
        img.alpha_composite(wipe(l2,eo3(seg(t,1.4,2.3))))
        shine(img,l2,seg(t,2.6,3.5),strength=200); shine(img,l2,seg(t,4.6,5.5),strength=200)
        pa=ease(seg(t,0.2,0.6))*(0.55+0.45*math.sin(t*3.5))
        d=ImageDraw.Draw(img,"RGBA"); d.rounded_rectangle((180-148,950-63,180+148,950+63),radius=26,outline=GOLD+(int(180*pa),),width=4)
        return img
    return fr

# ---------------- SLIDE 5 ----------------
def s5():
    base=stripes(W,H,15); d=ImageDraw.Draw(base,"RGBA")
    txt(d,(W/2,180),"THE DAY BANDHAVGARH WENT QUIET",B(52),CREAM); base.alpha_composite(gold_layer((W/2,320),"9 OCTOBER 2026",A(124))); d=ImageDraw.Draw(base,"RGBA")
    txt(d,(W/2,1330),"Samples sent for testing. Field Director, as reported.",BM(30),GREY,230)
    credit(d,"Screenshot: The Hans India, 11 Oct 2026",y=H-46); chrome(base,5)
    cs=S31.crop((0,0,1037,560)); cl=L(); card(cl,cs,W/2,600,0.82,0)
    facts=[("WHERE","Majhkheta beat, Manpur buffer"),("FOUND","During an elephant patrol"),("AGE","About 14 years"),("CAUSE","Natural, as per preliminary exam")]
    fl=[]; y=940
    for k,v in facts:
        l=L(); dl=ImageDraw.Draw(l,"RGBA"); txt(dl,(90,y),k,B(36),GOLD,255,"ls"); txt(dl,(W-90,y),v,A(42),CREAM,255,"rs"); dl.line((90,y+24,W-90,y+24),fill=GOLD+(60,),width=2); fl.append(l); y+=92
    def fr(t):
        img=base.copy(); p=eob(seg(t,0.2,1.0),1.3)
        comp(img,cl,eo3(seg(t,0.2,0.5)),dy=(1-p)*-500,sc=lerp(1.25,1,p),rot=lerp(-10,2.2,eo3(seg(t,0.2,1.0))))
        if 0.9<t<1.3: 
            k=1-seg(t,0.9,1.3); a=np.array(img).astype(np.float32); a[...,:3]=np.clip(a[...,:3]+k*25,0,255); img=Image.fromarray(a.astype(np.uint8))
        for i,l in enumerate(fl):
            tk=1.3+i*0.35; comp(img,l,eo3(seg(t,tk,tk+0.35)),dx=(1-eo3(seg(t,tk,tk+0.45)))*-60)
        return img
    return fr

# ---------------- SLIDE 6 ----------------
def s6():
    base=stripes(W,H,16); base.alpha_composite(gold_layer((W/2,250),"TWO CUBS",A(150))); d=ImageDraw.Draw(base,"RGBA")
    txt(d,(W/2,326),"LEFT BEHIND",B(64),CREAM)
    bx0,bx1,by=110,970,760; X=lambda m:bx0+(bx1-bx0)*m/24
    txt(d,(W/2,650),"HOW LONG CUBS STAY WITH MOM",B(42),GOLD)
    d.rounded_rectangle((bx0,by-22,bx1,by+22),radius=22,fill=(255,255,255,30))
    for m in (0,6,12,18,24): txt(d,(X(m),by+66),f"{m}",B(32),GREY)
    txt(d,(W/2,by+110),"MONTHS",B(28),GREY)
    d.rounded_rectangle((90,980,W-90,1210),radius=26,fill=(16,12,8,200),outline=CYAN+(160,),width=3)
    txt(d,(W/2,1060),"MONTHS SHORT OF INDEPENDENCE",A(56),CREAM); txt(d,(W/2,1130),"The forest department is monitoring them.",B(40),CYAN)
    txt(d,(W/2,1180),"Cub age as reported. 18-24 months is the usual range.",BM(28),GREY)
    credit(d,"Screenshot: Hindi news report, 10 Oct 2026",y=H-46); chrome(base,6)
    cs=S33.crop((0,0,845,190)); cl=L(); card(cl,cs,W/2,480,1.12,0)
    def fr(t):
        img=base.copy(); p=eob(seg(t,0.2,1.0),1.3)
        comp(img,cl,eo3(seg(t,0.2,0.5)),dx=(1-p)*-900,rot=lerp(6,-1.6,eo3(seg(t,0.2,1.0))))
        d=ImageDraw.Draw(img,"RGBA")
        ua=eo3(seg(t,1.1,1.5))
        if ua>0: d.rounded_rectangle((X(18),by-22,X(24),by+22),radius=22,fill=CYAN+(int(150*ua),)); txt(d,(X(21),by+8),"USUAL 18-24",B(28),INK,int(255*ua),"mm")
        f=15.5*ease(seg(t,1.3,2.8))
        if f>0.5: d.rounded_rectangle((bx0,by-22,X(f),by+22),radius=22,fill=AMB+(235,))
        ma=eo3(seg(t,2.7,3.1))
        if ma>0: d.line((X(15.5),by-60,X(15.5),by+30),fill=CREAM+(int(255*ma),),width=4); txt(d,(X(15.5),by-72),"DOTTY'S CUBS: 15-16 MONTHS",B(34),CREAM,int(255*ma))
        if t>3.1:
            pa=0.5+0.5*math.sin((t-3.1)*4); d.rounded_rectangle((X(15.5),by-30,X(18),by+30),radius=10,outline=RED+(int(200*pa),),width=3)
        return img
    return fr

# ---------------- SLIDE 7 ----------------
def s7():
    base=stripes(W,H,17); d=ImageDraw.Draw(base,"RGBA")
    txt(d,(W/2,180),"WHY 14 IS A FULL LIFE",B(60),CREAM)
    credit(d,"Photo: NBT, as published by The Hans India",y=840,x=W-60,anchor="rs")
    bx0,bx1,by=110,970,1110; X=lambda y_:bx0+(bx1-bx0)*y_/18
    d.rounded_rectangle((bx0,by-18,bx1,by+18),radius=18,fill=(255,255,255,30))
    for v in (0,5,10,15,18): txt(d,(X(v),by+58),f"{v}",B(30),GREY)
    txt(d,(W/2,1260),"Two zones. Many litters. A bloodline that still rules.",B(40),CREAM)
    txt(d,(W/2,1310),"Wild lifespan: general estimate.",BM(28),GREY); chrome(base,7)
    cache={}
    def fr(t):
        img=base.copy(); img.alpha_composite(photo_lay(P31,(0,0,820,490),(60,230,960,574),1+0.06*ease(t/DUR),AMB))
        d=ImageDraw.Draw(img,"RGBA")
        ra=eo3(seg(t,0.4,0.9))
        if ra>0: d.rounded_rectangle((X(10),by-18,X(15),by+18),radius=18,fill=GOLD+(int(120*ra),)); txt(d,(X(12.5),by-34),"MOST WILD TIGERS: 10-15 YRS",B(30),GOLD,int(255*ra))
        v=14*ease(seg(t,0.9,2.9)); n=int(round(v))
        d.rounded_rectangle((bx0,by-8,X(v)+1,by+8),radius=8,fill=AMB+(200,))
        d.ellipse((X(v)-20,by-20,X(v)+20,by+20),fill=AMB+(255,),outline=CREAM+(255,),width=4)
        if n not in cache: cache[n]=gold_layer((W/2,1010),f"{n} YEARS",A(140))
        img.alpha_composite(cache[n])
        if t>2.9:
            k=seg(t,2.9,3.6); rr=20+60*k; d.ellipse((X(14)-rr,by-rr,X(14)+rr,by+rr),outline=AMB+(int(220*(1-k)),),width=4)
            shine(img,cache[14],seg(t,3.2,4.2))
        return img
    return fr

# ---------------- SLIDE 8 ----------------
def s8():
    base=stripes(W,H,18); d=ImageDraw.Draw(base,"RGBA")
    base.alpha_composite(gold_layer((W/2,880),"DID YOU EVER",A(110))); base.alpha_composite(gold_layer((W/2,990),"SEE DOTTY?",A(110)))
    d=ImageDraw.Draw(base,"RGBA")
    cl=["Photos: © Ashish Tirkey / Pugdundee Safaris; NBT via The Hans India.","Screenshots: The Hans India; Hindi news report.","Images belong to their respective owners. DM for credit or removal.","With respect to every photographer who documented her."]
    y=1220
    for s in cl: txt(d,(W/2,y),s,BM(28),GREY,235); y+=40
    chrome(base,8,swipe=False)
    r=300; cxp,cyp=486,367
    mk=Image.new("L",(2*r,2*r),0); ImageDraw.Draw(mk).ellipse((0,0,2*r-1,2*r-1),fill=255)
    btn=L(); ImageDraw.Draw(btn,"RGBA").rounded_rectangle((W/2-330,1040,W/2+330,1136),radius=48,fill=GOLD+(245,))
    f=B(42); s1_="COMMENT \""; s2_="DOTTY"; s3_="\" + YOUR MEMORY"; tw=f.getlength(s1_+s2_+s3_); x0=W/2-tw/2
    a1=L(); txt(ImageDraw.Draw(a1,"RGBA"),(x0,1106),s1_,f,INK,255,"ls")
    x2=x0+f.getlength(s1_); w2=f.getlength(s2_)
    a3=L(); txt(ImageDraw.Draw(a3,"RGBA"),(x2+w2,1106),s3_,f,INK,255,"ls")
    def fr(t):
        img=base.copy(); z=1+0.08*ease(t/DUR); hw=105/z
        ph=S34.crop((int(cxp-hw),int(cyp-hw),int(cxp+hw),int(cyp+hw))).resize((2*r,2*r),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,80,2)).convert("RGBA"); ph.putalpha(mk)
        img.alpha_composite(ph,(W//2-r,140)); d=ImageDraw.Draw(img,"RGBA"); d.ellipse((W//2-r-4,136,W//2+r+4,140+2*r+4),outline=AMB+(255,),width=5)
        comp(img,btn,eo3(seg(t,0.3,0.6)),sc=lerp(0.5,1,eob(seg(t,0.3,0.9))))
        ta=eo3(seg(t,0.7,1.0)); comp(img,a1,ta); comp(img,a3,ta)
        n=int(5*seg(t,1.1,1.9)+0.999) if t>1.1 else 0
        pul=1+0.05*max(0,math.sin((t-2.0)*3.2)) if t>2.0 else 1
        if n>0:
            w=L(); dw=ImageDraw.Draw(w,"RGBA"); txt(dw,(x2,1106),s2_[:n],f,(150,36,8),255,"ls")
            comp(img,w,1,sc=pul)
        return img
    return fr

SL=[s1,s2,s3,s4,s5,s6,s7,s8]
def render(i):
    fr=SL[i]()
    out=f"Dotty_Motion_{i+1}.mp4"
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
        "-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","64k","-movflags","+faststart",out],stdin=subprocess.PIPE)
    for k in range(int(DUR*FPS)):
        p.stdin.write(to_arr(fr(k/FPS)).tobytes())
    p.stdin.close(); p.wait(); return out
if __name__=="__main__":
    from multiprocessing import Pool
    idx=[int(a)-1 for a in sys.argv[1:]] or list(range(8))
    with Pool(4) as pl: print(pl.map(render,idx))
