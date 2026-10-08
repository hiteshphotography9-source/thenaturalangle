import numpy as np, subprocess, wave, scipy.signal as sg, scipy.io.wavfile as wf
SR=48000; D=71.0; N=int(SR*D); rng=np.random.default_rng(7)
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/60c0f724-rec_2026-10-08_21-29-30.m4a"
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",U,"-af","highpass=f=70,alimiter=limit=0.9,loudnorm=I=-15:TP=-1.5:LRA=7","-ar",str(SR),"-ac","1","vo.wav"],check=True)
w=wave.open("vo.wav"); vo=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
voice=np.zeros(N,np.float32); voice[:min(N,len(vo))]=vo[:N]
def db(x): return 10**(x/20)
def tt(a,b): return np.arange(int(a*SR),int(b*SR))/SR
def place(sig,t0,g=0.0):
    out=np.zeros(N,np.float32); i=int(t0*SR); 
    if i<0: sig=sig[-i:]; i=0
    n=min(len(sig),N-i)
    if n>0: out[i:i+n]=sig[:n]*db(g)
    return out
def lp(x,fc,o=2): return sg.sosfilt(sg.butter(o,fc,'low',fs=SR,output='sos'),x).astype(np.float32)
def hp(x,fc,o=2): return sg.sosfilt(sg.butter(o,fc,'high',fs=SR,output='sos'),x).astype(np.float32)
def bp(x,a,b): return sg.sosfilt(sg.butter(2,[a,b],'band',fs=SR,output='sos'),x).astype(np.float32)
def noise(n): return rng.normal(0,1,n).astype(np.float32)
# reverb IR
def make_ir(sec=2.0,fc=4000):
    n=int(sec*SR); x=np.arange(n)/SR; ir=noise(n)*np.exp(-x*3.2); ir=lp(ir,fc); ir[:int(0.01*SR)]*=np.linspace(0,1,int(0.01*SR)); return ir/np.abs(ir).max()
IR=make_ir(2.2,3500)
def rev(x,wet=0.35):
    y=sg.fftconvolve(x,IR*0.12)[:len(x)+len(IR)-1].astype(np.float32); return x*(1-wet*0.0)+wet*y[:len(x)] if len(y)>=len(x) else x
def revtail(x,wet=0.5):
    y=sg.fftconvolve(x,IR*0.12).astype(np.float32); out=np.zeros(len(y),np.float32); out[:len(x)]+=x; out+=y*wet; return out
def sweep_noise(dur,f0,f1,q=1.2):
    n=int(dur*SR); x=noise(n); out=np.zeros(n,np.float32); hop=int(0.02*SR); win=np.hanning(hop*2)
    for i in range(0,n-hop*2,hop):
        f=f0*(f1/f0)**(i/n); b=sg.butter(2,[max(40,f/q),min(SR/2-100,f*q)],'band',fs=SR,output='sos')
        seg=sg.sosfilt(b,x[i:i+hop*2])*win; out[i:i+hop*2]+=seg.astype(np.float32)
    return out/ (np.abs(out).max()+1e-6)
def whoosh(t0,dur=0.9,up=True,g=-14,wet=0.35):
    f0,f1=(250,7000) if up else (7000,250); s=sweep_noise(dur,f0,f1); e=np.sin(np.pi*np.linspace(0,1,len(s)))**(1.2 if up else 1.2)
    if up: e=np.linspace(0,1,len(s))**2.2*np.linspace(1,0.0,len(s))**0.25
    return place(revtail(s*e,wet),t0,g)
def impact(t0,g=-6,big=1.0):
    x=tt(0,2.8); sub=np.sin(2*np.pi*np.cumsum(34+60*np.exp(-x*9))/SR)*np.exp(-x*1.5)
    body=lp(noise(len(x)),260)*np.exp(-x*6)*0.9; crack=hp(noise(len(x)),2500)*np.exp(-x*30)*0.5
    s=(sub*1.1+body+crack)*big; return place(revtail(s,0.5),t0,g)
