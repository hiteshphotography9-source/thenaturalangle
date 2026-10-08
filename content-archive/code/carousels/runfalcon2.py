
import ref2
from ref2 import *
ref2.OUT="falcon2/"
def bar_post(d,canvas,amask):
    x0,x1,y=64,W-64,1212
    d.text((x0,y-44),"SHARE OF PREY FED TO FOUR CHICKS, ONE NEST, 2019",font=bcs(22),fill=GOLD)
    wl=int((x1-x0)*0.79)
    d.rectangle([x0,y,x0+wl-4,y+58],fill=(226,184,104))
    d.rectangle([x0+wl,y,x1,y+58],fill=(92,90,84))
    d.text((x0+14,y+10),"SPINY-TAILED LIZARD  79%",font=bcs(32),fill=(20,16,8))
    d.text((x0+wl+10,y+16),"15 OTHER KINDS  21%",font=bc(22),fill=(235,232,222))
    d.text((x0,y+76),"Includes 4 reptile, 5 mammal and 3 bird species in total.",font=bar(24),fill=(190,186,176))
def ladder_post(d,canvas,amask):
    lx=1000; ytop,ybot=300,1130; scale=(ybot-ytop)/4360.0
    d.line([(lx,ytop),(lx,ybot)],fill=(150,146,134),width=3)
    marks=[(0,"SEA LEVEL",False),(1000,"1,000 M  USUAL LIMIT",False),(1980,"1,980 M  NEPAL",False),(4360,"4,360 M  LADAKH",True)]
    for m,lab,hi in marks:
        y=ybot-m*scale
        d.ellipse([lx-9,y-9,lx+9,y+9],fill=GOLD if hi else (210,205,194))
        f=bcs(26) if hi else bc(24)
        d.text((lx-24-d.textlength(lab,font=f),y-14),lab,font=f,fill=GOLD if hi else (215,210,198))
S=[
 (6,"In one falcon nest,",["79%","LIZARD"],"NOT BIRDS.",[("THE STUDY","One breeding pair, watched for a full season in 2019."),("THE PREY","Spiny-tailed lizards were 79% of what the chicks were fed.")],"1/8","slide1.jpg",dict(crop=(0.16,0.0,0.84,0.48),cap=230,s_force=1.1,subject_xshift=300)),
 (0,"Falcons hunt birds.",["BIRDS","ONLY?"],"NOT QUITE.",[("THE USUAL STORY","Fast aerial chases after doves and small birds."),("ALSO ON THE MENU","Bats, small mammals, lizards and large insects.")],"2/8","slide2.jpg",dict(bh_t=470)),
 (2,"In that same nest,",["16"],"KINDS OF PREY|FED TO FOUR CHICKS",[],"3/8","slide3.jpg",dict(bh_t=520,post=bar_post,sub_xy=('R',1016,372))),
 (5,"It hunts",["LOW","AND FAST"],"FROM A PERCH.|OR AT GROUND LEVEL.",[("HOW","From an exposed perch, or in fast, low flight over open ground."),("WHEN IT STOOPS","When the target is a bird.")],"4/8","slide4.jpg",dict(bh_t=330)),
 (4,"Once recorded at",["4,360 M"],"IN LADAKH.",[("USUAL RANGE","Mostly below 1,000 m. A resident, not a mountain bird."),("USUAL HOME","Dry, open country, farmland, villages and cities.")],"5/8","slide5.jpg",dict(bh_t=340,cap=225,post=ladder_post,ov=0.2,subject_xshift=120)),
 (3,"It does not build one.",["BORROWED","NEST"],"OLD NESTS OF|CROWS AND VULTURES.",[("THE NEST","Takes over old stick nests, even Egyptian Vulture nests, and adds no material."),("THE SEASON","Eggs are laid from January to April.")],"6/8","slide6.jpg",dict(crop=(0.0,0.02,1.0,0.80),bh_t=540,bird_bottom=1050,sub_xy=('R',1016,420))),
 (1,"A suspected fall of",["20-29%"],"IN ABOUT TEN YEARS.",[("WHAT IS LEFT","10,000 to 19,999 mature birds worldwide."),("WHY","Pesticides, habitat loss, and capture as bait for larger falcons.")],"7/8","slide7.jpg",dict(bh_t=300,cap=300,ov=0.12)),
 (0,"Next time a falcon sits on a pole,",["LOOK","TWICE"],"IT MIGHT BE|A LAGGAR.",[("PROTECTED","Schedule I of India's Wildlife Protection Act."),("YOUR TURN","Where have you seen one? Tell me below.")],"8/8","slide8.jpg",dict(crop=(0.18,0.22,0.82,0.98),bh_t=540,ov=0.3)),
]
for (idx,lead,lines,sub,facts,cnt,fn,kw) in S:
    print(fn,round(build(idx,lead,lines,sub,facts,cnt,fn,**kw),3),flush=True)
