import pytest

import cyber


def test_hash_thabiti():
    a = cyber.hesabu_hash(b"habari")
    b = cyber.hesabu_hash(b"habari")
    assert a == b
    assert len(a) == 64
    assert cyber.hesabu_hash(b"habari2") != a


def test_hash_file(tmp_path):
    f = tmp_path / "nakala.txt"
    f.write_bytes(b"habari")
    assert cyber.hash_file(str(f)) == cyber.hesabu_hash(b"habari")


def test_siri_mzunguko():
    doa = cyber.siri_mandishi("UJUMBE WANGU WA SIRI", "funguo123")
    assert doa != "UJUMBE WANGU WA SIRI"
    assert cyber.fungua_mandishi(doa, "funguo123") == "UJUMBE WANGU WA SIRI"


def test_siri_funguo_mbovu():
    doa = cyber.siri_mandishi("habari", "sahihi")
    with pytest.raises(ValueError):
        cyber.fungua_mandishi(doa, "mbovu")


def test_siri_si_base64():
    with pytest.raises(ValueError):
        cyber.fungua_mandishi("siyo!!!base64", "k")


def test_tengeneza_imara():
    neno = cyber.tengeneza_nenosiri(16)
    assert len(neno) == 16
    assert any(c.isupper() for c in neno)
    assert any(c.islower() for c in neno)
    assert any(c.isdigit() for c in neno)
    assert any(not c.isalnum() for c in neno)
    assert cyber.tengeneza_nenosiri(16) != neno
    with pytest.raises(ValueError):
        cyber.tengeneza_nenosiri(2)


def test_imarisha_mbovu():
    s = cyber.imarisha_nenosiri("123456")
    assert s["hukumu"].startswith("MBOVU")
    assert s["alama"] == 0


def test_imarisha_imara():
    s = cyber.imarisha_nenosiri("Tr0ub4dor&3XYZ")
    assert s["alama"] >= 5
    assert s["hukumu"] in ("WASTANI", "IMARA")
    assert s["entropy"] > 50


def test_ip_chambua():
    assert cyber.ip_funguo("192.168.118.10")["private"] is True
    assert cyber.ip_funguo("127.0.0.1")["loopback"] is True
    assert cyber.ip_funguo("8.8.8.8")["global"] is True
    with pytest.raises(ValueError):
        cyber.ip_funguo("siyo-ip")


def test_ports_huona_iliyofunguliwa():
    s = cyber.anzia_soketi()
    port = s.getsockname()[1]
    wazi = cyber.chunguza_ports("127.0.0.1", [port, 1], muda=0.4)
    s.close()
    assert port in wazi
    assert 1 not in wazi


def test_cli_hash(capsys):
    assert cyber.main(["hash", "habari"]) == 0
    out = capsys.readouterr().out
    assert len(out.splitlines()[0]) == 64


def test_cli_thibitisha_1():
    h = cyber.hesabu_hash(b"habari")
    assert cyber.main(["hash", "habari", "--thibitisha", h]) == 0
    assert cyber.main(["hash", "habari", "--thibitisha", "0" * 64]) == 1


def test_ripoti_html(tmp_path):
    s = cyber.anzia_soketi()
    port = s.getsockname()[1]
    wazi = cyber.chunguza_ports("127.0.0.1", [port], 0.4)
    s.close()
    njia = tmp_path / "ripoti.html"
    cyber.andika_ripoti("127.0.0.1", wazi, [port, 1], str(njia))
    m = njia.read_text(encoding="utf-8")
    assert str(port) in m
    assert "WAZI" in m
    assert "127.0.0.1" in m
    assert "ETHICS" in m
    assert "Hakuna port" not in m


def test_cli_ripoti(tmp_path):
    njia = tmp_path / "r.html"
    assert cyber.main(["ripoti", "127.0.0.1", "--a", "1",
                       "--muda", "0.3", "-o", str(njia)]) == 0
    assert njia.exists()
    assert "127.0.0.1" in njia.read_text(encoding="utf-8")


def test_menyu(capsys, monkeypatch):
    chaguo = iter(["4", "123456", "6", "", "0"])
    monkeypatch.setattr("builtins.input", lambda p="": next(chaguo))
    assert cyber.main(["menyu"]) == 0
    out = capsys.readouterr().out
    assert "MBOVU" in out
    assert "PRIVATE" in out
    assert "Kwaheri" in out
