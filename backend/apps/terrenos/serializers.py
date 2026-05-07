from rest_framework import serializers

from .models import FotografiaLote, Lote, Proyecto


class FotografiaLoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotografiaLote
        fields = ["id", "imagen", "descripcion", "orden", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class LoteSerializer(serializers.ModelSerializer):
    fotografias = FotografiaLoteSerializer(many=True, read_only=True)
    proyecto_nombre = serializers.CharField(source="proyecto.nombre", read_only=True)

    class Meta:
        model = Lote
        fields = [
            "id", "proyecto", "proyecto_nombre", "numero", "manzana",
            "medida_frente", "medida_fondo", "area_total",
            "num_finca", "folio", "libro", "precio_base",
            "estado", "coordenadas_lat", "coordenadas_lng",
            "notas", "fotografias", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class LoteListSerializer(serializers.ModelSerializer):
    proyecto_nombre = serializers.CharField(source="proyecto.nombre", read_only=True)

    class Meta:
        model = Lote
        fields = [
            "id", "proyecto", "proyecto_nombre", "numero", "manzana",
            "area_total", "precio_base", "estado",
        ]


class ProyectoSerializer(serializers.ModelSerializer):
    total_lotes = serializers.IntegerField(read_only=True)
    lotes_disponibles = serializers.IntegerField(read_only=True)
    lotes_vendidos = serializers.IntegerField(read_only=True)

    class Meta:
        model = Proyecto
        fields = [
            "id", "nombre", "ubicacion", "departamento", "municipio",
            "descripcion", "coordenadas_lat", "coordenadas_lng",
            "area_total", "is_active", "total_lotes",
            "lotes_disponibles", "lotes_vendidos",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
