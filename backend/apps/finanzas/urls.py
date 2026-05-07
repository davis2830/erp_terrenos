from django.urls import path

from . import views

app_name = "finanzas"

urlpatterns = [
    path("ventas/", views.VentaListCreateView.as_view(), name="venta_list_create"),
    path("ventas/<int:pk>/", views.VentaDetailView.as_view(), name="venta_detail"),
    path("ventas/<int:venta_pk>/plan-pago/", views.PlanPagoDetailView.as_view(), name="plan_pago"),
    path("abonos/", views.AbonoCreateView.as_view(), name="abono_create"),
    path("clientes/<int:cliente_pk>/estado-cuenta/", views.EstadoCuentaView.as_view(), name="estado_cuenta"),
    path("morosos/", views.MorososView.as_view(), name="morosos"),
]
