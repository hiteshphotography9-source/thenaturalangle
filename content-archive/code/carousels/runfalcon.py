
from ref2 import *
S=[
 (6,"In one falcon nest,",["79%","LIZARD"],"NOT BIRDS.",[("THE STUDY","One breeding pair, watched for a full season in 2019."),("THE PREY","Spiny-tailed lizards were 79% of what the chicks were fed.")],"1/7","slide1.jpg",dict(crop=(0.16,0.0,0.84,0.60),cap=230,s_force=0.87,bird_bottom=1100)),
 (0,"Falcons hunt birds.",["BIRDS","ONLY?"],"NOT QUITE.",[("THE USUAL STORY","Fast aerial chases after doves and small birds."),("ALSO ON THE MENU","Bats, small mammals, lizards and large insects.")],"2/7","slide2.jpg",dict(bh_t=470)),
 (2,"In that same nest,",["16"],"KINDS OF PREY|FED TO FOUR CHICKS",[("INCLUDING","4 reptile species"),("AND","5 mammal species"),("AND","3 bird species")],"3/7","slide3.jpg",dict(bh_t=560)),
 (5,"It hunts",["LOW","AND FAST"],"FROM A PERCH.|OR AT GROUND LEVEL.",[("HOW","From an exposed perch, or in fast, low flight over open ground."),("WHEN IT STOOPS","When the target is a bird.")],"4/7","slide4.jpg",dict(bh_t=330)),
 (4,"Once recorded at",["4,360 M"],"IN LADAKH.",[("USUAL RANGE","Mostly below 1,000 m. Up to 1,980 m in Nepal."),("USUAL HOME","Dry, open country, farmland, villages and cities.")],"5/7","slide5.jpg",dict(bh_t=380)),
 (3,"It does not build one.",["BORROWED","NEST"],"OLD NESTS OF|CROWS AND VULTURES.",[("THE NEST","Takes over old stick nests and adds no material."),("THE SEASON","Eggs are laid from January to April.")],"6/7","slide6.jpg",dict(crop=(0.0,0.02,1.0,0.80),bh_t=540,bird_bottom=1050)),
 (1,"Once India's most common falcon.",["NEAR","THREATENED"],"LOOK TWICE AT|THE NEXT POLE.",[("STATUS","IUCN Near Threatened, with a falling population."),("A TRAPPER'S TOOL","Captured to be used as bait for larger falcons.")],"7/7","slide7.jpg",dict(bh_t=300)),
]
for (idx,lead,lines,sub,facts,cnt,fn,kw) in S:
    print(fn,round(build(idx,lead,lines,sub,facts,cnt,fn,**kw),3),flush=True)
