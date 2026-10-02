import os

import httpx


def jibu(swali, muktadha, muda=90):
    """Piga Ollama (local) au API ya wingu kupitia .env - kubadilika kirahisi.

    Mfumo: OLLAMA_URL/MODEL; production: ongeza Anthropic/OpenAI client
    wenyewe hapa ndipo "interchangeable backends" inapotokea.
    """
    msingi = os.getenv("MJIBU_OLLAMA_URL",
                       "http://127.0.0.1:11434").rstrip("/")
    mfano = os.getenv("MJIBU_MODEL", "llama3.2:1b")
    kifungu = [
        {"role": "system", "content": muktadha},
        {"role": "user", "content": swali},
    ]
    try:
        r = httpx.post(
            msingi + "/api/chat",
            json={
                "model": mfano,
                "messages": kifungu,
                "stream": False,
                "options": {"temperature": 0.1, "num_predict": 300},
            },
            timeout=muda,
        )
        r.raise_for_status()
        return r.json()["message"]["content"]
    except Exception:
        return None
