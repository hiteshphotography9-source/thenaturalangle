import numpy as np, scipy.io.wavfile as w, noisereduce as nr, json, subprocess
sr,x=w.read('raw48.wav'); x=x.astype(np.float32)/32768
prof=np.concatenate([x[int(9.4*sr):int(11.6*sr)],x[int(0.2*sr):int(1.3*sr)]])
x=nr.reduce_noise(y=x,sr=sr,y_noise=prof,prop_decrease=0.75,stationary=True,n_fft=2048)
# (src_start, src_end, label, gap_before_s)   boundaries sit inside >=0.2 s silences
P=[(1.45,2.40,"Ye hai S3",0),(2.75,3.65,"isse Surai 3",0.20),(3.90,5.25,"aur Monarch bhi kaha jaata hai",0.20),(6.30,8.75,"Pilibhit ke sabse bade baaghon mein se ek",0.28),
   (12.40,18.30,"Local guides ke mutabik vazan 280-300 kilo, lambai lagbhag 10 feet",0.42),(18.85,20.40,"lekin ye official naap nahi hai",0.22),(21.95,24.75,"S3 ki umar 6-7 saal",0.30),
   (80.40,82.60,"S3 ka sabse bada rival S2 hai",0.42),(85.50,86.70,"local guides ke mutabik",0.22),(87.05,89.35,"dono ke beech ilaake ki jung",0.20),
   (90.05,92.90,"Kehte hain ek baar S2 ne S3 par hamla kiya",0.42),(93.30,94.90,"ki wo lagbhag mar hi gaya tha",0.22),(95.65,97.20,"Forest officials ne use bachaya",0.30),(97.50,98.60,"aur survive kar gaya",0.20),
   (106.60,107.10,"Aur aaj?",0.45),(107.85,108.75,"mazboot gardan",0.20),(109.20,110.25,"bhaari agle pair",0.20),(110.75,111.45,"aur ghana coat",0.20),(111.70,112.95,"ek survivor ki jhalak",0.20),
   (119.85,122.15,"Agar aap use apni aankhon se dekhna chahte hain",0.45),(122.45,123.85,"toh mere saath",0.18),(124.35,127.45,"Pilibhit safari par aaiye",0.20),(128.20,130.55,"Instagram par connect kar sakte hain",0.28),(131.00,132.60,"link neeche milega",0.22)]
PAD_A,PAD_B=0.10,0.16; fade=int(0.012*sr)
out=np.zeros(int(0.3*sr),np.float32); marks=[]
for a,b,lab,gap in P:
    out=np.concatenate([out,np.zeros(int(gap*sr),np.float32)]) if gap>0 else out
    seg=x[int((a-PAD_A)*sr):int((b+PAD_B)*sr)].copy(); n=min(fade,len(seg)); seg[:n]*=np.linspace(0,1,n); seg[-n:]*=np.linspace(1,0,n)
    marks.append((round((len(out)/sr)+PAD_A,3),round((len(out)+len(seg))/sr-PAD_B,3),lab)); out=np.concatenate([out,seg])
out=np.concatenate([out,np.zeros(int(0.3*sr),np.float32)])
w.write('vo_edit_raw.wav',sr,(np.clip(out,-1,1)*32767).astype(np.int16))
json.dump(marks,open('phrases.json','w'),ensure_ascii=False,indent=1)
print("dur %.2f"%(len(out)/sr))
for m in marks: print(m)
