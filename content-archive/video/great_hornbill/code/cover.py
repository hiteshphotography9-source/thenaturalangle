import sys; sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/hornbill')
from hscenes import *
a=fb("h3",0.5,0.9,z=1.0,cy=0.45)*np.array((1.04,1.0,0.94),np.float32); img=arr2img(a); scrim(img,1150,1920,0.0,0.92,(4,10,8)); scrim(img,0,300,0.7,0.0,(4,10,8)); brand(img,CREAM,200)
tchip(img,"GREAT HORNBILL",1.0,y=150,col=SUN)
comp(img,glayer((W/2,1440),"IT CANNOT BUILD",A(112),top=(255,250,240),bot=(255,208,120)),1.0)
comp(img,glayer((W/2,1570),"ITS OWN HOME",A(112),top=(255,250,240),bot=(255,208,120)),1.0)
pill(img,(W/2,1700),"THE TREE IS THE STORY",B(44),1.0,fg=INK,bg=SUN)
img.convert("RGB").save("Hornbill_cover_portrait.jpg",quality=92)
