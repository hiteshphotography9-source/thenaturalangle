import numpy as np, subprocess, scipy.signal as sg, scipy.io.wavfile as wf, json, os, sys
SR=48000
M=dict(hook=0.0,swim=5.0,sing=14.5,idea=24.5,bali=37.0,isl=51.0,punch=60.5,cta=69.5,end=76.0)
if os.path.exists("marks.json"): M.update(json.load(open("marks.json")))
D=M['end']; N=int(SR*D); rng=np.random.default_rng(3)
VO=sys.argv[1] if len(sys.argv)>1 else None
def db(x): return 10**(x/20)
def tt(a,b): return np.arange(int(a*SR),int(b*SR))/SR
def place(s,t0,g=0.0):
    o=np.zeros(N,np.float32); i=int(t0*SR)
    if i<0: s=s[-i:]; i=0
    n=min(len(s),N-i)
    if n>0: o[i:i+n]=s[:n]*db(g)
    return o
def lp(x,fc,o=2): return sg.sosfilt(sg.butter(o,fc,'low',fs=SR,output='sos'),x).astype(np.float32)
def hp(x,fc,o=2): return sg.sosfilt(sg.butter(o,fc,'high',fs=SR,output='sos'),x).astype(np.float32)
def bp(x,a,b): return sg.sosfilt(sg.butter(2,[a,b],'band',fs=SR,output='sos'),x).astype(np.float32)
def nz(n): return rng.normal(0,1,n).astype(np.float32)
IR=lp(nz(int(1.8*SR))*np.exp(-np.arange(int(1.8*SR))/SR*3.4),3000)
def revt(x,w=0.4): y=sg.fftconvolve(x,IR*0.1).astype(np.float32); o=np.zeros(len(y),np.float32); o[:len(x)]+=x; o+=y*w; return o
def whoosh(t0,dur=0.7,g=-16):
    n=int(dur*SR); x=nz(n); o=np.zeros(n,np.float32); hop=int(0.02*SR); win=np.hanning(hop*2)
    for i in range(0,n-hop*2,hop):
        f=300*(3500/300)**(i/n); b=sg.butter(2,[f/1.3,f*1.3],'band',fs=SR,output='sos'); o[i:i+hop*2]+=(sg.sosfilt(b,x[i:i+hop*2])*win).astype(np.float32)
    o/=np.abs(o).max()+1e-6; e=np.sin(np.pi*np.linspace(0,1,n))**1.5; return place(lp(revt(o*e,0.3),5000),t0-0.35,g)
def boom(t0,g=-10):
    x=tt(0,2.2); s=np.sin(2*np.pi*np.cumsum(38+50*np.exp(-x*9))/SR)*np.exp(-x*1.7)+lp(nz(len(x)),220)*np.exp(-x*6)*0.6; return place(lp(revt(s.astype(np.float32),0.35),900),t0,g)
def tick(t0,g=-18): x=tt(0,0.05); return place(lp((np.sin(2*np.pi*1500*x)*np.exp(-x*90)).astype(np.float32),2800),t0,g)
def thump(t0,g=-14): x=tt(0,0.35); return place((np.sin(2*np.pi*np.cumsum(55*(1+1.5*np.exp(-x*25)))/SR)*np.exp(-x*10)).astype(np.float32),t0,g)
def riser(t0,t1,g=-18):
    d=t1-t0; x=tt(0,d); s=bp(nz(len(x)),150,2500)*np.linspace(0,1,len(x))**2.5; return place(lp(s,3000),t0,g)
def pluck(t0,f,g=-20,d=1.4):
    xx=tt(0,d); s_=(np.sin(2*np.pi*f*xx)+0.35*np.sin(2*np.pi*2*f*xx)+0.1*np.sin(2*np.pi*3*f*xx))*np.exp(-xx*3.2); return place(lp(revt(s_.astype(np.float32),0.6),3200),t0,g)
def splash(t0,g=-12,d=1.2):
    x=tt(0,d); s=bp(nz(len(x)),400,6000)*np.exp(-x*4.5)*(1+0.6*np.sin(2*np.pi*13*x)); s+=lp(nz(len(x)),300)*np.exp(-x*7)*0.8
    return place(revt(s.astype(np.float32),0.3),t0,g)
