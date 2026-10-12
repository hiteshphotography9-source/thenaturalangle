import numpy as np, scipy.io.wavfile as w, scipy.signal as sg, noisereduce as nr, json, subprocess
sr,x=w.read('raw48.wav'); x=x.astype(np.float32)/32768
# noise profile from true pauses
prof=np.concatenate([x[int(0.4*sr):int(3.6*sr)],x[int(46.8*sr):int(47.8*sr)],x[int(73.2*sr):int(75.8*sr)]])
x=nr.reduce_noise(y=x,sr=sr,y_noise=prof,prop_decrease=0.75,stationary=True,n_fft=2048)
REM=[(0.0,3.80,"lead-in silence"),(72.75,len(x)/sr,"tail silence")]
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
marks={"hook":4.0,"dotty":7.5,"origin":8.7,"y2012":11.35,"magadhi":13.15,"spotty":15.0,"sukhi":16.95,"home":19.1,"kids":20.8,"d1":24.1,"son":26.0,"push":28.3,"daughters":30.7,"out":32.95,"tala":36.7,"mother":38.55,"twocubs":40.25,"oct":42.6,"manpur":44.5,"patrol":48.05,"age":51.55,"natural":53.4,"left":56.85,"months":58.55,"watch":60.95,"mom":64.3,"legacy":65.35,"seen":68.9,"comment":71.2,"end":72.5}
mk={k:round(src2out(v),3) for k,v in marks.items()}; print(mk)
json.dump({"removed":REM,"pause_cuts":cuts,"marks":mk,"dur":len(out)/sr},open('edl.json','w'))
