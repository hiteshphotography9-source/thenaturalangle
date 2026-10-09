import json
exec(open('audio_head.py').read())
TL={r[0]:(r[1],r[2]) for r in json.load(open('tl.json'))}
T=lambda k:TL[k][0]
sfx=np.zeros(N,np.float32); mus=np.zeros(N,np.float32); amb=np.zeros(N,np.float32)
x=tt(0,D)
amb+=lp(noise(N),420)*np.interp(x,[0,2,60,D],[0.7,1,1,0.5]).astype(np.float32)*db(-41)
def gridt(a,b,step):
    t=a
    while t<b-1e-6:
        yield t; t+=step
# ---- scene transitions (soft whoosh)
SCT=[T('C')-0.15,T('D')-0.15,T('G')-0.4,T('L')-0.2,T('O')-0.2,T('R')-0.3,T('S')-0.2,T('T')-0.2,T('U')-0.3,T('X')-0.3,T('AB')-0.2,T('AC')-0.2]
for t0 in SCT: sfx+=whoosh(t0-0.12,0.4,True,-24,0.3)
# ---- opening
sfx+=impact(0.12,-8,1.0)+thump(0.12,50,-6)
sfx+=riser(1.0,2.0,-26)
b0=T('B')+0.35; sfx+=thump(b0,48,-8,0.5)+thump(b0+0.28,48,-12,0.4)+thump(b0+1.6,48,-11,0.5)+thump(b0+1.88,48,-15,0.4)
# ---- C (40+)
for k,t0 in enumerate(gridt(T('C')+1.1,T('C')+2.4,0.045)): sfx+=tick(t0,-36,1300+k*35)
sfx+=pop(T('C')+1.0,600,-20)+bell(T('C')+2.45,-26,660)
# ---- D (poaching)
sfx+=riser(T('D')-0.9,T('D')+0.1,-24)+impact(T('D')+0.1,-12,0.9)+impact(T('D')+1.2,-16,0.7)
# ---- G / I / J (translocation)
g0=T('G'); i0=T('I'); j0=T('J'); j1=TL['J'][1]
for t0 in (g0+0.1,g0+2.0,g0+4.1): sfx+=ping(t0,-20,1000)+pop(t0,800,-22)
for t0 in (g0+1.9,g0+3.9,g0+5.9): sfx+=whoosh(t0-0.1,0.5,True,-26,0.3)
sfx+=bell(g0+0.05,-18,440)
for t0 in gridt(i0+0.3,i0+2.3,0.3): sfx+=thump(t0,56,-17,0.25)
sfx+=riser(j0-0.5,j0+0.3,-26)+bell(j1-0.2,-18,660)+bell(j1-0.15,-24,990)
# ---- cubs
l0=T('L'); m0=T('M'); n0=T('N')
sfx+=bell(l0+0.05,-18,523)
for i in range(4): sfx+=pop(l0+1.0+i*0.22,900+i*120,-20)
sfx+=thump(m0+0.1,46,-11,0.5)+thump(m0+0.45,46,-14,0.4)
sfx+=bell(n0+0.05,-18,659)
for i in range(4): sfx+=pop(n0+0.8+i*0.22,1000+i*120,-20)
sfx+=bell(n0+1.8,-18,880)
# ---- 2021 / 59 / 120
o0=T('O'); p0=T('P')
sfx+=impact(o0,-10,0.9)
for k,t0 in enumerate(gridt(p0+0.2,p0+1.6,0.04)): sfx+=tick(t0,-34,1200+k*30)
sfx+=pop(p0,700,-20)+bell(p0+1.65,-18,784)
for k,t0 in enumerate(gridt(p0+3.8,p0+4.9,0.04)): sfx+=tick(t0,-34,1400+k*25)
sfx+=impact(p0+4.95,-14,0.7)
# ---- leaving
r0=T('R'); sfx+=riser(r0-0.5,r0+0.4,-26)
for i in range(8): sfx+=pop(r0+0.6+i*0.28,500+i*70,-24)
sfx+=impact(r0+3.4,-14,0.7)
# ---- 99 km
s0=T('S')
for k,t0 in enumerate(gridt(s0+2.7,s0+3.6,0.04)): sfx+=tick(t0,-34,1300+k*40)
sfx+=impact(s0+3.65,-11,0.8)
# ---- T
a0=T('T'); sfx+=bell(a0+0.1,-14,523)+bell(a0+0.15,-20,784)
sfx+=riser(a0+2.4,a0+3.55,-24)+thump(a0+4.05,46,-8,0.5)+thump(a0+4.3,46,-12,0.4)
# ---- Ken-Betwa
u0=T('U'); v0=T('V'); x0=T('X')
sfx+=riser(u0-0.6,u0+0.1,-22)+impact(u0+0.05,-10,0.9)
sfx+=whoosh(u0+0.2,0.5,True,-24,0.3)+whoosh(u0+0.9,0.5,True,-24,0.3)
for t0 in (u0+1.0,u0+2.0): sfx+=ping(t0,-22,1200)
sfx+=whoosh(v0+0.3,2.4,True,-26,0.4)+ping(v0+1.4,-20,900)
sfx+=riser(x0-0.5,x0+0.1,-24)+impact(x0+0.5,-10,0.9)
# water-ish swell under the cost section
wn=bp(noise(int(8*SR)),300,2500)*np.sin(np.pi*np.linspace(0,1,int(8*SR)))**1.5; sfx+=place(wn.astype(np.float32),x0+2.0,-33)
sfx+=riser(x0+4.6,x0+5.7,-24)
for k,t0 in enumerate(gridt(x0+5.8,x0+6.9,0.04)): sfx+=tick(t0,-34,1200+k*35)
sfx+=impact(x0+5.75,-10,0.9)
# ---- close
h0=T('AB'); sfx+=bell(h0+0.05,-18,440)
c0=T('AC'); sfx+=bell(c0+0.6,-14,523)+bell(c0+0.65,-20,784)+bell(c0+0.7,-26,1046)
sfx+=impact(88.0,-12,0.8)+bell(88.05,-16,660)
# ---- music
Am=[110,164.8,220,261.6]; F=[87.3,130.8,174.6,220]; Cc=[130.8,196,261.6,329.6]; G=[98,146.8,196,246.9]; Dm=[73.4,110,146.8,174.6]
mus+=pad([55,82.4,110],0.0,T('C'),-30)+pad(Am,T('C'),T('D'),-29)+pad([55,65.4,82.4],T('D'),T('G'),-27)
mus+=pad(F,T('G'),T('L'),-29)+pad(Cc,T('L'),T('O'),-29)+pad(Am,T('O'),T('R'),-28)+pad(Dm,T('R'),T('T'),-29)
mus+=pad(F,T('T'),a0+3.5,-29)+pad([55,65.4,82.4],a0+3.5,T('U'),-27)+pad(Dm,T('U'),T('X'),-28)+pad([55,82.4,110],T('X'),T('AB'),-28)+pad(Cc,T('AB'),D,-27)
BEAT=0.6
def arp(a,b,notes,step=BEAT,g=-30):
    i=0
    for t0 in gridt(a,b,step): mus.__iadd__(pluck(t0,notes[i%len(notes)],g)); i+=1
