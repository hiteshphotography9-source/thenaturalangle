import numpy as np, subprocess, scipy.signal as sg, scipy.io.wavfile as wf
SR=48000; D=86.0; N=int(SR*D); rng=np.random.default_rng(21)
def tt(a,b): return np.arange(int(a*SR),int(b*SR))/SR
def db(x): return 10**(x/20)
def place(s,t0,g=0.0,buf=None):
    out=np.zeros(N,np.float32); i=int(t0*SR)
    if i<0 or i>=N: return out
    s=(s*db(g)).astype(np.float32); n=min(len(s),N-i); out[i:i+n]=s[:n]; return out
def lp(x,fc,o=2): return sg.sosfilt(sg.butter(o,fc,'low',fs=SR,output='sos'),x).astype(np.float32)
def hp(x,fc,o=2): return sg.sosfilt(sg.butter(o,fc,'high',fs=SR,output='sos'),x).astype(np.float32)
def bp(x,a,b): return sg.sosfilt(sg.butter(2,[a,b],'band',fs=SR,output='sos'),x).astype(np.float32)
def nz(n): return rng.normal(0,1,n).astype(np.float32)
IR=(rng.normal(0,1,int(SR*1.6))*np.exp(-np.arange(int(SR*1.6))/SR*3.2)).astype(np.float32)
def rev(x,w=0.5): y=sg.fftconvolve(x,IR*0.08)[:len(x)].astype(np.float32); return x*(1-w*0.3)+y*w
def whoosh(t0,dur=0.6,g=-16):
    x=tt(0,dur); e=np.sin(np.pi*x/dur)**1.6; s=bp(nz(len(x)),300,5000)*e; s=lp(s,np.linspace(1200,6000,1)[0]); return place(s,t0,g)
def impact(t0,g=-8):
    x=tt(0,1.2); s=np.sin(2*np.pi*np.cumsum(55*(1+2.2*np.exp(-x*14)))/SR)*np.exp(-x*3.4)+0.3*lp(nz(len(x)),400)*np.exp(-x*6); return place(s,t0,g)
def pop(t0,g=-14,f=620):
    x=tt(0,0.12); s=np.sin(2*np.pi*np.cumsum(f*(1+1.4*np.exp(-x*40)))/SR)*np.exp(-x*38); return place(s,t0,g)
def click(t0,g=-22): x=tt(0,0.02); return place(hp(nz(len(x)),3500)*np.exp(-x*200),t0,g)
def ping(t0,f=880,g=-18,dec=3.0):
    x=tt(0,1.6); s=(np.sin(2*np.pi*f*x)+0.3*np.sin(2*np.pi*2*f*x))*np.exp(-x*dec); return place(s,t0,g)
def thump(t0,g=-12,f=60):
    x=tt(0,0.5); return place(np.sin(2*np.pi*np.cumsum(f*(1+1.5*np.exp(-x*25)))/SR)*np.exp(-x*9),t0,g)
def chirp(t0,f0=3200,f1=4800,dur=0.12,g=-30):
    x=tt(0,dur); f=f0+(f1-f0)*(x/dur); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*x/dur)**1.2; return place(s,t0,g)
def trill(t0,g=-30,n=None):
    n=n or int(rng.integers(2,6)); b=np.zeros(N,np.float32); f=rng.uniform(2600,4200)
    for k in range(n): b+=chirp(t0+k*0.16,f+rng.uniform(-300,300),f+rng.uniform(600,1600),0.11,g)
    return b
def riser(t0,t1,g=-18):
    d=t1-t0; x=tt(0,d); s=bp(nz(len(x)),200,3500)*np.linspace(0,1,len(x))**2.5; return place(lp(s,4000),t0,g)
def env(points):
    xs=[p[0] for p in points]; ys=[p[1] for p in points]; return np.interp(np.arange(N)/SR,xs,ys).astype(np.float32)

