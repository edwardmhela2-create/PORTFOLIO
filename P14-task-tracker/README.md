# P14 — Task Tracker (Angular)

Mradi wa **Soko la Post 1 (Frontend)** kwa mujibu wa
*PPRA ICT Skills Learning Guide*: **"task tracker" kwa Angular + REST
backend** — hapa ni **sehemu ya Angular** (web app).

## Stack
- **Angular 21** (guide inahitaji v14+) + **TypeScript**
- Standalone component, **signals** (state), `@for` control flow
- Routing tayari (`app.routes.ts`), **Vitest** kwa mitihani
- UI ya Kiswahili (kawaida ya repo hii)

## Nguzo za somo la #1 na #2 zilizotumika
| Somo | Nguzo | Mahali hapa |
|---|---|---|
| #1 Angular | Component + Template, interpolation `{{ }}`, signal state, event/property binding, `@for`, router | `src/app/app.ts`, `app.html` |
| #2 TypeScript | **`interface Kazi`**, **`type Kichujio` (union)**, **class + `@Injectable` + private state**, **`inject()` (DI)**, `computed`, strict mode | `src/app/kazi.service.ts` |

## Endesha
```powershell
$env:NODE_OPTIONS="--dns-result-order=ipv4first"   # kwa hii kompyuta
ng serve --port 4200        # → http://127.0.0.1:4200
ng test --watch=false       # mitihani 4 (vitest)
```

## Kumbuka ya mtandao (kompyuta hii)
Node/npm inaweza kukwama kwa **IPv6** (haifanyi kazi hapa) — tumia
`NODE_OPTIONS=--dns-result-order=ipv4first` kila unapoinstall kwa
mara ya kwanza.

## Kilachofuata (Post 1)
- Skill #3: Tailwind + Flexbox/Grid + Angular Material
- Skill #5: NgRx (badala ya service signals)
- Skill #7: backend ya REST (FastAPI) + kuunganisha hapa
- App Store listing, Git workflow, Figma

## Mitihani
7 tests (vitest): component (kichwa, kichujio), **KaziService**
(hali, idhini, ongeza + usafi wa input).
