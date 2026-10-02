import sqlite3

import pytest

import app as mod


@pytest.fixture
def client(tmp_path):
    mod.app.config["TESTING"] = True
    mod.app.config["DB"] = str(tmp_path / "test.db")
    mod.tengeneza_db()
    return mod.app.test_client()


def weka_csrf(client, tok="karatasi-maandishi"):
    with client.session_transaction() as s:
        s["csrf"] = tok
    return tok


def post(client, url, **data):
    data["_csrf"] = weka_csrf(client)
    return client.post(url, data=data, follow_redirects=True)


def ingia(client, jina="admin", nenosiri="benki123"):
    tok = weka_csrf(client)
    return client.post("/ingia", data={"jina": jina, "nenosiri": nenosiri,
                                       "_csrf": tok},
                       follow_redirects=True)


def ongeza_mkuu(client):
    return post(client, "/ongeza", jina="Test Mteja", simu="0712345678",
                kiasi="100000", riba="15", miezi="6", aina="reducing")


def test_mwanzo_landing_na_bila_kuingia(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"BENKI" in r.data
    assert b"Ingia kwenye akaunti" in r.data
    r = client.get("/ripoti")
    assert r.status_code == 302
    assert "/ingia" in r.headers["Location"]


def test_nenosiri_si_sahihi(client):
    r = ingia(client, nenosiri="mbovu")
    assert b"si sahihi" in r.data


def test_sql_injection_haiwezi_kuingia(client):
    r = ingia(client, jina="' OR 1=1 --", nenosiri="x")
    assert b"si sahihi" in r.data


def test_ingia_kwa_mafanikio(client):
    r = ingia(client)
    assert r.status_code == 200
    assert b"Orodha ya Mikopo" in r.data


def test_csrf_bila_token_inakataa(client):
    ingia(client)
    r = client.post("/ongeza", data={"jina": "Mtu", "simu": "07",
                                     "kiasi": "1000", "riba": "10",
                                     "miezi": "3", "aina": "flat"},
                    follow_redirects=True)
    assert b"CSRF" in r.data
    r = client.get("/")
    assert b"Mtu" not in r.data


def test_mpokeaji_haongezi_mikopo(client):
    ingia(client, jina="mpokeaji", nenosiri="pokea123")
    r = ongeza_mkuu(client)
    assert b"HUNA RUHUSA" in r.data
    assert b"admin" in r.data


def test_mhasibu_haoni_ripoti(client):
    ingia(client, jina="mhasibu", nenosiri="hesabu123")
    r = client.get("/ripoti")
    assert r.status_code == 200
    assert b"Ripoti ya Benki" in r.data
    r = client.get("/wateja")
    assert b"Orodha ya Wateja" in r.data


def test_badilisha_nenosiri(client):
    ingia(client)
    r = post(client, "/badilisha", zamani="mbovu", jipya="sifuri123",
             rudia="sifuri123")
    assert b"zamani si sahihi" in r.data
    r = post(client, "/badilisha", zamani="benki123", jipya="sifuri123",
             rudia="tofauti")
    assert b"halilingani" in r.data
    r = post(client, "/badilisha", zamani="benki123", jipya="sifuri123",
             rudia="sifuri123")
    assert b"mafanikio" in r.data
    client.get("/toka")
    r = ingia(client, nenosiri="sifuri123")
    assert b"Orodha ya Mikopo" in r.data


def test_ongeza_mkopo_na_kuonekana(client):
    ingia(client)
    r = ongeza_mkuu(client)
    assert r.status_code == 200
    assert b"Test Mteja" in r.data
    assert b"umehifadhiwa" in r.data


def test_kiasi_hasi_imekataa(client):
    ingia(client)
    r = post(client, "/ongeza", jina="Mtu", simu="07", kiasi="-5000",
             riba="15", miezi="6", aina="flat")
    assert b"zaidi ya 0" in r.data


def test_lipa_na_trigger(client):
    ingia(client)
    post(client, "/ongeza", jina="Lipa Mtu", simu="0799999999",
         kiasi="500000", riba="20", miezi="10", aina="flat")
    r = post(client, "/mkopo/1/lipa", kiasi="100000", njia="m-pesa")
    assert b"pokelewa" in r.data
    r = post(client, "/mkopo/1/lipa", kiasi="999999999", njia="fedha")
    assert b"kubwa kuliko deni" in r.data


def test_mhasibu_halipi_malipo(client):
    ingia(client, jina="mhasibu", nenosiri="hesabu123")
    r = post(client, "/mkopo/1/lipa", kiasi="50000", njia="fedha")
    assert b"HUNA RUHUSA" in r.data


def test_futa_mteja_restRICT_na_cascade(client):
    ingia(client)
    ongeza_mkuu(client)
    r = post(client, "/wateja/1/futa")
    assert b"RESTRICT" in r.data
    r = post(client, "/mkopo/1/lipa", kiasi="10000", njia="fedha")
    assert b"pokelewa" in r.data
    db = sqlite3.connect(mod.app.config["DB"])
    n = db.execute("SELECT COUNT(*) FROM malipo").fetchone()[0]
    assert n == 1
    r = post(client, "/mkopo/1/futa")
    assert b"CASCADE" in r.data
    n = db.execute("SELECT COUNT(*) FROM malipo").fetchone()[0]
    assert n == 0
    r = post(client, "/wateja/1/futa")
    assert b"amefutwa" in r.data
    db.close()


def test_ripoti_na_kumbukumbu(client):
    ingia(client)
    post(client, "/ongeza", jina="Ripoti Mtu", simu="0788888888",
         kiasi="300000", riba="10", miezi="5", aina="flat")
    post(client, "/mkopo/1/lipa", kiasi="50000", njia="fedha")
    r = client.get("/ripoti")
    assert b"Ripoti ya Benki" in r.data
    assert b"300,000" in r.data
    db = sqlite3.connect(mod.app.config["DB"])
    n = db.execute("SELECT COUNT(*) FROM kumbukumbu_za_malipo").fetchone()[0]
    assert n == 1
    db.close()
