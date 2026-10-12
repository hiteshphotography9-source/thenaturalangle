import sys; sys.path.insert(0,'.')
from car import *
S34=ld('s34.png'); P31=ld('p31.png'); S31=ld('s31.png'); S33=ld('s33.png')
DX,DY=486,365
def save(img,n): Image.fromarray(np.array(img)[...,:3]).save(f"Dotty_Carousel_{n}.jpg",quality=95)

# 1 HOOK
img=stripes(W,H,11); 
box=(336,178,636,560); rect=(230,118,620,789)
photo(img,S34,box,rect,border=AMB)
sc=rect[2]/(box[2]-box[0]); sx=rect[0]+(DX-box[0])*sc; sy=rect[1]+(DY-box[1])*rect[3]/(box[3]-box[1])
glow_ellipse(img,sx,sy,40*sc,22*sc)
d=ImageDraw.Draw(img,"RGBA"); ly=rect[1]+78
d.line((sx,sy-22*sc*1.12,sx,ly+14),fill=AMB+(230,),width=3)
d.rounded_rectangle((sx-160,ly-46,sx+160,ly+14),radius=16,fill=(16,12,8,225),outline=AMB+(255,),width=3)
txt(d,(sx,ly-6),"HER \"D\" MARK",A(38),CREAM)
credit(d,"Photo: © Ashish Tirkey / Pugdundee Safaris",y=rect[1]+rect[3]+32,x=rect[0]+rect[2],anchor="rs")
txt(d,(W/2,1020),"SHE WAS BORN WITH A",B(54),CREAM)
gold_text(img,(W/2,1180),"\"D\" ON HER HEAD",A(150))
d=ImageDraw.Draw(img,"RGBA")
txt(d,(W/2,1250),"THE STORY OF DOTTY, BANDHAVGARH'S LEGEND",B(40),GREY)
txt(d,(W/2,1310),"c. 2012 TO 2026",B(36),GOLD)
chrome(img,1); save(img,1)

# 2 WHO
img=stripes(W,H,12); d=ImageDraw.Draw(img,"RGBA")
gold_text(img,(W/2,206),"WHO WAS DOTTY?",A(112))
photo(img,S34,(27,178,990,805),(60,262,960,586))
d=ImageDraw.Draw(img,"RGBA")
credit(d,"Photo: © Ashish Tirkey / Pugdundee Safaris",y=884,x=W-60,anchor="rs")
rows=[("BORN","c. 2012, Magadhi zone"),("MOTHER","Sukhi Patiha"),("SISTER","Spotty"),("NAMED FOR","The \"D\" on her forehead")]
y=975
for k,v in rows:
    d.rounded_rectangle((60,y-58,W-60,y+22),radius=18,fill=(16,12,8,170),outline=GOLD+(90,),width=2)
    txt(d,(96,y),k,B(36),GOLD,255,"ls"); txt(d,(W-96,y),v,A(44),CREAM,255,"rs"); y+=100
txt(d,(W/2,1360),"Family details from safari records, not official.",BM(28),GREY,230)
chrome(img,2); save(img,2)

# 3 LIFE TIMELINE
img=stripes(W,H,13); d=ImageDraw.Draw(img,"RGBA")
txt(d,(W/2,180),"PUSHED OUT BY",B(60),CREAM)
gold_text(img,(W/2,320),"HER OWN DAUGHTERS",A(118))
d=ImageDraw.Draw(img,"RGBA")
steps=[("c. 2012","Born in Magadhi zone",GOLD),("MAGADHI","Raised her litters here",GOLD),("THE TWIST","Her grown daughters took over",RED),("TALA ZONE","She moved, and started again",CYAN),("c. 2025","A mother again: 2 cubs",AMB)]
x0=200; y=470
d.line((x0,y,x0,y+4*190),fill=GOLD+(120,),width=4)
for k,(a,b,c) in enumerate(steps):
    yy=y+k*190
    d.ellipse((x0-24,yy-24,x0+24,yy+24),fill=c+(255,),outline=CREAM+(255,),width=4)
    txt(d,(x0+60,yy-6),a,A(54),c,255,"ls"); txt(d,(x0+60,yy+44),b,B(42),CREAM,240,"ls")
