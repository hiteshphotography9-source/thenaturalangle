"""Build one day of interior.photography content (carousel slides + single post) from a v2 JSON spec.
Usage: python3 make_content.py spec.json outdir [--ledger]
Run from the scratchpad directory (image paths in specs are relative to it).

Spec v2:
{ "theme": "Pools & rooftops", "date": "2026-11-27",
  "slides": [ {layout: cover|mat|wide|duo|note|close|close_photo, ...}, ... ],
  "post":   {layout: full|mat, ...},
  "caption": "...", "post_caption": "..." , "allow_names": false }
Crops are fractions of the original: [x0, y0, x1, y1]. "meta": "auto" reads EXIF from the original, or give your own text, or omit.
"""
import json, os, sys, subprocess, pathlib, re
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
HERE = pathlib.Path(__file__).resolve().parent; SK = HERE.parent
sys.path.insert(0, str(HERE)); import exif
spec = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
warn = []; used = []

def prep(img, crop, name, width=1620):
    im = Image.open(img).convert('RGB'); W, H = im.size
    if isinstance(crop, (int, float)):            # shorthand: centre x -> full-height 4:5 crop
        w = 0.8*H/W; x0 = min(max(crop - w/2, 0), 1 - w); crop = [x0, 0, x0 + w, 1]
    x0, y0, x1, y1 = crop or [0, 0, 1, 1]
    c = im.crop((int(x0*W), int(y0*H), int(x1*W), int(y1*H)))
    if c.width < 800: warn.append(f'{os.path.basename(img)}: crop only {c.width}px wide, may look soft')
    if c.width > width: c = c.resize((width, int(c.height*width/c.width)), Image.LANCZOS)
    c.save(out/name, quality=92); used.append(os.path.basename(img)); return name

def sq(img, x, name):
    im = Image.open(img).convert('RGB'); W, H = im.size; s = H; x0 = min(int(x*W), W-s)
    im.crop((x0, 0, x0+s, s)).resize((600, 600), Image.LANCZOS).save(out/name, quality=90); used.append(os.path.basename(img)); return name

def meta(o):
    m = o.get('meta', '')
    return exif.settings(o['image']) if m == 'auto' else m

slides = spec['slides']; N = len(slides); secs = []; ids = []
for k, o in enumerate(slides, 1):
    L = o['layout']; sid = f'c{k}'; ids.append(sid); pg = f'<span>{k} / {N}</span>'
    ft = f'<div class="ft"><span>Hitesh Chawla</span>{pg}</div>'
    if L == 'cover':
        f = prep(o['image'], o['crop'], f'{sid}_a.jpg')
        top = ' top' if o.get('pos') == 'top' else ''
        sub = f'<p>{o["sub"]}</p>' if o.get('sub') else ''
        secs.append(f'<section class="s" id="{sid}"><img class="full" src="{f}"><div class="shade{" up" if top else ""}"></div><div class="tl">Hitesh Chawla<b>Hotel &amp; interior photographer</b></div><div class="cv{top}"><h1>{o["title"]}</h1>{sub}</div><div class="sw">Swipe</div></section>')
    elif L == 'mat':
        f = prep(o['image'], o['crop'], f'{sid}_a.jpg')
        secs.append(f'<section class="s" id="{sid}"><img class="mat" src="{f}"><div class="cap"><div class="n">{o["n"]}<span>{o["label"]}</span></div><h2>{o["title"]}</h2><div class="m">{meta(o)}</div></div>{ft}</section>')
    elif L == 'wide':
        f = prep(o['image'], o.get('crop'), f'{sid}_a.jpg')
        note = f'<p>{o["note"]}</p>' if o.get('note') else ''
        secs.append(f'<section class="s" id="{sid}"><div class="thm"><span>{spec["theme"]}</span><span></span></div><img class="wide" src="{f}"><div class="wcap"><div class="n">{o["n"]}<span>{o["label"]}</span></div><h2>{o["title"]}</h2>{note}<div class="m">{meta(o)}</div></div>{ft}</section>')
    elif L == 'duo':
        a, b = o['images']
        fa = prep(a['image'], a['crop'], f'{sid}_a.jpg'); fb = prep(b['image'], b['crop'], f'{sid}_b.jpg')
        ma, mb = meta(a), meta(b)
        secs.append(f'<section class="s" id="{sid}"><img class="du a" src="{fa}"><img class="du b" src="{fb}"><div class="dl a">{a["label"]}<small>{ma}</small></div><div class="dl b">{b["label"]}<small>{mb}</small></div><div class="dcap"><div class="n">{o["n"]}<span>{o["tag"]}</span></div><h2>{o["title"]}</h2></div>{ft}</section>')
    elif L == 'note':
        rows = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in o['lines'])
        secs.append(f'<section class="s note" id="{sid}"><div class="k">{o["kicker"]}</div><h2>{o["title"]}</h2><div class="nl">{rows}</div>{ft}</section>')
    elif L == 'close':
        th = ''.join(f'<img src="{sq(t["image"], t.get("x", .4), f"{sid}_t{j}.jpg")}">' for j, t in enumerate(o['thumbs']))
        secs.append(f'<section class="s end" id="{sid}"><div class="strip">{th}</div><h2>{o["title"]}</h2><p>{o["body"]}</p><div class="k">{o["line"]}</div><div class="h"><b>Hitesh Chawla</b><span>@hiteshchawla.interiors</span></div></section>')
    elif L == 'close_photo':
        f = prep(o['image'], o['crop'], f'{sid}_a.jpg')
        secs.append(f'<section class="s end endp" id="{sid}"><img class="full" src="{f}"><div class="shade2"></div><h2>{o["title"]}</h2><p>{o["body"]}</p><div class="k">{o["line"]}</div><div class="h"><b>Hitesh Chawla</b><span>@hiteshchawla.interiors</span></div></section>')
    else: raise SystemExit(f'unknown layout {L}')
po = spec['post']; ids.append('p1')
if po['layout'] == 'mat':
    f = prep(po['image'], po['crop'], 'p1_a.jpg')
    secs.append(f'<section class="s" id="p1"><img class="mat" src="{f}"><div class="cap"><div class="n"><span style="margin-left:0">{po.get("label","")}</span></div><h2>{po["title"]}</h2><div class="m">{meta(po)}</div></div></section>')
else:
    f = prep(po['image'], po['crop'], 'p1_a.jpg')
    secs.append(f'<section class="s post" id="p1"><img class="full" src="{f}"><div class="shade"></div><div class="cap2"><h2>{po["title"]}</h2><div class="m">{meta(po)}</div></div></section>')
html = (SK/'templates'/'slides.html').read_text().replace('<!--SECTIONS-->', '\n'.join(secs))
(out/'slides.html').write_text(html)
subprocess.run(['node', str(HERE/'render.js'), str(out.resolve()), ','.join(ids)], check=True)
for i in ids: Image.open(out/f'{i}.png').convert('RGB').save(out/f'{i}.jpg', quality=93)
json.dump({'caption': spec.get('caption', ''), 'post_caption': spec.get('post_caption', ''), 'theme': spec['theme'], 'date': spec.get('date'), 'ids': ids, 'allow_names': spec.get('allow_names', False)}, open(out/'content.json', 'w'), ensure_ascii=False, indent=1)
if '--ledger' in sys.argv:
    lp = SK/'ledger.json'; led = json.load(open(lp)) if lp.exists() else {}
    for u in set(used): led[u] = spec.get('date', '')
    json.dump(led, open(lp, 'w'), indent=1)
print('built', ids); [print('WARN', w) for w in warn]
