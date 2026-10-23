import sys; sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/disp')
from dscenes import *
a=fb("d1",0.58,0.4,z=1.0,cy=0.5)*np.array((1.06,1.0,0.94),np.float32); img=arr2img(a); scrim(img,1100,1920,0.0,0.93,(8,6,2)); scrim(img,0,300,0.7,0.0,(8,6,2)); brand(img,CREAM,200)
tchip(img,"A TIGER'S JOURNEY",1.0,y=150,col=GOLD)
comp(img,glayer((W/2,1400),"3,000 KM WALKED.",A(112),top=(255,250,240),bot=(255,216,140)),1.0)
comp(img,glayer((W/2,1530),"315 KM IN A LINE.",A(112),top=(255,236,200),bot=GOLD),1.0)
pill(img,(W/2,1670),"THE REAL STORY OF T1-C1",B(44),1.0,fg=INK,bg=GOLD)
img.convert("RGB").save("TigerJourney_cover_portrait.jpg",quality=92)
