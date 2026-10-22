import sys; sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/s3tiger')
from tscenes import *
a=fb("t5",0.5,0.9,z=1.0)*np.array((1.06,1.0,0.92),np.float32); img=arr2img(a); scrim(img,1180,1920,0.0,0.9,(4,10,8)); scrim(img,0,300,0.7,0.0,(4,10,8)); brand(img,CREAM,200)
d=ImageDraw.Draw(img,"RGBA"); tchip(img,"PILIBHIT TIGER RESERVE",1.0,y=150,col=GOLD2)
comp(img,glayer((W/2,1500),"S3 OF PILIBHIT",A(120),top=(255,250,240),bot=(255,208,120)),1.0)
d=ImageDraw.Draw(img,"RGBA"); txt(d,(W/2,1600),"INDIA'S BIGGEST TIGER?",B(64),CREAM,255); pill(img,(W/2,1710),"WHAT WE ACTUALLY KNOW",B(44),1.0,fg=INK,bg=GOLD2)
img.convert("RGB").save("S3_cover_portrait.jpg",quality=92)
