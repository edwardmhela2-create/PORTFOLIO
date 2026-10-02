from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from mjibu import app as app_mod
from mjibu import embed, llm
from mjibu.ingest import gawanya, tengeneza_nyaraka
from mjibu.prompts import MSAIDIZI, jenga_muktadha
from mjibu.retrieve import Hifadhi, HifadhiChroma, hifadhi_mpya


@pytest.fixture
def huduma(monkeypatch, tmp_path):
    monkeypatch.setenv("MJIBU_LOAD", "0")
    monkeypatch.setenv("MJIBU_EMBED", "hashing")
    monkeypatch.setenv("MJIBU_BACKEND", "ollama")
    monkeypatch.setenv("MJIBU_DB", "tfidf")
    monkeypatch.setattr(app_mod, "DATA", tmp_path / "nyaraka")
    monkeypatch.setattr(app_mod, "hifadhi",
                        hifadhi_mpya(tmp_path / "hifadhi"))
    with TestClient(app_mod.app) as m:
        yield m


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


class TestVipimoVipya:

    def test_embed_hashing_thabiti_na_ukubwa(self, monkeypatch):
        monkeypatch.setenv("MJIBU_EMBED", "hashing")
        a = embed.vipimo(["habari yako"])
        b = embed.vipimo(["habari yako"])
        c = embed.vipimo(["tofauti kabisa"])
        assert a == b
        assert a[0] != c[0]
        assert len(a[0]) == 512

    def test_embed_ollama_hushindwa_kuanguka_hashing(self, monkeypatch):
        monkeypatch.setenv("MJIBU_EMBED", "auto")
        monkeypatch.setattr(embed, "_ollama", lambda m: None)
        monkeypatch.setattr(embed, "_hali", {"ollama_imeshindwa": False})
        v = embed.vipimo(["neno"])
        assert v and len(v[0]) == 512

    def test_embed_ollama_wajibu_na_kushindwa(self, monkeypatch):
        monkeypatch.setenv("MJIBU_EMBED", "ollama")
        monkeypatch.setattr(embed, "_ollama", lambda m: None)
        monkeypatch.setattr(embed, "_hali", {"ollama_imeshindwa": False})
        assert embed.vipimo(["neno"]) is None

    def test_chroma_tafuta_na_ondoa(self, tmp_path, monkeypatch):
        monkeypatch.setenv("MJIBU_EMBED", "hashing")
        h = HifadhiChroma(tmp_path / "ch")
        h.ongeza({"jina": "firewall.md",
                  "vipande": ["Firewall huzuia milango isiyo ya "
                              "kuruhusiwa kufunguliwa"],
                  "herufi": 60})
        h.ongeza({"jina": "dushi.md",
                  "vipande": ["Dushi la maji linaweza kuharibu kompyuta"],
                  "herufi": 50})
        m = h.tafuta("firewall huzuia milango")
        assert m and m[0]["jina"] == "firewall.md"
        assert m[0]["alama"] > 0
        h.ondoa("firewall.md")
        m2 = h.tafuta("firewall huzuia milango")
        assert all(x["jina"] != "firewall.md" for x in m2)

    def test_chroma_hudhurupio_kwa_kufungua_upya(self, tmp_path, monkeypatch):
        monkeypatch.setenv("MJIBU_EMBED", "hashing")
        njia = tmp_path / "ch2"
        h = HifadhiChroma(njia)
        h.ongeza({"jina": "a.md", "vipande": ["mipango ya kazi na shughuli"],
                  "herufi": 26})
        h2 = HifadhiChroma(njia)
        assert [n["jina"] for n in h2.nyaraka] == ["a.md"]
        m = h2.tafuta("mipango ya kazi")
        assert m and m[0]["jina"] == "a.md"
        h2.ondoa_yote()
        assert HifadhiChroma(njia).tafuta("mipango ya kazi") == []

    def test_kiunganisho_mbadala_mizunguko(self, tmp_path, monkeypatch):
        monkeypatch.setenv("MJIBU_DB", "tfidf")
        assert isinstance(hifadhi_mpya(tmp_path / "x"), Hifadhi)
        monkeypatch.setenv("MJIBU_DB", "chroma")
        monkeypatch.setenv("MJIBU_EMBED", "hashing")
        assert isinstance(hifadhi_mpya(tmp_path / "y"), HifadhiChroma)

    def test_swali_kupitia_chroma_api(self, monkeypatch, tmp_path):
        monkeypatch.setenv("MJIBU_LOAD", "0")
        monkeypatch.setenv("MJIBU_EMBED", "hashing")
        monkeypatch.setattr(app_mod, "DATA", tmp_path / "nyaraka")
        monkeypatch.setattr(app_mod, "hifadhi",
                            HifadhiChroma(tmp_path / "ch"))
        monkeypatch.setattr(app_mod.llm, "jibu",
                            lambda *a, **k: "Jibu: 94.7% [1]")
        with TestClient(app_mod.app) as huduma:
            _pakia(huduma, "ml.md",
                   "Mielelezo ilifikia asilimia 94.7 ya usahihi.")
            r = huduma.post(
                "/api/swali",
                json={"swali": "Mielelezo ilifikia asilimia ngapi?"})
        data = r.json()
        assert data["hali"] == "ok"
        assert data["vyanzo"][0]["jina"] == "ml.md"

    def test_ombizo_haijapiga_mtandao_hashing(self, monkeypatch):
        monkeypatch.setenv("MJIBU_EMBED", "hashing")
        monkeypatch.setattr(embed.httpx, "post",
                            lambda *a, **k: pytest.fail("hapaswi kupiga"))
        assert embed.vipimo(["neno lolote"])


