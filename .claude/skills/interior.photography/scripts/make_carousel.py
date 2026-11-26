"""Build the interior.photography carousel (5 slides) and single post from a JSON spec.
Usage: python3 make_carousel.py spec.json outdir
Crop values are fractions of the original image: [x0, y0, x1, y1]. A 4:5 crop of a 3:2 photo is width 0.5333, full height."""
import json, os, sys, subprocess, pathlib
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
HERE = pathlib.Path(__file__).resolve().parent
spec = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)

def prep(img, crop, name, width=1620):
    im = Image.open(img).convert('RGB'); W, H = im.size
    x0, y0, x1, y1 = crop
    c = im.crop((int(x0*W), int(y0*H), int(x1*W), int(y1*H)))
    c = c.resize((width, int(c.height*width/c.width)), Image.LANCZOS)
    c.save(out/name, quality=92); return name

def sq(img, x, name):
    im = Image.open(img).convert('RGB'); W, H = im.size; s = H; x0 = min(int(x*W), W-s)
    im.crop((x0, 0, x0+s, s)).resize((600, 600), Image.LANCZOS).save(out/name, quality=90); return name

cv = spec['cover']; n = len(spec['frames']); total = n + 2
cover = prep(cv['image'], cv['crop'], 'cover.jpg')
sections = [f'<section class="s" id="c1"><img class="full" src="{cover}"><div class="shade"></div><div class="tl">Hitesh Chawla<b>Hotel &amp; interior photographer</b></div><div class="cv"><h1>{cv["title"]}</h1></div><div class="sw">Swipe</div></section>']
for i, f in enumerate(spec['frames'], 1):
    fn = prep(f['image'], f['crop'], f'frame{i}.jpg')
    meta = f.get('meta', '')
    sections.append(f'<section class="s" id="c{i+1}"><img class="mat" src="{fn}"><div class="cap"><div class="n">{i:02d}<span>{f["label"]}</span></div><h2>{f["title"]}</h2><div class="m">{meta}</div></div><div class="ft"><span>Hitesh Chawla</span><span>{i+1} / {total}</span></div></section>')
cl = spec['closing']
thumbs = ''.join(f'<img src="{sq(t["image"], t.get("x", .4), f"sq{j}.jpg")}">' for j, t in enumerate(cl['thumbs']))
sections.append(f'<section class="s end" id="c{n+2}"><div class="strip">{thumbs}</div><h2>{cl["title"]}</h2><p>{cl["body"]}</p><div class="k">{cl["line"]}</div><div class="h"><b>Hitesh Chawla</b><span>@hiteshchawla.interiors</span></div></section>')
po = spec['post']
pf = prep(po['image'], po['crop'], 'post.jpg')
sections.append(f'<section class="s post" id="p1"><img class="full" src="{pf}"><div class="shade"></div><div class="cap2"><h2>{po["title"]}</h2><div class="m">{po.get("meta","")}</div></div></section>')
html = (HERE.parent/'templates'/'slides.html').read_text().replace('<!--SECTIONS-->', '\n'.join(sections))
(out/'slides.html').write_text(html)
ids = [f'c{i}' for i in range(1, total+1)] + ['p1']
subprocess.run(['node', str(HERE/'render.js'), str(out.resolve()), ','.join(ids)], check=True)
for i in ids:
    Image.open(out/f'{i}.png').convert('RGB').save(out/f'{i}.jpg', quality=93)
print('done:', [f'{i}.jpg' for i in ids])
