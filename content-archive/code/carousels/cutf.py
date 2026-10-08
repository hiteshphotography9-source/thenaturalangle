from rembg import remove, new_session
from PIL import Image
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
FL=["64a42d44","b1208e85","26726f42","dc158818","f02d75ca","4dec5138","35021122"]
s=new_session("isnet-general-use")
for i,f in enumerate(FL):
    im=Image.open(U+f+"-image.jpg").convert("RGB")
    out=remove(im,session=s); out.save(f"cutf/{i}.png"); print(i,im.size,flush=True)
