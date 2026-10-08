import numpy as np, subprocess, wave, os
SR=48000; D=80.0; N=int(SR*D)
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/c26843c2-Recording_36.m4a"
rng=np.random.default_rng(11)
# narration: loudnorm to -15 LUFS, stereo float
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",U,"-af","highpass=f=70,loudnorm=I=-15:TP=-1.5:LRA=7","-ar",str(SR),"-ac","1","vo.wav"],check=True)
w=wave.open("vo.wav"); vo=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
voice=np.zeros(N,np.float32); voice[:min(N,len(vo))]=vo[:N]
def tt(a,b): return np.arange(int(a*SR),int(b*SR))/SR
def place(sig,t0,gain_db=0.0):
    out=np.zeros(N,np.float32); i=int(t0*SR); n=min(len(sig),N-i)
    if n>0: out[i:i+n]=sig[:n]*10**(gain_db/20)
    return out
def lp(x,fc):
    from scipy.signal import butter,sosfilt
    return sosfilt(butter(2,fc,'low',fs=SR,output='sos'),x).astype(np.float32)
def bp(x,lo,hi):
    from scipy.signal import butter,sosfilt
    return sosfilt(butter(2,[lo,hi],'band',fs=SR,output='sos'),x).astype(np.float32)
def env(n,a,r): 
    e=np.ones(n,np.float32); na=int(a*SR); nr=int(r*SR); e[:na]=np.linspace(0,1,na); e[-nr:]=np.linspace(1,0,nr); return e
sfx=np.zeros(N,np.float32)
def impact(t0,db):
    x=tt(0,2.2); s=np.sin(2*np.pi*(46+30*np.exp(-x*5))*x)*np.exp(-x*2.6); n=lp(rng.normal(0,1,len(x)).astype(np.float32),180)*np.exp(-x*5)*0.6
    return place((s+n)*0.9,t0,db)
def pulse(t0,db):
    x=tt(0,0.35); return place(np.sin(2*np.pi*55*x)*np.exp(-x*11),t0,db)
def ping(t0,db):
    x=tt(0,1.8); s=np.sin(2*np.pi*1250*x)*np.exp(-x*3.2)
    s2=np.zeros_like(s); d=int(0.28*SR); s2[d:]=s[:-d]*0.4; d2=int(0.55*SR); s3=np.zeros_like(s); s3[d2:]=s[:-d2]*0.18
    return place(s+s2+s3,t0,db)
def swell(t0,t1,db,f0,f1):
    x=tt(0,t1-t0); f=f0+(f1-f0)*(x/(t1-t0)); ph=2*np.pi*np.cumsum(f)/SR; s=np.sin(ph)*np.sin(np.pi*x/(t1-t0))**2
    n=lp(rng.normal(0,1,len(x)).astype(np.float32),300)*np.sin(np.pi*x/(t1-t0))**2*0.5
    return place(s+n,t0,db)
def water(t0,t1,db):
    x=tt(0,t1-t0); n=rng.normal(0,1,len(x)).astype(np.float32); y=bp(n,300,2200)*np.sin(np.pi*x/(t1-t0))**1.5
    return place(y,t0,db)
def click(t0,db):
    x=tt(0,0.05); n=bp(rng.normal(0,1,len(x)).astype(np.float32),2500,4500)*np.exp(-x*90); return place(n,t0,db)
def tick(t0,db,f=1900):
    x=tt(0,0.06); return place(np.sin(2*np.pi*f*x)*np.exp(-x*70),t0,db)
def thump(t0,db):
    x=tt(0,0.2); return place(np.sin(2*np.pi*120*x)*np.exp(-x*22),t0,db)
sfx+=pulse(0.53,-15)+pulse(0.82,-18)
sfx+=ping(16.35,-24)
sfx+=swell(20.0,24.2,-22,38,72)
sfx+=impact(30.65,-9)+impact(67.3,-10)
sfx+=click(32.2,-20)
for t0 in (33.0,37.0,41.6,45.6,47.5): sfx+=thump(t0,-22)
sfx+=water(49.5,54.4,-30)
for t0 in (8.1,9.1,10.1): sfx+=tick(t0,-26)
sfx+=tick(2.35,-26,1500)+tick(4.6,-26,1500)+tick(22.0,-26,1700)+tick(59.3,-26,1500)+tick(64.9,-24,2200)
sfx+=swell(72.8,79.2,-26,90,150)
# forest bed 0-19
x=tt(0,D); bed=lp(rng.normal(0,1,N).astype(np.float32),600)*0.5
bed*=np.interp(x,[0,2,16,19.5,80],[0,1,1,0,0]).astype(np.float32)
bed=bed*10**(-38/20)
for t0 in [1.6,3.2,5.1,6.4,8.8,10.5,13.0,14.6,16.8]:
    xx=tt(0,0.22); f=3200+900*np.sin(xx*40); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*xx/0.22)**2
    bed+=place(s.astype(np.float32),t0,-40)*np.interp(t0,[0,16,19.5],[1,1,0]).astype(np.float32)
# pad
def tone(f,x): return np.sin(2*np.pi*f*x)+0.5*np.sin(2*np.pi*2*f*x+0.3)+0.2*np.sin(2*np.pi*3*f*x)
x=tt(0,D)
def chord(fs,a,b):
    e=np.interp(x,[a-1.2,a+0.8,b-0.8,b+1.2],[0,1,1,0]).astype(np.float32)
    s=sum(tone(f,x)*(1+0.15*np.sin(2*np.pi*(0.07+0.01*i)*x)) for i,f in enumerate(fs)).astype(np.float32)
    return lp(s,1800)*e
pad=chord([110,164.8,220,261.6],0,30.5)+chord([87.3,130.8,220,261.6],30.5,58)+chord([110,164.8,220,277.2],58,67.5)+chord([110,164.8,220,261.6,329.6],67.5,80.5)
pad*=np.interp(x,[0,3,72.5,76,80],[0.55,0.8,0.8,1.15,0.4]).astype(np.float32)
pad=pad/np.abs(pad).max()*10**(-26/20)
mix=voice*1.0+sfx+bed+pad
mix=mix*np.interp(x,[0,0.4,79.2,80],[0,1,1,0]).astype(np.float32)
st=np.stack([mix,mix],1); st[:,0]+=np.roll(pad,240)*0.15; st[:,1]+=np.roll(pad,-240)*0.15
st=np.clip(st,-1,1)
import scipy.io.wavfile as wf; wf.write("mix_raw.wav",SR,(st*32767).astype(np.int16))
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","mix_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","mix.wav"],check=True)
print(subprocess.run(["ffmpeg","-hide_banner","-i","mix.wav","-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr[-420:])
