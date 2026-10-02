from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.BidhaaOrodha.as_view(), name="bidhaa_orodha"),
    path("bidhaa/mpya/", views.BidhaaMpya.as_view(),
         name="bidhaa_mpya"),
    path("bidhaa/<int:pk>/", views.BidhaaMaelezo.as_view(),
         name="bidhaa_maelezo"),
    path("bidhaa/<int:pk>/hariri/", views.BidhaaHariri.as_view(),
         name="bidhaa_hariri"),
    path("bidhaa/<int:pk>/futa/", views.BidhaaFuta.as_view(),
         name="bidhaa_futa"),
    path("kikapu/", views.kikapu, name="kikapu"),
    path("kikapu/ongeza/<int:pk>/", views.kikapu_ongeza,
         name="kikapu_ongeza"),
    path("kikapu/badilisha/<int:pk>/", views.kikapu_badilisha,
         name="kikapu_badilisha"),
    path("kikapu/futa/<int:pk>/", views.kikapu_futa,
         name="kikapu_futa"),
    path("lipa/", views.lipa, name="lipa"),
    path("oda/", views.oda_orodha, name="oda_orodha"),
    path("oda/<int:pk>/", views.OdaMaelezo.as_view(),
         name="oda_maelezo"),
    path("ingia/", LoginView.as_view(template_name="ingia.html"),
         name="ingia"),
    path("toka/", LogoutView.as_view(), name="toka"),
]
