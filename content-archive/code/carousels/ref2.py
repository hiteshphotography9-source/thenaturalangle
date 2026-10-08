import numpy as np, cv2, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/"
FL=["64a42d44","b1208e85","26726f42","dc158818","f02d75ca","4dec5138","35021122"]
FD="fonts/"; OUT="falcon/"
W,H=1080,1440
CREAM=(244,238,226); GOLD=(226,184,104); GREY=(190,186,176); BG=(10,12,10)
anton=lambda s:ImageFont.truetype(FD+"Anton-Regular.ttf",int(s))
bc=lambda s:ImageFont.truetype(FD+"BarlowCondensed-Medium.ttf",int(s))
bcs=lambda s:ImageFont.truetype(FD+"BarlowCondensed-SemiBold.ttf",int(s))
bar=lambda s:ImageFont.truetype(FD+"Barlow-Regular.ttf",int(s))
barm=lambda s:ImageFont.truetype(FD+"Barlow-Medium.ttf",int(s))
def corm(s):
    f=ImageFont.truetype(FD+"CormorantGaramond-Italic[wght].ttf",int(s))
    try: f.set_variation_by_axes([500])
    except Exception: pass
    return f

def load_subject(i,xr=None,crop=None):
    src=Image.open(U+FL[i]+"-image.jpg").convert("RGB")
    a=np.array(Image.open(f"cutf/{i}.png").split()[-1])
    if crop:
        fx0,fy0,fx1,fy1=crop; X0,Y0,X1,Y1=int(fx0*src.width),int(fy0*src.height),int(fx1*src.width),int(fy1*src.height)
        src=src.crop((X0,Y0,X1,Y1)); a=a[Y0:Y1,X0:X1]
    b=(a>127).astype(np.uint8)
    if xr:
        b[:, :int(xr[0]*b.shape[1])]=0; b[:, int(xr[1]*b.shape[1]):]=0
    # keep only components above 1% of the largest
    n,lab,st,_=cv2.connectedComponentsWithStats(b,8)
    if n>1:
        big=st[1:,4].max(); keep=[k+1 for k in range(n-1) if st[k+1,4]>=0.01*big]
        b=np.isin(lab,keep).astype(np.uint8)
    ys,xs=np.where(b>0); bw,bh=xs.max()-xs.min(),ys.max()-ys.min()
    k=max(3,int(0.035*max(bw,bh))|1)
    b=cv2.morphologyEx(b,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k,k)))
    # fill holes
    ff=b.copy(); h_,w_=ff.shape; m=np.zeros((h_+2,w_+2),np.uint8); cv2.floodFill(ff,m,(0,0),2)
    b=np.where(ff==2,0,1).astype(np.uint8)
    alpha=cv2.GaussianBlur(b.astype(np.float32)*255,(0,0),1.6)
    tch=dict(t=b[0,:].mean()>0.01,b=b[-1,:].mean()>0.01,l=b[:,0].mean()>0.01,r=b[:,-1].mean()>0.01)
    return src,alpha,(xs.min(),ys.min(),xs.max(),ys.max()),tch

def gold_tex(seed=1):
    rng=np.random.default_rng(seed)
    yy=np.linspace(0,1,H)[:,None]; xx=np.linspace(0,1,W)[None,:]
    top=np.array([252,232,170],np.float32); bot=np.array([206,160,84],np.float32)
    base=top[None,None,:]*(1-yy[:,:,None])+bot[None,None,:]*yy[:,:,None]
    base=base*(0.96+0.08*xx[:,:,None])
    def nz(s): 
        n=rng.normal(0,1,(H,W)).astype(np.float32); return cv2.GaussianBlur(n,(0,0),s)
    n1=nz(40); n1/=np.abs(n1).max()
    n2=nz(10); n2/=np.abs(n2).max()
    ridge=np.abs(nz(5)-nz(12)); ridge/=ridge.max()
    fine=rng.normal(0,1,(H,W)).astype(np.float32)
    tex=base*(1+0.12*n1[:,:,None]+0.07*n2[:,:,None])+(ridge[:,:,None]**2)*34-8+fine[:,:,None]*5
    return np.clip(tex,0,255)
TEX=gold_tex()

def wrap_text(d,t,font,maxw):
    out=[];cur=""
    for w in t.split():
        c=(cur+" "+w).strip()
        if d.textlength(c,font=font)<=maxw: cur=c
        else: out.append(cur);cur=w
    out.append(cur);return out

def title_block(lines,cap):
    probe=ImageDraw.Draw(Image.new("L",(10,10)))
    f100=anton(100); wmax=max(probe.textlength(l,font=f100) for l in lines)
    size=min(920/wmax*100,cap)
    f=anton(size); asc,desc=f.getmetrics()
    capH=f.getbbox("H")[3]-f.getbbox("H")[1]
    lh=capH*1.12
    return f,size,capH,lh,len(lines)*lh-(lh-capH)

