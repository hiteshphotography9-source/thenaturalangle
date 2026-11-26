"""Print camera settings for a JPG as: 11mm · f/8 · 1/5s · ISO 250 (prints 'no full EXIF' if missing; never guesses). Also importable: settings(path)."""
import sys
from PIL import Image
from PIL.ExifTags import TAGS
Image.MAX_IMAGE_PIXELS = None
def settings(p):
    try:
        e = Image.open(p).getexif(); ex = e.get_ifd(0x8769)
    except Exception:
        return ''
    d = {TAGS.get(k, k): v for k, v in {**dict(e), **ex}.items()}
    fl, fn, et, iso = d.get('FocalLength'), d.get('FNumber'), d.get('ExposureTime'), d.get('ISOSpeedRatings')
    if not (fl and fn and et and iso): return ''
    et = float(et); t = f"{et:.1f}s" if et >= .3 else f"1/{round(1/et)}s"
    return f"{round(float(fl))}mm · f/{float(fn):g} · {t} · ISO {iso}"
if __name__ == '__main__':
    for p in sys.argv[1:]: print(p, '->', settings(p) or 'no full EXIF')
