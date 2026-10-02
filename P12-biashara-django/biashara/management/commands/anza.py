from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from biashara.models import Bidhaa, Lebo


class Command(BaseCommand):
    help = "Jaza duka la mfano: vikundi, watumiaji, lebo, bidhaa"

    def handle(self, *a, **kw):
        muuzaji, _ = Group.objects.get_or_create(name="muuzaji")
        mnnunuzi, _ = Group.objects.get_or_create(name="mnnunuzi")

        watu = [
            ("admin", "duka123", True, False),
            ("hassan", "muuz123", False, True),
            ("amina", "kinu123", False, False),
        ]
        for jina, nenosiri, superuser, ni_muuzaji in watu:
            if not User.objects.filter(username=jina).exists():
                u = User.objects.create_user(
                    username=jina, password=nenosiri)
                u.is_superuser = superuser
                u.is_staff = superuser
                u.save()
                if superuser:
                    u.groups.add(muuzaji, mnnunuzi)
                elif ni_muuzaji:
                    u.groups.add(muuzaji, mnnunuzi)
                else:
                    u.groups.add(mnnunuzi)
                self.stdout.write(
                    "Mtumiaji: %s / %s" % (jina, nenosiri))

        lebo = {}
        for j in ["nguo", "chakula", "vifaa", "elektroniki"]:
            lebo[j], _ = Lebo.objects.get_or_create(jina=j)

        bidhaa = [
            ("Sabuni ya Mche", 2000, 40, ["chakula"],
             "Sabuni ya kuosha mche na mikono."),
            ("Mchele wa Kilimo 5kg", 15000, 25, ["chakula"],
             "Mchele mweupe wa kila siku."),
            ("Mafuta ya Kukaanga 2L", 12000, 30, ["chakula"],
             "Mafuta ya kupikia yenye ubora."),
            ("Soda 500ml", 1000, 100, ["chakula"],
             "Vinywaji baridi vya asili."),
            ("T-Shiti ya Bluu", 8000, 20, ["nguo"],
             "T-shiti ya cotton, ukubwa wote."),
            ("Kiatu cha Michezo", 25000, 12, ["nguo"],
             "Kiatu rahisi cha mazoezi na kazi."),
            ("Kofia ya Mtandaoni", 5000, 35, ["nguo"],
             "Kofia ya kujilinda na jua."),
            ("Kichaji cha Kuchaji", 7000, 45, ["elektroniki"],
             "Chaja ya simu ya haraka (USB-C)."),
            ("Vipande vya Sikio", 12000, 22, ["elektroniki"],
             "Earphones za masikioni."),
            ("Kibatari cha Nuru", 4000, 60, ["vifaa"],
             "LED bulb ya chumba chako."),
            ("Kisu cha Jikoni", 6000, 30, ["vifaa"],
             "Kisu cha kupiga nyama na mboga."),
            ("Viazi Vitamu 10kg", 12000, 18, ["chakula"],
             "Viazi vitamu safi kutoka nyanda za juu."),
        ]
        for jina, bei, stoo, lebos, maelezo in bidhaa:
            b, iliyoundwa = Bidhaa.objects.get_or_create(
                jina=jina,
                defaults={"bei": bei, "stoo": stoo,
                          "maelezo": maelezo})
            if iliyoundwa:
                b.lebo.set(lebo[l] for l in lebos)

        self.stdout.write(self.style.SUCCESS(
            "Duka limejaa: %d bidhaa" % Bidhaa.objects.count()))
