from django.contrib import admin

from .models import FotografiaLote, Lote, Proyecto


class LoteInline(admin.TabularInline):
    model = Lote
    extra = 0
    fields = ["numero", "manzana", "area_total", "precio_base", "estado"]


class FotografiaInline(admin.TabularInline):
    model = FotografiaLote
    extra = 0


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "ubicacion", "departamento", "is_active", "created_at"]
    list_filter = ["departamento", "is_active"]
    search_fields = ["nombre", "ubicacion"]
    inlines = [LoteInline]


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ["__str__", "area_total", "precio_base", "estado"]
    list_filter = ["estado", "proyecto"]
    search_fields = ["numero", "manzana", "num_finca"]
    inlines = [FotografiaInline]
