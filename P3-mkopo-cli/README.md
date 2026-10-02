# P3 — Mkopo CLI Pro: Mfumo wa Mikopo (CLI + SQLite + Tests)

## Maelezo Mafupi (Description)
Mkopo CLI Pro ni programu ya terminal (CLI) ya kusimamia mikopo: kuongeza mteja,
kuweka mkopo, kuona jedwali la malipo la kila mwezi, ripoti za muhtasari, na
kufuta — **kwa kuhifadhi data kwenye database ya SQLite** (si memory tu).
Inajumuisha **mitihani (pytest)** inayothibitisha hesabu na validation.

## Kwa nini (Business value)
- **Kumbuka ya kudumu** — kompyuta ikizimwa data inabaki (database vs memory)
- **Uwazi wa hesabu** — jedwali la malipo kwa kila mwezi (mteja anajua analipa nini)
- **Ripoti kwa meneja** — jumla ya mikopo, nani anadai zaidi (SQL GROUP BY)
- **Usahihi** — mitihani inathibitisha hesabu kabla ya kutoa kwa mteja halisi
- **Ulinzi wa data** — kila mkopo unahusishwa na mteja (relationships) — kama database halisi

## Kanuni (How it works)
### Fomula mbili za riba
**1. Flat interest** (mradi wako wa kwanza `mkopo.py` — riba moja tu):
```
riba ya jumla = kiasi x (riba/100) x (miezi/12)
malipo/mwezi  = (kiasi + riba) / miezi
```

**2. Reducing balance** (jinsi CRDB/NMB halisi zinazofanya — default):
```
i  = riba/100/12                    (viwango vya mwezi)
malipo = kiasi x i / (1 - (1+i)^-n) (kila mwezi ni sawa — annuity)
kila mwezi: riba = salio x i;  marejesho = malipo - riba
```
> Mfano: kiasi 1,000,000 / riba 24% / miezi 12 → **reducing hulipa riba ndogo
> zaidi** kwa sababu riba inapimwa kwenye **deni linalobaki**, si kiasi chote.

### Muundo wa data
```
wateja (1) ----< mikopo (n)        (foreign key: mteja_id)
```

## Teknolojia (Tech stack)
| Kipengele | Teknolojia |
|---|---|
| Lugha | Python 3.14 |
| CLI | `argparse` (amri za nje) + menyu ya kubonyeza |
| DB | `sqlite3` (faili moja: `mkopo.db`, JOIN, GROUP BY, FOREIGN KEY) |
| Validation | classes + `ValueError` (`models.py`) |
| Tests | `pytest` |

## Jinsi ya kutumia (How to run)
```powershell
cd $env:USERPROFILE\Desktop\DATA\PORTFOLIO\P3-mkopo-cli
python -m pip install pytest                 # mara moja tu

python main.py wateja                        # orodha ya wateja
python main.py ongeza --jina "Juma" --simu "071..." --kiasi 1000000 --riba 24 --miezi 12
python main.py orodha                        # mikopo yote (JOIN: jina la mteja)
python main.py jadwali 1                     # jedwali la malipo la mkopo id=1
python main.py ripoti                        # muhtasari (GROUP BY)
python main.py hoji                          # maswali ya data (queries)
python main.py badilisha 3 --riba 18         # hariri mkopo (UPDATE)
python main.py badilisha 3 --jina "Jina Mpya" # hariri jina la mteja
python main.py hamisha                       # hamisha orodha -> mikopo.csv (Excel)
python main.py hamisha --jadwali 3           # hamisha jedwali -> jadwali-3.csv
python main.py kumbuka                       # kumbukumbu za amri (logs)
python main.py futa 1                        # kufuta mkopo
python main.py menyu                         # menyu ya kubonyeza (bila kuandika amri)

python -m pytest                             # mitihani yote
mkopo_cli.bat                               # GUI (bonyeza mara mbili)
```
Amri: `--aina flat` au `--aina reducing` (default: reducing).

### Maswali ya data (hoji)
| Swali | SQL inayotumika |
|---|---|
| 1. Nani kakopa zaidi? (ranking) | `GROUP BY + ORDER BY DESC` |
| 2. Jumla kwa aina (flat vs reducing) | `GROUP BY aina` |
| 3. Takwimu (wastani/kubwa/ndogo) | `AVG, MAX, MIN, SUM` |
| 4. Wateja wasio na mikopo | `LEFT JOIN + WHERE IS NULL` |
| 5. Tafuta kwa jina | `LIKE %sehemu%` |
| 6. Mikopo inayokaribia kuisha | `date('now') - tangu <= miezi` |

### Kipengele kingine
- **badilisha** — `UPDATE` (kubadilisha kiasi/riba/miezi/aina/jina/simu)
- **hamisha** — CSV ya Excel (orodha au jedwali)
- **kumbuka** — audit trail kwenye `logs.csv`: nani alifanya nini na lini
  (ongeza/futa/badilisha/hamisha — kama sheria ya usalama 3.1)

## Mitihani (Tests)
```powershell
python -m pytest -v
```
1. Flat: hesabu dhidi ya formula ya mkono
2. Reducing: jumla ya malipo == kiasi + riba; salio linaishia 0
3. Validation: kiasi hasi, miezi 0, riba > 100, jina tupu → `ValueError`
4. DB: ongeza → orodha → futa (mzunguko kamili)
5. JOIN: mkopo unarudisha jina sahihi la mteja
6. Ripoti: jumla ya mikopo == hesabu ya mkono
7. Maswali: ranking, GROUP BY aina, takwimu, LEFT JOIN, LIKE, mikopo inayoisha
8. UPDATE: badilisha (riba/jina/simu + validation), CSV export, logs

## Usalama na kisheria (Ethics)
Data ya wateja ni **siri** (jina, simu) — Sheria ya Ulinzi wa Data ya Tanzania
(Personal Data Protection Act, 2022): kuhifadhi kwa usalama, kutoa kwa
ruhusa, kutoenda kwa wengine. Database hii ni ya **mazoezi tu**.

## Malengo ya kiwango cha juu (Production upgrades)
1. **Authentication** — mtumiaji + roles (admin / mpokeaji)
2. **REST API** (FastAPI) + web frontend (kama P6 Benki App)
3. **PostgreSQL** — watumiaji wengi kwa wakati mmoja (server ya kweli)
4. **Ripoti PDF/Excel** kwa meneja + email alerts (deni la karibu kulipwa)
5. **Riba inayobadilika** (kiwango cha Benki Kuu — CBRT base rate) + penalty/late fees
6. **Logs** — nani alifanya nini na lini (audit trail) — **imeanza**: `logs.csv`
   (ongeza/futa/badilisha/hamisha) — ikubore: kwenye DB + mtumiaji kwa kila amri

## Mtandao wa hatua zinazofuata (Roadmap)
- [x] P1 — SysReport
- [x] P2 — NetMapper
- [x] P3 — Mkopo CLI Pro
- [ ] P4 — Portfolio website (kitovu cha project zote)
