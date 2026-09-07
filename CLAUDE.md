# vrdlovec.cz — kontext pro Claude Code

Statická stránka, žádný build. Rozhodnutí o obsahu, barvách, fotkách
a rozvržení jsou v předávce `OneDrive\…\Dokumenty\AI\R\Web prototyp\predavka-do-code.md` — přečti ji dřív, než
začneš měnit kód.

Obrázky se nesázejí ručně: `produkce.py` vygeneruje sady velikostí
z originálů, `sestav.py` poskládá `index.html` se `srcset`.

---

## Kde co leží — dvě složky, dvě role

Platí od 7. 9. 2026 pro všechny weby.

| | kde | co tam patří |
|---|---|---|
| **Repozitáře** | `C:\Users\Public\Documents\Repository\` | kód, hotové obrázky, build skripty — všechno, co jde do gitu |
| **Zdroje** | `OneDrive\…\Dokumenty\AI\` | fotoarchivy, návrhy, předávky, rozpracované texty |

**Proč nejsou repozitáře v OneDrivu.** OneDrive synchronizuje i vnitřek `.git`,
takže se zámky a index dají zasynchronizovat uprostřed operace. A soubory
„na vyžádání" se tváří jako přítomné, i když na disku nejsou — na to se
při přípravě vrdlovec.cz narazilo, když šla fotka přečíst až napodruhé.
Zálohu a synchronizaci repozitáře dělá **GitHub**, ne OneDrive.

**Z toho plyne jedno pravidlo:** co není pushnuté, to zálohované není.
Necommitnuté změny a neodeslané commity žijí jen na tomhle disku.

**Pro Claude Code:** kořenový adresář je nastavený do OneDrivu, aby tam
vznikaly pracovní soubory. Repozitář je tedy **mimo něj** — když se má sahat
na kód, je potřeba si říct o přístup k `C:\Users\Public\Documents\Repository\`.
Pracovní a rozpracované soubory patří dál do OneDrivu, ne do repozitáře.
