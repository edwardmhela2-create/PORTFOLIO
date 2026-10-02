# P11 — Ofisi 360 (Django #2) — MRADI MKUU #2 (PPRA-aligned)

## Maelezo Mafupi (Description)
Mfumo wa ofisi kwa **Django**: daftari la **barua** (namba ya
kiotomatiki `WDA/2026/001` + upakuaji wa faili), **maombi** yenye
**workflow (state machine)**: rasimu → imewasilishwa →
imeidhinishwa/imekataliwa, **kumbukumbu za kiotomatiki (signals)**,
pagination, utafutaji, na **ripoti ya CSV**.

## Kwa nini mradi huu? (Business value)
- Ni **mfumo halisi wa ofisi** (PPRA/sekta ya umma): barua na maombi
  ndio "damu" ya ofisi yoyote ya umma
- **Workflow** inazuia makosa: mtu asiweze "kuidhinisha maombi yake
  mwenyewe", kataa lisilokuwa na maoni lisitokee, hali mbaya
  (kukagua mara mbili) isitokee - **sheria ndani ya code**
- **Audit trail (kumbukumbu)**: "nani alifanya nini na lini" -
  msingi wa uwajibikaji (accountability) ofisini

## Nadharia kwa maana halisi (Theory)
| Dhana | Sampuli ya maisha | P11 |
|---|---|---|
| **State machine** | Tiketi ya safari: wazi → imeagizwa → imefika (hauwezi kurudi nyuma bila sababu) | `Maombi.wasilisha()/kagua()` |
| **Signal** | Alarm ya ofisi inayojiwasha yenyewe kila mtu aingiapo | `post_save` → Kumbukumbu |
| **Class-based views** | "Vifaa tayari" vya Django (badala ya function kila kitu) | `ListView/DetailView/CreateView` |
| **Pagination** | Kurasa za kitabu - 10 kwa ukurasa si orodha ndefu | `paginate_by=10` |
| **File upload + MEDIA** | Kuhifadhi barua halisi kwenye boxi la ofisi | `FileField` + `/media/` |
| **CSV export** | "Excel button" ya ripoti | `HttpResponse(text/csv)` + BOM |
| **PermissionDenied vs redirect** | 403 = "huna kadi"; 302 = "enda lipa kadi kwanza" | mixin + decorator |

## Jinsi ya kutumia (How to run)
```powershell
cd $env:USERPROFILE\Desktop\DATA\PORTFOLIO\P11-ofisi-django
python manage.py migrate
python manage.py anza     # majukumu + watumiaji + data ya mfano
python manage.py runserver
```
- Mfumo: http://127.0.0.1:8000 | Admin: `/admin/`
- Watumiaji: **admin/ofisi123** (kila kitu), **juma/mtum123**
  (mfanyakazi - kuandika+kuwasilisha maombi), **neema/meneja123**
  (meneja - kukagua+ripoti+kumbukumbu), **rejest/rej123**
  (rejista - kupakia barua)
- Mitihani: `python -m pytest -q` (**20 tests**)

## Ethical AI / Ethics
1. **Audit trail haziwezi kufutwa** UI - uwajibikaji > urahisi
2. **Faili ni siri**: uploads ni za ofisi tu (media haipaswi kufunguliwa
   nje bila auth - production: nginx + auth)
3. **Kukataa lazima liwe na maoni** - maamuzi ya binadamu yanahitaji
   sababu (explainability)
4. **CSV na data ni ya ndani** - haishirikiwi na server za nje
5. CSRF: kila POST ina tokeni ({% csrf_token %})

## Malengo ya kiwango cha juu (Production upgrades)
1. **PostgreSQL + Gunicorn/Nginx/HTTPS** (P8) + `DEBUG=False` + `.env`
2. **Django REST Framework** + JWT (API kwa simu ya ofisi)
3. **Mention/Email**: Django `send_mail` (offisi SMTP) wakati maombi
   yamewasilishwa
4. **Kurasa za hariri** (UpdateView) + kuondoa rasimu (DELETE)
5. **Docker** (P8): app + postgres + nginx + media volume
6. **Git + GitHub**: `.env` (SECRET_KEY) si kwenye Git

## Mtandao wa hatua zinazofuata (Roadmap)
- [x] P1-P9 (miradi 9 ya msingi)
- [x] P10 Benki 360 (Django #1) - CRUD, roles, CSRF
- [x] **P11 Ofisi 360 (hii)** - workflow, signals, files, CSV, CBV
- [ ] P12 Biashara (E-commerce) - mradi mkuu #3
- [ ] Vyeti (Ngazi ya 4) baada ya miradi mitatu mikubwa