arp(T('C')+0.4,T('D')-0.4,[440,523.3,659.3],BEAT,-31)
arp(T('G'),T('L')-0.3,[349.2,440,523.3,440],BEAT,-31)
arp(T('L'),T('O')-0.4,[523.3,659.3,784,659.3],BEAT,-31)
arp(T('O'),T('R')-0.4,[440,523.3,659.3,784],BEAT/2,-30)
arp(T('T'),a0+3.4,[349.2,440,523.3],BEAT,-31)
arp(T('AB'),D-1.0,[523.3,659.3,784,659.3],BEAT,-30)
# soft pulse in the tense parts
for a,b in ((T('D'),T('G')-0.4),(T('I'),T('J')),(a0+3.6,T('U')-0.3),(T('X'),T('X')+10)):
    for t0 in gridt(a,b,1.2): mus.__iadd__(kick(t0,-20))
# voice duck + mix
env=np.abs(voice); k=int(0.06*SR); env=np.convolve(env,np.ones(k)/k,mode='same'); env=lp(env,6,1); env=np.clip(env/(np.percentile(env,95)+1e-6),0,1)
act=env>0.3
def rms(z): return float(np.sqrt(np.mean(z[act]**2))+1e-9)
rv=rms(voice); mb=mus*(1-0.55*env); sb=sfx*(1-0.3*env); ab=amb*(1-0.6*env)
mb*=min(1.0,rv*db(-13)/rms(mb)); sb*=min(1.0,rv*db(-10)/rms(sb))
end=np.interp(x,[0,0.08,D-1.2,D],[0,1,1,0]).astype(np.float32)
musfx=np.tanh(mb+sb+ab)*end
wf.write("stem_raw.wav",SR,(np.clip(np.stack([musfx,musfx],1),-1,1)*32767).astype(np.int16))
mix=np.tanh(voice+mb+sb+ab)*end
wf.write("mix_raw.wav",SR,(np.clip(np.stack([mix,mix],1),-1,1)*32767).astype(np.int16))
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","mix_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","mix.wav"],check=True)
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","stem_raw.wav","-af","loudnorm=I=-16:TP=-1.5:LRA=11","-ar","48000","stem.wav"],check=True)
print(subprocess.run(["ffmpeg","-hide_banner","-i","mix.wav","-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr[-260:])
