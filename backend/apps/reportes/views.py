from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminOrGerente


class DashboardView(APIView):
    """Métricas principales del dashboard directivo."""

    permission_classes = [IsAdminOrGerente]

    def get(self, request):
        # Placeholder: se implementará con agregaciones reales
        return Response(
            {
                "total_lotes": 0,
                "lotes_disponibles": 0,
                "lotes_reservados": 0,
                "lotes_vendidos": 0,
                "ingresos_mes": "0.00",
                "ingresos_total": "0.00",
                "clientes_activos": 0,
                "clientes_morosos": 0,
            },
            status=status.HTTP_200_OK,
        )


class FlujoCajaView(APIView):
    """Flujo de caja mensual (proyección de cobros)."""

    permission_classes = [IsAdminOrGerente]

    def get(self, request):
        # Placeholder
        return Response(
            {"detail": "Endpoint pendiente de implementación."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


class VentasPorVendedorView(APIView):
    """KPIs de rendimiento por vendedor."""

    permission_classes = [IsAdminOrGerente]

    def get(self, request):
        # Placeholder
        return Response(
            {"detail": "Endpoint pendiente de implementación."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


class InventarioResumenView(APIView):
    """Resumen de inventario: disponibles vs vendidos por proyecto."""

    def get(self, request):
        # Placeholder
        return Response(
            {"detail": "Endpoint pendiente de implementación."},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )
