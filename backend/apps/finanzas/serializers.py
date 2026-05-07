from rest_framework import serializers

from .models import Abono, Cuota, PlanPago, Venta


class AbonoSerializer(serializers.ModelSerializer):
    registrado_por_nombre = serializers.CharField(
        source="registrado_por.get_full_name", read_only=True
    )

    class Meta:
        model = Abono
        fields = [
            "id", "cuota", "monto", "fecha_pago", "metodo_pago",
            "comprobante", "registrado_por", "registrado_por_nombre",
            "notas", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class CuotaSerializer(serializers.ModelSerializer):
    abonos = AbonoSerializer(many=True, read_only=True)

    class Meta:
        model = Cuota
        fields = [
            "id", "numero", "monto", "monto_capital", "monto_interes",
            "fecha_vencimiento", "estado", "saldo_restante", "abonos",
        ]


class PlanPagoSerializer(serializers.ModelSerializer):
    cuotas = CuotaSerializer(many=True, read_only=True)

    class Meta:
        model = PlanPago
        fields = [
            "id", "venta", "cuota_mensual", "total_cuotas",
            "saldo_pendiente", "cuotas", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source="cliente.nombre_completo", read_only=True)
    lote_info = serializers.CharField(source="lote.__str__", read_only=True)
    vendedor_nombre = serializers.CharField(source="vendedor.get_full_name", read_only=True)
    monto_financiado = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Venta
        fields = [
            "id", "lote", "lote_info", "cliente", "cliente_nombre",
            "vendedor", "vendedor_nombre", "reserva",
            "precio_venta", "enganche", "monto_financiado",
            "plazo_meses", "tasa_interes", "fecha_venta",
            "estado", "notas", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
