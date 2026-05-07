from django.contrib import admin

from .models import CoordenadaLote, MapaProyecto


class CoordenadaInline(admin.TabularInline):
    model = CoordenadaLote
    extra = 0


@admin.register(MapaProyecto)
class MapaProyectoAdmin(admin.ModelAdmin):
    list_display = ["proyecto", "ancho", "alto", "created_at"]
    inlines = [CoordenadaInline]
