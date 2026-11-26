"""Turn a folder of built days (day1..day7/) into a publish plan. Usage: python3 weekplan.py weekdir > plan.md
Carousel 12:00 IST, post 19:00 IST. Prints files, times and captions so drafting in vidIQ is copy-paste."""
import json, sys, pathlib
w = pathlib.Path(sys.argv[1]); print('# Week plan\n')
for d in sorted(w.glob('day*/content.json')):
    c = json.load(open(d)); folder = d.parent
    ids = [i for i in c['ids'] if i != 'p1']
    print(f'## {folder.name}: {c["theme"]} ({c["date"]})\n- Carousel 12:00 PM IST: ' + ', '.join(f'{i}.jpg' for i in ids) + '\n- Post 7:00 PM IST: p1.jpg\n')
    print('**Carousel caption**\n\n' + c['caption'] + '\n\n**Post caption**\n\n' + c['post_caption'] + '\n')
