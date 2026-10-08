
from ref import *
N=12
S=[
 (6,"Meet the",["BIRDS","OF THE","ANDAMANS"],"10 BIRDS. 3 FOUND|NOWHERE ELSE.",[],"1/12","slide1.jpg",dict(footer_text="Swipe to meet them.")),
 (10,"Andaman",["SERPENT","EAGLE"],"ENDEMIC TO|THE ANDAMANS",[("HABITAT","Wet evergreen forest in the interior of the larger islands."),("LOOK FOR","Yellow face, dark body with white spots."),("STATUS","Listed Vulnerable and declining.")],"2/12","slide2.jpg",{}),
 (6,"Andaman",["BULBUL"],"ENDEMIC TO|THE ANDAMANS",[("HABITAT","Evergreen forest, forest edge and thick secondary growth."),("LOOK FOR","Olive-yellow body, dark head and a blue eye ring."),("STATUS","Locally common. Eats small fruit.")],"3/12","slide3.jpg",{}),
 (1,"Andaman",["TEAL"],"ENDEMIC TO|THE ANDAMANS",[("HABITAT","Ponds, tidal creeks, mangroves and brackish swamps."),("LOOK FOR","A small brown duck with a white eye ring."),("STATUS","Near Threatened. Wetlands are being reclaimed.")],"4/12","slide4.jpg",dict(xr=(0.62,1.0),bh_t=330)),
 (7,"Long-tailed",["PARAKEET"],"RED CHEEKS.|LONG TAIL.",[("HABITAT","Forests, swamps, mangroves and partly cleared areas."),("LOOK FOR","Red cheek patch and a black stripe along the neck.")],"5/12","slide5.jpg",{}),
 (8,"Oriental",["DOLLARBIRD"],"RED BILL.|BLUE THROAT.",[("HABITAT","Woodland edges, clearings and open country with large trees."),("LOOK FOR","Red bill and blue throat. Perches openly on high branches.")],"6/12","slide6.jpg",dict(bh_t=420)),
 (9,"Collared",["KINGFISHER"],"BLUE BACK.|WHITE COLLAR.",[("HABITAT","Coastal mangroves, tidal flats and sheltered bays."),("LOOK FOR","Blue back, white collar and a heavy dark bill.")],"7/12","slide7.jpg",{}),
 (5,"Forest",["WAGTAIL"],"WINTER|VISITOR",[("HABITAT","Shaded forest, forest paths and clearings."),("LOOK FOR","Two black bands across a white breast. Wags its tail side to side.")],"8/12","slide8.jpg",{}),
 (4,"Eurasian",["WHIMBREL"],"MIGRANT OF|THE MUDFLATS",[("HABITAT","Intertidal mudflats, shores, marshes and flooded fields."),("LOOK FOR","A long down-curved bill and a striped crown.")],"9/12","slide9.jpg",{}),
 (3,"The",["SNIPE"],"A BILL BUILT|FOR MUD",[("HABITAT","Marshes, wet fields and muddy edges."),("LOOK FOR","A very long bill and a striped head. It probes the mud.")],"10/12","slide10.jpg",dict(bh_t=380)),
 (2,"The",["PIPIT"],"OPEN-GROUND|WALKER",[("HABITAT","Open grassy ground, fields and rocks."),("LOOK FOR","Streaked brown body, thin bill and a pale eyebrow.")],"11/12","slide11.jpg",{}),
]
for (idx,lead,lines,sub,facts,cnt,fn,kw) in S:
    print(fn,round(build(idx,lead,lines,sub,facts,cnt,fn,**kw),3),flush=True)

# slide 12 summary
src=Image.open(U+FL[6]+"-image.jpg").convert("RGB")
cov=max(W/src.width,H/src.height); im=src.resize((int(src.width*cov)+1,int(src.height*cov)+1))
im=im.crop(((im.width-W)//2,(im.height-H)//2,(im.width-W)//2+W,(im.height-H)//2+H)).filter(ImageFilter.GaussianBlur(28))
arr=np.array(im).astype(np.float32)*0.45
yy,xx=np.mgrid[0:H,0:W]; dd=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
arr*=(1-0.35*np.clip(dd-0.4,0,1))[:,:,None]
f,size,capH,lh,tb=title_block(["WHERE","TO LOOK"],215)
tm=Image.new("L",(W,H),0); td=ImageDraw.Draw(tm); off=f.getbbox("H")[1]; y0=200; ys=y0-off
for ln in ["WHERE","TO LOOK"]: td.text((64,ys),ln,font=f,fill=255,anchor="la"); ys+=lh
t=np.array(tm).astype(np.float32)/255
arr=arr*(1-(cv2.GaussianBlur(t,(0,0),14)*0.5)[:,:,None]); arr=arr*(1-t[:,:,None])+TEX*t[:,:,None]
c=Image.fromarray(np.clip(arr,0,255).astype(np.uint8)); d=ImageDraw.Draw(c)
d.text((66,y0-106),"In the Andamans",font=corm(78),fill=(236,230,214),anchor="la")
d.text((64,52),"THE NATURAL ANGLE",font=bcs(26),fill=(220,214,200))
tw=d.textlength("12/12",font=bcs(26))+44; d.rounded_rectangle([W-64-tw,38,W-64,86],radius=24,fill=(20,20,18)); d.text((W-64-tw+22,48),"12/12",font=bcs(26),fill=CREAM)
rows=[("FOREST INTERIOR","Andaman Serpent Eagle, Andaman Bulbul, Forest Wagtail"),("FOREST EDGE AND CLEARINGS","Long-tailed Parakeet, Oriental Dollarbird"),("WETLANDS AND MANGROVES","Andaman Teal, Collared Kingfisher"),("MUDFLATS AND SHORES","Eurasian Whimbrel, Snipe"),("OPEN GROUND","Pipit")]
y=y0+tb+70
for lab,v in rows:
    d.line([(64,y),(64,y+88)],fill=(150,146,134),width=2)
    d.text((86,y-2),lab,font=bcs(24),fill=GOLD)
    for j,l in enumerate(wrap_text(d,v,bar(28),900)[:2]): d.text((86,y+30+j*34),l,font=bar(28),fill=CREAM)
    y+=104 if len(wrap_text(d,v,bar(28),900))<2 else 138
d.text((64,1262),"Save this for your Andaman trip.",font=corm(52),fill=GOLD)
d.text((64,1336),"Photographs by Hitesh Chawla  \u00b7  The Natural Angle",font=bar(24),fill=(215,208,192))
a=np.array(c).astype(np.float32)+np.random.default_rng(7).normal(0,5.5,(H,W,1))
Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save(OUT+"slide12.jpg",quality=95)
print("done")
