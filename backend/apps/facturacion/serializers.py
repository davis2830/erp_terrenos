from rest_framework import serializers

from .models import DocumentoLegal, Factura, PlantillaContrato


class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = [
            "id", "venta", "abono", "numero_fel", "serie",
            "numero_autorizacion", "fecha_emision", "monto",
            "estado", "pdf_url", "error_detalle", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class DocumentoLegalSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)

    class Meta:
        model = DocumentoLegal
        fields = [
            "id", "cliente", "tipo", "tipo_display",
            "archivo", "descripcion", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class PlantillaContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantillaContrato
        fields = [
            "id", "nombre", "contenido_template",
            "variables_requeridas", "is_active", "created_at",
        ]
        read_only_fields = ["id", "created_at"]
