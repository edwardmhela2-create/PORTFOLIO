from decimal import Decimal

import pytest
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import Client

from .models import Akaunti, Miamala, Mkopo, Wateja


@pytest.fixture
def majukumu(db):
    for j in ["admin", "mpokeaji", "mhasibu"]:
        Group.objects.get_or_create(name=j)


def mtumiaji(jina, jukumu):
    u = User.objects.create_user(username=jina, password="siri12345")
    u.groups.add(Group.objects.get(name=jukumu))
    return u


def test_nyumbani_bila_kuingia(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "Ingia" in r.content.decode()


def test_orodha_wateja_hindikwa(client):
    r = client.get("/wateja/")
    assert r.status_code == 302
    assert "/ingia/" in r["Location"]


def test_mpokeaji_aona_wateja(client, majukumu):
    u = mtumiaji("mpokeaji", "mpokeaji")
    Wateja.objects.create(jina="Asha Juma", simu="0712345678")
    client.force_login(u)
    r = client.get("/wateja/")
    assert r.status_code == 200
    assert "Asha Juma" in r.content.decode()


def test_mpokeaji_hafanai_futa(client, majukumu):
    u = mtumiaji("mpokeaji", "mpokeaji")
    m = Wateja.objects.create(jina="John Mwakalinga", simu="0756111222")
    client.force_login(u)
    r = client.post("/wateja/%d/futa/" % m.pk)
    assert r.status_code == 403
    assert Wateja.objects.filter(pk=m.pk).exists()


def test_admin_futa_kwa_cascade(client, majukumu):
    u = mtumiaji("boss", "admin")
    m = Wateja.objects.create(jina="Neema Charles", simu="0787000999")
    a = Akaunti.objects.create(wateja=m, salio=Decimal("50000"))
    Miamala.objects.create(akaunti=a, aina="kuweka",
                           kiasi=Decimal("50000"))
    client.force_login(u)
    r = client.post("/wateja/%d/futa/" % m.pk)
    assert r.status_code == 302
    assert not Wateja.objects.exists()
    assert not Akaunti.objects.exists()
    assert not Miamala.objects.exists()


def test_ongeza_wateja(client, majukumu):
    u = mtumiaji("admin", "admin")
    client.force_login(u)
    r = client.post("/wateja/ongeza/", {
        "jina": "Neema Charles", "simu": "0787000999",
        "barua_pepe": "", "anwani": "Mwanza"})
    assert r.status_code == 302
    assert Wateja.objects.filter(simu="0787000999").exists()


def test_ongeza_simu_duplikati(client, majukumu):
    Wateja.objects.create(jina="Tayariupo", simu="0711000111")
    u = mtumiaji("admin", "admin")
    client.force_login(u)
    r = client.post("/wateja/ongeza/", {
        "jina": "Mpya", "simu": "0711000111",
        "barua_pepe": "", "anwani": ""})
    assert r.status_code == 200
    assert Wateja.objects.count() == 1


def test_akaunti_namba_ya_kiotomatiki(db):
    m = Wateja.objects.create(jina="Asha", simu="0712345678")
    a = Akaunti.objects.create(wateja=m)
    assert a.namba.startswith("TZ")
    assert len(a.namba) == 12


def test_kuweka_kuongeza_salio(db):
    m = Wateja.objects.create(jina="Asha", simu="0712345678")
    a = Akaunti.objects.create(wateja=m)
    a.weka(Decimal("10000"))
    a.refresh_from_db()
    assert a.salio == Decimal("10000")


def test_kutoa_zaidi_ya_salio_kushindwa(db):
    m = Wateja.objects.create(jina="Asha", simu="0712345678")
    a = Akaunti.objects.create(wateja=m, salio=Decimal("5000"))
    with pytest.raises(ValidationError):
        a.toa(Decimal("99999"))
    a.refresh_from_db()
    assert a.salio == Decimal("5000")


def test_fedha_kuweka_hindikwa(client, majukumu):
    u = mtumiaji("mpokeaji", "mpokeaji")
    m = Wateja.objects.create(jina="Asha", simu="0712345678")
    a = Akaunti.objects.create(wateja=m)
    client.force_login(u)
    r = client.post("/fedha/", {
        "akaunti": a.pk, "aina": "kuweka",
        "kiasi": "20000", "maelezo": "Amana ya benki"})
    assert r.status_code == 302
    a.refresh_from_db()
    assert a.salio == Decimal("20000")
    mt = Miamala.objects.get()
    assert mt.alifanya == u
    assert mt.aina == "kuweka"


def test_fedha_kutoa_haizidi_salio(client, majukumu):
    u = mtumiaji("mpokeaji", "mpokeaji")
    m = Wateja.objects.create(jina="Asha", simu="0712345678")
    a = Akaunti.objects.create(wateja=m, salio=Decimal("10000"))
    client.force_login(u)
    r = client.post("/fedha/", {
        "akaunti": a.pk, "aina": "kutoa",
        "kiasi": "999999", "maelezo": ""})
    assert r.status_code == 200
    assert "haitoshi" in r.content.decode()
    a.refresh_from_db()
    assert a.salio == Decimal("10000")
    assert not Miamala.objects.exists()


def test_ripoti_mhasibu_200(client, majukumu):
    u = mtumiaji("mhasibu", "mhasibu")
    client.force_login(u)
    assert client.get("/ripoti/").status_code == 200


def test_ripoti_mpokeaji_403(client, majukumu):
    u = mtumiaji("mpokeaji", "mpokeaji")
    client.force_login(u)
    assert client.get("/ripoti/").status_code == 403


def test_csrf_haikubaliki(majukumu):
    mtembeleaji = Client(enforce_csrf_checks=True)
    u = mtumiaji("admin", "admin")
    mtembeleaji.force_login(u)
    r = mtembeleaji.post("/wateja/ongeza/", {
        "jina": "Bila Tokeni", "simu": "0700000000",
        "barua_pepe": "", "anwani": ""})
    assert r.status_code == 403
    assert not Wateja.objects.exists()


def test_mikopo_mpokeaji_403(client, majukumu):
    u = mtumiaji("mpokeaji", "mpokeaji")
    client.force_login(u)
    r = client.post("/mikopo/ongeza/", {
        "wateja": "", "kiasi": "1000", "riba_asilimia": "10"})
    assert r.status_code == 403


def test_mkopo_lipa_hindikwa(client, majukumu):
    u = mtumiaji("mpokeaji", "mpokeaji")
    m = Wateja.objects.create(jina="Asha", simu="0712345678")
    k = Mkopo.objects.create(wateja=m, kiasi=Decimal("100000"),
                             riba_asilimia=Decimal("10"))
    assert k.salio == Decimal("110000")
    client.force_login(u)
    r = client.post("/mikopo/%d/lipa/" % k.pk)
    assert r.status_code == 302
    k.refresh_from_db()
    assert k.hali == "umelipa"
    assert k.salio == 0


def test_anza_data(db, capsys):
    call_command("anza")
    assert User.objects.filter(username="admin").exists()
    a = User.objects.get(username="mpokeaji")
    assert a.check_password("pokea123")
    assert a.groups.filter(name="mpokeaji").exists()
    assert Wateja.objects.count() == 3
    assert Mkopo.objects.count() == 1


def test_toka_hindikwa(client, majukumu):
    u = mtumiaji("admin", "admin")
    client.force_login(u)
    r = client.post("/toka/")
    assert r.status_code == 302
    r2 = client.get("/")
    assert "Ingia" in r2.content.decode()
