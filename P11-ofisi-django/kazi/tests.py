from datetime import date

import pytest
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Barua, Kumbukumbu, Maombi


@pytest.fixture
def majukumu(db):
    for j in ["wafanyakazi", "meneja", "rejista"]:
        Group.objects.get_or_create(name=j)


def mtumiaji(jina, *majukumu):
    u = User.objects.create_user(username=jina, password="siri12345")
    for j in majukumu:
        u.groups.add(Group.objects.get(name=j))
    return u


def test_landing_na_ingia(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Ingia" in r.content.decode()


def test_maombi_hindikwa_bila_kuingia(client):
    r = client.get("/maombi/")
    assert r.status_code == 302
    assert "/ingia/" in r["Location"]


def test_mtumiaji_bila_kundi_403(client, majukumu):
    u = User.objects.create_user(username="mgeni", password="siri12345")
    client.force_login(u)
    assert client.get("/maombi/").status_code == 403


def test_mfanyakazi_aona_maombi(client, majukumu):
    u = mtumiaji("juma", "wafanyakazi")
    Maombi.objects.create(mhusika=u, aina="likizo",
                          maelezo="Likizo ya wiki 2")
    client.force_login(u)
    r = client.get("/maombi/")
    assert r.status_code == 200
    assert "Likizo" in r.content.decode()


def test_kuunda_maombi_mpya(client, majukumu):
    u = mtumiaji("juma", "wafanyakazi")
    client.force_login(u)
    r = client.post("/maombi/mpya/", {
        "aina": "fedha", "maelezo": "Ninahitaji fedha za basi"})
    assert r.status_code == 302
    m = Maombi.objects.get()
    assert m.mhusika == u
    assert m.hali == "rasimu"


def test_signal_huandika_kumbukumbu(db, majukumu):
    u = mtumiaji("juma", "wafanyakazi")
    Maombi.objects.create(mhusika=u, aina="likizo", maelezo="x")
    assert Kumbukumbu.objects.count() == 1
    assert "limeandikwa" in Kumbukumbu.objects.get().mada


def test_wasilisha_hubadilisha_hali(db, majukumu):
    u = mtumiaji("juma", "wafanyakazi")
    m = Maombi.objects.create(mhusika=u, aina="likizo", maelezo="x")
    m.wasilisha(u)
    m.refresh_from_db()
    assert m.hali == "imewasilishwa"
    assert m.imewasilishwa is not None
    assert Kumbukumbu.objects.count() == 2


def test_wasilisha_si_yangu_kushindwa(db, majukumu):
    mwenye = mtumiaji("juma", "wafanyakazi")
    mwingine = mtumiaji("reuss", "wafanyakazi")
    m = Maombi.objects.create(mhusika=mwenye, aina="likizo",
                              maelezo="x")
    with pytest.raises(ValidationError):
        m.wasilisha(mwingine)


def test_wasilisha_rasimu_tu(db, majukumu):
    u = mtumiaji("juma", "wafanyakazi")
    m = Maombi.objects.create(mhusika=u, aina="likizo", maelezo="x")
    m.wasilisha(u)
    with pytest.raises(ValidationError):
        m.wasilisha(u)


def test_kagua_idhini(client, majukumu):
    meneja = mtumiaji("neema", "meneja")
    juma = mtumiaji("juma", "wafanyakazi")
    m = Maombi.objects.create(mhusika=juma, aina="likizo",
                              maelezo="x")
    m.wasilisha(juma)
    client.force_login(meneja)
    r = client.post("/maombi/%d/kagua/" % m.pk,
                    {"amri": "idhini", "maoni": "Sawa kabisa"})
    assert r.status_code == 302
    m.refresh_from_db()
    assert m.hali == "imeidhinishwa"
    assert m.meneja == meneja
    assert Kumbukumbu.objects.count() == 3


def test_kagua_si_meneja_403(client, majukumu):
    juma = mtumiaji("juma", "wafanyakazi")
    m = Maombi.objects.create(mhusika=juma, aina="likizo",
                              maelezo="x")
    m.wasilisha(juma)
    client.force_login(juma)
    r = client.post("/maombi/%d/kagua/" % m.pk,
                    {"amri": "idhini", "maoni": ""})
    assert r.status_code == 403
    m.refresh_from_db()
    assert m.hali == "imewasilishwa"


def test_kataa_bila_maoni_kushindwa(db, majukumu):
    meneja = mtumiaji("neema", "meneja")
    juma = mtumiaji("juma", "wafanyakazi")
    m = Maombi.objects.create(mhusika=juma, aina="likizo",
                              maelezo="x")
    m.wasilisha(juma)
    with pytest.raises(ValidationError):
        m.kagua(meneja, idhini=False, maoni="  ")
    m.refresh_from_db()
    assert m.hali == "imewasilishwa"


def test_kagua_marumbili_kushindwa(db, majukumu):
    meneja = mtumiaji("neema", "meneja")
    juma = mtumiaji("juma", "wafanyakazi")
    m = Maombi.objects.create(mhusika=juma, aina="likizo",
                              maelezo="x")
    m.wasilisha(juma)
    m.kagua(meneja, idhini=True, maoni="sawa")
    with pytest.raises(ValidationError):
        m.kagua(meneja, idhini=False, maoni="badilisha")


def test_futa_rasimu(client, majukumu):
    juma = mtumiaji("juma", "wafanyakazi")
    m = Maombi.objects.create(mhusika=juma, aina="likizo",
                              maelezo="x")
    client.force_login(juma)
    r = client.post("/maombi/%d/futa/" % m.pk)
    assert r.status_code == 302
    assert not Maombi.objects.exists()


def test_pagination_10_kwa_ukurasa(client, majukumu):
    u = mtumiaji("juma", "wafanyakazi")
    for i in range(12):
        Maombi.objects.create(mhusika=u, aina="likizo",
                              maelezo="ombi %d" % i)
    client.force_login(u)
    r1 = client.get("/maombi/")
    assert len(r1.context["maombi"]) == 10
    r2 = client.get("/maombi/?page=2")
    assert len(r2.context["maombi"]) == 2


def test_ripoti_na_csv(client, majukumu):
    meneja = mtumiaji("neema", "meneja")
    juma = mtumiaji("juma", "wafanyakazi")
    Maombi.objects.create(mhusika=juma, aina="likizo", maelezo="x")
    client.force_login(meneja)
    r = client.get("/ripoti/")
    assert r.status_code == 200
    assert "Ripoti ya maombi" in r.content.decode()
    rc = client.get("/ripoti/csv/")
    assert rc.status_code == 200
    assert rc["Content-Type"] == "text/csv"
    assert "Aina" in rc.content.decode("utf-8-sig")


def test_ripoti_jua_403(client, majukumu):
    juma = mtumiaji("juma", "wafanyakazi")
    client.force_login(juma)
    assert client.get("/ripoti/").status_code == 403


def test_barua_faili_na_namba(client, majukumu, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path
    rejest = mtumiaji("rejest", "rejista")
    client.force_login(rejest)
    faili = SimpleUploadedFile("barua.txt", b"MAUDHUI YA BARUA")
    r = client.post("/barua/mpya/", {
        "aina": "ingia", "kichwa": "Barua ya ukaguzi",
        "mhusika": "Ofisi ya Mhasibu", "tarehe": date.today().isoformat(),
        "faili": faili})
    assert r.status_code == 302
    b = Barua.objects.get()
    assert b.namba.startswith("WDA/")
    assert b.faili and b.faili.name.endswith("barua.txt")


def test_barua_si_rejista_403(client, majukumu):
    juma = mtumiaji("juma", "wafanyakazi")
    client.force_login(juma)
    assert client.get("/barua/mpya/").status_code == 403


def test_anza_data(db):
    call_command("anza")
    assert User.objects.filter(username="juma").exists()
    juma = User.objects.get(username="juma")
    assert juma.check_password("mtum123")
    assert juma.groups.filter(name="wafanyakazi").exists()
    assert Maombi.objects.count() == 4
    assert Barua.objects.count() == 2
    assert Kumbukumbu.objects.count() >= 4
