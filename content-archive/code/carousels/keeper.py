import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import ref2
from ref2 import anton,bc,bcs,bar,barm,corm,TEX,W,H,CREAM,GOLD,BG,wrap_text
SRC=Image.open("/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/fed2e363-image.jpg").convert("RGB")
SW,SH=SRC.size
RED=(206,70,58)
def crop(box,w,h,dim=1.0,sat=1.0):
    x0,y0,x1,y1=[int(box[0]*SW),int(box[1]*SH),int(box[2]*SW),int(box[3]*SH)]
    im=SRC.crop((x0,y0,x1,y1)); s=max(w/im.width,h/im.height)
    im=im.resize((max(w,round(im.width*s)),max(h,round(im.height*s))),Image.LANCZOS)
    l=(im.width-w)//2;t=(im.height-h)//2; im=im.crop((l,t,l+w,t+h))
    if dim!=1.0: im=Image.fromarray((np.array(im).astype(np.float32)*dim).clip(0,255).astype(np.uint8))
    return im
def base(dimfill=0.0):
    return Image.new("RGB",(W,H),BG)
def gold_text(c,xy,t,font,anchor="la"):
    m=Image.new("L",(W,H),0); ImageDraw.Draw(m).text(xy,t,font=font,fill=255,anchor=anchor)
    mn=np.array(m).astype(np.float32)/255
    a=np.array(c).astype(np.float32)
    sh=cv2.GaussianBlur(mn,(0,0),12)*0.5
    a=a*(1-sh[:,:,None]); a=a*(1-mn[:,:,None])+TEX*mn[:,:,None]
    return Image.fromarray(np.clip(a,0,255).astype(np.uint8))
def header(c,i):
    d=ImageDraw.Draw(c); d.text((64,52),"THE NATURAL ANGLE",font=bcs(26),fill=(220,214,200))
    cnt=f"{i}/6"; tw=d.textlength(cnt,font=bcs(26))+44
    d.rounded_rectangle([W-64-tw,38,W-64,86],radius=24,fill=(20,20,18)); d.text((W-64-tw+22,48),cnt,font=bcs(26),fill=CREAM)
def finish(c,name,vig=0.28):
    a=np.array(c).astype(np.float32)
    yy,xx=np.mgrid[0:H,0:W]; d=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
    a*=(1-vig*np.clip(d-0.5,0,1)**1.4)[:,:,None]
    a+=np.random.default_rng(7).normal(0,5.0,(H,W,1))
    Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save("keeper/"+name,quality=95)
def lead(c,xy,t,size=78):
    ImageDraw.Draw(c).text(xy,t,font=corm(size),fill=(236,230,214),anchor="la")
def grad(c,y0,y1,a0,a1):
    a=np.array(c).astype(np.float32); yy=np.arange(H)[:,None]
    t=np.clip((yy-y0)/max(1,(y1-y0)),0,1); al=(a0+(a1-a0)*t)[:,:,None]
    a=a*(1-al)+np.array(BG,np.float32)*al
    return Image.fromarray(a.astype(np.uint8))
def aperture(d,cx,cy,r,col,w=3):
    d.ellipse([cx-r,cy-r,cx+r,cy+r],outline=col,width=w)
    import math
    for k in range(6):
        a=k*math.pi/3
        x1,y1=cx+r*math.cos(a),cy+r*math.sin(a)
        x2,y2=cx+r*0.52*math.cos(a+1.1),cy+r*0.52*math.sin(a+1.1)
        d.line([(x1,y1),(x2,y2)],fill=col,width=w)
def brackets(d,x0,y0,x1,y1,col,L=46,w=4):
    for (x,y,sx,sy) in [(x0,y0,1,1),(x1,y0,-1,1),(x0,y1,1,-1),(x1,y1,-1,-1)]:
        d.line([(x,y),(x+sx*L,y)],fill=col,width=w); d.line([(x,y),(x,y+sy*L)],fill=col,width=w)
def tag(d,x,y,t,fill,fg=(255,255,255),size=22):
    f=bcs(size); tw=d.textlength(t,font=f)+22
    d.rectangle([x,y,x+tw,y+size+14],fill=fill); d.text((x+11,y+5),t,font=f,fill=fg); return tw
