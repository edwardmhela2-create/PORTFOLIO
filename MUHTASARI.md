# MUHTASARI WA NOTES — Toka Mwanzo hadi Leo
(Notes za kujirekebisha haraka — kila kitu tulichojifunza Ngazi 1 → Git)

## 1. Mazingira ya mashine (marudio ya kazi)
- **Python 3.14.6** (pip HAIPO kwenye PATH → daima `python -m pip ...`), pytest 9.1.1, Django 6.0.7, sklearn 1.8.0, pandas 3.0.0
- **PowerShell 5.1**: `Out-File`/`Add-Content` = UTF-16 (null bytes) → SyntaxError; tumia Write tool/UTF-8. Pipi za objects si text. `;` = kupanga mfululizo, si `&&`.
- Mtandao: 25–50% packet loss → **jaribu tena**; kwanza offline.
- Tkinter: **Tk MOJA tu** kwa moduli + retry loop (TclError ya combobox).
- Ollama `llama3.2:1b` imewekwa (matumizi ya ndani/ML).

## 2. Ngazi ya 1 — Msingi (P1–P2)
- **CLI/PowerShell**: cmdlets, pipeline, objects; ripoti za OS kwa `Get-CimInstance`; **Task Scheduler** kwa kazi za kiotomatiki → **P1 SysReport** (HTML report).
- **Mitandao**: IP, port, ARP; `socket` + `ThreadPool`; kugundua milango wazi → **P2 NetMapper** (riposti HTML, `.bat`).
- **Ethics**: port scan ni ya **mifumo yako tu**.

## 3. Ngazi ya 2 — Programu (P3–P6)
- **Python**: argparse (CLI), CRUD, SQLite3 (`?paramstyle` — si f-string!), `Decimal` kwa pesa si `float`, try/except, pytest → **P3 Mkopo CLI** (riba/simple vs declining, CSV logs, tests 18).
- **Web**: HTML/CSS/JS, responsive, kichujio cha miradi bila framework → **P4 Portfolio** (tovuti hii).
- **SQL**: ERD, normalization (1NF–3NF), constraints (PK/FK/UNIQUE/NOT NULL), **VIEW, TRIGGER**, CASCADE/SET NULL/RESTRICT → **P5 Database Design** (`schema.sql`, `queries.sql`, `fanya.py`).
- **Flask**: sessions, login, `generate_password_hash` (PBKDF2), `@login_required`, majukumu (authz), CSRF token kwa kila POST, errors 404/403/500 → **P6 Benki App** (tests 14).
- **Ethics**: nenosiri halisiwi (hash si reverse-able); faragha ya data.

## 4. Ngazi ya 3 — Usalama, Cloud, AI (P7–P9)
- **Cyber**: SHA-256/512 (hash), **HMAC** (integrity), password salama, hardening checklist, port scan → **P7 CyberToolkit** (zana 8 + GUI, tests 15).
- **Docker**: Dockerfile, `.dockerignore` (build context ndogo), **volumes** (data haiharibiki), healthcheck, `docker compose up` → **P8 Docker/Compose** (P6 ndani ya container, tests 6).
- **AI/ML (P9 Mielelezo)**: pandas (74 samples sw/en), **train/test split 25%** (kuzuia overfitting), **stratify**, seed=42, **TF-IDF (ngram 1–2) + MultinomialNB**, accuracy **94.7%**, confusion matrix → precision/recall, **false positive** = Type I (OTP halisi = SPAM → hasara ya kuaminika), pickle `model.pkl`, GUI = threads → tests 12.
- **Ethics**: model si hukumu ya mwisho; NLP ni **lugha maalum** (Kiingereza haitambui Kifaransa).

## 5. Miradi makubwa 3 — Django (P10–P12) = **tests 63**
- **P10 Benki 360 (19)**: settings/ALLOWED_HOSTS, INSTALLED_APPS, ORM + migrations, **Groups + decorator ya jukumu**, CSRF kiotomatiki, CASCADE, messages, **admin ya Kiswahili** (`LANGUAGE_CODE='sw'`), `transaction.atomic`, forms, pytest-django, `anza` command.
  - *Gocha*: `if not self.salio` hu-compute upya kwa 0 → tumia `self._state.adding`.
