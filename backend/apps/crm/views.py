from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cliente, Reserva, SeguimientoCliente
from .serializers import ClienteSerializer, ReservaSerializer, SeguimientoClienteSerializer


class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.select_related("vendedor_asignado").all()
    serializer_class = ClienteSerializer
    search_fields = ["nombre", "apellido", "dpi", "nit", "telefono"]
    ordering_fields = ["apellido", "nombre", "created_at"]


class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.select_related("vendedor_asignado").all()
    serializer_class = ClienteSerializer


class ReservaListCreateView(generics.ListCreateAPIView):
    queryset = Reserva.objects.select_related("lote", "cliente", "vendedor").all()
    serializer_class = ReservaSerializer
    filterset_fields = ["estado", "lote", "cliente", "vendedor"]
    ordering_fields = ["fecha_expiracion", "created_at"]


class ReservaDetailView(generics.RetrieveUpdateAPIView):
    queryset = Reserva.objects.select_related("lote", "cliente", "vendedor").all()
    serializer_class = ReservaSerializer


class ReservaConcretarView(APIView):
    """Convierte una reserva activa en una venta."""

    def post(self, request, pk):
        # Placeholder: la lógica completa se implementará en la fase de codificación
        return Response(
            {"detail": "Endpoint pendiente de implementación."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


class SeguimientoListCreateView(generics.ListCreateAPIView):
    serializer_class = SeguimientoClienteSerializer
    filterset_fields = ["tipo_contacto"]

    def get_queryset(self):
        return SeguimientoCliente.objects.select_related("vendedor").filter(
            cliente_id=self.kwargs["cliente_pk"]
        )

    def perform_create(self, serializer):
        serializer.save(
            cliente_id=self.kwargs["cliente_pk"],
            vendedor=self.request.user,
        )


class WhatsAppMessageView(APIView):
    """Envía un mensaje de WhatsApp a un cliente via Twilio."""

    def post(self, request, pk):
        # Placeholder: se implementará con integración Twilio
        return Response(
            {"detail": "Endpoint pendiente de implementación."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )
