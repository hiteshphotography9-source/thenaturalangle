import numpy as np, scipy.io.wavfile as w, noisereduce as nr, json
sr,x=w.read('raw48.wav'); x=x.astype(np.float32)/32768
prof=np.concatenate([x[int(0.2*sr):int(1.6*sr)],x[int(125.3*sr):int(126.4*sr)]])
x=nr.reduce_noise(y=x,sr=sr,y_noise=prof,prop_decrease=0.8,stationary=True,n_fft=2048)
REM=[(0.0,1.65,"lead-in"),(94.35,109.85,"FIRST closing take incl. 'Registani billi' slip (95.15-108.3); clean retake from 110.05 kept"),(125.3,len(x)/sr,"tail")]
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
thr=-38; quiet=lev<thr; i=0; cuts=[]
while i<len(quiet):
    if quiet[i]:
        j=i
        while j<len(quiet) and quiet[j]: j+=1
        if (j-i)*0.02>0.70: cuts.append((i*0.02+0.25,j*0.02-0.25))
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
OFF=0.5
anch=dict(S1=0.0,S2=11.35-0.3,S3a=24.85-0.3,S3b=29.2-0.3,S4a=37.25-0.3,S4b=40.0,S5=54.7-0.4,S6a=68.35-0.35,S6b=74.05-0.25,S7=81.95-0.3,S8=110.05-0.3)
marks={k:(0.0 if k=="S1" else round(s2o(v)+OFF,3)) for k,v in anch.items()}
marks["end"]=round(s2o(124.8)+OFF+1.7,3)
print("pause cuts",len(cuts),"dur %.2f"%(len(out)/sr)); print(marks)
json.dump(marks,open('../marks.json','w'))
json.dump({"removed":REM,"pause_cuts":cuts,"marks":marks},open('edl.json','w'),indent=1)
