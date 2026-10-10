import numpy as np, subprocess, scipy.signal as sg, scipy.io.wavfile as wf
SR=48000; D=52.55; N=int(SR*D); rng=np.random.default_rng(3)
sr,v=wf.read('orig48.wav'); v=v.astype(np.float32)/32768; voice=np.zeros(N,np.float32); o=int(1.5*SR); voice[o:o+len(v)]=v[:N-o]; voice=np.clip(voice,-0.89,0.89)
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
mus=np.zeros(N,np.float32)
Am=[55,82.4,110,130.8]; Fm=[43.7,65.4,87.3,130.8]; Dm=[36.7,55,73.4,87.3]; Em=[41.2,61.7,82.4,98]
for a,b,ch in ((0,11.4,Am),(11.4,26.1,Fm),(26.1,36.0,Dm),(36.0,45.5,Em),(45.5,52.55,Am)): mus+=pad(ch,a,b,-30)
for k,t0 in enumerate(np.arange(36.2,45.4,0.95)): mus+=thump(t0,-27+k*0.35)+thump(t0+0.22,-31+k*0.35)
sfx=np.zeros(N,np.float32)
sfx+=riser(0.0,1.45,-25)+boom(1.5,-15)
for t0 in (11.4,26.1,36.0,45.5): sfx+=whoosh(t0)
sfx+=thump(11.43,-17)+thump(26.13,-17)
for t0 in (15.3,): sfx+=tick(t0)+tick(t0+0.15,-31)
for t0 in np.arange(27.0,45.0,1.0): sfx+=tick(t0,-34)
for t0 in (46.2,46.35,46.5): sfx+=tick(t0,-28)
sfx+=boom(36.0,-19)
env=np.sqrt(np.maximum(sg.fftconvolve(voice**2,np.ones(int(0.06*SR))/int(0.06*SR),'same'),0)); env=lp(env,8,1)
duck=1/(1+(env/(np.percentile(env,90)+1e-6))*1.6)
under=(mus*0.9+sfx*0.7)*np.clip(duck*1.1,0.3,1)
fin=np.tanh((voice+under)*0.9)/np.tanh(0.9)
end=np.interp(np.arange(N)/SR,[0,0.1,D-0.5,D],[0,1,1,0]).astype(np.float32)
wf.write('mixS_raw.wav',SR,(np.clip(fin*end,-1,1)*32767).astype(np.int16))
subprocess.run(['ffmpeg','-y','-v','error','-i','mixS_raw.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=9','-ar','48000','mixS.wav'],check=True)
def rms(x,a,b): s_=x[int(a*SR):int(b*SR)]; return 20*np.log10(np.sqrt((s_**2).mean())+1e-9)
print("voice %.1f mus %.1f sfx %.1f"%(rms(voice,2,50),rms(mus*0.9,2,50),rms(sfx*0.7,2,50)))
