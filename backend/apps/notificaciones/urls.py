from django.urls import path

from . import views

app_name = "notificaciones"

urlpatterns = [
    path("plantillas/", views.PlantillaMensajeListCreateView.as_view(), name="plantilla_list_create"),
    path("plantillas/<int:pk>/", views.PlantillaMensajeDetailView.as_view(), name="plantilla_detail"),
    path("historial/", views.NotificacionListView.as_view(), name="notificacion_list"),
    path("enviar/", views.EnviarMensajeView.as_view(), name="enviar_mensaje"),
]
