import sys; sys.path.insert(0,'.')
from rscenes import *
def make(fn,l1,l2,badge):
    img=jungle(41); brand(img)
    tm=pwin(img,WK,(0,0,984,654),(60,640,960,640),z=1.0,spot=(265,235,200,160),k=1.0,border=RUST)
    d=ImageDraw.Draw(img,"RGBA"); fx,fy=tm(265,235)
    brackets(d,fx-190,fy-165,fx+190,fy+165,EMBER,1.0)
    A1=glayer((W/2,400),l1,A(118)); A2=glayer((W/2,530),l2,A(118)); img.alpha_composite(glow(A1,RUST,24,0.6)); img.alpha_composite(A1); img.alpha_composite(A2)
    d=ImageDraw.Draw(img,"RGBA"); d.rounded_rectangle((W/2-330,1380,W/2+330,1490),radius=55,fill=(10,14,10,235),outline=RUST+(255,),width=4); txt(d,(W/2,1462),badge,A(62),EMBER)
    txt(d,(W/2,1600),"TIGER. LEOPARD. AND THE ONE PEOPLE FORGET.",B(40),CREAM)
    credit(d,"Photo: Wikimedia Commons",y=1296,x=W-60,anchor="rs")
    out=np.array(img)[...,:3].astype(np.float32); Image.fromarray(finish(out,0)).save(fn,quality=94)
make("Dhole_Reel_cover_portrait.jpg","THE PREDATOR","PEOPLE FORGET","THE DHOLE")
