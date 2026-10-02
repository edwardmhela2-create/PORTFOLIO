# P7 — CyberToolkit: Zana za Usalama (CLI)

## Maelezo Mafupi (Description)
Programu **moja ya amri (CLI)** ikiwa na zana **6 za usalama** zinazotumia
ujuzi wa 3.1: hash, encrypt, password generator/checker, port scanner na
ip classification. Zote **offline** (hazitumii internet).

## Kwa nini (Business value)
- **SOC/IT support** huhitaji kuthibitisha files (hash), kujenga nenosiri
  imara, na kuchunguza ports - kila siku
- **Ethics kwanza**: zana kama hizi ni **halali kwenye mifumo YAKO** tu -
  kuchunguza port za mtu mwingine bila ruhusa = **kosa la sheria** (3.1)
- Inaonyesha: **mtu mwenye zana nzuri + maadili** = muajiriwa mwema

## Teknolojia (Tech stack)
| Kipengele | Moduli (Python standard tu - hakuna package mpya!) |
|---|---|
| Hash/verify | `hashlib`, `hmac` |
| Encrypt demo | `base64` + XOR (funzo la crypto - si ya production!) |
| Passwords | `secrets`, `math` (entropy) |
| Ports | `socket`, `concurrent.futures` (threading) |
| IP | `ipaddress`, `socket` |

## Jinsi ya kutumia (How to run)
```powershell
cd $env:USERPROFILE\Desktop\DATA\PORTFOLIO\P7-cyber-toolkit
python cyber.py              - na amri: onyesha msaada
python cyber.py hash "habari"
python cyber.py hash --mzigo nakala.zip
python cyber.py siri --fumbo siri123 --andika "UJUMBE WANGU"
python cyber.py siri --fumbo siri123 --fungua "V2l6..."
python cyber.py tengeneza -n 20
python cyber.py imarisha "123456"
python cyber.py ports 192.168.118.1
python cyber.py ip 192.168.118.10
python cyber.py menyu            - menyu ya kibonzo (interactive)
python cyber.py ripoti 127.0.0.1 --fungua   - ripoti HTML + browser
```
Au double-click `cyber.bat`.

## GUI (dirisha la kibonzo - bila terminal!)
```powershell
python cyber_gui.py
```
Au double-click **`cyber_gui.bat`** (dirisha linafunguka moja kwa moja).

| Tab | Kazi |
|---|---|
| **Hash** | andika neno AU chagua file → hash; bandika hash → **Thibitisha** |
| **Siri** | Ficha/Fungua maandishi kwa funguo (HMAC inathibitisha) |
| **Nenosiri** | Tengeneza (urefu wowote) + Kagua nguvu (alama/entropy) |
| **Ports** | Chunguza host/porta - inakimbia kwa **thread** (dirisha halisimami!) |
| **IP** | Chambua IP yoyote au onyesha IP yako |

> Kiufundi: GUI ni **Tkinter** (inakuja na Python - hakuna package mpya) na
> inaita **functions zile zile** za `cyber.py` - code moja, interface mbili.
> Ports zinakimbia kwenye **thread** tofauti: kama zisingekimbia hivyo,
> dirisha lingesimama (frozen) wakati wa uchunguzi - somo muhimu la GUI.

## Zana 8
| Amri | Kazi | Ujuzi wa 3.1 |
|---|---|---|
| `hash` | SHA-256/512/1 ya neno AU file + thibitisha | Hashing, integrity |
| `siri` | Encrypt/decrypt (XOR+base64+HMAC) kwa funguo | Encryption (si ya prod!) |
| `tengeneza` | Nenosiri imara + entropy bits | Password policy |
| `imarisha` | Kagua nenosiri: alama + mapendekezo | Brute-force defense |
| `ports` | TCP scan ya ports (threading, timeout) | Network recon |
| `ip` | Classify IP: private/loopback/public... | IP addressing |
| `menyu` | Menyu ya kibonzo (interactive, bila kuandika amri) | CLI UX |
| `ripoti` | Uchunguzi wa ports → **file ya HTML** + browser | Ripoti/uzalishaji |

## Ethics (muhimu - 3.1)
1. **Tumia kwenye mifumo YAKO pekee** (kompyuta, router yako, network yako)
2. Kuchunguza port za mtu bila ruhusa = **kosa la sheria** (CMA/Cybercrimes)
3. XOR hapa ni **funzo tu** - kwa encryption halisi: AES-GCM (`cryptography`)
4. `imarisha` inakumbuka nembo za kawaida ("123456", "password", "qwerty")

## Malengo ya kiwango cha juu (Production upgrades)
1. **AES-GCM** halisi (`cryptography`) + key management (KMS)
2. **Nmap-style** service fingerprinting + UDP scan
3. **Rate limiting** + logging ya uchunguzi (audit)
4. **Dashboard** ya HTML kama ripoti ya P2
5. **Packaging**: `pip install .` au PyInstaller (.exe)
6. Fuzzing / vulnerability checks (mitihani ya usalama)

## Mtandao wa hatua zinazofuata (Roadmap)
- [x] P1-P6
- [x] P7 — CyberToolkit (hii)
- [ ] P8 — Docker
- [ ] P9 — ML Predictor
