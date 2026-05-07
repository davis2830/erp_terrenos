from rest_framework import generics

from apps.accounts.permissions import IsAdminOrGerente

from .models import MapaProyecto
from .serializers import MapaProyectoSerializer


class MapaProyectoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """Obtener o actualizar el mapa SVG de un proyecto."""

    serializer_class = MapaProyectoSerializer
    lookup_field = "proyecto_id"
    lookup_url_kwarg = "proyecto_pk"

    def get_queryset(self):
        return MapaProyecto.objects.select_related("proyecto").prefetch_related(
            "coordenadas__lote"
        )

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH"):
            return [IsAdminOrGerente()]
        return super().get_permissions()
