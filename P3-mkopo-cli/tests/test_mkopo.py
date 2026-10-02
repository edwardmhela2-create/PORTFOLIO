import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from mkopo import db
from mkopo.amortization import hesabu
from mkopo.models import Mteja, Mkopo


def test_flat_hesabu_kama_mkono():
    m = hesabu("flat", 1000000, 20, 12)
    assert m["riba_ya_jumla"] == pytest.approx(
        1000000 * 20 / 100 * (12 / 12))
    assert m["jumla"] == pytest.approx(1200000)
    assert m["malipo_mwezi"] == pytest.approx(100000)
    assert m["jedwali"][-1]["salio"] == 0
    jumla_ya_malipo = sum(r["malipo"] for r in m["jedwali"])
    assert jumla_ya_malipo == pytest.approx(1200000)


def test_reducing_inaishia_salio_sifuri():
    m = hesabu("reducing", 1000000, 24, 12)
    assert len(m["jedwali"]) == 12
    assert m["jedwali"][-1]["salio"] == 0
    jumla_ya_malipo = sum(r["malipo"] for r in m["jedwali"])
    assert jumla_ya_malipo == pytest.approx(m["kiasi"] + m["riba_ya_jumla"])
    assert m["riba_ya_jumla"] < 1000000 * 24 / 100


def test_reducing_riba_sifuri():
    m = hesabu("reducing", 600000, 0, 6)
    assert m["malipo_mwezi"] == pytest.approx(100000)
    assert m["riba_ya_jumla"] == 0
    assert m["jedwali"][-1]["salio"] == 0


def test_validation_inakatali_mabaya():
    with pytest.raises(ValueError):
        hesabu("reducing", -5, 10, 12)
    with pytest.raises(ValueError):
        hesabu("flat", 1000000, 10, 0)
    with pytest.raises(ValueError):
        hesabu("flat", 1000000, 101, 12)
    with pytest.raises(ValueError):
        hesabu("mbaya", 1000000, 10, 12)
    with pytest.raises(ValueError):
        Mteja("   ")
    with pytest.raises(ValueError):
        Mkopo("abc", 10, 12)


def test_db_mzunguko(tmp_path):
    p = str(tmp_path / "jaribio.db")
    db.tengeneza(p)
    mteja_id = db.hifadhi_mteja("Juma", "0712345678", p)
    assert mteja_id > 0
    kopo_id = db.hifadhi_mkopo(mteja_id, 500000, 18, 6, "flat", p)
    rows = db.orodha_mikopo(p)
    assert len(rows) == 1
    assert rows[0]["id"] == kopo_id
    assert db.futa_mkopo(kopo_id, p) is True
    assert db.orodha_mikopo(p) == []
    assert db.futa_mkopo(kopo_id, p) is False


def test_db_join_na_hifadhi_maradufu(tmp_path):
    p = str(tmp_path / "join.db")
    db.tengeneza(p)
    a = db.hifadhi_mteja("Asha", "", p)
    b = db.hifadhi_mteja("Asha", "", p)
    assert a == b
    db.hifadhi_mkopo(a, 2000000, 20, 12, "reducing", p)
    rows = db.orodha_mikopo(p)
    assert rows[0]["mteja"] == "Asha"


def test_db_mteja_haipo(tmp_path):
    p = str(tmp_path / "tatu.db")
    db.tengeneza(p)
    with pytest.raises(ValueError):
        db.hifadhi_mkopo(99, 100000, 10, 6, "flat", p)


def test_ripoti_jumla(tmp_path):
    p = str(tmp_path / "ripoti.db")
    db.tengeneza(p)
    m1 = db.hifadhi_mteja("Chiku", "", p)
    m2 = db.hifadhi_mteja("Devota", "", p)
    db.hifadhi_mkopo(m1, 1000000, 10, 12, "reducing", p)
    db.hifadhi_mkopo(m1, 500000, 10, 6, "flat", p)
    db.hifadhi_mkopo(m2, 700000, 10, 12, "reducing", p)
    r = db.ripoti(p)
    assert r["idadi"] == 3
    assert r["jumla_kiasi"] == 2200000
    assert r["kwa_mteja"][0]["jina"] == "Chiku"
    assert r["kwa_mteja"][0]["kiasi"] == 1500000


def _jaza(path):
    db.tengeneza(path)
    a = db.hifadhi_mteja("Asha", "", path)
    b = db.hifadhi_mteja("Asha Nyeusi", "", path)
    c = db.hifadhi_mteja("Baraka", "", path)
    db.hifadhi_mkopo(a, 1000000, 10, 12, "reducing", path)
    db.hifadhi_mkopo(a, 500000, 10, 6, "flat", path)
    db.hifadhi_mkopo(b, 700000, 10, 12, "reducing", path)
    return a, b, c


def test_nani_kakopa_zaidi(tmp_path):
    p = str(tmp_path / "ranking.db")
    _jaza(p)
    rows = db.nani_kakopa_zaidi(p)
    assert rows[0]["jina"] == "Asha"
    assert rows[0]["jumla"] == 1500000
    assert len(rows) == 2


def test_jumla_kwa_aina(tmp_path):
    p = str(tmp_path / "aina.db")
    _jaza(p)
    rows = db.jumla_kwa_aina(p)
    kwa_aina = {r["aina"]: r for r in rows}
    assert kwa_aina["flat"]["idadi"] == 1
    assert kwa_aina["reducing"]["idadi"] == 2
    assert kwa_aina["flat"]["jumla"] == 500000


def test_takwimu(tmp_path):
    p = str(tmp_path / "takwimu.db")
    _jaza(p)
    t = db.takwimu(p)
    assert t["idadi"] == 3
    assert t["kubwa"] == 1000000
    assert t["ndogo"] == 500000
    assert t["wastani_kiasi"] == pytest.approx(2200000 / 3)


def test_wateja_bila_mikopo(tmp_path):
    p = str(tmp_path / "bila.db")
    _, _, c = _jaza(p)
    rows = db.wateja_bila_mikopo(p)
    assert len(rows) == 1
    assert rows[0]["jina"] == "Baraka"


def test_tafuta_jina(tmp_path):
    p = str(tmp_path / "tafuta.db")
    _jaza(p)
    rows = db.tafuta_jina("ash", p)
    assert len(rows) == 3
    assert db.tafuta_jina("cho", p) == []
    with pytest.raises(ValueError):
        db.tafuta_jina("   ", p)


def test_mikopo_yanayokaribia_kuisha(tmp_path):
    p = str(tmp_path / "kuisha.db")
    _, b, _ = _jaza(p)
    with db.fungua(p) as conn:
        conn.execute(
            "UPDATE mikopo SET tangu = date('now', '-10 months') "
            "WHERE mteja_id = ?", (b,))
    rows = db.mikopo_yanayokaribia_kuisha(3, p)
    assert len(rows) == 1
    assert rows[0]["mteja"] == "Asha Nyeusi"
    assert rows[0]["yaliyobaki"] == 2
    with pytest.raises(ValueError):
        db.mikopo_yanayokaribia_kuisha(-1, p)


def test_badilisha_update(tmp_path):
    p = str(tmp_path / "badili.db")
    _, b, _ = _jaza(p)
    kidogo = db.orodha_mikopo(p)
    id_b = [r["id"] for r in kidogo if r["mteja"] == "Asha Nyeusi"][0]
    db.badilisha_mkopo(id_b, p, riba=30, miezi=9)
    baada = db.pata_mkopo(id_b, p)
    assert baada["riba"] == 30
    assert baada["miezi"] == 9
    assert baada["kiasi"] == 700000
    with pytest.raises(ValueError):
        db.badilisha_mkopo(id_b, p)
    with pytest.raises(ValueError):
        db.badilisha_mkopo(id_b, p, riba=150)
    with pytest.raises(ValueError):
        db.badilisha_mkopo(99, p, riba=10)


def test_badilisha_jina_la_mteja(tmp_path):
    p = str(tmp_path / "jina.db")
    a, _, _ = _jaza(p)
    kidogo = db.orodha_mikopo(p)
    id_a = [r["id"] for r in kidogo if r["mteja"] == "Asha"][0]
    db.badilisha_mkopo(id_a, p, jina="Asha Hassan", simu="0755000111")
    rows = db.orodha_mikopo(p)
    mechi = [r for r in rows if r["id"] == id_a]
    assert mechi[0]["mteja"] == "Asha Hassan"
    w = [x for x in db.orodha_wateja(p) if x["id"] == a][0]
    assert w["simu"] == "0755000111"


def test_hamisha_csv(tmp_path):
    p = str(tmp_path / "asilia.db")
    _jaza(p)
    faili = str(tmp_path / "nje.csv")
    n = db.hamisha_mikopo_csv(faili, p)
    assert n == 3
    maandishi = open(faili, encoding="utf-8-sig").read()
    mistari = maandishi.strip().splitlines()
    assert len(mistari) == 4
    assert "mteja" in mistari[0]
    assert "Asha" in maandishi


def test_kumbuka_logs(tmp_path, monkeypatch):
    logi = str(tmp_path / "logs.csv")
    monkeypatch.setattr(db, "LOG_FILE", logi)
    db.kumbuka("ongeza", "mkopo id=1 kwa Asha")
    db.kumbuka("futa", "mkopo id=1 umefutwa")
    rows = db.soma_kumbuka()
    assert rows[0] == ["wakati", "amri", "maelezo"]
    assert len(rows) == 3
    assert rows[1][1] == "ongeza"
    assert "umefutwa" in rows[2][2]
