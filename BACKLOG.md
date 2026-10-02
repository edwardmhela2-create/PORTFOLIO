# BACKLOG — Ngazi ya 4 (Agile board)

Kanuni: kila **user story** ina `Kama..., nataka..., ili...` + **acceptance
criteria** (vipimo vya "imekamilika"). Hakuna kitu kinachoitwa "done" bila
kriteria zote kufikiwa. Sprint = kipindi kilichopangwa; retro = maswali ya
mwisho.

## ✅ Sprint 1 — Git + GitHub (IMEKAMILIKA)
**Kama** mtu anayechunguza CV yangu, **nataka** kuona miradi yote kwenye
GitHub, **ili** nithibitishe ujuzi wangu bila kusema tu.
- [x] Repo ya umma imetengenezwa na faili 202 zimepakiwa
- [x] `.gitignore` — DB/`__pycache__`/media hazipo, hakuna secrets
- [x] `main` inafuatana `origin/main`
- [x] Ramani imesasishwa (item 7 ✅)
**Retro:** kwa nini db.sqlite3 haipaswi kuingia Git?

## ⬜ Sprint 2 — Vyeti bure mtandaoni
**Kama** mwombaji wa PPRA, **nataka** vyeti vya bure vinavyothibitisha
ujuzi, **ili** CV iwe na alama za kimataifa bila gharama.
- [ ] ISC² Certified in Cybersecurity (CC) — mtihani BURE: jisajili,
      soma kozi, panga mtihani (angalau: akaunti + ratiba)
- [ ] Cisco Skills for All — badge ya kwanza
      ("Introduction to Cybersecurity" au "Networking Basics")
- [ ] freeCodeCamp — cheti kimoja (Python Scientific Computing au
      Responsive Web Design)
- [ ] Ratiba ya kujisomea: dakika 60/siku × wiki 4
**Acceptance criteria:** alama 3 (badges/certs) + viungo vyao kwenye
README ya PORTFOLIO. **Retro:** je, mtaala uliohitaji ni "certification"
au "ujuzi unaoshindikana kusema bila cheti"?

## ⬜ Sprint 3 — Agile/Scrum (4.2)
**Kama** kiongozi wa timu, **nataka** kutumia lugha ya Agile, **ili**
nyinyi muweze kufanya kazi pamoja bila mgongano.
- [x] Maelezo: sprint, story, DoD, retro (yamewekwa kwenye mazungumzo)
- [x] Backlog hii imeanzishwa
- [ ] Andika sprint 1 ya P12 ilivyofanya kazi (sprint review ya
      miashara: alama 24/24, smoke 200/302)
**Acceptance criteria:** unaweza kueleza "sprint" na "story of Done"
kwa sentensi moja kila moja kwenye interview.

## ⬜ Sprint 4 — P13: Document Q&A (AI/RAG) — mradi wa PPRA
**Kama** mwombaji wa nafasi ya AI Applications, **nataka** mradi wa
RAG (Retrieval-Augmented Generation), **ili** nithibitishe ujuzi wa
Ollama + Python + vector search ulioanza P9.
- [ ] FastAPI endpoint ya kuuliza maswali kwenye PDF
- [ ] Embeddings + vector DB (Chroma) nje ya mtandao
- [ ] Nyuma: Ollama (halisi) **au** API ya wingu (linganisha)
- [ ] UI rahisi + README yenye architecture decisions
- [ ] Tests + push kwenye GitHub
**Acceptance criteria:** swali kwa PDF → jibu lenye citation; tests
zinaenda; repo ipo. **Retro:** Ollama alifanya kazi vipi bila intaneti?

## ⬜ Sprint 5 — File 2: Maombi ya PPRA (CV + barua)
**Kama** sekretari wa PSRS, **nataka** barua iliyosainiwa na CV sahihi,
**ili** maombi yangu yapatikane.
- [ ] CV (English) yenye viungo vya GitHub + miradi 12 + mitihani 125
- [ ] Barua ya maombi (Kiswahili au Kiingereza) — mtindo wa PPRA
      (sekretari, S.L.P. 2320, Dodoma)
- [ ] NGOs 3, pasipoti picha, vyeti vilivyothibitishwa (kumbuka:
      *result slips hazikubaliwi*)
- [ ] Jaribio la portal.ajira.go.tz (mwaka unaofuata)
**Acceptance criteria:** barua moja ya kiolesura + CV ya kurasa 2
zipo PDF, zimepakiwa kwenye repo (bila taarifa za faragha).

## ⬜ Epic ya baadaye — Vyeti vya kulipwa (hakuna gharama bado)
- [ ] CompTIA A+ → Network+ → Security+ (utafiti wa bure: Professor
      Messer, official objectives) — anza tu ukiwa na vipaji
- [ ] (Hiari) Cisco CCNA — baada ya Network+
**Acceptance criteria:** ratiba ya kujisomea + alama za kujithibitisha
(zana za bure) kabla ya kununua mtihani.

## Kanuni za mchezo (team agreements)
1. Kila kitu kinachokamilika → `git push` (hakuna "done" bila kushare).
2. Hakuna secrets kwenye Git (`.env` tu).
3. Kila sprint ina retro: maswali 3 ya kufikiria.
4. Mtaala + PPRA ndio "product owner" — kila sprint lazima iwe na
   thamani ya soko, si kufurahisha tu.
