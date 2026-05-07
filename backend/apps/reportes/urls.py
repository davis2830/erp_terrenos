from django.urls import path

from . import views

app_name = "reportes"

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("flujo-caja/", views.FlujoCajaView.as_view(), name="flujo_caja"),
    path("ventas-por-vendedor/", views.VentasPorVendedorView.as_view(), name="ventas_por_vendedor"),
    path("inventario/", views.InventarioResumenView.as_view(), name="inventario_resumen"),
]
