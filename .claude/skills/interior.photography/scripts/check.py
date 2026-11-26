"""Preflight for a built day folder. Usage: python3 check.py outdir
Fails on: phone numbers, hotel names (unless allow_names), wrong image size, titles over 2 lines, bad hashtag count, price on organic image."""
import json, re, sys, pathlib
from PIL import Image
d = pathlib.Path(sys.argv[1]); c = json.load(open(d/'content.json')); html = (d/'slides.html').read_text()
text = re.sub(r'<[^>]+>', ' ', re.sub(r'<style.*?</style>', '', html, flags=re.S)) + ' ' + c['caption'] + ' ' + c['post_caption']
errs = []
for i in c['ids']:
    w, h = Image.open(d/f'{i}.jpg').size
    if (w, h) != (1080, 1350): errs.append(f'{i}.jpg is {w}x{h}, need 1080x1350')
if re.search(r'(\+?\d[\d\s\-]{8,}\d)', re.sub(r'\d+ ?/ ?\d+', '', text)): errs.append('phone-like number found')
if '₹' in html or re.search(r'\bRs\.?\s?\d', html): errs.append('price on an image')
NAMES = ['gold souk', 'goldsouk', 'shimla', 'joystreet', 'shanti palace', 'hotel pearl', 'park blue', 'parkblue', 'tara palace', 'mamra', 'silver ferns', 'silverferns', "palm d'or", 'palmdor', 'jivitesh', 'garv', 'grandway', 'hotel crown', 'stay well', 'banz', 'krishna', 'shipra', 'rwa', 'rajan wadhwa']
if not c.get('allow_names'):
    low = text.lower()
    for n in NAMES:
        if n in low: errs.append(f'property name "{n}" found (not allowed unless allow_names)')
for t in re.findall(r'<h[12][^>]*>(.*?)</h[12]>', html, flags=re.S):
    if t.count('<br>') > 1: errs.append(f'title has more than 2 lines: {t[:40]}')
for key in ('caption', 'post_caption'):
    tags = re.findall(r'#\w+', c[key])
    if not 6 <= len(tags) <= 8: errs.append(f'{key}: {len(tags)} hashtags (want 6-8)')
    if len(c[key]) > 2200: errs.append(f'{key} too long')
print('PASS' if not errs else 'FAIL'); [print(' -', e) for e in errs]; sys.exit(1 if errs else 0)
