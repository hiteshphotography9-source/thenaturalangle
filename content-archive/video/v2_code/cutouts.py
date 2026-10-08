from PIL import Image
from rembg import remove, new_session
import numpy as np
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
s=new_session("isnet-general-use")
for k in ["a4bcbe52","260a7220","4d5819bf","05008004","ce145a99","0a195c9b","454eb397","4d856e57"]:
    im=Image.open(U+k+"-image.jpg").convert("RGB"); sc=min(1,2400/max(im.size)); im=im.resize((int(im.width*sc),int(im.height*sc)),Image.LANCZOS)
    o=remove(im,session=s); o.save(f"cut_{k}.png"); a=np.array(o)[:,:,3]; print(k,im.size,round((a>128).mean(),3),flush=True)
