from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .decorators import linahitaji_jukumu
from .forms import FedhaForm, MkopoForm, WatejaForm
from .models import Akaunti, Miamala, Mkopo, Wateja


def nyumbani(request):
    if not request.user.is_authenticated:
        return render(request, "nyumbani.html")
    dashibodi = {
        "wateja": Wateja.objects.count(),
        "akaunti": Akaunti.objects.count(),
        "salio_jumla": Akaunti.objects.aggregate(
            j=Sum("salio"))["j"] or 0,
        "miamala": Miamala.objects.count(),
        "mikopo_hai": Mkopo.objects.filter(hali="hai").count(),
    }
    return render(request, "nyumbani.html", {"dashibodi": dashibodi})


@linahitaji_jukumu("admin", "mpokeaji", "mhasibu")
def wateja_orodha(request):
    q = request.GET.get("q", "").strip()
    wat = Wateja.objects.all()
    if q:
        wat = wat.filter(Q(jina__icontains=q)
                         | Q(simu__icontains=q))
    return render(request, "wateja_orodha.html",
                  {"wateja": wat.distinct(), "q": q})


@linahitaji_jukumu("admin", "mpokeaji")
def wateja_ongeza(request):
    if request.method == "POST":
        f = WatejaForm(request.POST)
        if f.is_valid():
            mteja = f.save()
            messages.success(request,
                             "Mteja %s amesajiliwa" % mteja.jina)
            return redirect("wateja_orodha")
    else:
        f = WatejaForm()
    return render(request, "wateja_fomu.html",
                  {"f": f, "kichwa": "Sajili mteja mpya"})


@require_POST
@linahitaji_jukumu("admin")
def wateja_futa(request, pk):
    mteja = get_object_or_404(Wateja, pk=pk)
    jina = mteja.jina
    namba = mteja.akaunti.count()
    mteja.delete()
    messages.warning(
        request,
        "Mteja %s amefutwa pamoja na akaunti zake (%d) - CASCADE"
        % (jina, namba))
    return redirect("wateja_orodha")


@linahitaji_jukumu("admin", "mpokeaji", "mhasibu")
def akaunti_orodha(request):
    akaunti = Akaunti.objects.select_related("wateja")
    return render(request, "akaunti_orodha.html",
                  {"akaunti": akaunti,
                   "wateja": Wateja.objects.all()})


@require_POST
@linahitaji_jukumu("admin", "mpokeaji")
def akaunti_fungua(request, wateja_pk):
    mteja = get_object_or_404(Wateja, pk=wateja_pk)
    akaunti = Akaunti.objects.create(wateja=mteja)
    messages.success(request, "Akaunti %s imefunguliwa kwa %s"
                     % (akaunti.namba, mteja.jina))
    return redirect("akaunti_orodha")


@linahitaji_jukumu("admin", "mpokeaji")
def fedha(request):
    hatari = None
    if request.method == "POST":
        f = FedhaForm(request.POST)
        if f.is_valid():
            akaunti = f.cleaned_data["akaunti"]
            aina = f.cleaned_data["aina"]
            kiasi = f.cleaned_data["kiasi"]
            maelezo = f.cleaned_data["maelezo"]
            try:
                with transaction.atomic():
                    if aina == "kuweka":
                        akaunti.weka(kiasi)
                    else:
                        akaunti.toa(kiasi)
                    Miamala.objects.create(
                        akaunti=akaunti, aina=aina, kiasi=kiasi,
                        maelezo=maelezo, alifanya=request.user)
                messages.success(
                    request, "%s %s Tsh %s - salio jipya %s"
                    % (aina.capitalize(), kiasi, akaunti.namba,
                       akaunti.salio))
                return redirect("jedwali")
            except ValidationError as e:
                hatari = "; ".join(e.messages)
    else:
        f = FedhaForm()
    return render(request, "fedha.html", {"f": f, "hatari": hatari})


@linahitaji_jukumu("admin", "mpokeaji", "mhasibu")
def jedwali(request):
    miamala = Miamala.objects.select_related(
        "akaunti__wateja", "alifanya")[:50]
    return render(request, "jedwali.html", {"miamala": miamala})


@linahitaji_jukumu("admin", "mpokeaji", "mhasibu")
def mikopo_orodha(request):
    mikopo = Mkopo.objects.select_related("wateja")
    fomu = MkopoForm()
    return render(request, "mikopo_orodha.html",
                  {"mikopo": mikopo, "f": fomu})


@linahitaji_jukumu("admin", "mhasibu")
def mkopo_ongeza(request):
    if request.method == "POST":
        f = MkopoForm(request.POST)
        if f.is_valid():
            mkopo = f.save()
            messages.success(
                request, "Mkopo wa Tsh %s kwa %s umepewa (deni %s)"
                % (mkopo.kiasi, mkopo.wateja.jina, mkopo.salio))
            return redirect("mikopo_orodha")
    else:
        f = MkopoForm()
    return render(request, "wateja_fomu.html",
                  {"f": f, "kichwa": "Mkopo mpya"})


@require_POST
@linahitaji_jukumu("admin", "mpokeaji")
def mkopo_lipa(request, pk):
    mkopo = get_object_or_404(Mkopo, pk=pk)
    if mkopo.hali != "hai":
        messages.warning(request, "Mkopo huu tayari umelipwa")
        return redirect("mikopo_orodha")
    try:
        mkopo.lipa(mkopo.salio)
    except ValidationError as e:
        messages.error(request, "; ".join(e.messages))
        return redirect("mikopo_orodha")
    messages.success(request, "Mkopo wa %s UMELIPWA"
                     % mkopo.wateja.jina)
    return redirect("mikopo_orodha")


@linahitaji_jukumu("admin", "mhasibu")
def ripoti(request):
    rows = []
    for w in Wateja.objects.all():
        rows.append({
            "w": w,
            "salio": sum(a.salio for a in w.akaunti.all()),
            "deni": sum(k.salio for k in w.mikopo.all()),
            "idadi_akaunti": w.akaunti.count(),
        })
    rows.sort(key=lambda r: r["salio"], reverse=True)
    jumla = sum(r["salio"] for r in rows)
    deni_jumla = sum(r["deni"] for r in rows)
    return render(request, "ripoti.html", {
        "rows": rows, "jumla": jumla, "deni_jumla": deni_jumla})
