from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [
    path("clientes/", views.ClienteListCreateView.as_view(), name="cliente_list_create"),
    path("clientes/<int:pk>/", views.ClienteDetailView.as_view(), name="cliente_detail"),
    path("clientes/<int:pk>/whatsapp/", views.WhatsAppMessageView.as_view(), name="cliente_whatsapp"),
    path("clientes/<int:cliente_pk>/seguimientos/", views.SeguimientoListCreateView.as_view(), name="seguimiento_list_create"),
    path("reservas/", views.ReservaListCreateView.as_view(), name="reserva_list_create"),
    path("reservas/<int:pk>/", views.ReservaDetailView.as_view(), name="reserva_detail"),
    path("reservas/<int:pk>/concretar/", views.ReservaConcretarView.as_view(), name="reserva_concretar"),
]
