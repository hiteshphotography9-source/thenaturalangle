set -e
ffmpeg -y -loglevel error -i v2_noaudio.mp4 -i mix2.wav -c:v libx264 -preset slow -crf 21 -maxrate 10M -bufsize 20M -pix_fmt yuv420p -profile:v high -c:a aac -b:a 192k -ar 48000 -map 0:v -map 1:a -t 80 -movflags +faststart HQ.mp4
ffmpeg -y -loglevel error -i v2_noaudio.mp4 -an -vf hqdn3d=1.5:1.2:3:2.5 -c:v libx264 -preset slow -b:v 2500k -maxrate 3400k -bufsize 6800k -pix_fmt yuv420p -profile:v high -pass 1 -passlogfile q2 -f null /dev/null
ffmpeg -y -loglevel error -i v2_noaudio.mp4 -i mix2.wav -vf hqdn3d=1.5:1.2:3:2.5 -c:v libx264 -preset slow -b:v 2500k -maxrate 3400k -bufsize 6800k -pix_fmt yuv420p -profile:v high -pass 2 -passlogfile q2 -c:a aac -b:a 160k -ar 48000 -map 0:v -map 1:a -t 80 -movflags +faststart share.mp4
ls -la HQ.mp4 share.mp4
