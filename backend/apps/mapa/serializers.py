from rest_framework import serializers

from .models import CoordenadaLote, MapaProyecto


class CoordenadaLoteSerializer(serializers.ModelSerializer):
    lote_numero = serializers.CharField(source="lote.numero", read_only=True)
    lote_estado = serializers.CharField(source="lote.estado", read_only=True)
    lote_precio = serializers.DecimalField(
        source="lote.precio_base", max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = CoordenadaLote
        fields = ["id", "lote", "lote_numero", "lote_estado", "lote_precio", "svg_path"]


class MapaProyectoSerializer(serializers.ModelSerializer):
    coordenadas = CoordenadaLoteSerializer(many=True, read_only=True)
    proyecto_nombre = serializers.CharField(source="proyecto.nombre", read_only=True)

    class Meta:
        model = MapaProyecto
        fields = [
            "id", "proyecto", "proyecto_nombre", "svg_data",
            "configuracion_colores", "ancho", "alto",
            "coordenadas", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
