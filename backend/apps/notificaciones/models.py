from django.db import models

from utils.mixins import TimestampMixin


class PlantillaMensaje(TimestampMixin):
    """Plantillas de mensajes predefinidos para WhatsApp/SMS."""

    class TipoPlantilla(models.TextChoices):
        RECORDATORIO_PAGO = "recordatorio_pago", "Recordatorio de pago"
        RESERVA_EXPIRA = "reserva_expira", "Reserva por expirar"
        BIENVENIDA = "bienvenida", "Bienvenida"
        CONFIRMACION_PAGO = "confirmacion_pago", "Confirmación de pago"
        SEGUIMIENTO = "seguimiento", "Seguimiento"
        PERSONALIZADO = "personalizado", "Personalizado"

    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    tipo = models.CharField(
        max_length=30,
        choices=TipoPlantilla.choices,
        verbose_name="Tipo",
    )
    contenido = models.TextField(
        verbose_name="Contenido",
        help_text="Usa variables como {{cliente_nombre}}, {{monto}}, {{fecha_vencimiento}}, etc.",
    )
    is_active = models.BooleanField(default=True, verbose_name="Activa")

    class Meta:
        verbose_name = "Plantilla de mensaje"
        verbose_name_plural = "Plantillas de mensajes"

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class NotificacionEnviada(TimestampMixin):
    """Registro de notificaciones enviadas."""

    class Canal(models.TextChoices):
        WHATSAPP = "whatsapp", "WhatsApp"
        SMS = "sms", "SMS"

    class Estado(models.TextChoices):
        ENVIADA = "enviada", "Enviada"
        ENTREGADA = "entregada", "Entregada"
        FALLIDA = "fallida", "Fallida"
        PENDIENTE = "pendiente", "Pendiente"

    cliente = models.ForeignKey(
        "crm.Cliente",
        on_delete=models.CASCADE,
        related_name="notificaciones",
        verbose_name="Cliente",
    )
    plantilla = models.ForeignKey(
        PlantillaMensaje,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="envios",
        verbose_name="Plantilla",
    )
    canal = models.CharField(
        max_length=20,
        choices=Canal.choices,
        default=Canal.WHATSAPP,
        verbose_name="Canal",
    )
    mensaje_enviado = models.TextField(verbose_name="Mensaje enviado")
    telefono_destino = models.CharField(max_length=20, verbose_name="Teléfono destino")
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
        verbose_name="Estado",
    )
    twilio_sid = models.CharField(max_length=100, blank=True, verbose_name="Twilio SID")
    error_detalle = models.TextField(blank=True, verbose_name="Detalle de error")

    class Meta:
        verbose_name = "Notificación enviada"
        verbose_name_plural = "Notificaciones enviadas"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.canal} → {self.cliente} ({self.estado})"
