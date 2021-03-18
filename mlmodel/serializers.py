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
        fields = ["DOI", "target_property","train_MSE", "test_MSE", "baseline_MSE", "train_MAE", "test_MAE", "baseline_MAE", "material_system","svr", 'data']

class MaterialsSystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MaterialSystem
        fields = ["elements", "mlmodel"]

class TrainingDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrainingData
        fields = "__all__"
#
# class dual_coef_testSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = dual_coef_test
#         fields = ['__all__']
#
# class dual_coef_rowSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = dual_coef_row
#         fields = ['dual_coef_weight']
#
# class dual_coef_weightSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = dual_coef_weight
#         fields = ['weight']