def riser(t0,t1,g=-18):
    d=t1-t0; x=tt(0,d); s=sweep_noise(d,200,9000,1.5)*np.linspace(0,1,len(x))**2.5
    tone=np.sin(2*np.pi*np.cumsum(180+1800*(x/d)**2)/SR)*np.linspace(0,1,len(x))**3*0.25
    return place(s+tone,t0,g)
def pop(t0,f=700,g=-20): x=tt(0,0.07); return place(np.sin(2*np.pi*np.cumsum(f*(1+x*8))/SR)*np.exp(-x*55),t0,g)
def tick(t0,g=-26,f=2200): x=tt(0,0.03); return place(np.sin(2*np.pi*f*x)*np.exp(-x*140),t0,g)
def thump(t0,f=62,g=-12,d=0.4): x=tt(0,d); return place(np.sin(2*np.pi*np.cumsum(f*(1+2*np.exp(-x*30)))/SR)*np.exp(-x*9),t0,g)
def ping(t0,g=-20,f=1250): x=tt(0,2.2); s=np.sin(2*np.pi*f*x)*np.exp(-x*2.6); return place(revtail(s,0.6),t0,g)
def bell(t0,g=-18,f=880):
    x=tt(0,3.0); s=sum(np.sin(2*np.pi*f*m*x)*np.exp(-x*(1.5+i))*a for i,(m,a) in enumerate(((1,1),(2.76,0.5),(5.4,0.3),(8.9,0.2)))); return place(revtail(s.astype(np.float32),0.5),t0,g)
def splash(t0,g=-14):
    x=tt(0,0.9); s=bp(noise(len(x)),600,7000)*np.exp(-x*7)+hp(noise(len(x)),4000)*np.exp(-x*18)*0.4
    for k in range(7):
        i=int(rng.uniform(0.05,0.5)*SR); b=np.sin(2*np.pi*rng.uniform(900,2400)*x[:int(0.05*SR)])*np.exp(-x[:int(0.05*SR)]*70)*0.3; s[i:i+len(b)]+=b
    return place(s,t0,g)
def glitch(t0,g=-18,n=6):
    out=np.zeros(N,np.float32)
    for k in range(n):
        x=tt(0,0.045); s=np.sign(noise(len(x)))*np.exp(-x*30); s=hp(s,400); out+=place(s*0.8,t0+k*0.055,g)
    return out
def slash(t0,g=-12): x=tt(0,0.5); s=sweep_noise(0.5,9000,500)*np.exp(-x*5); return place(revtail(s,0.3),t0,g)
def kick(t0,g=-10): x=tt(0,0.28); return place(np.sin(2*np.pi*np.cumsum(46+110*np.exp(-x*28))/SR)*np.exp(-x*11)+0.2*hp(noise(len(x)),3000)*np.exp(-x*120),t0,g)
def hat(t0,g=-30,open_=False): x=tt(0,0.12 if open_ else 0.04); return place(hp(noise(len(x)),7000)*np.exp(-x*(25 if open_ else 80)),t0,g)
def bassnote(t0,f,d=0.28,g=-16):
    x=tt(0,d); s=sg.sawtooth(2*np.pi*f*x)*np.exp(-x*5); s=lp(s.astype(np.float32),340,2)+0.6*np.sin(2*np.pi*f*x)*np.exp(-x*4); return place(s.astype(np.float32),t0,g)
def pluck(t0,f,g=-26,d=0.9):
    x=tt(0,d); s=(np.sin(2*np.pi*f*x)+0.4*np.sin(2*np.pi*2*f*x)+0.15*np.sin(2*np.pi*3*f*x))*np.exp(-x*5.5); return place(revtail(s.astype(np.float32),0.55),t0,g)
def tone(f,x): return np.sin(2*np.pi*f*x)+0.5*np.sin(2*np.pi*2*f*x+0.3)+0.2*np.sin(2*np.pi*3*f*x)
def pad(freqs,a,b,g=-30):
    x=tt(0,b-a+3); e=np.interp(x,[0,1.5,b-a,b-a+2.5],[0,1,1,0]).astype(np.float32); s=sum(tone(f,x)*(1+0.12*np.sin(2*np.pi*(0.08+0.013*i)*x)) for i,f in enumerate(freqs)).astype(np.float32)
    return place(lp(s,1700)*e/len(freqs),a-0.0,g)

import numpy as _np
NEWT=[0,1.9,3.0,4.4,6.6,8.0,9.93,13.3,15.4,17.0,18.3,20.5,20.55,22.9,23.4,24.0,24.3,25.9,27.1,28.7,31.4,31.5,33.6,34.0,37.6,37.9,38.35,40.5,42.3,44.5,46.4,48.7,48.8,50.0,52.0,52.05,54.2,55.8,58.6,60.55,60.6,60.8,62.7,63.05,64.8,68.2,68.4,70.2,71.0]
OLDT=[0,1.6,2.6,3.6,7.6,8.6,10.0,11.4,12.0,14.0,16.2,22.4,22.5,24.4,26.5,28.0,29.0,29.5,31.8,34.0,36.4,36.5,40.0,41.5,44.2,44.4,44.9,47.5,51.0,52.4,54.0,56.5,56.6,57.2,61.9,62.0,62.7,66.0,67.8,70.4,70.5,70.6,73.1,73.3,73.7,77.0,77.4,79.2,80.0]
def O2N(t): return float(_np.interp(t,OLDT,NEWT))
sfx=np.zeros(N,np.float32); mus=np.zeros(N,np.float32); amb=np.zeros(N,np.float32)
def gridt(a,b,step):
    t=a
    while t<b-1e-6:
        yield t; t+=step
x=tt(0,D)
amb+=lp(noise(N),500)*0.5*np.interp(x,[0,2,20,23,71],[0,1,1,0,0]).astype(np.float32)*db(-38)
HITS_OLD=[(0.12,1.4),(1.6,1.0),(2.7,0.7),(7.5,1.2),(8.7,1.3),(10.1,1.0),(11.4,0.7),(14.0,0.8),(16.3,1.2),(22.7,1.2),(24.4,0.8),(29.5,0.8),(31.8,0.8),(34.0,0.8),(36.5,1.0),(41.5,1.3),(44.9,1.1),(51.1,1.2),(52.4,0.8),(57.2,1.5),(62.1,1.2),(66.0,0.9),(67.8,1.1),(70.6,1.2),(73.3,0.9),(77.4,0.8)]
for t0,s in HITS_OLD:
    tn=O2N(t0); sfx+=impact(tn,-10-(1.4-s)*5,s*0.8)+whoosh(tn-0.22,0.25,True,-20)+glitch(tn,-26,3)
