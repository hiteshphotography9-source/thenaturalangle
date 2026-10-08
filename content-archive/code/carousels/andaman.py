import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
IMG="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/images/"
OUT="/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/andaman/"
W,H=1080,1440
F="/usr/share/fonts/truetype/liberation/"
serif=lambda s:ImageFont.truetype(F+"LiberationSerif-Bold.ttf",s)
serifi=lambda s:ImageFont.truetype(F+"LiberationSerif-Italic.ttf",s)
sans=lambda s:ImageFont.truetype(F+"LiberationSans-Regular.ttf",s)
sansb=lambda s:ImageFont.truetype(F+"LiberationSans-Bold.ttf",s)
CREAM=(244,238,226); ACC=(226,138,52); BG=(12,14,11)

def load(n): return Image.open(IMG+f"{n}.jpg").convert("RGB")
def cover(im,box=None):
    if box: im=im.crop(box)
    s=max(W/im.width,H/im.height)
    im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    l=(im.width-W)//2; t=(im.height-H)//2
    return im.crop((l,t,l+W,t+H))
def grad(canvas,y0,y1,a0,a1):
    arr=np.array(canvas).astype(float)
    ys=np.arange(H)[:,None]
    t=np.clip((ys-y0)/(y1-y0),0,1)
    a=(a0+(a1-a0)*t)[:,:,None]
    arr=arr*(1-a)+np.array(BG)*a
    return Image.fromarray(arr.astype("uint8"))
def vignette(im,strength=0.28):
    arr=np.array(im).astype(float)
    y,x=np.mgrid[0:H,0:W]
    d=np.sqrt(((x-W/2)/(W/2))**2+((y-H/2)/(H/2))**2)
    m=1-strength*np.clip(d-0.5,0,1)**1.5
    return Image.fromarray((arr*m[:,:,None]).clip(0,255).astype("uint8"))
def grain(im,amt=7):
    arr=np.array(im).astype(float)
    n=np.random.default_rng(3).normal(0,amt,(H,W,1))
    return Image.fromarray((arr+n).clip(0,255).astype("uint8"))
def wrap(d,text,font,maxw):
    words=text.split();lines=[];cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur);cur=w
    lines.append(cur);return lines
def text(d,xy,t,font,fill=CREAM,maxw=900,lh=1.16,shadow=True):
    x,y=xy
    for ln in wrap(d,t,font,maxw):
        if shadow: d.text((x+2,y+2),ln,font=font,fill=(0,0,0))
        d.text((x,y),ln,font=font,fill=fill); y+=int(font.size*lh)
    return y
def label(d,xy,t,fill=ACC,size=24):
    f=sansb(size);x,y=xy
    for ch in t:
        d.text((x,y),ch,font=f,fill=fill); x+=d.textlength(ch,font=f)+4
def letter(n,y,box=None):
    im=load(n)
    if box: im=im.crop(box)
    r=W/im.width; im=im.resize((W,round(im.height*r)),Image.LANCZOS)
    c=Image.new("RGB",(W,H),BG); c.paste(im,(0,y)); return c,im.height
def footer(d,i,total=6,swipe=True):
    label(d,(70,H-82),"THE NATURAL ANGLE",CREAM,20)
    d.text((W-70-d.textlength(f"{i} / {total}",font=sans(22)),H-84),f"{i} / {total}",font=sans(22),fill=(170,165,150))
    if swipe and i<total:
        d.line([(W-190,H-120),(W-70,H-120)],fill=ACC,width=3)
        d.polygon([(W-70,H-120),(W-84,H-128),(W-84,H-112)],fill=ACC)
def finish(c,name):
    c=grain(vignette(c)); c.save(OUT+name,quality=95)


U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
FL=["420b43f0","fbef6e8d","2b628c77","7934ba9e","d9b4f677","a3ed0078","a9b048a2","95e895d5","a8dfbe30","cba82924","4402c392"]
def bird(i): return Image.open(U+FL[i]+"-image.jpg").convert("RGB")
def crop_to(im,w,h,cx,cy,zoom=1.0):
    r=w/h
    cw=min(im.width,im.height*r)/zoom; ch=cw/r
    x0=min(max(cx*im.width-cw/2,0),im.width-cw); y0=min(max(cy*im.height-ch/2,0),im.height-ch)
    return im.crop((int(x0),int(y0),int(x0+cw),int(y0+ch))).resize((w,h),Image.LANCZOS)
TOT=12

# S1 hook collage
c=Image.new("RGB",(W,H),BG)
tiles=[(7,.5,.4,1.3),(10,.68,.5,2.3),(1,.76,.55,2.0),(8,.45,.35,1.2),(9,.62,.45,1.8),(6,.62,.55,2.0)]
tw,th,gap=320,420,20; x0=(W-(3*tw+2*gap))//2
for k,(i,cx,cy,z) in enumerate(tiles):
    c.paste(crop_to(bird(i),tw,th,cx,cy,z),(x0+(k%3)*(tw+gap),380+(k//3)*(th+gap)))
d=ImageDraw.Draw(c)
label(d,(70,80),"FIELD GUIDE  ·  BIRDS OF THE ANDAMANS")
text(d,(70,125),"10 birds. 3 found nowhere else on Earth.",serif(60),maxw=940,shadow=False)
text(d,(70,1290),"Swipe to meet them.",serifi(36),fill=ACC,shadow=False)
footer(d,1,TOT); finish(c,"slide1.jpg")

DATA=[
 (10,(.68,.5,1.0),"Andaman Serpent Eagle","Spilornis elgini","ENDEMIC","Closed-canopy wet evergreen forest in the interior of the larger islands.","Yellow face, dark brown body with white spots. Hunts snakes, lizards and rats.","Listed Vulnerable and declining."),
 (6,(.62,.55,1.0),"Andaman Bulbul","Microtarsus fuscoflavescens","ENDEMIC","Evergreen forest, forest edge and thick secondary growth, in the understorey.","Olive-yellow body, dark head, blue eye ring. Usually in pairs, eating small fruit.","Locally common."),
 (1,(.5,.55,1.0),"Andaman Teal","Anas albogularis","ENDEMIC","Freshwater ponds, tidal creeks, mangroves, lagoons and brackish swamps.","A small brown duck with a white eye ring.","Near Threatened. Wetland reclamation is the new threat."),
 (7,(.5,.45,1.0),"Long-tailed Parakeet","Psittacula longicauda",None,"Forests, swamps, mangroves and partly cleared areas.","Red cheek patch and a black stripe along the neck. The tail is long."," "),
 (8,(.45,.45,1.0),"Oriental Dollarbird","Eurystomus orientalis",None,"Woodland edges, clearings and open country with scattered large trees.","Red bill and a blue throat. Perches openly on high branches."," "),
 (9,(.65,.5,1.0),"Collared Kingfisher","Todiramphus chloris",None,"Coastal mangroves, tidal flats and sheltered bays.","Blue back, white collar and a heavy dark bill."," "),
 (5,(.4,.5,1.0),"Forest Wagtail","Dendronanthus indicus","MIGRANT","Shaded forest, forest paths and clearings in winter.","Two black bands across a white breast. Wags its tail from side to side."," "),
 (4,(.38,.5,1.0),"Eurasian Whimbrel","Numenius phaeopus","MIGRANT","Intertidal mudflats, shores, marshes and flooded fields.","Long down-curved bill and a striped crown."," "),
 (3,(.35,.5,1.0),"Snipe","Gallinago sp.","MIGRANT","Marshes, wet fields and muddy edges.","A very long bill and a striped head. It probes the mud."," "),
 (2,(.55,.5,1.0),"Pipit","Anthus sp.",None,"Open, grassy ground, fields and rocks.","Streaked brown body, thin bill, pale eyebrow. Feeds on the ground."," "),
]
pw,ph=940,780
for k,(i,(cx,cy,z),name,sci,tag,hab,look,note) in enumerate(DATA):
    c=Image.new("RGB",(W,H),BG)
    if name=="Andaman Teal":
        b=bird(i); h2=round(pw*b.height/b.width); c.paste(b.resize((pw,h2),Image.LANCZOS),((W-pw)//2,250+(ph-h2)//2))
    else:
        c.paste(crop_to(bird(i),pw,ph,cx,cy,z),((W-pw)//2,250))
    d=ImageDraw.Draw(c)
    label(d,(70,76),f"SPECIES {k+1} OF 10")
    d.text((70,112),name,font=serif(58),fill=CREAM)
    d.text((70,186),sci,font=serifi(30),fill=(244,200,140))
    if tag:
        f=sansb(22); tw_=d.textlength(tag,font=f)+40
        d.rounded_rectangle([W-70-tw_,118,W-70,158],radius=20,fill=ACC)
        d.text((W-70-tw_+20,127),tag,font=f,fill=BG)
    label(d,(70,1055),"HABITAT",ACC,22)
    y=text(d,(70,1089),hab,sans(28),fill=CREAM,maxw=940,lh=1.2,shadow=False)
    label(d,(70,y+16),"LOOK FOR",ACC,22)
    y=text(d,(70,y+50),look,sans(26),fill=(215,208,192),maxw=940,lh=1.2,shadow=False)
    if note.strip(): d.text((70,y+14),note,font=sans(22),fill=(150,146,132))
    footer(d,k+2,TOT); finish(c,f"slide{k+2}.jpg")

# S12 summary
c=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(c)
label(d,(70,90),"WHERE TO LOOK IN THE ANDAMANS")
text(d,(70,135),"Know the habitat, find the bird.",serif(60),maxw=940,shadow=False)
rows=[("Forest interior","Andaman Serpent Eagle, Andaman Bulbul, Forest Wagtail"),("Forest edge and clearings","Long-tailed Parakeet, Oriental Dollarbird"),("Wetlands and mangroves","Andaman Teal, Collared Kingfisher"),("Mudflats and shores","Eurasian Whimbrel, Snipe"),("Open ground","Pipit")]
y=340
for k,v in rows:
    d.line([(70,y),(W-70,y)],fill=(60,58,50),width=2)
    d.text((70,y+26),k,font=sansb(26),fill=CREAM)
    lines=wrap(d,v,serif(26),480)
    for j,ln in enumerate(lines):
        d.text((W-70-d.textlength(ln,font=serif(26)),y+22+j*36),ln,font=serif(26),fill=ACC)
    y+=max(100,40+len(lines)*36+20)
d.line([(70,y),(W-70,y)],fill=(60,58,50),width=2)
text(d,(70,y+60),"Save this for your Andaman trip.",serif(46),maxw=940,shadow=False)
d.text((70,y+135),"Photographs by Hitesh Chawla  ·  The Natural Angle",font=sans(26),fill=(215,208,192))
footer(d,12,TOT,swipe=False); finish(c,"slide12.jpg")
print("ok")
