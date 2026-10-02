import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from .decorators import MtumiajiWaOfisi, linahitaji_jukumu
from .forms import BaruaForm, KaguaForm, MaombiForm
from .models import Barua, Kumbukumbu, Maombi


def nyumbani(request):
    if request.user.is_authenticated:
        return redirect("maombi")
    return render(request, "landing.html")


class MaombiOrodha(MtumiajiWaOfisi, ListView):
    model = Maombi
    template_name = "maombi_list.html"
    context_object_name = "maombi"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        hali = self.request.GET.get("hali", "")
        m = Maombi.objects.select_related("mhusika")
        if q:
            m = m.filter(Q(maelezo__icontains=q)
                         | Q(aina__icontains=q)
                         | Q(mhusika__username__icontains=q))
        if hali:
            m = m.filter(hali=hali)
        return m


class MaombiMaelezo(MtumiajiWaOfisi, DetailView):
    model = Maombi
    template_name = "maombi_detail.html"
    context_object_name = "m"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        u = self.request.user
        ctx["ni_mwombaji"] = (u.is_superuser
                              or self.object.mhusika_id == u.pk)
        ctx["ni_meneja"] = (u.is_superuser
                            or u.groups.filter(name="meneja").exists())
        ctx["fomu_kagua"] = KaguaForm()
        return ctx


class MaombiMpya(MtumiajiWaOfisi, CreateView):
    form_class = MaombiForm
    template_name = "maombi_form.html"

    def form_valid(self, form):
        form.instance.mhusika = self.request.user
        messages.success(
            self.request,
            "Rasimu limehifadhiwa - sasa libonyeze 'Wasilisha'")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("maombi_maelezo", args=[self.object.pk])


@login_required
def maombi_wasilisha(request, pk):
    m = get_object_or_404(Maombi, pk=pk)
    if m.mhusika_id != request.user.pk and not request.user.is_superuser:
        raise PermissionDenied("Haya si maombi yako")
    if request.method != "POST":
        return redirect("maombi_maelezo", pk=pk)
    try:
        m.wasilisha(request.user)
        messages.success(
            request,
            "Maombi #%s yamewasilishwa - sanaa meneja yakague"
            % m.pk)
    except ValidationError as e:
        messages.error(request, "; ".join(e.messages))
    return redirect("maombi_maelezo", pk=pk)


@login_required
def maombi_kagua(request, pk):
    if not (request.user.is_superuser
            or request.user.groups.filter(name="meneja").exists()):
        raise PermissionDenied("Kukagua ni kazi ya meneja")
    m = get_object_or_404(Maombi, pk=pk)
    if request.method != "POST":
        return redirect("maombi_maelezo", pk=pk)
    amri = request.POST.get("amri", "")
    maoni = request.POST.get("maoni", "").strip()
    try:
        m.kagua(request.user, idhini=(amri == "idhini"), maoni=maoni)
        messages.success(request, "Maombi #%s: %s"
                         % (m.pk, m.get_hali_display()))
    except ValidationError as e:
        messages.error(request, "; ".join(e.messages))
    return redirect("maombi_maelezo", pk=pk)


@login_required
def maombi_futa(request, pk):
    m = get_object_or_404(Maombi, pk=pk)
    if m.mhusika_id != request.user.pk and not request.user.is_superuser:
        raise PermissionDenied("Haya si maombi yako")
    if request.method != "POST":
        return redirect("maombi_maelezo", pk=pk)
    if m.hali != "rasimu":
        messages.error(request,
                       "Ni RASIMU pekee zinazoweza kufutwa (hali: %s)"
                       % m.get_hali_display())
    else:
        m.delete()
        messages.warning(request, "Rasimu limefutwa")
    return redirect("maombi")


class BaruaOrodha(MtumiajiWaOfisi, ListView):
    model = Barua
    template_name = "barua_list.html"
    context_object_name = "barua"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        b = Barua.objects.select_related("aliwasilisha")
        if q:
            b = b.filter(Q(kichwa__icontains=q)
                         | Q(namba__icontains=q)
                         | Q(mhusika__icontains=q))
        return b


class BaruaMpya(MtumiajiWaOfisi, CreateView):
    form_class = BaruaForm
    template_name = "barua_form.html"

    def dispatch(self, request, *args, **kwargs):
        if (request.user.is_authenticated
                and not (request.user.is_superuser
                         or request.user.groups.filter(
                             name="rejista").exists())):
            raise PermissionDenied(
                "Kurejistra barua ni kazi ya REJISTA pekee")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.aliwasilisha = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request,
            "Barua %s imerejistrwa" % form.instance.namba)
        return response

    def get_success_url(self):
        return reverse("barua")


@linahitaji_jukumu("meneja")
def ripoti(request):
    takwimu = [{"hali": h, "jina": j,
                "idadi": Maombi.objects.filter(hali=h).count()}
               for h, j in Maombi.HALI]
    return render(request, "ripoti.html", {
        "takwimu": takwimu,
        "jumla": Maombi.objects.count(),
        "barua_jumla": Barua.objects.count(),
        "karibuni": Kumbukumbu.objects.select_related(
            "alifanya")[:10],
    })


@linahitaji_jukumu("meneja")
def ripoti_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="ripoti-maombi.csv"')
    response.write("\ufeff")  # BOM - Excel iweze kusoma Kiswahili
    w = csv.writer(response)
    w.writerow(["Id", "Aina", "Mombaji", "Hali", "Imewasilishwa",
                "Imeamuliwa", "Maoni"])
    for m in Maombi.objects.select_related("mhusika").iterator():
        w.writerow([m.pk, m.get_aina_display(), m.mhusika.username,
                    m.get_hali_display(),
                    m.imewasilishwa or "", m.imeamuliwa or "",
                    m.maoni])
    return response


@linahitaji_jukumu("meneja")
def kumbukumbu_orodha(request):
    return render(request, "kumbukumbu_list.html", {
        "kumbukumbu": Kumbukumbu.objects.select_related(
            "alifanya", "maombi")[:50]})
