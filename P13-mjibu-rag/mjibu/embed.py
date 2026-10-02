import os

import httpx
from sklearn.feature_extraction.text import HashingVectorizer

# Vekta za maneno (hashing): namba thabiti, offline, bure.
# Mfumo wa kisasa wa Ollama (0.5+ /api/embed) hutoa embeddings halisi
# za maana - zinapatikana kwa MJIBU_EMBED=ollama; Ollama hii (0.35)
# haiunga mkono /api/embed, hivyo auto huanguka kwenye hashing.
_mashine = HashingVectorizer(n_features=512, ngram_range=(1, 2),
                             alternate_sign=False, lowercase=True)
_hali = {"ollama_imeshindwa": False}


def vipimo(maadhi):
    """Badilisha matini kuwa vekta. Ollama (neural) -> hashing (offline)."""
    mfumo = os.getenv("MJIBU_EMBED", "auto")
    if mfumo in ("auto", "ollama") and not _hali["ollama_imeshindwa"]:
        v = _ollama(maadhi)
        if v is not None:
            return v
        _hali["ollama_imeshindwa"] = True
        if mfumo == "ollama":
            return None
    return _hashing(maadhi)


def _hashing(maadhi):
    return _mashine.transform(maadhi).toarray().astype("float32").tolist()


def _ollama(maadhi):
    msingi = os.getenv("MJIBU_OLLAMA_URL",
                       "http://127.0.0.1:11434").rstrip("/")
    mfano = os.getenv("MJIBU_EMBED_MODEL",
                      os.getenv("MJIBU_MODEL", "llama3.2:1b"))
    majibu = []
    try:
        for m in maadhi:
            r = httpx.post(msingi + "/api/embeddings",
                           json={"model": mfano, "prompt": m},
                           timeout=30)
            r.raise_for_status()
            majibu.append(r.json()["embedding"])
        return majibu
    except Exception:
        return None
