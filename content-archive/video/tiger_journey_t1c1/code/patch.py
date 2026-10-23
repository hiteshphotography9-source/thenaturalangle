import sys, subprocess
sys.path.insert(0,'/tmp/claude-0/-home-user/530e917f-6900-5386-87f2-01588fc50eb7/scratchpad/disp')
from dscenes import *
A0,A1=int(sys.argv[1]),int(sys.argv[2])
def chunk(i,n=4):
    a=A0+i*(A1-A0)//n; b=A0+(i+1)*(A1-A0)//n
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","30","-i","-","-c:v","libx264","-preset","fast","-crf","19","-pix_fmt","yuv420p",f"pc_{i}.mp4"],stdin=subprocess.PIPE)
    for k in range(a,b): p.stdin.write(frame(k/30).tobytes())
    p.stdin.close(); p.wait(); return i
if __name__=="__main__":
    from multiprocessing import Pool
    with Pool(4) as pl: pl.map(chunk,range(4))
    open("plist.txt","w").write("".join(f"file 'pc_{i}.mp4'\n" for i in range(4)))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i","plist.txt","-c","copy","patch.mp4"],check=True)
