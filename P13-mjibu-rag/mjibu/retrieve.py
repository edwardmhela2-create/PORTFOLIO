from sklearn.feature_extraction.text import TfidfVectorizer


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
