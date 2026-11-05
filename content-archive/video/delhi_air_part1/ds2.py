import sys; sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/delhi')
from ds import *
import ds
TOTAL2=86.0
def multi(lay,y,pieces,font,a=1.0,sw=8,x0=None):
    tot=sum(font.getlength(p) for p,_ in pieces); x=(W-tot)/2 if x0 is None else x0
    for p,c in pieces:
        lay.t((x,y),p,font,c,a,anchor='lm',sw=sw); x+=font.getlength(p)
def pill(lay,y,txt,col,a=1.0,font=None):
    font=font or BC(40); w=font.getlength(txt)+60; x0=(W-w)/2
    lay.d.rounded_rectangle((x0,y-34,x0+w,y+34),radius=34,fill=(10,16,14,int(235*cl(a))),outline=tuple(col)+(int(255*cl(a)),),width=4)
    lay.d.text((W/2,y),txt,font=font,fill=tuple(col)+(int(255*cl(a)),),anchor='mm')
def zoomf(fr,s,blur=0):
    if abs(s-1)>1e-3: M=cv2.getRotationMatrix2D((W/2,H/2),0,s); fr=cv2.warpAffine(fr,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    if blur>1:
        k=int(blur)|1; ker=np.zeros((1,k),np.float32); ker[0,:]=1.0/k; fr=cv2.filter2D(fr,-1,ker)
    return fr
def punch(t,times,amp=0.10):
    s=1.0
    for tp in times:
        d=t-tp
        if 0<=d<0.55: s=max(s,1+amp*math.exp(-d*7.5))
    return s
def card_bg(t,kind):
    if kind=='air':
        fr=world(t,0.95)*0.5; pt=particles(t,200,5,0.8,None); return fr*(1-pt[...,None]*0.6)+np.array((205,170,110),np.float32)*pt[...,None]*0.6
    if kind=='water':
        fr=grad((22,28,32),(36,46,44)).copy(); ys=np.arange(H,dtype=np.float32)[:,None]; xs=np.arange(W,dtype=np.float32)[None,:]
        rip=np.sin(xs*0.02+ys*0.07-t*2.0)+np.sin(xs*0.05-ys*0.04+t*1.3); fr+=rip[...,None]*np.array((6,14,14),np.float32)
        r=np.random.default_rng(9); n=160; f=np.zeros((H,W),np.float32)
        for i in range(n): cv2.circle(f,(int((r.random()*W+t*r.uniform(20,60))%W),int((r.random()*H+t*r.uniform(40,120))%H)),int(r.uniform(5,20)),1.0,-1,cv2.LINE_AA)
        f=cv2.GaussianBlur(f,(0,0),2)*0.45; return fr*(1-f[...,None])+np.array((240,240,236),np.float32)*f[...,None]
    fr=grad((12,16,20),(20,24,28)).copy(); gx=np.arange(W)[None,:]; fr+=((gx%90)<2).astype(np.float32)[...,None]*8; return fr
def stat_card(t,t0,kind,tag,big,bigcol,pieces,pillt,pillcol,sub=None):
    st=t-t0; fr=card_bg(t,kind); lay=L()
    lay.t((W//2,330),tag,BC(54),ACC,eo3(seg(st,0.0,0.3)),anchor='mm',sw=6)
    k=eob(seg(st,0.05,0.5),2.2); sz=int(380*max(0.05,k))
    lay.t((W//2,760),big,AN(sz),bigcol,min(1,k*1.5),anchor='mm',sw=14)
    multi(lay,1040,pieces[0],BC(76),eo3(seg(st,0.4,0.8)),8)
    if len(pieces)>1: multi(lay,1130,pieces[1],BC(76),eo3(seg(st,0.6,1.0)),8)
    pill(lay,1290,pillt,pillcol,eo3(seg(st,1.0,1.4)))
    if sub: lay.t((W//2,1370),sub,BM(34),(225,225,225),eo3(seg(st,1.2,1.6)),anchor='mm',sw=0,shadow=False)
    return composite(fr,lay)
def chapter(t,t0,num,name,col=ACC):
    st=t-t0; fr=grad((8,12,10),(18,22,20)).copy()
    R=((np.arange(W)[None,:]-W/2)**2+(np.arange(H)[:,None]-H*0.42)**2).astype(np.float32); fr+=np.exp(-R/(2*380**2))[...,None]*np.array(col,np.float32)*0.28
    lay=L(); k=eob(seg(st,0.0,0.4),2.0)
    lay.t((W//2,720),num,AN(560*max(0.2,k)),col,min(1,k*1.4),anchor='mm',sw=16)
    lay.d.rectangle((W//2-170,1020,W//2+170,1030),fill=col+(int(255*eo3(seg(st,0.3,0.6))),))
    lay.t((W//2,1130),name,AN(112),WHT,eo3(seg(st,0.35,0.75)),anchor='mm',sw=10)
    return composite(fr,lay)
# ---- beats
def air_a(t):
    st=t-20.3; fr=world(t,0.95)*0.62
    pt=particles(t,260,5,0.9,None); fr=fr*(1-pt[...,None]*0.7)+np.array((205,170,110),np.float32)*pt[...,None]*0.7
    m=np.zeros((H,W),np.uint8); bigbird(m,W//2+int(math.sin(t*0.7)*30),700+int(math.sin(t*1.3)*14),400,t*5.0); fr=apply_mask(fr,m.astype(np.float32)/255*0.92)
    lay=L(); lay.t((60,210),"WHAT SMOG",AN(130),CREAM,eo3(seg(st,0.1,0.5)),sw=10); lay.t((60,350),"DOES TO BIRDS",AN(130),ACC,eo3(seg(st,0.3,0.7)),sw=10)
    return composite(fr,lay)
def water_a(t):
    st=t-33.3; fr=card_bg(t,'water'); lay=L()
    lay.t((60,300),"THEN THE",AN(130),CREAM,eo3(seg(st,0.1,0.5)),sw=10); lay.t((60,450),"WATER",AN(230),TEAL,eo3(seg(st,0.3,0.7)),sw=12)
    lay.t((60,1250),"FOAM. DETERGENT. SEWAGE.",AN(80),WHT,eo3(seg(st,1.0,1.4)),sw=9)
    return composite(fr,lay)
def cpca(t):
    st=t-40.5; fr=card_bg(t,'water'); lay=L()
    lay.t((W//2,330),"CPCB TEST, 2018",BC(54),ACC,eo3(seg(st,0.0,0.3)),anchor='mm',sw=6)
    n=int(17*ease(seg(st,0.3,1.6)))
    for i in range(17):
        cx=110+(i%6)*170; cy=620+(i//6)*170; on=i<13; vis=i<n
        if vis: lay.d.ellipse((cx-52,cy-52,cx+52,cy+52),fill=((235,60,50) if on else (90,110,100))+(255,),outline=WHT+(255,),width=5)
    k=eob(seg(st,1.6,2.1),2.0); lay.t((W//2,1190),"13 OF 17",AN(int(220*max(0.05,k))),RED,min(1,k*1.5),anchor='mm',sw=12)
    multi(lay,1370,[("SPOTS: AMMONIA ABOVE THE ",WHT),("SAFE LIMIT",ACC)],BC(58),eo3(seg(st,2.0,2.4)),7)
    pill(lay,1470,"HARYANA TO DELHI",TEAL,eo3(seg(st,2.4,2.8)))
    return composite(fr,lay)
def countA(t):
    return countbars(t,46.3,"NAJAFGARH JHEEL",27673,"2021",10592,"2022","Species: 81 to 71. Flamingos: 100 to 500 a day, to one.",0.2)
def countB(t):
    return countbars(t,55.0,"SULTANPUR",9026,"2023",2686,"2024","Species: 51 to 43. (Haryana forest dept says its totals rose.)",0.2)
def countbars(t,t0,name,a,al,b,bl,note,delay):
    st=t-t0; fr=card_bg(t,'count'); lay=L()
    lay.t((W//2,300),"ASIAN WATERBIRD CENSUS",BC(54),ACC,eo3(seg(st,0.0,0.3)),anchor='mm',sw=6)
    lay.t((W//2,420),name,AN(130),CREAM,eo3(seg(st,0.1,0.5)),anchor='mm',sw=10)
    sc=800/a; va=a*ease(seg(st,0.4,1.4)); lay.d.rounded_rectangle((60,560,60+max(8,va*sc),680),radius=18,fill=(120,220,90,255))
    lay.t((72,620),al,BC(52),(8,12,10),1.0,anchor='lm',sw=0,shadow=False); lay.t((60+max(8,va*sc)+(-12 if va*sc>500 else 14),620),f"{int(va):,}",AN(70),(8,12,10) if va*sc>500 else WHT,1.0,anchor='rm' if va*sc>500 else 'lm',sw=0 if va*sc>500 else 5,shadow=False)
    kb=eo3(seg(st,2.0,2.4))
    if kb>0:
        vb=a-(a-b)*ease(seg(st,2.2,3.4)); lay.d.rounded_rectangle((60,720,60+max(8,vb*sc),840),radius=18,fill=(235,60,50,int(255*kb)))
        lay.t((72,780),bl,BC(52),WHT,kb,anchor='lm',sw=0,shadow=False); lay.t((60+max(8,vb*sc)+14,780),f"{int(vb):,}",AN(70),WHT,kb,anchor='lm',sw=5)
    pc=int(round((1-b/a)*100)); kp=eob(seg(st,3.4,3.9),2.2)
    if kp>0: lay.t((W//2,1130),f"-{pc}%",AN(int(380*max(0.05,min(1,kp)))),RED,min(1,kp*1.5),anchor='mm',sw=16)
    lay.t((W//2,1400),note,BM(36),(225,225,225),eo3(seg(st,4.0,4.5)),anchor='mm',sw=0,shadow=False)
    return composite(fr,lay)
def notair(t):
    st=t-65.3; fr=world(t,0.8)*0.5; pt=particles(t,140,6,0.6,None); fr=fr*(1-pt[...,None]*0.5)+np.array((200,165,105),np.float32)*pt[...,None]*0.5
    lay=L(); lay.t((60,210),"BUT IT IS NOT",AN(110),CREAM,eo3(seg(st,0.1,0.5)),sw=9); lay.t((60,335),"ONLY THE AIR.",AN(135),ORG,eo3(seg(st,0.3,0.7)),sw=10)
    chips=[("DRYING WETLANDS",TEAL),("DIRTY WATER",(120,220,90)),("DUST AND BUILDING",AMB),("LATE, WARMER WINTERS",(235,110,110))]
    for i,(c,col) in enumerate(chips):
        k=eob(seg(st,1.0+i*1.1,1.4+i*1.1)); 
        if k>0: lay.chip((60,640+i*165),c,BC(64),col,min(1,k),pad=34)
    lay.t((60,1400),"EXPERTS STILL DEBATE HOW MUCH",BC(54),CREAM,eo3(seg(st,6.0,6.5)),sw=6); lay.t((60,1465),"IS THE AIR ALONE.",BC(54),ACC,eo3(seg(st,6.4,6.9)),sw=6)
    return composite(fr,lay)
def close(t):
    st=t-76.0; haze=0.9-0.8*ease(seg(st,0.8,6.5)); fr=world(t,haze)
    fr=apply_mask(fr,flock(t,15,ease(seg(st,1.5,3.0)),560,110,28,seed=8))
    lay=L(); lay.t((60,260),"PROTECT",AN(150),CREAM,eo3(seg(st,0.2,0.6)),sw=11); lay.t((60,430),"THE WETLANDS.",AN(150),ACC,eo3(seg(st,0.5,0.9)),sw=11)
    lay.t((60,640),"THEY CLEAN THE CITY TOO.",BC(66),WHT,eo3(seg(st,1.1,1.5)),sw=7)
    lay.t((60,1280),"DELHI'S AIR",AN(88),CREAM,eo3(seg(st,3.2,3.6)),sw=9); lay.t((60,1380),"PART 1 OF 3",AN(88),ORG,eo3(seg(st,3.5,3.9)),sw=9)
    lay.t((60,1500),"Sources in the caption.",BM(36),(230,230,230),eo3(seg(st,4.6,5.0)),sw=0,shadow=False); lay.t((60,1575),"@thenaturalangle",BC(54),WHT,eo3(seg(st,5.2,5.6)),sw=6)
    return composite(fr,lay)
# beat table: (t0,t1,fn,punch_times)
BEATS=[(0,8,ds.s1,[3.3,5.3,5.9,7.3]),
 (8,19,lambda t:ds.s2(t+1.0),[9.6,10.7,11.8,12.9,16.8]),
 (19,20.3,lambda t:chapter(t,19,"01","THE AIR"),[]),
 (20.3,23.8,air_a,[20.4]),
 (23.8,26.8,lambda t:stat_card(t,23.8,'air',"EVIDENCE 1 OF 3","LUNGS",ORG,[[("FINE PARTICLES CAN ",WHT),("INFLAME",ACC)],[("BIRD LUNGS",WHT)]],"RESEARCH REVIEW, 2025",ORG),[23.9]),
 (26.8,29.8,lambda t:stat_card(t,26.8,'air',"EVIDENCE 2 OF 3","~25",ORG,[[("BIRDS WITH ",WHT),("WATERY EYES",ACC)],[("IN A FEW WEEKS",WHT)]],"ONE EAST DELHI CLINIC, DEC 2025",ORG,"Not a census."),[26.9]),
 (29.8,32.0,lambda t:stat_card(t,29.8,'air',"EVIDENCE 3 OF 3","LINK",ORG,[[("WORSE AIR, ",WHT),("FEWER SPECIES",ACC)]],"HARYANA STUDY, 2019 TO 2022",ORG,"A link, not proof of cause."),[29.9]),
 (32,33.3,lambda t:chapter(t,32,"02","THE WATER",TEAL),[]),
 (33.3,36.5,water_a,[33.4]),
 (36.5,40.5,lambda t:stat_card(t,36.5,'water',"YAMUNA, DELHI","22 KM",TEAL,[[("MOST POLLUTED OF ",WHT),("INDIA'S 311",ACC)],[("POLLUTED RIVER STRETCHES",WHT)]],"CEEW",TEAL),[36.6]),
 (40.5,45.0,cpca,[40.6,42.2]),
 (45,46.3,lambda t:chapter(t,45,"03","THE COUNT",ACC),[]),
 (46.3,55.0,countA,[46.7,49.7]),
 (55.0,64.0,countB,[55.4,58.4]),
 (64,65.3,lambda t:chapter(t,64,"04","NOT ONLY AIR",ORG),[]),
 (65.3,76,notair,[66.3,67.4,68.5,69.6]),
 (76,86,close,[76.2,79.2,79.5])]
WHIPS=[19,32,45,64]
def frame2(i):
    t=min(i/FPS,TOTAL2-1e-3)
    for a,b,f,pk in BEATS:
        if a<=t<b:
            fr=f(t).astype(np.float32)
            s=punch(t,pk)*(1+0.03*(t-a)/(b-a))
            bl=0
            for w in WHIPS:
                if w<=t<w+0.22: u=1-(t-w)/0.22; s*=1+0.5*u*u; bl=max(bl,45*u*u)
                if w+1.3-0.2<=t<w+1.3: u=(t-(w+1.3-0.2))/0.2; s*=1+0.5*u*u; bl=max(bl,45*u*u)
                if w+1.3<=t<w+1.5: u=1-(t-(w+1.3))/0.2; s*=1+0.25*u*u; bl=max(bl,25*u*u)
            if a==0 and t<0.3: fr=fr*seg(t,0,0.3)
            return np.clip(zoomf(fr,s,bl),0,255).astype(np.uint8)
    return np.zeros((H,W,3),np.uint8)
