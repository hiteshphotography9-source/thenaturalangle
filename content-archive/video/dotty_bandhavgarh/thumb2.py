import sys; sys.path.insert(0,'.')
from scenes_dt2 import *
Wt,Ht=1280,720
bg=cv2.resize(STR[200:200+760,0:1200],(Wt,Ht))*0.55
img=Image.fromarray(np.clip(bg,0,255).astype(np.uint8)).convert("RGBA")
img=photo_win(img,P34,(330,178,700,640),(40,40,560,640),1.0,rad=24,border=AMB)
d=ImageDraw.Draw(img,"RGBA")
box=(330,178,700,640); rect=(40,40,560,640); DX,DY=488,338
sx=rect[0]+(DX-box[0])/(box[2]-box[0])*rect[2]; sy=rect[1]+(DY-box[1])/(box[3]-box[1])*rect[3]; rr=40*rect[2]/(box[2]-box[0])
for k_,wid,al in ((1.25,12,120),(1.0,6,255)): d.ellipse((sx-rr*k_,sy-rr*k_,sx+rr*k_,sy+rr*k_),outline=AMB+(al,),width=wid)
m=Image.new("L",(Wt,Ht),0); dm=ImageDraw.Draw(m); dm.text((935,300),"DOTTY",font=F("Anton-Regular.ttf",200),fill=255,anchor="ms")
mm=np.array(m).astype(np.float32)[...,None]/255; tex=cv2.resize(TEX,(Wt,Ht))
arr=np.array(img).astype(np.float32); sh=cv2.GaussianBlur(np.roll(np.roll(mm[...,0],8,0),6,1),(0,0),8)[...,None]
arr[...,:3]=arr[...,:3]*(1-sh*0.7); arr[...,:3]=arr[...,:3]*(1-mm)+tex*mm
img=Image.fromarray(arr.astype(np.uint8)).convert("RGBA"); d=ImageDraw.Draw(img,"RGBA")
d.text((935,385),"BANDHAVGARH'S \"D\" TIGRESS",font=F("BarlowCondensed-SemiBold.ttf",46),fill=CREAM+(255,),anchor="ms")
d.rounded_rectangle((720,425,1150,505),radius=40,fill=(16,12,8,230),outline=GOLD+(255,),width=3)
d.text((935,482),"2 CUBS LEFT BEHIND",font=F("Anton-Regular.ttf",48),fill=GOLD+(255,),anchor="ms")
d.text((935,565),"c. 2012 TO 2026",font=F("BarlowCondensed-SemiBold.ttf",38),fill=GREY+(255,),anchor="ms")
d.text((600,700),"Photo: © Ashish Tirkey / Pugdundee Safaris",font=F("BarlowCondensed-Medium.ttf",20),fill=GREY+(230,),anchor="ls")
img.convert("RGB").save('YT_Dotty_thumb.jpg',quality=93)
