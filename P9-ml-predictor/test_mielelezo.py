import os
import time

import pytest

import mielelezo as m


@pytest.fixture(scope="module")
def gui():
    from tkinter import TclError
    import mielelezo_gui
    app = None
    for jaribu in range(3):
        try:
            app = mielelezo_gui.MielelezoGUI()
            break
        except TclError:
            if jaribu == 2:
                raise
            time.sleep(0.3)
    yield app
    app.destroy()


@pytest.fixture
def model(tmp_path, monkeypatch):
    njia = str(tmp_path / "model.pkl")
    monkeypatch.setattr(m, "MODEL", njia)
    m.fundisha()
    return njia


def test_data_safi():
    u, l = m.pakua_data()
    assert len(u) >= 60
    assert set(l) == {"spam", "ham"}
    assert all(u) and all(l)


def test_fundisha_usahihi(model):
    d = m.fundisha()
    assert 0.75 <= d["usahihi"] <= 1.0
    assert d["jumla"] == 74
    assert os.path.exists(model)
    assert "spam" in d["ripoti"]


def test_tabiri_spam(model):
    r = m.angalia("Umeshinda Tsh 5,000,000 tuma namba ya siri sasa")
    assert r["aina"] == "spam"
    assert r["uwezo"] > 50


def test_tabiri_ham(model):
    r = m.angalia("Habari ya asubuhi umefika salama")
    assert r["aina"] == "ham"


def test_pickle_mzunguko(model, tmp_path):
    r1 = m.angalia("Congratulations you won send bank details")
    mchoro = m.pakua_model()
    with open(model, "rb") as f:
        import pickle
        mchoro2 = pickle.load(f)
    assert mchoro2.predict(["x"]).tolist() is not None
    r2 = m.angalia("Congratulations you won send bank details")
    assert r1 == r2


def test_model_haipo(tmp_path):
    with pytest.raises(FileNotFoundError):
        m.angalia("x", model_njia=str(tmp_path / "haipo.pkl"))


def test_cli_fundisha_angalia(capsys):
    assert m.main(["fundisha"]) == 0
    out = capsys.readouterr().out
    assert "IMEFUNDISHWA" in out
    assert m.main(["angalia", "Umeshinda zawadi tuma namba ya siri"]) == 0
    assert "SPAM" in capsys.readouterr().out


def test_cli_thibitisha(capsys):
    m.fundisha()
    assert m.main(["thibitisha"]) == 0
    out = capsys.readouterr().out
    assert "Usahihi" in out


def test_cli_bila_model(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(m, "MODEL", str(tmp_path / "haipo.pkl"))
    assert m.main(["angalia", "habari"]) == 1
    assert "fundisha" in capsys.readouterr().out


def test_gui_inafunguka(gui):
    gui.update_idletasks()
    assert "Mielelezo" in gui.title()


def test_gui_tabiri_spam(gui, tmp_path, monkeypatch):
    monkeypatch.setattr(m, "MODEL", str(tmp_path / "m.pkl"))
    m.fundisha()
    gui.t_ndani.delete("1.0", "end")
    gui.t_ndani.insert("1.0",
                       "Umeshinda Tsh 5,000,000 tuma namba ya siri")
    gui.tabiri()
    assert gui.t_alama.cget("text") == "SPAM"


def test_gui_bila_model(gui, tmp_path, monkeypatch):
    monkeypatch.setattr(m, "MODEL", str(tmp_path / "haipo.pkl"))
    gui.t_ndani.delete("1.0", "end")
    gui.t_ndani.insert("1.0", "habari")
    gui.tabiri()
    assert "Fundisha" in gui.t_maelezo.cget("text")
