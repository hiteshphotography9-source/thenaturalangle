import numpy as np, scipy.io.wavfile as w, scipy.signal as sg, noisereduce as nr, json, subprocess
sr,x=w.read('raw48.wav'); x=x.astype(np.float32)/32768
# 1) targeted notch of the horn lines that overlap speech (119.3-119.9)
def notch(sig,t0,t1,freqs,Q=35):
    a,b=int(t0*sr),int(t1*sr); seg=sig[a:b].copy()
    for f0 in freqs:
        bb,aa=sg.iirnotch(f0,Q,sr); seg=sg.filtfilt(bb,aa,seg)
    sig[a:b]=seg; return sig
x=notch(x,119.25,120.25,[3003,3375,3830,3090,3221])
# 2) gentle noise reduction from true pauses
prof=np.concatenate([x[int(51.4*sr):int(53.4*sr)],x[int(66.1*sr):int(66.9*sr)],x[int(81.5*sr):int(81.9*sr)],x[int(0.05*sr):int(0.7*sr)]])
x=nr.reduce_noise(y=x,sr=sr,y_noise=prof,prop_decrease=0.75,stationary=True,n_fft=2048)
# 3) removals (source seconds): horn/noise bursts, false start, click
REM=[(11.05,12.08,"noise/horn burst between phrases"),(30.02,30.48,"horn tone before phrase"),(71.40,77.30,"cough/noise + false start 'garmiyon mein k...' + dead air"),
     (86.35,87.22,"click"),(119.88,120.16,"horn tone in pause"),(122.76,125.08,"horn + click")]
keep=[];cur=0.0
for a,b,_ in REM: keep.append((cur,a)); cur=b
keep.append((cur,len(x)/sr))
GAPS={0:0.14,1:0.30,2:0.0,3:0.0,4:0.0,5:0.0}   # silence inserted at each removal join (join keeps original pause on both sides where present)
fade=int(0.012*sr)
out=np.zeros(0,np.float32); map_=[]
def xf_append(buf,seg):
    if len(buf)==0: return seg.copy()
    n=min(fade,len(buf),len(seg)); ramp=np.linspace(0,1,n,dtype=np.float32)
    buf[-n:]=buf[-n:]*(1-ramp)+seg[:n]*ramp; return np.concatenate([buf,seg[n:]])
t_out=0.0
for k,(a,b) in enumerate(keep):
    seg=x[int(a*sr):int(b*sr)]
    out=xf_append(out,seg)
    if k<len(REM):
        g=GAPS[k]
        if g>0: out=np.concatenate([out,np.zeros(int(g*sr),np.float32)])
# 4) cap very long pauses (>1.2 s of quiet) to 0.9 s
h=int(sr*0.02); lev=np.array([20*np.log10(np.sqrt((out[i:i+h]**2).mean())+1e-9) for i in range(0,len(out)-h,h)])
quiet=lev<-44; i=0; cuts=[]
while i<len(quiet):
    if quiet[i]:
        j=i
        while j<len(quiet) and quiet[j]: j+=1
        if (j-i)*0.02>1.2: cuts.append((i*0.02+0.45,j*0.02-0.45))
        i=j
    else: i+=1
res=[];cur=0.0
for a,b in cuts: res.append((cur,a)); cur=b
res.append((cur,len(out)/sr)); 
new=np.zeros(0,np.float32)
for a,b in res: new=xf_append(new,out[int(a*sr):int(b*sr)])
out=new
print("cuts for long pauses:",[(round(a,2),round(b,2)) for a,b in cuts])
print("duration %.1f s"%(len(out)/sr))
w.write('vo_edit_raw.wav',sr,(np.clip(out,-1,1)*32767).astype(np.int16))
json.dump({"removed":[(a,b,r) for a,b,r in REM],"pause_cuts":cuts},open('edl.json','w'))
