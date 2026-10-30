from PIL import Image;import os,re
src=open('index.html').read()
css=re.search(r'<style>(.*?)</style>',src,re.S).group(1)
T='Ich habe jedes KI-Video-Tool getestet (tier list)'
cards=''
for n in range(1,201):
  out=f'tierlist/images/{n:03d}.jpg'
  if not os.path.exists(out): Image.open(f'/workspace/thumb-non/tierlist/t{n:03d}.png').convert('RGB').save(out,quality=90)
  cards+=f'<div class="c"><div class="t"><a href="images/{n:03d}.jpg" target="_blank"><img loading="lazy" src="images/{n:03d}.jpg"></a><span class="b">12:34</span><span class="n">#{n:03d}</span></div><div class="m"><div class="a">N</div><div><div class="ti">{T}</div><div class="s">nonafterdark</div><div class="s">XX Aufrufe • vor X Tagen</div></div></div></div>'
open('tierlist/index.html','w').write(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Thumbnail Feed – Tier List</title><style>{css}</style></head><body><div class="tabs"><a href="../"><button>← Claude-Run</button></a><button class="on">Tier List (200)</button></div><div class="g">{cards}</div></body></html>')