def build(idx,lead,lines,sub,facts,counter,fname,cap=None,subject_xshift=0,bird_bottom=1130,force_title_top=None,sub_side=None,bg_fill=None,xr=None,bh_t=520,footer_text=None,crop=None,s_force=None,post=None,subject_xshift_=0,ov=0.5,sub_xy=None):
    src,alpha,(bx0,by0,bx1,by1),tch=load_subject(idx,xr,crop)
    Ws,Hs=src.size; bw,bh=bx1-bx0,by1-by0; bcx=(bx0+bx1)/2
    cap=cap or (380 if len(lines)==1 else 300 if len(lines)==2 else 250)
    f,size,capH,lh,tblock=title_block(lines,cap)
    s=min(980/bw,bh_t/bh,2.3)
    if s_force: s=s_force
    bhs=bh*s
    if bhs>=400:
        btop=bird_bottom-bhs
        ttop=btop+ov*capH-tblock
        if ttop<200: ttop=200; btop=max(btop,ttop+tblock-ov*capH)
    else:
        ttop=force_title_top or 300
        btop=min(ttop+tblock-ov*capH,bird_bottom-bhs)
    # place source
    ox=540+subject_xshift-s*bcx; oy=btop-s*by0
    ox=min(0,max(1080-s*Ws,ox)) if s*Ws>=1080 else (1080-s*Ws)/2
    sw,sh=int(Ws*s),int(Hs*s)
    ph=src.resize((sw,sh),Image.LANCZOS); al=Image.fromarray(alpha.astype(np.uint8)).resize((sw,sh),Image.LANCZOS)
    ix,iy=int(ox),int(oy)
    pl,pt,pr,pb=max(0,ix),max(0,iy),max(0,W-ix-sw),max(0,H-iy-sh)
    pa=np.array(ph)
    if pl or pt or pr or pb:
        padded=cv2.copyMakeBorder(pa,min(pt,sh-1),min(pb,sh-1),min(pl,sw-1),min(pr,sw-1),cv2.BORDER_REPLICATE)
        if padded.shape[0]<sh+pt+pb or padded.shape[1]<sw+pl+pr:
            padded=cv2.copyMakeBorder(padded,0,max(0,sh+pt+pb-padded.shape[0]),0,max(0,sw+pl+pr-padded.shape[1]),cv2.BORDER_REPLICATE)
        blurred=cv2.GaussianBlur(padded,(0,0),30)
        mk=np.zeros(padded.shape[:2],np.float32); mk[pt:pt+sh,pl:pl+sw]=1
        mk=cv2.GaussianBlur(mk,(0,0),55)[:,:,None]
        fill=blurred.copy().astype(np.float32)
        padded=padded.copy()
        if tch['b']: padded[pt+sh:,:]=BG
        if tch['t']: padded[:pt,:]=BG
        if tch['l']: padded[:,:pl]=BG
        if tch['r']: padded[:,pl+sw:]=BG
        if tch['b']: fill[pt+sh:,:]=BG
        if tch['t']: fill[:pt,:]=BG
        if tch['l']: fill[:,:pl]=BG
        if tch['r']: fill[:,pl+sw:]=BG
        pad_all=(padded*mk+fill*(1-mk)).astype(np.uint8)
    else: pad_all=pa
    ox0=ix-pl; oy0=iy-pt
    cx0=-ox0; cy0=-oy0
    canvas=Image.fromarray(pad_all[cy0:cy0+H,cx0:cx0+W])
    arr=np.array(canvas).astype(np.float32)
    arr*=0.80
    # vignette + bottom gradient
    yy,xx=np.mgrid[0:H,0:W]; d=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2)
    arr*= (1-0.30*np.clip(d-0.5,0,1)**1.4)[:,:,None]
    g=np.clip((yy-1020)/420,0,1)*0.82; arr=arr*(1-g[:,:,None])+np.array(BG,np.float32)*g[:,:,None]
    gt=np.clip((240-yy)/240,0,1)*0.55; arr=arr*(1-gt[:,:,None])+np.array(BG,np.float32)*gt[:,:,None]
    # title (gold) behind subject
    tm=Image.new("L",(W,H),0); td=ImageDraw.Draw(tm)
    ys=ttop
    for ln in lines:
        td.text((64,ys),ln,font=f,fill=255,anchor="la")
        # Anton top bearing: adjust so cap top == ys
        ys+=lh
    # shift: compensate font bearing
    bb=f.getbbox("H"); off=bb[1]
    tm=Image.new("L",(W,H),0); td=ImageDraw.Draw(tm); ys=ttop-off
    for ln in lines: td.text((64,ys),ln,font=f,fill=255,anchor="la"); ys+=lh
    tmn=np.array(tm).astype(np.float32)/255
    sh_=cv2.GaussianBlur(tmn,(0,0),14)*0.55
    arr=arr*(1-sh_[:,:,None])
    arr=arr*(1-tmn[:,:,None])+TEX*tmn[:,:,None]
    canvas=Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
    # subject on top
    sub_rgb=ph; full_al=Image.new("L",(W,H),0); full_al.paste(al,(int(ox),int(oy)))
    sub_layer=Image.new("RGB",(W,H),(0,0,0)); sub_layer.paste(sub_rgb,(int(ox),int(oy)))
    canvas=Image.composite(sub_layer,canvas,full_al)
    amask=np.array(full_al).astype(np.float32)/255
    d=ImageDraw.Draw(canvas)
    # lead italic
    d.text((66,ttop-106),lead,font=corm(78),fill=(236,230,214),anchor="la")
    # header
    d.text((64,52),"THE NATURAL ANGLE",font=bcs(26),fill=(220,214,200))
    cnt=counter; tw=d.textlength(cnt,font=bcs(26))+44
    d.rounded_rectangle([W-64-tw,38,W-64,86],radius=24,fill=(20,20,18))
    d.text((W-64-tw+22,48),cnt,font=bcs(26),fill=CREAM)
    # subtitle
    tb=ttop+tblock
    sublines=sub.split("|")
    probe2=ImageDraw.Draw(Image.new('L',(10,10)))
    sf=bc(64)
    if max(probe2.textlength(l,font=sf) for l in sublines)>470: sf=bc(50)
    lead_w=probe2.textlength(lead,font=corm(78))+66
    sw_=max(d.textlength(l,font=sf) for l in sublines); sh2=len(sublines)*(62 if sf.size>=60 else 50)
    cands=[(64,tb+30),(W-64-sw_,tb+30)]
    if W-64-sw_>lead_w+24: cands.append((W-64-sw_,ttop-sh2-6))
    best=None
    for (cx_,cy_) in cands:
        x0_,y0_,x1_,y1_=int(cx_),int(cy_),int(cx_+sw_),int(cy_+sh2)
        reg=amask[max(0,y0_):min(H,y1_),max(0,x0_):min(W,x1_)]
        ov=reg.mean() if reg.size else 1
        if best is None or ov<best[0]: best=(ov,cx_,cy_)
    ov,sx,sy=best
    if sub_side=="left": sx,sy=64,tb+30
    if sub_side=="right": sx,sy=W-64-sw_,tb+30
    step=(62 if sf.size>=60 else 50)
    for k,l in enumerate(sublines):
        if sub_xy:
            mode,xx,yy=sub_xy
            px=xx if mode=='L' else xx-d.textlength(l,font=sf)
            d.text((px,yy+k*step),l,font=sf,fill=(205,200,190))
        else:
            d.text((sx if sx==64 else W-64-d.textlength(l,font=sf),sy+k*step),l,font=sf,fill=(205,200,190))
    if footer_text: d.text((64,1262),footer_text,font=corm(52),fill=GOLD)
    # facts
    n=max(1,len(facts)); gap=36; colw=(W-128-gap*(n-1))/n
    fy=1196
    for k,(lab,txt) in enumerate(facts if facts else []):
        x=64+k*(colw+gap)
        d.line([(x,fy),(x,fy+128)],fill=(150,146,134),width=2)
        d.text((x+22,fy-2),lab,font=bcs(22),fill=GOLD)
        ls=wrap_text(d,txt,bar(26),colw-30)
        for j,l in enumerate(ls[:4]): d.text((x+22,fy+30+j*32),l,font=bar(26),fill=CREAM)
    if post: post(d,canvas,amask)
    # grain
    arr=np.array(canvas).astype(np.float32)+np.random.default_rng(7).normal(0,5.5,(H,W,1))
    Image.fromarray(np.clip(arr,0,255).astype(np.uint8)).save(OUT+fname,quality=95)
    return ov

if __name__=="__main__":
    t=sys.argv[1]
    if t=="test":
        print(build(10,"Andaman",["SERPENT","EAGLE"],"ENDEMIC TO|THE ANDAMANS",[("HABITAT","Wet evergreen forest in the interior of the larger islands."),("LOOK FOR","Yellow face, dark body with white spots."),("STATUS","Listed Vulnerable and declining.")],"2/12","t_eagle.jpg"))
        print(build(1,"Andaman",["TEAL"],"ENDEMIC TO|THE ANDAMANS",[("HABITAT","Ponds, tidal creeks, mangroves and brackish swamps."),("LOOK FOR","A small brown duck with a white eye ring."),("STATUS","Near Threatened. Wetlands are being reclaimed.")],"4/12","t_teal.jpg",xr=(0.62,1.0)))
        print(build(9,"Collared",["KINGFISHER"],"BLUE BACK.|WHITE COLLAR.",[("HABITAT","Coastal mangroves, tidal flats and sheltered bays."),("LOOK FOR","Blue back, white collar and a heavy dark bill.")],"7/12","t_king.jpg"))
