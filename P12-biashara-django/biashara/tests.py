from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Bidhaa, Kipengele, Lebo, Oda, OdaBidhaa


def _mtumiaji(jina, jukumu=None, nenosiri="siri1234"):
    u = User.objects.create_user(username=jina, password=nenosiri)
    if jukumu:
        g, _ = Group.objects.get_or_create(name=jukumu)
        u.groups.add(g)
    return u


class DukaHabariTests(TestCase):
    """Ukurasa wa bidhaa ni UMMA - hamuhitaji kuingia."""

    def setUp(self):
        self.nguo = Lebo.objects.create(jina="nguo")
        self.chakula = Lebo.objects.create(jina="chakula")
        self.b1 = Bidhaa.objects.create(
            jina="T-Shiti", bei=8000, stoo=10,
            maelezo="Nzuri sana ya kulala")
        self.b1.lebo.add(self.nguo)
        self.b2 = Bidhaa.objects.create(
            jina="Mchele", bei=15000, stoo=5,
            maelezo="Wa kila siku")

    def test_rodha_ya_umma_bila_kuingia(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "T-Shiti")
        self.assertContains(r, "8000")

    def test_utafutaji_wa_jina(self):
        r = self.client.get("/", {"q": "mchele"})
        self.assertContains(r, "Mchele")
        self.assertNotContains(r, "T-Shiti")

    def test_kichujio_cha_lebo(self):
        r = self.client.get("/", {"lebo": "nguo"})
        self.assertContains(r, "T-Shiti")
        self.assertNotContains(r, "Mchele")

    def test_maelezo_ya_bidhaa_na_404(self):
        r = self.client.get("/bidhaa/%d/" % self.b1.pk)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "T-Shiti")
        r2 = self.client.get("/bidhaa/99999/")
        self.assertEqual(r2.status_code, 404)

    def test_ukurasa_wa_pili_wa_machapisho(self):
        for i in range(2, 10):
            Bidhaa.objects.create(jina="Bidhaa %d" % i,
                                  bei=1000, stoo=1)
        r = self.client.get("/")
        self.assertEqual(len(r.context["bidhaa"]), 8)
        r2 = self.client.get("/", {"page": 2})
        self.assertEqual(len(r2.context["bidhaa"]), 2)

    def test_context_processor_badge(self):
        r = self.client.get("/")
        self.assertEqual(r.context["idadi_kikapu"], 0)
        m = _mtumiaji("halima")
        self.client.login(username="halima", password="siri1234")
        Kipengele.objects.create(bidhaa=self.b1, mtumiaji=m,
                                 idadi=3)
        r2 = self.client.get("/")
        self.assertEqual(r2.context["idadi_kikapu"], 3)


class KikapuTests(TestCase):

    def setUp(self):
        self.b = Bidhaa.objects.create(jina="Sabuni", bei=1000,
                                       stoo=5)
        self.m = _mtumiaji("asha", "mnnunuzi")
        self.client.login(username="asha", password="siri1234")

    def _ongeza(self, idadi):
        return self.client.post(
            reverse("kikapu_ongeza", args=[self.b.pk]),
            {"idadi": idadi})

    def test_kuingia_linahitajika(self):
        self.client.logout()
        r = self._ongeza(1)
        self.assertEqual(r.status_code, 302)
        self.assertIn("ingia", r["Location"])

    def test_ongeza_hutengeneza_kipengele(self):
        r = self._ongeza(2)
        self.assertRedirects(r, reverse("kikapu"))
        k = Kipengele.objects.get()
        self.assertEqual(k.idadi, 2)
        self.assertEqual(k.mtumiaji, self.m)

    def test_ongeza_maradufu_huongeza_idadi(self):
        self._ongeza(1)
        self._ongeza(2)
        self.assertEqual(Kipengele.objects.get().idadi, 3)

    def test_ongeza_hushindwa_kuzidi_stoo(self):
        r = self._ongeza(9)
        self.assertEqual(Kipengele.objects.count(), 0)
        self.assertRedirects(
            r, reverse("bidhaa_maelezo", args=[self.b.pk]))

    def test_jumla_ya_kikapu_sahihi(self):
        Kipengele.objects.create(bidhaa=self.b, mtumiaji=self.m,
                                 idadi=3)
        r = self.client.get(reverse("kikapu"))
        self.assertEqual(r.context["jumla"], 3000)

    def test_badilisha_na_futa_mali_yangu(self):
        k = Kipengele.objects.create(bidhaa=self.b, mtumiaji=self.m,
                                     idadi=1)
        self.client.post(reverse("kikapu_badilisha", args=[k.pk]),
                         {"idadi": 4})
        k.refresh_from_db()
        self.assertEqual(k.idadi, 4)
        self.client.post(reverse("kikapu_futa", args=[k.pk]))
        self.assertEqual(Kipengele.objects.count(), 0)

    def test_huwezi_kugusa_kikapu_cha_mtu_wingine(self):
        """Mali ya mwingine = 404 (si 403) - tusionyeshe kuwa ipo."""
        m2 = _mtumiaji("zawadi")
        k2 = Kipengele.objects.create(bidhaa=self.b, mtumiaji=m2,
                                      idadi=2)
        r = self.client.post(
            reverse("kikapu_badilisha", args=[k2.pk]),
            {"idadi": 5})
        self.assertEqual(r.status_code, 404)
        k2.refresh_from_db()
        self.assertEqual(k2.idadi, 2)


