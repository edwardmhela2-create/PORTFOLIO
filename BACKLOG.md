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

## ⏸️ Sprint 2 — Vyeti bure mtandaoni — IMESITISHWA KWA SASA (2 Okt 2026)
> **Uamuzi wa Edward:** *"tuiruke kwanza, tutairudia."* Mwongozo
> uko tayari kwenye `SPRINT2-VYETI.md` (ratiba 60'/siku × wiki 4) —
> ukirudi ni kufuata hatua 1: netacad.com.
**Kama** mwombaji wa PPRA, **nataka** vyeti vya bure vinavyothibitisha
ujuzi, **ili** CV iwe na alama za kimataifa bila gharama.
> **Ukweli (utafiti wa Okt 2026):** ISC² **1MCC imefungwa** kwa
> wajipya (20 Mei 2026) → badala yake: **Cisco NetAcad** (bure +
> badges). Mwongozo kamili + ratiba: `SPRINT2-VYETI.md`.
- [x] Mwongozo wa usajili, ukweli wa vyeti 4, ratiba 60'/siku ×
      wiki 4 — `SPRINT2-VYETI.md`
- [ ] Cisco NetAcad — badge **2**: *Introduction to Modern AI* (6h,
      AI post!) + *Introduction to Cybersecurity* (6h) — netacad.com
- [ ] Kaggle micro-courses: *Intro to ML* (3h) + *Pandas* (4h) —
      cheti: kaggle.com/learn
- [ ] freeCodeCamp — *Data Analysis with Python*
- [ ] Ratiba ya kujisomea: dakika 60/siku × wiki 4
**Acceptance criteria:** alama 3 (badges/certs) + viungo vyao kwenye
README ya PORTFOLIO + CV. **Retro:** je, mtaala uliohitaji ni
"certification" au "ujuzi unaoshindikana kusema bila cheti"?

## ✅ Sprint 3 — Agile/Scrum (4.2) (IMEKAMILIKA)
**Kama** kiongozi wa timu, **nataka** kutumia lugha ya Agile, **ili**
nyinyi muweze kufanya kazi pamoja bila mgongano.
- [x] Maelezo: sprint, story, DoD, retro (yamewekwa kwenye mazungumzo)
- [x] Backlog hii imeanzishwa
- [x] Andika sprint review ya P12 (hapa chini)
**Acceptance criteria:** unaweza kueleza "sprint" na "story of Done"
kwa sentensi moja kila moja kwenye interview — **Imefikiwa**:
- *Sprint* = kipindi kigupya chenye lengo moja kinachozalisha
  kipengele kinachotumika + kimejaribiwa + kimepushwa.
- *Story of Done* = kiolesura: requirements zimekamilika, mitihani
  inapita, README ipo, ethics zimeelezwa, na `git push` imefanyika.

### Sprint review — mradi wa "sprint 1" (P12: Duka la Kwanza)
- **Sprint goal:** e-commerce kamili: bidhaa → kikapu → malipo → oda.
- **Yaliyotolewa:** models (Lebo **M2M**, **Oda + snapshot**
  `OdaBidhaa`, kipengele cha unique), kikapu kwenye kila ukurasa
  (**context processor**), checkout yenye `transaction.atomic` + stoo,
  RBAC (muuzaji/mnunuzi/madmini), templates 10, `anza` command,
  README yenye ethics + production upgrades.
- **Miashara:** mitihani **24/24** ✓ · smoke `/` → 200, `/kikapu/`
  anon → 302 ✓ · `manage.py makosa` → 0 ✓ · **push imefanyika** ✓.
- **Definition of Done:** zote 5 zimepimwa hapo juu → **DONE**.
- **Retro (gofchi tulizokwama):** `Decimal._state.adding`
  (kiashiria cha ORM); jina la linajukumu likagongana na field
  (`kagua` → `meneja`); PowerShell `Out-File` = UTF-16 → SyntaxError;
  unique constraint ni **sheria ya biashara**, si SQL tu.

## ✅ Sprint 4 — P13: Document Q&A (AI/RAG) — mradi wa PPRA (IMEKAMILIKA)
**Kama** mwombaji wa nafasi ya AI Applications, **nataka** mradi wa
RAG (Retrieval-Augmented Generation), **ili** nithibitishe ujuzi wa
Ollama + Python + vector search ulioanza P9.
- [x] FastAPI endpoint ya kuuliza maswali kwenye PDF/TXT/MD
- [x] TF-IDF cosine retrieval (backend inayobadilika — embeddings
      Chroma/Q..resha baadaye)
- [x] Nyuma: Ollama (halisi, llama3.2:1b) + `.env` kwa mabadiliko
- [x] UI rahisi + README yenye architecture decisions + ethics
      (prompt injection, hallucination, faragha)
- [x] Tests 18 + push kwenye GitHub
- [x] **Uimarishaji (2 Okt 2026):** **Chroma vector DB** + embeddings
      (hashing/Ollama) + **LLM mbadala** (`MJIBU_BACKEND=openai` =
      wingu; `.env` loader) — inaolingana na *Portfolio Project Idea*
      ya PSRS; tests → **30**
**Acceptance criteria:** swali kwa PDF → jibu lenye citation
(`[1] portfolio.md`) ✓; tests 30/30 ✓; repo ipo ✓; vector DB +
interchangeable backends ✓ (PSRS idea).
**Retro:** Ollama alifanya kazi bila intaneti — data haikuenda
wingu; mara ya kwanza = 81s (model load) → streaming ndio jibu la
production.

## ⬜ Sprint 5 — File 2: Maombi ya PPRA (CV + barua) — Hali: kiolesura KIMETENGENEZWA
**Kama** sekretari wa PSRS, **nataka** barua iliyosainiwa na CV sahihi,
**ili** maombi yangu yapatikane.
- [x] CV (English, kurasa 2) yenye viungo vya GitHub + miradi 13 +
      mitihani 146 — `FILE2-PPRA/CV.pdf` (kiolesura, placeholders)
- [x] Barua ya maombi (Kiswahili, kurasa 1) mtindo wa PSRS —
      `FILE2-PPRA/BARUA_MAOMBI.pdf` (S.L.P. 2320, Tambukareli, Dodoma)
- [ ] Jaza taarifa binafsi (jina/simu/elimu/wadhamini 3) →
      `FILE2-PPRA/IMETIMLIWA/` (gitignored) + saini
- [ ] NGOs 3, pasipoti picha, vyeti vilivyothibitishwa (kumbuka:
      *result slips hazikubaliwi*)
- [ ] Jaribio la portal.ajira.go.tz (mwaka unaofuata)
**Acceptance criteria:** barua moja ya kiolesura + CV ya kurasa 2
zipo PDF, zimepakiwa kwenye repo (bila taarifa za faragha) —
**ZIMEFIKIWA** ✓ (PDF 2 zimesajiliwa).
**Retro:** kwa nini CV ya kigeni iwekee "146 tests" badala ya
"kazi ya miaka 3"? (Kwa sababu portfolio ndio uthibitisho wetu —
tangazo linasema wazi: *"draft your application letter referencing
specific pieces of the project"*).

## ⏸️ Sprint 2b — Data / AI / ML certificates (SEHEMU ILIYOONGEZWA)
> **Pia imesitishwa** (2 Okt 2026) — inasubiri pamoja na Sprint 2.
**Kwa nini haikuwepo?** Mtaala 4.1 haikuorodhesha vyeti vya data/AI
(CompTIA/CCNA pekee) ingawa 3.3 ilifundisha AI — lakini soko (PPRA
*nafasi ya AI Applications*) + P9 zinahitaji. Kama mwombaji wa AI
post, **nataka** vyeti vya data/AI, **ili** ujuzi wa ML uwe na alama
rasmi.
- [ ] **Kaggle micro-courses** (BURE + cheti): https://www.kaggle.com/learn
      — "Intro to Machine Learning", "Pandas", "Intro to Deep Learning"
- [ ] **freeCodeCamp Data Analysis with Python** (BURE cheti):
      https://www.freecodecamp.org/learn/data-analysis-with-python/
- [ ] **Hugging Face NLP course** (BURE — LLM era):
      https://huggingface.co/learn/nlp-course
- [ ] (Baadaye, kulipwa) Google Data Analytics / TensorFlow Developer
      Certificate / Databricks — mara tu VIPAJI vipo
**Acceptance criteria:** vyeti 2 vya bure + viungo kwenye CV.

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
