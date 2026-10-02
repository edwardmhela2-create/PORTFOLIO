# PORTFOLIO — Miradi (P1–P9 + mradi mkuu P10 → P12)

Hii ndiyo **portfolio yako ya ujuzi** - kila mradi unajibu **kitu halisi**
kilichoambuliwa kwenye CV/PPRA na kinarudiana na kipindi cha 1.1 → 3.3.

## Ramani ya miradi

| # | Mradi | Ujuzi unaothibitisha | Amri ya haraka |
|---|-------|----------------------|----------------|
| P1 | **SysReport** | PowerShell, ripoti za OS, Task Scheduler | `powershell -File sysreport.ps1` |
| P2 | **NetMapper** | sockets, ports, ARP, ripoti HTML | `python netmap.py` |
| P3 | **Mkopo CLI Pro** | CRUD, SQLite, argparse, pytest 18 | `python main.py menyu` |
| P4 | **Portfolio Website** | HTML/CSS/JS (tovuti hii) | fungua `index.html` |
| P5 | **Database Design** | ERD, constraints, VIEW, TRIGGER | `python fanya.py` |
| P6 | **Benki App v2** | Flask, authn/authz, CSRF, sessions | `python app.py` → :5000 |
| P7 | **CyberToolkit** | hashing, HMAC, port scan, GUI | `python cyber.py menyu` |
| P8 | **Docker/Compose** | Dockerfile, volumes, healthcheck | `docker compose up -d --build` |
| P9 | **Mielelezo (ML)** | scikit-learn, TF-IDF, metrics, 94.7% | `python mielelezo.py fundisha` |
| P10 | **Benki 360 (Django)** | Django 6, ORM, majukumu, CSRF, admin Kiswahili (tests 19) | `python manage.py runserver` |
| P11 | **Ofisi 360 (Django)** | workflow (state machine), signals/audit, faili+CSV, CBV, pagination (tests 20) | `python manage.py runserver` |
| P12 | **Duka la Kwanza (Biashara)** | e-commerce: M2M, kikapu+context processor, checkout atomic, snapshot, Update/DeleteView (tests 24) | `python manage.py runserver` |

## Sentensi moja kwa kila mradi (kwa CV/interview)
1. **SysReport** - nilijenga ripoti inayojitengeneza ya hali ya kompyuta
   + ratiba ya kila siku (PowerShell + Task Scheduler).
2. **NetMapper** - nilichambua mtandao wangu: IP zilizo hai, milango
   wazi, na alama za usalama (Python sockets + ThreadPool).
3. **Mkopo CLI Pro** - mfumo kamili wa mikopo (riba, riba inayopungua,
   SQL, CSV, logs) wenye **mitihani 18**.
4. **Portfolio Website** - tovuti responsive yenye kichujio cha miradi
   (HTML/CSS/JS, bila framework).
5. **Database Design** - niliundа **ERD**, kuweka constraints, VIEW na
   TRIGGER halisi; data inazuiwa kuharibika (SET NULL/RESTRICT).
6. **Benki App v2** - web app yenye **usalama wa kweli**: sessions,
   CSRF token kwa kila POST, majukumu 3, nenosiri halisiwa (PBKDF2) -
   **mitihani 14**.
7. **CyberToolkit** - zana 8 za usalama (hash, HMAC integrity, port
   scan, hardening checklist) + **GUI** ya Tkinter - **mitihani 15**.
8. **Docker/Compose** - nilipanga P6 ndani ya **container** yenye
   volume ya data (haiharibiki) + healthcheck + build context ndogo
   (45KB) kwa `.dockerignore` - **mitihani 6**.
9. **Mielelezo (ML)** - spam predictor wa **offline** (Kiswahili/
   Kiingereza): TF-IDF + Naive Bayes, train/test split, **94.7%**
   usahihi, model iliyohifadhiwa - **mitihani 9**.
10. **Benki 360 (Django)** - mradi mkubwa wa Django 6: ORM +
    migrations, majukumu 3 (Group), CSRF kiotomatiki, CASCADE,
    **admin ya Kiswahili**, ripoti - **mitihani 19**.
11. **Ofisi 360 (Django)** - daftari la barua (namba + faili),
    **workflow ya maombi** (rasimu → idhini/kataa + maoni),
    **audit trail kwa signals**, ripoti ya CSV, pagination -
    **mitihani 20**.
12. **Duka la Kwanza (Django)** - e-commerce kamili: **M2M lebo**,
    kikapu (unique constraint + **context processor**), checkout
    **transaction.atomic**, **snapshot ya bei/jina** (SET_NULL),
    Update/DeleteView - **mitihani 24**.

## Jumla kwa CV (verification)
- **Miradi 12/12** (P1-P12) ✅ | **mitihani 125** (18+14+15+6+9+19+20+24) inapita
- Teknolojia: PowerShell, Python, Flask, **Django**, SQLite,
  HTML/CSS/JS, scikit-learn, Docker, Git(→ kujifunza), Tkinter
- **Ethics**: hashing si reverse-able, port scan ni ya mifumo yako tu,
  secrets hazipikwi kwenye picha, faragha ya data, model si hukumu ya
  mwisho (precision/false-positive)

## Hatua zinazofuata (kulingana na ramani)
1. ✅ Ngazi 1-3 + Miradi P1-P9 → IMEKAMILIKA
2. ✅ **P10 Benki 360 (Django)** → IMEKAMILIKA (tests 19)
3. ✅ **P11 Mfumo wa Ofisi (Django #2)** → IMEKAMILIKA (tests 20)
4. ✅ **P12 Biashara (E-commerce)** → IMEKAMILIKA (tests 24) - mradi wa mwisho mkubwa
5. ⬜ **Ngazi ya 4: Vyeti** → fundamentals (Cisco/MTA/Google) → CHL
   (baada ya P10-P12 kama ulivyosema)
6. ⬜ **File 2: Maombi ya PPRA** (miradi ya sampuli ya barua + CV)
7. ⬜ Git: `git init` kwenye PORTFOLIO + GitHub (bila API keys/secrets;
   SECRET_KEY ya Django iwe kwenye `.env`, si kwenye Git)
