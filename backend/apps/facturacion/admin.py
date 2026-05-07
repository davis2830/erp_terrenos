from django.contrib import admin

from .models import DocumentoLegal, Factura, PlantillaContrato


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ["__str__", "venta", "monto", "estado", "fecha_emision"]
    list_filter = ["estado"]
    search_fields = ["numero_fel", "serie"]


@admin.register(DocumentoLegal)
class DocumentoLegalAdmin(admin.ModelAdmin):
    list_display = ["cliente", "tipo", "descripcion", "created_at"]
    list_filter = ["tipo"]


@admin.register(PlantillaContrato)
class PlantillaContratoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "is_active", "created_at"]
    list_filter = ["is_active"]
