from django.contrib import admin

from .models import NotificacionEnviada, PlantillaMensaje


@admin.register(PlantillaMensaje)
class PlantillaMensajeAdmin(admin.ModelAdmin):
    list_display = ["nombre", "tipo", "is_active", "created_at"]
    list_filter = ["tipo", "is_active"]


@admin.register(NotificacionEnviada)
class NotificacionEnviadaAdmin(admin.ModelAdmin):
    list_display = ["cliente", "canal", "estado", "created_at"]
    list_filter = ["canal", "estado"]
    search_fields = ["cliente__nombre", "cliente__apellido", "telefono_destino"]
