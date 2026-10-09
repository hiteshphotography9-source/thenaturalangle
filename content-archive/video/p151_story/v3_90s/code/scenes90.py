import sys, math
sys.path.insert(0,'.')
import scenes151b as S
from scenes151b import *
from cut90 import SEGS,TOTAL,n2o
_orig=S.S14
def S14b(t):
    if 108.0<=t<110.1:
        fr=S.shot("bts3",t,[(108.0,0.22,0.5,1.0),(110.1,0.30,0.5,1.1)]); gradv(fr,0,600,0.5,0.0); gradv(fr,1450,H,0.0,0.55); motes(fr,t,0.35)
        pill(fr,"BEHIND THE SCENES",W/2,1790,ease(seg(t,108.1,108.5)),size=30,fg=(230,230,230),bg=(14,24,30)); S.B.LASTA=None; return fr
    fr=S.shot("two_look",t,[(110.1,0.5,0.5,0.76),(118.7,0.5,0.5,0.82)],dim=0.85,grade="cold"); gradv(fr,1450,H,0.0,0.6); motes(fr,t,0.3)
    kt(fr,"LESS SPACE.",anton(130),WHITE,W/2,250,t,110.3,hold_end=118.5,sw=9,glow=(0,0,0)); kt(fr,"HARDER SURVIVAL.",anton(105),RED,W/2,380,t,111.5,hold_end=118.5,sw=9,glow=(255,40,30)); return fr
S.SC=[(a,b,(S14b if fn is _orig else fn)) for a,b,fn in S.SC]
S.HITS=[(h,s) for h,s in S.HITS if h!=108.2]+[(110.3,0.6)]
def frame(t):
    o,k=n2o(t); n0,n1,o0,o1=SEGS[k]
    fr=S.frame(o)
    d=t-n0
    if k>0 and d<0.3:
        po=SEGS[k-1][3]-0.02; prev=S.frame(po); u=d/0.3; e=ease(u); L=int(60*math.sin(math.pi*u))
        fr=(S.motionblur_h(prev,L).astype(np.float32)*(1-e)+S.motionblur_h(fr,L).astype(np.float32)*e).astype(np.uint8)
    fade(fr,ease(seg(t,TOTAL-0.9,TOTAL))); return fr
if __name__=="__main__":
    ts=[float(x) for x in sys.argv[2:]]; tiles=[]
    for t in ts:
        f=frame(t); f=cv2.resize(f,(270,480)); cv2.putText(f,f"{t}",(6,24),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,0),2); tiles.append(f)
    cols=8; rows=(len(tiles)+cols-1)//cols; img=np.zeros((rows*480,cols*270,3),np.uint8)
    for i,f in enumerate(tiles): img[(i//cols)*480:(i//cols+1)*480,(i%cols)*270:(i%cols+1)*270]=f
    cv2.imwrite(sys.argv[1],cv2.cvtColor(img,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,88])
