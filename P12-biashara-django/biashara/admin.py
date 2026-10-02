from django.contrib import admin

from .models import Bidhaa, Kipengele, Lebo, Oda, OdaBidhaa


@admin.register(Lebo)
class LeboAdmin(admin.ModelAdmin):
    list_display = ["jina"]


@admin.register(Bidhaa)
class BidhaaAdmin(admin.ModelAdmin):
    list_display = ["jina", "bei", "stoo", "inauzwa"]
    list_filter = ["lebo"]
    search_fields = ["jina", "maelezo"]


class OdaBidhaaInline(admin.TabularInline):
    model = OdaBidhaa
    extra = 0
    readonly_fields = ["bidhaa", "jina_la_bidhaa", "bei", "idadi"]


@admin.register(Oda)
class OdaAdmin(admin.ModelAdmin):
    list_display = ["ref", "mtumiaji", "hali", "jumla",
                    "imeandikwa"]
    list_filter = ["hali", "njia"]
    inlines = [OdaBidhaaInline]


admin.site.register(Kipengele)
