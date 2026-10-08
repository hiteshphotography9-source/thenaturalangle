import numpy as np, cv2, pickle, json, math, glob
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
from shapely.geometry import shape, box
from shapely.validation import make_valid
PPD=60; C=math.cos(math.radians(8.5)); LON0,LON1,LAT0,LAT1=60.0,100.0,0.0,30.0
RW=int((LON1-LON0)*PPD*C); RH=int((LAT1-LAT0)*PPD)
BOX=box(LON0-2,LAT0-2,LON1+2,LAT1+2)
def load(f):
    out=[]
    for ft in json.load(open(f))['features']:
        g=make_valid(shape(ft['geometry'])).intersection(BOX)
        geoms=[g] if g.geom_type=='Polygon' else [x for x in getattr(g,'geoms',[]) if x.geom_type=='Polygon']
        for p in geoms:
            a=np.asarray(p.exterior.coords,np.float32)
            if len(a)>3: out.append(a)
    return out
land=load('../land.json'); deep=load('../k200.json')
def rast(rings):
    m=np.zeros((RH,RW),np.uint8)
    for r in rings:
        x=(r[:,0]-LON0)*PPD*C; y=(LAT1-r[:,1])*PPD
        cv2.fillPoly(m,[np.stack([x,y],1).astype(np.int32)],255)
    return m
lm=rast(land); dm=rast(deep)
dl=cv2.distanceTransform((lm==0).astype(np.uint8),cv2.DIST_L2,5); dd=cv2.distanceTransform((dm==0).astype(np.uint8),cv2.DIST_L2,5)
dd=np.where(dd>1e8,1e5,dd).astype(np.float32); dl=dl.astype(np.float32)
D=200*(dl/(dl+dd+1e-3))**1.8; D[lm>0]=0; D[dm>0]=999; D=D.astype(np.float32)
# relief
im=Image.open('NE1_50M_SR_W/NE1_50M_SR_W.tif'); W_,H_=im.size
x0=int((LON0+180)/360*W_); x1=int((LON1+180)/360*W_); y0=int((90-LAT1)/180*H_); y1=int((90-LAT0)/180*H_)
cr=np.array(im.crop((x0,y0,x1,y1)).convert('RGB'))
cr=cv2.resize(cr,(RW,RH),interpolation=cv2.INTER_CUBIC)
hsv=cv2.cvtColor(cr,cv2.COLOR_RGB2HSV).astype(np.float32)
hsv[:,:,1]=np.clip(hsv[:,:,1]*1.9+10,0,255); hsv[:,:,2]=np.clip((hsv[:,:,2]/255)**1.5*255*0.95,0,255)
land_rgb=cv2.cvtColor(hsv.astype(np.uint8),cv2.COLOR_HSV2RGB)
lum=cv2.cvtColor(cr,cv2.COLOR_RGB2GRAY).astype(np.float32)/255
sea_detail=(lum-cv2.GaussianBlur(lum,(0,0),6))   # high-pass relief for seabed texture
pickle.dump(dict(land=land,deep=deep,D=D,lm=lm,land_rgb=land_rgb,sea_detail=sea_detail.astype(np.float32),RW=RW,RH=RH),open('assets.pkl','wb'))
cv2.imwrite('land_rgb.png',cv2.cvtColor(land_rgb,cv2.COLOR_RGB2BGR)); print(RW,RH,len(land),len(deep))
