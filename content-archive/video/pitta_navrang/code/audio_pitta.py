exec(open('audio_head_p.py').read())
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
def splash2(dur=1.1):
    x_=tt(0,dur); s=bp(noise(len(x_)),500,6500)*np.exp(-x_*5)+hp(noise(len(x_)),3500)*np.exp(-x_*16)*0.4
    for k in range(8):
        i=int(rng.uniform(0.05,0.6)*SR); L=int(0.05*SR); b=np.sin(2*np.pi*rng.uniform(900,2400)*x_[:L])*np.exp(-x_[:L]*70)*0.25; s[i:i+L]+=b
    return lp(revtail(s.astype(np.float32),0.3),6500)
def snap(): 
    x_=tt(0,0.25); return lp((hp(noise(len(x_)),700)*np.exp(-x_*60)+np.sin(2*np.pi*120*x_)*np.exp(-x_*40)*0.8).astype(np.float32),4500)
def hang(f,dur=2.4):
    x_=tt(0,dur); s=(np.sin(2*np.pi*f*x_)+0.35*np.sin(2*np.pi*f*2.01*x_)+0.15*np.sin(2*np.pi*f*3.02*x_))*np.exp(-x_*2.4); return revtail(lp(s.astype(np.float32),3200),0.6)

def marimba(f,dur=1.4):
    x_=tt(0,dur); s=(np.sin(2*np.pi*f*x_)*np.exp(-x_*5)+0.4*np.sin(2*np.pi*f*4*x_)*np.exp(-x_*14)); return revtail(lp(s.astype(np.float32),4200),0.4)
def rustle(dur=0.35):
    x_=tt(0,dur); return lp((hp(noise(len(x_)),2500)*np.exp(-x_*10)*np.sin(np.pi*x_/dur)).astype(np.float32),7000)
def rain(a,b,peak):
    n_=int((b-a)*SR); s=hp(noise(n_),1800)*(0.7+0.3*lp(noise(n_),5,1)/(np.abs(lp(noise(n_),5,1)).max()+1e-6)); e=np.minimum(1,np.minimum(np.arange(n_)/(0.8*SR),(n_-np.arange(n_))/(0.8*SR)))
    return place(norm_peak((lp(s,6500)*e).astype(np.float32),peak*vmax),a,0.0)
def ploc(t0,pk): return at(rustle(),t0,pk)
# ambience: forest floor (soft wind, insects, small birds), rain in map beat
wn=lp(noise(N),500)*(0.7+0.3*np.sin(2*np.pi*0.09*x)); amb+=norm_peak(wn.astype(np.float32),0.03*vmax)
ins=bp(noise(N),3800,5600)*(0.5+0.5*np.sin(2*np.pi*0.25*x+1)**2)*(0.6+0.4*np.sign(np.sin(2*np.pi*30*x))); amb+=norm_peak(ins.astype(np.float32),0.02*vmax)*np.interp(x,[0,3,20,21,27,34],[0.7,1,1,0.3,0.3,0.9]).astype(np.float32)
t=0.8
while t<D-3:
    if not (21.0<t<27.5):
        for k in range(rng.integers(1,4)): amb+=at(chirp(rng.uniform(2800,3900),rng.uniform(2000,3000),rng.uniform(0.08,0.2)),t+k*rng.uniform(0.16,0.3),0.05)
    t+=rng.uniform(2.8,5.5)
amb+=rain(21.0,27.8,0.10)
# music: bright D major wonder with marimba arp
Dm=[73.4,110,146.8,185]; Bm=[61.7,92.5,123.5,185]; G=[98,146.8,196,246.9]; A=[55,110,164.8,220]
for a,b,ch in ((0,3,[55,82.4,110]),(3,9,Dm),(9,15,Bm),(15,21,G),(21,27.5,[73.4,110,146.8,174.6]),(27.5,D,Dm)): mus+=pad(ch,a,b,-27)
pent=[293.7,329.6,370,440,493.9,587.3,659.3,740,880]
i=0
for t0 in gridt(3.0,21.0,0.6):
    mus+=place(norm_peak(marimba(pent[(i*2)%5+ (1 if i%3==0 else 0)]),0.05*vmax),t0,0.0); i+=1
for t0 in gridt(21.5,27.0,1.2): mus+=place(norm_peak(marimba(pent[(int(t0*3))%4]),0.045*vmax),t0,0.0)
for t0 in gridt(27.7,33.0,0.6): mus+=place(norm_peak(marimba(pent[(int(t0*5))%6]),0.055*vmax),t0,0.0)
# sfx
sfx+=at(riser_s(0.5),0.0,0.10)+at(boom(),0.2,0.30)
sfx+=at(splash2(0.35),1.5,0.12) if False else at(rustle(0.5),1.5,0.20)
for t0 in (3.0,9.0,15.0,21.0,27.5): sfx+=at(softwhoosh(),t0-0.25,0.18)
sfx+=at(boom(),9.0,0.24)
SWT=[3.8,4.8,5.8,6.8,7.8,8.5,10.2,11.6,12.9]
for i,t0 in enumerate(SWT): sfx+=at(marimba(pent[i%9],1.0),t0,0.17)+at(tick_soft(),t0,0.07)
for t0 in (0.2,3.1,9.1,15.1,27.7): sfx+=at(tick_soft(),t0,0.14)
sfx+=at(rustle(0.4),16.6,0.14)+at(rustle(0.4),17.0,0.12)
sfx+=at(snap(),17.9,0.18)+at(tick_soft(),18.0,0.2)+at(marimba(587.3,0.8),18.05,0.12)
sfx+=at(riser_s(0.7),20.3,0.10)
sfx+=at(boom(),21.3,0.18)
for t0 in (22.6,25.4): sfx+=at(softwhoosh(0.9),t0-0.1,0.16)
sfx+=at(boom(),27.7,0.26)
for i in range(9): sfx+=at(marimba(pent[i],1.2),27.7+i*0.12,0.14)
mb=0.30*vmax*np.tanh(mus/(0.30*vmax)); sb=0.45*vmax*np.tanh(sfx/(0.45*vmax)); ab=amb
print("peaks: sfx %.1f music %.1f amb %.1f"%tuple(20*np.log10(np.abs(z).max()/vmax) for z in (sb,mb,ab)))
end=np.interp(x,[0,0.15,D-1.0,D],[0,1,1,0]).astype(np.float32)
mix=np.tanh(mb+sb+ab)*end
wf.write("mixP_raw.wav",SR,(np.clip(np.stack([mix,mix],1),-1,1)*32767).astype(np.int16))
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","mixP_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","mixP.wav"],check=True)
print(subprocess.run(["ffmpeg","-hide_banner","-i","mixP.wav","-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr[-140:])
