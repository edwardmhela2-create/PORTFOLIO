# P13 — Mjibu: Maswali kwa Nyaraka (RAG)

Mradi wa **AI wa PPRA**: uliza swali lolote kuhusu PDF/TXT/MD uliyopakia,
jibu linakuja na **vyanzo** — ukiendeshwa **ndani ya kompyuta yako**
(Ollama), bila kutuma data kwenye wingu. **Imeimarishwa** (Okt 2026):
**Chroma vector DB** + **embeddings** + **backend mbadala**
(Ollama ⇄ API ya wingu) — sawa na *Portfolio Project Idea* ya tangazo
la PSRS.

**Stack:** FastAPI + **Chroma** (vector DB, cosine) + embeddings
(hashing/Ollama) + LLM **mbadala** (Ollama `llama3.2:1b` au OpenAI-style
kwa `.env`) + UI ya mazungumzo.

## Thamani ya biashara
Kampuni/taasisi (k.m. PPRA) zina nyaraka nyingi (taratibu, kanuni,
ripoti). Mfumo kama huu: **sekunde chache** badala ya kusoma saa 3;
na kwa kuwa Ollama ni **local**, taarifa za siri **haziendi nje**.

## Nadharia kwa mifano halisi
| Nadharia | Mfano wa maisha |
|---|---|
| **RAG** (Retrieve + Generate) | Mwalimu anapewa **kitabu** kabla ya kujibu — jibu lake linatoka kwenye kitabu, si kumbukumbu tu |
| **Chunking** (vipande) | Kitabu kisomekwe kwa kurasa, si mara moja — LLM hawezi kukariri kitu kirefu |
| **TF-IDF + cosine** | Ulinganifu wa maneno "muhimu" (nadra = thamani zaidi) — jina "firewall" linazidi "la" |
| **Embeddings** (sasa: hashing 512; Ollama-neural: `.env`) | Badala ya maneno la jadi — maana. `MJIBU_EMBED=ollama` ukawa na Ollama ya kisasa (`/api/embed`), Auto → hashing (offline) bila kushindwa |
| **Citations [1], [2]** | Ripoti ya mwanasayansi: kila dai lina chanzo — jibu lisilo na chanzo = habari ya kupewa |
| **Hallucination** | LLM anaweza "kubuni" — kanuni ya "Sijui" + temperature 0.1 hupunguza |
| **Prompt injection** | Mtu anaweza kupakia nyaraka: "ignore instructions..." — README inaeleza kinga |
| **Interchangeable backend** | Badilisha Ollama → API ya wingu kwa kubadilisha `.env` tu |

## Endesha
```powershell
python -m pip install -r requirements.txt   # mara ya kwanza
ollama serve                                # kama haipo bado (11434)
python -m uvicorn mjibu.app:app --port 8002 # au mjibu.bat
# fungua http://127.0.0.1:8002
```
Nyaraka 2 za mfano (`portfolio.md`, `usalama.md`) zinapakia
**automatiki** start. Badilisha `.env.example` → `.env` kwa mipangilio:

| Kipengele | Jukumu |
|---|---|
| `MJIBU_DB=auto\|chroma\|tfidf` | Hifadhi: **Chroma** (kudumu, cosine) au TF-IDF ya ndani |
| `MJIBU_EMBED=auto\|ollama\|hashing` | Vipimo: Ollama neural (ukawa na mfumo wa kisasa) → hashing 512-d offline |
| `MJIBU_BACKEND=ollama\|openai` | **LLM mbadala**: ndani (bure/siri) au wingu (weka `MJIBU_OPENAI_API_KEY` `.env` tu) |

## Mwendo wa jaribio
1. Kwenye UI: uliza *"Mielelezo ilifikia asilimia ngapi?"* → jibu lenye
   **[1] portfolio.md**.
2. Pakia PDF halisi (taarifa/tarati) → uliza swali lake → angalia
   vyanzo (kwenye `GET /api/nyaraka` unaona vipande vyake).
