from django.db import models
import pickle
import base64
import codecs
import numpy as np
import ast
import json
from mlmodel.custom import NumpyArrayField, DictField

class Element(models.Model):
    """
    Elements model
    Attributes:
        name: str
            name of the element
        symbol : str
            symbol of the element
    """
    name = models.TextField()
    symbol = models.CharField(max_length=2)

    def __str__(self):
        return self.symbol

class MaterialSystem(models.Model):
    """
    Material-System that a MLModel is valid for
    Relationships:
        :model: 'mlmodel.Element' via elements
    Attributes:
        num_elements : int
            Number of elements in the material system
    """
    num_elements = models.IntegerField()
    #num_entries = models.IntegerField()
    elements = models.ManyToManyField(Element)
    def __str__(self):
        string = ''
        return '-'.join([str(element) for element in self.elements.all()])

class MLModel(models.Model):
    """
    MLModel model. Currently the central model all ml model types will be related to this model.
    Relationships:
        :model: 'mlmodel.MaterialSystem' via material_system
    Attributes:
        train_MAE : float
            mean absoulute error of trainning data
        train_MSE : float
            mean squared error of trainning data
        test_MAE : float
            mean absoulute error of testing data
        test_MSE : float
            mean squared error of testing data 
        baseline_MAE : float
            mean absoulute error if all targets are computed as the mean value
        baseline_MSE : float
            mean squared error if all targets are computed as the mean value
        targer_property : str
            name of property model will predict
        name : str
            name given to populated database
    """
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
    name = models.TextField()
    DOI = models.TextField()
    def __str__(self):
        string = ''
        return '-'.join([str(element) for element in self.material_system.elements.all()]) + '\t' + str(self.target_property)

class SVRModel(models.Model):
    """
    Model containing information to rebuild an support vector regression model
    Relationships:
        :model: 'mlmodel.MaterialSystem' via material_system
        :model: 'mlmodel.MLModel' via mlmodel
    Attributes:
        parameters : dict
            dictionary containing all of the svr hiperparameters
        intercept: np.array
            sklearn parameter for model
        dual_coef : np.array
            sklearn parameter
        sparse : boolean
            sklearn parameter
        shape_fit : str
            sklearn parameter
        support : np.array
            sklearn parameter
        support_vectors : np.array
            sklearn parameter
        probA : np.array
            sklearn parameter
        probB : np.array
            sklearn parameter
        gamma : float
            sklearn parameter
        descriptor_parameters : dict
            dictionary containing all information to compute the descriptor
        transformed : boolean
            True if the data is altered after the descriptor is computed
        pickle_str : str
            pickle string of svr model for python reconcstruction
        pickle_str_transformer : str
            pickle string of transformer for python reconstruction
                                        
        
    """
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
    material_system = models.ForeignKey(MaterialSystem, on_delete=models.CASCADE)
    pickle_str = models.TextField()
    pickle_str_transformer = models.TextField(null = True)

    def __str__(self):
        string = ''
        return '-'.join([str(element) for element in self.material_system.elements.all()]) + '\t' + str(self.transformed)

class SVRModelManager(models.Manager):
    """
    used to create svr model and all relationships
    """
    def create_model(
        self, model_path, elements, results, params, target, name, transformer_path=None
    ):
        """
        Parameters
        ----------
            model_path : str
                path to *.sav file for svr model
            elements : list
                list of elements by symbol
            results: dict
                dictionary containning all errors for mlmodel
            params : dict
                dictionary of all information needed to reconstruct the descriptor
            targer : str
                name of property model will predict
            name : str
                name given to populated database
        Returns:
            model :
                database entry

        """
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
            name = name,
        )
        mlmodel.save()

        if transformer_path is not None:
            with open(transformer_path, "rb") as mod:
                transformer = pickle.load(mod)

            #scale = transformer.scale_
            #mean = transformer.mean_
            #var = transformer.var_
            #n_samples_seen = transformer.n_samples_seen_
            pickle_str_transformer = codecs.encode(pickle.dumps(transformer), "base64").decode()
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
                #scale=scale,
                #mean=mean,
                #var=var,
                #n_samples_seen=n_samples_seen,
                pickle_str = pickle_str,
                pickle_str_transformer= pickle_str_transformer

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
                pickle_str = pickle_str,
                pickle_str_transformer = None
            )

        return model

class TrainingData(models.Model):
    structure = DictField()
    energy = models.FloatField()
    model = models.ForeignKey(MLModel, related_name='data', on_delete=models.CASCADE)

