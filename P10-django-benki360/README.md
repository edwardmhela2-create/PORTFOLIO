# P10 — Benki 360 (Django) — MRADI MKUU #1

## Maelezo Mafupi (Description)
Mfumo kamili wa benki uliojengwa kwa **Django 6** (Python): wateja,
akaunti, kuweka/kutoa fedha, mikopo, ripoti - ukiwa na **usalama wa
Django** (CSRF kiotomatiki, sessions, auth), **majukumu 3**, admin ya
Kiswahili, na **mitihani ya pytest-django**.

## Kwa nini Django? (Business value)
- P6 (Flask) ilitufundisha **msingi**; Django ni **kiwango cha
  kibiashara** - ndio kinatumika na kampuni nyingi (Instagram, Mozilla)
- **Vitu uliyolazimika kujenga mwenyewe kwenye Flask, Django anatoa
  tayari**: admin, auth, CSRF, ORM, migrations, forms, messages,
  password validation
- Hii ni **mradi kubwa zaidi** ya portfolio: inaonyesha ukuaji
  (Flask -> Django) kwa mwajiri

## Nadharia kwa maana halisi (Theory)
| Dhana | Sampuli ya maisha | P10 |
|---|---|---|
| **ORM** | Kufanya kazi na DB kama "orodha za Python" - SQL umefichwa | `Wateja.objects.filter(...)` |
| **Migration** | Ramani mpya ya ofisi - mpango unaohifadhiwa kwa hatua | `makemigrations` + `migrate` |
| **MVT** | M (data) - V (maamuzi) - T (muundo wa kuona) | models - views - templates |
| **CSRF token** | Kadi ya usalama kwa kila fomu | `{% csrf_token %}` |
| **Groups (majukumu)** | Kadi ya mlango: admin/mpokeaji/mhasibu | `linahitaji_jukumu` |
| **admin site** | "Ofisi ya mfumo" iliyojengwa tayari | `/admin/` (Kiswahili!) |
| **Django messages** | Ujumbe wa "imehifadhiwa!" unaodumu kwa sekunde chache | `messages.success(...)` |

## Jinsi ya kutumia (How to run)
```powershell
cd $env:USERPROFILE\Desktop\DATA\PORTFOLIO\P10-django-benki360
python manage.py migrate
python manage.py anza        # majukumu + watumiaji + data ya mfano
python manage.py runserver   # au double-click start.bat
```
- Mfumo: http://127.0.0.1:8000
- Admin (Kiswahili): http://127.0.0.1:8000/admin/ (admin/benki123)
- Majukumu: **admin**/benki123 (kila kitu), **mpokeaji**/pokea123
  (wateja, fedha, malipo), **mhasibu**/hesabu123 (ripoti, mikopo)
- Mitihani: `python -m pytest -q` (18 tests)

## Ethical AI / Ethics
1. **Nenosiri**: Django linatumia PBKDF2 (kama P6) - halionekani popote
2. **Faragha**: data ya wateja ni ya ndani - ripoti haionyeshwi bila
   ruhusa (403 kwa jukumu lisilofaa)
3. **CASCADE**: kufuta mteja kunafuta akaunti/miamala - hatari! hivyo
   ni kazi ya **admin pekee** + confirmation
4. **Secrets**: `SECRET_KEY` ya demo si ya production (angalia upgrades)
5. **CSRF**: kila POST ina tokeni - jaribu kuifuta ukione 403

## Malengo ya kiwango cha juu (Production upgrades)
1. **PostgreSQL** (P8) badala ya SQLite + `dj-database-url`
2. **Gunicorn + Nginx + HTTPS** (certbot) + `DEBUG=False` + env vars
3. **Django REST Framework**: API ya JSON (JWT) kwa simu/app
4. **Docker** (P8 skills): image + compose (app + postgres + nginx)
5. **Git/GitHub**: repo + `.env` (SECRET_KEY haijapikwi!) + CI (tests)
6. **Celery/Redis** kwa ripoti kubwa, **pagination**, **i18n** (EN/SW)

## Mtandao wa hatua zinazofuata (Roadmap)
- [x] P1-P9 (miradi 9 ya msingi)
- [x] **P10 Benki 360 (hii)** - mradi mkuu #1: Django core
- [ ] **P11 Mfumo wa Ofisi** - mradi mkuu #2: workflows/maombi (PPRA)
- [ ] **P12 Biashara (E-commerce)** - mradi mkuu #3: duka la mtandaoni
- [ ] Vyeti (Ngazi ya 4) baada ya miradi hii mitatu
