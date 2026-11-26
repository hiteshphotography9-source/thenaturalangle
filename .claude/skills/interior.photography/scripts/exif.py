"""Print camera settings for a JPG as: 11mm · f/8 · 1/5s · ISO 250  (never guess; prints nothing if EXIF is missing)."""
import sys
from PIL import Image
from PIL.ExifTags import TAGS
Image.MAX_IMAGE_PIXELS = None
for p in sys.argv[1:]:
    e = Image.open(p).getexif(); ex = e.get_ifd(0x8769)
    d = {TAGS.get(k, k): v for k, v in {**dict(e), **ex}.items()}
    fl, fn, et, iso = d.get('FocalLength'), d.get('FNumber'), d.get('ExposureTime'), d.get('ISOSpeedRatings')
    if not (fl and fn and et and iso):
        print(p, '-> no full EXIF'); continue
    et = float(et); t = f"{et:.1f}s" if et >= .3 else f"1/{round(1/et)}s"
    print(p, '->', f"{round(float(fl))}mm · f/{float(fn):g} · {t} · ISO {iso}")
