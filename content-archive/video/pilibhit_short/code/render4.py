import subprocess, multiprocessing as mp
from sc import frame, W, H
FPS=30; TOTAL=2130; NP=4
def work(i):
    a=i*TOTAL//NP; b=(i+1)*TOTAL//NP
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r","30","-i","-","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p",f"p_{i}.mp4"],stdin=subprocess.PIPE)
    for n in range(a,b): p.stdin.write(frame(n/FPS).tobytes())
    p.stdin.close(); p.wait(); return i
if __name__=="__main__":
    with mp.Pool(NP) as pool: print(pool.map(work,range(NP)))
