# P1 — SysReport: Ripoti ya Mfumo kwa PowerShell

## Maelezo Mafupi (Description)
SysReport ni script ya PowerShell inayokusanya taarifa muhimu za kompyuta
(hardware, mifumo ya uendeshaji, mtandao, afya ya betri/diski) na kuzitengeneza
kuwa **ripoti ya HTML** inayosomeka kwenye browser yoyote.

Inalenga ICT Officers / System Administrators wanaohitaji kuona hali ya
kompyuta (asset inventory) bila kutembelea kila kifaa kwa mkono.

## Kwa nini (Business value)
- **Audit** — TCRA / benki: kuonyesha vifaa vyote vya ICT vinavyotumika
- **Bajeti** — kutambua kompyuta zinazohitaji kuongezwa RAM / diski
- **Helpdesk** — kutatua matatizo bila kuondoka kwenye kiti
- **Usalama** — kutambua Windows/programu zisizolindwa
- **Automation** — inaweza kuendeshwa kila siku kwa Task Scheduler

## Teknolojia (Tech stack)
| Kipengele | Teknolojia |
|---|---|
| Lugha | PowerShell 5.1+ |
| Kukusanya data | CIM/WMI (`Get-CimInstance`) |
| Output | HTML (`ConvertTo-Html`) |
| Kuendesha mara kwa mara | Windows Task Scheduler |

## Vipengele (Features)
- CPU: jina, core, kasi
- RAM: jumla, iliyotumika, iliyobaki
- Diski: ukubwa, % iliyojaa (kwa alama 🔴/🟡/🟢)
- Mfumo: Windows version, uptime (muda tangu kuzimwa mwisho)
- Mtandao: IP, MAC, gateway
- Betri: afya % (laptop)
- Ripoti ya HTML yenye rangi na tahadhari

## Jinsi ya kutumia (How to run)
```powershell
# Kwenye folda ya mradi:
Set-Location .\P1-sysreport
.\sysreport.ps1
```
Script itakusanya data kisha **kufungua ripoti kwenye browser**.

## Output
Faili `report.html` lenye ripoti kamili + onyo la tahadhari kwa kila sehemu.

## Malengo ya kiwango cha juu (Production upgrades)
Kwa makampuni makumbwa (CRDB, Vodacom, NMB, TCRA):
1. Kukusanya data kwa **remote** kutoka PC zote za mtandao (WinRM)
2. Kuhifadhi kwenye **PostgreSQL** ili kuona mabadiliko kwa muda (history)
3. **Dashboard** (Grafana/Power BI) — PC zote kwenye skrini moja
4. **Alerts** — barua pepe otomatiki kama disk imejaa 90%

## Mtandao wa hatua zinazofuata (Roadmap)
- [ ] P2 — NetMapper (utafutaji wa mtandao + port scan)
- [ ] P3 — Mkopo CLI Pro
- [ ] P4 — Portfolio website (kitovu cha project zote)