- **P11 Ofisi 360 (20)**: **CBV** (List/Detail/Create + `paginate_by`), **state machine** kwenye model (`wasilisha()`/`kagua()`), **signals** (`post_save` → audit trail), FileField upload (`media/`, `upload_to`), CSV + BOM, mixin ya ruhusa, CBV `get_queryset` = faragha.
  - *Gocha*: **jina moja = field/method collision** (`kagua` FK + `kagua()` → safu haikubuniwa!); suluhisho: field `meneja`.
- **P12 Duka la Kwanza (24)**: **M2M** (lebo), **context processor** (badge ya kikapu kila ukurasa), **unique constraint** kwa cart, checkout **`transaction.atomic` + `refresh_from_db` + `F()`**, **snapshot** (bei/jina huhifadhiwa; bidhaa ikifutwa → `SET_NULL` bila kupoteza oda), **UpdateView/DeleteView**, 404-vs-403 (mali ya mwingine = 404, usionyeshe ipo).
  - *Gocha*: field/method bug ya P11 ilitokana na kupuuza — somo: soma Django errors mapema.

## 5b. P13 Mjibu (AI/RAG) — tests 18
- **RAG** = Retrieve + Generate: TF-IDF cosine (sklearn) →
  muktadha → **Ollama (llama3.2:1b, local)** → jibu + citations [1].
- FastAPI (UploadFile, pydantic validation 400/422/404), chunking
  (ukubwa 600/hatua 500 = overlap), system prompt imara
  ("Sijui" + jibu kwa lugha ya swali + tu muktadha).
- LLM client hurejesha `None` mtandao ukiwa chini → ujumbe wa
  kirafiki (tests hazimhitaji Ollama — mock).
- *Gochi*: `for` iliyopotewa; uvicorn = `--log-level` si
  `--loglevel`; FastAPI inahitaji `python-multipart`; `ondoa()`
  ilikuwa inaweka dict badala ya index (shadowing).

## 6. Git + GitHub + Agile (Ngazi ya 4 yaliyoanza)
- `git init -b main` → `.gitignore` (**DB/media/`__pycache__` HAZIINGII**; `sms.csv` = source data NAINGIA) → `add` → `commit` → `remote add` → `push -u origin main` → **credential (GCM) huhifadhiwa** (push za baadaye = `git push` tu).
- Repo: **github.com/edwardmhela2-create/PORTFOLIO** (Public, faili 202, 125 tests + backlog).
- **Snapshot** si Save: historia ya kila faili + maelezo + mwenzako; `push` ukiwa nyuma → **non-fast-forward** → `git pull` kwanza.
- **Agile**: Product Owner (thamani), backlog (`BACKLOG.md`), sprint (kipindi kifupi), user story ("Kama..., nataka..., ili..."), acceptance criteria (= tests), **Definition of Done** (tests + README + check + push — si test pekee), retro (maswali 3).

## 7. Kanuni tulizozijenga (team agreements)
1. Kila kitu kikikamilika → `git push`.
2. Hakuna secrets kwenye Git (`.env` tu; funguo = `P0-vyanzo/funguo.key` sio kwenye repo).
3. UI = **Kiswahili**, code identifiers = Kiingereza/mchanganyiko; kila mradi na README + pytest.
4. Ethics kila mradi: hashing, faragha, malipo ni mfano, model si hukumu.
5. Jibu la "soko": **PPRA inahitaji ujuzi + portfolio**, vyeti ni thawabu (sprint 2).

## 8. Nambari za kumbuka
| Kipimo | Idadi |
|---|---|
| P3+P5+P6+P7+P8+P9 | 18+14+15+6+9... (jumla ya zamani 62→62) |
| P10 + P11 + P12 + P13 | 19 + 20 + 24 + 18 |
| **JUMLA MITIHANI** | **146 tests** (18+14+15+6+12+19+20+24+18) |
| Miradi | **13/13** + BACKLOG + site P4 |
