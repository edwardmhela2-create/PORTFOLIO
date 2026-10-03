# BACKLOG â€” Ngazi ya 4 (Agile board)

Kanuni: kila **user story** ina `Kama..., nataka..., ili...` + **acceptance
criteria** (vipimo vya "imekamilika"). Hakuna kitu kinachoitwa "done" bila
kriteria zote kufikiwa. Sprint = kipindi kilichopangwa; retro = maswali ya
mwisho.

## âœ… Sprint 1 â€” Git + GitHub (IMEKAMILIKA)
**Kama** mtu anayechunguza CV yangu, **nataka** kuona miradi yote kwenye
GitHub, **ili** nithibitishe ujuzi wangu bila kusema tu.
- [x] Repo ya umma imetengenezwa na faili 202 zimepakiwa
- [x] `.gitignore` â€” DB/`__pycache__`/media hazipo, hakuna secrets
- [x] `main` inafuatana `origin/main`
- [x] Ramani imesasishwa (item 7 âœ…)
**Retro:** kwa nini db.sqlite3 haipaswi kuingia Git?

## â¸ï¸ Sprint 2 â€” Vyeti bure mtandaoni â€” IMESITISHWA KWA SASA (2 Okt 2026)
> **Uamuzi wa Edward:** *"tuiruke kwanza, tutairudia."* Mwongozo
> uko tayari kwenye `SPRINT2-VYETI.md` (ratiba 60'/siku Ã— wiki 4) â€”
> ukirudi ni kufuata hatua 1: netacad.com.
**Kama** mwombaji wa PPRA, **nataka** vyeti vya bure vinavyothibitisha
ujuzi, **ili** CV iwe na alama za kimataifa bila gharama.
> **Ukweli (utafiti wa Okt 2026):** ISCÂ² **1MCC imefungwa** kwa
> wajipya (20 Mei 2026) â†’ badala yake: **Cisco NetAcad** (bure +
> badges). Mwongozo kamili + ratiba: `SPRINT2-VYETI.md`.
- [x] Mwongozo wa usajili, ukweli wa vyeti 4, ratiba 60'/siku Ã—
      wiki 4 â€” `SPRINT2-VYETI.md`
- [ ] Cisco NetAcad â€” badge **2**: *Introduction to Modern AI* (6h,
      AI post!) + *Introduction to Cybersecurity* (6h) â€” netacad.com
- [ ] Kaggle micro-courses: *Intro to ML* (3h) + *Pandas* (4h) â€”
      cheti: kaggle.com/learn
- [ ] freeCodeCamp â€” *Data Analysis with Python*
- [ ] Ratiba ya kujisomea: dakika 60/siku Ã— wiki 4
**Acceptance criteria:** alama 3 (badges/certs) + viungo vyao kwenye
README ya PORTFOLIO + CV. **Retro:** je, mtaala uliohitaji ni
"certification" au "ujuzi unaoshindikana kusema bila cheti"?

## âœ… Sprint 3 â€” Agile/Scrum (4.2) (IMEKAMILIKA)
**Kama** kiongozi wa timu, **nataka** kutumia lugha ya Agile, **ili**
nyinyi muweze kufanya kazi pamoja bila mgongano.
- [x] Maelezo: sprint, story, DoD, retro (yamewekwa kwenye mazungumzo)
- [x] Backlog hii imeanzishwa
- [x] Andika sprint review ya P12 (hapa chini)
**Acceptance criteria:** unaweza kueleza "sprint" na "story of Done"
kwa sentensi moja kila moja kwenye interview â€” **Imefikiwa**:
- *Sprint* = kipindi kigupya chenye lengo moja kinachozalisha
  kipengele kinachotumika + kimejaribiwa + kimepushwa.
- *Story of Done* = kiolesura: requirements zimekamilika, mitihani
  inapita, README ipo, ethics zimeelezwa, na `git push` imefanyika.

### Sprint review â€” mradi wa "sprint 1" (P12: Duka la Kwanza)
- **Sprint goal:** e-commerce kamili: bidhaa â†’ kikapu â†’ malipo â†’ oda.
- **Yaliyotolewa:** models (Lebo **M2M**, **Oda + snapshot**
  `OdaBidhaa`, kipengele cha unique), kikapu kwenye kila ukurasa
  (**context processor**), checkout yenye `transaction.atomic` + stoo,
  RBAC (muuzaji/mnunuzi/madmini), templates 10, `anza` command,
  README yenye ethics + production upgrades.
- **Miashara:** mitihani **24/24** âœ“ Â· smoke `/` â†’ 200, `/kikapu/`
  anon â†’ 302 âœ“ Â· `manage.py makosa` â†’ 0 âœ“ Â· **push imefanyika** âœ“.
- **Definition of Done:** zote 5 zimepimwa hapo juu â†’ **DONE**.
- **Retro (gofchi tulizokwama):** `Decimal._state.adding`
  (kiashiria cha ORM); jina la linajukumu likagongana na field
  (`kagua` â†’ `meneja`); PowerShell `Out-File` = UTF-16 â†’ SyntaxError;
  unique constraint ni **sheria ya biashara**, si SQL tu.

## âœ… Sprint 4 â€” P13: Document Q&A (AI/RAG) â€” mradi wa PPRA (IMEKAMILIKA)
**Kama** mwombaji wa nafasi ya AI Applications, **nataka** mradi wa
RAG (Retrieval-Augmented Generation), **ili** nithibitishe ujuzi wa
Ollama + Python + vector search ulioanza P9.
- [x] FastAPI endpoint ya kuuliza maswali kwenye PDF/TXT/MD
- [x] TF-IDF cosine retrieval (backend inayobadilika â€” embeddings
      Chroma/Q..resha baadaye)
- [x] Nyuma: Ollama (halisi, llama3.2:1b) + `.env` kwa mabadiliko
- [x] UI rahisi + README yenye architecture decisions + ethics
      (prompt injection, hallucination, faragha)
- [x] Tests 18 + push kwenye GitHub
- [x] **Uimarishaji (2 Okt 2026):** **Chroma vector DB** + embeddings
      (hashing/Ollama) + **LLM mbadala** (`MJIBU_BACKEND=openai` =
      wingu; `.env` loader) â€” inaolingana na *Portfolio Project Idea*
      ya PSRS; tests â†’ **30**
**Acceptance criteria:** swali kwa PDF â†’ jibu lenye citation
(`[1] portfolio.md`) âœ“; tests 30/30 âœ“; repo ipo âœ“; vector DB +
interchangeable backends âœ“ (PSRS idea).
**Retro:** Ollama alifanya kazi bila intaneti â€” data haikuenda
wingu; mara ya kwanza = 81s (model load) â†’ streaming ndio jibu la
production.

## â¬œ Sprint 5 â€” File 2: Maombi ya PPRA (CV + barua) â€” Hali: kiolesura KIMETENGENEZWA
**Kama** sekretari wa PSRS, **nataka** barua iliyosainiwa na CV sahihi,
**ili** maombi yangu yapatikane.
- [x] CV (English, kurasa 2) yenye viungo vya GitHub + miradi 13 +
      mitihani 146 â€” `FILE2-PPRA/CV.pdf` (kiolesura, placeholders)
- [x] Barua ya maombi (Kiswahili, kurasa 1) mtindo wa PSRS â€”
      `FILE2-PPRA/BARUA_MAOMBI.pdf` (S.L.P. 2320, Tambukareli, Dodoma)
- [ ] Jaza taarifa binafsi (jina/simu/elimu/wadhamini 3) â†’
      `FILE2-PPRA/IMETIMLIWA/` (gitignored) + saini
- [ ] NGOs 3, pasipoti picha, vyeti vilivyothibitishwa (kumbuka:
      *result slips hazikubaliwi*)
- [ ] Jaribio la portal.ajira.go.tz (mwaka unaofuata)
**Acceptance criteria:** barua moja ya kiolesura + CV ya kurasa 2
zipo PDF, zimepakiwa kwenye repo (bila taarifa za faragha) â€”
**ZIMEFIKIWA** âœ“ (PDF 2 zimesajiliwa).
**Retro:** kwa nini CV ya kigeni iwekee "146 tests" badala ya
"kazi ya miaka 3"? (Kwa sababu portfolio ndio uthibitisho wetu â€”
tangazo linasema wazi: *"draft your application letter referencing
specific pieces of the project"*).

## â¸ï¸ Sprint 2b â€” Data / AI / ML certificates (SEHEMU ILIYOONGEZWA)
> **Pia imesitishwa** (2 Okt 2026) â€” inasubiri pamoja na Sprint 2.
**Kwa nini haikuwepo?** Mtaala 4.1 haikuorodhesha vyeti vya data/AI
(CompTIA/CCNA pekee) ingawa 3.3 ilifundisha AI â€” lakini soko (PPRA
*nafasi ya AI Applications*) + P9 zinahitaji. Kama mwombaji wa AI
post, **nataka** vyeti vya data/AI, **ili** ujuzi wa ML uwe na alama
rasmi.
- [ ] **Kaggle micro-courses** (BURE + cheti): https://www.kaggle.com/learn
      â€” "Intro to Machine Learning", "Pandas", "Intro to Deep Learning"
- [ ] **freeCodeCamp Data Analysis with Python** (BURE cheti):
      https://www.freecodecamp.org/learn/data-analysis-with-python/
- [ ] **Hugging Face NLP course** (BURE â€” LLM era):
      https://huggingface.co/learn/nlp-course
- [ ] (Baadaye, kulipwa) Google Data Analytics / TensorFlow Developer
      Certificate / Databricks â€” mara tu VIPAJI vipo
**Acceptance criteria:** vyeti 2 vya bure + viungo kwenye CV.

## â¬œ Epic ya baadaye â€” Vyeti vya kulipwa (hakuna gharama bado)
- [ ] CompTIA A+ â†’ Network+ â†’ Security+ (utafiti wa bure: Professor
      Messer, official objectives) â€” anza tu ukiwa na vipaji
- [ ] (Hiari) Cisco CCNA â€” baada ya Network+
**Acceptance criteria:** ratiba ya kujisomea + alama za kujithibitisha
(zana za bure) kabla ya kununua mtihani.

## Kanuni za mchezo (team agreements)
1. Kila kitu kinachokamilika â†’ `git push` (hakuna "done" bila kushare).
2. Hakuna secrets kwenye Git (`.env` tu).
3. Kila sprint ina retro: maswali 3 ya kufikiria.
4. Mtaala + PPRA ndio "product owner" â€” kila sprint lazima iwe na
   thamani ya soko, si kufurahisha tu.

## SPRINT 6 — Skills za PPRA (mtaala: PPRA ICT Skills Learning Guide)
[**Post 1: Frontend** — kila skill: theory + practical + mradi]

- [x] **Skill #1 Angular** — theory + practical + mradi (3 Okt 2026):
      CLI 21.2.24 ilikuwa vigumu (npm ETIMEDOUT → suluhisho
      `NODE_OPTIONS=--dns-result-order=ipv4first` + retries) ·
      `ng new` P14 · component/signals/@for · serve 200 OK
      (headless Edge DOM) · vitest **4/4** · push
- [ ] Skill #2 TypeScript (interfaces, OOP, reactive)
- [ ] Skill #3 Tailwind + HTML5 + Flexbox/Grid + Angular Material
- [ ] Skill #4 Flutter & Dart (app ya simu)
- [ ] Skill #5 NgRx (state management)
- [ ] Skill #6 Play Console / App Store listing
- [ ] Skill #7 REST + GraphQL/Apollo (backend FastAPI + client)
- [ ] Skill #8 Git + code review workflow
- [ ] Skill #9 Figma (Advantage)
- [ ] Skill #10-19: Post 2 Backend (Java/Spring/...)
- [ ] Skill #20-29: Post 3 AI (tayari 9/10 — LangChain bado)
- [ ] Skill #30-38: Post 4 Systems Analyst
- [ ] Wiki 6 ya roadmap: package + maombi (File 2 isubiri taarifa 4)
