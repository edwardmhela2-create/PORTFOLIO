# FILE 2 — Maombi ya PSRS/PPRA (CV + Barua)

Sprint 5 ya BACKLOG. Lengo: **kuwa tayari kwa round inayofuata** ya
tangazo la PSRS kwa niaba ya PPRA (round ya Ref. Na. JA.9/16/01/54
— mwisho 14 Sep 2026 — **imeisha**; hii faili ni maandalizi ya
round ijayo).

## Fanya nini hapa
| Faili | Hadhi |
|---|---|
| `CV.html` → `CV.pdf` | ✅ kiolesura cha kurasa 2 (English) — **hakuna taarifa binafsi** |
| `BARUA_MAOMBI.html` → `BARUA_MAOMBI.pdf` | ✅ barua ya Kiswahili, mtindo wa PSRS |
| `IMETIMLIWA/` (gitignored) | ⬜ hapa utaweka PDF zilizojazwa — **hazipendi GitHub** |

## Mahitaji ya PSRS (kwa mujibu wa *General Application Reminders*)
1. Barua **imesainiwa**, Kiswahili au Kiingereza, na kuandikwa kwa:
   **The Secretary, PSRS, P.O. Box 2320, Mahakama Street,
   Tambukareli, Dodoma.**
2. Ambatisha **vyeti vilivyothibitishwa (certified)** na **transcripts**
   — *result slips na testimonials HAZIKUBALIWI*.
3. **Picha ya pasipoti** (ya karibuni) + **wadhamini watatu** wenye
   mawasiliano sahihi.
4. Tuma **kupitia http://portal.ajira.go.tz TU** — njia zingine
   hazipokelewi.
5. Ujumbe wa mwongozo (line ya passport): *"Package everything as a
   portfolio project on GitHub ... draft your application letter
   referencing specific pieces of the project"* — hiki ndicho
   tunachofanya (repo + P13).

## Jinsi ya kujaza + kutengeneza PDF
1. Fungua `CV.html` / `BARUA_MAOMBI.html` → badilisha kila `[NAMBARI
   HII]` kwa taarifa zako (neno la kupata: `[` — nitaona `[JINA]`).
2. Fungua folda hii kwenye terminal na endesha:
   ```powershell
   $edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
   foreach ($f in @("CV","BARUA_MAOMBI")) {
     $h = (Resolve-Path "$f.html").Path -replace "\\","/"
     & $edge --headless --disable-gpu --user-data-dir="$env:TEMP\edgepdf" `
             --no-pdf-header-footer --print-to-pdf="$PWD\$f.pdf" "file:///$h"
   }
   ```
3. Nakala PDF zilizojazwa → folda `IMETIMLIWA\` (haiendi Git).

## Orodha ya kukagua kabla ya kutuma
- [ ] Jina, simu, barua pepe, mji yamejazwa
- [ ] Elimu (chuoni/kozi) imewekwa + vyeti **vyenye uthibitisho**
- [ ] Wadhamini 3 wamekubali (jina, cheo, simu)
- [ ] Picha ya pasipoti ya karibuni
- [ ] PDF imesainiwa (barua) — tarehe sahihi, tangazo jipya Ref. Na.
- [ ] CV ina kiungo cha GitHub + mradi wa **Mjibu (RAG)** umeelezewa
- [ ] Imepakiwa **portal.ajira.go.tz TU**; nakala za vyeti ziko
- [ ] (Hakikisha ujuzi: `git log` ni safi; PDF za Git zipo)

## Bahati nasibu njema 🍀
Tangazo linalofuata likitoka, CV + barua zako zitakuwa **zimejaa
tayari** — jaza tu tarehe/ref. na tuma.
