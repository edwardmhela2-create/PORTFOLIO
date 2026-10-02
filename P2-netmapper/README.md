# P2 — NetMapper: Ramani ya Mtandao (IP Sweep + Port Scan)

## Maelezo Mafupi (Description)
NetMapper ni programu ya Python inayotembeza mtandao wa LAN na kutengeneza
"ramani" ya vifaa vyote vilivyo mtandaoni: IP zilizo hai, majina (hostname),
na milango (ports) iliyofunguliwa — pamoja na **alama za usalama** (🔴/🟡/🟢).

## Kwa nini (Business value)
- **Usalama wa mtandao** — kutambua kifaa kisichojulikana kinachoingia (rogue device)
- **Ukaguzi (audit)** — TCRA/benki: kufuatilia ufikiaji wa huduma (RDP, SSH, SMB)
- **Inventory** — kuona vifaa vyote vya kampuni bila kutembelea kila jack
- **Kutafuta hatari** — port 3389/445 wazi bila mpangilio = hatari ya shambulio

## Kanuni (How it works)
1. **IP Sweep** — IP zote za subnet (`/24`) zinapigwa maswali "uko hai?" kwa haraka
   (parallel — maswali mengi kwa wakati mmoja kwa `ThreadPoolExecutor`)
2. **Port Scan** — kwa kila IP iliyojibu, inajaribu milango muhimu
   (22, 80, 135, 445, 3389, n.k.) kwa TCP connect
3. **Dashboard** — inatengeneza `netmap.html` yenye alama za usalama

## Teknolojia (Tech stack)
| Kipengele | Teknolojia |
|---|---|
| Lugha | Python 3.14 |
| Sweep/Scan | `socket`, `concurrent.futures.ThreadPoolExecutor` |
| Output | HTML dashboard (bila API ya nje) |
| Security notice | "Authorized testing only" (mtandao wako tu) |

## Jinsi ya kutumia (How to run)
```powershell
cd $env:USERPROFILE\Desktop\DATA\PORTFOLIO\P2-netmapper
python netmapper.py                 # scan ya mtandao wako (192.168.118.0/24)
python netmapper.py --ports 80,445  # chagua ports maalum
```
Matokeo: `netmap.html` inafunguka kwenye browser.

## Output
`netmap.html` — jedwali: IP, hostname, ports wazi, alama za usalama (🟢/🟡/🔴).

## Usalama na kisheria (Ethics)
Kutumia tu kwenye **mtandao wenyewe** au uliopewa **ruhusa**. Ni kinyume cha
sheria kutafuta mtandao wa mtu mwingine bila ruhusa (Computer Misuse Act /
Sheria ya Mtandao ya Tanzania).

## Malengo ya kiwango cha juu (Production upgrades)
1. MAC address + kampuni (vendor/OUI lookup)
2. Historia ya scan + alert kwa IP mpya ("rogue device detected")
3. Ufikiaji wa mbali (remote scan ya mitandao mingi) + credential salama
4. Kuunganisha na firewall/SIEM (mf. Wazuh, Splunk) kwa uelewa wa pamoja

## Mtandao wa hatua zinazofuata (Roadmap)
- [x] P1 — SysReport
- [x] P2 — NetMapper
- [ ] P3 — Mkopo CLI Pro
- [ ] P4 — Portfolio website (kitovu cha project zote)
