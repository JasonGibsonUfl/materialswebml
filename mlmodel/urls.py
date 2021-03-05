from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"SVRModel", views.SVRModelViewSet)
router.register(r"MLModel", views.MLModelViewSet)
router.register(r"MaterialSystem", views.MaterialsSystemViewSet)
router.register(r"Element", views.ElementViewSet)
router.register(r'TrainingData', views.TrainingDataViewSet)
# router.register(r"dual_coef_test", views.dual_coef_testViewSet)
# router.register(r"dual_coef_row", views.dual_coef_rowViewSet)
# router.register(r"dual_coef_weight", views.dual_coef_weightViewSet)
# router.register(r'Descriptors', views.DescriptorsViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("rest/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
