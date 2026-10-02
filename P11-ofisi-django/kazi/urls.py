from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.nyumbani, name="nyumbani"),
    path("ingia/", LoginView.as_view(template_name="ingia.html",
                                     redirect_authenticated_user=True),
         name="ingia"),
    path("toka/", LogoutView.as_view(), name="toka"),
    path("maombi/", views.MaombiOrodha.as_view(), name="maombi"),
    path("maombi/mpya/", views.MaombiMpya.as_view(),
         name="maombi_mpya"),
    path("maombi/<int:pk>/", views.MaombiMaelezo.as_view(),
         name="maombi_maelezo"),
    path("maombi/<int:pk>/wasilisha/", views.maombi_wasilisha,
         name="maombi_wasilisha"),
    path("maombi/<int:pk>/kagua/", views.maombi_kagua,
         name="maombi_kagua"),
    path("maombi/<int:pk>/futa/", views.maombi_futa,
         name="maombi_futa"),
    path("barua/", views.BaruaOrodha.as_view(), name="barua"),
    path("barua/mpya/", views.BaruaMpya.as_view(), name="barua_mpya"),
    path("ripoti/", views.ripoti, name="ripoti"),
    path("ripoti/csv/", views.ripoti_csv, name="ripoti_csv"),
    path("kumbukumbu/", views.kumbukumbu_orodha,
         name="kumbukumbu_orodha"),
]
