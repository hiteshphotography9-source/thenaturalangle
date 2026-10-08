import numpy as np, subprocess, wave, scipy.signal as sg, scipy.io.wavfile as wf
SR=48000; D=80.0; N=int(SR*D); rng=np.random.default_rng(7)
U="/root/.claude/uploads/530e917f-6900-5386-87f2-01588fc50eb7/c26843c2-Recording_36.m4a"
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",U,"-af","highpass=f=70,loudnorm=I=-15:TP=-1.5:LRA=7","-ar",str(SR),"-ac","1","vo2.wav"],check=True)
w=wave.open("vo2.wav"); vo=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
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
sfx=np.zeros(N,np.float32); mus=np.zeros(N,np.float32); amb=np.zeros(N,np.float32)
BEAT=0.6
def gridt(a,b,step): 
    t=a; 
    while t<b-1e-6: yield t; t+=step
# ----- ambience 0-18
x=tt(0,D); bed=lp(noise(N),500)*0.5*np.interp(x,[0,2,16,19.5,80],[0,1,1,0,0]).astype(np.float32); amb+=bed*db(-36)
for t0 in [1.7,3.3,5.2,8.8,10.6,13.1,14.7,16.9]:
    xx=tt(0,0.22); f=3300+900*np.sin(xx*40); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*xx/0.22)**2; amb+=place(s.astype(np.float32),t0,-42)