xx=np.arange(N)/SR
def kick(t0,g=-9): return thump(t0,g,58)
def hat(t0,g=-30): x=tt(0,0.05); return place(hp(nz(len(x)),6500)*np.exp(-x*80),t0,g)
def clap(t0,g=-24): x=tt(0,0.18); return place(bp(nz(len(x)),1200,5000)*np.exp(-x*22),t0,g)
def sub(t0,f,dur,g=-14): x=tt(0,dur); return place(np.sin(2*np.pi*f*x)*np.exp(-x*1.2)*np.minimum(1,x/0.02),t0,g)
# ambience
amb=bp(nz(N),150,700)*(0.5+0.5*np.sin(2*np.pi*xx/3.3)).astype(np.float32)*0.25+bp(nz(N),300,1200)*(0.5+0.5*np.sin(2*np.pi*xx/9.0+1)).astype(np.float32)*0.12
birds=np.zeros(N,np.float32); t=0.3
while t<3.2: birds+=trill(t+rng.uniform(0,0.4),-28); t+=rng.uniform(0.5,1.0)
t=78.0
while t<85.0: birds+=trill(t,-30); t+=rng.uniform(0.7,1.4)
birds+=trill(7.4,-32,3)
amb_env=env([(0,0.0),(0.3,1),(2.8,1),(5.0,0.12),(77.5,0.12),(78.5,0.6),(82,1),(85,1),(86,0)])
amb=(amb+birds)*amb_env
# drone and pads
dr=np.zeros(N,np.float32)
for f,g in ((55.0,1.0),(82.4,0.6),(110.0,0.4)):
    for det in (-0.7,0.0,0.8): dr+=(g*(2*((f*(1+det*0.003)*xx)%1.0)-1)).astype(np.float32)/3
dr=lp(dr,300)*(0.7+0.3*np.sin(2*np.pi*xx/11.0)).astype(np.float32)+(0.4*np.sin(2*np.pi*36.7*xx)).astype(np.float32)
pad=np.zeros(N,np.float32)
for f in (146.8,155.6,207.7): pad+=(np.sin(2*np.pi*f*xx)+0.2*np.sin(2*np.pi*2*f*xx)).astype(np.float32)
pad=lp(pad,1400)*0.1
hope=np.zeros(N,np.float32)
for f in (146.8,220.0,277.2,370.0): hope+=(np.sin(2*np.pi*f*xx)+0.15*np.sin(2*np.pi*2*f*xx)).astype(np.float32)
hope=lp(hope,1800)*0.09
CH=[19,32,45,64]
dro=[(0,0),(2.8,0),(3.4,0.8),(7.0,0.8),(7.4,0.2),(8.3,0.2),(8.8,0.8)]
for c in CH: dro+=[(c-0.05,0.8),(c,0.15),(c+1.3,0.15),(c+1.5,0.8)]
dro=sorted(dro)+[(75.5,0.8),(77,0.1),(86,0)]
dr_env=env(sorted(set(dro)))
pad_env=env([(0,0),(13,0),(18,1),(19,0.3),(20.3,1),(33,0.8),(46,0.6),(76,0.8),(77.5,0),(86,0)])
hope_env=env([(0,0),(76,0),(78,0.7),(84,1),(86,0)])
bed=dr*dr_env*0.8+pad*pad_env+hope*hope_env+amb
# driving beat 96 bpm, on in the right windows
BPM=96; beat=60/BPM
def beat_on(t):
    if t<3.4 or 7.2<=t<8.8 or t>=76.5: return False
    for c in CH:
        if c-0.1<=t<c+1.5: return False
    return True
