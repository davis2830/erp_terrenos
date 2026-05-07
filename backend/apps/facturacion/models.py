from django.db import models

from utils.mixins import TimestampMixin


class Factura(TimestampMixin):
    """Factura electrónica emitida vía FEL/SAT."""

    class Estado(models.TextChoices):
        EMITIDA = "emitida", "Emitida"
        ANULADA = "anulada", "Anulada"
        ERROR = "error", "Error"

    venta = models.ForeignKey(
        "finanzas.Venta",
        on_delete=models.PROTECT,
        related_name="facturas",
        verbose_name="Venta",
    )
    abono = models.ForeignKey(
        "finanzas.Abono",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="facturas",
        verbose_name="Abono asociado",
    )
    numero_fel = models.CharField(max_length=100, blank=True, verbose_name="Número FEL")
    serie = models.CharField(max_length=50, blank=True, verbose_name="Serie")
    numero_autorizacion = models.CharField(max_length=200, blank=True, verbose_name="Número de autorización")
    fecha_emision = models.DateTimeField(verbose_name="Fecha de emisión")
    monto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto (Q)")
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.EMITIDA,
        verbose_name="Estado",
    )
    xml_fel = models.TextField(blank=True, verbose_name="XML FEL")
    pdf_url = models.URLField(blank=True, verbose_name="URL del PDF")
    error_detalle = models.TextField(blank=True, verbose_name="Detalle de error")

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ["-fecha_emision"]

    def __str__(self):
        return f"Factura {self.serie}-{self.numero_fel}"


class DocumentoLegal(TimestampMixin):
    """Documentos legales asociados a un cliente."""

    class TipoDocumento(models.TextChoices):
        DPI = "dpi", "DPI"
        RTU = "rtu", "RTU"
        PROMESA_CV = "promesa_cv", "Promesa de Compra-Venta"
        ESCRITURA = "escritura", "Escritura"
        OTRO = "otro", "Otro"

    cliente = models.ForeignKey(
        "crm.Cliente",
        on_delete=models.CASCADE,
        related_name="documentos_legales",
        verbose_name="Cliente",
    )
    tipo = models.CharField(
        max_length=20,
        choices=TipoDocumento.choices,
        verbose_name="Tipo de documento",
    )
    archivo = models.FileField(upload_to="documentos_legales/", verbose_name="Archivo")
    descripcion = models.CharField(max_length=200, blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Documento legal"
        verbose_name_plural = "Documentos legales"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.cliente}"


class PlantillaContrato(TimestampMixin):
    """Plantillas para generar contratos automáticamente."""

    nombre = models.CharField(max_length=200, verbose_name="Nombre de la plantilla")
    contenido_template = models.TextField(
        verbose_name="Contenido de la plantilla",
        help_text="Usa variables como {{cliente_nombre}}, {{lote_numero}}, {{precio_venta}}, etc.",
    )
    variables_requeridas = models.JSONField(
        default=list,
        verbose_name="Variables requeridas",
        help_text="Lista de nombres de variables que se deben reemplazar en la plantilla.",
    )
    is_active = models.BooleanField(default=True, verbose_name="Activa")

    class Meta:
        verbose_name = "Plantilla de contrato"
        verbose_name_plural = "Plantillas de contratos"

    def __str__(self):
        return self.nombre
