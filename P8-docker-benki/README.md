# P8 — Docker: Benki App (P6) kwenye Container

## Maelezo Mafupi (Description)
Kuendesha **P6 (Benki App)** ndani ya **container** - package moja
inayojitegemea (Python + Flask + DB) inayofanya kazi **popote** pale
Docker inapokuwa: kompyuta yako, server ya mchakato, cloud... bila
kusema "inakwenda kwangu!"

## Nadharia kwa maana halisi (Theory)

**Container vs Virtual Machine (VM):**
| | Container (Docker) | VM (VirtualBox) |
|---|---|---|
| Analogia | **Mashipu ya mizigo** (container bandari!) | **Jengo** lenye umeme, umeme, back-up |
| Kina nini? | Programu tu (mbunifu: Python+app) | OS yote (Windows/Linux) |
| Uzito | **Mara chache ya MB** | GB nzima |
| Kuanza | sekunde chache | dakika |
| Mfano wetu | `benki-p8` (~150MB) | Windows 11 (~20GB) |

**Image vs Container:**
- **Image** = **mpishi/recipe** (haijapikwa - ni maelezo tu)
- **Container** = **chakula kilichopikwa** (kinakimbia sasa!)
> Ukifuta container - **image bado ipo**, unaweza kutengeneza jipya.

**Kwa nini data haipaswi kuwa ndani ya container?**
Container ni **ya muda** (inaweza kufutwa/dispose) - kama **kikombe
cha mkahawa**: unakunywa, unaweka kama chupa ya **volume** (benki.db)
- container inapofungwa, **data inabaki** volume.

## Jinsi ya kutumia (How to run)

### Njia 1: Docker Compose (rahisi zaidi - inashauriwa)
```powershell
cd $env:USERPROFILE\Desktop\DATA\PORTFOLIO\P8-docker-benki
docker compose up -d --build
# browser: http://localhost:5000  (admin / benki123)
docker compose logs -f           # soma logs (Ctrl+C = simamisha kuona)
docker compose down              # simamisha + futa container (DATA INABAKI!)
```

### Njia 2: Amri za kawaida (build + run)
```powershell
cd $env:USERPROFILE\Desktop\DATA\PORTFOLIO
docker build -f P8-docker-benki/Dockerfile -t benki-p8 .
docker run -d --name benki-p8 -p 127.0.0.1:5000:5000 -v benki-data:/data benki-p8
docker ps                       # onyesha inayokimbia
docker stop benki-p8            # simamisha
docker rm benki-p8              # futa container (volume inabaki!)
```

### Kuona data imehifadhiwa (volume):
```powershell
docker volume inspect P8-docker-benki_benki-data   # njia ya volume
docker exec benki-p8 ls -la /data                  # benki.db ipo hapa!
```

## Dockerfile - kila hatua inamaana gani?
| Hatua | Maana |
|---|---|
| `FROM python:3.12-slim` | Anza na msingi: Python ndogo (si full OS!) |
| `WORKDIR /app` | Folder ya kufanya kazi ndani ya container |
| `COPY P6-benki-app/ ./` | Leta code ya app (kutoka nje) |
| `RUN pip install flask` | Sakinisha mahitaji (mtandaoni wakati wa build) |
| `RUN useradd...` | **MTUMIAJI SI ROOT** (usalama! hata kama app inavunjika...) |
| `USER mtumiaji` | Endesha kama mtumiaji huyo, si mwenye uwezo mkuu |
| `ENV BENKI_DB=/data/benki.db` | DB iwe kwenye **volume** (si ndani ya container) |
| `EXPOSE 5000` | Onyesha port (arifa tu - lazima `-p` pia!) |
| `HEALTHCHECK` | Docker ichunguze: "je, app bado inafanya kazi?" |
| `CMD ["python","app.py"]` | Amri ya mwisho: inachocheza wakati container inapoanza |

## Ulinzi (security)
- **127.0.0.1:5000:5000** = port inafunguka **kwenye PC yako tu** (si network!)
  - kwa kila mtu wa LAN: badilisha kuwa `"5000:5000"` (kwa matumizi ya ndani tu)
- **USER si root**: hata kama mtu anapata udhibiti wa app, hana ruhusa za juu
- **Volume**: data haipotei; hakuna data ndani ya image (image ni "safi")
- **.dockerignore**: `*.db`, `P1-P7` zinakwepushwa - hakuna siri/programu
  nyingine zinaingia kwenye build (sawa na `.gitignore`)
- **Ethics**: tumia tu kwenye mifumo yako; usichapishe image zenye siri
  (funguo za siri/`secret_key`) kwenye registry ya umma (Docker Hub)

## Malengo ya kiwango cha juu (Production upgrades)
1. **Registry** (Docker Hub/AWS ECR) + **image signing** (usalama wa supply chain)
2. **Multi-stage build** (image ndogo zaidi: build haina compiler)
3. **Kubernetes** (orchestration - container nyingi kwa pamoja)
4. **CI/CD**: GitHub Actions - build + test kila ukibadilisha code
5. **Secrets management** (Docker secrets/KMS - si ENV ya wazi!)
6. **Log aggregation** + monitoring (Prometheus/Grafana)

## Mtandao wa hatua zinazofuata (Roadmap)
- [x] P1-P7
- [x] P8 — Docker (hii)
- [ ] P9 — ML Predictor