class LipaTests(TestCase):

    def setUp(self):
        self.b = Bidhaa.objects.create(jina="Kofia", bei=1000,
                                       stoo=5)
        self.m = _mtumiaji("juma", "mnnunuzi")
        self.client.login(username="juma", password="siri1234")
        Kipengele.objects.create(bidhaa=self.b, mtumiaji=self.m,
                                 idadi=2)

    def test_lipa_huhitaji_kuingia(self):
        self.client.logout()
        r = self.client.post(reverse("lipa"),
                             {"njia": "taslimu", "simu": ""})
        self.assertEqual(r.status_code, 302)
        self.assertIn("ingia", r["Location"])

    def test_lipa_fanikiwa_hushusha_stoo(self):
        r = self.client.post(reverse("lipa"),
                             {"njia": "taslimu", "simu": ""})
        o = Oda.objects.get()
        self.assertRedirects(r, reverse("oda_maelezo",
                                        args=[o.pk]))
        self.assertTrue(o.ref.startswith("ORD/"))
        self.assertEqual(o.jumla, 2000)
        self.assertEqual(o.hali, "tarajiwa")
        self.b.refresh_from_db()
        self.assertEqual(self.b.stoo, 3)
        self.assertEqual(Kipengele.objects.count(), 0)
        v = OdaBidhaa.objects.get()
        self.assertEqual(v.bei, 1000)
        self.assertEqual(v.idadi, 2)

    def test_lipa_mpesa_hitaji_namba_sahihi(self):
        r = self.client.post(reverse("lipa"),
                             {"njia": "mpesa", "simu": ""})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Oda.objects.count(), 0)
        r2 = self.client.post(reverse("lipa"),
                              {"njia": "mpesa", "simu": "12345"})
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(Oda.objects.count(), 0)

    def test_lipa_kikapu_tupu_hakuna_oda(self):
        Kipengele.objects.all().delete()
        r = self.client.post(reverse("lipa"),
                             {"njia": "taslimu", "simu": ""})
        self.assertRedirects(r, reverse("kikapu"))
        self.assertEqual(Oda.objects.count(), 0)

    def test_lipa_hushindwa_stoo_iliyobadilika(self):
        self.b.stoo = 1
        self.b.save()
        r = self.client.post(reverse("lipa"),
                             {"njia": "taslimu", "simu": ""})
        self.assertRedirects(r, reverse("kikapu"))
        self.assertEqual(Oda.objects.count(), 0)
        self.b.refresh_from_db()
        self.assertEqual(self.b.stoo, 1)
        self.assertEqual(Kipengele.objects.count(), 1)

    def test_bei_ya_oda_ni_snapshot(self):
        self.client.post(reverse("lipa"),
                         {"njia": "taslimu", "simu": ""})
        self.b.bei = 9999
        self.b.save()
        v = OdaBidhaa.objects.get()
        self.assertEqual(v.bei, 1000)
        o = Oda.objects.get()
        self.assertEqual(o.jumla, 2000)

    def test_beleshani_mtu_wingine_haoni_oda_yako(self):
        self.client.post(reverse("lipa"),
                         {"njia": "taslimu", "simu": ""})
        o = Oda.objects.get()
        self.client.logout()
        _mtumiaji("naima")
        self.client.login(username="naima", password="siri1234")
        r = self.client.get(reverse("oda_orodha"))
        self.assertNotContains(r, o.ref)
        r2 = self.client.get(reverse("oda_maelezo", args=[o.pk]))
        self.assertEqual(r2.status_code, 404)


class MauzajiTests(TestCase):
    """Kuongeza/hariri/futa bidhaa = MUUZAJI au admin tu."""

    def setUp(self):
        self.lebo = Lebo.objects.create(jina="vifaa")
        self.b = Bidhaa.objects.create(jina="Chaja", bei=7000,
                                       stoo=9)

    def _jaribu_403(self, url, data=None):
        try:
            if data is None:
                r = self.client.get(url)
            else:
                r = self.client.post(url, data)
            return r.status_code
        except PermissionDenied:
            return 403

    def test_mnnunuzi_hawezi_kuongeza(self):
        _mtumiaji("amina", "mnnunuzi")
        self.client.login(username="amina", password="siri1234")
        self.assertEqual(
            self._jaribu_403(reverse("bidhaa_mpya")), 403)

    def test_muuzaji_haongeza_na_haondolei_mlemaji(self):
        _mtumiaji("hassan", "muuzaji")
        self.client.login(username="hassan", password="siri1234")
        r = self.client.get(reverse("bidhaa_mpya"))
        self.assertEqual(r.status_code, 200)
        r2 = self.client.post(reverse("bidhaa_mpya"), {
            "jina": "Kofia", "maelezo": "Mpya kabisa",
            "bei": "3000", "stoo": "7",
            "lebo": [self.lebo.pk]})
        self.assertRedirects(r2, reverse("bidhaa_orodha"))
        mpya = Bidhaa.objects.get(jina="Kofia")
        self.assertEqual(mpya.lebo.count(), 1)

    def test_muuzaji_hariri_na_kufuta(self):
        _mtumiaji("hassan", "muuzaji")
        self.client.login(username="hassan", password="siri1234")
        self.client.post(
            reverse("bidhaa_hariri", args=[self.b.pk]),
            {"jina": "Chaja", "maelezo": "", "bei": "5500",
             "stoo": "9", "lebo": [self.lebo.pk]})
        self.b.refresh_from_db()
        self.assertEqual(self.b.bei, 5500)
        self.client.post(reverse("bidhaa_futa", args=[self.b.pk]))
        self.assertEqual(Bidhaa.objects.count(), 0)


class OdaAmanaTests(TestCase):

    def test_anza_data_ya_mfano(self):
        call_command("anza")
        self.assertTrue(
            Group.objects.filter(name="muuzaji").exists())
        self.assertTrue(
            User.objects.filter(username="hassan").exists())
        self.assertEqual(Lebo.objects.count(), 4)
        self.assertGreaterEqual(Bidhaa.objects.count(), 10)
