from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView)
from django.urls import path

from . import views

urlpatterns = [
    path("", views.nyumbani, name="nyumbani"),
    path("ingia/", LoginView.as_view(template_name="ingia.html",
                                     redirect_authenticated_user=True),
         name="ingia"),
    path("toka/", LogoutView.as_view(), name="toka"),
    path("badilisha/",
         PasswordChangeView.as_view(
             template_name="badilisha.html",
             success_url="/badilisha/mafanikio/"),
         name="badilisha"),
    path("badilisha/mafanikio/",
         PasswordChangeDoneView.as_view(
             template_name="badilisha_mafanikio.html"),
         name="badilisha_mafanikio"),
    path("wateja/", views.wateja_orodha, name="wateja_orodha"),
    path("wateja/ongeza/", views.wateja_ongeza, name="wateja_ongeza"),
    path("wateja/<int:pk>/futa/", views.wateja_futa, name="wateja_futa"),
    path("akaunti/", views.akaunti_orodha, name="akaunti_orodha"),
    path("akaunti/<int:wateja_pk>/fungua/", views.akaunti_fungua,
         name="akaunti_fungua"),
    path("fedha/", views.fedha, name="fedha"),
    path("jedwali/", views.jedwali, name="jedwali"),
    path("mikopo/", views.mikopo_orodha, name="mikopo_orodha"),
    path("mikopo/ongeza/", views.mkopo_ongeza, name="mkopo_ongeza"),
    path("mikopo/<int:pk>/lipa/", views.mkopo_lipa, name="mkopo_lipa"),
    path("ripoti/", views.ripoti, name="ripoti"),
]
