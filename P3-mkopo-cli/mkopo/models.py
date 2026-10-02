AINA_ZINAZORUHUSIWA = ("flat", "reducing")


def thibitisha_kiasi(kiasi):
    try:
        kiasi = float(kiasi)
    except (TypeError, ValueError):
        raise ValueError("Kiasi si namba sahihi: %r" % (kiasi,))
    if kiasi <= 0:
        raise ValueError("Kiasi lazima liwe zaidi ya 0 (umeingiza: %s)" % kiasi)
    return kiasi


def thibitisha_riba(riba):
    try:
        riba = float(riba)
    except (TypeError, ValueError):
        raise ValueError("Riba si namba sahihi: %r" % (riba,))
    if riba < 0 or riba > 100:
        raise ValueError("Riba lazima iwe kati ya 0 na 100 (umeingiza: %s)" % riba)
    return riba


def thibitisha_miezi(miezi):
    try:
        miezi = int(miezi)
    except (TypeError, ValueError):
        raise ValueError("Miezi si namba sahihi: %r" % (miezi,))
    if miezi < 1 or miezi > 360:
        raise ValueError("Miezi lazima iwe kati ya 1 na 360 (umeingiza: %s)" % miezi)
    return miezi


def thibitisha_aina(aina):
    aina = str(aina).lower().strip()
    if aina not in AINA_ZINAZORUHUSIWA:
        raise ValueError("Aina isiyojulikana: %s (tumia: flat au reducing)" % aina)
    return aina


def thibitisha_jina(jina):
    if not isinstance(jina, str) or not jina.strip():
        raise ValueError("Jina halikubaliwi kuwa tupu")
    return jina.strip()


class Mteja:
    def __init__(self, jina, simu=""):
        self.jina = thibitisha_jina(jina)
        self.simu = str(simu).strip()

    def __repr__(self):
        return "Mteja(%r, %r)" % (self.jina, self.simu)


class Mkopo:
    def __init__(self, kiasi, riba, miezi, aina="reducing", mteja_id=None):
        self.kiasi = thibitisha_kiasi(kiasi)
        self.riba = thibitisha_riba(riba)
        self.miezi = thibitisha_miezi(miezi)
        self.aina = thibitisha_aina(aina)
        self.mteja_id = mteja_id

    def __repr__(self):
        return "Mkopo(%s, %s%%, %s miezi, %s)" % (
            self.kiasi, self.riba, self.miezi, self.aina)
