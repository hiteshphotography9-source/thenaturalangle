"""Build the inner pages (Tours, Watch, Learn, Shop) in the homepage design.
Shares header, footer and sections with index.html so everything stays in sync."""
import re, json, html, pathlib
from urllib.parse import quote
E = html.escape
ROOT = pathlib.Path(__file__).resolve().parent.parent
idx = (ROOT / "index.html").read_text()
WA = "https://wa.me/919899114998?text="

def grab(pat):
    m = re.search(pat, idx, re.S); return m.group(0)

head_links = grab(r'<link rel="preconnect".*?rel="stylesheet">')
header = grab(r'<header class="hd".*?</header>')
header = header.replace('href="#top"', 'href="/"')
for a, b in [('#tours', 'Tours.html'), ('#watch', 'Watch.html'), ('#learn', 'Learn.html'), ('#ebooks', 'Shop.html')]:
    header = header.replace(f'href="{a}"', f'href="{b}"')
header = header.replace('>Ebooks<', '>Shop<')
connect = grab(r'<section class="sx connect".*?</section>')
cband = grab(r'<section class="cband".*?</section>')
footer = grab(r'<footer class="ft">.*?</footer>').replace('href="#top"', 'href="/"').replace('href="#ebooks"', 'href="Shop.html#ebooks"')
botnav = grab(r'<nav class="bn".*?</nav>')
for a, b in [('#top', '/'), ('#tours', 'Tours.html'), ('#watch', 'Watch.html'), ('#learn', 'Learn.html'), ('#ebooks', 'Shop.html')]:
    botnav = botnav.replace(f'href="{a}"', f'href="{b}"')
botnav = botnav.replace('Ebooks</a>', 'Shop</a>')

TRIPS_LD = re.findall(r'<script type="application/ld\+json">.*?</script>', idx, re.S)
def page(fn, title, desc, active, body, img="assets/img/22789f77a00bc6d5113807b48600b740.webp"):
    h = header.replace(f'href="{active}"', f'href="{active}" class="on"')
    b = botnav.replace(f'href="{active}"', f'href="{active}" class="on"')
    out = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="https://thenaturalangle.com/{fn}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:image" content="https://thenaturalangle.com/{img}"><meta property="og:url" content="https://thenaturalangle.com/{fn}">
<meta name="theme-color" content="#0E0F0D"><link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icons/icon-192.png">
{head_links}
{"".join(TRIPS_LD[1:]) if fn=="Tours.html" else ""}
<link rel="stylesheet" href="home.css?v=11">
</head><body id="top" class="inner"><div class="prog" aria-hidden="true"></div>
{h}
{body}
{connect}
{cband if fn=='Tours.html' else ''}
{footer}
{b}
<script src="home.js?v=4" defer></script><script src="site.js?v=4" defer></script>
</body></html>'''
    (ROOT / fn).write_text(out)

def phero(kick, h1, sub, img, extra=""):
    return f'''<section class="phero"><img class="pbg" src="{img}" alt=""><div class="hsh"></div>
