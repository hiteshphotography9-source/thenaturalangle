exec(open('audio_head_c.py').read())
rng=np.random.default_rng(31)
vmax=float(np.abs(voice).max())
sfx=np.zeros(N,np.float32); mus=np.zeros(N,np.float32); amb=np.zeros(N,np.float32)
x=tt(0,D)
def gridt(a,b,step):
    t=a
    while t<b-1e-6: yield t; t+=step
def norm_peak(s,p): 
    m=np.abs(s).max(); return s*(p/m) if m>0 else s
def at(sig,t0,peak):  # place a sound with a given absolute peak (relative to voice peak=1)
    return place(norm_peak(sig,peak*vmax),t0,0.0)
# ---------- sound design primitives (all darkened, no bell/ping tones)
def boom(dur=2.4):
    x_=tt(0,dur); sub=np.sin(2*np.pi*np.cumsum(46+70*np.exp(-x_*10))/SR)*np.exp(-x_*2.0)
    body=lp(noise(len(x_)),220)*np.exp(-x_*6)*0.8; return revtail(lp((sub*1.1+body).astype(np.float32),900),0.45)
def heart(dur=0.9):
    x_=tt(0,dur); b=lambda t0,a: np.sin(2*np.pi*np.cumsum(58*(1+1.6*np.exp(-np.clip(x_-t0,0,9)*28)))/SR)*np.exp(-np.clip(x_-t0,0,9)*14)*(x_>=t0)*a
    return lp((b(0,1.0)+b(0.23,0.7)).astype(np.float32),240)
def shutter():
    x_=tt(0,0.22); c=lambda t0,a: (hp(noise(len(x_)),1800)*np.exp(-np.clip(x_-t0,0,9)*160)+np.sin(2*np.pi*95*x_)*np.exp(-np.clip(x_-t0,0,9)*90)*0.8)*(x_>=t0)*a
    return lp((c(0,1.0)+c(0.085,0.8)).astype(np.float32),5200)
def softwhoosh(dur=0.55,up=True): 
    s=sweep_noise(dur,300,4200 if up else 4200,1.4) if up else sweep_noise(dur,4200,300,1.4)
    e=np.sin(np.pi*np.linspace(0,1,len(s)))**1.6; return lp(revtail((s*e).astype(np.float32),0.25),3800)
def riser_s(dur):
    s=sweep_noise(dur,180,3800,1.6)*np.linspace(0,1,int(dur*SR))**2.2; return lp(s.astype(np.float32),3200)
def tick_soft():
    x_=tt(0,0.05); return lp((hp(noise(len(x_)),900)*np.exp(-x_*120)).astype(np.float32),3500)
def chirp(f0=3200,f1=2300,dur=0.14):
    x_=tt(0,dur); f=f0+(f1-f0)*(x_/dur); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*x_/dur)**2
    s=s+0.3*np.sin(2*np.pi*np.cumsum(f*2)/SR)*np.sin(np.pi*x_/dur)**2; return revtail(lp(s.astype(np.float32),5200),0.5)
def water_bed(a,b,peak):
    d=b-a; n_=int(d*SR); s=bp(noise(n_),500,2600)*(0.6+0.4*lp(noise(n_),6,1)/ (np.abs(lp(noise(n_),6,1)).max()+1e-6)); s=s*np.minimum(1,np.minimum(np.arange(n_)/(1.0*SR),(n_-np.arange(n_))/(1.0*SR)))
    return place(norm_peak(s.astype(np.float32),peak*vmax),a,0.0)


def splash2(dur=1.1):
    x_=tt(0,dur); s=bp(noise(len(x_)),500,6500)*np.exp(-x_*5)+hp(noise(len(x_)),3500)*np.exp(-x_*16)*0.4
    for k in range(8):
        i=int(rng.uniform(0.05,0.6)*SR); L=int(0.05*SR); b=np.sin(2*np.pi*rng.uniform(900,2400)*x_[:L])*np.exp(-x_[:L]*70)*0.25; s[i:i+L]+=b
    return lp(revtail(s.astype(np.float32),0.3),6500)
def snap(): 
    x_=tt(0,0.25); return lp((hp(noise(len(x_)),700)*np.exp(-x_*60)+np.sin(2*np.pi*120*x_)*np.exp(-x_*40)*0.8).astype(np.float32),4500)
def hang(f,dur=2.4):
    x_=tt(0,dur); s=(np.sin(2*np.pi*f*x_)+0.35*np.sin(2*np.pi*f*2.01*x_)+0.15*np.sin(2*np.pi*f*3.02*x_))*np.exp(-x_*2.4); return revtail(lp(s.astype(np.float32),3200),0.6)
def river(a,b,peak):
    n_=int((b-a)*SR); s=bp(noise(n_),300,3200); mod=0.7+0.3*lp(noise(n_),3,1)/(np.abs(lp(noise(n_),3,1)).max()+1e-6); s=s*mod
    e=np.minimum(1,np.minimum(np.arange(n_)/(1.2*SR),(n_-np.arange(n_))/(1.2*SR))); return place(norm_peak((s*e).astype(np.float32),peak*vmax),a,0.0)
amb+=river(0,D,0.16)+river(15.0,22.5,0.12)   # stronger flow in the strong-current shot
t=1.0
while t<D-3:
    for k in range(rng.integers(1,3)): amb+=at(chirp(rng.uniform(2400,3400),rng.uniform(1800,2600),rng.uniform(0.1,0.22)),t+k*rng.uniform(0.2,0.35),0.05)
    t+=rng.uniform(4.0,8.0)
# mystery bed: D minor drone + slow hang-drum notes
Dm=[73.4,110,146.8,174.6]; Am=[55,110,164.8,220]; Fm=[87.3,130.8,174.6,261.6]
for a,b,ch in ((0,6.7,Dm),(6.7,12.7,Am),(12.7,17.2,Dm),(17.2,22.2,Fm),(22.2,D,Dm)): mus+=pad(ch,a,b,-26)
notes=[293.7,349.2,440,523.3,440,349.2]
i=0
for t0 in gridt(1.0,D-1,1.2):
    if 6.5<t0<17.0 and i%2==0: i+=1; continue
    mus+=at_raw(hang(notes[i%len(notes)]),t0,0.07)  if False else place(norm_peak(hang(notes[i%len(notes)]),0.075*vmax),t0,0.0); i+=1
# sub heartbeat while waiting
for t0 in gridt(7.0,17.0,1.5): sfx+=at(heart(),t0,0.20)
# SFX (medium level)
sfx+=at(riser_s(1.8),0.0,0.10)+at(boom(),0.25,0.30)
for t0 in (2.2,6.7,12.7,17.2,22.2): sfx+=at(softwhoosh(),t0-0.25,0.16)
for t0,pk in ((0.4,0.18),(2.6,0.14),(7.1,0.16),(13.0,0.18),(17.5,0.18),(22.6,0.18)): sfx+=at(tick_soft(),t0,pk)
sfx+=at(splash2(),1.1,0.30)+at(snap(),1.4,0.30)
sfx+=at(splash2(),3.2,0.20)
sfx+=at(riser_s(1.3),15.9,0.12)
sfx+=at(splash2(),17.5,0.34)+at(snap(),17.6,0.32)+at(boom(),17.3,0.26)
sfx+=at(splash2(),20.9,0.32)+at(snap(),21.05,0.30)
sfx+=at(boom(),22.5,0.22)
mb=0.30*vmax*np.tanh(mus/(0.30*vmax)); sb=0.45*vmax*np.tanh(sfx/(0.45*vmax)); ab=amb
print("peaks (dBFS of voice-ref): sfx %.1f music %.1f amb %.1f"%tuple(20*np.log10(np.abs(z).max()/vmax) for z in (sb,mb,ab)))
end=np.interp(x,[0,0.15,D-1.0,D],[0,1,1,0]).astype(np.float32)
mix=np.tanh(mb+sb+ab)*end
wf.write("mixCroc_raw.wav",SR,(np.clip(np.stack([mix,mix],1),-1,1)*32767).astype(np.int16))
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","mixCroc_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","mixCroc.wav"],check=True)
print(subprocess.run(["ffmpeg","-hide_banner","-i","mixCroc.wav","-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr[-160:])