def xmark(d,cx,cy,r,w=7,col=RED):
    d.line([(cx-r,cy-r),(cx+r,cy+r)],fill=col,width=w); d.line([(cx-r,cy+r),(cx+r,cy-r)],fill=col,width=w)

# ---------- SLIDE 1
c=base(); ph=crop((0.0,0.0,1.0,1.0),W,H,dim=0.48)
# cover crop aligned to tiger lower: use full image scaled to cover
c=ph; c=grad(c,0,620,0.55,0.0); c=grad(c,1180,H,0.0,0.7)
c=gold_text(c,(64,180),"47 SHOTS",anton(250*0+ 0 or 215))
d=ImageDraw.Draw(c)
lead(c,(66,92),"Wildlife photography,")
# arrow
d.line([(70,470),(250,470)],fill=GOLD,width=8); d.polygon([(268,470),(238,448),(238,492)],fill=GOLD)
c=gold_text(c,(64,520),"1 KEEPER",anton(215))
d=ImageDraw.Draw(c)
d.text((66,1235),"THIS IS WHAT WILDLIFE PHOTOGRAPHY",font=bcs(30),fill=GOLD)
d.text((66,1275),"REALLY LOOKS LIKE.",font=bc(46),fill=(215,210,198))
aperture(d,930,1290,70,(226,184,104),3); d.ellipse([918,1278,942,1302],outline=(226,184,104),width=3)
brackets(d,36,150,W-36,1335,(244,238,226),L=40,w=3)
d.text((W-64-d.textlength("REC  47",font=bcs(24)),1350),"REC  47",font=bcs(24),fill=RED)
header(c,1); finish(c,"slide1.jpg")

# ---------- SLIDE 2 contact sheet
c=base(); c=Image.fromarray(np.full((H,W,3),(14,15,13),np.uint8))
lead(c,(66,108),"You see ONE photograph.",70)
c=gold_text(c,(64,200),"THE 46",anton(150)); d=ImageDraw.Draw(c)
d.text((64,372),"YOU DON'T SEE.",font=bc(70),fill=(205,200,190))
d.text((66,455),"They didn't make the cut.",font=corm(40),fill=(200,194,180))
tiles=[((0.30,0.46,0.85,0.95),"BAD CROP",'x'),((0.45,0.05,0.95,0.50),"NOT THE ONE",'x'),((0.0,0.0,1.0,0.55),"BAD CROP",'x'),
       ((0.33,0.47,0.50,0.58),"TOO TIGHT",'x'),((0.15,0.50,0.60,0.78),"CUT OFF",'x'),((0.0,0.60,1.0,1.0),"BAD CROP",'x'),
       ((0.0,0.30,0.55,1.0),"REJECTED",'x'),((0.20,0.40,0.52,0.70),"NOT THE ONE",'x'),(None,"+ 37 MORE",'m')]
