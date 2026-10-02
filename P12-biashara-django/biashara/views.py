from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import F, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  ListView, UpdateView)

from .forms import BidhaaForm, KikapuForm, LipaForm
from .linajukumu import MauzajiWaBidhaa
from .models import Bidhaa, Kipengele, Lebo, Oda, OdaBidhaa


class BidhaaOrodha(ListView):
    """Ukurasa wa duka: UMMA (hauhitaji kuingia) + utafutaji + lebo."""
    model = Bidhaa
    template_name = "bidhaa_orodha.html"
    context_object_name = "bidhaa"
    paginate_by = 8

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("lebo")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(jina__icontains=q)
                           | Q(maelezo__icontains=q))
        lebo = self.request.GET.get("lebo", "").strip()
        if lebo:
            qs = qs.filter(lebo__jina=lebo)
        return qs.distinct()

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["lebo_zote"] = Lebo.objects.all()
        ctx["q"] = self.request.GET.get("q", "")
        ctx["lebo_mchagua"] = self.request.GET.get("lebo", "")
        return ctx


class BidhaaMaelezo(DetailView):
    """Maelezo ya bidhaa + fomu ya kuongeza kikapu."""
    model = Bidhaa
    template_name = "bidhaa_maelezo.html"
    context_object_name = "bidhaa"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["fomu"] = KikapuForm()
        return ctx


@login_required
def kikapu_ongeza(request, pk):
    bidhaa = get_object_or_404(Bidhaa, pk=pk)
    if request.method != "POST":
        return redirect("bidhaa_maelezo", pk=pk)
    f = KikapuForm(request.POST)
    if f.is_valid():
        idadi = f.cleaned_data["idadi"]
        zilizopo = Kipengele.objects.filter(
            bidhaa=bidhaa, mtumiaji=request.user).first()
        msingi = zilizopo.idadi if zilizopo else 0
        if msingi + idadi > bidhaa.stoo:
            messages.error(request,
                           "Stoo haizidi: %d pekee yanapatikana"
                           % bidhaa.stoo)
        else:
            if zilizopo:
                zilizopo.idadi = msingi + idadi
                zilizopo.save()
            else:
                Kipengele.objects.create(bidhaa=bidhaa,
                                         mtumiaji=request.user,
                                         idadi=idadi)
            messages.success(request,
                             "%s imeongezwa kikapuni" % bidhaa.jina)
            return redirect("kikapu")
    messages.error(request, "Idadi si sahihi")
    return redirect("bidhaa_maelezo", pk=pk)


@login_required
def kikapu(request):
    vipengele = (Kipengele.objects
                 .select_related("bidhaa")
                 .filter(mtumiaji=request.user))
    jumla = sum((v.jumla for v in vipengele), 0)
    return render(request, "kikapu.html",
                  {"vipengele": vipengele, "jumla": jumla})


@login_required
def kikapu_badilisha(request, pk):
    kipengele = get_object_or_404(Kipengele, pk=pk,
                                  mtumiaji=request.user)
    if request.method != "POST":
        return redirect("kikapu")
    f = KikapuForm(request.POST)
    if f.is_valid():
        idadi = f.cleaned_data["idadi"]
        if idadi > kipengele.bidhaa.stoo:
            messages.error(request, "Stoo haizidi: %d"
                           % kipengele.bidhaa.stoo)
        else:
            kipengele.idadi = idadi
            kipengele.save()
            messages.success(request, "Idadi imebadilishwa")
    return redirect("kikapu")


@login_required
def kikapu_futa(request, pk):
    kipengele = get_object_or_404(Kipengele, pk=pk,
                                  mtumiaji=request.user)
    if request.method == "POST":
        jina = kipengele.bidhaa.jina
        kipengele.delete()
        messages.success(request, "%s imeondolewa" % jina)
    return redirect("kikapu")


@login_required
def lipa(request):
    vipengele = (Kipengele.objects
                 .select_related("bidhaa")
                 .filter(mtumiaji=request.user))
    if not vipengele:
        messages.error(request, "Kikapu ni tupu - nunua kwanza")
        return redirect("kikapu")
    jumla = sum((v.jumla for v in vipengele), 0)
    if request.method == "POST":
        f = LipaForm(request.POST)
        if f.is_valid():
            try:
                with transaction.atomic():
                    kwa_hifadhi = []
                    jumla_halisi = 0
                    for v in vipengele:
                        v.bidhaa.refresh_from_db()
                        if v.idadi > v.bidhaa.stoo:
                            raise ValidationError(
                                "Stoo ya '%s' imeisha (unaona %d, "
                                "stoo %d)" % (v.bidhaa.jina, v.idadi,
                                              v.bidhaa.stoo))
                        kwa_hifadhi.append((v, v.bidhaa.bei))
                        jumla_halisi += v.bidhaa.bei * v.idadi
                    oda = Oda.objects.create(
                        mtumiaji=request.user,
                        njia=f.cleaned_data["njia"],
                        simu=f.cleaned_data.get("simu", ""),
                        jumla=jumla_halisi)
                    for v, bei in kwa_hifadhi:
                        OdaBidhaa.objects.create(
                            oda=oda, bidhaa=v.bidhaa,
                            jina_la_bidhaa=v.bidhaa.jina,
                            bei=bei, idadi=v.idadi)
                        Bidhaa.objects.filter(pk=v.bidhaa.pk).update(
                            stoo=F("stoo") - v.idadi)
                    Kipengele.objects.filter(
                        mtumiaji=request.user).delete()
                messages.success(
                    request, "Oda %s imepokelewa karibu!"
                    % oda.ref)
                return redirect("oda_maelezo", pk=oda.pk)
            except ValidationError as e:
                messages.error(request, "; ".join(e.messages))
                return redirect("kikapu")
    return render(request, "lipa.html",
                  {"fomu": LipaForm(), "vipengele": vipengele,
                   "jumla": jumla})


@login_required
def oda_orodha(request):
    oda_zangu = (Oda.objects
                 .filter(mtumiaji=request.user)
                 .prefetch_related("vipengele"))
    return render(request, "oda_orodha.html",
                  {"oda_zangu": oda_zangu})


class OdaMaelezo(DetailView):
    """Muonekano wa oda: MTU HUWEZI kuona oda ya mwingine (404)."""
    model = Oda
    template_name = "oda_maelezo.html"
    context_object_name = "oda"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Oda.objects.all()
        return Oda.objects.filter(mtumiaji=self.request.user)


class BidhaaMpya(MauzajiWaBidhaa, CreateView):
    model = Bidhaa
    form_class = BidhaaForm
    template_name = "bidhaa_form.html"
    success_url = reverse_lazy("bidhaa_orodha")

    def form_valid(self, form):
        messages.success(self.request, "Bidhaa imeongezwa dukani")
        return super().form_valid(form)


class BidhaaHariri(MauzajiWaBidhaa, UpdateView):
    model = Bidhaa
    form_class = BidhaaForm
    template_name = "bidhaa_form.html"
    success_url = reverse_lazy("bidhaa_orodha")

    def form_valid(self, form):
        messages.success(self.request, "Bidhaa imehaririwa")
        return super().form_valid(form)


class BidhaaFuta(MauzajiWaBidhaa, DeleteView):
    model = Bidhaa
    template_name = "bidhaa_confirm_delete.html"
    success_url = reverse_lazy("bidhaa_orodha")

    def form_valid(self, form):
        messages.success(self.request, "Bidhaa imefutwa")
        return super().form_valid(form)
