from django.db import models


class TimestampMixin(models.Model):
    """Agrega campos de fecha de creación y actualización."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        abstract = True


class AuditMixin(TimestampMixin):
    """Extiende TimestampMixin con campos de auditoría de usuario."""

    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        verbose_name="Creado por",
    )
    updated_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        verbose_name="Actualizado por",
    )

    class Meta:
        abstract = True
