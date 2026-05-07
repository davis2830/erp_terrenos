from django.urls import path

from . import views

app_name = "mapa"

urlpatterns = [
    path(
        "proyectos/<int:proyecto_pk>/mapa/",
        views.MapaProyectoRetrieveUpdateView.as_view(),
        name="mapa_proyecto",
    ),
]
