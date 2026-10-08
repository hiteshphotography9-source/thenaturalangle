# The Natural Angle: content archive

Carousels, video and build code made with Claude. All wildlife photographs are by Hitesh Chawla (The Natural Angle). Maps use [Natural Earth](https://www.naturalearthdata.com/) public domain data.

## Carousels (1080x1350 JPG)

| Folder | Subject |
|---|---|
| 01_kishanpur_beldanda | Beldanda, Kishanpur |
| 02_panna_p151_and_cubs | Tigress P151 and cubs, Panna |
| 03_silhouette_teaching | Silhouette teaching carousel |
| 04_raptors | Montagu's harrier, Laggar falcon and other raptors |
| 05_andaman_birds_v1, 06_andaman_birds_gold_style | Andaman birds (two styles) |
| 07_laggar_falcon | Laggar falcon (female) |
| 08_47_shots_one_keeper | "47 shots, 1 keeper" |
| 09_she_was_alone | Tiger story, Kishanpur |
| 10_sanjay_dubri | Sanjay-Dubri tigers |
| 11_mausi_story | Mausi, tigress who raised her dead sister's cubs (Sanjay-Dubri) |
| 12_this_shot_was_planned | Built from the "This Shot Was Planned" reel |
| 13_ibis_backlight | Black-headed ibis, backlight teaching |
| 14_pilibhit_part1 | Pilibhit Part 1 |
| 15_pilibhit_part2 | Pilibhit Part 2 (one sighting, told as a story) |

## Video

Version 2 (current): `video/NoTigersSriLanka_V2_HQ_90MB.mp4` (upload this one) and `NoTigersSriLanka_V2_share_25MB.mp4`. Real shaded-relief map, 3D-parallax tigers, kinetic text, synthesized sound design and music. Code in `video/v2_code/`. Version 1 files are listed below.


`video/NoTigersSriLanka_share_25MB.mp4` (1080x1920, 80 s, -14.4 LUFS) and `NoTigersSriLanka_HQ_76MB.mp4` (same cut, higher bitrate, use this one for upload).

Title: Why Are There No Tigers in Sri Lanka? The Answer Isn't Distance

Claims in the video, and how sure they are:
- Fact: no wild tigers in Sri Lanka today; leopard is the apex predator.
- Fact: Sri Lanka was joined to India by a land bridge for more than half of the last 500,000 years; sea level about 120 m lower at the last glacial maximum; last link closed roughly 10,000 to 7,500 years ago (sources differ).
- Hypothesis: a toe bone (Batadomba Cave, about 16,500 years old) and a tooth (Ratnapura) were tentatively identified as tiger (Manamendra-Arachchi et al., 2005, Raffles Bulletin of Zoology Suppl. 12). A later catalogue lists the toe bone as distinct from both lion and tiger.
- Hypothesis: a small isolated island population was not sustained after the bridge flooded; the leopard held the top-predator role.
- Map depth shading is illustrative.

## Panna reel (Tourist vs Photographer), version 3

`video/panna_reel/PannaReel_TouristVsPhotographer_V3.mp4` (56 s, 1080x1920). Re-edit of the original reel: hook cut, split screen, kinetic captions, callouts, autofocus-hunting graphic, sound effects layered over the original audio. Code in `video/panna_reel/code/` (needs `video/v2_code/eng.py`; source frames were extracted from the original reel).

## Code

`code/carousels/`: Python (Pillow, NumPy, OpenCV) used to render the slides. `code/fonts/`: Anton, Barlow, Barlow Condensed, Cormorant Garamond.
`code/video/`: map and scene renderer, audio mix and encode scripts. To rebuild the video, download `ne_10m_land.geojson` and `ne_10m_bathymetry_K_200.geojson` from Natural Earth, run `geo.py`, `audio.py`, then `render.py`. Photo and audio paths inside the scripts point to the original upload folder and need updating.

Original photographs are not stored here.

## Pilibhit Short (with voiceover)

`video/pilibhit_short/`: 71 s, 1080x1920, Hinglish voiceover by Hitesh Chawla. Story: tigers 25 (2014) to 65 (2018), the earlier fall, what NTCA credits, 57 resident plus 8 transit, TX2 award, conflict at the edge. `stem_music_sfx_no_vo.mp3` is the music and effects without voice. Facts and sources are in the chat research notes; the 2010 and 2013 counts are reported estimates and sources differ.
