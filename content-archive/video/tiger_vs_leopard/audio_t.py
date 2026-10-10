import numpy as np, subprocess, scipy.signal as sg, scipy.io.wavfile as wf
SR=48000; D=54.1; N=int(SR*D); rng=np.random.default_rng(3)
sr,v=wf.read('orig48.wav'); v=v.astype(np.float32)/32768; voice=np.zeros(N,np.float32); voice[:min(N,len(v))]=v[:N]; voice=voice*0.5
def db(x): return 10**(x/20)
def tt(a,b): return np.arange(int(a*SR),int(b*SR))/SR
def place(s,t0,g=0.0):
    o=np.zeros(N,np.float32); i=int(t0*SR); n=min(len(s),N-i)
    if n>0: o[i:i+n]=s[:n]*db(g)
    return o
def lp(x,fc,o=2): return sg.sosfilt(sg.butter(o,fc,'low',fs=SR,output='sos'),x).astype(np.float32)
def hp(x,fc,o=2): return sg.sosfilt(sg.butter(o,fc,'high',fs=SR,output='sos'),x).astype(np.float32)
def bp(x,a,b): return sg.sosfilt(sg.butter(2,[a,b],'band',fs=SR,output='sos'),x).astype(np.float32)
def nz(n): return rng.normal(0,1,n).astype(np.float32)
IR=lp(nz(int(1.8*SR))*np.exp(-np.arange(int(1.8*SR))/SR*3.4),3000)
def revt(x,w=0.4): y=sg.fftconvolve(x,IR*0.1).astype(np.float32); o=np.zeros(len(y),np.float32); o[:len(x)]+=x; o+=y*w; return o
def whoosh(t0,dur=0.8,g=-24):
    n=int(dur*SR); x=nz(n); o=np.zeros(n,np.float32); hop=int(0.02*SR); win=np.hanning(hop*2)
    for i in range(0,n-hop*2,hop):
        f=300*(3500/300)**(i/n); b=sg.butter(2,[f/1.3,f*1.3],'band',fs=SR,output='sos'); o[i:i+hop*2]+=(sg.sosfilt(b,x[i:i+hop*2])*win).astype(np.float32)
    o/=np.abs(o).max()+1e-6; e=np.sin(np.pi*np.linspace(0,1,n))**1.5; return place(lp(revt(o*e,0.3),5000),t0-0.15,g)
def boom(t0,g=-14):
    x=tt(0,2.2); s=np.sin(2*np.pi*np.cumsum(38+50*np.exp(-x*9))/SR)*np.exp(-x*1.7)+lp(nz(len(x)),220)*np.exp(-x*6)*0.6; return place(lp(revt(s.astype(np.float32),0.35),900),t0,g)
def tick(t0,g=-28): x=tt(0,0.04); return place(lp((np.sin(2*np.pi*1500*x)*np.exp(-x*110)).astype(np.float32),2600),t0,g)
def thump(t0,g=-22): x=tt(0,0.35); return place((np.sin(2*np.pi*np.cumsum(55*(1+1.5*np.exp(-x*25)))/SR)*np.exp(-x*10)).astype(np.float32),t0,g)
def riser(t0,t1,g=-26):
    d=t1-t0; x=tt(0,d); s=bp(nz(len(x)),150,2500)*np.linspace(0,1,len(x))**2.5; return place(lp(s,3000),t0,g)
def pad(fr,a,b,g=-31):
    x=tt(0,b-a+3); e=np.interp(x,[0,2,b-a,b-a+2.5],[0,1,1,0]).astype(np.float32)
    s=sum((np.sin(2*np.pi*f*x)+0.4*np.sin(2*np.pi*2*f*x+0.4))*(1+0.1*np.sin(2*np.pi*(0.07+0.011*i)*x)) for i,f in enumerate(fr)).astype(np.float32)
    return place(lp(s,1100)*e/len(fr),a,g)
