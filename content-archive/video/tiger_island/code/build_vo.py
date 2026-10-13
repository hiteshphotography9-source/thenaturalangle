import numpy as np, scipy.io.wavfile as w, noisereduce as nr, json, subprocess
sr,x=w.read('raw48.wav'); x=x.astype(np.float32)/32768
prof=np.concatenate([x[int(0.3*sr):int(4.0*sr)],x[int(138.6*sr):int(140.8*sr)]])
x=nr.reduce_noise(y=x,sr=sr,y_noise=prof,prop_decrease=0.75,stationary=True,n_fft=2048)
REM=[(0.0,4.05,"lead-in"),(96.45,101.55,"Bali 1927 sentence (factual slip: last confirmed 1937)"),(138.55,len(x)/sr,"tail")]
fade=int(0.012*sr)
def xf(buf,seg):
    if len(buf)==0: return seg.copy()
    n=min(fade,len(buf),len(seg)); r=np.linspace(0,1,n,dtype=np.float32); buf[-n:]=buf[-n:]*(1-r)+seg[:n]*r; return np.concatenate([buf,seg[n:]])
keep=[];cur=0.0
for a,b,_ in REM: keep.append((cur,a)); cur=b
keep=[(a,b) for a,b in keep if b-a>0.05]
out=np.zeros(0,np.float32); mp=[]
for a,b in keep: mp.append([a,b,len(out)/sr]); out=xf(out,x[int(a*sr):int(b*sr)])
h=int(sr*0.02); lev=np.array([20*np.log10(np.sqrt((out[i:i+h]**2).mean())+1e-9) for i in range(0,len(out)-h,h)])
thr=-36; quiet=lev<thr; i=0; cuts=[]
while i<len(quiet):
    if quiet[i]:
        j=i
        while j<len(quiet) and quiet[j]: j+=1
        if (j-i)*0.02>0.40: cuts.append((i*0.02+0.14,j*0.02-0.14))
        i=j
    else: i+=1
res=[];cur=0.0
for a,b in cuts: res.append((cur,a)); cur=b
res.append((cur,len(out)/sr))
new=np.zeros(0,np.float32); mp2=[]
for a,b in res: mp2.append([a,b,len(new)/sr]); new=xf(new,out[int(a*sr):int(b*sr)])
out=new
def s2o(ts):
    mid=None
    for a,b,o in mp:
        if a<=ts<=b: mid=o+(ts-a); break
    if mid is None:
        for a,b,o in mp:
            if ts<a: mid=o; break
    for a,b,o in mp2:
        if a<=mid<=b: return o+(mid-a)
    for a,b,o in mp2:
        if mid<a: return o
    return len(out)/sr
w.write('vo_edit_raw.wav',sr,(np.clip(out,-1,1)*32767).astype(np.int16))
src=dict(hook=4.25,swim=9.35,sing=30.50,idea=50.45,bali=73.15,isl=103.10,punch=119.40,cta=130.75)
mk={k:round(s2o(v),3) for k,v in src.items()}; mk['vo_end']=round(len(out)/sr,3)
print("pause cuts",len(cuts),"dur %.2f"%(len(out)/sr)); print(mk)
json.dump({"removed":REM,"pause_cuts":cuts,"marks":mk},open('edl.json','w'),indent=1)