3. Funga Ollama → uliza tena → ujumbe wa kirafiki (API haivunji);
   badilisha `MJIBU_BACKEND=openai` + ufunguo → jibu linatoka wingu
   (badala ya ndani).
4. Ondoa nyaraka zote → uliza → **"Sijui"** (haijibu kwa kubuni).

## Mitihani
```powershell
python -m pytest -q    # 30 tests (LLM + Ollama embed imemock-iwa)
```
- Chunking (ukubwa/overlap/tupu), **hashing embeddings** (thabiti,
  fallback), **Chroma store** (tafuta/ondoa/hudhurupio/persistence),
  kiunganisho (`auto|chroma|tfidf`), API (pakia/nyaraka/futa/swali +
  validation 400/404/422), prompt (kanuni + vyanzo), LLM **mbadala**
  (Ollama haipo → `None`; OpenAI payload/auth/parse; `maelezo()`),
  `.env` loader.

## Maadili (Ethics)
- **Faragha**: nyaraka huishi kwenye kompyuta yako — lakini PDF za
  watumiaji haziwezi kubaki milele; ondoa baada ya kazi (endpoint ya
  `DELETE /api/nyaraka`).
- **Prompt injection**: nyaraka mpya inaweza kujaribu kuamuru LLM
  "sahau kanuni" — kinga: system prompt imara + kuaachia LLM
  kutumia TU muktadha; production: ongeza input sanitization +
  moderation.
- **Hallucination**: hata na citations, jibu la LLM si ukweli wa
  mwisho — binadamu huthibitisha (somo la P9 likirudiwa).
- `.env` haingii Git; hakuna API key kwenye repo hii.

## Viwango vya production (Production upgrades)
- ✅ **Imekamilika (Okt 2026):** **Chroma vector DB** (persistent,
  cosine) · **embeddings** (`MJIBU_EMBED`; auto → hashing 512-d) ·
  **LLM mbadala** (`MJIBU_BACKEND=openai` + `.env` key = jibu la
  wingu bila kubadilisha code) · `.env` loader bila package za ziada.
- **Embeddings halisi** (Ollama `nomic-embed-text` au
  sentence-transformers) — semantic search kamili; sasa hashing ni
  ya maneno tu (faida: offline, haraka; hasara: "mlango wa usalama"
  bado hailingani na "firewall").
- **Streaming** (SSE) — jibu lionekane herufi kwa herufi (saa ¼ si
  nzuri kwa mtumiaji).
- **LangChain/LlamaIndex** kwa orchestration + multi-hop retrieval.
- Auth + rate limiting + virus scan ya faili zinazopakiwa.
- Docker (`uvicorn` image) + PostgreSQL kwa metadata ya nyaraka.

## Ramani (Roadmap)
- ✅ P10–P12 (Django trilogy)
- ✅ **P13 Mjibu (AI/RAG)** — unakoona hapa (tests 30; Chroma +
  embeddings + backend mbadala)
- ⬜ Sprint 2/2b: vyeti bure (ISC², Kaggle, fCC)
- ⬜ File 2: maombi ya PPRA (CV yenye kiungo cha GitHub hiki)

## Maswali ya kufikiria
1. Kwa nini `tafuta()` inajenga upya (`jenga()`) kila nyaraka
   mpya? Nini kitatokea na nyaraka 10,000 (onyo: O(n) — production
   nini?)
2. Jina "firewall" linafanana na "mlango wa usalama"? TF-IDF
   **hapana** — embeddings **ndiyo**: ni tatizo gani kwa mazungumzo
   ya Kiswahili ambayo maneno mengi hayapo kwenye korpusi?
3. LLM alijibu 94.7% — kama angeandika "94.7% kwa data ya
   mafanikio" (si "usahihi"), nani ndio ana hatia: LLM, retriever,
   au mchapishaji wa `portfolio.md`? (Suluhisho letu = citations +
   "Sijui" — kwa nini haitoshi pekee?)
