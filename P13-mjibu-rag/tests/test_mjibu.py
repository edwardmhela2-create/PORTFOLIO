from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from mjibu import app as app_mod
from mjibu import llm
from mjibu.ingest import gawanya, tengeneza_nyaraka
from mjibu.prompts import MSAIDIZI, jenga_muktadha
from mjibu.retrieve import Hifadhi


@pytest.fixture
def huduma(monkeypatch, tmp_path):
    monkeypatch.setenv("MJIBU_LOAD", "0")
    monkeypatch.setattr(app_mod, "DATA", tmp_path / "nyaraka")
    app_mod.hifadhi.ondoa_yote()
    with TestClient(app_mod.app) as m:
        yield m
    app_mod.hifadhi.ondoa_yote()


def _pakia(huduma, jina, maandishi):
    return huduma.post(
        "/api/pakia",
        files={"faili": (jina, maandishi.encode("utf-8"))})


class TestChunking:

    def test_gawanya_ukubwa_na_ukingo(self):
        mk = "neno " * 400
        v = gawanya(mk, ukubwa=200, hatua=150)
        assert v
        assert all(len(x) <= 200 for x in v)
        assert v[0][:50] == v[1][:50]

    def test_gawanya_tupu_na_mstari_mrefu(self):
        assert gawanya("") == []
        assert gawanya("   \n\n  ") == []
        v = gawanya("habari yako")
        assert v == ["habari yako"]

    def test_gawanya_huondoa_mstari_mrefu_wasiolazimu(self):
        v = gawanya("habari\n\n\n\n\nnzuri")
        assert "\n\n\n" not in v[0]

    def test_tengeneza_nyaraka_kutoka_md(self, tmp_path):
        f = tmp_path / "jaribio.md"
        f.write_text("# Habari\nMaudhui ya jaribio.",
                     encoding="utf-8")
        ny = tengeneza_nyaraka(f)
        assert ny["jina"] == "jaribio.md"
        assert len(ny["vipande"]) >= 1
        assert "Maudhui" in ny["vipande"][0]


class TestHifadhi:

    def test_tafuta_hurudisha_nyaraka_sahihi(self):
        h = Hifadhi()
        h.ongeza({"jina": "firewall.md",
                  "vipande": ["Firewall huzuia milango isiyo "
                              "ya kuruhusiwa kufunguliwa"],
                  "herufi": 60})
        h.ongeza({"jina": "dushi.md",
                  "vipande": ["Dushi la maji linaweza kuharibu "
                              "kompyuta"],
                  "herufi": 50})
        m = h.tafuta("firewall huzuia milango")
        assert m[0]["jina"] == "firewall.md"
        assert m[0]["alama"] > 0

    def test_tafuta_bila_nyaraka_yoyote(self):
        assert Hifadhi().tafuta("lolote") == []

    def test_tafuta_hakuna_muingiliano(self):
        h = Hifadhi()
        h.ongeza({"jina": "a.md", "vipande": ["mchele viazi sukari"],
                  "herufi": 19})
        assert h.tafuta("blockchain bitcoin ethereum") == []

    def test_ondoa_nyaraka_hurejesha_index(self):
        h = Hifadhi()
        h.ongeza({"jina": "a.md", "vipande": ["talanta"], "herufi": 7})
        h.ongeza({"jina": "b.md", "vipande": ["mipango"], "herufi": 7})
        h.ondoa("a.md")
        assert [n["jina"] for n in h.nyaraka] == ["b.md"]
        m = h.tafuta("mipango ya kazi")
        assert m and m[0]["jina"] == "b.md"


class TestAPI:

    def test_pakia_nyaraka_txt_na_orodha(self, huduma):
        r = _pakia(huduma, "jaribio.txt",
                   "Nyaraka hii inazungumzia firewall na port scan.")
        assert r.status_code == 200
        assert r.json()["vipande"] >= 1
        orodha = huduma.get("/api/nyaraka").json()
        assert any(n["jina"] == "jaribio.txt" for n in orodha)

    def test_pakia_aina_haiyokubalika(self, huduma):
        r = _pakia(huduma, "programu.exe", "binary")
        assert r.status_code == 400

    def test_futa_nyaraka(self, huduma):
        _pakia(huduma, "ondoa.md", "maudhui ya kufutwa")
        r = huduma.delete("/api/nyaraka/ondoa.md")
        assert r.status_code == 200
        assert huduma.delete("/api/nyaraka/ondoa.md").status_code == 404

    def test_swali_bila_muktadha(self, huduma):
        r = huduma.post("/api/swali", json={"swali": "nini hili?"})
        assert r.status_code == 200
        assert r.json()["hali"] == "hakuna_muktadha"

    def test_swali_bila_kipengele(self, huduma):
        assert huduma.post("/api/swali", json={}).status_code == 422
        assert huduma.post(
            "/api/swali",
            json={"swali": ""}).status_code == 422

    def test_swali_na_llm_yaliyofananishwa(self, huduma, monkeypatch):
        yaliyopokelewa = {}

        def lmfano(swali, muktadha, muda=90):
            yaliyopokelewa["s"] = swali
            yaliyopokelewa["m"] = muktadha
            return "Jibu: 94.7% [1]"

        monkeypatch.setattr(app_mod.llm, "jibu", lmfano)
        _pakia(huduma, "ml.md",
               "Mielelezo ilifikia asilimia 94.7 ya usahihi.")
        r = huduma.post("/api/swali",
                        json={"swali": "Mielelezo ilifikia asilimia ngapi?"})
        data = r.json()
        assert data["hali"] == "ok"
        assert "94.7%" in data["jibu"]
        assert data["vyanzo"][0]["jina"] == "ml.md"
        assert "94.7" in yaliyopokelewa["m"]
        assert "Kanuni ngumu" in yaliyopokelewa["m"]

    def test_swali_llm_haipatikani(self, huduma, monkeypatch):
        monkeypatch.setattr(app_mod.llm, "jibu",
                            lambda *a, **k: None)
        _pakia(huduma, "x.md", "firewall ni lango la usalama")
        r = huduma.post("/api/swali", json={"swali": "firewall?"})
        assert r.json()["hali"] == "llm_hai"
        assert r.json()["vyanzo"]


class TestPromptNaLLM:

    def test_muktadha_una_kanuni_na_vyanzo(self):
        m = jenga_muktadha([
            {"alama": 0.91, "jina": "a.md", "namba": 3,
             "maandishi": "maneno muhimu"}])
        assert "[1] a.md" in m
        assert "Sijui" in m
        assert MSAIDIZI in m

    def test_llm_harudi_none_mtandao_haupo(self, monkeypatch):
        monkeypatch.setenv("MJIBU_OLLAMA_URL", "http://127.0.0.1:9")
        assert llm.jibu("swali", "muktadha", muda=1) is None

    def test_pakia_yote_husoma_kwenye_start(self, huduma):
        d = app_mod.DATA
        d.mkdir(parents=True, exist_ok=True)
        (d / "asili.md").write_text(
            "firewall ni lango la usalama", encoding="utf-8")
        app_mod.pakia_yote()
        assert [n["jina"] for n in
                app_mod.hifadhi.nyaraka] == ["asili.md"]
