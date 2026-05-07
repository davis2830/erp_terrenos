from django.urls import path

from . import views

app_name = "terrenos"

urlpatterns = [
    path("proyectos/", views.ProyectoListCreateView.as_view(), name="proyecto_list_create"),
    path("proyectos/<int:pk>/", views.ProyectoDetailView.as_view(), name="proyecto_detail"),
    path("lotes/", views.LoteListCreateView.as_view(), name="lote_list_create"),
    path("lotes/<int:pk>/", views.LoteDetailView.as_view(), name="lote_detail"),
    path("lotes/<int:lote_pk>/fotografias/", views.FotografiaLoteUploadView.as_view(), name="lote_foto_upload"),
    path("lotes/<int:pk>/disponibilidad/", views.LoteDisponibilidadView.as_view(), name="lote_disponibilidad"),
]
