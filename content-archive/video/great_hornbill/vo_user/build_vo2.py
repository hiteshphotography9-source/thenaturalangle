import numpy as np, scipy.io.wavfile as w, noisereduce as nr, json, subprocess
sr,x=w.read('raw48.wav'); x=x.astype(np.float32)/32768
prof=np.concatenate([x[int(0.3*sr):int(3.2*sr)],x[int(148.5*sr):int(152.3*sr)]])
x=nr.reduce_noise(y=x,sr=sr,y_noise=prof,prop_decrease=0.85,stationary=True,n_fft=2048)
# phrase idx -> list of (src_start, src_end); idx follows the script (same indices the video scenes use)
P={0:[(3.50,4.85),(5.05,5.90)],1:[(6.85,8.40)],2:[(9.30,10.50)],3:[(11.35,13.60)],4:[(14.15,15.40),(15.60,16.20)],5:[(16.55,19.10)],6:[(20.05,22.10),(22.30,25.10),(25.55,27.80)],
7:[(29.20,31.40)],8:[(31.80,32.45),(32.80,33.65),(34.25,36.90)],9:[(38.45,40.55)],10:[(41.80,43.15)],11:[(43.15,44.50)],12:[(50.60,52.40),(52.70,53.80),(54.10,55.25)],
13:[(57.50,59.15)],14:[(59.70,60.70)],15:[(61.60,64.50)],16:[(65.05,67.80)],17:[(69.35,71.05)],18:[(71.45,75.70)],19:[(76.95,79.20)],
20:[(83.90,85.35)],21:[(85.35,86.40)],22:[(87.10,89.05)],23:[(89.45,91.00)],24:[(92.28,94.35),(95.55,96.80),(97.15,98.60)],
26:[(103.00,104.65)],27:[(105.00,105.80),(106.25,107.65),(110.60,114.00)],28:[(114.30,116.60)],
29:[(117.45,118.85)],30:[(119.60,122.55)],31:[(122.95,124.75)],32:[(125.20,126.70)],33:[(127.95,130.30),(131.15,133.65)],34:[(134.10,137.10)],
35:[(140.90,143.45)],36:[(144.00,144.60),(144.95,145.95)],37:[(146.20,147.10)]}
SC={0:0,1:0,2:0,3:1,4:1,5:1,6:1,7:2,8:2,9:2,10:2,11:2,12:2,13:3,14:3,15:3,16:3,17:4,18:4,19:4,20:5,21:5,22:5,23:5,24:5,25:5,26:6,27:6,28:6,29:7,30:7,31:7,32:7,33:7,34:7,35:8,36:8,37:8}
PA,PB=0.06,0.10; fade=int(0.008*sr); TEMPO=float(__import__('sys').argv[1]) if len(__import__('sys').argv)>1 else 1.0
out=np.zeros(int(0.3*sr),np.float32); marks={}; prev=None
for idx in sorted(P):
    gap=0 if prev is None else (0.34 if SC[idx]!=SC[prev] else 0.14); prev=idx
    out=np.concatenate([out,np.zeros(int(gap*sr),np.float32)]); st=len(out)/sr+PA
    for j,(a,b) in enumerate(P[idx]):
        if j>0: out=np.concatenate([out,np.zeros(int(0.10*sr),np.float32)])
        seg=x[int((a-PA)*sr):int((b+PB)*sr)].copy(); n=min(fade,len(seg)); seg[:n]*=np.linspace(0,1,n); seg[-n:]*=np.linspace(1,0,n); out=np.concatenate([out,seg])
    marks[idx]=[st/TEMPO,(len(out)/sr-PB)/TEMPO]
out=np.concatenate([out,np.zeros(int(0.3*sr),np.float32)])
w.write('vo_edit_raw.wav',sr,(np.clip(out,-1,1)*32767).astype(np.int16))
json.dump({str(k):[round(a,3),round(b,3),""] for k,(a,b) in marks.items()},open('phrases.json','w'))
af=("atempo=%.3f,"%TEMPO if TEMPO!=1 else "")+"highpass=f=80,lowpass=f=9000,equalizer=f=220:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1:g=2.2,acompressor=threshold=-22dB:ratio=3:attack=8:release=100:makeup=3,loudnorm=I=-16:TP=-1.5:LRA=9"
subprocess.run(["ffmpeg","-y","-v","error","-i","vo_edit_raw.wav","-af",af,"-ar","48000","-ac","1","VO_clean_user.wav"],check=True)
print("dur %.2f"%(len(out)/sr/TEMPO), "last",marks[37])
