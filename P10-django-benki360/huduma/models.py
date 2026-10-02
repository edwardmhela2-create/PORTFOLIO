import uuid
from decimal import Decimal, InvalidOperation

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def safi_kiasi(kiasi):
    try:
        k = Decimal(str(kiasi))
    except (InvalidOperation, ValueError):
        raise ValidationError("Kiasi si sahihi")
    if k <= 0:
        raise ValidationError("Kiasi lazima liwe chanya")
    return k


class Wateja(models.Model):
    jina = models.CharField("Jina kamili", max_length=120)
    simu = models.CharField("Simu", max_length=20, unique=True)
    barua_pepe = models.EmailField("Barua pepe", blank=True)
    anwani = models.CharField("Anwani", max_length=200, blank=True)
    imesajiliwa = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["jina"]

    def __str__(self):
        return "%s (%s)" % (self.jina, self.simu)


class Akaunti(models.Model):
    AINATU = [("hifadhi", "Hifadhi"), ("biashara", "Biashara")]
    namba = models.CharField(max_length=16, unique=True, blank=True)
    wateja = models.ForeignKey(Wateja, on_delete=models.CASCADE,
                               related_name="akaunti")
    aina = models.CharField(max_length=20, choices=AINATU,
                            default="hifadhi")
    salio = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    imefunguliwa = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-imefunguliwa"]

    def save(self, *args, **kwargs):
        if not self.namba:
            self.namba = "TZ" + uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s - %s" % (self.namba, self.wateja.jina)

    def weka(self, kiasi):
        self.salio += safi_kiasi(kiasi)
        self.save(update_fields=["salio"])

    def toa(self, kiasi):
        kiasi = safi_kiasi(kiasi)
        if kiasi > self.salio:
            raise ValidationError("Salio haitoshi (halipo %s)" % self.salio)
        self.salio -= kiasi
        self.save(update_fields=["salio"])


class Miamala(models.Model):
    AINATU = [("kuweka", "Kuweka"), ("kutoa", "Kutoa")]
    akaunti = models.ForeignKey(Akaunti, on_delete=models.CASCADE,
                                related_name="miamala")
    aina = models.CharField(max_length=10, choices=AINATU)
    kiasi = models.DecimalField(max_digits=12, decimal_places=2)
    maelezo = models.CharField(max_length=200, blank=True)
    tarehe = models.DateTimeField(auto_now_add=True)
    alifanya = models.ForeignKey(User, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name="miamala")

    class Meta:
        ordering = ["-tarehe"]

    def __str__(self):
        return "%s %s -> %s" % (self.aina, self.kiasi, self.akaunti.namba)


class Mkopo(models.Model):
    HALI = [("hai", "Hai"), ("umelipa", "Umelipa")]
    wateja = models.ForeignKey(Wateja, on_delete=models.CASCADE,
                               related_name="mikopo")
    kiasi = models.DecimalField(max_digits=12, decimal_places=2)
    riba_asilimia = models.DecimalField(max_digits=5, decimal_places=2,
                                        default=10)
    salio = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hali = models.CharField(max_length=10, choices=HALI, default="hai")
    tarehe = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-tarehe"]

    def save(self, *args, **kwargs):
        if self._state.adding and not self.salio and self.kiasi:
            riba = self.kiasi * self.riba_asilimia / Decimal("100")
            self.salio = self.kiasi + riba
        super().save(*args, **kwargs)

    def lipa(self, kiasi):
        kiasi = safi_kiasi(kiasi)
        if kiasi > self.salio:
            raise ValidationError("Malipo hayawezi zidi deni (%s)"
                                  % self.salio)
        self.salio -= kiasi
        if self.salio == 0:
            self.hali = "umelipa"
        self.save(update_fields=["salio", "hali"])

    def __str__(self):
        return "Mkopo %s - %s" % (self.kiasi, self.wateja.jina)
