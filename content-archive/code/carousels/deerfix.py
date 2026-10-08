import cv2,numpy as np
d=cv2.imread("shot/deer_a.png")
x0,y0,x1,y1=292,1392,790,1489
reg=d[y0:y1,x0:x1].astype(np.float32)
g=cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)
tm=np.zeros(g.shape,np.uint8); tm[y0:y1,x0:x1]=((g[y0:y1,x0:x1]>120)*255)
tm=cv2.dilate(tm,np.ones((7,7),np.uint8))
d1=cv2.inpaint(d,tm,5,cv2.INPAINT_TELEA)
# pill darkening: compare ring just outside vs interior border strip
pm=np.zeros(g.shape,np.float32); cv2.rectangle(pm,(x0+4,y0+4),(x1-4,y1-4),1,-1)
out=np.zeros(g.shape,np.float32); cv2.rectangle(out,(x0-30,y0-30),(x1+30,y1+30),1,-1); cv2.rectangle(out,(x0-4,y0-4),(x1+4,y1+4),0,-1)
gi=cv2.cvtColor(d1,cv2.COLOR_BGR2GRAY).astype(np.float32)
ratio=gi[out>0].mean()/gi[(pm>0)].mean()
print(ratio)
a=d1.astype(np.float32); m=cv2.GaussianBlur((np.zeros(g.shape,np.float32)+0),(0,0),1)
box=np.zeros(g.shape,np.float32); cv2.rectangle(box,(x0-3,y0-3),(x1+3,y1+3),1,-1); box=cv2.GaussianBlur(box,(0,0),6)
gain=1+(ratio-1)*box
a=np.clip(a*gain[:,:,None],0,255).astype(np.uint8)
# avatar
am=np.zeros(g.shape,np.uint8); am[170:460,770:1045]=255
a=cv2.inpaint(a,am,7,cv2.INPAINT_TELEA)
cv2.imwrite("shot/deer_clean2.png",a); cv2.imwrite("shot/dc2_crop.png",a[1300:1560,150:950])
