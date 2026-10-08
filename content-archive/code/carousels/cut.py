from rembg import remove, new_session
from PIL import Image
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
FL=["420b43f0","fbef6e8d","2b628c77","7934ba9e","d9b4f677","a3ed0078","a9b048a2","95e895d5","a8dfbe30","cba82924","4402c392"]
s=new_session("isnet-general-use")
for i,f in enumerate(FL):
    if i==0: continue
    im=Image.open(U+f+"-image.jpg").convert("RGB")
    out=remove(im,session=s)
    out.save(f"cut/{i}.png"); print(i,im.size,flush=True)
