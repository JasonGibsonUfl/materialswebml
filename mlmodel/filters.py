from django_filters.rest_framework import filters
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from mlmodel.models import MLModel

class MLModelFilter(django_filters.FilterSet):
    elements = django_filters.CharFilter(field_name='material_system__elements', lookup_expr='icontains')
    test_MAE = filters.RangeFilter()
    class Meta:
        model = MLModel
        fields = ["test_MAE", "elements"]