<div class="wrap phc"><span class="kick ani" style="--i:0">{kick}</span><h1 class="ani" style="--i:1">{h1}</h1><p class="hsub ani" style="--i:2">{sub}</p>{extra}</div></section>'''

# ---------- TOURS ----------
tours_sec = grab(r'<section class="sx tours" id="tours">.*?</section>')
tours_body = phero("Safari tours · 11 destinations &amp; counting", 'Photography-first <span class="hl">safaris</span>',
    "Small groups, max <mark>4 photographers per gypsy</mark>, planned around light and animal movement. Tigers, leopards, birds and the stories in between.",
    "assets/img/93826c3fe975d7905c157ab31d70db48.webp",
    f'<div class="hcta ani" style="--i:3"><a class="btn gold lg" href="#tours">See all tours</a><a class="btn ghost lg" href="{WA}{quote("Hi Hitesh, which safari tour suits me?")}">Ask on WhatsApp</a></div>') + tours_sec
page("Tours.html", "Wildlife Photography Safari Tours in India · The Natural Angle",
     "Photography-first safari tours to Panna, Sanjay Dubri, Jim Corbett, Rajaji, Pilibhit, Dudhwa, Bharatpur, Tal Chhapar, Bikaner, Jhalana and Delhi NCR birding. Small groups, max 4 per gypsy.",
     "Tours.html", tours_body, "assets/img/93826c3fe975d7905c157ab31d70db48.webp")

# ---------- WATCH ----------
feed = json.loads((ROOT / "data" / "feed.json").read_text())
L, S = feed["youtube"]["long"], feed["youtube"]["shorts"]
def th(i, q="hqdefault"): return f"https://i.ytimg.com/vi/{i}/{q}.jpg"
def dt(s):
    import datetime
    try: return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).strftime("%-d %b")
    except Exception: return ""
vgrid = "".join(f'<a class="vc rv" href="https://www.youtube.com/watch?v={v["id"]}"><div class="vt"><img loading="lazy" src="{th(v["id"])}" alt=""><span class="pl2"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span></div><b>{E(v["title"])}</b><small>{dt(v["published"])}</small></a>' for v in L)
sgrid = "".join(f'<a class="short rv" href="https://www.youtube.com/shorts/{v["id"]}"><img loading="lazy" src="{th(v["id"])}" alt=""><span>{E(v["title"])}</span></a>' for v in S)
watch_body = phero("Watch", 'Stories from the <span class="hl">safari track</span>', "Safari stories, field lessons and tiger news from India's forests. New videos appear here on their own.",
    "assets/img/1b45e7829a45faa2bdcc8cf92fec74b7.webp",
    '<div class="hcta ani" style="--i:3"><a class="btn gold lg" href="https://www.youtube.com/@thenaturalangle?sub_confirmation=1">Subscribe on YouTube</a></div>') + f'''
<section class="sx" id="videos"><div class="wrap"><div class="shd"><div><span class="kick">Latest videos</span><h2 class="rv">Long-form <span class="hl">safari stories</span></h2></div><a class="more" href="https://www.youtube.com/@thenaturalangle/videos">All on YouTube ↗</a></div>
<div class="vgrid" data-feed="long">{vgrid}</div></div></section>
<section class="sx alt" id="shorts"><div class="wrap"><div class="shd"><div><span class="kick">Shorts</span><h2 class="rv">60 seconds <span class="hl">in the wild</span></h2></div><a class="more" href="https://www.youtube.com/@thenaturalangle/shorts">All Shorts ↗</a></div>
<div class="sgrid" data-feed="shorts">{sgrid}</div></div></section>'''
page("Watch.html", "Watch · Wildlife Safari Videos and Shorts · The Natural Angle",
     "Latest wildlife safari videos and Shorts from Hitesh Chawla: tigers, leopards, birds and field lessons from India's forests.", "Watch.html", watch_body,
     "assets/img/1b45e7829a45faa2bdcc8cf92fec74b7.webp")

# ---------- LEARN ----------
bdg = grab(r'<div class="bdg">.*?</div></a></div>') if '<div class="bdg">' in idx else ""
bdg = re.search(r'<div class="bdg">(.*?)</div>\s*<div class="shd sm">', idx, re.S).group(1)
guides = [("g-2956a871146857","Reading the Signal Before the Move","Fieldcraft before the animal moves","Start here"),
("g-3403fca6140789","Stop Looking for Tigers. Read the Jungle Instead.","Alarm calls, sentinel behaviour, terrain and territory","Fieldcraft"),
("g-1e30d638648068","When Tigers Actually Move","Why golden hour isn't the window that matters","Fieldcraft"),
("g-59e71667d49b29","The Family We Almost Missed","Two safaris with Beldanda and her cubs, Kishanpur","Story"),
("g-68694d28ae5001","Focus Through It","Clean autofocus through branches and grass","Technique"),
("g-c790eebc25eb38","3 Camera Settings for Sunbirds","Shutter, aperture and focus for the upside-down feed","Settings"),
("g-14a5ebc39b934b","One Fish. Three Different Species Wanted It.","The toss is your shutter cue","Action"),
("g-7f135cb5e9890d","I Underexposed Every Single One of These. On Purpose.","The rim-light exposure rule, five langur frames","Light"),
("g-29f2620fab8b0f","We Didn't Move 10 Feet. The Light Did All the Work.","Read the light instead of repositioning","Light"),
("g-541c57cb337b33","Empty Space Is Not Empty","Four reserves, four species, one lesson on negative space","Composition"),
("g-f4d6c0ea6048e5","You Don't Need More Lens","When the reach you already have is enough","Composition"),
("g-b3ddd5fe9ae996","Your ₹2 Lakh Camera Won't Fix This Mistake","Four questions to ask before you blame your gear","Decisions"),
("g-b75187d4aa4f72","I Used One Lens for 10 Years. Then I Switched.","EF 100-400 L to RF 100-400: what actually mattered","Gear"),
("g-5dde2ae7868bc8","Start Your Own Local Species List","One park and a reason to keep going back","Field guide")]
gd = "".join(f'<a class="gd rv" href="guides/{g}.pdf" download><span class="kick">{c}</span><b>{E(t)}</b><span class="gs">{E(d)}</span><span class="dl">Free PDF ↓</span></a>' for g,t,d,c in guides)
tools = re.search(r'<div class="tools">.*?</a></div>', idx, re.S).group(0)
series = "".join(f'<a class="ser rv" href="https://www.instagram.com/thenaturalangle/"><img loading="lazy" src="assets/img/{i}.webp" alt="{E(a)}"><span class="kick">Part {n}</span><b>{E(t)}</b></a>' for n,(i,a,t) in enumerate([("93e8dc15f7d76910f2a3f03296e26975","The WAIT checklist","Run it before every sighting"),("af3a61f550dae068aa0a8d0df3531a69","The WATCH checklist","Read it before you raise the camera"),("cbf9ca22264a454351ee52c3600c36c9","The SHOOT checklist","Run it the moment the action starts")],1))
learn_body = phero("Learn", 'Learn wildlife photography <span class="hl">in the field</span>', "Shot breakdowns, <mark>14 free field guides</mark>, a camera settings tool and checklists that work with no signal.",
    "assets/img/ce0ebd9b5cedc2d43efa390ca8fa86b5.webp",
    '<div class="hcta ani" style="--i:3"><a class="btn gold lg" href="#guides">Get the free guides</a><a class="btn ghost lg" href="#breakdowns">Shot breakdowns</a></div>') + f'''
