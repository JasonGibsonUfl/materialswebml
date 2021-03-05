from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SVRModel)
admin.site.register(MLModel)
admin.site.register(MaterialSystem)
admin.site.register(Element)
admin.site.register(TrainingData)
# admin.site.register(dual_coef_test)
# admin.site.register(dual_coef_row)
# admin.site.register(dual_coef_weight)
