from django.db import models
import pickle

# from django_mysql.models import Model
# Create your models here.


class MaterialSystem(models.Model):
    num_elements = models.IntegerField()
    num_entries = models.IntegerField()
    elements = models.CharField(max_length=30)


class MLModel(models.Model):
    train_MAE = models.FloatField()
    train_MSE = models.FloatField()
    test_MAE = models.FloatField()
    test_MSE = models.FloatField()
    baseline_MSE = models.FloatField()
    baseline_MAE = models.FloatField()
    material_system = models.ForeignKey(MaterialSystem, related_name='mlmodel', on_delete=models.CASCADE)


class SVRModel(models.Model):
    parameters = models.TextField()
    intercept = models.TextField()
    dual_coef = models.TextField()
    sparse = models.TextField()
    shape_fit = models.TextField()
    support = models.TextField()
    support_vectors = models.TextField()
    n_support = models.TextField()
    probA = models.TextField()
    probB = models.TextField()
    gamma = models.TextField()
    mlmodel = models.OneToOneField(MLModel, related_name='svr', on_delete=models.CASCADE)
    descriptor_parameters = models.TextField()
    transformed = models.BooleanField(default=False)
    scale = models.TextField(null=True)
    mean = models.TextField(null=True)
    var = models.TextField(null=True)
    n_samples_seen = models.IntegerField(null=True)
    material_system = models.ForeignKey(MaterialSystem, on_delete=models.CASCADE)


class SVRModelManager(models.Manager):
    def create_model(
        self, model_path, elements, results, params, transformer_path=None
    ):
        with open(model_path, "rb") as mod:
            model = pickle.load(mod)
        intercept = str(model._intercept_)
        dual_coef = str(model._dual_coef_)
        sparse = str(model._sparse)
        shape_fit = str(model.shape_fit_)
        support = str(model.support_)
        support_vectors = str(model.support_vectors_)
        n_support = str(model._n_support)
        probA = str(model.probA_)
        probB = str(model.probB_)
        gamma = str(model._gamma)
        parameters = str(model.get_params())
        material_system = MaterialSystem.objects.get(elements=elements)
        # Create MLModel
        mlmodel = MLModel.objects.create(
            train_MAE=results["train_MAE"],
            train_MSE=results["train_MSE"],
            test_MAE=results["test_MAE"],
            test_MSE=results["test_MSE"],
            baseline_MSE=results["baseline_MSE"],
            baseline_MAE=results["baseline_MAE"],
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
            )

        return model
