import os

import httpx


def jibu(swali, muktadha, muda=90):
    """Backend inayobadilika: Ollama (ndani) au API ya wingu (.env).

    Kasoro zote mbili zinatumia mfumo mmoja wa prompt; kubadilisha
    ni MJIBU_BACKEND=ollama|openai pekee (halali: .env tu, si Git).
    """
    mfumo = os.getenv("MJIBU_BACKEND", "ollama").lower()
    if mfumo == "openai":
        return _wingu(swali, muktadha, muda)
    return _ollama(swali, muktadha, muda)


def maelezo():
    """Ujumbe wa kirafiki kwa mtumiaji kulingana na backend iliyochaguliwa."""
    if os.getenv("MJIBU_BACKEND", "ollama").lower() == "openai":
        return ("API ya wingu haipatikani. Hakikisha MJIBU_OPENAI_API_KEY "
                "ipo kwenye .env na mtandao uko sawa, jaribu tena.")
    return ("LLM haipatikani. Hakikisha Ollama inaendeshwa "
            "(ollama serve) jaribu tena.")


def _ollama(swali, muktadha, muda=90):
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


def _wingu(swali, muktadha, muda=90):
    msingi = os.getenv("MJIBU_OPENAI_URL",
                       "https://api.openai.com/v1").rstrip("/")
    ufunguo = os.getenv("MJIBU_OPENAI_API_KEY")
    if not ufunguo:
        return None
    mfano = os.getenv("MJIBU_OPENAI_MODEL", "gpt-4o-mini")
    try:
        r = httpx.post(
            msingi + "/chat/completions",
            headers={"Authorization": "Bearer " + ufunguo},
            json={
                "model": mfano,
                "temperature": 0.1,
                "max_tokens": 300,
                "messages": [
                    {"role": "system", "content": muktadha},
                    {"role": "user", "content": swali},
                ],
            },
            timeout=muda,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception:
        return None
