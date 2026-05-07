"""
URL configuration for ERP Terrenos project.
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/terrenos/", include("apps.terrenos.urls")),
    path("api/v1/mapa/", include("apps.mapa.urls")),
    path("api/v1/crm/", include("apps.crm.urls")),
    path("api/v1/finanzas/", include("apps.finanzas.urls")),
    path("api/v1/facturacion/", include("apps.facturacion.urls")),
    path("api/v1/reportes/", include("apps.reportes.urls")),
    path("api/v1/notificaciones/", include("apps.notificaciones.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
