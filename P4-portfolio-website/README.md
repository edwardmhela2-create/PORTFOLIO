# P4 — Portfolio Website: Tovuti ya Kuonyesha Miradi Yako

## Maelezo Mafupi (Description)
Tovuti ya static (bila server ya nje) inayoonyesha **ujuzi, miradi P1–P9,
na ramani ya masomo** — mradi huu ni **kitovu (hub) cha portfolio yote**:
kila mradi wa baadaye utaongezwa hapa kwa kuongeza kadi moja kwenye `script.js`.

## Kwa nini (Business value)
- **Kiwango cha kitaalamu** — watu wa ajira (HR) wanataka **link moja**
  kuona kazi zako (si folda za kompyuta)
- **Uzoefu wa web** — HTML/CSS/JS halisi: responsive, DOM, events, data-driven
- **Kuonyesha maendeleo** — ramani inaonyesha mlango uliopo (ujifunzi/uendeleaji)
- **Msingi wa GitHub Pages** — tovuti hii inaweza kupakiwa mtandaoni bila gharama

## Teknolojia (Tech stack)
| Kipengele | Teknolojia |
|---|---|
| Muundo | HTML5 (semantic), CSS Grid/Flexbox |
| Rangi/Muundo | CSS variables, media query (simu) |
| Uhuishaji | JavaScript (DOM, arrays, events, `filter`) |
| Nje | Hakuna library — kila kitu cha mkono |

## Jinsi ya kutumia (How to run)
**Njia 1 (rahisi):** bonyeza mara mbili `index.html`
(viungo vya miradi vinafanya kazi pia kwenye file://)

**Njia 2 (kama server halisi — unajifunza 3.2):**
```powershell
cd $env:USERPROFILE\Desktop\DATA\PORTFOLIO
python -m http.server 8000
# kisha browser: http://localhost:8000/P4-portfolio-website/
```
> Server lazima izinduliwe kwenye **folda ya PORTFOLIO** (si ndani) ili
> kadi ziweze kufungua miradi mingine (P1 report.html, P2 netmap.html, n.k.).
Au bonyeza mara mbili `start_server.bat`.

## Vipengele (Features)
1. **Menyu ya juu** inayoruka kwa laini (smooth scroll) kwenye sehemu zote
2. **Miradi 9** inayotengenezwa na **JavaScript** kutoka orodha ya data
   (huongeza kadi mpya = kuongeza kadi MOJA kwenye `miradi` array)
3. **Bonyeza kadi → dirisha (modal)** linafunguka: maelezo, jinsi ya
   kuendesha, na **kiungo cha kufungua** mradi (P1 ripoti, P2 dashboard, P3 folda)
4. **Vichujio** — Zote / Zimekamilika / Zinakuja (button + click event)
5. **Responsive** — inafanya kazi kwenye simu (media query)
6. **Ramani** — checklist ya masomo yaliyokamilika na yayoambayo
7. **Mwaka wa sasa** kwa JavaScript (`new Date().getFullYear()`)

## Nini cha kubadilisha (jifunze kwa kugusa!)
1. `index.html` → sehemu ya **hero**: weka **jina lako halisi**, maelezo, mawasiliano
2. `style.css` → `:root` → badilisha `--accent` (rangi ya kwanza) — tovuti
   yote itabadilika (nguvu ya CSS variables!)
3. `script.js` → ongeza kadi mpya kwa mradi wa baadaye:
   ```js
   { id: "P10", jina: "Jina", hali: "coming", maelezo: "...", tekh: ["..."] },
   ```

## Malengo ya kiwango cha juu (Production upgrades)
1. **GitHub Pages** — kupakia mtandaoni (bila gharama) — hatua ya 2 baada ya
   kuwa na GitHub account (ramani yetu!)
2. **Kuunganisha kila mradi** kwenye GitHub repo (link ya kila kadi)
3. **Dark mode** (jua CSS + JS toggle) + animation (CSS `@keyframes`)
4. **Fomu ya mawasiliano** (kwa Flask backend — P6)
5. **Analytics** (jinsi gani ya trafiki — Google Analytics/plausible)

## Mtandao wa hatua zinazofuata (Roadmap)
- [x] P1 — SysReport
- [x] P2 — NetMapper
- [x] P3 — Mkopo CLI Pro
- [x] P4 — Portfolio website (kitovu cha project zote)
- [ ] P5 — Database design
