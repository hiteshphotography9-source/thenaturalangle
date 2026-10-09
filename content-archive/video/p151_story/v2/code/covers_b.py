import sys; sys.path.insert(0,'.')
import numpy as np
import scenes151b as S, scenes as B
from scenes151b import *
def mk(name,img,keys,draw,pin='bottom',dim=1.0):
    B.REC=np.zeros((H,W),bool)
    fr=S.shot(img,0.0,keys,dim=dim,shake=0.0,pin=pin)
    draw(fr)
    ov=int((B.REC&B.LASTA).sum()); print(name,"text/subject overlap px:",ov)
    f=cv2.cvtColor(fr,cv2.COLOR_RGB2BGR); cv2.imwrite("cov/"+name,f,[cv2.IMWRITE_JPEG_QUALITY,95]); B.REC=None
def pillB(fr,text,cy,size=40): pill(fr,text,W/2,cy,1.0,fg=(20,16,8),bg=GOLD,size=size)
def T(fr,text,font,fill,cy,glow=None,sw=9): paste(fr,sprite(text,font,fill,sw=sw,glow=glow),W/2,cy,1.0)
def dA(fr):
    gradv(fr,0,620,0.6,0.0); T(fr,"P-151",anton(270),GOLD,300,(255,150,0),13); T(fr,"AND HER CUBS",bcs(86),WHITE,500,None,6); pillB(fr,"PANNA TIGER RESERVE",620)
mk("IG_P151_A.jpg","yawn",[(0,0.5,0.5,0.72)],dA)
def dB(fr):
    gradv(fr,0,620,0.6,0.0); T(fr,"WHO IS",bcs(90),CREAM,170,None,6); T(fr,"P-151?",anton(250),GOLD,350,(255,150,0),12); pillB(fr,"PANNA TIGER RESERVE",610)
mk("IG_P151_B.jpg","two_look",[(0,0.5,0.5,0.72)],dB)
def dC(fr):
    gradv(fr,0,640,0.62,0.0); T(fr,"HER MOTHER DIED.",anton(125),WHITE,200,(0,0,0),9); T(fr,"NEXT DAY,",anton(135),WHITE,350,(0,0,0),9); T(fr,"P-151 WALKED OUT",anton(135),GOLD,500,(255,150,0),9); pillB(fr,"PANNA TIGER RESERVE",625,44)
mk("YT_P151_A.jpg","stretch",[(0,0.5,0.5,0.72)],dC)
def dD(fr):
    gradv(fr,0,640,0.55,0.0); gradv(fr,1450,H,0.0,0.6); T(fr,"P-151",anton(260),GOLD,260,(255,150,0),13); T(fr,"THE FULL STORY",bcs(86),WHITE,1600,None,6); pillB(fr,"PANNA TIGER RESERVE",1740,44)
mk("YT_P151_B.jpg","cub_pair",[(0,0.62,0.5,1.0)],dD)
