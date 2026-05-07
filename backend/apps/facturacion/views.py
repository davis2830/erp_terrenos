from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminOrGerente

from .models import DocumentoLegal, Factura, PlantillaContrato
from .serializers import DocumentoLegalSerializer, FacturaSerializer, PlantillaContratoSerializer


class FacturaListCreateView(generics.ListCreateAPIView):
    queryset = Factura.objects.select_related("venta", "abono").all()
    serializer_class = FacturaSerializer
    permission_classes = [IsAdminOrGerente]
    filterset_fields = ["estado", "venta"]
    ordering_fields = ["fecha_emision", "monto"]


class FacturaDetailView(generics.RetrieveAPIView):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer


class FacturaPDFView(APIView):
    """Descargar PDF de una factura."""

    def get(self, request, pk):
        # Placeholder: se implementará con generación de PDF
        return Response(
            {"detail": "Endpoint pendiente de implementación."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


class DocumentoLegalListCreateView(generics.ListCreateAPIView):
    queryset = DocumentoLegal.objects.all()
    serializer_class = DocumentoLegalSerializer
    filterset_fields = ["tipo", "cliente"]


class DocumentoLegalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentoLegal.objects.all()
    serializer_class = DocumentoLegalSerializer


class PlantillaContratoListView(generics.ListAPIView):
    queryset = PlantillaContrato.objects.filter(is_active=True)
    serializer_class = PlantillaContratoSerializer


class GenerarContratoView(APIView):
    """Genera un contrato a partir de una plantilla y datos de venta."""

    permission_classes = [IsAdminOrGerente]

    def post(self, request):
        # Placeholder: se implementará con motor de plantillas
        return Response(
            {"detail": "Endpoint pendiente de implementación."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )
