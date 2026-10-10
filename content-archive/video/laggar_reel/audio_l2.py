import numpy as np, subprocess, scipy.signal as sg, scipy.io.wavfile as wf
SR=48000; D=65.5; N=int(SR*D); rng=np.random.default_rng(3)
sr,v=wf.read('VO_clean_Laggar.wav'); v=v.astype(np.float32)/32768; voice=np.zeros(N,np.float32); o_=int(0.4*SR); voice[o_:o_+len(v)]=v[:N-o_]
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
starts=[0.0,4.9,9.1,14.1,20.95,28.3,36.5,40.4,44.8,49.8,56.5,65.5]
Am=[55,82.4,110,130.8]; Fm=[43.7,65.4,87.3,130.8]; Dm=[36.7,55,73.4,87.3]; Em=[41.2,61.7,82.4,98]
chs=[Am,Am,Am,Fm,Dm,Am,Fm,Fm,Em,Em,Am]
mus=np.zeros(N,np.float32)
for i,ch in enumerate(chs): mus+=pad(ch,starts[i],starts[i+1],-27)
def pluck(t0,f,g=-26,d=0.9):
    xx=tt(0,d); s_=(np.sin(2*np.pi*f*xx)+0.4*np.sin(2*np.pi*2*f*xx))*np.exp(-xx*5.5); return place(lp(revt(s_.astype(np.float32),0.5),3500),t0,g)
pent=[220,261.6,293.7,329.6,392,440,523.3]; k=0
for t0 in np.arange(2.0,63.0,0.9):
    if rng.random()<0.7: mus+=pluck(t0,pent[(k*3+int(t0))%7],-29); k+=1
amb=lp(nz(N),450)*(0.7+0.3*np.sin(2*np.pi*0.1*x))*0.05+bp(nz(N),3800,5200)*(0.5+0.5*np.sin(2*np.pi*0.2*x)**2)*0.01
def chirp(f0,f1,d): xx=tt(0,d); return (np.sin(2*np.pi*np.cumsum(np.linspace(f0,f1,len(xx)))/SR)*np.sin(np.pi*xx/d)).astype(np.float32)
t_=1.5
while t_<62:
    for j in range(rng.integers(1,3)): amb+=place(lp(chirp(rng.uniform(2800,3600),rng.uniform(2200,3000),0.12),5000),t_+j*0.2,-33)
    t_+=rng.uniform(3,6)
def shutter(t0,g=-22):
    o=np.zeros(N,np.float32)
    for dt,gg in ((0,0),(0.09,-3)):
        xx=tt(0,0.05); c=(hp(nz(len(xx)),900)*np.exp(-xx*90)+np.sin(2*np.pi*180*xx)*np.exp(-xx*60)*0.6); o+=place(lp(c.astype(np.float32),5000),t0+dt,g+gg)
    return o
sfx=np.zeros(N,np.float32)
sfx+=boom(0.1,-17)+boom(56.5,-17)
for t0 in starts[1:11]: sfx+=whoosh(t0)
for t0 in starts[:11]: sfx+=shutter(t0+0.05)
for i in range(14): sfx+=tick(9.1+0.3+i*0.1,-32)
for i in range(16): sfx+=tick(14.1+1.0+i*0.1,-26)
for i in range(22): sfx+=tick(40.4+0.3+i*0.1,-33)
sfx+=riser(9.9,11.5,-27)+riser(40.5,42.6,-28)+riser(50.2,52.5,-28)+boom(45.0,-24)
vr=20*np.log10(np.sqrt((voice[int(3*SR):int(62*SR)]**2).mean())+1e-9)
env=np.sqrt(np.maximum(sg.fftconvolve(voice**2,np.ones(int(0.06*SR))/int(0.06*SR),'same'),0)); env=lp(env,8,1)
duck=np.clip(1/(1+(env/(np.percentile(env,90)+1e-6))*1.8)*1.1,0.25,1)
sc=10**((vr-0.0)/20)/10**(-19/20)*10**(-19/20)   # relative scaling: bed/sfx stay ~19/15 dB under voice
# reference design levels were set against voice rms -19 dB; scale to actual voice level
ref=10**((vr+19)/20)*0.62
under=(mus*0.9+amb*0.6+sfx*0.8)*ref*duck
fin=voice*0.9+under
fin=np.tanh(fin*0.9)/np.tanh(0.9)
end=np.interp(x,[0,0.1,D-0.7,D],[0,1,1,0]).astype(np.float32)
wf.write('mixL2_raw.wav',SR,(np.clip(fin*end,-1,1)*32767).astype(np.int16))
subprocess.run(['ffmpeg','-y','-v','error','-i','mixL2_raw.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=9','-ar','48000','mixL2.wav'],check=True)
def rms(a,b_,c): s_=a[int(b_*SR):int(c*SR)]; return 20*np.log10(np.sqrt((s_**2).mean())+1e-9)
print("voice %.1f mus %.1f sfx %.1f ref %.2f"%(rms(voice,3,62),rms(mus*0.9*ref,3,62),rms(sfx*0.8*ref,3,62),ref))
