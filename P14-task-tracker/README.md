# P14 — Task Tracker (Angular)

Mradi wa **Soko la Post 1 (Frontend)** kwa mujibu wa
*PPRA ICT Skills Learning Guide*: **"task tracker" kwa Angular + REST
backend** — hapa ni **sehemu ya Angular** (web app).

## Stack
- **Angular 21** (guide inahitaji v14+) + **TypeScript**
- Standalone component, **signals** (state), `@for` control flow
- Routing tayari (`app.routes.ts`), **Vitest** kwa mitihani
- UI ya Kiswahili (kawaida ya repo hii)

## Nguzo za somo la #1 zilizotumika
| Nguzo | Mahali hapa |
|---|---|
| Component + Template | `src/app/app.ts` + `app.html` |
| Interpolation `{{ }}` | kichwa, counter |
| Signal state | `signal<Kazi[]>(...)`, `computed(...)` |
| Event binding `(click)` | kubonyeza kazi/checkbox |
| Property binding `[class]`, `[checked]` | mstari wa kukatwa |
| `@for` loop | orodha ya kazi |
| Router | `<router-outlet />` (tayari kwa kurasa zinazofuata) |

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
- Skill #2: TypeScript (interfaces, OOP, reactive)
- Skill #3: Tailwind + Flexbox/Grid + Angular Material
- Skill #7: backend ya REST (FastAPI) + kuunganisha hapa
- NgRx, App Store listing, Git workflow, Figma

## Mitihani
4 tests — hali ya kazi (kubadilisha/kukamilika), mwitikio wa UI,
ujuzi wa component.
