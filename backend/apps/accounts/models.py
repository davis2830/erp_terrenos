from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.mixins import TimestampMixin


class User(AbstractUser):
    """Usuario personalizado con roles para el sistema inmobiliario."""

    class Role(models.TextChoices):
        ADMIN = "admin", "Administrador"
        GERENTE = "gerente", "Gerente"
        VENDEDOR = "vendedor", "Vendedor"

    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VENDEDOR,
        verbose_name="Rol",
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    @property
    def is_admin_or_gerente(self):
        return self.role in (self.Role.ADMIN, self.Role.GERENTE)


class AuditLog(TimestampMixin):
    """Bitácora de acciones críticas del sistema."""

    class Action(models.TextChoices):
        CREATE = "create", "Crear"
        UPDATE = "update", "Actualizar"
        DELETE = "delete", "Eliminar"
        LOGIN = "login", "Inicio de sesión"
        PRICE_CHANGE = "price_change", "Cambio de precio"
        STATUS_CHANGE = "status_change", "Cambio de estado"
        CANCEL = "cancel", "Cancelación"

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="audit_logs",
        verbose_name="Usuario",
    )
    action = models.CharField(max_length=30, choices=Action.choices, verbose_name="Acción")
    model_name = models.CharField(max_length=100, verbose_name="Modelo")
    object_id = models.PositiveIntegerField(verbose_name="ID del objeto")
    details = models.JSONField(default=dict, blank=True, verbose_name="Detalles")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Dirección IP")

    class Meta:
        verbose_name = "Registro de auditoría"
        verbose_name_plural = "Registros de auditoría"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}#{self.object_id}"
