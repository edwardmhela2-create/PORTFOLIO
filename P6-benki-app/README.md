# P6 — Benki App v2: Mfumo wa Benki kwenye Web (Flask + Login + Database)

## Maelezo Mafupi (Description)
Programu ya web (kama benki halisi) yenye **uingiaji (login)**, orodha ya
mikopo, kuongeza mteja/mkopo, **jedwali la malipo**, **kurekodi malipo**,
na ripoti — data iko kwenye **SQLite yenye muundo wa P5** (wateja, watumiaji,
mikopo, malipo + **trigger**).

> **Hii inaunganisha:** P3 (hesabu/CLI) + P4 (web) + P5 (database/trigger)
> + 3.2 (Flask) kwenye **mradi mmoja**.

## Kwa nini (Business value)
- **Login + roles** — kila mtumiaji anajua nani yuko (admin/mpokeaji) — 3.1
- **Nenosiri HAIHIFADHIWI wazi** — `werkzeug` inahash + salt (3.1 hashing)
- **Web = upatikanaji** — wateja/wafanyakazi hutumia browser, si terminal
- **Malipo yanarekodiwa** — na trigger ya P5 inakumbuka yenyewe!
- **SQL salama** — kila swali linatumia parameters (SQL injection = 3.1)

## Teknolojia (Tech stack)
| Kipengele | Teknolojia |
|---|---|
| Backend | Python + **Flask** (routes, sessions, templates) |
| Ulinzi wa nenosiri | `werkzeug.security` (PBKDF2 + salt — si hash ya wazi!) |
| DB | SQLite + schema ya P5 (FK, CHECK, TRIGGER) |
| Frontend | HTML/Jinja2 templates + CSS |
| Tests | Flask `test_client` + pytest |

## Jinsi ya kutumia (How to run)
```powershell
cd $env:USERPROFILE\Desktop\DATA\PORTFOLIO\P6-benki-app
python app.py
# browser: http://localhost:5000
```
Au double-click `start.bat`.

**Kuingia (demo — akaunti 3):**
| Jina | Nenosiri | Jukumu | Anacho-ona/fanya |
|---|---|---|---|
| `admin` | `benki123` | admin | Kila kitu (+ futa) |
| `mpokeaji` | `pokea123` | mpokeaji | Orodha + kupokea malipo (haongezi) |
| `mhasibu` | `hesabu123` | mhasibu | Orodha + ripoti (halipi/hafuti) |

> ⚠️ Hizi ni **demo tu** — kazi halisi: kila mtumiaji abadilishe nenosiri
> (bofya **Nenosiri** hapo juu) — hata wewe, badilisha `benki123` mara moja!

## Vipengele (Features)
1. **Login/Logout** — session ya Flask (cookie salama iliyosainiwa)
2. **Orodha ya mikopo** — JOIN + deni halisi (kama view ya P5)
3. **Ongeza** — fomu ya mteja + mkopo (validation: kiasi>0, riba 0-100)
4. **Jedwali** — flat/reducing (kama P3 — hesabu zile zile)
5. **Lipa** — rekodi malipo → **trigger inakumbuka otomatiki**
6. **Ripoti** — GROUP BY: jumla, nani anadai zaidi, takwimu
7. **Badilisha nenosiri** — thibitisha la zamani + hash mpya (+salt)
8. **Ulinzi wa Roles (authorization)** — kila jukumu ana ruhusa yake:
   kila POST inalinda `@linahitaji_jukumu(...)`
9. **CSRF token** — kila fomu ina token ya siri (`hmac.compare_digest`)
10. **Wateja + Futa** — RESTRICT/CASCADE **live** browser:
   futa mteja aliyeko na mikopo → database **ikikataa**
11. **Ulinzi** — `@linahitaji_kuingia` (ukijaribu bila kuingia → unarudishwa
    kwenye ukurasa wa kuingia), SQL parameters (si string concatenation)

## Usalama uliotumika (3.1 + 3.2)
| Hatari | Ulinzi wetu |
|---|---|
| Nenosiri wazi DB | `generate_password_hash` (PBKDF2 + salt) |
| Mtu anaingia bila ruhusa | `@linahitaji_kuingia` + session |
| Mtumiaji anafanya KITU cha juu (authz) | `@linahitaji_jukumu("admin", ...)` |
| SQL injection | Parameters (`?`) — **si kuunganisha string!** |
| Session ya kughushi | `secret_key` + Flask hunyesha cookie iliyosainiwa |
| CSRF (link mbaya imemfunga) | Token kwenye fomu + `hmac.compare_digest` |
> Bado HAIKO (production): **HTTPS** (TLS), rate-limit ya kuingia (3.1),
> nenosiri thabiti (bcrypt/argon2), session timeout.
> (CSRF: tumetengeneza **sisi wenyewe** bila package — kwa kujifunza;
> production hutumia Flask-WTF yenye ulinzi kamili.)

## Malengo ya kiwango cha juu (Production upgrades)
1. **HTTPS** (TLS) + rate-limit ya kuingia + session timeout (3.1)
2. **Roles kamili + UI** — mhasibu apate CSV ya ripoti (P3 hamisha)
3. **PostgreSQL** + server ya kweli (P5 ilieleza tofauti)
4. **PDF ya mkataba** + email alert (deni la karibu kulipwa)
5. **Audit trail kwenye DB** (trigger za UPDATE/DELETE — P5)
6. **Deploy** — Dockerize (P8) + nginx (production hosting)

## Kuhusu mitihani (tests)
```powershell
python -m pytest test_app.py -v
```
**14 tests**: access control, login, **SQL injection**, **CSRF**, roles
(authz), badilisha nenosiri, validation, trigger, **RESTRICT/CASCADE live**.

## Mtandao wa hatua zinazofuata (Roadmap)
- [x] P1 — SysReport
- [x] P2 — NetMapper
- [x] P3 — Mkopo CLI Pro
- [x] P4 — Portfolio website
- [x] P5 — Database design
- [x] P6 — Benki App v2 (hii)
- [ ] P7 — CyberToolkit
