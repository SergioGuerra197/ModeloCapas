from django.urls import path, include
from rest_framework import routers
from mi_app_rest import views

router = routers.DefaultRouter()
router.register(r'clientes', views.clienteViewSet)
router.register(r'porcinos', views.porcinosViewSet)
router.register(r'alimentos', views.alimentosViewSet)
router.register(r'hasAlimentacion', views.porcinosHasAlimentacionViewSet)
# router.register(r'razas', views.razasViewSet)

urlpatterns = [
    path('', include(router.urls)) 
]