# -*- coding: utf-8 -*-
"""Produkcni sady obrazku pro vrdlovec.cz.
   Z originalu v archivu (plne rozliseni) -> recept C -> tonalita srovnana
   histogramem proti schvalene verzi z prototypu (pres obraceny LUT) ->
   sada sirek v AVIF / WebP / JPEG."""
import io, os, re, base64, sys
from PIL import Image, ImageOps, ImageEnhance
Image.MAX_IMAGE_PIXELS=None

PROTO='C:/Users/vrdlo/OneDrive - Nadační fond pro skutečně strádající/Dokumenty/AI/R/Web prototyp/vrdlovec.html'
ARCH='C:/Users/vrdlo/OneDrive - Nadační fond pro skutečně strádající/Dokumenty/AI/R/Fotky zdroje/'
VAR='C:/Users/vrdlo/OneDrive - Nadační fond pro skutečně strádající/Dokumenty/AI/R/Web prototyp/img/golda-varianty/golda-Q.jpg'
OUT='produkce/img'
# hero lezi ve slozce, jejiz jmeno obsahuje znak, ktery Windows mapuje
# do privatni zony () - cesta se proto bere z ulozeneho parovani
import json
HERO=json.load(io.open('parovani.json',encoding='utf-8'))['hero']['kandidati'][1]['soubor'].replace(chr(92),'/')
os.makedirs(OUT, exist_ok=True)

# jmeno, index v prototypu, zdroj, otoceni, sirky
UKOLY=[
 ('hero',        0, ARCH+HERO, 0, [640,960,1280,1920]),
 ('golda',       1, VAR,                                0, [600,900,1200,1800,2400]),
 ('zpravodaj',   2, ARCH+'Identity/Marty/RICHARD3/3I8A6170-2.jpg', 0, [400,600,900,1300]),
 ('fond',        3, ARCH+'Identity/Marty/V obleku Zf/3I8A2355.jpg', 0, [400,600,900,1300]),
 ('fond-fondu',  4, ARCH+'Identity/Marty/RICHARD2/3I8A1964.jpg', 0, [400,600,900,1300]),
 ('les',         5, ARCH+'Identity/Marty/RICHARD3/3I8A6185.jpg', 0, [640,960,1280,1920]),
 ('yoga-karlin', 6, ARCH+'_YK martin/DSC_0010 (3).JPG', 270, [400,600,900,1300]),
 ('kurz-meditace',7,ARCH+'Identity/Vlastní/3I8A5935.jpg', 0, [400,600,900,1300]),
 ('nirvana',     8, ARCH+'Identity/Marty/RICHARD2/3I8A2027.jpg', 0, [400,600,900,1300,1800]),
 ('kurz-online', 9, ARCH+'Richard fotky/IMG_20210822_103301_754.jpg', 0, [400,600,900,1300]),
]

stopy=[(0.00,(0x19,0x0F,0x2E)),(0.30,(46,40,56)),(0.70,(170,168,172)),(1.00,(0xFE,0xFB,0xF3))]
lut=[[],[],[]]
for i in range(256):
    t=i/255.0
    for j in range(len(stopy)-1):
        t0,c0=stopy[j]; t1,c1=stopy[j+1]
        if t0<=t<=t1:
            f=0 if t1==t0 else (t-t0)/(t1-t0)
            for k in range(3): lut[k].append(int(c0[k]+(c1[k]-c0[k])*f+0.5))
            break
fj=[0.299*lut[0][v]+0.587*lut[1][v]+0.114*lut[2][v] for v in range(256)]
finv=[min(range(256), key=lambda v: abs(fj[v]-y)) for y in range(256)]

def cdf(h):
    n=sum(h); c=0; o=[]
    for k in h: c+=k; o.append(c/n)
    return o
def srovnej(src,cil):
    cs=cdf(src.histogram()); cc=cdf(cil); m=[]; j=0
    for v in range(256):
        while j<255 and cc[j]<cs[v]: j+=1
        m.append(j)
    return src.point(m)

s=io.open(PROTO,encoding='utf-8').read()
uris=re.findall(r'src="(data:image/[a-z+]+;base64,[^"]+)"', s)

def receptC_sedy(im):
    g=ImageOps.grayscale(im)
    g=ImageOps.autocontrast(g,cutoff=1)
    return ImageEnhance.Contrast(g).enhance(1.12)

manifest=[]
for jm, idx, zdroj, otoc, sirky in UKOLY:
    schvaleny=Image.open(io.BytesIO(base64.b64decode(uris[idx].split(',',1)[1])))
    if jm=='golda':
        mistr=Image.open(zdroj)                       # uz je po receptu C
    else:
        im=Image.open(zdroj)
        if otoc: im=im.rotate(otoc, expand=True)
        # orez na pomer schvalene verze
        ps=schvaleny.size[0]/schvaleny.size[1]
        w,h=im.size
        if w/h > ps: nw=int(h*ps); im=im.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
        else:        nh=int(w/ps); im=im.crop((0,(h-nh)//2,w,(h-nh)//2+nh))
        g=receptC_sedy(im)
        cil=[0]*256
        for v,k in enumerate(ImageOps.grayscale(schvaleny).histogram()): cil[finv[v]]+=k
        g=srovnej(g,cil)
        mistr=Image.merge('RGB',[g.point(lut[k]) for k in range(3)])
    print('%-14s zdroj %s -> mistr %s' % (jm, os.path.basename(zdroj)[:30], mistr.size), flush=True)
    for w in sirky:
        if w>mistr.size[0]:
            print('   %4d px  PRESKOCENO (mistr ma jen %d)'%(w,mistr.size[0]), flush=True); continue
        v=mistr.resize((w, round(w*mistr.size[1]/mistr.size[0])), Image.LANCZOS)
        radek={'jmeno':jm,'sirka':w,'vyska':v.size[1]}
        for fmt,ext,kw in (('AVIF','avif',{'quality':52,'speed':6}),
                           ('WEBP','webp',{'quality':72,'method':6}),
                           ('JPEG','jpg', {'quality':74,'optimize':True,'progressive':True})):
            p=os.path.join(OUT,'%s-%d.%s'%(jm,w,ext))
            v.save(p,fmt,**kw); radek[ext]=os.path.getsize(p)
        manifest.append(radek)
        print('   %4d px  avif %5.0f kB  webp %5.0f kB  jpg %5.0f kB'%(
              w,radek['avif']/1024,radek['webp']/1024,radek['jpg']/1024), flush=True)
import json
io.open('produkce/manifest.json','w',encoding='utf-8').write(json.dumps(manifest,ensure_ascii=False,indent=1))
print('\nHOTOVO: %d renditions, %d souboru'%(len(manifest),len(manifest)*3))