x=np.arange(N)/SR
mus=np.zeros(N,np.float32)
Am=[55,82.4,110,130.8]; Fm=[43.7,65.4,87.3,130.8]; Dm=[36.7,55,73.4,87.3]; Em=[41.2,61.7,82.4,98]
for a,b,ch in ((0,13.2,Am),(13.2,26.2,Fm),(26.2,35.2,Dm),(35.2,45.9,Em),(45.9,54.1,Am)): mus+=pad(ch,a,b,-27)
amb=lp(nz(N),500)*(0.7+0.3*np.sin(2*np.pi*0.09*x))*0.05+bp(nz(N),3800,5200)*(0.5+0.5*np.sin(2*np.pi*0.2*x)**2)*0.012
def chirp(f0,f1,d): xx=tt(0,d); return (np.sin(2*np.pi*np.cumsum(np.linspace(f0,f1,len(xx)))/SR)*np.sin(np.pi*xx/d)).astype(np.float32)
t_=1.0
while t_<52:
    for j in range(rng.integers(1,4)): amb+=place(lp(chirp(rng.uniform(2800,3900),rng.uniform(2000,3000),rng.uniform(0.08,0.2)),5000),t_+j*0.22,-33)
    t_+=rng.uniform(2.5,5.0)
def rustle(t0,g=-30): xx=tt(0,0.5); return place(lp((hp(nz(len(xx)),2500)*np.exp(-xx*9)*np.sin(np.pi*xx/0.5)).astype(np.float32),7000),t0,g)
def shutter(t0,g=-22):
    o=np.zeros(N,np.float32)
    for dt,gg in ((0,0),(0.09,-3)):
        xx=tt(0,0.05); c=(hp(nz(len(xx)),900)*np.exp(-xx*90)+np.sin(2*np.pi*180*xx)*np.exp(-xx*60)*0.6); o+=place(lp(c.astype(np.float32),5000),t0+dt,g+gg)
    return o
sfx=np.zeros(N,np.float32)
for t0 in (8.3,13.2,17.1,35.23,45.9): sfx+=whoosh(t0)
sfx+=riser(25.0,26.2,-26)+boom(26.2,-17)+whoosh(26.2)
for t0 in (1.7,2.25,2.8): sfx+=thump(t0,-17)+tick(t0+0.05)
for t0 in (27.1,27.5,27.9): sfx+=tick(t0,-26)+thump(t0,-26)
for t0 in (14.3,14.65,19.5,31.2,31.9,32.6,36.0): sfx+=tick(t0,-25)
sfx+=rustle(36.5)+rustle(40.2,-32)+rustle(43.0,-32)
sfx+=shutter(47.4)+shutter(52.0,-26)+boom(47.4,-24)
vr=20*np.log10(np.sqrt((voice[int(2*SR):int(52*SR)]**2).mean())+1e-9)
env=np.sqrt(np.maximum(sg.fftconvolve(voice**2,np.ones(int(0.06*SR))/int(0.06*SR),'same'),0)); env=lp(env,8,1)
duck=np.clip(1/(1+(env/(np.percentile(env,90)+1e-6))*1.8)*1.1,0.25,1)
ref=10**((vr+19)/20)*0.62
under=(mus*0.9+amb*0.7+sfx*0.8)*ref*duck
fin=np.tanh((voice+under)*0.9)/np.tanh(0.9)
end=np.interp(x,[0,0.1,D-0.5,D],[0,1,1,0]).astype(np.float32)
wf.write('mixT_raw.wav',SR,(np.clip(fin*end,-1,1)*32767).astype(np.int16))
subprocess.run(['ffmpeg','-y','-v','error','-i','mixT_raw.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=9','-ar','48000','mixT.wav'],check=True)
def rms(a,b_,c): s_=a[int(b_*SR):int(c*SR)]; return 20*np.log10(np.sqrt((s_**2).mean())+1e-9)
print("voice %.1f mus %.1f sfx %.1f ref %.2f"%(rms(voice,2,52),rms(mus*0.9*ref,2,52),rms(sfx*0.8*ref,2,52),ref))