class TestLLMMbadala:

    def test_wingu_openai_payload_na_jibu(self, monkeypatch):
        yaliyotumwa = {}

        class M:
            def raise_for_status(self):
                pass

            def json(self):
                return {"choices": [{"message": {
                    "content": "Jibu la wingu [1]"}}]}

        def piga(url, **kw):
            yaliyotumwa["url"] = url
            yaliyotumwa.update(kw)
            return M()

        monkeypatch.setenv("MJIBU_BACKEND", "openai")
        monkeypatch.setenv("MJIBU_OPENAI_API_KEY", "siri-123")
        monkeypatch.setattr(llm.httpx, "post", piga)
        assert llm.jibu("swali", "muktadha") == "Jibu la wingu [1]"
        assert yaliyotumwa["url"].endswith("/chat/completions")
        assert yaliyotumwa["headers"]["Authorization"] == "Bearer siri-123"
        assert yaliyotumwa["json"]["temperature"] == 0.1

    def test_wingu_bila_ufunguo_harudi_none(self, monkeypatch):
        monkeypatch.setenv("MJIBU_BACKEND", "openai")
        monkeypatch.delenv("MJIBU_OPENAI_API_KEY", raising=False)
        monkeypatch.setattr(llm.httpx, "post",
                            lambda *a, **k: pytest.fail("hapaswi kupiga"))
        assert llm.jibu("s", "m") is None
        assert "API ya wingu" in llm.maelezo()

    def test_maelezo_hubadilika_kulingana_na_backend(self, monkeypatch):
        monkeypatch.setenv("MJIBU_BACKEND", "ollama")
        assert "Ollama" in llm.maelezo()
        monkeypatch.setenv("MJIBU_BACKEND", "openai")
        assert "wingu" in llm.maelezo()

    def test_paza_env_soma_dotenv(self, tmp_path, monkeypatch):
        import os
        f = tmp_path / ".env"
        f.write_text("MJIBU_MODEL=jaribio\n# maoni\nMJIBU_K=9\n",
                     encoding="utf-8")
        monkeypatch.delenv("MJIBU_MODEL", raising=False)
        monkeypatch.delenv("MJIBU_K", raising=False)
        app_mod._paza_env(f)
        assert os.environ["MJIBU_MODEL"] == "jaribio"
        assert os.environ["MJIBU_K"] == "9"
