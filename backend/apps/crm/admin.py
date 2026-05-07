from django.contrib import admin

from .models import Cliente, Reserva, SeguimientoCliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["nombre_completo", "dpi", "telefono", "vendedor_asignado", "created_at"]
    list_filter = ["vendedor_asignado"]
    search_fields = ["nombre", "apellido", "dpi", "nit", "telefono"]


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ["lote", "cliente", "vendedor", "estado", "fecha_expiracion"]
    list_filter = ["estado"]
    search_fields = ["cliente__nombre", "cliente__apellido", "lote__numero"]


@admin.register(SeguimientoCliente)
class SeguimientoClienteAdmin(admin.ModelAdmin):
    list_display = ["cliente", "vendedor", "tipo_contacto", "created_at"]
    list_filter = ["tipo_contacto"]
