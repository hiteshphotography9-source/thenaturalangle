Long1_Barahi 1080p, 10 playable MP4 clips in order (A01 to A10), total 8:42.
Each plays on its own. To get ONE file, drop them in order into CapCut / Premiere / DaVinci and export, or on a PC with ffmpeg:
  ffmpeg -f concat -safe 0 -i list.txt -c copy Long1_Barahi_1080p.mp4
(list.txt lines: file 'Long1_Barahi_1080p_partA01.mp4' ... through A10)
