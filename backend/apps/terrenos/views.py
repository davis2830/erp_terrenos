from django.db.models import Count, Q, Sum
from rest_framework import generics, parsers, status
from rest_framework.response import Response
from rest_framework.views import APIView

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


class DashboardStatsView(APIView):
    """KPIs y estadísticas para el dashboard principal."""

    def get(self, request):
        estados = Lote.objects.aggregate(
            total=Count("id"),
            disponibles=Count("id", filter=Q(estado=Lote.Estado.DISPONIBLE)),
            reservados=Count("id", filter=Q(estado=Lote.Estado.RESERVADO)),
            vendidos=Count("id", filter=Q(estado=Lote.Estado.VENDIDO)),
            valor_total=Sum("precio_base"),
            valor_vendido=Sum(
                "precio_base", filter=Q(estado=Lote.Estado.VENDIDO)
            ),
            valor_disponible=Sum(
                "precio_base", filter=Q(estado=Lote.Estado.DISPONIBLE)
            ),
        )

        proyectos_count = Proyecto.objects.filter(is_active=True).count()

        return Response(
            {
                "lotes": {
                    "total": estados["total"] or 0,
                    "disponibles": estados["disponibles"] or 0,
                    "reservados": estados["reservados"] or 0,
                    "vendidos": estados["vendidos"] or 0,
                },
                "valores": {
                    "total": float(estados["valor_total"] or 0),
                    "vendido": float(estados["valor_vendido"] or 0),
                    "disponible": float(estados["valor_disponible"] or 0),
                },
                "proyectos_activos": proyectos_count,
            },
            status=status.HTTP_200_OK,
        )
