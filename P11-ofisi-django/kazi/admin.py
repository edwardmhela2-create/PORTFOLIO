from django.contrib import admin

from .models import Barua, Kumbukumbu, Maombi


@admin.register(Maombi)
class MaombiAdmin(admin.ModelAdmin):
    list_display = ["pk", "aina", "mhusika", "hali",
                    "imetengenezwa"]
    list_filter = ["hali", "aina"]
    search_fields = ["maelezo", "mhusika__username"]


@admin.register(Barua)
class BaruaAdmin(admin.ModelAdmin):
    list_display = ["namba", "aina", "kichwa", "mhusika", "tarehe"]
    list_filter = ["aina"]
    search_fields = ["namba", "kichwa"]


@admin.register(Kumbukumbu)
class KumbukumbuAdmin(admin.ModelAdmin):
    list_display = ["tarehe", "mada", "alifanya"]
    list_filter = ["tarehe"]
    readonly_fields = ["tarehe"]
