import json,pickle,numpy as np,cv2
from shapely.geometry import shape, box
from shapely.validation import make_valid
BB=(45,110,-15,45); BOX=box(BB[0],BB[2],BB[1],BB[3])
def load(f):
    out=[]
    for ft in json.load(open(f))['features']:
        g=make_valid(shape(ft['geometry'])).intersection(BOX)
        geoms=[g] if g.geom_type=='Polygon' else [x for x in getattr(g,'geoms',[]) if x.geom_type=='Polygon']
        for p in geoms:
            a=np.asarray(p.exterior.coords,np.float32)
            if len(a)>3: out.append(a)
    return out
land=load('land.json'); deep=load('k200.json')
print(len(land),sum(len(r) for r in land),len(deep),sum(len(r) for r in deep))
# pseudo depth raster
PPD=160; C=np.cos(np.radians(8.5)); LON0,LAT1=76.0,12.0; LAT0,LON1=4.5,84.5
RW=int((LON1-LON0)*PPD*C); RH=int((LAT1-LAT0)*PPD)
def rast(rings):
    m=np.zeros((RH,RW),np.uint8)
    for r in rings:
        if r[:,0].max()<LON0-1 or r[:,0].min()>LON1+1 or r[:,1].max()<LAT0-1 or r[:,1].min()>LAT1+1: continue
        x=(r[:,0]-LON0)*PPD*C; y=(LAT1-r[:,1])*PPD
        cv2.fillPoly(m,[np.stack([x,y],1).astype(np.int32)],255)
    return m
lm=rast(land); dm=rast(deep)
dl=cv2.distanceTransform((lm==0).astype(np.uint8),cv2.DIST_L2,5); dd=cv2.distanceTransform((dm==0).astype(np.uint8),cv2.DIST_L2,5)
D=200*(dl/(dl+dd+1e-3))**1.8; D[lm>0]=0; D[dm>0]=999; D=D.astype(np.float32)
pickle.dump(dict(land=land,deep=deep,D=D,lm=lm,dm=dm),open('geo.pkl','wb'))
cv2.imwrite('Dprev.png',np.clip(D/200*255,0,255).astype(np.uint8))