nums=[3,9,14,21,26,31,35,40,47]
tw_,th_,gp=320,236,16; x0=(W-(3*tw_+2*gp))//2; y0=540
for k,(box,lab,kind) in enumerate(tiles):
    x=x0+(k%3)*(tw_+gp); y=y0+(k//3)*(th_+gp)
    if box:
        c.paste(crop(box,tw_,th_,dim=0.62),(x,y)); d=ImageDraw.Draw(c)
        d.rectangle([x,y,x+tw_,y+th_],outline=(60,60,54),width=2)
        xmark(d,x+tw_-34,y+34,16,6); tag(d,x,y+th_-34,lab,(150,40,34),size=20)
        d.text((x+10,y+8),f"#{nums[k]:02d}",font=bcs(22),fill=(235,232,222))
    else:
        d=ImageDraw.Draw(c); d.rectangle([x,y,x+tw_,y+th_],fill=(24,24,21),outline=(60,60,54),width=2)
        d.text((x+tw_/2,y+th_/2-6),"+ 37",font=anton(70),fill=GOLD,anchor="mm"); d.text((x+tw_/2,y+th_/2+46),"MORE FRAMES",font=bcs(24),fill=(190,186,176),anchor="mm")
d.text((64,1330),"ILLUSTRATIVE CROPS OF ONE FRAME",font=bc(20),fill=(120,118,108))
header(c,2); finish(c,"slide2.jpg")

# ---------- SLIDE 3 analysis
c=Image.fromarray(np.full((H,W,3),(14,15,13),np.uint8))
lead(c,(66,98),"Some frames are",70)
c=gold_text(c,(64,176),"ALMOST",anton(170)); d=ImageDraw.Draw(c)
d.text((66,372),"perfect.",font=corm(70),fill=(236,230,214))
bx=(0.0,0.36,1.0,0.95); PW,PH=1080,796; py=490
c.paste(crop(bx,PW,PH),(0,py)); d=ImageDraw.Draw(c)
def P(xf,yf): return (xf*SW/ SW*1080/1.0*(1/1.0)*0+xf*1080, py+(yf-0.36)/(0.95-0.36)*PH)
ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
for t in (1/3,2/3):
    od.line([(t*1080,py),(t*1080,py+PH)],fill=(255,255,255,70),width=2); od.line([(0,py+t*PH),(1080,py+t*PH)],fill=(255,255,255,70),width=2)
c=Image.alpha_composite(c.convert("RGBA"),ov).convert("RGB"); d=ImageDraw.Draw(c)
eye=P(0.41,0.51); brackets(d,eye[0]-34,eye[1]-30,eye[0]+34,eye[1]+30,GOLD,L=16,w=3)
def callout(label,sub,tx,ty,px,py_,right=True):
    d.line([(px,py_),(tx-8 if right else tx+8,ty+16)],fill=GOLD,width=2); d.ellipse([px-6,py_-6,px+6,py_+6],fill=GOLD)
    d.text((tx,ty),label,font=bcs(26),fill=GOLD,anchor="la")
    d.text((tx,ty+32),sub,font=bar(22),fill=CREAM,anchor="la")
callout("COMPOSITION","Tiger low left, trunk leans in.",640,545,P(0.45,0.70)[0],P(0.45,0.70)[1])
callout("SUBJECT","Eye sits near a third.",640,665,eye[0]+40,eye[1])
callout("BACKGROUND","Soft haze. Clean road.",640,785,P(0.12,0.62)[0],P(0.12,0.62)[1])
callout("TIMING","Head turned, mid-sniff.",640,905,P(0.48,0.56)[0],P(0.48,0.56)[1])
c=gold_text(c,(64,1320),"Sharp is not GREAT.",anton(0 or 80)) if False else c
d=ImageDraw.Draw(c); d.text((64,1334),"Sharp doesn't automatically mean GREAT.",font=bcs(40),fill=GOLD)
d.text((64,1384),"Ask: is this the moment I was waiting for?",font=bar(26),fill=(205,200,190))
header(c,3); finish(c,"slide3.jpg")

# ---------- SLIDE 4 burst
c=Image.fromarray(np.full((H,W,3),(14,15,13),np.uint8))
lead(c,(66,98),"Wildlife doesn't give you",66)
c=gold_text(c,(64,184),"UNLIMITED",anton(190)); c=gold_text(c,(64,396),"CHANCES.",anton(190))
d=ImageDraw.Draw(c)
seq=[(0.0,0.20,1.0,0.98),(0.06,0.26,0.96,0.94),(0.12,0.34,0.90,0.92),(0.18,0.40,0.84,0.90),(0.22,0.45,0.78,0.88)]
nm=[41,42,43,44,45]; tw_,th_,gp=320,290,16; x0=(W-(3*tw_+2*gp))//2; y0=690
d.rectangle([x0-14,y0-30,x0+3*tw_+2*gp+14,y0+2*th_+gp+30],fill=(8,8,7))
for k in range(6):
    x=x0+(k%3)*(tw_+gp); y=y0+(k//3)*(th_+gp)
    if k<5:
        c.paste(crop(seq[k],tw_,th_,dim=0.9),(x,y)); d=ImageDraw.Draw(c)
        d.text((x+12,y+10),f"#{nm[k]}",font=anton(34),fill=(244,238,226))
    else:
        d=ImageDraw.Draw(c); d.rectangle([x,y,x+tw_,y+th_],fill=(22,22,19),outline=GOLD,width=3)
        d.text((x+tw_/2,y+th_/2-10),"#46",font=anton(70),fill=GOLD,anchor="mm"); d.text((x+tw_/2,y+th_/2+50),"...ONE MORE",font=bcs(24),fill=(215,210,198),anchor="mm")
    for hx in range(x+8,x+tw_,34): d.rectangle([hx,y-22,hx+14,y-10],fill=(40,40,36)); d.rectangle([hx,y+th_+10,hx+14,y+th_+22],fill=(40,40,36))
d.text((64,1334),"You have to anticipate the moment.",font=bcs(42),fill=GOLD)
d.text((64,1384),"ILLUSTRATIVE CROPS OF ONE FRAME. FRAME NUMBERS TELL THE STORY.",font=bc(20),fill=(120,118,108))
header(c,4); finish(c,"slide4.jpg")

# ---------- SLIDE 5 selection
c=Image.fromarray(np.full((H,W,3),(14,15,13),np.uint8))
lead(c,(66,98),"Then comes",70)
c=gold_text(c,(64,184),"THE HARDEST",anton(135)); c=gold_text(c,(64,328),"PART.",anton(135))
d=ImageDraw.Draw(c)
cells=[((0.30,0.46,0.85,0.95),False),((0.0,0.0,1.0,0.55),False),((0.15,0.50,0.60,0.78),False),((0.06,0.455,0.78,0.875),True)]
tw_,th_,gp=500,310,20; x0=(W-(2*tw_+gp))//2; y0=585
for k,(box,keep) in enumerate(cells):
    x=x0+(k%2)*(tw_+gp); y=y0+(k//2)*(th_+gp)
    c.paste(crop(box,tw_,th_,dim=1.0 if keep else 0.42),(x,y)); d=ImageDraw.Draw(c)
    if keep:
        d.rectangle([x-5,y-5,x+tw_+5,y+th_+5],outline=GOLD,width=6)
        d.rectangle([x,y+th_-52,x+tw_,y+th_],fill=(226,184,104)); d.text((x+16,y+th_-45),"KEEP",font=anton(34),fill=(20,16,8))
        d.line([(x+tw_-70,y+th_-24),(x+tw_-52,y+th_-10),(x+tw_-22,y+th_-42)],fill=(20,16,8),width=7)
    else:
        xmark(d,x+tw_-40,y+40,20,7); d.rectangle([x,y+th_-44,x+tw_,y+th_],fill=(120,34,28)); d.text((x+16,y+th_-38),"REJECT ×",font=bcs(28),fill=(255,255,255))
d.text((64,1268),"The goal isn't more photographs.",font=bcs(36),fill=(205,200,190))
c=gold_text(c,(64,1312),"It's the RIGHT photograph.",anton(66))
header(c,5); finish(c,"slide5.jpg")

# ---------- SLIDE 6 keeper
c=crop((0.0,0.0,1.0,1.0),W,H)
c=grad(c,1180,H,0.0,0.82)
a=np.array(c).astype(np.float32); yy=np.arange(H)[:,None]
t=np.clip((260-yy)/260,0,1)*0.40; a=a*(1-t[:,:,None])+np.array(BG,np.float32)*t[:,:,None]; c=Image.fromarray(a.astype(np.uint8))
c=gold_text(c,(64,62),"FRAME #47",anton(108)); d=ImageDraw.Draw(c)
d.text((66,200),"THE KEEPER.",font=corm(64),fill=(244,238,226))
d.text((64,1268),"Wildlife photography isn't about getting one lucky shot.",font=bar(27),fill=(240,236,226))
d.text((64,1306),"It's about being ready when the moment happens.",font=bar(27),fill=(240,236,226))
d.text((64,1372),"SAVE THIS BEFORE YOUR NEXT SAFARI.",font=bcs(24),fill=GOLD)
d.text((W-64-d.textlength("THE NATURAL ANGLE",font=bcs(22)),1376),"THE NATURAL ANGLE",font=bcs(22),fill=(200,196,184))
finish(c,"slide6.jpg",vig=0.12)
print("done")
