from django.db import models
import pickle
import base64
import codecs
import numpy as np
from collections import defaultdict
import ast
import json
class NumpyArrayField(models.TextField):
    description = "Stores a Numpy ndarray."
    #__metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(NumpyArrayField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, list):
            value = np.array(list)
        if isinstance(value, np.ndarray):
            return value

        if not value:
            return np.array([])

        return np.array(pickle.loads(str(value)))

    def get_prep_value(self, value):
        if isinstance(value, list):
            return str(value)
        elif isinstance(value, np.ndarray):
            return str(value.tolist())
            #return pickle.dumps(value.tolist())
        else:
            raise TypeError('%s is not a list or numpy array' % value)

class DictField(models.TextField):
    #__metaclass__ = models.SubfieldBase
    description = "Stores a python dictionary"

    def __init__(self, *args, **kwargs):
        super(DictField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = {}

        if isinstance(value, dict):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        if isinstance(value, defaultdict):
            value = dict(value)

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class JSONField(models.TextField):
    #__metaclass__ = models.SubfieldBase
    description = "Stores a python dictionary"

    def __init__(self, *args, **kwargs):
        super(JSONField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return value
        if not isinstance(value, str):
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        print('get prep value', value)
        return json.dumps(value)


class Element(models.Model):
    name = models.TextField()
    symbol = models.CharField(max_length=2)

    def __str__(self):
        return self.symbol

class MaterialSystem(models.Model):
    num_elements = models.IntegerField()
    num_entries = models.IntegerField()
    #change to Foriegnkey
    elements = models.ManyToManyField(Element)
    def __str__(self):
        string = ''
        return '-'.join([str(element) for element in self.elements.all()])

class MLModel(models.Model):

    TARGET_PROBERTY_CHOICES = [
        ('Formation Energy', 'Formation Energy'),
        ('Force', 'Force'),
    ]
    train_MAE = models.FloatField()
    train_MSE = models.FloatField()
    test_MAE = models.FloatField()
    test_MSE = models.FloatField()
    baseline_MSE = models.FloatField()
    baseline_MAE = models.FloatField()
    target_property = models.CharField(max_length=25,choices=TARGET_PROBERTY_CHOICES)
    material_system = models.ForeignKey(MaterialSystem, related_name='mlmodel', on_delete=models.CASCADE)
    def __str__(self):
        string = ''
        return '-'.join([str(element) for element in self.material_system.elements.all()]) + '\t' + str(self.target_property)



class SVRModel(models.Model):
    parameters = DictField()
    intercept = NumpyArrayField()
    dual_coef = NumpyArrayField()
    sparse = models.BooleanField()
    shape_fit = models.TextField()
    support = NumpyArrayField()
    support_vectors = NumpyArrayField()
    n_support = NumpyArrayField()
    probA = NumpyArrayField()
    probB = NumpyArrayField()
    gamma = models.FloatField()
    mlmodel = models.OneToOneField(MLModel, related_name='svr', on_delete=models.CASCADE)
    descriptor_parameters = DictField()
    transformed = models.BooleanField(default=False)
    scale = models.TextField(null=True)
    mean = models.TextField(null=True)
    var = models.TextField(null=True)
    n_samples_seen = models.IntegerField(null=True)
    material_system = models.ForeignKey(MaterialSystem, on_delete=models.CASCADE)
    pickle_str = models.TextField()

    def __str__(self):
        string = ''
        return '-'.join([str(element) for element in self.material_system.elements.all()]) + '\t' + str(self.transformed)

class SVRModelManager(models.Manager):
    def create_model(
        self, model_path, elements, results, params, target, transformer_path=None
    ):
        with open(model_path, "rb") as mod:
            model = pickle.load(mod)
        pickle_str = codecs.encode(pickle.dumps(model), "base64").decode()

        #pickle_s = base64.b64encode(pickle_obj)
        intercept = model._intercept_
        dual_coef = model._dual_coef_
        sparse = model._sparse
        shape_fit = model.shape_fit_
        support = model.support_
        support_vectors = model.support_vectors_
        n_support = model._n_support
        probA = model.probA_
        probB = model.probB_
        gamma = model._gamma
        parameters = model.get_params()
        material_system = MaterialSystem.objects.filter(elements__symbol=elements[0]).filter(elements__symbol=elements[1]).get()
        target = target
        #material_system = MaterialSystem.objects.get(elements__symbols=elements)
        # Create MLModel
        mlmodel = MLModel.objects.create(
            train_MAE=results["train_MAE"],
            train_MSE=results["train_MSE"],
            test_MAE=results["test_MAE"],
            test_MSE=results["test_MSE"],
            baseline_MSE=results["baseline_MSE"],
            baseline_MAE=results["baseline_MAE"],
            target_property = target,
            material_system=material_system,
        )
        mlmodel.save()

        if transformer_path is not None:
            with open(transformer_path, "rb") as mod:
                transformer = pickle.load(mod)

            scale = transformer.scale_
            mean = transformer.mean_
            var = transformer.var_
            n_samples_seen = transformer.n_samples_seen_

            model = SVRModel.objects.create(
                intercept=intercept,
                dual_coef=dual_coef,
                sparse=sparse,
                shape_fit=shape_fit,
                support=support,
                support_vectors=support_vectors,
                n_support=n_support,
                probB=probB,
                probA=probA,
                gamma=gamma,
                parameters=parameters,
                material_system=material_system,
                mlmodel=mlmodel,
                descriptor_parameters=params,
                transformed=True,
                scale=scale,
                mean=mean,
                var=var,
                n_samples_seen=n_samples_seen,
                pickle_str = pickle_str
            )
        else:
            model = SVRModel.objects.create(
                intercept=intercept,
                dual_coef=dual_coef,
                sparse=sparse,
                shape_fit=shape_fit,
                support=support,
                support_vectors=support_vectors,
                n_support=n_support,
                probB=probB,
                probA=probA,
                gamma=gamma,
                parameters=parameters,
                material_system=material_system,
                mlmodel=mlmodel,
                descriptor_parameters=params,
                pickle_str = pickle_str
            )

        return model

class TrainingData(models.Model):
    structure = DictField()
    energy = models.FloatField()
    model = models.ForeignKey(MLModel, related_name='data', on_delete=models.CASCADE)
#class dual_coef_test(models.Model):
#    svrmodel = models.OneToOneField(SVRModel, on_delete=models.CASCADE)

# class dual_coef_row(models.Model):
#     row = models.ForeignKey(SVRModel, on_delete=models.CASCADE, related_name='dual_coef_row')
#     def __str__(self):
#         return str(self.id)
#
# class dual_coef_weight(models.Model):
#     weight = models.FloatField()
#     weight_row = models.ForeignKey(dual_coef_row, on_delete=models.CASCADE, related_name='dual_coef_weight')
#     def __str__(self):
#         return str(self.weight)
    
