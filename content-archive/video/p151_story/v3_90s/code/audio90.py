exec(open('audio_head90.py').read())
rng=np.random.default_rng(31)
vmax=float(np.abs(voice).max())
sfx=np.zeros(N,np.float32); mus=np.zeros(N,np.float32); amb=np.zeros(N,np.float32)
x=tt(0,D)
def gridt(a,b,step):
    t=a
    while t<b-1e-6: yield t; t+=step
def norm_peak(s,p): 
    m=np.abs(s).max(); return s*(p/m) if m>0 else s
def at_raw(sig,t0,peak):  # place a sound with a given absolute peak (relative to voice peak=1)
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

from cut90 import o2n,SEGS,TOTAL
def at(sig,t0,peak):
    n=o2n(t0)
    if n is None: return np.zeros(N,np.float32)
    return at_raw(sig,n,peak)
def atn(sig,t0,peak): return at_raw(sig,t0,peak)
wn=lp(noise(N),600)*(0.7+0.3*np.sin(2*np.pi*0.07*x)); wn=wn*np.interp(x,[0,3,86,D],[0.5,1,1,0.3]).astype(np.float32)
amb+=norm_peak(wn.astype(np.float32),0.030*vmax)
ins=bp(noise(N),3600,5400)*(0.5+0.5*np.sin(2*np.pi*0.2*x+1)**2)*(0.6+0.4*np.sign(np.sin(2*np.pi*28*x))); amb+=norm_peak(ins.astype(np.float32),0.020*vmax)*np.interp(x,[0,4,60,D],[0.6,1,0.6,0.5]).astype(np.float32)
t=2.0
while t<D-4:
    for k in range(rng.integers(1,4)): amb+=atn(chirp(rng.uniform(2600,3600),rng.uniform(1900,2800),rng.uniform(0.09,0.2)),t+k*rng.uniform(0.15,0.3),0.028)
    t+=rng.uniform(3.5,8.5)
amb+=water_bed(27.6,37.3,0.030); amb+=water_bed(53.8,57.9,0.030)
# cut transitions: soft whoosh + shutter on every jump cut
for n0,n1,o0,o1 in SEGS[1:]:
    sfx+=atn(softwhoosh(),n0-0.25,0.18); sfx+=atn(shutter(),n0+0.02,0.13)
sfx+=atn(boom(),0.85,0.34)+atn(riser_s(1.4),0.0,0.10)
sfx+=at(boom(),7.5,0.20)
sfx+=at(boom(),16.4,0.22)+at(boom(),19.95,0.30)
sfx+=at(boom(),24.4,0.18)
for k,t0 in enumerate(gridt(24.6,26.6,0.1)): sfx+=at(tick_soft(),t0,0.06)
for i in range(13): sfx+=at(tick_soft(),25.2+i*0.12,0.07)
sfx+=at(heart(),30.5,0.28)
for t0 in (55.15,56.55,57.45): sfx+=at(shutter(),t0,0.28)+at(boom(0.9),t0,0.20)
sfx+=at(boom(),66.0,0.20)
sfx+=at(boom(),85.4,0.36)
for t0 in gridt(86.0,92.0,1.15): sfx+=at(heart(),t0,0.12)
sfx+=at(boom(),110.3,0.30)
for t0 in gridt(111.0,118.0,1.3): sfx+=at(heart(),t0,0.11)
sfx+=at(boom(),119.2,0.22)+at(boom(),121.7,0.16)+at(boom(),124.5,0.24)
Am=[110,164.8,220,261.6]; F=[87.3,130.8,174.6,220]; Cc=[130.8,196,261.6,329.6]; Dm=[73.4,110,146.8,174.6]; low=[55,82.4,110]
plan=[(0.75,5.6,low),(5.85,12.45,Am),(16.25,22.9,low),(23.8,32.65,F),(33.35,43.5,Cc),(44.5,54.0,Am),(55.1,58.05,F),(64.4,68.5,low),(68.85,72.95,Cc),(85.3,95.15,low),(108.0,118.2,Dm),(119.0,123.6,Am),(124.35,130.2,Cc)]
pn=[]
for a,b,ch in plan: pn.append((o2n(a) if o2n(a) is not None else 0,ch))
bounds=[0]+[o2n(a) for a,b,ch in plan[1:]]+[D]
for i,(a,b,ch) in enumerate(plan): mus+=pad(ch,bounds[i],bounds[i+1],-26)
BEAT=0.6
def arp(a,b,notes,step=BEAT,g=-30):
    i=0
    for t0 in gridt(a,b,step): mus.__iadd__(lp(pluck(t0,notes[i%len(notes)],g),1800)); i+=1
arp(4.9,18.3,[440,523.3,659.3]); arp(18.6,27.4,[349.2,440,523.3,440]); arp(27.6,43.1,[523.3,659.3,784,659.3]); arp(53.8,57.9,[523.3,659.3,784,659.3],BEAT*1.5,-32); arp(78.2,D-2,[523.3,659.3,784,659.3],BEAT,-30)
for a,b in ((49.5,53.7),(58.1,64.6),(67.8,78.0)):
    for t0 in gridt(a,b,1.3): mus.__iadd__(lp(kick(t0,-18),300))
env=np.abs(voice); k=int(0.06*SR); env=np.convolve(env,np.ones(k)/k,mode='same'); env=lp(env,6,1); env=np.clip(env/(np.percentile(env,95)+1e-6),0,1)
act=env>0.3
def rms(z): return float(np.sqrt(np.mean(z[act]**2))+1e-9)
rv=rms(voice)
mb=mus*(1-0.55*env); sb=sfx*(1-0.25*env); ab=amb*(1-0.35*env)
mb*=min(1.0,rv*db(-14)/rms(mb)); mb=0.26*vmax*np.tanh(mb/(0.26*vmax))
sb=0.42*vmax*np.tanh(sb/(0.42*vmax))
print("peaks rel voice (dB): sfx %.1f music %.1f amb %.1f"%tuple(20*np.log10(np.abs(z).max()/vmax) for z in (sb,mb,ab)))
end=np.interp(x,[0,0.1,D-1.2,D],[0,1,1,0]).astype(np.float32)
mix=np.tanh(voice+mb+sb+ab)*end
wf.write("mixC_raw.wav",SR,(np.clip(np.stack([mix,mix],1),-1,1)*32767).astype(np.int16))
mf=np.tanh(mb+sb+ab)*end; wf.write("stemC_raw.wav",SR,(np.clip(np.stack([mf,mf],1),-1,1)*32767).astype(np.int16))
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","mixC_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","mixC.wav"],check=True)
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","stemC_raw.wav","-af","loudnorm=I=-16:TP=-1.5:LRA=11","-ar","48000","stemC.wav"],check=True)
print(subprocess.run(["ffmpeg","-hide_banner","-i","mixC.wav","-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr[-200:])
