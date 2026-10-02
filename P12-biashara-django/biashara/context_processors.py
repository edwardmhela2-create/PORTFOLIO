from django.db.models import Sum


def kikapu_hali(request):
    """Context processor: idadi ya kikapu kwa KILA ukurasa (navbar).

    Fundisho: hii inaenda kwenye MODALI ZOTE - hivyo vipengele vya
    DB vipewe cache/lowa gharama kwenye tovuti kubwa (production).
    """
    if request.user.is_authenticated:
        from .models import Kipengele
        idadi = Kipengele.objects.filter(
            mtumiaji=request.user).aggregate(
            j=Sum("idadi"))["j"] or 0
        return {"idadi_kikapu": idadi}
    return {"idadi_kikapu": 0}
