# Claude Dispatch prompt: Long Video 1 (Barahi / S3)

Paste everything below the line into Claude Dispatch. Replace the three PLACEHOLDERS first.

---

TASK: Build a finished YouTube long video (landscape 1920x1080, 30 fps, 8 to 10 minutes) from my podcast episode, working on this PC. Do the whole job yourself, check your own output, and do not stop to ask me unless a rule below says STOP.

PLACEHOLDERS (fill before running)
- PODCAST_FILE = C:\PATH\TO\full_podcast_episode.mp4
- PHOTOS_DIR = C:\PATH\TO\my_tiger_photos   (my own photos only)
- OUTPUT_DIR = C:\PATH\TO\long1_barahi_output

ABOUT ME
Hitesh Chawla, brand "The Natural Angle" (YouTube, Instagram, Facebook), wildlife photography. Voice: authentic, grounded, direct. Never use em-dashes in any text you write. Never use the words BOL, SUN, TU, TERA, TUJHE in any text. No AI cliches ("delve", "testament", "game-changer").

TITLE
"The Day Every Jeep Reversed for a Tigress (Barahi, Pilibhit)"

SOURCE SEGMENTS (timestamps are approximate, +/- 20 s. Find the true start and end by listening and reading the transcript, cut on sentence boundaries)
1. 33:29 to 36:50 : the S3 and S2 story, who Barahi is.
2. 39:00 to 45:35 : jeeps reversing, my gypsy being the only one with head-on shots, the tigress crossing.
Keep my own voice and speech from the podcast. Mute or cut host and guest speech unless it is a short question needed for context (max 6 s each).

STEP 1 PREP
- Install or use ffmpeg and faster-whisper (or whisper.cpp). Make OUTPUT_DIR with subfolders: work, frames, final.
- Extract the two segments, transcribe in Hindi with word timestamps, save transcript.txt.
- Remove dead air, fumbles, repeated starts and filler. Compress any silence over 0.45 s to 0.30 s. Use 8 ms audio crossfades. Enhance voice: high-pass 90 Hz, mild denoise, light compression, loudnorm -16 LUFS.
- Target length after cleanup: 8 to 10 minutes. If over 10:00, cut the weakest tangents, never the story beats.

STEP 2 STORY STRUCTURE (chapters, also used for YouTube chapters)
00:00 Hook (first 20 to 30 s): open on my best head-on tiger photo or the strongest line about getting the head-on shot while others got the tail. Big title card within 3 s. No long intro.
01 The Setup: S3 and S2 background.
02 Who is Barahi: her history as I tell it.
03 The Walk: animated route map (see below).
04 The Jeep Chaos: jeeps reversing, line-up diagram animation.
05 The Crossing: build tension, the crossing, the head-on shots.
06 Last line + CTA end card (5 s).

STEP 3 VISUAL STYLE (match my recent reel "Squirrel_Flora")
- Palette: near-black #080C0A panels, cream #FFF4DC text, accent lime #E8FF3D.
- Font: Inter (Bold and ExtraBold). Do not use Poppins.
- Captions: Hinglish (Roman letters) or English translation, 1 to 2 lines, bold, lime text on semi-transparent dark box, lower-left, min 44 px at 1080p. NEVER place captions or graphics over an animal's face.
- Persistent chapter tracker at top center: rounded dark pill with a lime number badge and chapter name, and a segmented progress bar underneath.
- Headline plates for each beat (rounded dark plate, lime outline, cream ExtraBold text).
- Snap-zoom (about 120 to 125 percent, 0.3 s hold) on 4 to 6 key lines, with a soft thud.
- Checklist pop cards (3 items with lime check marks) for the setup facts.
- Camera viewfinder HUD (REC, timecode, corner brackets, focus box that locks onto the tiger with a green LOCK, flash on lock) over my best crossing photo.
- Zoom-through-cut transitions between chapters (fast push with radial blur).
- Ken Burns slow push on every still photo. Use only photos from PHOTOS_DIR. If a needed photo is missing, use a simple labelled placeholder card "PHOTO TO BE ADDED" and list it in the report. Do NOT download or generate any wildlife images.
- Jeep diagram animation (top-down road, 4 beige jeeps, our yellow jeep, green GAP box, spotted tiger icon crossing). Label text must not overlap icons.
- Route map animation for Barahi's walk. Use a simple stylised dark map. State on screen "ROUTE APPROXIMATE" and "~34 km (as told by Hitesh)". Do not invent place names, coordinates or distances I did not say.

STEP 4 AUDIO
- My voice is the main track. Add a quiet music bed at about -20 dB under voice, ducked under speech.
- SFX audible but not loud: SFX average level about 7.5 dB below voice. Use whooshes on transitions, soft thuds on snap zooms, ticks on checklist items, pings on map points. Generate or use royalty-free sounds only.
- Final master: -14 LUFS, true peak -1.5 dB, no clipping.

STEP 5 FACT RULES
- Every factual claim on screen must come from my speech or a source you cite. Examples to flag for my confirmation: size of the tiger (I said about 10 feet), the 34 km route, who rescued S3, dates, "two years ago". Put each in report.md under "FACTS TO CONFIRM" with the exact timestamp. Never state a guess as fact. Label estimates as estimates.
- Do not mention or show the podcast channel logo. Crop or cover any channel logo or burned-in title. (Rights: I must get written permission from the podcast host before publishing. Remind me in report.md.)

STEP 6 OUTPUTS (in OUTPUT_DIR\final)
1. Long1_Barahi_HQ.mp4 : 1920x1080, H.264, about 12 to 14 Mbps, AAC 192k.
2. Long1_Barahi_share.mp4 : under 100 MB.
3. thumbnail_1.jpg, thumbnail_2.jpg, thumbnail_3.jpg : 1280x720 under 2 MB, high-contrast, 3 to 5 words, my best tiger photo, no text over the tiger's face.
4. subtitles.srt (Hinglish) and subtitles_en.srt (English).
5. metadata.md containing:
   - 5 title options (max 60 chars, curiosity plus clarity, no clickbait lies), best one marked.
   - Description: strong first 2 lines, chapter timestamps that match the video exactly, my book "Mastering Wildlife Photography" mention, Instagram @thenaturalangle, hashtags (max 5).
   - 15 tags.
   - Pinned comment (a question to drive replies plus the book link placeholder).
   - End-screen and card suggestions with timestamps.
6. report.md: what was cut and why, chapter list with timestamps, FACTS TO CONFIRM, photos used, photos missing, any caption lines you are unsure about (ASR doubt), and the rights reminder.

STEP 7 SELF-CHECK BEFORE FINISHING (fix, do not just report)
- Watch 12 evenly spaced frames and 12 frames at graphic moments. Look for: text over faces, overlapping text or icons, cropped text, leftover channel logo, blurry upscales, wrong chapter name.
- Confirm duration 8:00 to 10:00, audio levels, no clipping, no silent gaps over 0.5 s, chapter timestamps match.
- If any check fails, fix and re-render. List what you fixed in report.md.

STOP and ask me only if: the podcast file cannot be found, fewer than 6 of my photos are available, or the two segments cannot be located in the transcript.

When done, print the full path of every file in OUTPUT_DIR\final and the three most important FACTS TO CONFIRM.
