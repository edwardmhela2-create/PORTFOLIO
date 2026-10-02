from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Lebo(models.Model):
    jina = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ["jina"]

    def __str__(self):
        return self.jina


class Bidhaa(models.Model):
    jina = models.CharField(max_length=120)
    maelezo = models.TextField(blank=True)
    bei = models.DecimalField(max_digits=10, decimal_places=0)
    stoo = models.PositiveIntegerField(default=0)
    lebo = models.ManyToManyField(Lebo, blank=True,
                                  related_name="bidhaa")
    imeongezwa = models.DateTimeField(auto_now_add=True)
    imebadilishwa = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["jina"]

    def __str__(self):
        return self.jina

    @property
    def inauzwa(self):
        return self.stoo > 0


class Kipengele(models.Model):
    """Kipengele cha kikapu - kwa kila mtumiaji + bidhaa (unique)."""
    bidhaa = models.ForeignKey(Bidhaa, on_delete=models.CASCADE,
                               related_name="kikapuni")
    mtumiaji = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name="kikapu")
    idadi = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["bidhaa", "mtumiaji"],
                name="kipekee_kwa_mtumiaji"),
        ]

    @property
    def jumla(self):
        return self.bidhaa.bei * self.idadi

    def __str__(self):
        return "%s x%d" % (self.bidhaa.jina, self.idadi)


class Oda(models.Model):
    HALI = [("tarajiwa", "Inasubiri malipo"),
            ("imekulipwa", "Imekulipwa"),
            ("imefutwa", "Imefutwa")]
    NJIA = [("mpesa", "M-Pesa"), ("taslimu", "Taslimu")]
    ref = models.CharField(max_length=20, unique=True, blank=True)
    mtumiaji = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name="oda")
    hali = models.CharField(max_length=15, choices=HALI,
                            default="tarajiwa")
    njia = models.CharField(max_length=10, choices=NJIA)
    simu = models.CharField(max_length=15, blank=True)
    jumla = models.DecimalField(max_digits=10, decimal_places=0,
                                default=0)
    imeandikwa = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-imeandikwa"]

    def save(self, *args, **kwargs):
        if not self.ref:
            mwaka = self.imeandikwa.year if self.imeandikwa else None
            if mwaka is None:
                from datetime import date
                mwaka = date.today().year
            idadi = Oda.objects.filter(
                ref__contains=str(mwaka)).count() + 1
            self.ref = "ORD/%s/%04d" % (mwaka, idadi)
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s (%s)" % (self.ref, self.mtumiaji.username)


class OdaBidhaa(models.Model):
    """Snapshot: bei + jina yahifadhiwa wakati wa ununuzi."""
    oda = models.ForeignKey(Oda, on_delete=models.CASCADE,
                            related_name="vipengele")
    bidhaa = models.ForeignKey(Bidhaa, on_delete=models.SET_NULL,
                               null=True, related_name="mauzo")
    jina_la_bidhaa = models.CharField(max_length=120)
    bei = models.DecimalField(max_digits=10, decimal_places=0)
    idadi = models.PositiveIntegerField()

    @property
    def jumla(self):
        return self.bei * self.idadi

    def __str__(self):
        return "%s x%d" % (self.jina_la_bidhaa, self.idadi)
