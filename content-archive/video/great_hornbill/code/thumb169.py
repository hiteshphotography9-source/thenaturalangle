import sys; sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/hornbill')
from hscenes import *
FS.load("h1"); Wt,Ht=1280,720
a=view("h1",(0.0,0.15,1.0,0.15+(Ht/Wt)*(1.0)*(5404/3993)),(Wt,Ht),1.0)
img=Image.fromarray(np.clip(a*np.array((1.06,1.0,0.94),np.float32),0,255).astype(np.uint8)).convert("RGBA")
g=np.zeros((Ht,Wt),np.uint8); g[:]=np.clip(np.linspace(235,0,260)[:,None].repeat(Wt,1).max(1,keepdims=True).repeat(1,1) if False else 0,0,255)
ramp=np.clip(np.linspace(225,0,250),0,255).astype(np.uint8); g[:250,:]=ramp[:,None]
ov=Image.new("RGBA",(Wt,Ht),(6,16,12,0)); ov.putalpha(Image.fromarray(g)); img.alpha_composite(ov)
d=ImageDraw.Draw(img,"RGBA")
d.text((50,92),"THIS BIRD CANNOT",font=A(76),fill=(255,250,240,255),anchor="ls")
d.text((50,176),"BUILD ITS OWN HOME.",font=A(76),fill=(255,176,60,255),anchor="ls")
d.rounded_rectangle((860,628,1240,696),radius=34,fill=(255,176,60,255)); d.text((1050,676),"GREAT HORNBILL",font=B(40),fill=(14,16,18,255),anchor="ms")
d.text((50,696),"THE NATURAL ANGLE",font=B(28),fill=(244,238,226,210),anchor="ls")
img.convert("RGB").save("Hornbill_thumbnail_16x9.jpg",quality=92)
