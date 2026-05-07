from django.db import models

from utils.mixins import AuditMixin


class Proyecto(AuditMixin):
    """Proyecto de lotificación (una o más manzanas con lotes)."""

    nombre = models.CharField(max_length=200, verbose_name="Nombre del proyecto")
    ubicacion = models.CharField(max_length=300, verbose_name="Ubicación")
    departamento = models.CharField(max_length=100, default="Petén", verbose_name="Departamento")
    municipio = models.CharField(max_length=100, blank=True, verbose_name="Municipio")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    coordenadas_lat = models.DecimalField(
        max_digits=10, decimal_places=7, null=True, blank=True, verbose_name="Latitud"
    )
    coordenadas_lng = models.DecimalField(
        max_digits=10, decimal_places=7, null=True, blank=True, verbose_name="Longitud"
    )
    area_total = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Área total (m²)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.nombre

    @property
    def total_lotes(self):
        return self.lotes.count()

    @property
    def lotes_disponibles(self):
        return self.lotes.filter(estado=Lote.Estado.DISPONIBLE).count()

    @property
    def lotes_vendidos(self):
        return self.lotes.filter(estado=Lote.Estado.VENDIDO).count()


class Lote(AuditMixin):
    """Terreno individual dentro de un proyecto."""

    class Estado(models.TextChoices):
        DISPONIBLE = "disponible", "Disponible"
        RESERVADO = "reservado", "Reservado"
        VENDIDO = "vendido", "Vendido"

    proyecto = models.ForeignKey(
        Proyecto, on_delete=models.CASCADE, related_name="lotes", verbose_name="Proyecto"
    )
    numero = models.CharField(max_length=20, verbose_name="Número de lote")
    manzana = models.CharField(max_length=20, blank=True, verbose_name="Manzana")
    medida_frente = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Medida frente (m)"
    )
    medida_fondo = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Medida fondo (m)"
    )
    area_total = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Área total (m²)"
    )
    num_finca = models.CharField(max_length=50, blank=True, verbose_name="Número de finca")
    folio = models.CharField(max_length=50, blank=True, verbose_name="Folio")
    libro = models.CharField(max_length=50, blank=True, verbose_name="Libro")
    precio_base = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Precio base (Q)"
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.DISPONIBLE,
        db_index=True,
        verbose_name="Estado",
    )
    coordenadas_lat = models.DecimalField(
        max_digits=10, decimal_places=7, null=True, blank=True, verbose_name="Latitud"
    )
    coordenadas_lng = models.DecimalField(
        max_digits=10, decimal_places=7, null=True, blank=True, verbose_name="Longitud"
    )
    notas = models.TextField(blank=True, verbose_name="Notas")

    class Meta:
        verbose_name = "Lote"
        verbose_name_plural = "Lotes"
        ordering = ["proyecto", "manzana", "numero"]
        unique_together = ["proyecto", "manzana", "numero"]

    def __str__(self):
        mz = f"Mz.{self.manzana} " if self.manzana else ""
        return f"{self.proyecto.nombre} - {mz}Lote {self.numero}"


class FotografiaLote(models.Model):
    """Fotografías o planos asociados a un lote."""

    lote = models.ForeignKey(
        Lote, on_delete=models.CASCADE, related_name="fotografias", verbose_name="Lote"
    )
    imagen = models.ImageField(upload_to="lotes/fotos/", verbose_name="Imagen")
    descripcion = models.CharField(max_length=200, blank=True, verbose_name="Descripción")
    orden = models.PositiveSmallIntegerField(default=0, verbose_name="Orden")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fotografía de lote"
        verbose_name_plural = "Fotografías de lotes"
        ordering = ["orden"]

    def __str__(self):
        return f"Foto {self.orden} - {self.lote}"
