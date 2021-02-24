from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import *
from .serializers import *
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend
class SVRModelViewSet(viewsets.ModelViewSet):
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

# Create your views here.