<section class="sx" id="guides"><div class="wrap"><div class="shd sm" style="margin-top:0"><h2 class="kick fg"><span class="hl">Free</span> field guides · all 14</h2></div>
<p class="lead" style="margin-bottom:24px">One lesson each, from real sightings. Download once, read offline in the park.</p><div class="gdg">{gd}</div></div></section>
<section class="sx alt" id="breakdowns"><div class="wrap"><div class="shd"><div><span class="kick">How I shot this</span><h2 class="rv">One photograph, <span class="hl">taken apart</span></h2></div></div><div class="bdg">{bdg}</div></div></section>
<section class="sx" id="tools"><div class="wrap"><div class="shd"><div><span class="kick">Field tools</span><h2 class="rv">Use these <span class="hl">on safari</span></h2></div></div>{tools}
<div class="shd sm"><h3 class="kick">The series · Wait. Watch. Shoot.</h3><a class="more" href="https://www.instagram.com/thenaturalangle/">On Instagram ↗</a></div><div class="sers">{series}</div></div></section>'''
page("Learn.html", "Learn Wildlife Photography · Free Field Guides · The Natural Angle",
     "14 free wildlife photography field guides, shot breakdowns with real settings, a camera settings tool and safari checklists by Hitesh Chawla.", "Learn.html", learn_body,
     "assets/img/ce0ebd9b5cedc2d43efa390ca8fa86b5.webp")

# ---------- SHOP ----------
ebg = re.search(r'<div class="ebg">.*?</details>', idx, re.S).group(0)
quote_html = re.search(r'<figure class="quote.*?</figure>', idx, re.S).group(0)
AMZ = "https://www.amazon.in/shop/thenaturalangle?ref=ac_inf_tb_vh"
gear = [("Camera","Canon EOS R7","Crop reach and Animal Eye AF that holds through grass.","M4 8h3.5L9 5.5h6L16.5 8H20v11H4z|C12 13 3.5"),
("Lens","Canon RF 100-400mm","Hand-holdable all day, sharp enough at 400.","C12 12 8.5|C12 12 4.5"),
("Support","Beanbag","Steadier than a monopod on a jeep door.","M4 15c0-4 4-7 8-7s8 3 8 7v3H4z"),
("Cleaning","Camera cleaning kit","Safari tracks put dust on everything.","M8 3h8v5H8zM6 8h12v13H6z")]
def ic(spec):
    out=""
    for p in spec.split("|"):
        if p.startswith("C"): x,y,r=p[1:].split(); out+=f'<circle cx="{x}" cy="{y}" r="{r}"/>'
        else: out+=f'<path d="{p}"/>'
    return out
gr = "".join(f'<a class="gear rv" href="{AMZ}" target="_blank" rel="noopener"><svg viewBox="0 0 24 24">{ic(s)}</svg><span class="kick">{c}</span><b>{E(n)}</b><span>{E(w)}</span><em>View on Amazon ↗</em></a>' for c,n,w,s in gear)
shop_body = phero("Shop", 'Kit I trust. <span class="hl">Books I wrote.</span>', "Ebooks you can read tonight, the book in print, and only the gear I've carried into the field.",
    "assets/img/ea094febf2f83025f98beeac3a4c7cb6.webp",
    '<div class="hcta ani" style="--i:3"><a class="btn gold lg" href="#ebooks">Ebooks from ₹99</a><a class="btn ghost lg" href="#gear">My gear</a></div>') + f'''
<section class="sx" id="ebooks"><div class="wrap"><div class="shd"><div><span class="kick">Ebooks &amp; guides</span><h2 class="rv">Learn it once. <span class="hl">Use it on every safari.</span></h2></div></div>{ebg}{quote_html}<p class="note">Instant PDF download after payment. Questions? WhatsApp +91 98991 14998.</p></div></section>
<section class="sx alt" id="book"><div class="wrap bk"><img class="rv" loading="lazy" src="assets/img/ab9bec5e51d45fd7c7ff00fed81cdf2a.webp" alt="The Natural Angle: Mastering Wildlife Photography book cover">
<div class="rv"><span class="kick">The book</span><h2>The Natural Angle: <span class="hl">Mastering Wildlife Photography</span></h2><p class="lead">From Panna to the Himalayas. 13 chapters, from the exposure triangle to reading the wild.</p>
<div class="hcta"><a class="btn gold" href="https://www.amazon.in/dp/B0HFC84XND">Amazon India</a><a class="btn ghost" href="https://www.amazon.com/dp/B0HJ8634J8">Amazon US</a><a class="btn ghost" href="https://play.google.com/store/books/details/Hitesh_Chawla_The_Natural_Angle_Mastering_Wildlife?id=r-b8EQAAQBAJ">Google Play</a><a class="btn ghost" href="BookDetail.html">Free chapter</a></div>
<p class="note">Next book coming soon: <b>The Untold Jungle Tales</b>, stories from the field.</p></div></div></section>
<section class="sx" id="gear"><div class="wrap"><div class="shd"><div><span class="kick">In my bag</span><h2 class="rv">Gear I <span class="hl">actually carry</span></h2></div><a class="more" href="{AMZ}">Amazon storefront ↗</a></div>
<div class="gearg">{gr}</div><p class="note">Previous kit: Canon EOS M50 + EF 100-400mm f/4.5-5.6L. The tern, kingfisher and heron frames were shot on it. Some links are affiliate links; I may earn a small commission at no extra cost to you. It never decides what I recommend.</p>
<div class="gdg" style="margin-top:22px"><a class="gd rv" href="guides/g-b75187d4aa4f72.pdf" download><span class="kick">Free · Gear</span><b>I Used One Lens for 10 Years. Then I Switched.</b><span class="dl">Free PDF ↓</span></a><a class="gd rv" href="guides/g-b3ddd5fe9ae996.pdf" download><span class="kick">Free · Decisions</span><b>Your ₹2 Lakh Camera Won't Fix This Mistake</b><span class="dl">Free PDF ↓</span></a></div></div></section>'''
page("Shop.html", "Shop · Wildlife Photography Ebooks, Book and Gear · The Natural Angle",
     "Wildlife photography ebooks from ₹99, the book Mastering Wildlife Photography, and the camera gear Hitesh Chawla carries on safari.", "Shop.html", shop_body,
     "assets/img/ab9bec5e51d45fd7c7ff00fed81cdf2a.webp")
print("pages built")
