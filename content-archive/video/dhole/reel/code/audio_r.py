import numpy as np, subprocess, scipy.signal as sg, scipy.io.wavfile as wf, json, sys
sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/dhreel')
import rscenes as R
SR=48000; D=R.TOTAL; N=int(SR*D); rng=np.random.default_rng(3)
VO=sys.argv[1] if len(sys.argv)>1 else 'vo/VO_clean_Dhole.wav'
T=R.T
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

def whistle(t0,f0=1900,f1=2700,d=0.45,g=-16):
    x=tt(0,d); f=f0+(f1-f0)*(x/d)**0.8+30*np.sin(2*np.pi*22*x); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*np.clip(x/d,0,1))**1.2
    s=(s+0.25*np.sin(2*np.pi*np.cumsum(2*f)/SR)*0.5).astype(np.float32); return place(lp(revt(s,0.5),5000),t0,g)
def ping(t0,f=1250,g=-14):
    x=tt(0,1.6); s=np.sin(2*np.pi*f*x)*np.exp(-x*4.5)+0.5*np.sin(2*np.pi*2*f*x)*np.exp(-x*7); s=s.astype(np.float32)
    o=revt(s,0.7); return place(lp(o,6000),t0,g)
def slam(t0,g=-8):
    x=tt(0,0.9); s=np.sin(2*np.pi*np.cumsum(70*(1+1.8*np.exp(-x*22)))/SR)*np.exp(-x*7)+lp(nz(len(x)),3500)*np.exp(-x*28)*0.9
    return place(lp(revt(s.astype(np.float32),0.25),4500),t0,g)
def tick2(t0,f=1500,g=-16):
    x=tt(0,0.05); return place(lp((np.sin(2*np.pi*f*x)*np.exp(-x*90)).astype(np.float32),3500),t0,g)
def glitch(t0,g=-14,d=0.4):
    x=tt(0,d); s=bp(nz(len(x)),1500,7000)*(np.sign(np.sin(2*np.pi*38*x))*0.5+0.5)*np.exp(-x*5); return place(s.astype(np.float32),t0,g)
def chord(t0,fr,g=-20,d=2.0):
    x=tt(0,d); s=sum(np.sin(2*np.pi*f*x) for f in fr)*np.exp(-x*1.6)/len(fr); return place(lp(revt(s.astype(np.float32),0.6),3500),t0,g)