# ----- heart / hits
sfx+=thump(0.53,60,-6)+thump(0.83,60,-9)+impact(0.55,-12,0.6)
sfx+=whoosh(2.05,0.4,True,-16)+whoosh(2.28,0.45,False,-14)         # whip
sfx+=pop(2.45,700)+pop(3.7,820)+pop(4.65,500)+tick(3.9)+tick(4.1)+tick(4.3)
sfx+=riser(4.9,6.0,-20)+impact(6.02,-3,1.3)+glitch(6.02,-22,5)
sfx+=riser(6.45,7.35,-24)
for t0,f in ((7.45,620),(8.75,700),(9.95,780)): sfx+=pop(t0,f,-14)+ping(t0+0.05,-26,f*1.5)
sfx+=pop(10.95,300,-12)+glitch(10.95,-24,4)+whoosh(10.8,0.3,True,-24)
sfx+=whoosh(12.7,0.35,True,-16)+splash(12.9,-24)
sfx+=splash(14.22,-12)+impact(14.22,-14,0.6)+pop(14.6,800,-18)
sfx+=whoosh(15.75,0.4,True,-16)+ping(16.3,-22)+ping(17.1,-24)+ping(17.9,-26)+tick(16.4)+tick(16.6)+tick(16.8)+tick(17.0)
sfx+=impact(18.75,-9,0.9)+whoosh(18.55,0.3,True,-16)
for k,t0 in enumerate(gridt(19.0,23.9,0.09)): sfx+=tick(t0,-34-2*(k%2),1600+(k%5)*40)
sx=tt(0,4.4); sfx+=place(np.sin(2*np.pi*np.cumsum(34+34*(sx/4.4)**2)/SR)*np.sin(np.pi*sx/4.4)**2+lp(noise(len(sx)),240)*np.sin(np.pi*sx/4.4)**2*0.5,19.9,-20)
sfx+=impact(21.25,-9,0.8)+whoosh(21.15,0.3,True,-16)+riser(23.2,24.9,-24)+impact(24.9,-8,0.9)
sfx+=riser(25.0,27.0,-18)
for t0 in gridt(27.1,30.65,0.9): sfx+=thump(t0,56,-8)+thump(t0+0.28,56,-11)
sfx+=impact(30.65,-1,1.5)+ping(30.9,-20,700)+whoosh(30.6,0.3,False,-20)
sfx+=whoosh(31.95,0.3,True,-20)
sfx+=pop(32.7,700,-14)+whoosh(32.0,0.2,True,-20)
for t0 in gridt(33.1,34.65,0.045): sfx+=tick(t0,-34,1500+int((t0-33.1)*700))
sfx+=pop(36.9,700,-14)+whoosh(36.8,0.25,True,-22)
sfx+=riser(40.2,41.6,-20)+impact(41.6,-3,1.4)+glitch(41.6,-20,6)
sfx+=impact(44.8,-8,1.0)+whoosh(44.6,0.4,True,-18)+thump(45.5,70,-7)+glitch(45.5,-24,4)+thump(47.4,70,-7)+glitch(47.4,-24,4)
sfx+=impact(48.9,-5,1.1)+whoosh(48.7,0.3,True,-14)
sx=tt(0,4.9); sfx+=place(bp(noise(len(sx)),400,3200)*np.sin(np.pi*sx/4.9)**1.5,49.4,-24)
for k,t0 in enumerate(gridt(49.5,54.3,0.1)): sfx+=tick(t0,-34,1500)
sfx+=impact(52.45,-8,0.9)+whoosh(52.4,0.3,True,-18)
sfx+=pop(54.4,500,-16)+riser(55.4,58.9,-22)+impact(56.25,-12,0.6)+glitch(56.3,-22,4)
sfx+=whoosh(58.7,0.3,True,-18)+impact(59.3,-6,1.0)
sfx+=slash(63.0,-10)+thump(63.0,45,-8)
sfx+=riser(64.0,64.8,-22)+bell(64.8,-14,740)+bell(64.85,-20,1480)+pop(64.8,1000,-14)
sfx+=riser(65.8,67.3,-16)+impact(67.3,-1,1.6)
for t0 in (68.4,69.5): sfx+=impact(t0,-14,0.7)+whoosh(t0-0.2,0.25,True,-18)
sfx+=impact(70.02,-8,1.0)+pop(70.8,800,-16)+whoosh(70.0,0.2,True,-20)
sfx+=riser(75.6,77.3,-26)+bell(77.3,-14,440)+bell(77.35,-22,660)
# ----- music
Am=[110,164.8,220,261.6]; F=[87.3,130.8,174.6,220]; Cc=[130.8,196,261.6,329.6]; G=[98,146.8,196,246.9]
mus+=pad(Am,0.0,7.2,-33)+pad(Am,7.2,30.6,-31)+pad(F,12.0,18.0,-35)+pad(Cc,18.0,24.0,-35)+pad(G,24.0,27.0,-36)+pad([55,110,164.8],27.0,30.6,-33)
mus+=pad(Am,32.1,44.8,-33)+pad([110,130.8,164.8],44.8,48.9,-33)+pad(Am,48.9,58.9,-31)+pad([55,82.4,110],58.9,67.3,-31)+pad(Am,67.3,72.8,-30)+pad(F,72.8,76.5,-32)+pad(Am,76.5,80,-34)
# drums & bass patterns
def groove(a,b,kick_on=True,hat_on=True,bass_on=True,level=0.0):
    k=0
    for t0 in gridt(a,b,BEAT):
        if kick_on: mus.__iadd__(kick(t0,-11+level))
        if hat_on:
            mus.__iadd__(hat(t0+BEAT/2,-30+level,True)); mus.__iadd__(hat(t0,-35+level)); mus.__iadd__(hat(t0+BEAT/4,-38+level)); mus.__iadd__(hat(t0+3*BEAT/4,-38+level))
        if bass_on:
            f=(55,55,43.65,43.65,65.4,65.4,49,49)[(int((t0-a)/BEAT)//4)%8 if False else (int((t0-a)/BEAT/4))%4*2]
            mus.__iadd__(bassnote(t0,f,0.26,-17+level)); mus.__iadd__(bassnote(t0+BEAT/2,f,0.2,-21+level))
        k+=1
groove(7.45,12.8,True,False,False,-3)
groove(12.9,26.0,True,True,True,-2)
groove(32.2,41.5,False,True,False,-8)
groove(48.9,58.9,True,True,True,0)
groove(67.3,72.8,True,True,True,1.5)
# arps
def arp(a,b,notes,step=BEAT/2,g=-27):
    i=0
    for t0 in gridt(a,b,step): mus.__iadd__(pluck(t0,notes[i%len(notes)],g)); i+=1
Pm=[440,523.3,659.3,784,659.3,523.3]
arp(18.0,26.0,Pm,BEAT/2,-28); arp(32.2,44.8,[440,659.3,523.3,880],BEAT,-30); arp(49.0,58.0,Pm,BEAT/2,-26); arp(67.4,72.8,Pm,BEAT/2,-25); arp(72.9,78.0,[440,659.3],BEAT*2,-28)
# ----- sidechain duck from voice
env=np.abs(voice); k=int(0.06*SR); env=np.convolve(env,np.ones(k)/k,mode='same'); env=lp(env,6,1); env=np.clip(env/ (np.percentile(env,95)+1e-6),0,1)
duck=1-0.62*env
musbus=mus*duck*db(-3); ambus=amb*duck
sfxbus=sfx*(1-0.25*env)
act=env>0.3
def rms(x): return float(np.sqrt(np.mean(x[act]**2))+1e-9)
rv=rms(voice); rmu=rms(musbus); rsf=rms(sfxbus)
musbus*=min(1.0,rv*db(-13)/rmu); sfxbus*=min(1.0,rv*db(-9)/rsf)
print('rel dB music',20*np.log10(rmu/rv),'sfx',20*np.log10(rsf/rv))
mix=voice*1.0+sfxbus+musbus+ambus
x=tt(0,D); mix*=np.interp(x,[0,0.15,78.6,80.0],[0,1,1,0]).astype(np.float32)
mix=np.tanh(mix*1.05)
st=np.stack([mix,mix],1)
# gentle stereo spread of music
st[:,0]+=np.roll(musbus,300)*0.18; st[:,1]+=np.roll(musbus,-300)*0.18
wf.write("mix2_raw.wav",SR,(np.clip(st,-1,1)*32767).astype(np.int16))
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","mix2_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","mix2.wav"],check=True)
print(subprocess.run(["ffmpeg","-hide_banner","-i","mix2.wav","-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr[-380:])
