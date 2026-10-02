from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from huduma.models import Akaunti, Miamala, Mkopo, Wateja


class Command(BaseCommand):
    help = "Tengeneza majukumu, watumiaji wa majaribio na data ya mfano"

    def handle(self, *args, **options):
        for j in ["admin", "mpokeaji", "mhasibu"]:
            Group.objects.get_or_create(name=j)
        wat = [
            ("admin", "benki123", "admin", True),
            ("mpokeaji", "pokea123", "mpokeaji", False),
            ("mhasibu", "hesabu123", "mhasibu", False),
        ]
        for jina, nenosiri, jukumu, mzizi in wat:
            u, mpya = User.objects.get_or_create(
                username=jina,
                defaults={"is_superuser": mzizi, "is_staff": mzizi})
            if mpya:
                u.set_password(nenosiri)
                u.save()
            u.groups.add(Group.objects.get(name=jukumu))
        if Wateja.objects.count() == 0:
            mpokeaji = User.objects.get(username="mpokeaji")
            data = [
                ("Asha Juma", "0712345678", "Dar es Salaam", "150000"),
                ("John Mwakalinga", "0756111222", "Arusha", "80000"),
                ("Neema Charles", "0787000999", "Mwanza", "250000"),
            ]
            for jina, simu, anwani, salio in data:
                m = Wateja.objects.create(jina=jina, simu=simu,
                                          anwani=anwani)
                a = Akaunti.objects.create(wateja=m,
                                           salio=Decimal(salio))
                Miamala.objects.create(
                    akaunti=a, aina="kuweka", kiasi=Decimal(salio),
                    maelezo="Amana ya kuanzia", alifanya=mpokeaji)
            Mkopo.objects.create(wateja=Wateja.objects.first(),
                                 kiasi=Decimal("500000"))
        self.stdout.write(self.style.SUCCESS(
            "Tayari: majukumu 3; watumiaji admin/benki123, "
            "mpokeaji/pokea123, mhasibu/hesabu123; data ya mfano"))
