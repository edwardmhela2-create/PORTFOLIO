import re
from pathlib import Path

import pypdf

MAHITAJI = {".txt", ".md", ".pdf"}


def gawanya(mandishi, ukubwa=600, hatua=500):
    """Vipande vya herufi vinavyojirudia (overlap) - huboresha retrieval."""
    mandishi = re.sub(r"\n{3,}", "\n\n", (mandishi or "").strip())
    if not mandishi:
        return []
    vipande = []
    i = 0
    while i < len(mandishi):
        vipande.append(mandishi[i:i + ukubwa])
        if i + ukubwa >= len(mandishi):
            break
        i += hatua
    return vipande


def soma_pdf(njia):
    hadithi = pypdf.PdfReader(njia)
    sehemu = []
    for kwa, ukurasa in enumerate(hadithi.pages, 1):
        sehemu.append("[ukurasa %d]\n%s" % (kwa, ukurasa.extract_text() or ""))
    return "\n\n".join(sehemu)


def soma_faili(njia):
    njia = Path(njia)
    if njia.suffix.lower() == ".pdf":
        return soma_pdf(njia)
    if njia.suffix.lower() in {".txt", ".md"}:
        return njia.read_text(encoding="utf-8", errors="replace")
    raise ValueError("Aina ya faili haikubaliwi: %s" % njia.suffix)


def tengeneza_nyaraka(njia, jina=None):
    mandishi = soma_faili(njia)
    return {
        "jina": jina or Path(njia).name,
        "vipande": gawanya(mandishi),
        "herufi": len(mandishi),
    }
