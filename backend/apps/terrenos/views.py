from rest_framework import generics, parsers, status
from rest_framework.response import Response

from apps.accounts.permissions import IsAdminOrGerente

from .filters import LoteFilter
from .models import FotografiaLote, Lote, Proyecto
from .serializers import (
    FotografiaLoteSerializer,
    LoteListSerializer,
    LoteSerializer,
    ProyectoSerializer,
)


class ProyectoListCreateView(generics.ListCreateAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrGerente()]
        return super().get_permissions()


class ProyectoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    permission_classes = [IsAdminOrGerente]


class LoteListCreateView(generics.ListCreateAPIView):
    queryset = Lote.objects.select_related("proyecto").all()
    filterset_class = LoteFilter
    search_fields = ["numero", "manzana", "num_finca"]
    ordering_fields = ["precio_base", "area_total", "numero", "created_at"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return LoteListSerializer
        return LoteSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrGerente()]
        return super().get_permissions()


class LoteDetailView(generics.RetrieveUpdateAPIView):
    queryset = Lote.objects.select_related("proyecto").prefetch_related("fotografias").all()
    serializer_class = LoteSerializer

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH"):
            return [IsAdminOrGerente()]
        return super().get_permissions()


class FotografiaLoteUploadView(generics.CreateAPIView):
    serializer_class = FotografiaLoteSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    permission_classes = [IsAdminOrGerente]

    def perform_create(self, serializer):
        lote_id = self.kwargs["lote_pk"]
        lote = Lote.objects.get(pk=lote_id)
        serializer.save(lote=lote)


class LoteDisponibilidadView(generics.GenericAPIView):
    queryset = Lote.objects.all()

    def get(self, request, pk):
        lote = self.get_object()
        return Response(
            {
                "id": lote.id,
                "numero": lote.numero,
                "estado": lote.estado,
                "disponible": lote.estado == Lote.Estado.DISPONIBLE,
            },
            status=status.HTTP_200_OK,
        )
