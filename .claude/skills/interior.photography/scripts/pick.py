"""Contact sheet(s) for choosing photos. Skips images already in the ledger and images too small for crisp 4:5 crops.
Usage: python3 pick.py out_prefix folder_or_glob [more ...]   -> out_prefix_0.png ...   (numbers on the sheet = list in out_prefix.txt)"""
import sys, glob, os, json, pathlib
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
HERE = pathlib.Path(__file__).resolve().parent
led = json.load(open(HERE.parent/'ledger.json')) if (HERE.parent/'ledger.json').exists() else {}
used = {os.path.basename(k) for k in led}
files = []
for a in sys.argv[2:]:
    files += sorted(glob.glob(a if any(c in a for c in '*?') else os.path.join(a, '*')))
files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
keep = []
for f in files:
    im = Image.open(f); w, h = im.size
    tag = ('USED ' if os.path.basename(f) in used else '') + ('LOWRES ' if min(w, h*0.8) < 850 else '')
    keep.append((f, w, h, tag))
open(sys.argv[1]+'.txt', 'w').write('\n'.join(f'#{i} {f} {w}x{h} {t}' for i, (f, w, h, t) in enumerate(keep)))
per, cols, cw, ch = 48, 8, 250, 190
for s in range(0, len(keep), per):
    chunk = keep[s:s+per]; rows = (len(chunk)+cols-1)//cols
    sheet = Image.new('RGB', (cw*cols, (ch+16)*rows), 'white'); d = ImageDraw.Draw(sheet)
    for k, (f, w, h, t) in enumerate(chunk):
        x = Image.open(f).convert('RGB'); x.thumbnail((cw-4, ch)); X, Y = (k % cols)*cw, (k//cols)*(ch+16)
        sheet.paste(x, (X, Y+16)); d.text((X+3, Y+2), f'#{s+k} {t}', fill=(200, 0, 0))
    sheet.save(f'{sys.argv[1]}_{s//per}.png')
print(len(keep), 'images')
