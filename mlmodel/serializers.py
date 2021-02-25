from rest_framework import serializers
from .models import *

class ElementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"

class SVRModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SVRModel
        fields = "__all__"

class MLModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MLModel
        fields = ["target_property","train_MSE", "test_MSE", "baseline_MSE", "train_MAE", "test_MAE", "baseline_MAE", "material_system","svr"]

class MaterialsSystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaterialSystem
        fields = ["elements", "mlmodel"]
