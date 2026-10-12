import numpy as np, subprocess, scipy.signal as sg, scipy.io.wavfile as wf
SR=48000; D=58.6; N=int(SR*D); rng=np.random.default_rng(3)
sr,v=wf.read('VO_clean_Dotty.wav'); v=v.astype(np.float32)/32768; voice=np.zeros(N,np.float32); o_=int(0.6*SR); voice[o_:o_+len(v)]=v[:N-o_]
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
OFF=0.6
M={'dotty':3.56,'oct':31.696,'manpur':32.804,'patrol':35.242,'natural':39.568,'left':42.106,'watch':45.794,'mom':48.272,'twocubs':30.458,'tala':27.14,'out':24.282,'d1':17.248,'kids':14.32,'y2012':6.858,'magadhi':8.506,'spotty':9.804,'sukhi':11.754,'months':43.806,'age':38.31,'seen':51.908,'comment':53.776}
T={k:v+OFF for k,v in M.items()}
SC=[6.9,13.3,T['oct'],T['left']-0.1,T['mom']-0.1]
mus=np.zeros(N,np.float32)
Am=[55,82.4,110,130.8]; Fm=[43.7,65.4,87.3,130.8]; Dm=[36.7,55,73.4,87.3]; Em=[41.2,61.7,82.4,98]; C=[65.4,98,130.8,164.8]
for a,b,ch in ((0,6.9,Dm),(6.9,13.3,Fm),(13.3,T['push'] if 'push' in T else 20.9,Am),(20.9,T['oct'],Dm),(T['oct'],T['left']-0.1,Em),(T['left']-0.1,T['mom']-0.1,Fm),(T['mom']-0.1,58.6,Am)): mus+=pad(ch,a,b,-27)
def pluck(t0,f,g=-27,d=1.4):
    xx=tt(0,d); s_=(np.sin(2*np.pi*f*xx)+0.35*np.sin(2*np.pi*2*f*xx)+0.1*np.sin(2*np.pi*3*f*xx))*np.exp(-xx*3.2); return place(lp(revt(s_.astype(np.float32),0.6),3200),t0,g)
mel=[220,261.6,329.6,293.7,261.6,246.9,220,196]
k=0
for t0 in np.arange(5.0,56.0,1.6):
    if not (T['oct']<t0<T['natural']): mus+=pluck(t0,mel[k%8],-29); k+=1
sfx=np.zeros(N,np.float32)
sfx+=riser(1.0,T['dotty'],-28)+boom(T['dotty'],-16)
for t0 in SC: sfx+=whoosh(t0)
for t0 in (T['y2012'],T['magadhi'],T['spotty'],T['sukhi'],T['kids'],T['d1'],T['twocubs'],T['months']): sfx+=tick(t0,-27)
sfx+=boom(T['out'],-22)+whoosh(T['tala'])
sfx+=boom(T['oct'],-14)
for t0 in (T['manpur']+0.6,T['patrol']+0.4,T['natural']+0.6):
    for i in range(6): sfx+=tick(t0+i*0.05,-30)
for k_,t0 in enumerate(np.arange(T['oct']+0.6,T['natural'],1.05)): sfx+=thump(t0,-26)+thump(t0+0.24,-30)
for i in range(3): sfx+=pluck(T['watch']+i*0.9,880,-30,1.0)
sfx+=pluck(T['twocubs'],659.3,-27)+pluck(T['left'],523.3,-27)
sfx+=boom(T['mom']-0.1,-22)
vr=20*np.log10(np.sqrt((voice[int(2*SR):int(55*SR)]**2).mean())+1e-9)
env=np.sqrt(np.maximum(sg.fftconvolve(voice**2,np.ones(int(0.06*SR))/int(0.06*SR),'same'),0)); env=lp(env,8,1)
duck=np.clip(1/(1+(env/(np.percentile(env,90)+1e-6))*1.8)*1.1,0.25,1)
ref=10**((vr+19)/20)*0.7
under=(mus*0.9+sfx*0.8)*ref*duck
fin=np.tanh((voice+under)*0.9)/np.tanh(0.9)
end=np.interp(x,[0,0.1,D-0.8,D],[0,1,1,0]).astype(np.float32)
wf.write('mixDT_raw.wav',SR,(np.clip(fin*end,-1,1)*32767).astype(np.int16))
subprocess.run(['ffmpeg','-y','-v','error','-i','mixDT_raw.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=9','-ar','48000','mixDT.wav'],check=True)
def rms(a,b_,c): s_=a[int(b_*SR):int(c*SR)]; return 20*np.log10(np.sqrt((s_**2).mean())+1e-9)
print("voice %.1f mus %.1f sfx %.1f"%(rms(voice,2,55),rms(mus*0.9*ref,2,55),rms(sfx*0.8*ref,2,55)))
