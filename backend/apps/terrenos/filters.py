import django_filters

from .models import Lote


class LoteFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name="precio_base", lookup_expr="gte")
    precio_max = django_filters.NumberFilter(field_name="precio_base", lookup_expr="lte")
    area_min = django_filters.NumberFilter(field_name="area_total", lookup_expr="gte")
    area_max = django_filters.NumberFilter(field_name="area_total", lookup_expr="lte")

    class Meta:
        model = Lote
        fields = ["proyecto", "estado", "manzana"]
