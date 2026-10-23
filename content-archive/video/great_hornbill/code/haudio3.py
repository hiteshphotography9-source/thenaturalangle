import numpy as np, subprocess, scipy.signal as sg, scipy.io.wavfile as wf, json, sys
sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/hornbill')
import hscenes3 as F
SR=48000; D=F.TOTAL; N=int(SR*D); rng=np.random.default_rng(3)
VO=sys.argv[1] if len(sys.argv)>1 and sys.argv[1]!="none" else None
SFXDB=float(sys.argv[2]) if len(sys.argv)>2 else -7.5
def AT(n,lt): return F.START[n]+lt
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

def chirp(t0,f0=3000,f1=4600,d=0.07,g=-14):
    x=tt(0,d); f=f0+(f1-f0)*x/d; s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*x/d)**1.5; return place(s.astype(np.float32),t0,g)
def cricket(a,b,g=-30,rate=5.2):
    o=np.zeros(N,np.float32)
    for t0 in np.arange(a,b,1/rate):
        x=tt(0,0.05); s=np.sin(2*np.pi*4300*x)*(0.5+0.5*np.sin(2*np.pi*90*x))*np.sin(np.pi*x/0.05); o+=place(s.astype(np.float32),t0+rng.uniform(0,0.05),g)
    return o
def rustle(t0,d=0.25,g=-18): x=tt(0,d); s=bp(nz(len(x)),1800,7000)*np.sin(np.pi*x/d)**2*(0.6+0.4*np.sign(np.sin(2*np.pi*30*x))); return place(s.astype(np.float32),t0,g)
def crunch(t0,g=-14): x=tt(0,0.18); s=bp(nz(len(x)),600,5000)*np.exp(-x*28)*(1+np.sign(np.sin(2*np.pi*55*x))*0.6); return place(s.astype(np.float32),t0,g)
def buzz(t0,d=0.5,g=-18): x=tt(0,d); s=np.sin(2*np.pi*210*x)*(0.5+0.5*np.sin(2*np.pi*38*x))*np.sin(np.pi*x/d); return place(lp(s.astype(np.float32),2500),t0,g)
def popf(t0,f=900,g=-14): x=tt(0,0.12); s=np.sin(2*np.pi*np.cumsum(f*(1+2*np.exp(-x*40)))/SR)*np.exp(-x*30); return place(s.astype(np.float32),t0,g)
def windy(a,b,g=-30):
    x=tt(0,b-a); s=bp(nz(len(x)),180,1200)*(0.55+0.45*np.sin(2*np.pi*0.13*x+1)); e=np.interp(x,[0,1.5,b-a-1.5,b-a],[0,1,1,0]); return place((s*e).astype(np.float32),a,g)
def sand(a,b,g=-24,every=0.33):
    o=np.zeros(N,np.float32)
    for t0 in np.arange(a,b,every): o+=rustle(t0+rng.uniform(0,0.1),rng.uniform(0.12,0.22),g+rng.uniform(-3,2))
    return o


def chuff(t0,n=6,rate=2.2,g=-14):
    o=np.zeros(N,np.float32)
    for i in range(n):
        x=tt(0,0.22); s=bp(nz(len(x)),90,900)*np.exp(-x*18)*(1-np.exp(-x*160)); s+=0.5*np.sin(2*np.pi*70*x)*np.exp(-x*20)
        o+=place(lp(s.astype(np.float32),1400),t0+i/rate/(1+0.06*i),g)
    return o
def knock(t0,g=-10):
    x=tt(0,0.12); s=np.sin(2*np.pi*190*x)*np.exp(-x*45)+0.6*bp(nz(len(x)),400,3000)*np.exp(-x*60); return place(s.astype(np.float32),t0,g)
