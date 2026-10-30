import random,os,glob
from PIL import Image,ImageDraw,ImageFont,ImageFilter
G='/usr/share/fonts/truetype/sand-box/google/'
FA=G+'Anton/Anton-Regular.ttf';FB=G+'Archivo Black/ArchivoBlack-Regular.ttf'
W,H=1280,720
L={os.path.basename(f)[:-4]:Image.open(f).convert('RGBA') for f in glob.glob('/workspace/thumb-non/tierlist-v2/logos/final/*.png')}
NAMES=sorted(L)
TC={'S':'#ff4b4b','A':'#ff9f2e','B':'#ffd93b','C':'#7ee26b','D':'#4fb3ff','F':'#9b6bff'}
TEXTS=['ALLE GETESTET','NUR 1 IST S-TIER','S-TIER?','KI-VIDEO-TOOLS','NICHT KAUFEN','WELCHES GEWINNT?','EHRLICH GERANKT','ALLES GETESTET','DAS IST S-TIER','SPAR DIR DAS']
def font(f,s):return ImageFont.truetype(f,s)
def logo(name,s,r=0.22):
  im=L[name].copy();im.thumbnail((s,s));T=Image.new('RGBA',(s,s),(0,0,0,0));T.alpha_composite(im,((s-im.width)//2,(s-im.height)//2));return T
def blurred(name,s):
  T=Image.new('RGBA',(s,s),(0,0,0,0));m=Image.new('L',(s,s));ImageDraw.Draw(m).rounded_rectangle((0,0,s-1,s-1),s//5,fill=255)
  T.paste(Image.new('RGBA',(s,s),'#e8e8e8'),(0,0),m);T.alpha_composite(logo(name,int(s*.9)),(s//20,s//20))
  B=T.filter(ImageFilter.GaussianBlur(s/6));B.putalpha(m);return B
def qbox(s,col='#ffffff'):
  T=Image.new('RGBA',(s,s),(0,0,0,0));d=ImageDraw.Draw(T);d.rounded_rectangle((0,0,s-1,s-1),s//5,fill='#1d1d24',outline=col,width=max(4,s//28));f=font(FA,int(s*.8));d.text((s/2,s/2),'?',font=f,fill=col,anchor='mm');return T
def bg(r,style):
  if style==0:
    c1,c2=r.choice([('#0b0b12','#1c1030'),('#06121f','#0c2a3d'),('#140707','#2b0d0d'),('#0d0d0d','#262626')])
  elif style==1:c1,c2=('#f4f4f4','#d9d9d9')
  else:c1,c2=r.choice([('#1a0033','#4b0082'),('#001a12','#004d33'),('#202020','#3a3a3a')])
  im=Image.new('RGB',(W,H),c1);top=Image.new('RGB',(W,H),c2);m=Image.linear_gradient('L').rotate(r.choice([0,90,180,270])).resize((W,H))
  return Image.composite(top,im,m).convert('RGBA')
def stroke_text(d,xy,t,f,fill,anchor='la',sw=8):
  mw=1200 if anchor=='mm' else 1240-xy[0] if anchor[0]=='l' else xy[0]-40
  while d.textlength(t,font=f)>mw:f=ImageFont.truetype(f.path,int(f.size*.92))
  d.text(xy,t,font=f,fill=fill,anchor=anchor,stroke_width=sw,stroke_fill='black')
def photo(im,x,y,w,h):
  d=ImageDraw.Draw(im);d.rounded_rectangle((x,y,x+w,y+h),30,fill=(60,60,70,255),outline='#ffffff',width=4)
  cx=x+w//2;d.ellipse((cx-w*.22,y+h*.18,cx+w*.22,y+h*.18+w*.44),fill=(95,95,108));d.rounded_rectangle((cx-w*.38,y+h*.62,cx+w*.38,y+h+40),60,fill=(95,95,108))
  im.alpha_composite(Image.new('RGBA',(W,H),(0,0,0,0)));d.text((cx,y+h-28),'DEIN FOTO',font=font(FB,30),fill='#ffffff',anchor='mm')
def arrow(d,p0,p1,col='#ff2020',w=16):
  d.line([p0,p1],fill=col,width=w);import math;a=math.atan2(p1[1]-p0[1],p1[0]-p0[0]);s=46
  d.polygon([p1,(p1[0]-s*math.cos(a-.5),p1[1]-s*math.sin(a-.5)),(p1[0]-s*math.cos(a+.5),p1[1]-s*math.sin(a+.5))],fill=col)
def tiers(im,r,rows,x0,y0,w,h,sz,picks,mode,lab='S'):
  d=ImageDraw.Draw(im);rh=h//len(rows);import itertools;it=itertools.cycle(picks);cap=max(1,(len(picks)-1)//len(rows));mark=None
  for i,t in enumerate(rows):
    y=y0+i*rh;d.rectangle((x0,y,x0+rh,y+rh-4),fill=TC[t]);d.text((x0+rh/2,y+rh/2),t,font=font(FA,int(rh*.7)),fill='black',anchor='mm')
    d.rectangle((x0+rh,y,x0+w,y+rh-4),fill=(25,25,30,235))
    n=max(1,min(sz,(w-rh)//(rh)))
    k=1 if (t=='S' and mode in('blur','q','one')) else r.randint(1,min(n,cap))
    for j in range(k):
      s=rh-18;x=x0+rh+12+j*(s+12)
      if t=='S' and mode=='blur':tile=blurred(next(it),s)
      elif t=='S' and mode=='q':tile=qbox(s,'#ffd93b')
      else:tile=logo(next(it),s)
      im.alpha_composite(tile,(x,y+7))
      if t=='S' and j==0:mark=(x,y+7,s)
  return mark
def make(n):
  r=random.Random(n*7919);lay=n%8;im=bg(r,0 if lay!=5 else r.choice([0,2]));d=ImageDraw.Draw(im)
  picks=r.sample(NAMES,len(NAMES));txt=r.choice(TEXTS);ph=r.random()<.6;tcol=r.choice(['#ffffff','#ffd93b','#ff4b4b'])
  if lay in(0,1,2):  # few rows, big logos
    rows=r.choice([['S','A','F'],['S','C','F'],['S','B','F'],['S','F']]);mode=['blur','q','one'][lay]
    w=760 if ph else 1180;m=tiers(im,r,rows,40,150,w,540,3,picks,mode)
    stroke_text(d,(40,25),txt,font(FA,100),tcol)
    if ph:photo(im,850,170,400,550)
    if mode!='one' and r.random()<.7:
      x,y,s=m;d.ellipse((x-14,y-14,x+s+14,y+s+14),outline='#ff2020',width=12)
  elif lay==3:  # full S-F, small, face
    rows=['S','A','B','C','D','F'];w=820 if ph else 1200
    tiers(im,r,rows,40,40,w,640,6,picks,r.choice(['blur','q','plain']))
    if ph:photo(im,890,60,360,520)
    stroke_text(d,(1240 if ph else 1240,700),txt,font(FA,72),tcol,'rd')
  elif lay==4:  # one huge blurred S logo + arrow
    s=420;n0=picks[0];im.alpha_composite(blurred(n0,s) if r.random()<.6 else qbox(s,'#ffd93b'),(90,200));d=ImageDraw.Draw(im)
    d.rounded_rectangle((60,170,540,650),40,outline=TC['S'],width=14);d.rounded_rectangle((40,120,190,250),20,fill=TC['S']);d.text((115,185),'S',font=font(FA,120),fill='black',anchor='mm')
    stroke_text(d,(600,60),txt,font(FA,110),tcol)
    if ph:photo(im,860,220,380,500)
    else:
      for j,nm in enumerate(picks[1:5]):im.alpha_composite(logo(nm,170),(620+(j%2)*200,250+(j//2)*200))
    arrow(ImageDraw.Draw(im),(720,230),(560,330))
  elif lay==5:  # floating app icon grid, one "?" 
    k=r.choice([6,8,10]);cols=k//2;s=200 if k<10 else 170;gx=40;gy=210
    q=r.randrange(k)
    for j in range(k):
      t=qbox(s,'#ffd93b') if j==q else logo(picks[j],s);t=t.rotate(r.uniform(-8,8),expand=True,resample=Image.BICUBIC)
      im.alpha_composite(t,(gx+(j%cols)*(s+20),gy+(j//cols)*(s+30)))
    stroke_text(d,(40,30),txt,font(FA,110),tcol)
    if ph and cols*(s+20)+gx<860:photo(im,880,180,370,520)
  elif lay==6:  # versus S vs F
    a,b=picks[:2];s=380;[d.rounded_rectangle((x-25,195,x+s+25,625),40,fill=(255,255,255,40)) for x in(70,830)];im.alpha_composite(logo(a,s),(70,220));im.alpha_composite(logo(b,s) if r.random()<.5 else blurred(b,s),(830,220))
    for x,t in((70,'S'),(830,'F')):d.rounded_rectangle((x+s-110,180,x+s+20,310),20,fill=TC[t]);d.text((x+s-45,245),t,font=font(FA,110),fill='black',anchor='mm')
    stroke_text(d,(640,420),'VS',font(FA,160),'#ffffff','mm')
    stroke_text(d,(640,90),txt,font(FA,110),tcol,'mm')
  else:  # S row only, rest in "trash" F
    s=230;d.rectangle((0,160,W,160+s+40),fill=(25,25,30,240));d.rectangle((0,160,190,160+s+40),fill=TC['S']);d.text((95,160+(s+40)/2),'S',font=font(FA,200),fill='black',anchor='mm')
    im.alpha_composite(blurred(picks[0],s) if r.random()<.5 else qbox(s,'#ffd93b'),(230,180))
    d=ImageDraw.Draw(im);d.rectangle((0,470,W,H),fill=(25,25,30,240));d.rectangle((0,470,190,H),fill=TC['F']);d.text((95,595),'F',font=font(FA,200),fill='black',anchor='mm')
    for j,nm in enumerate(picks[1:7]):im.alpha_composite(logo(nm,170),(220+j*175,500))
    stroke_text(d,(40,25),txt,font(FA,110),tcol)
    if ph:photo(im,880,30,370,430)
  return im.convert('RGB')
if __name__=='__main__':
  for n in range(1,161):make(n).save(f'/workspace/thumb-non/tierlist-v2/out/{n:03d}.jpg',quality=90)
