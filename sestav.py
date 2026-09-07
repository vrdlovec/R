# -*- coding: utf-8 -*-
"""Sestaveni produkcni slozky: base64 -> soubory se srcset, font lokalne."""
import io, re, os, json, shutil
PROTO='C:/Users/vrdlo/OneDrive - Nadační fond pro skutečně strádající/Dokumenty/AI/R/Web prototyp/vrdlovec.html'
OUT='produkce'
s=io.open(PROTO,encoding='utf-8').read()
man=json.load(io.open(OUT+'/manifest.json',encoding='utf-8'))
sirky={}
for r in man: sirky.setdefault(r['jmeno'],[]).append((r['sirka'],r['vyska']))
for k in sirky: sirky[k].sort()

CELA='100vw'
def sz(px, vw1081):
    return ('(min-width:1568px) %dpx, (min-width:1081px) %dvw, '
            '(min-width:761px) 46vw, 92vw') % (px, vw1081)
POPIS=[
 ('hero','Richard Vrdlovec', CELA, 'eager','high'),
 ('golda','',  sz(1200,84), 'lazy',None),
 ('zpravodaj','', sz(645,45),'lazy',None),
 ('fond','',      sz(535,37),'lazy',None),
 ('fond-fondu','',sz(535,37),'lazy',None),
 ('les','',       CELA,      'lazy',None),
 ('yoga-karlin','',sz(420,29),'lazy',None),
 ('kurz-meditace','',sz(645,45),'lazy',None),
 ('nirvana','',   sz(865,61),'lazy',None),
 ('kurz-online','',sz(535,37),'lazy',None),
]
def srcset(jm, ext):
    return ', '.join('img/%s-%d.%s %dw'%(jm,w,ext,w) for w,h in sirky[jm])

# --- nahrazeni obrazku ---
mista=[m for m in re.finditer(r'<img([^>]*?)src="data:image/[a-z+]+;base64,[^"]+"([^>]*?)>', s)]
assert len(mista)==10, len(mista)
for m,(jm,alt,sizes,load,pri) in reversed(list(zip(mista,POPIS))):
    pred, po = m.group(1), m.group(2)
    tridy=re.search(r'class="([^"]*)"', pred+po)
    tridy=tridy.group(1) if tridy else ''
    w,h=sirky[jm][-1]
    atr='class="%s" '%tridy if tridy else ''
    pict=('<picture>'
          '<source type="image/avif" sizes="%s" srcset="%s">'
          '<source type="image/webp" sizes="%s" srcset="%s">'
          '<img %ssrc="img/%s-%d.jpg" sizes="%s" srcset="%s" '
          'width="%d" height="%d" alt="%s" loading="%s" decoding="async"%s>'
          '</picture>') % (sizes,srcset(jm,'avif'), sizes,srcset(jm,'webp'),
                           atr, jm, w, sizes, srcset(jm,'jpg'), w,h, alt, load,
                           ' fetchpriority="high"' if pri else '')
    s=s[:m.start()]+pict+s[m.end():]

# <picture> je inline a rozbil by pravidla psana pro hole <img>
# (.tm img { height:100% } by se vztahlo k obalu bez vysky a obrazky
# by se smrskly na nulu; s loading=lazy by se pak vubec nenacetly).
# display:contents obal z rozvrzeni vyradi a puvodni CSS plati beze zmeny.
one_img="img { display:block; max-width:100%; }"
assert s.count(one_img)==1
s=s.replace(one_img, one_img+chr(10)+"picture { display:contents; }",1)

# --- font lokalne ---
gf=io.open('gf.css',encoding='utf-8').read()
bloky=[]
for blok in re.findall(r'@font-face\s*\{[^}]*\}', gf):
    url=re.search(r'url\((https://fonts\.gstatic\.com/[^)]+)\)', blok)
    if not url: continue
    lok='font/archivo-'+os.path.basename(url.group(1))
    bloky.append(blok.replace(url.group(1), lok).replace("font-display: swap","font-display: swap"))
one=('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
     '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap">')
assert s.count(one)==1
s=s.replace(one, '<style>\n'+'\n'.join(bloky)+'\n</style>\n'
    '<link rel="preload" href="font/archivo-'+os.path.basename(
        re.findall(r'url\((https://fonts\.gstatic\.com/[^)]+)\)', gf)[-1])+'" as="font" type="font/woff2" crossorigin>',1)

# --- hlavicka, kterou artefakt doplnoval sam ---
s=('<!doctype html>\n<html lang="cs">\n<head>\n'+s.replace('<meta charset="utf-8">\n','',1))
s=s.replace('</style>\n\n<header>','</style>\n</head>\n<body>\n\n<header>',1)
s=s.rstrip()+'\n</body>\n</html>\n'
s=s.replace('<meta name="viewport"','<meta charset="utf-8">\n<meta name="viewport"',1)

io.open(OUT+'/index.html','w',encoding='utf-8',newline='\n').write(s)
io.open(OUT+'/CNAME','w',encoding='utf-8',newline='\n').write('vrdlovec.cz\n')
io.open(OUT+'/.nojekyll','w',encoding='utf-8',newline='\n').write('')
print('index.html %.0f kB'%(len(s)/1024))
print('obrazku %d, fontu %d'%(len(os.listdir(OUT+'/img')), len(os.listdir(OUT+'/font'))))
print('kontrola: base64 zbylo %d, <picture> %d'%(s.count('base64,'), s.count('<picture>')))
print('poskozene znacky:', len(re.findall(r'<[a-z0-9]+[^>]*<', s)))
