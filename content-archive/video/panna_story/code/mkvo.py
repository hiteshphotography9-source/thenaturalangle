import numpy as np, scipy.io.wavfile as w, noisereduce as nr, subprocess, json
F="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/09bd6ae7-Recording_35.m4a"
subprocess.run(["ffmpeg","-v","error","-y","-i",F,"-ac","1","-ar","48000","raw48.wav"],check=True)
sr,x=w.read("raw48.wav"); x=x.astype(np.float32)/32768
prof=np.concatenate([x[int(.1*sr):int(.7*sr)],x[int(6.2*sr):int(6.7*sr)],x[int(90.8*sr):int(91.9*sr)]])
y=nr.reduce_noise(y=x,sr=sr,y_noise=prof,prop_decrease=0.92,stationary=True,n_fft=2048)
# kept segments (src start,end, label, gap_before)
K=[("A",0.75,1.90,0),("B",6.75,9.05,0.50),("C",10.0,13.4,0.30),("D",14.1,16.9,0.25),
("G",23.0,29.3,0.40),("I",34.1,36.75,0.30),("J",44.05,46.15,0.18),
("L",50.75,54.25,0.45),("M",54.9,56.25,0.18),("N",56.85,59.3,0.22),
("O",64.1,65.1,0.40),("P",65.6,70.95,0.12),("R",79.15,84.5,0.40),("S",85.5,90.75,0.22),
("T",92.0,99.05,0.45),("U",100.2,105.05,0.45),("V",105.7,109.3,0.22),
("X",112.65,122.7,0.35),("AB",146.6,149.0,0.45),("AC",151.7,155.05,0.45)]
pre,post=0.10,0.16
out=[];tl=[];cur=0.0
def fade(a,n):
    a=a.copy(); n=min(n,len(a)//2); a[:n]*=np.linspace(0,1,n); a[-n:]*=np.linspace(1,0,n); return a
for lab,a,b,g in K:
    cur+=g; out.append(np.zeros(int(g*sr),np.float32))
    s=y[int((a-pre)*sr):int((b+post)*sr)]; s=fade(s,int(0.012*sr))
    out.append(s); tl.append((lab,round(cur+pre,3),round(cur+pre+(b-a),3),a,b)); cur+=len(s)/sr
v=np.concatenate(out); print("dur",len(v)/sr)
w.write("vo_raw.wav",sr,(np.clip(v,-1,1)*32767).astype(np.int16)); json.dump(tl,open("tl.json","w"))
for t in tl: print(t)
