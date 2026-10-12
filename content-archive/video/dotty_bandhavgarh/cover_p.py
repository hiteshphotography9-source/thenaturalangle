import sys; sys.path.insert(0,'.')
from scenes_dt2 import *
def cover(fn,line2,badge):
    bg=STR[100:100+H,0:W]*0.55
    img=Image.fromarray(np.clip(bg,0,255).astype(np.uint8)).convert("RGBA")
    box=(336,178,636,560); rect=(70,170,940,1060)
    img=photo_win(img,P34,box,rect,1.0,rad=28,border=AMB)
    sc_=rect[2]/(box[2]-box[0]); DX,DY=486,365
    sx=rect[0]+(DX-box[0])*sc_; sy=rect[1]+(DY-box[1])*rect[3]/(box[3]-box[1])
    img=mark(img,sx,sy,40*sc_,22*sc_,1.0,0.3)
    d=ImageDraw.Draw(img,"RGBA")
    ly=rect[1]+70; d.line((sx,sy-22*sc_,sx,ly+14),fill=AMB+(230,),width=3)
    d.rounded_rectangle((sx-170,ly-48,sx+170,ly+14),radius=16,fill=(16,12,8,225),outline=AMB+(255,),width=3)
    d.text((sx,ly-6),"HER \"D\" MARK",font=F("Anton-Regular.ttf",40),fill=CREAM+(255,),anchor="ms")
    d.text((rect[0]+rect[2],rect[1]+rect[3]+32),"Photo: © Ashish Tirkey / Pugdundee Safaris",font=F("BarlowCondensed-Medium.ttf",26),fill=GREY+(235,),anchor="rs")
    m=Image.new("L",(W,H),0); dm=ImageDraw.Draw(m); dm.text((W/2,1560),"DOTTY",font=F("Anton-Regular.ttf",260),fill=255,anchor="ms")
    mm=np.array(m).astype(np.float32)[...,None]/255
    arr=np.array(img).astype(np.float32); shd=cv2.GaussianBlur(np.roll(np.roll(mm[...,0],10,0),8,1),(0,0),10)[...,None]
    arr[...,:3]=arr[...,:3]*(1-shd*0.65); arr[...,:3]=arr[...,:3]*(1-mm)+TEX*mm
    img=Image.fromarray(np.clip(arr,0,255).astype(np.uint8)).convert("RGBA"); d=ImageDraw.Draw(img,"RGBA")
    d.text((W/2,1640),line2,font=F("BarlowCondensed-SemiBold.ttf",54),fill=CREAM+(255,),anchor="ms")
    d.rounded_rectangle((W/2-300,1680,W/2+300,1780),radius=50,fill=(16,12,8,235),outline=GOLD+(255,),width=4)
    d.text((W/2,1750),badge,font=F("Anton-Regular.ttf",60),fill=GOLD+(255,),anchor="ms")
    d.text((W/2,1855),"c. 2012 TO 2026",font=F("BarlowCondensed-SemiBold.ttf",44),fill=GREY+(255,),anchor="ms")
    out=np.array(img)[...,:3].astype(np.float32)*VIG
    Image.fromarray(np.clip(out,0,255).astype(np.uint8)).save(fn,quality=94)
cover('YT_Dotty_cover_portrait.jpg',"BANDHAVGARH'S \"D\" TIGRESS IS GONE","2 CUBS LEFT BEHIND")
cover('IG_cover_Dotty.jpg',"BANDHAVGARH'S \"D\" TIGRESS","2 CUBS LEFT BEHIND")
