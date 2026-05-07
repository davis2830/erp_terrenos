from django.db import models
from django.conf import settings

from utils.mixins import AuditMixin, TimestampMixin


class Venta(AuditMixin):
    """Registro de venta de un lote a un cliente."""

    class Estado(models.TextChoices):
        ACTIVA = "activa", "Activa"
        COMPLETADA = "completada", "Completada"
        CANCELADA = "cancelada", "Cancelada"

    lote = models.OneToOneField(
        "terrenos.Lote",
        on_delete=models.PROTECT,
        related_name="venta",
        verbose_name="Lote",
    )
    cliente = models.ForeignKey(
        "crm.Cliente",
        on_delete=models.PROTECT,
        related_name="ventas",
        verbose_name="Cliente",
    )
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ventas_realizadas",
        verbose_name="Vendedor",
    )
    reserva = models.OneToOneField(
        "crm.Reserva",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="venta",
        verbose_name="Reserva origen",
    )
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio de venta (Q)")
    enganche = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Enganche (Q)")
    plazo_meses = models.PositiveIntegerField(verbose_name="Plazo (meses)")
    tasa_interes = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, verbose_name="Tasa de interés anual (%)"
    )
    fecha_venta = models.DateField(verbose_name="Fecha de venta")
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.ACTIVA,
        db_index=True,
        verbose_name="Estado",
    )
    notas = models.TextField(blank=True, verbose_name="Notas")

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ["-fecha_venta"]

    def __str__(self):
        return f"Venta {self.lote} → {self.cliente}"

    @property
    def monto_financiado(self):
        return self.precio_venta - self.enganche


class PlanPago(TimestampMixin):
    """Plan de pagos generado para una venta a plazos."""

    venta = models.OneToOneField(
        Venta,
        on_delete=models.CASCADE,
        related_name="plan_pago",
        verbose_name="Venta",
    )
    cuota_mensual = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Cuota mensual (Q)")
    total_cuotas = models.PositiveIntegerField(verbose_name="Total de cuotas")
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Saldo pendiente (Q)")

    class Meta:
        verbose_name = "Plan de pago"
        verbose_name_plural = "Planes de pago"

    def __str__(self):
        return f"Plan - {self.venta}"


class Cuota(models.Model):
    """Cuota individual dentro de un plan de pagos."""

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        PAGADA = "pagada", "Pagada"
        MORA = "mora", "En mora"
        PARCIAL = "parcial", "Pago parcial"

    plan_pago = models.ForeignKey(
        PlanPago,
        on_delete=models.CASCADE,
        related_name="cuotas",
        verbose_name="Plan de pago",
    )
    numero = models.PositiveIntegerField(verbose_name="Número de cuota")
    monto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto (Q)")
    monto_capital = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Capital (Q)"
    )
    monto_interes = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Interés (Q)"
    )
    fecha_vencimiento = models.DateField(verbose_name="Fecha de vencimiento")
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
        db_index=True,
        verbose_name="Estado",
    )
    saldo_restante = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Saldo restante (Q)"
    )

    class Meta:
        verbose_name = "Cuota"
        verbose_name_plural = "Cuotas"
        ordering = ["plan_pago", "numero"]
        unique_together = ["plan_pago", "numero"]

    def __str__(self):
        return f"Cuota {self.numero}/{self.plan_pago.total_cuotas} - {self.plan_pago.venta}"


class Abono(TimestampMixin):
    """Registro de un pago/abono a una cuota."""

    class MetodoPago(models.TextChoices):
        EFECTIVO = "efectivo", "Efectivo"
        TRANSFERENCIA = "transferencia", "Transferencia bancaria"
        CHEQUE = "cheque", "Cheque"
        DEPOSITO = "deposito", "Depósito bancario"
        OTRO = "otro", "Otro"

    cuota = models.ForeignKey(
        Cuota,
        on_delete=models.PROTECT,
        related_name="abonos",
        verbose_name="Cuota",
    )
    monto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto abonado (Q)")
    fecha_pago = models.DateField(verbose_name="Fecha de pago")
    metodo_pago = models.CharField(
        max_length=20,
        choices=MetodoPago.choices,
        default=MetodoPago.EFECTIVO,
        verbose_name="Método de pago",
    )
    comprobante = models.FileField(
        upload_to="comprobantes/", blank=True, null=True, verbose_name="Comprobante"
    )
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="abonos_registrados",
        verbose_name="Registrado por",
    )
    notas = models.TextField(blank=True, verbose_name="Notas")

    class Meta:
        verbose_name = "Abono"
        verbose_name_plural = "Abonos"
        ordering = ["-fecha_pago"]

    def __str__(self):
        return f"Abono Q{self.monto} - {self.cuota}"
