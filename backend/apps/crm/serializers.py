from rest_framework import serializers

from .models import Cliente, Reserva, SeguimientoCliente


class ClienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.CharField(read_only=True)
    whatsapp_link = serializers.CharField(read_only=True)
    vendedor_nombre = serializers.CharField(
        source="vendedor_asignado.get_full_name", read_only=True
    )

    class Meta:
        model = Cliente
        fields = [
            "id", "nombre", "apellido", "nombre_completo", "dpi", "nit",
            "telefono", "email", "direccion", "notas",
            "vendedor_asignado", "vendedor_nombre", "whatsapp_link",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ReservaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source="cliente.nombre_completo", read_only=True)
    lote_info = serializers.CharField(source="lote.__str__", read_only=True)
    vendedor_nombre = serializers.CharField(source="vendedor.get_full_name", read_only=True)

    class Meta:
        model = Reserva
        fields = [
            "id", "lote", "lote_info", "cliente", "cliente_nombre",
            "vendedor", "vendedor_nombre", "fecha_expiracion",
            "estado", "enganche_acordado", "notas",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class SeguimientoClienteSerializer(serializers.ModelSerializer):
    vendedor_nombre = serializers.CharField(source="vendedor.get_full_name", read_only=True)

    class Meta:
        model = SeguimientoCliente
        fields = [
            "id", "cliente", "vendedor", "vendedor_nombre",
            "tipo_contacto", "descripcion", "fecha_proximo_contacto",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
