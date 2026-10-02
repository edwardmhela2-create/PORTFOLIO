from django.contrib import admin

from .models import Akaunti, Miamala, Mkopo, Wateja


@admin.register(Wateja)
class WatejaAdmin(admin.ModelAdmin):
    list_display = ["jina", "simu", "anwani", "imesajiliwa"]
    search_fields = ["jina", "simu"]


@admin.register(Akaunti)
class AkauntiAdmin(admin.ModelAdmin):
    list_display = ["namba", "wateja", "aina", "salio"]
    list_filter = ["aina"]
    search_fields = ["namba", "wateja__jina"]


@admin.register(Miamala)
class MiamalaAdmin(admin.ModelAdmin):
    list_display = ["tarehe", "aina", "kiasi", "akaunti", "alifanya"]
    list_filter = ["aina"]


@admin.register(Mkopo)
class MkopoAdmin(admin.ModelAdmin):
    list_display = ["wateja", "kiasi", "riba_asilimia", "salio", "hali"]
    list_filter = ["hali"]
