---
name: interior.photography
description: Create portfolio-style Instagram content (5-slide carousel + 1 single post) for Hitesh Chawla's hotel and interior photography account @hiteshchawla.interiors. Minimalist gallery-wall look, no phone number, no hotel names unless asked, real EXIF camera settings, caption + hashtags, and scheduling through vidIQ (carousel 12:00 PM IST, post 7:00 PM IST). Use when asked for interior, hotel or resort photography posts, carousels, a week of content, or "interior.photography".
---

# interior.photography

Builds Instagram content that looks like a photographer's portfolio, not an ad. The viewer should want to see more and book, without being sold to.

## What it produces (per day)
- **1 carousel, 5 slides**, 1080x1350 (4:5), scheduled **12:00 PM IST**
- **1 single post**, 1080x1350, scheduled **7:00 PM IST**
- A caption and 6-8 hashtags for each

## Look and feel (do not drift from this)
- **Gallery wall**: cream mat (#F3EFE8), photo framed with soft shadow, tiny type. Cover and single post are full-bleed photos with a dark gradient at the bottom.
- Fonts: Newsreader (titles, with one *italic* word), Barlow Condensed (small caps labels), DM Mono (camera settings).
- Colours: ink #0A1A24, coral #D93D14 for the slide number only, teal #7FD3CF for small labels on the dark closing slide.
- **Minimal text**: one short title per slide (max 2 lines), a label ("01 Lobby") and one line of real camera settings.
- **No phone number anywhere** (organic posts never carry it; the number is for ads).
- **No hotel or property names** unless the user asks for a named version.
- No price, no discount, no "book now" banners, no emoji on images.

## Carousel structure (5 slides)
1. **Cover**: full-bleed hero photo, title like "Rooms worth a *second* look.", tiny "Swipe →", small name label top-left.
2. **Frame 01** (e.g. Lobby): matted photo, one-line craft note, settings.
3. **Frame 02** (e.g. Room): same layout.
4. **Frame 03** (a detail crop): same layout, add "(cropped)" in the notes if the crop changes the focal length.
5. **Closing** on ink background: strip of 3 square thumbnails, "Your property, framed *like this.*", "Free photo audit: send your listing link in DM.", location line, name and @hiteshchawla.interiors. **No phone number.**

## Single post
One strong photo, full-bleed, two-line title bottom-left ("Warm wood. One clean frame."), settings bottom-right.

## Workflow
1. **Pick photos.** Use full-resolution originals when they exist (scratchpad `reel/orig/*.jpg`, 6960px) otherwise the 2400px set in `drive/web`. Make a contact sheet and look at it. Prefer straight verticals, true colour, warm light. Do not reuse a photo that was posted in the last 7 days.
2. **Read EXIF** for the settings line. Never invent settings. Run `scripts/exif.py <jpg>`. If a photo has no EXIF, leave the settings line out of that slide.
3. **Write a spec** (see `examples/spec-week1.json`) and run it **from the scratchpad directory**, because the image paths in the spec (`reel/orig/...`, `drive/web/...`) are relative to it:
   `python3 -I /home/user/thenaturalangle/.claude/skills/interior.photography/scripts/make_carousel.py spec.json outdir`
   Needs Python PIL and Node with Playwright (both already installed in this environment).
   This crops to 4:5, builds the HTML, renders PNG and JPG files with Playwright.
4. **Look at every output image** before showing the user. Check text does not collide with the photo, nothing is clipped, no phone number.
5. **Send to the user for approval** (SendUserFile) with the caption text. Wait for the go-ahead unless the user already said to schedule it.
6. **Host and upload.** Copy the JPGs to `/home/user/thenaturalangle/interiors/social/`, commit, push to `main` and to the session branch, wait for the GitHub Pages deploy, then `vidiq_upload_image` with `https://thenaturalangle.com/interiors/social/<file>.jpg` (404 means the deploy is not finished yet).
7. **Draft** with `vidiq_social_post_draft_create` on account `30417939854472455` (@hiteshchawla.interiors), carousel `publishAt` = today/day 12:00 +05:30, post = 19:00 +05:30. Publish with `vidiq_social_post_publish` only after the user approved the content. Scheduling costs no credits; confirm with the returned `scheduled` status.
8. Tell the user clearly what is scheduled and when.

## Caption rules
- Line 1 is the hook (same words as the cover or post title).
- 2-3 short sentences about the photography (straight lines, true colour, light), not about price.
- One soft call to action: "Send your listing link in DM for a free photo audit."
- Location line: "Delhi NCR, shooting across India since 2016."
- **6-8 hashtags only**, no hashtag walls. Core set: #hotelphotography #interiorphotography #hospitalityphotography #hotelphotographer #delhihotels #interiordesign #architecturephotography #roomdesign. Swap in #resortphotography #aerialphotography for resorts, #restaurantphotography for dining.
- Hinglish only if the user asks. Default is English, matching the account.

## Weekly theme bank (one carousel per day)
1. Rooms worth a second look (lobby, room, detail) *done*
2. Before / after (phone shot vs pro frame) using `img/ba-*-before/after.webp`
3. Pools and rooftops at dusk
4. Restaurants and dining ambience
5. One room, three lights (day, warm, evening)
6. Lobbies and first impressions
7. Resort at golden hour (aerial / villas)

## Never do
- Put a phone number, price or discount on an organic image.
- Name a hotel without being asked.
- Publish without the user's approval of that exact content.
- Spend vidIQ credits on analysis tools without checking `vidiq_balance`; credits are shared with the website's Instagram feed refresh (5 per run).
