from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import *
from .serializers import *
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend

class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    http_method_names = ["get"]

class SVRModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SVRModel.objects.all().order_by("id")
    serializer_class = SVRModelSerializer
    http_method_names = ["get"]

class MLModelViewSet(viewsets.ModelViewSet):
    queryset = MLModel.objects.all().order_by("id")
    serializer_class = MLModelSerializer
    http_method_names = ["get"]
    filter_class = MLModelFilter

class MaterialsSystemViewSet(viewsets.ModelViewSet):
    queryset = MaterialSystem.objects.all().order_by("id")
    serializer_class = MaterialsSystemSerializer
    http_method_names = ["get"]

class TrainingDataViewSet(viewsets.ModelViewSet):
    queryset = TrainingData.objects.all()
    serializer_class = TrainingDataSerializer
    http_method_names = ['get']
# class dual_coef_testViewSet(viewsets.ModelViewSet):
#     queryset = dual_coef_test.objects.all()
#     serializer_class = dual_coef_testSerializer
#     http_method_names = ["get"]
#
# class dual_coef_rowViewSet(viewsets.ModelViewSet):
#     queryset = dual_coef_row.objects.all()
#     serializer_class = dual_coef_rowSerializer
#     http_method_names = ["get"]
#
# class dual_coef_weightViewSet(viewsets.ModelViewSet):
#     queryset = dual_coef_weight.objects.all()
#     serializer_class = dual_coef_weightSerializer
#     http_method_names = ["get"]
