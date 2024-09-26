"""
URL configuration for Granja project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mi_app.views import add, eliminarCliente, porcinos, agregar_porcino, deletePorcino, getPorcino, actualizarPorcino, alimentacion, agregarAlimentacion, deleteAlimento, editarDosis, getAlimento
from mi_app.views import index
from mi_app.views import get_cliente
from mi_app.views import actualizarCliente
from mi_app.views import reportClientes
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='index'),
    path('porcinos', porcinos, name = 'porcinos'),
    path('save', add),
    path('cliente/<str:cedula>/', get_cliente, name='get_cliente'),
    path('eliminar_cliente/<str:cedula>/', eliminarCliente, name='eliminar_cliente'),
    path('actualizar_cliente/<str:cedula>/', actualizarCliente, name='actualizar_cliente'),
    path('agregar_porcino', agregar_porcino, name='agregar_porcino'),
    path("report", reportClientes),
    path("porcino/profile/<int:idPorcino>/", getPorcino, name="getPorcino"),
    path("porcino/delete/<int:idPorcino>/", deletePorcino, name="deletePorcino"),
    path("actualizar_porcino/<int:idPorcino>/", actualizarPorcino, name="actualizar_porcino"),
    path('alimentacion', alimentacion, name=  'alimentacion'),
    path('agregarAlimentacion', agregarAlimentacion, name = 'agregarAlimentacion'),
    path('eliminarAlimento/<int:idalimentacion>/', deleteAlimento, name= 'eliminarAlimento'),
    path('alimento/<int:idalimentacion>/', getAlimento, name = 'getAlimento'),
    path('editarDosis/<int:idalimentacion>/', editarDosis , name = 'editarDosis' ),
    path('api/v1/', include('mi_app_rest.urls')),
    path('docs/', include_docs_urls(title='Api Documentation'))
]
