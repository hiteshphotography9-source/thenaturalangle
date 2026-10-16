import sys; sys.path.insert(0,'.')
from fscenes import *
img=fb("f9",0.62,0.78,z=1.0); a=arr2img(img*np.array((1.05,0.98,0.9),np.float32))
scrim(a,0,720,0.6,0.0,(30,12,20)); scrim(a,1120,1800,0.0,0.72,(30,12,20)); brand(a,CREAM,170)
comp(a,glayer((W/2,330),"50°C IN THE THAR.",A(112)),1.0); comp(a,glayer((W/2,470),"WHERE DOES IT HIDE?",A(100),top=(255,250,240),bot=(255,214,160)),1.0)
d=ImageDraw.Draw(a,"RGBA"); d.rounded_rectangle((W/2-330,1380,W/2+330,1490),radius=55,fill=(12,14,30,235),outline=AMB+(255,),width=4); txt(d,(W/2,1460),"THE DESERT FOX",A(62),AMB)
txt(d,(W/2,1590),"A NIGHT IN THE THAR",B(40),CREAM)
out=np.array(a)[...,:3].astype(np.float32); Image.fromarray(finish(out,0)).save("DesertFox_cover_portrait.jpg",quality=94)