txt(d,(W/2,1360),"The jungle's oldest rule: territory goes to the strongest.",BM(30),GREY,230)
chrome(img,3); save(img,3)

# 4 LEGACY / FAMILY TREE
img=stripes(W,H,14); d=ImageDraw.Draw(img,"RGBA")
txt(d,(W/2,180),"HER BLOODLINE",B(60),CREAM)
gold_text(img,(W/2,320),"STILL RULES",A(140))
d=ImageDraw.Draw(img,"RGBA")
def node(cx,cy,l,s,col=GOLD,w=320,h=110):
    d.rounded_rectangle((cx-w/2,cy-h/2,cx+w/2,cy+h/2),radius=22,fill=(16,12,8,225),outline=col+(255,),width=3)
    txt(d,(cx,cy+(0 if s else 16)),l,A(46),CREAM); 
    if s: txt(d,(cx,cy+40),s,B(28),col)
def ln(a,b): d.line((a,b),fill=GOLD+(150,),width=4)
node(540,450,"SUKHI PATIHA","MOTHER")
ln((540,505),(540,600)); ln((300,600),(780,600)); ln((300,600),(300,640)); ln((780,600),(780,640))
node(300,695,"DOTTY","THE \"D\" TIGRESS",AMB); node(780,695,"SPOTTY","HER SISTER")
ln((300,750),(300,840)); ln((180,840),(900,840))
for x in (180,540,900): ln((x,840),(x,890))
node(180,950,"D1","REPORTED SON",GOLD,280); node(540,950,"DAUGHTERS","TOOK MAGADHI",CYAN,280); node(900,950,"2 CUBS","BORN c. 2025",AMB,280)
d.rounded_rectangle((90,1090,W-90,1240),radius=24,fill=(16,12,8,200),outline=GOLD+(110,),width=2)
txt(d,(W/2,1150),"D1 IS NOW CALLED THE",B(40),GOLD); txt(d,(W/2,1210),"KING OF KHITAULI",A(56),CREAM)
txt(d,(W/2,1360),"Lineage as reported in safari records, not official.",BM(30),GREY,230)
chrome(img,4); save(img,4)

# 5 THE NEWS
img=stripes(W,H,15); d=ImageDraw.Draw(img,"RGBA")
txt(d,(W/2,180),"THE DAY BANDHAVGARH WENT QUIET",B(52),CREAM)
gold_text(img,(W/2,320),"9 OCTOBER 2026",A(124))
cs=S31.crop((0,0,1037,560)); card(img,cs,W/2,600,0.82,2.2)
d=ImageDraw.Draw(img,"RGBA")
facts=[("WHERE","Majhkheta beat, Manpur buffer"),("FOUND","During an elephant patrol"),("AGE","About 14 years"),("CAUSE","Natural, as per preliminary exam")]
y=940
for k,v in facts:
    txt(d,(90,y),k,B(36),GOLD,255,"ls"); txt(d,(W-90,y),v,A(42),CREAM,255,"rs")
    d.line((90,y+24,W-90,y+24),fill=GOLD+(60,),width=2); y+=92
txt(d,(W/2,1330),"Samples sent for testing. Field Director, as reported.",BM(30),GREY,230)
credit(d,"Screenshot: The Hans India, 11 Oct 2026",y=H-46)
chrome(img,5); save(img,5)