def bubbles(t0,d=1.2,g=-22):
    o=np.zeros(int(d*SR),np.float32)
    for _ in range(int(d*14)):
        st=rng.integers(0,len(o)-2400); f0=rng.uniform(500,1400); x=np.arange(2400)/SR
        o[st:st+2400]+=np.sin(2*np.pi*np.cumsum(f0*(1+x*30))/SR)*np.exp(-x*60)
    return place(o,t0,g)
def water(a,b,g=-26):
    x=tt(0,b-a); s=lp(nz(len(x)),700)*(0.6+0.4*np.sin(2*np.pi*0.18*x))+bp(nz(len(x)),1200,3000)*0.15*(0.5+0.5*np.sin(2*np.pi*0.31*x+1))
    e=np.interp(x,[0,0.8,b-a-0.8,b-a],[0,1,1,0]); return place((s*e).astype(np.float32),a,g)
def drain(t0,d=2.2,g=-16):
    x=tt(0,d); s=bp(nz(len(x)),120,900)*np.sin(np.pi*x/d)**1.2; s=lp(s,lambda_:=600) if False else lp(s,600)
    s+=np.sin(2*np.pi*np.cumsum(90-40*x/d)/SR)*0.3*np.sin(np.pi*x/d); return place(revt(s.astype(np.float32),0.4),t0,g)
def pad(fr,a,b,g=-24):
    x=tt(0,b-a+3); e=np.interp(x,[0,2,b-a,b-a+2.5],[0,1,1,0]).astype(np.float32)
    s=sum((np.sin(2*np.pi*f*x)+0.4*np.sin(2*np.pi*2*f*x+0.4))*(1+0.1*np.sin(2*np.pi*(0.07+0.011*i)*x)) for i,f in enumerate(fr)).astype(np.float32)
    return place(lp(s,1100)*e/len(fr),a,g)
T=M
OLD=dict(hook=0.0,swim=5.0,sing=14.5,idea=24.5,bali=37.0,isl=51.0,punch=60.5,cta=69.5,end=76.0)
_K=['hook','swim','sing','idea','bali','isl','punch','cta','end']
def SF(k):
    i=_K.index(k); return (M[_K[i+1]]-M[k])/(OLD[_K[i+1]]-OLD[k])
Dm=[36.7,55,73.4,87.3]; Fm=[43.7,65.4,87.3,130.8]; Am=[55,82.4,110,130.8]; C=[65.4,98,130.8,164.8]; Gm=[49,73.4,98,116.5]; Bb=[58.3,87.3,116.5,146.8]
mus=np.zeros(N,np.float32)
for a,b,ch in ((0,T['swim'],Dm),(T['swim'],T['sing'],Fm),(T['sing'],T['idea'],Am),(T['idea'],T['bali'],Gm),(T['bali'],T['isl'],Dm),(T['isl'],T['punch'],Bb),(T['punch'],T['cta'],Fm),(T['cta'],D,Dm)): mus+=pad(ch,a,b)
mel=[293.7,349.2,440,392,349.2,329.6,293.7,261.6]
for k,t0 in enumerate(np.arange(T['swim'],T['punch']-0.5,0.8)):
    mus+=pluck(t0,mel[k%8]*(0.5 if k%4==3 else 1),-29,1.0)
