from PIL import Image;import glob,os,hashlib,json
def ok(f): return not f.endswith('_feed.png')
src=[('tt13',sorted(filter(ok,glob.glob('/workspace/tt13/k*.png'))),'none'),
('tt14',sorted(f for f in filter(ok,glob.glob('/workspace/tt14/c*_v*.png')) if not os.path.basename(f).startswith('c0')),'none'),
('tt15',sorted(filter(ok,glob.glob('/workspace/tt15/p*.png'))),'ph'),
('tt16',sorted(glob.glob('/workspace/tt16/s[0-9][0-9].png')),'ph'),
('tt17',sorted(glob.glob('/workspace/tt17/t[0-9][0-9].png')),'ph'),
    ('tt18',sorted(glob.glob('/workspace/tt18/u[0-9][0-9].png')),'ph')]
items=[];seen=set()
for tag,fs,kind in src:
  for f in fs:
    im=Image.open(f).convert('RGB');h=hashlib.md5(im.resize((32,18)).tobytes()).hexdigest()
    if h in seen: continue
    seen.add(h);n=len(items)+1;out=f'images/{n:03d}.jpg'
    if not os.path.exists(out): im.resize((1280,720)).save(out,quality=80)
    items.append({'n':n,'img':out,'kind':kind,'src':tag+'/'+os.path.basename(f)})
json.dump(items,open('items.json','w'),indent=1)
T='Claude schneidet meine Videos, während ich arbeite'
cards=''.join(f'''<div class="c" data-k="{i['kind']}"><div class="t"><img loading="lazy" src="{i['img']}"><span class="b">12:34</span><span class="n">#{i['n']}</span></div><div class="m"><div class="a">N</div><div><div class="ti">{T}</div><div class="s">nonafterdark</div><div class="s">XX Aufrufe • vor X Tagen</div></div></div></div>''' for i in items)
open('index.html','w').write(f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Thumbnail Feed – Claude</title><style>
body{{background:#0f0f0f;color:#f1f1f1;font-family:Roboto,Arial,sans-serif;margin:0;padding:16px}}
.tabs{{display:flex;gap:10px;margin:0 0 20px}}.tabs button{{background:#272727;color:#f1f1f1;border:0;border-radius:8px;padding:8px 14px;font-size:14px;cursor:pointer}}.tabs button.on{{background:#f1f1f1;color:#0f0f0f}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:40px 16px}}@media(max-width:900px){{.g{{grid-template-columns:repeat(2,1fr)}}}}@media(max-width:560px){{.g{{grid-template-columns:1fr}}}}
.t{{position:relative}}.t img{{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:12px;display:block}}
.b{{position:absolute;right:8px;bottom:8px;background:rgba(0,0,0,.8);font-size:12px;font-weight:500;padding:2px 5px;border-radius:4px}}
.n{{position:absolute;left:8px;top:8px;background:#ffd400;color:#000;font-weight:700;font-size:13px;padding:2px 7px;border-radius:6px}}
.m{{display:flex;gap:12px;margin-top:12px}}.a{{width:36px;height:36px;border-radius:50%;background:#3a3a3a;display:flex;align-items:center;justify-content:center;flex:none}}
.ti{{font-size:16px;font-weight:500;line-height:22px;margin-bottom:4px}}.s{{color:#aaa;font-size:14px;line-height:20px}}</style></head><body>
<div class="tabs"><button class="on" data-f="all">Alle</button><button data-f="ph">mit Platzhalter</button><button data-f="none">ohne Person</button></div><div class="g">{cards}</div>
<script>document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');document.querySelectorAll('.c').forEach(c=>c.style.display=(b.dataset.f=='all'||c.dataset.k==b.dataset.f)?'':'none')}})</script></body></html>''')
print(len(items))
