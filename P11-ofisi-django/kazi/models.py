from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Kumbukumbu(models.Model):
    """Audit trail: kila hatua ya maombi inaandikwa (signal + methods)."""
    maombi = models.ForeignKey("Maombi", null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name="kumbukumbu")
    mada = models.CharField(max_length=200)
    maelezo = models.CharField(max_length=300, blank=True)
    alifanya = models.ForeignKey(User, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name="kumbukumbu_angu")
    tarehe = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-tarehe"]

    def __str__(self):
        return self.mada


class Maombi(models.Model):
    HALI = [
        ("rasimu", "Rasimu"),
        ("imewasilishwa", "Imewasilishwa"),
        ("imeidhinishwa", "Imeidhinishwa"),
        ("imekataliwa", "Imekataliwa"),
    ]
    AINATU = [
        ("likizo", "Likizo"),
        ("kuagiza", "Kuagiza vifaa"),
        ("fedha", "Maombi ya fedha"),
    ]
    mhusika = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="maombi_yangu")
    aina = models.CharField(max_length=20, choices=AINATU)
    maelezo = models.TextField("Maelezo")
    hali = models.CharField(max_length=20, choices=HALI,
                            default="rasimu")
    meneja = models.ForeignKey(User, null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name="amekagua")
    maoni = models.CharField(max_length=300, blank=True)
    imewasilishwa = models.DateTimeField(null=True, blank=True)
    imeamuliwa = models.DateTimeField(null=True, blank=True)
    imetengenezwa = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-imetengenezwa"]

    def __str__(self):
        return "#%s %s - %s" % (self.pk, self.get_aina_display(),
                                self.hali)

    def wasilisha(self, mtumiaji):
        if mtumiaji != self.mhusika:
            raise ValidationError("Maombi ni ya mhusika pekee")
        if self.hali != "rasimu":
            raise ValidationError(
                "Kinachoweza kutumwa ni RASIMU tu (hali: %s)"
                % self.hali)
        self.hali = "imewasilishwa"
        self.imewasilishwa = timezone.now()
        self.save()
        Kumbukumbu.objects.create(
            maombi=self,
            mada="Maombi #%s yamewasilishwa" % self.pk,
            alifanya=mtumiaji)

    def kagua(self, mtumiaji, idhini, maoni=""):
        if self.hali != "imewasilishwa":
            raise ValidationError(
                "Hakuna la kukagua (hali hii: %s)" % self.hali)
        if not idhini and not maoni.strip():
            raise ValidationError("Kukataa lazima liwe na maoni")
        self.hali = "imeidhinishwa" if idhini else "imekataliwa"
        self.meneja = mtumiaji
        self.maoni = maoni
        self.imeamuliwa = timezone.now()
        self.save()
        Kumbukumbu.objects.create(
            maombi=self,
            mada="Maombi #%s %s" % (
                self.pk,
                "YAMEIDHINISHWA" if idhini else "YAMEKATALIWA"),
            maelezo=maoni, alifanya=mtumiaji)


class Barua(models.Model):
    """Daftari la barua (registry) - namba ya kiotomatiki + faili."""
    AINATU = [("ingia", "Imeingia"), ("toka", "Imetoka")]
    namba = models.CharField(max_length=30, unique=True, blank=True)
    aina = models.CharField(max_length=10, choices=AINATU,
                            default="ingia")
    kichwa = models.CharField(max_length=200)
    mhusika = models.CharField(max_length=120,
                               help_text="Ofisi/mtu anayetumiwa")
    tarehe = models.DateField(default=date.today)
    faili = models.FileField(upload_to="barua/%Y/", blank=True)
    aliwasilisha = models.ForeignKey(User, null=True, blank=True,
                                     on_delete=models.SET_NULL,
                                     related_name="barua")
    imerejistrwa = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-tarehe", "-imerejistrwa"]

    def save(self, *args, **kwargs):
        if not self.namba:
            mwaka = self.tarehe.year
            idadi = Barua.objects.filter(
                tarehe__year=mwaka).count() + 1
            self.namba = "WDA/%s/%03d" % (mwaka, idadi)
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s - %s" % (self.namba, self.kichwa)


@receiver(post_save, sender=Maombi)
def kumbukumbu_ya_utengenezaji(sender, instance, created, **kwargs):
    """Signal: kila maombi mapya yanajirekodi yenyewe (bila views)."""
    if created:
        Kumbukumbu.objects.create(
            maombi=instance,
            mada="Maombi #%s limeandikwa (rasimu)" % instance.pk,
            alifanya=instance.mhusika)
