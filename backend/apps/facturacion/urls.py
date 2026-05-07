from django.urls import path

from . import views

app_name = "facturacion"

urlpatterns = [
    path("facturas/", views.FacturaListCreateView.as_view(), name="factura_list_create"),
    path("facturas/<int:pk>/", views.FacturaDetailView.as_view(), name="factura_detail"),
    path("facturas/<int:pk>/pdf/", views.FacturaPDFView.as_view(), name="factura_pdf"),
    path("documentos/", views.DocumentoLegalListCreateView.as_view(), name="documento_list_create"),
    path("documentos/<int:pk>/", views.DocumentoLegalDetailView.as_view(), name="documento_detail"),
    path("plantillas/", views.PlantillaContratoListView.as_view(), name="plantilla_list"),
    path("contratos/generar/", views.GenerarContratoView.as_view(), name="generar_contrato"),
]
