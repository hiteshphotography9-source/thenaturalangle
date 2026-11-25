"""Refresh data/feed.json with the latest YouTube uploads and Instagram posts.
Runs in GitHub Actions on a schedule. YouTube needs no key (public RSS).
Instagram is updated only when the IG_TOKEN secret is set (Instagram API long-lived token)."""
import json, os, sys, urllib.request, urllib.error, xml.etree.ElementTree as ET, datetime, pathlib

CHANNEL = "UC_fN2PYbjuB16k6wqI64e6A"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "feed.json"
UA = {"User-Agent": "Mozilla/5.0 (feed updater)"}

def get(url, **kw):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30, **kw)

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None

def is_short(vid):
    op = urllib.request.build_opener(NoRedirect)
    try:
        r = op.open(urllib.request.Request(f"https://www.youtube.com/shorts/{vid}", headers=UA), timeout=20)
        return r.status == 200
    except urllib.error.HTTPError as e:
        return False
    except Exception:
        return None

def youtube(old):
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "m": "http://search.yahoo.com/mrss/"}
    root = ET.fromstring(get(f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL}").read())
    known = {v["id"]: v.get("short") for v in old.get("long", []) + old.get("shorts", [])}
    for v in old.get("long", []): known[v["id"]] = False
    for v in old.get("shorts", []): known[v["id"]] = True
    longs, shorts = [], []
    for e in root.findall("a:entry", ns):
        vid = e.find("yt:videoId", ns).text
        item = {"id": vid, "title": e.find("a:title", ns).text, "published": e.find("a:published", ns).text}
        s = known.get(vid)
        if s is None: s = is_short(vid)
        if s is None: s = False
        (shorts if s else longs).append(item)
    # keep older items we already had so lists stay full
    def merge(new, prev, n):
        ids = {x["id"] for x in new}
        return (new + [x for x in prev if x["id"] not in ids])[:n]
    return {"long": merge(longs, old.get("long", []), 12), "shorts": merge(shorts, old.get("shorts", []), 12)}

def instagram(old):
    tok = os.environ.get("IG_TOKEN")
    if not tok: return old
    url = ("https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,timestamp"
           f"&limit=12&access_token={tok}")
    data = json.load(get(url)).get("data", [])
    imgdir = ROOT / "data" / "ig"; imgdir.mkdir(parents=True, exist_ok=True)
    out = []
    for p in data:
        thumb = p.get("thumbnail_url") or p.get("media_url")
        local = None
        if thumb:
            local = f"data/ig/{p['id']}.jpg"
            try:
                (ROOT / local).write_bytes(get(thumb).read())
            except Exception:
                local = None
        cap = (p.get("caption") or "").strip().split("\n")[0][:110]
        out.append({"permalink": p["permalink"], "caption": cap, "type": p.get("media_type"), "thumb": local, "timestamp": p.get("timestamp")})
    keep = {x["thumb"] for x in out if x["thumb"]}
    for f in imgdir.glob("*.jpg"):
        if f"data/ig/{f.name}" not in keep: f.unlink()
    return out

def main():
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    new = dict(old)
    try: new["youtube"] = youtube(old.get("youtube", {}))
    except Exception as e: print("youtube failed:", e, file=sys.stderr)
    try: new["instagram"] = instagram(old.get("instagram", []))
    except Exception as e: print("instagram failed:", e, file=sys.stderr)
    if new != old:
        new["updated"] = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        OUT.write_text(json.dumps(new, ensure_ascii=False, indent=1))
        print("feed updated")
    else:
        print("no change")

if __name__ == "__main__":
    main()
