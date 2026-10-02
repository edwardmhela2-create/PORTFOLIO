import os
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import llm
from .ingest import MAHITAJI, tengeneza_nyaraka
from .prompts import jenga_muktadha
from .retrieve import Hifadhi

MIZIZI = Path(__file__).resolve().parent.parent
DATA = MIZIZI / "data" / "nyaraka"
hifadhi = Hifadhi()


def pakia_yote():
    if not DATA.exists():
        return
    yaliopo = {n["jina"] for n in hifadhi.nyaraka}
    for f in sorted(DATA.iterdir()):
        if f.suffix.lower() in MAHITAJI and f.name not in yaliopo:
            try:
                hifadhi.ongeza(tengeneza_nyaraka(f))
            except Exception:
                continue


@asynccontextmanager
async def lifespan(app):
    if os.getenv("MJIBU_LOAD", "1") == "1":
        pakia_yote()
    yield


app = FastAPI(title="Mjibu - Maswali kwa Nyaraka (RAG)",
              lifespan=lifespan)


class Swali(BaseModel):
    swali: str = Field(min_length=2, max_length=500)


@app.post("/api/pakia")
async def pakia(faili: UploadFile = File(...)):
    jina = Path(faili.filename or "bila_jina").name
    if Path(jina).suffix.lower() not in MAHITAJI:
        raise HTTPException(400, "Tumia .txt, .md au .pdf pekee")
    DATA.mkdir(parents=True, exist_ok=True)
    barua = await faili.read()
    (DATA / jina).write_bytes(barua)
    try:
        ny = tengeneza_nyaraka(DATA / jina)
    except Exception as e:
        raise HTTPException(400, "Haiwezi kusoma faili: %s" % e)
    hifadhi.ondoa(jina)
    hifadhi.ongeza(ny)
    return {"jina": jina, "vipande": len(ny["vipande"]),
            "herufi": ny["herufi"]}


@app.get("/api/nyaraka")
def nyaraka():
    return [{"jina": n["jina"], "vipande": len(n["vipande"]),
             "herufi": n["herufi"]} for n in hifadhi.nyaraka]


@app.delete("/api/nyaraka/{jina}")
def futa(jina: str):
    if not any(n["jina"] == jina for n in hifadhi.nyaraka):
        raise HTTPException(404, "Nyaraka haipo")
    hifadhi.ondoa(jina)
    f = DATA / jina
    if f.exists():
        f.unlink()
    return {"imefutwa": jina}


@app.post("/api/swali")
def uliza(s: Swali):
    k = int(os.getenv("MJIBU_K", "4"))
    matokeo = hifadhi.tafuta(s.swali, k=k)
    vyanzo = [{"jina": m["jina"], "namba": m["namba"],
               "alama": m["alama"]} for m in matokeo]
    if not matokeo:
        return {"hali": "hakuna_muktadha",
                "jibu": "Sijui - hakuna nyaraka zinazohusiana na "
                        "swali hili kwenye database.",
                "vyanzo": []}
    muktadha = jenga_muktadha(matokeo)
    muda = time.time()
    majibu = llm.jibu(s.swali, muktadha)
    if majibu is None:
        return {"hali": "llm_hai",
                "jibu": "LLM haipatikani. Hakikisha Ollama inaendeshwa "
                        "(ollama serve) jaribu tena.",
                "vyanzo": vyanzo}
    return {"hali": "ok", "jibu": majibu, "vyanzo": vyanzo,
            "muda_ms": int((time.time() - muda) * 1000)}


@app.get("/")
def nyumbani():
    return FileResponse(MIZIZI / "static" / "index.html")


app.mount("/static",
          StaticFiles(directory=MIZIZI / "static"), name="static")
