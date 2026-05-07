from django.contrib import admin

from .models import Abono, Cuota, PlanPago, Venta


class CuotaInline(admin.TabularInline):
    model = Cuota
    extra = 0
    fields = ["numero", "monto", "fecha_vencimiento", "estado"]


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ["lote", "cliente", "vendedor", "precio_venta", "estado", "fecha_venta"]
    list_filter = ["estado"]
    search_fields = ["cliente__nombre", "cliente__apellido", "lote__numero"]


@admin.register(PlanPago)
class PlanPagoAdmin(admin.ModelAdmin):
    list_display = ["venta", "cuota_mensual", "total_cuotas", "saldo_pendiente"]
    inlines = [CuotaInline]


@admin.register(Abono)
class AbonoAdmin(admin.ModelAdmin):
    list_display = ["cuota", "monto", "fecha_pago", "metodo_pago", "registrado_por"]
    list_filter = ["metodo_pago"]
