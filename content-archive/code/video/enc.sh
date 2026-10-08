set -e
ffmpeg -y -loglevel error -i final.mp4 -an -vf hqdn3d=2:1.5:4:3 -c:v libx264 -preset slow -b:v 2600k -maxrate 3500k -bufsize 7000k -pix_fmt yuv420p -profile:v high -pass 1 -passlogfile p2 -f null /dev/null
ffmpeg -y -loglevel error -i final.mp4 -i mix.wav -vf hqdn3d=2:1.5:4:3 -c:v libx264 -preset slow -b:v 2600k -maxrate 3500k -bufsize 7000k -pix_fmt yuv420p -profile:v high -pass 2 -passlogfile p2 -c:a aac -b:a 160k -ar 48000 -map 0:v -map 1:a -t 80 -movflags +faststart TheNaturalAngle_NoTigersInSriLanka.mp4
ls -la TheNaturalAngle_NoTigersInSriLanka.mp4
