from rembg import remove, new_session
from PIL import Image
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
s=new_session("isnet-general-use")
im=Image.open(U+"364811ee-image.jpg").convert("RGB"); remove(im,session=s).save("tiger/p1_cut.png"); print("ok")
