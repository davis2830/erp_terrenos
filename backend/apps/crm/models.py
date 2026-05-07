from django.db import models
from django.conf import settings

from utils.mixins import AuditMixin, TimestampMixin


class Cliente(AuditMixin):
    """Cliente interesado en la compra de terrenos."""

    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    dpi = models.CharField(max_length=20, unique=True, verbose_name="DPI")
    nit = models.CharField(max_length=20, blank=True, verbose_name="NIT")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Correo electrónico")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    notas = models.TextField(blank=True, verbose_name="Notas")
    vendedor_asignado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clientes_asignados",
        verbose_name="Vendedor asignado",
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def whatsapp_link(self):
        phone = self.telefono.replace(" ", "").replace("-", "")
        if not phone.startswith("+"):
            phone = f"+502{phone}"
        return f"https://wa.me/{phone}"


class Reserva(TimestampMixin):
    """Reserva temporal de un lote para un cliente."""

    class Estado(models.TextChoices):
        ACTIVA = "activa", "Activa"
        CONCRETADA = "concretada", "Concretada"
        EXPIRADA = "expirada", "Expirada"
        CANCELADA = "cancelada", "Cancelada"

    lote = models.ForeignKey(
        "terrenos.Lote",
        on_delete=models.PROTECT,
        related_name="reservas",
        verbose_name="Lote",
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="reservas",
        verbose_name="Cliente",
    )
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reservas_realizadas",
        verbose_name="Vendedor",
    )
    fecha_expiracion = models.DateTimeField(verbose_name="Fecha de expiración")
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.ACTIVA,
        db_index=True,
        verbose_name="Estado",
    )
    enganche_acordado = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Enganche acordado (Q)"
    )
    notas = models.TextField(blank=True, verbose_name="Notas")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reserva {self.lote} - {self.cliente}"


class SeguimientoCliente(TimestampMixin):
    """Registro de seguimiento/contacto con un cliente."""

    class TipoContacto(models.TextChoices):
        LLAMADA = "llamada", "Llamada"
        WHATSAPP = "whatsapp", "WhatsApp"
        VISITA = "visita", "Visita en campo"
        EMAIL = "email", "Correo electrónico"
        OTRO = "otro", "Otro"

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="seguimientos",
        verbose_name="Cliente",
    )
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="seguimientos_realizados",
        verbose_name="Vendedor",
    )
    tipo_contacto = models.CharField(
        max_length=20, choices=TipoContacto.choices, verbose_name="Tipo de contacto"
    )
    descripcion = models.TextField(verbose_name="Descripción")
    fecha_proximo_contacto = models.DateTimeField(
        null=True, blank=True, verbose_name="Próximo contacto"
    )

    class Meta:
        verbose_name = "Seguimiento de cliente"
        verbose_name_plural = "Seguimientos de clientes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tipo_contacto} - {self.cliente} ({self.created_at:%d/%m/%Y})"
