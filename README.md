# vrdlovec.cz

Osobní web Richarda Vrdlovce. Statická stránka, žádný build.

## Co je kde

| | |
|---|---|
| `index.html` | celá stránka, jeden soubor |
| `img/` | 126 souborů — 42 velikostí × AVIF / WebP / JPEG |
| `font/` | Archivo, variabilní, hostovaný lokálně (ne z Google Fonts) |
| `CNAME` | doména pro GitHub Pages |
| `.nojekyll` | vypne Jekyll, ať Pages servírují soubory tak, jak jsou |

## Jak měnit obrázky

`produkce.py` vygeneruje celou sadu z originálů v `AI\R\Fotky zdroje`.
`sestav.py` z prototypu poskládá `index.html` se `srcset`.
Zdroje a postup jsou popsané v `AI\R\Web prototyp\predavka-do-code.md`, oddíl 5b.

## Proč to nesedí v OneDrivu

Git a OneDrive si do sebe kopou: OneDrive synchronizuje i `.git/`, takže zámky
a index se dají zasynchronizovat uprostřed operace, a soubory „na vyžádání"
se tváří jako přítomné, i když na disku nejsou. V téhle relaci to už jednou
padlo — fotka k heru šla přečíst až napodruhé, protože byla jen zástupná.

Repozitáře všech webů proto leží v `C:\Users\Public\Documents\Repository\`.
Zálohu a synchronizaci tady dělá GitHub, ne OneDrive. Zdroje (`Fotky zdroje`,
`Web prototyp`, předávka) zůstávají v OneDrivu, kam patří.

## Nasazení

GitHub Pages z větve `main`, složka `/`. Postup krok za krokem je v předávce.
