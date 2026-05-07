from django.db import models

from utils.mixins import TimestampMixin


class MapaProyecto(TimestampMixin):
    """Mapa SVG interactivo de un proyecto de lotificación."""

    proyecto = models.OneToOneField(
        "terrenos.Proyecto",
        on_delete=models.CASCADE,
        related_name="mapa",
        verbose_name="Proyecto",
    )
    svg_data = models.TextField(verbose_name="Datos SVG del mapa")
    configuracion_colores = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Configuración de colores",
        help_text="Colores por estado: {'disponible': '#22c55e', 'reservado': '#f59e0b', 'vendido': '#ef4444'}",
    )
    ancho = models.PositiveIntegerField(default=800, verbose_name="Ancho (px)")
    alto = models.PositiveIntegerField(default=600, verbose_name="Alto (px)")

    class Meta:
        verbose_name = "Mapa de proyecto"
        verbose_name_plural = "Mapas de proyectos"

    def __str__(self):
        return f"Mapa - {self.proyecto.nombre}"


class CoordenadaLote(models.Model):
    """Coordenadas SVG de un lote dentro del mapa del proyecto."""

    mapa = models.ForeignKey(
        MapaProyecto,
        on_delete=models.CASCADE,
        related_name="coordenadas",
        verbose_name="Mapa",
    )
    lote = models.OneToOneField(
        "terrenos.Lote",
        on_delete=models.CASCADE,
        related_name="coordenada_mapa",
        verbose_name="Lote",
    )
    svg_path = models.TextField(
        verbose_name="Path SVG",
        help_text="Coordenadas del polígono SVG que representa el lote en el mapa.",
    )

    class Meta:
        verbose_name = "Coordenada de lote en mapa"
        verbose_name_plural = "Coordenadas de lotes en mapa"

    def __str__(self):
        return f"Coordenada - {self.lote}"