for t0 in np.arange(T['swim'],T['punch'],1.6): mus+=thump(t0,-27)
sfx=np.zeros(N,np.float32)
# hook
sfx+=splash(0.05,-11)+bubbles(0.3,1.5,-20)+water(0,T['swim']+0.5,-24)+riser(0.6,2.1,-17)+boom(2.1,-9)
for k in ['swim','sing','idea','bali','isl','punch','cta']: sfx+=whoosh(T[k],0.7,-15)
s=T['swim'];F=SF('swim'); sfx+=water(s,T['sing'],-27)+tick(s+F*2.6,-15)+riser(s+F*4.3,s+F*6.3,-22)+bubbles(s+F*4.6,1.6,-21)+thump(s+F*5.0,-13)+boom(s+F*7.0,-12)
s=T['sing'];F=SF('sing'); sfx+=water(s,T['idea'],-28)+tick(s+F*2.8,-16)+splash(s+F*3.4,-15,0.9)+tick(s+F*3.8,-15)+tick(s+F*6.0,-14)+riser(s+F*6.0,s+F*7.4,-20)+thump(s+F*7.4,-11)+pluck(s+F*8.2,220,-18)
s=T['idea'];F=SF('idea'); sfx+=splash(s+F*0.6,-17,1.6)+bubbles(s+F*0.8,1.6,-22)+thump(s+F*2.4,-13)
for d_ in (3.5,5.5,7.5): sfx+=tick(s+F*d_,-14)+pluck(s+F*d_,659.3,-22,0.8)
sfx+=pluck(s+F*3.6,523.3,-19)+riser(s+F*5.7,s+F*7.2,-21)
for i in range(8): sfx+=tick(s+F*7.7+i*0.05,-22)
sfx+=boom(s+F*9.2,-10)+thump(s+F*10.4,-10)+thump(s+F*10.6,-13)
s=T['bali'];F=SF('bali'); sfx+=tick(s+F*1.8,-15)+drain(s+F*2.4,2.4,-12)+tick(s+F*2.6,-15)+bubbles(s+F*4.8,1.8,-23)+riser(s+F*6.0,s+F*7.0,-20)+thump(s+F*7.0,-10)+boom(s+F*9.7,-9)+drain(s+F*11.6,1.8,-16)+tick(s+F*12.4,-14)
s=T['isl'];F=SF('isl')
for d_ in (0.9,2.3,3.7,5.1): sfx+=tick(s+F*d_,-13)+pluck(s+F*d_,440 if d_>1 else 392,-20,0.9)
sfx+=riser(s+F*5.4,s+F*6.6,-18)+boom(s+F*6.6,-9)
s=T['punch'];F=SF('punch'); sfx+=riser(s+F*1.0,s+F*2.6,-16)+boom(s+F*2.6,-8)+thump(s+F*5.5,-12)+boom(s+F*6.6,-12)
s=T['cta'];F=SF('cta'); sfx+=pluck(s+F*1.2,587.3,-18)+pluck(s+F*1.5,880,-21)+tick(s+F*2.2,-15)
x=np.arange(N)/SR
if VO:
    sr,v=wf.read(VO); v=v.astype(np.float32)/32768
    if v.ndim>1: v=v.mean(1)
    voice=np.zeros(N,np.float32); o_=int(0.5*SR); n_=min(len(v),N-o_); voice[o_:o_+n_]=v[:n_]
    def r_(a): return np.sqrt((a**2).mean())+1e-9
    act=voice[np.abs(voice)>0.01]; vr=np.sqrt((act**2).mean())
    env=np.sqrt(np.maximum(sg.fftconvolve(voice**2,np.ones(int(0.06*SR))/int(0.06*SR),'same'),0)); env=lp(env,8,1)
    duck=np.clip(1/(1+(env/(np.percentile(env,90)+1e-6))*1.6)*1.1,0.35,1)
    m2=mus*(vr*db(-19)/r_(mus)); s2=sfx*(vr*db(-7.5)/r_(sfx))
    mixed=voice+m2*duck+s2*(0.7+0.3*duck)
    out='mix_vo_raw.wav'; final='mix_vo.wav'
else:
    mixed=mus*0.8+sfx*1.0; out='mix_na_raw.wav'; final='mix_na.wav'
fin=np.tanh(mixed/ (np.abs(mixed).max()+1e-9)*1.4)/np.tanh(1.4)
end=np.interp(x,[0,0.05,D-0.8,D],[0,1,1,0]).astype(np.float32)
wf.write(out,SR,(np.clip(fin*end,-1,1)*32767).astype(np.int16))
subprocess.run(['ffmpeg','-y','-v','error','-i',out,'-af','loudnorm=I=-14:TP=-1.5:LRA=11','-ar','48000',final],check=True)
def rms(a): return 20*np.log10(np.sqrt((a**2).mean())+1e-9)
print("mus %.1f sfx %.1f"%(rms(mus*0.8),rms(sfx)))
