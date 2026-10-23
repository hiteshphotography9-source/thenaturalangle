import numpy as np, scipy.io.wavfile as w, json, subprocess
sr,x=w.read('raw48.wav'); x=x.astype(np.float32)/32768
SEG=[(0.14,2.76),(3.54,5.3),(5.84,6.88),(7.56,10.24),(10.74,12.92),(13.24,16.08),(16.56,24.5),(24.96,27.38),(27.86,31.3),(31.72,33.48),(34.0,34.82),(35.22,35.96),(36.52,40.28),(40.8,42.64),(43.04,43.48),(43.88,47.08),(47.6,50.48),(50.96,52.66),(53.08,58.4),(58.88,61.48),(61.92,63.6),(63.92,65.14),(65.52,67.26),(67.54,68.94),(69.36,73.4),(73.8,76.2),(76.6,78.5),(78.94,83.28),(83.7,86.14),(86.56,88.0),(88.46,91.68),(92.02,93.82),(94.16,95.82),(96.16,100.74),(101.08,104.56),(104.94,107.96),(108.4,109.16),(109.6,110.62),(111.06,112.64)]
SCN=[0,0,0,1,1,1,1,2,2,2,2,2,2,3,3,3,3,4,4,4,5,5,5,5,5,5,6,6,6,7,7,7,7,7,7,8,8,8,8]
LAB=["Ye parinda apna ghar bana nahi sakta","Use sirf viraasat mein milta hai","Great hornbill","Na ye ped khodta hai na ghonsla bunta hai","Use chahiye ek bada purana ped","jis mein kudrat ne pehle se ek khokhal bana rakha ho","Anaimalai study nest wale ped 18.5 m oonche, 1 m motay","Do se chaar kilo ka ye bhaari parinda","Jab udta hai toh paron ki awaaz door se sunayi deti hai","jaise bhaap ka engine chal pada ho","Aur ye peela rang","Ye makeup hai","Tail ke paas ki gland ka tel, chonch aur paron par","Chonch ke upar ye khokhli topi","casque","Nar hornbill hawa mein casque takraate hain","Iska asli kaam abhi tak pata nahi","Aise jungle ab kahan bache hain","Himalaya talhati, North-East, Western Ghats","Poore Asia mein Vulnerable list mein","Par ye sirf jungle mein rehta nahi","jungle ugata bhi hai","Bade beej wale phal nigalta hai","aur door jaakar girata hai","Ek study mein 69 se 100 percent beej maa ped se door","Shayad apne hi bhavishya ke ghar ugata hai","Lekin iski casque ki keemat thi","Nyishi samaj ke taj mein ise pehna jaata tha","Shikaar badha aur hornbill ghatne laga","Phir ek anokha badlaav","Pakke mein kayi purane shikari nest protector ban gaye","Hornbill Nest Adoption Program","dus gaon dus rakhwale","2012 se 2018 tak 119 chicks","taj mein asli chonch ki jagah fibreglass ki chonch","Agli baar jungle mein jao sirf parinde ko mat dekhna","Ped ko dekhna","Wahi iska ghar hai","Follow The Natural Angle"]
TEMPO=1.20; PA,PB=0.05,0.10
out=np.zeros(int(0.3*sr),np.float32); marks=[]; fade=int(0.008*sr)
SKIP={25}
prev=None
for i,((a,b),sc) in enumerate(zip(SEG,SCN)):
    if i in SKIP: continue
    gap=0 if prev is None else (0.42 if SCN[prev]!=sc else 0.14); prev=i
    out=np.concatenate([out,np.zeros(int(gap*sr),np.float32)])
    seg=x[int((a-PA)*sr):int((b+PB)*sr)].copy(); n=min(fade,len(seg)); seg[:n]*=np.linspace(0,1,n); seg[-n:]*=np.linspace(1,0,n)
    marks.append([(len(out)/sr+PA)/TEMPO,((len(out)+len(seg))/sr-PB)/TEMPO,LAB[i],i]); out=np.concatenate([out,seg])
out=np.concatenate([out,np.zeros(int(0.35*sr),np.float32)])
w.write('vo_edit_raw.wav',sr,(np.clip(out,-1,1)*32767).astype(np.int16))
json.dump({str(s):[round(a,3),round(b,3),l] for a,b,l,s in marks},open('phrases.json','w'),ensure_ascii=False)
subprocess.run(["ffmpeg","-y","-v","error","-i","vo_edit_raw.wav","-af",f"atempo={TEMPO},highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=100:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=9","-ar","48000","-ac","1","VO_clean_Hornbill.wav"],check=True)
print("dur", round(len(out)/sr/TEMPO,2))