sfx+=impact(0.12,-4,1.4)+thump(0.12,58,-6)
for a,b,g in ((4.9,6.6,-20),(8.2,9.9,-20),(18.3,20.5,-20),(19.0,20.5,-22),(46.5,48.7,-20),(59.0,60.6,-20),(66.6,68.4,-18),(49.0,50.0,-20)): sfx+=riser(a,b,g)
for k,t0 in enumerate(gridt(4.4,6.6,0.1)): sfx+=tick(t0,-34,1500+k*18)
for k,t0 in enumerate(gridt(31.5,33.6,0.05)): sfx+=tick(t0,-36,1300+(k%8)*60)
for k,t0 in enumerate(gridt(23.4,24.3,0.05)): sfx+=tick(t0,-36,1400+k*20)
for k,t0 in enumerate(gridt(55.8,56.8,0.05)): sfx+=tick(t0,-34,1500)
for t0 in (25.9,27.1,28.7): sfx+=bell(t0+0.1,-16,880)
sfx+=bell(50.0,-12,660)+bell(50.1,-16,990)+bell(50.2,-20,1320)
sfx+=ping(38.5,-22,1000)+ping(39.6,-24,1100)
sfx+=slash(42.3,-12)+thump(55.8,50,-8)+thump(58.6,50,-8)
sfx+=bell(68.4,-14,440)+bell(68.45,-22,660)
Am=[110,164.8,220,261.6]; F=[87.3,130.8,174.6,220]; Cc=[130.8,196,261.6,329.6]; G=[98,146.8,196,246.9]
BEAT=0.6
mus+=pad(Am,0.0,9.9,-30)+pad(F,9.9,20.5,-30)+pad(Am,20.5,31.4,-29)+pad(Cc,31.4,37.6,-29)+pad(G,37.9,42.3,-29)+pad(Am,42.3,48.8,-28)+pad(F,48.8,52.0,-28)+pad([110,130.8,164.8],52.0,60.6,-29)+pad(Am,60.6,71.0,-28)
def groove(a,b,lv=0.0,hats=True,bass=True,kick_on=True):
    for t0 in gridt(a,b,BEAT):
        if kick_on: mus.__iadd__(kick(t0,-13+lv))
        if hats: mus.__iadd__(hat(t0+BEAT/2,-31+lv,True)); mus.__iadd__(hat(t0,-37+lv))
        if bass:
            f=(55,55,43.65,43.65,65.4,65.4,49,49)[(int((t0-a)/BEAT/4))%8]
            mus.__iadd__(bassnote(t0,f,0.26,-19+lv)); mus.__iadd__(bassnote(t0+BEAT/2,f,0.2,-23+lv))
groove(1.9,9.9,0,False,False); groove(9.93,20.5,-3,True,True,False); groove(20.55,31.4,0); groove(31.5,37.6,-1); groove(37.9,42.3,0); groove(42.3,48.8,1); groove(48.8,52.0,2); groove(52.05,60.55,-1); groove(60.6,68.2,2)
def arp(a,b,notes,step=BEAT/2,g=-28):
    i=0
    for t0 in gridt(a,b,step): mus.__iadd__(pluck(t0,notes[i%len(notes)],g)); i+=1
Pm=[440,523.3,659.3,784,659.3,523.3]
arp(9.93,20.5,[440,523.3,659.3],BEAT,-30); arp(20.55,31.4,Pm,BEAT/2,-28); arp(31.5,37.6,[392,493.9,587.3,784],BEAT/2,-28); arp(42.3,52.0,Pm,BEAT/2,-26); arp(60.6,69.0,Pm,BEAT/2,-26)
mus*=np.where(x<1.9,0.4,1.0).astype(np.float32)
# voice duck
env=np.abs(voice); k=int(0.06*SR); env=np.convolve(env,np.ones(k)/k,mode='same'); env=lp(env,6,1); env=np.clip(env/(np.percentile(env,95)+1e-6),0,1)
act=env>0.3
def rms(z): return float(np.sqrt(np.mean(z[act]**2))+1e-9)
rv=rms(voice); mb=mus*(1-0.55*env); sb=sfx*(1-0.3*env); ab=amb*(1-0.6*env)
mb*=min(1.0,rv*db(-12)/rms(mb)); sb*=min(1.0,rv*db(-9)/rms(sb))
end=np.interp(x,[0,0.1,69.8,71.0],[0,1,1,0]).astype(np.float32)
import scipy.io.wavfile as wf
musfx=np.tanh((mb+sb+ab))*end
wf.write("stem5_raw.wav",SR,(np.clip(np.stack([musfx,musfx],1),-1,1)*32767).astype(np.int16))
mix=np.tanh(voice+mb+sb+ab)*end
wf.write("mix5_raw.wav",SR,(np.clip(np.stack([mix,mix],1),-1,1)*32767).astype(np.int16))
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","mix5_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","mix5.wav"],check=True)
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","stem5_raw.wav","-af","loudnorm=I=-16:TP=-1.5:LRA=11","-ar","48000","stem5.wav"],check=True)
print(subprocess.run(["ffmpeg","-hide_banner","-i","mix5.wav","-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr[-300:])
