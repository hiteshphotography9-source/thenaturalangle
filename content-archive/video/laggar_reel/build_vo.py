import numpy as np, scipy.io.wavfile as w, scipy.signal as sg, noisereduce as nr, json, subprocess
sr,x=w.read('raw48.wav'); x=x.astype(np.float32)/32768
# noise profile from true pauses
prof=np.concatenate([x[int(35.2*sr):int(36.6*sr)],x[int(44.9*sr):int(45.8*sr)],x[int(54.15*sr):int(54.95*sr)],x[int(0.4*sr):int(2.2*sr)]])
x=nr.reduce_noise(y=x,sr=sr,y_noise=prof,prop_decrease=0.75,stationary=True,n_fft=2048)
REM=[(0.0,2.34,"lead-in noise/breath"),(14.68,14.98,"false-start fragment before 'khaas kar lizards'"),(17.33,18.42,"'okay/or' false start before 'solah'"),
     (23.36,23.86,"'I'm' fumble before 'menu'"),(30.62,31.82,"fumble between 'udna' and 'zameen'"),(73.10,77.85,"'India protected Schedule I species' line (removed as asked)"),(81.30,len(x)/sr,"tail")]
fade=int(0.012*sr)
def xf(buf,seg):
    if len(buf)==0: return seg.copy()
    n=min(fade,len(buf),len(seg)); r=np.linspace(0,1,n,dtype=np.float32); buf[-n:]=buf[-n:]*(1-r)+seg[:n]*r; return np.concatenate([buf,seg[n:]])
keep=[];cur=0.0
for a,b,_ in REM: keep.append((cur,a)); cur=b
keep=[(a,b) for a,b in keep if b-a>0.05]
# map: list of (src_start,src_end,out_start) for later timeline mapping
out=np.zeros(0,np.float32); mp=[]
for a,b in keep:
    seg=x[int(a*sr):int(b*sr)]; mp.append([a,b,len(out)/sr]); out=xf(out,seg)
# pause compression: quiet runs > 0.50 s -> 0.40 s (keep 0.2 each side) ; track mapping
h=int(sr*0.02); lev=np.array([20*np.log10(np.sqrt((out[i:i+h]**2).mean())+1e-9) for i in range(0,len(out)-h,h)])
thr=-34; quiet=lev<thr; i=0; cuts=[]
while i<len(quiet):
    if quiet[i]:
        j=i
        while j<len(quiet) and quiet[j]: j+=1
        d=(j-i)*0.02
        if d>0.40: cuts.append((i*0.02+0.15,j*0.02-0.15))
        i=j
    else: i+=1
res=[];cur=0.0
for a,b in cuts: res.append((cur,a)); cur=b
res.append((cur,len(out)/sr))
new=np.zeros(0,np.float32); mp2=[]
for a,b in res: mp2.append([a,b,len(new)/sr]); new=xf(new,out[int(a*sr):int(b*sr)])
out=new
def src2out(ts):
    # src -> mid -> out
    mid=None
    for a,b,o in mp:
        if a<=ts<=b: mid=o+(ts-a); break
    if mid is None:
        # nearest following kept
        for a,b,o in mp:
            if ts<a: mid=o; break
        if mid is None: mid=mp[-1][2]+(mp[-1][1]-mp[-1][0])
    for a,b,o in mp2:
        if a<=mid<=b: return o+(mid-a)
    for a,b,o in mp2:
        if mid<a: return o
    return len(out)/sr
print("cuts:",[(round(a,2),round(b,2)) for a,b in cuts]); print("duration %.1f"%(len(out)/sr))
w.write('vo_edit_raw.wav',sr,(np.clip(out,-1,1)*32767).astype(np.int16))
marks={"hook":2.44,"study":7.89,"pct":12.10,"lizard":15.0,"sixteen":18.45,"menu":23.9,"shikar":26.65,"nest":36.85,"kauwe":40.3,"aam":45.94,"ladakh":49.82,"fourk":50.75,"survival":55.11,"estimate":58.99,"pct2":60.55,"habitat":64.20,"agli":68.78,"laggar":72.26,"kahan":78.49,"end":81.0}
mk={k:round(src2out(v),3) for k,v in marks.items()}; print(mk)
json.dump({"removed":REM,"pause_cuts":cuts,"marks":mk,"dur":len(out)/sr},open('edl.json','w'))