ST=F.START; ORD=F.ORDER; PV=F.PV
def pv(i,o=0.0): return PV[i][0]+o
ENT=ORD[:-1]
mus=np.zeros(N,np.float32)
Am=[55,82.4,110,130.8]; Dm=[73.4,110,146.8]; Fm=[87.3,130.8,174.6]; Em=[82.4,123.5,164.8]; Gm=[49,73.4,98,123.5]
padmap={"S1":Am,"S2":Gm,"S3":Am,"S4":Em,"S5":Dm,"S6":Fm,"S7":Em,"S8":Fm,"S9":Am}
for i,n in enumerate(ENT): mus+=pad(padmap[n],ST[n],ST[ORD[i+1]],-22)
mel=[220,261.6,329.6,293.7,261.6,220,196,220,329.6,392,329.6,293.7]; k=0
for t0 in np.arange(1.0,D-3,1.0): mus+=pluck(t0,mel[k%len(mel)]*(0.5 if k%6==5 else 1),-27,1.4); k+=1
sfx=np.zeros(N,np.float32)
for n in ENT[1:]: sfx+=whoosh(ST[n],0.6,-12)
sfx+=windy(0,D,-31)+cricket(0.5,D-1,-33)
rng2=np.random.default_rng(11)
for t0 in sorted(rng2.uniform(1,D-2,16)): sfx+=chirp(t0,2600+rng2.uniform(0,1500),3800+rng2.uniform(0,1500),0.09,-27)
# S1
sfx+=riser(0.1,pv(0),-16)+boom(pv(0),-9)+tick(pv(0,1.0),-12)+tick(pv(1),-12)+boom(pv(1,0.9),-8)+tick(pv(2),-12)+pluck(pv(2,0.1),220,-14)
# S2
sfx+=tick(pv(3),-13)+tick(pv(4),-13)+knock(pv(5,0.4),-12)+riser(pv(5),pv(5,2.2),-19)+thump(pv(5,2.2),-11)+thump(pv(5,2.7),-14)
for o in (1.6,4.4): sfx+=ping(pv(6,o),1250,-12)+tick(pv(6,o),-12)
sfx+=pluck(pv(6,6.0),196,-14)
# S3
for i,o in enumerate((pv(7),pv(8),pv(11,-0.2))): sfx+=tick(o,-12)+ping(o+0.05,1480,-15)
sfx+=chuff(pv(8,0.2),6,2.4,-12)+pluck(pv(12,0.2),246.9,-14)
# S4
sfx+=tick(pv(13),-13)+boom(pv(13),-10)+tick(pv(15),-12)+riser(pv(15,1.0),pv(15,1.8),-15)+knock(pv(15,1.8),-7)+slam(pv(15,1.8),-12)+knock(pv(15,2.15),-10)+glitch(pv(15,1.8),-18,0.3)
sfx+=tick(pv(16),-12)+tick(pv(16,1.0),-14)+pluck(pv(16,1.5),329.6,-14)
# S5
ob=pv(18,0.0)
for o,f_ in ((0.2,1000),(1.9,1150),(3.3,1300)): sfx+=riser(ob+o-0.2,ob+o+0.5,-19)+ping(ob+o+0.9,f_,-12)
for o in (2.4,3.6): sfx+=ping(ob+o,1568,-12)
sfx+=tick(pv(17),-13)+tick(pv(19),-12)+boom(pv(19,1.3),-8)+tick(pv(19,2.0),-12)
# S6
sfx+=tick(pv(20),-13)+tick(pv(21),-12)
for i in range(5): sfx+=popf(pv(22,-0.2+i*0.1),700+i*60,-17)
sfx+=chuff(pv(22,0.6),6,2.8,-13)+tick(pv(22),-12)+ping(pv(23,1.0),700,-12)+tick(pv(23,0.7),-12)+riser(pv(24),pv(24,2.6),-19)+chord(pv(24,2.6),[392,493.9,587.3],-15,2.4)+tick(pv(24,0.8),-12)+pluck(pv(24,2.8),392,-14)
# S7
sfx+=tick(pv(26),-13)+boom(pv(26),-8)+tick(pv(27),-12)+thump(pv(28),-9)+thump(pv(28,1.0),-9)+pluck(pv(28,1.8),164.8,-14)
# S8
sfx+=tick(pv(29),-13)+chord(pv(30),[349.2,440,523.3],-14,3.0)+tick(pv(31),-12)
for i in range(10): sfx+=tick2(pv(32,i*0.09),1300+i*60,-18)
for i in range(14): sfx+=tick2(pv(33,1.0+i*0.115),1000+i*50,-19)
sfx+=ping(pv(32,0.9),1568,-12)+ping(pv(33,2.6),1760,-12)+tick(pv(33),-12)+ping(pv(34),1320,-13)+pluck(pv(34,1.2),392,-14)
# S9
sfx+=tick(pv(35),-13)+tick(pv(35,1.3),-12)+slam(pv(36),-10)+tick(pv(38),-11)+ping(pv(38,0.3),1320,-13)+chord(pv(38),[220,277.2,329.6],-15,3.5)
x=np.arange(N)/SR
def r_(a): return np.sqrt((a**2).mean())+1e-9
if VO:
    sr,v=wf.read(VO); v=v.astype(np.float32)/32768
    if v.ndim>1: v=v.mean(1)
    voice=np.zeros(N,np.float32); o_=int(0.5*SR); n_=min(len(v),N-o_); voice[o_:o_+n_]=v[:n_]
    act=voice[np.abs(voice)>0.01]; vr=np.sqrt((act**2).mean())
    env=np.sqrt(np.maximum(sg.fftconvolve(voice**2,np.ones(int(0.06*SR))/int(0.06*SR),'same'),0)); env=lp(env,8,1)
    duck=np.clip(1/(1+(env/(np.percentile(env,90)+1e-6))*1.6)*1.1,0.35,1)
    m2=mus*(vr*db(-20)/r_(mus)); s2=sfx*(vr*db(SFXDB)/r_(sfx)); mixed=voice+m2*duck+s2*(0.7+0.3*duck); out='fx_vo_raw.wav'; final='mix_vo.wav'
else:
    m2=mus*(db(-24)/r_(mus)); s2=sfx*(db(-20)/r_(sfx)); mixed=m2+s2; out='fx_na_raw.wav'; final='mix_na.wav'
fin=np.tanh(mixed/(np.abs(mixed).max()+1e-9)*1.5)/np.tanh(1.5)
end=np.interp(x,[0,0.05,D-1.2,D],[0,1,1,0]).astype(np.float32)
wf.write(out,SR,(np.clip(fin*end,-1,1)*32767).astype(np.int16))
subprocess.run(['ffmpeg','-y','-v','error','-i',out,'-af','loudnorm=I=-14:TP=-1.5:LRA=11','-ar','48000',final],check=True)
print("mus %.1f sfx %.1f dBFS"%(20*np.log10(r_(m2)),20*np.log10(r_(s2))))
