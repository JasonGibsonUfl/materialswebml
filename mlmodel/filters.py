from django_filters.rest_framework import filters
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from mlmodel.models import MLModel

class MLModelFilter(django_filters.FilterSet):
    element1 = django_filters.CharFilter(field_name='material_system__elements__symbol', lookup_expr='icontains')
    element2 = django_filters.CharFilter(field_name='material_system__elements__symbol', lookup_expr='icontains')

    #test_MAE = filters.RangeFilter()
    target_property = django_filters.CharFilter(field_name='target_property')
    class Meta:
        model = MLModel
        fields = ["target_property", "element1", "element2"]