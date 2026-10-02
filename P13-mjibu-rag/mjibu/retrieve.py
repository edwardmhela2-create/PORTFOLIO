import json
import os
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer

from . import embed


class Hifadhi:
    """Hifadhi ya vekta (TF-IDF cosine sasa; embeddings/Chroma baadaye).

    Fundisho: RAG = Retrieve + Generate. Ubora wa retrieve ndio
    unaogombana na LLM nzuri - hii ni sehemu ya kwanza ya mfumo.
    """

    def __init__(self):
        self.nyaraka = []
        self.vipande = []
        self.mashine = None
        self.matrix = None

    def ongeza(self, nyaraka):
        kwa = len(self.nyaraka)
        self.nyaraka.append(nyaraka)
        for namba, maandishi in enumerate(nyaraka["vipande"]):
            self.vipande.append({
                "nyaraka": kwa,
                "namba": namba,
                "maandishi": maandishi,
            })
        self.jenga()

    def jenga(self):
        if not self.vipande:
            self.mashine = None
            self.matrix = None
            return
        maandishi = [v["maandishi"] for v in self.vipande]
        self.mashine = TfidfVectorizer(
            lowercase=True, ngram_range=(1, 2), min_df=1)
        self.matrix = self.mashine.fit_transform(maandishi)

    def ondoa(self, jina):
        mpya = []
        kwa_fupi = {}
        for k, n in enumerate(self.nyaraka):
            if n["jina"] == jina:
                continue
            kwa_fupi[k] = len(mpya)
            mpya.append(n)
        vip = []
        for v in self.vipande:
            if v["nyaraka"] in kwa_fupi:
                vip.append({**v, "nyaraka": kwa_fupi[v["nyaraka"]]})
        self.nyaraka = mpya
        self.vipande = vip
        self.jenga()

    def ondoa_yote(self):
        self.nyaraka = []
        self.vipande = []
        self.jenga()

    def tafuta(self, swali, k=4):
        if not self.vipande or not self.mashine:
            return []
        sw = self.mashine.transform([swali])
        alama = (self.matrix @ sw.T).toarray().ravel()
        nafasi = alama.argsort()[::-1][:k]
        matokeo = []
        for i in nafasi:
            if alama[i] <= 0:
                continue
            v = self.vipande[i]
            matokeo.append({
                "alama": round(float(alama[i]), 4),
                "jina": self.nyaraka[v["nyaraka"]]["jina"],
                "namba": v["namba"],
                "maandishi": v["maandishi"],
            })
        return matokeo


class HifadhiChroma:
    """Hifadhi ya vekta ya kudumu (Chroma) + embeddings (embed.py).

    Fundisho: vector DB = mahali pa kuhifadhi vekta na kutafuta kwa
    umbali (cosine) kwa haraka; vekta vinatolewa na embed.py ili
    zibadilike (hashing -> Ollama/neural) bila kugusa hifadhi hii.
    """

    def __init__(self, njia):
        import chromadb
        from chromadb.api.types import EmbeddingFunction

        class Tovuti(EmbeddingFunction):
            def __init__(self):
                pass

            def name(self):
                return "mjibu-vipimo"

            def __call__(self, input):
                raise RuntimeError(
                    "Tumia embed.vipimo() badala ya EF ya chroma")

        self.njia = Path(njia)
        self.njia.mkdir(parents=True, exist_ok=True)
        self.mteule = chromadb.PersistentClient(path=str(self.njia))
        self.mizigo = self.mteule.get_or_create_collection(
            "vipande", embedding_function=Tovuti(),
            metadata={"hnsw:space": "cosine"})
        self.nyaraka = []
        if self._faili().exists():
            self.nyaraka = json.loads(
                self._faili().read_text(encoding="utf-8"))

    def _faili(self):
        return self.njia / "nyaraka.json"

    def _hifadhi_kumbukumbu(self):
        self._faili().write_text(
            json.dumps(self.nyaraka, ensure_ascii=False),
            encoding="utf-8")

    def ongeza(self, nyaraka):
        self.nyaraka = [n for n in self.nyaraka
                        if n["jina"] != nyaraka["jina"]]
        self.nyaraka.append(nyaraka)
        self._hifadhi_kumbukumbu()
        self.mizigo.delete(where={"jina": nyaraka["jina"]})
        if not nyaraka["vipande"]:
            return
        vekta = embed.vipimo(nyaraka["vipande"])
        if vekta is None:
            raise RuntimeError("Vipimo havipatikani (angalia MJIBU_EMBED)")
        n = len(nyaraka["vipande"])
        self.mizigo.upsert(
            ids=["%s#%d" % (nyaraka["jina"], i) for i in range(n)],
            embeddings=vekta,
            documents=list(nyaraka["vipande"]),
            metadatas=[{"jina": nyaraka["jina"], "namba": i}
                       for i in range(n)])

    def ondoa(self, jina):
        self.nyaraka = [n for n in self.nyaraka if n["jina"] != jina]
        self._hifadhi_kumbukumbu()
        self.mizigo.delete(where={"jina": jina})

    def ondoa_yote(self):
        self.nyaraka = []
        self._hifadhi_kumbukumbu()
        ids = self.mizigo.get()["ids"]
        if ids:
            self.mizigo.delete(ids=ids)

    def tafuta(self, swali, k=4):
        idadi = self.mizigo.count()
        if not idadi:
            return []
        sw = embed.vipimo([swali])
        if not sw:
            return []
        res = self.mizigo.query(
            query_embeddings=sw, n_results=max(1, min(k, idadi)),
            include=["documents", "metadatas", "distances"])
        matokeo = []
        for maandishi, meta, umbali in zip(res["documents"][0],
                                           res["metadatas"][0],
                                           res["distances"][0]):
            alama = 1.0 - float(umbali)
            if alama <= 0:
                continue
            matokeo.append({
                "alama": round(alama, 4),
                "jina": meta["jina"],
                "namba": meta["namba"],
                "maandishi": maandishi,
            })
        return matokeo


def hifadhi_mpya(njia=None):
    """MJIBU_DB=auto (chroma kama ipo) | chroma | tfidf."""
    mchaguo = os.getenv("MJIBU_DB", "auto")
    if mchaguo in ("auto", "chroma") and njia is not None:
        try:
            return HifadhiChroma(njia)
        except Exception:
            if mchaguo == "chroma":
                raise
    return Hifadhi()
