exec(open('audio_head151.py').read())
_bell,_ping,_pop,_tick,_impact,_riser,_whoosh=bell,ping,pop,tick,impact,riser,whoosh
bell=lambda t0,g=-18,f=880: lp(_bell(t0,g-10,f),1800)
pop=lambda t0,f=700,g=-20: lp(_pop(t0,f,g-8),1800)
tick=lambda t0,g=-26,f=2200: lp(_tick(t0,g-12,f),2200)
impact=lambda t0,g=-6,big=1.0: lp(_impact(t0,g-5,big*0.7),800)
riser=lambda t0,t1,g=-18: lp(_riser(t0,t1,g-8),1500)
whoosh=lambda t0,dur=0.9,up=True,g=-14,wet=0.35: lp(_whoosh(t0,dur,up,g-6,wet),2200)
sfx=np.zeros(N,np.float32); mus=np.zeros(N,np.float32); amb=np.zeros(N,np.float32)
x=tt(0,D)
amb+=lp(noise(N),420)*np.interp(x,[0,2,125,D],[0.7,1,1,0.4]).astype(np.float32)*db(-42)
def gridt(a,b,step):
    t=a
    while t<b-1e-6: yield t; t+=step
SCT=[5.7,13.0,16.1,23.5,33.0,44.2,54.7,58.9,64.4,68.8,78.0,85.0,98.5,118.7,124.2]
for t0 in SCT: sfx+=whoosh(t0-0.15,0.45,True,-24,0.3)
sfx+=impact(0.85,-8,0.9)+thump(0.85,50,-8)
sfx+=riser(4.4,5.7,-26)+thump(7.5,48,-12,0.5)
sfx+=impact(16.4,-12,0.8)+impact(19.95,-10,0.9)
for k,t0 in enumerate(gridt(24.6,26.6,0.1)): sfx+=tick(t0,-30,1200+k*20)
for i in range(13): sfx+=pop(25.2+i*0.12,700+i*30,-24)
sfx+=thump(30.5,46,-12,0.5)
for t0,f in ((55.15,500),(56.55,560),(57.45,620)): sfx+=thump(t0,52,-12,0.4)
sfx+=riser(64.0,64.4,-26)+impact(66.0,-14,0.7)
sfx+=impact(85.4,-9,1.0)+thump(85.4,44,-9,0.7)
for t0 in (108.2,): sfx+=riser(106.5,108.2,-26)+impact(t0,-11,0.8)
sfx+=impact(119.2,-14,0.7)+impact(124.5,-14,0.7)
Am=[110,164.8,220,261.6]; F=[87.3,130.8,174.6,220]; Cc=[130.8,196,261.6,329.6]; G=[98,146.8,196,246.9]; Dm=[73.4,110,146.8,174.6]; low=[55,82.4,110]
plan=[(0,5.7,low),(5.7,16.1,Am),(16.1,23.5,low),(23.5,33.0,F),(33.0,44.2,Cc),(44.2,54.7,Am),(54.7,64.4,F),(64.4,68.8,low),(68.8,78.0,Cc),(78.0,85.0,F),(85.0,98.5,low),(98.5,118.7,Dm),(118.7,124.2,Am),(124.2,D,Cc)]
for a,b,ch in plan: mus+=pad(ch,a,b,-29)
BEAT=0.6
def arp(a,b,notes,step=BEAT,g=-33):
    i=0
    for t0 in gridt(a,b,step): mus.__iadd__(pluck(t0,notes[i%len(notes)],g)); i+=1
arp(5.7,16.0,[440,523.3,659.3]); arp(23.5,33.0,[349.2,440,523.3,440]); arp(33.0,44.0,[523.3,659.3,784,659.3]); arp(68.8,84.8,[523.3,659.3,784,659.3],BEAT*1.5,-35); arp(118.7,D-2,[523.3,659.3,784,659.3],BEAT,-33)
for a,b in ((64.4,68.8),(85.0,98.5),(108.0,118.5)):
    for t0 in gridt(a,b,1.3): mus.__iadd__(kick(t0,-22))
env=np.abs(voice); k=int(0.06*SR); env=np.convolve(env,np.ones(k)/k,mode='same'); env=lp(env,6,1); env=np.clip(env/(np.percentile(env,95)+1e-6),0,1)
act=env>0.3
def rms(z): return float(np.sqrt(np.mean(z[act]**2))+1e-9)
rv=rms(voice); mb=mus*(1-0.6*env); sb=sfx*(1-0.4*env); ab=amb*(1-0.6*env)
mb*=min(1.0,rv*db(-16)/rms(mb)); sb*=min(1.0,rv*db(-24)/rms(sb))
vmax=float(np.abs(voice).max()); cs=0.16*vmax; cm=0.26*vmax
sb=cs*np.tanh(sb/cs); mb=cm*np.tanh(mb/cm)
print("peak dB rel voice: sfx %.1f music %.1f"%(20*np.log10(np.abs(sb).max()/vmax),20*np.log10(np.abs(mb).max()/vmax)))
end=np.interp(x,[0,0.1,D-1.5,D],[0,1,1,0]).astype(np.float32)
mix=np.tanh(voice+mb+sb+ab)*end
wf.write("mix151_raw.wav",SR,(np.clip(np.stack([mix,mix],1),-1,1)*32767).astype(np.int16))
mf=np.tanh(mb+sb+ab)*end; wf.write("stem151_raw.wav",SR,(np.clip(np.stack([mf,mf],1),-1,1)*32767).astype(np.int16))
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","mix151_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=9","-ar","48000","mix151.wav"],check=True)
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i","stem151_raw.wav","-af","loudnorm=I=-16:TP=-1.5:LRA=11","-ar","48000","stem151.wav"],check=True)
print(subprocess.run(["ffmpeg","-hide_banner","-i","mix151.wav","-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr[-220:])
