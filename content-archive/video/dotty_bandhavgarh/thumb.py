import sys; sys.path.insert(0,'.')
from scenes_dt import *
Wt,Ht=1280,720
bg=cv2.resize(STR[200:200+760,0:1200],(Wt,Ht))*0.8
yy2,xx2=np.mgrid[0:Ht,0:Wt]
g=np.exp(-(((xx2-330)/330.0)**2+((yy2-380)/300.0)**2))[...,None]
bg=bg*(1+g*1.3)
img=Image.fromarray(np.clip(bg,0,255).astype(np.uint8)).convert("RGBA")
D=Image.new("L",(Wt,Ht),0); dd=ImageDraw.Draw(D); dd.text((330,610),"D",font=F("Anton-Regular.ttf",560),fill=255,anchor="ms")
Dm=np.array(D).astype(np.float32)/255; Dg=cv2.GaussianBlur(Dm,(0,0),30)
arr=np.array(img).astype(np.float32); arr[...,:3]=np.clip(arr[...,:3]+Dg[...,None]*np.array(AMB)*1.4+Dm[...,None]*np.array((255,214,150))*0.9,0,255)
img=Image.fromarray(arr.astype(np.uint8)); d=ImageDraw.Draw(img,"RGBA")
m=Image.new("L",(Wt,Ht),0); dm=ImageDraw.Draw(m); dm.text((920,330),"DOTTY",font=F("Anton-Regular.ttf",230),fill=255,anchor="ms")
mm=np.array(m).astype(np.float32)[...,None]/255; tex=cv2.resize(TEX,(Wt,Ht))
arr=np.array(img).astype(np.float32); sh=cv2.GaussianBlur(np.roll(np.roll(mm[...,0],8,0),6,1),(0,0),8)[...,None]
arr[...,:3]=arr[...,:3]*(1-sh*0.7); arr[...,:3]=arr[...,:3]*(1-mm)+tex*mm
img=Image.fromarray(arr.astype(np.uint8)).convert("RGBA"); d=ImageDraw.Draw(img,"RGBA")
d.text((920,420),"BANDHAVGARH'S \"D\" TIGRESS",font=F("BarlowCondensed-SemiBold.ttf",52),fill=CREAM+(255,),anchor="ms")
d.rounded_rectangle((690,470,1150,550),radius=40,fill=(16,12,8,230),outline=GOLD+(255,),width=3)
d.text((920,527),"2 CUBS LEFT BEHIND",font=F("Anton-Regular.ttf",50),fill=GOLD+(255,),anchor="ms")
d.text((920,610),"c. 2012 TO 2026",font=F("BarlowCondensed-SemiBold.ttf",40),fill=GREY+(255,),anchor="ms")
out=np.array(img)[...,:3].astype(np.float32)
v=(1-0.45*(((xx2-Wt/2)/(Wt/2))**2*0.5+((yy2-Ht/2)/(Ht/2))**2*0.8)).clip(0.4,1)[...,None]
Image.fromarray(np.clip(out*v,0,255).astype(np.uint8)).save('YT_Dotty_thumb.jpg',quality=93)