S1E=R.S1END;S2E=R.S2END;S3E=R.S3END;S4E=R.S4END;S5E=R.S5END;S6E=R.S6END;S7E=R.S7END
bounds=[0,S1E,S2E,S3E,S4E,S5E,S6E,S7E,D]
Dm=[36.7,55,73.4,87.3]; Fm=[43.7,65.4,87.3,130.8]; Am=[55,82.4,110,130.8]; Gm=[49,73.4,98,116.5]; Bb=[58.3,87.3,116.5,146.8]; Em=[41.2,61.7,82.4,98]; Cm=[65.4,98,130.8,164.8]
mus=np.zeros(N,np.float32)
for (a,b),ch in zip(zip(bounds[:-1],bounds[1:]),[Dm,Fm,Am,Gm,Em,Bb,Fm,Dm]): mus+=pad(ch,a,b)
mel=[293.7,349.2,440,392,349.2,329.6,293.7,261.6]
for k,t0 in enumerate(np.arange(5.0,D-3,1.0)): mus+=pluck(t0,mel[k%8]*(0.5 if k%4==3 else 1),-28,1.0)
sfx=np.zeros(N,np.float32)
rev=T(7.1)-0.45
# S1
sfx+=tick(0.15,-12)+tick(0.9,-12)+riser(1.3,rev,-14)+whoosh(rev,0.7,-12)+boom(rev+0.02,-6)+whistle(rev+0.5,1700,2400,0.5,-18)
for s_ in (S1E,S2E,S3E,S4E,S5E,S6E,S7E): sfx+=whoosh(s_,0.7,-12)
# S2
sfx+=tick(T(9.8)+0.9,-12)+thump(T(14.75)-0.1,-10)+tick(T(14.75)-0.1,-12)+boom(T(16.35)-0.1,-12)
for i in range(9): sfx+=tick2(T(16.35)+0.4+i*0.22,1100+i*90,-14)
# S3
sfx+=tick(T(19.45),-12)+thump(T(19.45),-11)
for i in range(7): sfx+=tick2(T(19.45)+0.4+i*0.1,1300+i*60,-16)
sfx+=boom(T(20.9)-0.05,-11)
for i in range(20): sfx+=tick2(T(20.9)+i*0.05,1400+i*20,-18)
for i,(a,b) in enumerate(((1900,2700),(1750,2500),(2000,2900))): sfx+=whistle(T(22.85)+0.2+i*1.0,a,b,0.5,-12)
# S4
ta=T(28.4); sfx+=riser(ta-0.2,ta+2.4,-15)
for i in range(14): sfx+=tick2(ta+i*0.17,700+(i%4)*120,-17)
tt_=T(32.55)-0.25; sfx+=boom(tt_,-7)+slam(tt_,-12)+riser(tt_-1.5,tt_,-17)
for i in range(6): sfx+=tick2(tt_+1.0+i*0.15,900,-15)+thump(tt_+1.2+i*0.3,-18)
# S5
tA=T(38.1); sfx+=pad([55,82.4,110],tA,tA+3,-26)
rs=T(40.55)+0.4; sfx+=riser(rs-0.2,rs+1.4,-14)
for i in range(18): sfx+=tick2(rs+i*0.08,900+i*45,-17)
sfx+=boom(rs+1.45,-8)
sfx+=slam(T(44.15),-13)
stt=T(46.55)+0.9; sfx+=slam(stt,-5)+whoosh(stt-0.2,0.4,-14)+chord(T(46.55)+2.4,[261.6,329.6,392],-14,2.0)
cs=T(52.25)+0.3
for i in range(30): sfx+=tick2(cs+i*0.07,800+i*35,-15)
sfx+=boom(cs+2.15,-8)+chord(cs+2.15,[293.7,370,440],-14,1.6)
# S6
for tp,f in ((T(59.4)-0.1,1250),(T(67.4),1480),(T(70.55),1250)): sfx+=ping(tp,f,-10)+tick(tp,-12)
sfx+=whoosh(T(59.4)+0.2,0.5,-14)+whoosh(T(65.9),0.5,-14)+whoosh(T(70.55)+0.1,0.5,-14)+thump(T(70.55),-12)+pad([220,277,330],S5E,S5E+4,-25)
# S7
sfx+=tick(T(74.65),-12)+tick(T(76.65),-12)
tc=T(79.75); sfx+=riser(tc-0.1,tc+1.0,-14)+whoosh(tc+0.1,0.8,-11)+tick2(tc+1.0,1800,-11)+tick2(tc+1.15,2200,-11)+tick2(tc+1.7,1500,-12)+tick2(tc+2.3,2400,-11)+boom(tc+2.4,-9)+pluck(tc+2.5,659.3,-16)
# S8
sfx+=tick(T(95.15),-13)+glitch(T(96.15)-0.1,-10,0.35)+boom(T(96.15),-6)+pluck(T(97.0),523.3,-14)+pluck(T(101.2),587.3,-14)+pluck(T(101.2)+0.3,880,-17)+whoosh(T(102.85),0.5,-13)+tick(T(102.85)+0.1,-12)
for i in range(5): sfx+=tick2(T(104.55)+i*0.16,1600+i*50,-13)
sfx+=chord(T(104.55)+0.9,[293.7,370,440,587],-15,3.0)
x=np.arange(N)/SR
sr,v=wf.read(VO); v=v.astype(np.float32)/32768
if v.ndim>1: v=v.mean(1)
voice=np.zeros(N,np.float32); o_=int(0.5*SR); n_=min(len(v),N-o_); voice[o_:o_+n_]=v[:n_]
def r_(a): return np.sqrt((a**2).mean())+1e-9
act=voice[np.abs(voice)>0.01]; vr=np.sqrt((act**2).mean())
env=np.sqrt(np.maximum(sg.fftconvolve(voice**2,np.ones(int(0.06*SR))/int(0.06*SR),'same'),0)); env=lp(env,8,1)
duck=np.clip(1/(1+(env/(np.percentile(env,90)+1e-6))*1.6)*1.1,0.35,1)
SFXDB=float(sys.argv[2]) if len(sys.argv)>2 else -7.5
m2=mus*(vr*db(-20)/r_(mus)); s2=sfx*(vr*db(SFXDB)/r_(sfx))
mixed=voice+m2*duck+s2*(0.7+0.3*duck)
fin=np.tanh(mixed/(np.abs(mixed).max()+1e-9)*1.5)/np.tanh(1.5)
end=np.interp(x,[0,0.05,D-1.0,D],[0,1,1,0]).astype(np.float32)
wf.write('mix_raw.wav',SR,(np.clip(fin*end,-1,1)*32767).astype(np.int16))
subprocess.run(['ffmpeg','-y','-v','error','-i','mix_raw.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-ar','48000','mix_dhole.wav'],check=True)
print("voice rms %.1f dBFS | mus %.1f | sfx %.1f"%(20*np.log10(vr),20*np.log10(r_(m2)),20*np.log10(r_(s2))))
