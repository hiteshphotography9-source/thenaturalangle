import numpy as np, subprocess, wave, scipy.signal as sg, scipy.io.wavfile as wf
SR=48000; D=56.1667; N=int(SR*D); rng=np.random.default_rng(7)
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/7028e642-Panna_-_Tourist_vs_Photographer_-_Short_v2.mp4"
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",U,"-af","anull","-ar",str(SR),"-ac","1","orig.wav"],check=True)
w=wave.open("orig.wav"); vo=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
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

sfx=np.zeros(N,np.float32); mus=np.zeros(N,np.float32)
def gridt(a,b,step):
    t=a
    while t<b-1e-6:
        yield t; t+=step
sfx+=impact(0.0,-8,0.8)+impact(0.8,-14,0.5)+impact(1.6,-14,0.5)
sfx+=whoosh(0.7,0.2,True,-20)+whoosh(1.5,0.2,True,-20)+whoosh(2.3,0.3,True,-16)+impact(2.4,-6,1.0)+glitch(2.4,-22,4)
sfx+=impact(3.8,-8,0.9)+whoosh(3.65,0.2,True,-18)
sfx+=pop(4.4,700,-14)+pop(4.56,900,-18)+whoosh(4.3,0.2,True,-22)
sfx+=pop(9.6,700,-14)+pop(9.75,850,-16)+pop(11.6,620,-14)+whoosh(9.5,0.2,True,-22)
sfx+=riser(13.2,15.0,-22)+impact(15.0,-3,1.4)+glitch(15.0,-18,6)
for t0 in (16.87,24.2): sfx+=whoosh(t0-0.2,0.25,True,-18)+impact(t0,-12,0.6)
sfx+=riser(22.0,23.9,-22)+impact(23.9,-5,1.2)+glitch(23.95,-20,5)
for k in range(5): sfx+=tick(24.3+k*0.5,-26,900+k*70)
sfx+=whoosh(27.1,0.25,True,-18)+impact(27.27,-12,0.6)
sfx+=impact(32.0,-8,0.9)+pop(32.0,700,-14)+whoosh(31.8,0.25,True,-20)
sfx+=whoosh(35.8,0.25,True,-18)+impact(36.0,-8,0.8)+pop(36.1,500,-12)
sfx+=whoosh(37.9,0.2,True,-20)+impact(39.4,-5,1.2)+whoosh(39.2,0.25,True,-16)
sfx+=impact(42.0,-8,0.9)+riser(42.3,44.4,-22)
for k in range(24): sfx+=tick(44.4+k*(1/5.5),-18,1800 if k%2==0 else 1200)   # AF hunting beeps
sfx+=impact(44.4,-10,0.7)
sfx+=riser(47.5,48.8,-20)
sfx+=impact(48.8,-3,1.5)+bell(48.85,-14,1320)+bell(49.0,-18,1760)+pop(49.2,1200,-16)
sfx+=riser(51.5,52.9,-20)+impact(52.9,-3,1.5)+whoosh(52.7,0.3,True,-16)
sfx+=bell(53.5,-16,440)+bell(53.55,-22,660)+pop(54.4,900,-16)
Am=[110,164.8,220,261.6]; F=[87.3,130.8,174.6,220]
mus+=pad(Am,0.0,15.0,-37)+pad(F,15.0,39.4,-36)+pad(Am,39.4,56.17,-35)
for t0 in gridt(15.0,23.9,0.6): mus+=kick(t0,-14)+hat(t0+0.3,-34,True)
for t0 in gridt(39.4,48.8,0.6): mus+=kick(t0,-14)+hat(t0+0.3,-34,True)
x=np.arange(N)/SR
sfx*=np.interp(x,[0,0.05,55.4,56.1667],[1,1,1,0]).astype(np.float32)
orig=voice.copy()
mix=orig*1.0+sfx*db(-3)+mus*db(-3)
mix=np.tanh(mix*1.0)
wf.write("mix3_raw.wav",SR,(np.clip(np.stack([mix,mix],1),-1,1)*32767).astype(np.int16))
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","mix3_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","mix3.wav"],check=True)
print(subprocess.run(["ffmpeg","-hide_banner","-i","mix3.wav","-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr[-330:])