bt=np.zeros(N,np.float32); t=3.4; b=0; root=[36.7,36.7,43.65,41.2]
while t<76:
    if beat_on(t):
        if b%4 in (0,2): bt+=kick(t,-8)
        if b%4 in (1,3): bt+=clap(t,-24)
        bt+=hat(t,-31)+hat(t+beat/2,-29)
        if b%8==0: bt+=sub(t,root[(b//8)%4]*2,beat*7,-12)
    t+=beat; b+=1
bed+=bt*0.8
hiss=hp(nz(N),2500)*0.03*env([(0,0),(14.5,0),(18,0.6),(19,0.2),(21,0.7),(32,0.7),(33,0),(76,0),(78,0.3),(82,0)]); bed+=hiss
# ---------------- sfx
sfx=np.zeros(N,np.float32)
BEATSTART=[8,20.3,23.8,26.8,29.8,33.3,36.5,40.5,46.3,55.0,65.3,76]
for a in BEATSTART: sfx+=whoosh(a-0.05,0.4,-17)
for c in CH: sfx+=riser(c-0.7,c,-20)+whoosh(c-0.05,0.5,-12)+impact(c+0.05,-9)+pop(c+0.2,-14,520)+whoosh(c+1.1,0.4,-16)
sfx+=riser(2.4,3.3,-22)+impact(3.3,-9)
t=3.4
while t<8.3:
    dens=2+28*min(1,(t-3.4)/1.4) if t<5.0 else (14 if t<7.2 else 6)
    sfx+=click(t,-20); t+=rng.exponential(1.0/dens)
sfx+=impact(5.3,-8)+thump(5.3,-6,45)+pop(5.9,-14,420)+ping(6.0,330,-16,2.0)+whoosh(7.1,0.5,-18)
for tp,f in ((9.6,880),(10.7,990),(11.8,1100),(12.9,1245)): sfx+=ping(tp,f,-16)+pop(tp,-18,700)
sfx+=pop(13.6,-18,520)+riser(14.5,16.8,-20)+impact(16.8,-8)
for t0 in (23.9,26.9,29.9,36.6): sfx+=pop(t0,-13,540)+thump(t0,-9,52)+click(t0+0.02,-20)
sfx+=pop(24.6,-18,700)+pop(27.6,-18,700)+pop(30.6,-18,700)+pop(37.6,-18,700)
t=33.5
while t<36.4: sfx+=pop(t,-24,rng.uniform(300,900))+(ping(t+0.05,rng.uniform(1100,1700),-30,6.0) if rng.random()<0.4 else 0); t+=rng.exponential(0.2)
for k in range(17): sfx+=click(40.8+k*0.077,-22)
sfx+=pop(42.1,-12,500)+impact(42.1,-9)+thump(42.1,-6,45)
for t0 in (46.7,55.4):
    for k in range(20): sfx+=click(t0+k*0.05,-24)
for t0,t1 in ((48.5,49.7),(57.2,58.4)):
    x=tt(0,t1-t0); sw=np.sin(2*np.pi*np.cumsum(900*(1-0.75*x/(t1-t0)))/SR)*np.exp(-x*1.6)*0.35; sfx+=place(sw,t0,-18)
sfx+=impact(49.7,-8)+impact(58.4,-8)+thump(49.7,-6,45)+thump(58.4,-6,45)
for i in range(4): sfx+=pop(66.3+i*1.1,-14,500+i*60)+click(66.32+i*1.1,-20)
sfx+=whoosh(71.2,0.4,-18)+pop(71.4,-16,600)
sfx+=impact(76.2,-10)+pop(79.2,-14,640)+pop(79.5,-14,720)+ping(79.6,1320,-18,2.5)+whoosh(84.6,0.5,-20)
bed=rev(bed,0.12); sfx=rev(sfx,0.2)
def rm(a): return np.sqrt((a**2).mean())+1e-9
bedn=bed/rm(bed)*db(-26); sfxn=sfx/rm(sfx)*db(-21)
mix=bedn+sfxn; fade=env([(0,0),(0.05,1),(84.8,1),(86,0)]); mix=np.tanh(mix*1.3)/np.tanh(1.3)*fade
def w(name,x,ln=False):
    x=np.clip(x,-1,1); wf.write(name+'_raw.wav',SR,(x*32767).astype(np.int16))
    af='loudnorm=I=-14:TP=-1.5:LRA=9' if ln else 'volume=1'
    subprocess.run(['ffmpeg','-y','-v','error','-i',name+'_raw.wav','-af',af,'-ar','48000',name+'.wav'],check=True)
w('mix',mix,True); w('bed',np.tanh(bedn*1.3)/np.tanh(1.3)*fade*2.2,True)
print('ok',D)