# 6 CUBS
img=stripes(W,H,16); d=ImageDraw.Draw(img,"RGBA")
gold_text(img,(W/2,250),"TWO CUBS",A(150))
d=ImageDraw.Draw(img,"RGBA")
txt(d,(W/2,326),"LEFT BEHIND",B(64),CREAM)
cs=S33.crop((0,0,845,190)); card(img,cs,W/2,480,1.12,-1.6)
d=ImageDraw.Draw(img,"RGBA")
# bar: cub dependence 0..24 months
bx0,bx1,by=110,970,760
txt(d,(W/2,650),"HOW LONG CUBS STAY WITH MOM",B(42),GOLD)
d.rounded_rectangle((bx0,by-22,bx1,by+22),radius=22,fill=(255,255,255,30))
X=lambda m:bx0+(bx1-bx0)*m/24
d.rounded_rectangle((X(18),by-22,X(24),by+22),radius=22,fill=CYAN+(150,))
d.rounded_rectangle((bx0,by-22,X(15.5),by+22),radius=22,fill=AMB+(235,))
for m in (0,6,12,18,24): txt(d,(X(m),by+66),f"{m}",B(32),GREY)
txt(d,(W/2,by+110),"MONTHS",B(28),GREY)
d.line((X(15.5),by-60,X(15.5),by+30),fill=CREAM+(255,),width=4)
txt(d,(X(15.5),by-72),"DOTTY'S CUBS: 15-16 MONTHS",B(34),CREAM)
txt(d,(X(21),by+8),"USUAL 18-24",B(28),INK,255,"mm")
d.rounded_rectangle((90,980,W-90,1210),radius=26,fill=(16,12,8,200),outline=CYAN+(160,),width=3)
txt(d,(W/2,1060),"MONTHS SHORT OF INDEPENDENCE",A(56),CREAM)
txt(d,(W/2,1130),"The forest department is monitoring them.",B(40),CYAN)
txt(d,(W/2,1180),"Cub age as reported. 18-24 months is the usual range.",BM(28),GREY)
credit(d,"Screenshot: Hindi news report, 10 Oct 2026",y=H-46)
chrome(img,6); save(img,6)

# 7 14 YEARS
img=stripes(W,H,17); d=ImageDraw.Draw(img,"RGBA")
txt(d,(W/2,180),"WHY 14 IS A FULL LIFE",B(60),CREAM)
photo(img,P31,(0,0,820,490),(60,230,960,574),border=AMB)
d=ImageDraw.Draw(img,"RGBA")
credit(d,"Photo: NBT, as published by The Hans India",y=840,x=W-60,anchor="rs")
gold_text(img,(W/2,1010),"14 YEARS",A(140))
d=ImageDraw.Draw(img,"RGBA")
bx0,bx1,by=110,970,1110; X=lambda y_:bx0+(bx1-bx0)*(y_-0)/18
d.rounded_rectangle((bx0,by-18,bx1,by+18),radius=18,fill=(255,255,255,30))
d.rounded_rectangle((X(10),by-18,X(15),by+18),radius=18,fill=GOLD+(120,))
d.ellipse((X(14)-20,by-20,X(14)+20,by+20),fill=AMB+(255,),outline=CREAM+(255,),width=4)
for v in (0,5,10,15,18): txt(d,(X(v),by+58),f"{v}",B(30),GREY)
txt(d,(X(12.5),by-34),"MOST WILD TIGERS: 10-15 YRS",B(30),GOLD)
txt(d,(W/2,1260),"Two zones. Many litters. A bloodline that still rules.",B(40),CREAM)
txt(d,(W/2,1310),"Wild lifespan: general estimate.",BM(28),GREY)
chrome(img,7); save(img,7)

# 8 CTA
img=stripes(W,H,18); d=ImageDraw.Draw(img,"RGBA")
# circular portrait
box=(381,262,591,472); r=300
ph=S34.crop(box).resize((2*r,2*r),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,80,2)).convert("RGBA")
mk=Image.new("L",(2*r,2*r),0); ImageDraw.Draw(mk).ellipse((0,0,2*r-1,2*r-1),fill=255); ph.putalpha(mk)
img.alpha_composite(ph,(W//2-r,140)); d=ImageDraw.Draw(img,"RGBA")
d.ellipse((W//2-r-4,136,W//2+r+4,140+2*r+4),outline=AMB+(255,),width=5)
gold_text(img,(W/2,880),"DID YOU EVER",A(110)); gold_text(img,(W/2,990),"SEE DOTTY?",A(110))
d=ImageDraw.Draw(img,"RGBA")
d.rounded_rectangle((W/2-330,1040,W/2+330,1136),radius=48,fill=GOLD+(245,))
txt(d,(W/2,1106),"COMMENT \"DOTTY\" + YOUR MEMORY",B(42),INK)
cl=["Photos: © Ashish Tirkey / Pugdundee Safaris; NBT via The Hans India.","Screenshots: The Hans India; Hindi news report.","Images belong to their respective owners. DM for credit or removal.","With respect to every photographer who documented her."]
y=1220
for s in cl: txt(d,(W/2,y),s,BM(28),GREY,235); y+=40
chrome(img,8,swipe=False); save(img,8)
