from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminOrGerente

from .models import Abono, Cuota, PlanPago, Venta
from .serializers import AbonoSerializer, PlanPagoSerializer, VentaSerializer


class VentaListCreateView(generics.ListCreateAPIView):
    queryset = Venta.objects.select_related("lote", "cliente", "vendedor").all()
    serializer_class = VentaSerializer
    filterset_fields = ["estado", "vendedor", "cliente"]
    ordering_fields = ["fecha_venta", "precio_venta", "created_at"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrGerente()]
        return super().get_permissions()


class VentaDetailView(generics.RetrieveUpdateAPIView):
    queryset = Venta.objects.select_related("lote", "cliente", "vendedor").all()
    serializer_class = VentaSerializer
    permission_classes = [IsAdminOrGerente]


class PlanPagoDetailView(generics.RetrieveAPIView):
    """Obtener el plan de pago (con tabla de amortización) de una venta."""

    serializer_class = PlanPagoSerializer
    lookup_field = "venta_id"
    lookup_url_kwarg = "venta_pk"

    def get_queryset(self):
        return PlanPago.objects.select_related("venta").prefetch_related("cuotas__abonos")


class AbonoCreateView(generics.CreateAPIView):
    queryset = Abono.objects.all()
    serializer_class = AbonoSerializer

    def perform_create(self, serializer):
        serializer.save(registrado_por=self.request.user)


class EstadoCuentaView(APIView):
    """Estado de cuenta de un cliente."""

    def get(self, request, cliente_pk):
        # Placeholder: se implementará con lógica financiera completa
        return Response(
            {"detail": "Endpoint pendiente de implementación."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


class MorososView(generics.ListAPIView):
    """Lista de clientes con cuotas en mora."""

    permission_classes = [IsAdminOrGerente]

    def get(self, request):
        # Placeholder: se implementará con queries de mora
        return Response(
            {"detail": "Endpoint pendiente de implementación."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )
