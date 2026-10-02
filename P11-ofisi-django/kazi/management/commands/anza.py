from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from kazi.models import Barua, Maombi


class Command(BaseCommand):
    help = "Majukumu, watumiaji wa majaribio na data ya mfano ya ofisi"

    def handle(self, *args, **options):
        for j in ["wafanyakazi", "meneja", "rejista"]:
            Group.objects.get_or_create(name=j)
        wat = [
            ("admin", "ofisi123", [], True),
            ("juma", "mtum123", ["wafanyakazi"], False),
            ("neema", "meneja123", ["wafanyakazi", "meneja"], False),
            ("rejest", "rej123", ["wafanyakazi", "rejista"], False),
        ]
        for jina, nenosiri, majukumu, mzizi in wat:
            u, mpya = User.objects.get_or_create(
                username=jina,
                defaults={"is_superuser": mzizi, "is_staff": mzizi})
            if mpya:
                u.set_password(nenosiri)
                u.save()
            for j in majukumu:
                u.groups.add(Group.objects.get(name=j))
        if Maombi.objects.count() == 0:
            juma = User.objects.get(username="juma")
            neema = User.objects.get(username="neema")
            rejest = User.objects.get(username="rejest")
            a = Maombi.objects.create(
                mhusika=juma, aina="likizo",
                maelezo="Likizo ya siku 10 - mwezi ujao")
            a.wasilisha(juma)
            Maombi.objects.create(
                mhusika=juma, aina="kuagiza",
                maelezo="Kununua viti 5 vya ofisini")
            b = Maombi.objects.create(
                mhusika=neema, aina="fedha",
                maelezo="Fedha za kikao cha taifa")
            b.wasilisha(neema)
            b.kagua(neema, idhini=False,
                    maoni="Tafadhali ongeza bajeti na kibali")
            Maombi.objects.create(
                mhusika=rejest, aina="likizo",
                maelezo="Likizo ya wiki 2 bahari")
            Barua.objects.create(
                aina="ingia", kichwa="Barua ya ukaguzi wa BAJETI",
                mhusika="Ofisi ya Mhasibu Mkuu", aliwasilisha=rejest)
            Barua.objects.create(
                aina="toka",
                kichwa="Wito wa kikao cha Baraza la Mawaziri",
                mhusika="Wizara ya Fedha", aliwasilisha=rejest)
        self.stdout.write(self.style.SUCCESS(
            "Tayari: majukumu 3; admin/ofisi123, juma/mtum123, "
            "neema/meneja123, rejest/rej123; data ya mfano"))
