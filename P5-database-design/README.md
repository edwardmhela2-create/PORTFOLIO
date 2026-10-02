# P5 — Database Design: Mfumo wa Mikopo na Usajili (ERD + SQL)

## Maelezo Mafupi (Description)
Muundo halisi wa database (schema design) kwa mfumo wa mikopo:
**tables 4** (wateja, watumiaji, mikopo, malipo), **view 1** (deni halisi),
**index 2**, pamoja na **ERD** (ramani ya uhusiano) na **maswali 8** ya SQL
yaliyoendeshwa kwa ukweli (SQLite).

## Kwa nini (Business value)
- **Muundo mzuri = mfumo mzima** — kabla ya kuandika programu, mtaalamu
  hupanga **data ipite wapi** (kama mhandisi anayechora ramani ya nyumba)
- **Ulinzi wa data** — CHECK/UNIQUE/FOREIGN KEY: database yenyewe inakataa
  data mbovu (hata kama programu imekosa)
- **Uhusiano (relationships)** — kila mkopo unajua mteja na nani aliuingiza
- **Maswali (queries)** — ripoti zote (deni, ranking, wastani) zinatoka hapa

## Kanuni (How it works)
### Muundo wa uhusiano (ERD)
```
watumiaji 1──<N mikopo >──1 wateja
     (aliyeandika_id)  (mteja_id)     mikopo 1──<N malipo
```
- **PK** = kitambulisho (id) · **FK** = uhusiano kati ya tables
- **ON DELETE RESTRICT** = hauwezi kufuta mteja aliyeko na mikopo
- **ON DELETE CASCADE** = malipo yanafutwa pamoja na mkopo wake
- **VIEW deni_halisi** = asilia − malipo (LEFT JOIN + GROUP BY)
- **TRIGGER** = database **yenyewe** inafanya kazi: kila malipo linaingia →
  `kumbukumbu_za_malipo` inajaa otomatikini (sawa na logs ya P3, lakini
  **bila programu!** — DB ndiyo inafanya)
- **Backup**: `python fanya.py --backup` → `nakala-YYYYMMDD-HHMMSS.db`
  (kazi #1 ya DBA: data kupotea = kufungwa!)

### Ulinzi (constraints) unaofanya kazi:
| Ulinzi | Anazuia nini |
|---|---|
| `CHECK (kiasi > 0)` | kiasi hasi (kama ulijaribu -5 → IMEKATAA) |
| `CHECK (riba 0..100)` | riba ya kipumbavu (mf. 150%) |
| `CHECK (aina IN ...)` | aina isiyojulikana |
| `CHECK (jukumu IN ...)` | jukumu halisi (admin/mpokeaji/mhasibu) |
| `UNIQUE (simu)` | simu mbili za mtu mmoja |
| `UNIQUE (jina_la_mtumiaji)` | mtumiaji mbili wa jina moja |
| `FOREIGN KEY` | mkopo wa mteja asiyekuwepo |

## Teknolojia (Tech stack)
| Kipengele | Teknolojia |
|---|---|
| Schema/data/queries | SQL (SQLite-compatible + maoni ya PostgreSQL) |
| Uendeshaji | Python + `sqlite3` (stdlib — hakuna kusakinisha) |
| ERD | HTML/CSS (bila tools ya nje) |
| Kutafuta | `fanya.py` (huendesha yote na kuonyesha matokeo) |

## Jinsi ya kutumia (How to run)
```powershell
cd $env:USERPROFILE\Desktop\DATA\PORTFOLIO\P5-database-design
python fanya.py               # inatengeneza mfumo.db + kuendesha maswali 10
python fanya.py --backup      # nakala ya database (backup)
```
Kisha: fungua **`erd.html`** (double-click) kuona ramani.

Matokeo ya `fanya.py`:
1. Hesabu ya tables + idadi ya data
2. Maswali 10 (JOIN, GROUP BY, HAVING, subquery, view, LEFT JOIN, AVG)
3. **Jaribio la ulinzi 5**: kiasi hasi, aina mbovu, simu maradufu, FK
   asiyekuwepo, jukumu mbovu → database **IMEKATAA zote**
4. **Trigger**: kumbukumbu za malipo 6 zimeandikwa na **database yenyewe**
   (bila Python!)

## Maswali 10 (queries.sql)
1. Mikopo + wateja + waliyeandika (JOIN ya vitatu)
2. Kilicholipwa vs kilichobaki (LEFT JOIN + GROUP BY)
3. Deni kwa mteja (GROUP BY + ORDER)
4. Nani anadai zaidi (subquery/LIMIT)
5. View: deni halisi
6. Malipo kwa njia (m-pesa/benki/fedha)
7. Wateja wasio na mikopo (IS NULL)
8. Wastani kwa aina (AVG + GROUP BY)
9. Wateja wenye jumla > 500,000 (HAVING)
10. Malipo makubwa kuliko wastani (subquery ndani ya WHERE)

## Normalization (kwa nini tables hizi?)
- **1NF** — hakuna orodha ndani ya seli (kila kitu ni sehemu moja)
- **2NF** — kila kitu kinategemea PK pekee (si sehemu ya PK)
- **3NF** — hakuna "dua" za siri: simu ya mteja **haipo** kwenye `mikopo`
  (ingekuwa hapo, ungelazimika kuisahihisha kila mara! — kwa hiyo tunaita
  kutoka `wateja.id`)
> Analogi: kila kitu kwenye **sehemu yake** — kama faili za ofisini:
> kadi ya mteja ni MOJA, mkopo ni PAMOKE, malipo ni PAMOKE — unaunganisha
> kwa **namba**, si kuandika upya jina kila wakati.

## PostgreSQL vs SQLite (tofauti ya kazi halisi)
| SQLite (hapa) | PostgreSQL (kwa kazi/kampuni) |
|---|---|
| Faili moja (`mfumo.db`) | Server ya kweli (watumiaji wengi) |
| `TEXT/INTEGER/REAL` | `VARCHAR/NUMERIC/BIGINT` |
| `AUTOINCREMENT` | `SERIAL` |
| Mzito: PC 1 | Mzito: server + backup/ulinzi |
> Muundo (ERD, uhusiano, ulinzi) **ni ule ule** — hubadilika ni lugha/SQL ndogo.

## Malengo ya kiwango cha juu (Production upgrades)
1. **PostgreSQL server** + user roles (read-only kwa mhasibu)
2. **Triggers zaidi** — kumbukumbu za UPDATE/DELETE pia (nani alibadilisha nini)
   — **imeanza**: trigger ya INSERT kwenye `malipo`
3. **Migrations** (Alembic) — mabadiliko ya schema bila kupoteza data
4. **Backup/restore** (pg_dump) + data encryption (3.1) — **imeanza**:
   `python fanya.py --backup`
5. **Kuongeza**: table ya `aminika` (guarantor) + `adhabu` (late fees)

## Mtandao wa hatua zinazofuata (Roadmap)
- [x] P1 — SysReport
- [x] P2 — NetMapper
- [x] P3 — Mkopo CLI Pro
- [x] P4 — Portfolio website
- [x] P5 — Database design
- [ ] P6 — Benki App v2 (Flask + muundo huu + auth)
