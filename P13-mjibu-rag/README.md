# P13 — Mjibu: Maswali kwa Nyaraka (RAG)

Mradi wa **AI wa PPRA**: uliza swali lolote kuhusu PDF/TXT/MD uliyopakia,
jibu linakuja na **vyanzo** — ukiendeshwa **ndani ya kompyuta yako**
(Ollama), bila kutuma data kwenye wingu.

**Stack:** FastAPI + scikit-learn (TF-IDF cosine retrieval) +
Ollama `llama3.2:1b` + UI ya mazungumzo.

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
| **Embeddings** (uwezo wa baadaye) | Badala ya maneno — maana (meaning); "mlango wa usalama" ≈ "firewall" bila neno moja |
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
**automatiki** start. Badilisha `.env.example` → `.env` kwa mipangilio
(`MJIBU_MODEL`, `MJIBU_K`, n.k.).

## Mwendo wa jaribio
1. Kwenye UI: uliza *"Mielelezo ilifikia asilimia ngapi?"* → jibu lenye
   **[1] portfolio.md**.
2. Pakia PDF halisi (taarifa/tarati) → uliza swali lake → angalia
   vyanzo.
3. Funga Ollama → uliza tena → ujumbe wa kirafiki "LLM haipatikani"
   (API haivunji).
4. Ondoa nyaraka zote → uliza → **"Sijui"** (haijibu kwa kubuni).

## Mitihani
```powershell
python -m pytest -q    # 18 tests (LLM imemock-iwa - inaenda offline)
```
- Chunking (ukubwa/overlap/tupu), hifadhi ya vekta (tafuta/ondoa),
  API (pakia/nyaraka/futa/swali + validation 400/404/422),
  prompt (kanuni + vyanzo), LLM client (haipo → `None`), auto-load.

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
- **Embeddings halisi** + vector DB (**Chroma/Qdrant**) —
  semantic search (sasa: TF-IDF, inafanya kazi bila mtandao).
- **Streaming** (SSE) — jibu lionekane herufi kwa herufi (81s si
  nzuri kwa mtumiaji!).
- **LangChain/LlamaIndex** kwa orchestration + multi-hop retrieval.
- Auth + rate limiting + virus scan ya faili zinazopakiwa.
- Docker (`uvicorn` image) + PostgreSQL kwa metadata ya nyaraka.
- Backend ya pili: API ya Anthropic/OpenAI (mfano: `.env` mbadala).

## Ramani (Roadmap)
- ✅ P10–P12 (Django trilogy)
- ✅ **P13 Mjibu (AI/RAG)** — unakoona hapa (tests 18)
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
