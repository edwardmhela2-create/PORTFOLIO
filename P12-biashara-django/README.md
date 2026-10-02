# P12 — Duka la Kwanza (Biashara / E-commerce)

Mradi wa **3 na wa mwisho mkubwa** wa Django: duka la mtandaoni
lenye kikapu, oda, malipo ya mfano, stoo, na simamiaji wa bidhaa.
Unaunganisha kila ulichojifunza P10 (ORM/roles/CSRF) na P11
(CBV/state machine/signals) pamoja na vipengele vipya:

- **ManyToMany (M2M)** — bidhaa nyingi ↔ lebo nyingi
- **Context processor** — idadi ya kikapu kwenye KILA ukurasa (navbar)
- **Checkout ya `transaction.atomic`** — oda + kupunguza stoo pamoja
  au kutofautika (all-or-nothing)
- **Snapshot** — bei + jina la bidhaa hifadhiwa kwenye oda (mabadiliko
  ya baadaye hayaathiri oda za zamani)
- **UpdateView / DeleteView** — CBV za hariri/futa (P11 alikuwa
  List/Detail/Create pekee)
- **Unique constraint** — kila mtumiaji haezi kuwa na bidhaa
  ileile mara mbili kikapuni

## Thamani ya biashara
Hii ndiyo **PPRA capstone**: kampuni nyingi za Tanzania zinahitaji mtu
ayejua e-commerce (oda, stoo, malipo, ripoti) — si Django tu, bali
**mfumo kamili wa biashara**.

## Nadharia kwa mifano halisi
| Nadharia | Mfano wa maisha |
|---|---|
| M2M | "Chapisho" na "Lebo" — kila la moja linaweza kuwa na zaidi ya moja |
| Context processor | Idadi ya kikapu kwenye kila ukurasa kama **risiti ya kifua** |
| `transaction.atomic` | Pesa zinatoka akaunti A **NA** kuingia B — si nusu |
| Snapshot | Unanunua soda kwa 1,000; bei inapanda kesho risiti yako bado ni 1,000 |
| `SET_NULL` + snapshot | Bidhaa ikifutwa dukani, oda yako bado inaonyesha ulichonunua |

## Endesha
```powershell
python manage.py migrate      # mara ya kwanza tu
python manage.py anza         # jaza duka: 12 bidhaa + watumiaji
python manage.py runserver    # au start.bat
# http://127.0.0.1:8000
```

## Watumiaji wa majaribio
| Mtumiaji | Nenosiri | Jukumu |
|---|---|---|
| `admin` | `duka123` | admin (superuser + muuzaji) |
| `hassan` | `muuz123` | muuzaji (ongeza/hariri/futa bidhaa) |
| `amina` | `kinu123` | mnunuzi (kikapu + oda) |

## Mwendo wa jaribio
1. Ugomboa **bila kuingia**: bidhaa zinaonekana (mchepuo wa P11);
   kikapu/lipa vinakataa (302 → ingia).
2. Ingia `amina` → ongeza bidhaa 2 kikapuni → badilisha idadi →
   futa moja → **Lipa Sasa** (jaribu M-Pesa bila namba = makosa!) →
   ona namba ya oda `ORD/2026/0001`.
3. Ingia `hassan` → **+ Bidhaa mpya** → jaribu `amina` kwa hiyo
   njia = **403** (PermissionDenied).
4. Badilisha bei ya bidhaa uliyonunua → fungua oda yako →
   bei ya zamani **haijabadilika** (snapshot).

## Maadili (Ethics)
- Malipo ni **MFANO** — hakuna M-Pesa API halisi, hakuna pesa
  halisi zinazohamia; hii ni demo ya workflow tu.
- Hifadhi data za watumiaji kwa uangalifu (namba za simu) —
  production: privacy policy + encryption + access logs.
- Watumiaji wasipate stoo au bei za wapinzani kwa sirini (tumia
  permissions kama hizi hapa juu).

## Viwango vya production (Production upgrades)
- Malipo halisi: M-Pesa C2B/B2C API + webhook + idhini ya mara
  mbili (signature verification).
- Bei salama: `select_for_update()` + PostgreSQL (SQLite
  inapuuza locking — race condition bado iko hapa).
- Picha za bidhaa: `ImageField` + Pillow + media hosting (S3).
- Wageni (guest cart): kikapu cha session kabla ya kuingia.
- Ripoti: foleni ya kazi (Celery) kwa oda kubwa + email notifications.
- Cache ya navbar badge (context processor inapiga DB kila ukurasa).
- SEO: slugs, meta tags, sitemap.

## Ramani (Roadmap)
- ✅ P10 Benki 360 (Django #1)
- ✅ P11 Ofisi 360 (Django #2)
- ✅ **P12 Duka la Kwanza (Django #3)** — unakoona hapa
- ⬜ Ngazi ya 4: Vyeti (Django certification, Google/IBM, n.k.)
- ⬜ Kuomba kazi kwa PPRA (File 2)

## Maswali ya kufikiria
1. Kwa nini `kikapu_hali` (context processor) inapiga DB **kila
   ukurasa**? Ni hatari gani kwenye tovuti yenye watumiaji 100,000,
   na ni suluhisho gani (cache/session)?
2. `OdaBidhaa.bei` ni **snapshot** — kwa nini si tu kuunganisha
   `bidhaa.bei` live? Onyesha kwa sentensi: nini kingetokea bidhaa
   ikifutwa ikiwa tulitumia FK tu?
3. `lipa()` inaweka kila kitu ndani ya `transaction.atomic()` —
   kama hatua ya mwisho (`Kipengele.delete()`) inashindwa, nini
   kimehifadhiwa na nini hakujatokea? Kwa nini hii ni bora kuliko
   kuandika hatua 5 kando kando?

## Mitihani
```powershell
python -m pytest -q    # 24 tests
```
