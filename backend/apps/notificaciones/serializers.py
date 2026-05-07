from rest_framework import serializers

from .models import NotificacionEnviada, PlantillaMensaje


class PlantillaMensajeSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)

    class Meta:
        model = PlantillaMensaje
        fields = [
            "id", "nombre", "tipo", "tipo_display",
            "contenido", "is_active", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class NotificacionEnviadaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source="cliente.nombre_completo", read_only=True)

    class Meta:
        model = NotificacionEnviada
        fields = [
            "id", "cliente", "cliente_nombre", "plantilla",
            "canal", "mensaje_enviado", "telefono_destino",
            "estado", "twilio_sid", "error_detalle", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class EnviarMensajeSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField()
    plantilla_id = serializers.IntegerField(required=False)
    mensaje = serializers.CharField(required=False)
    canal = serializers.ChoiceField(
        choices=NotificacionEnviada.Canal.choices,
        default=NotificacionEnviada.Canal.WHATSAPP,
    )
