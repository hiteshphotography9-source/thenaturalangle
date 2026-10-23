import sys, subprocess, numpy as np, os
sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/hornbill')
from hscenes import *
def chunk(i,n=4):
    nf=int(TOTAL*30); a=i*nf//n; b=(i+1)*nf//n
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","30","-i","-","-c:v","libx264","-preset","fast","-crf","19","-pix_fmt","yuv420p",f"ch_{i}.mp4"],stdin=subprocess.PIPE)
    for k in range(a,b): p.stdin.write(frame(k/30).tobytes())
    p.stdin.close(); p.wait(); return i
if __name__=="__main__":
    from multiprocessing import Pool
    tag=sys.argv[1] if len(sys.argv)>1 else "na"
    with Pool(4) as pl: print(pl.map(chunk,range(4)))
    open("list.txt","w").write("".join(f"file 'ch_{i}.mp4'\n" for i in range(4)))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i","list.txt","-c","copy",f"video_{tag}.mp4"],check=True)
