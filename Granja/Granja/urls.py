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
from django.urls import path
from mi_app.views import my_view, add, get, registrarCliente, eliminarCliente, actualizarCliente
from mi_app.views import registrarPorcino, savePorcino, todosPorcino, deletePorcino, profilePorcino, porcinoHasAlimento, deletePorcinoHasAlimento
from mi_app.views import listarAlimentos, registrarAlimento, saveAlimento, deleteAlimento
from mi_app.views import reportClientes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', my_view, name="home"),
    path('cliente/save', add),
    path("consulta/<int:cedula>", get, name="consulta"),
    path("cliente/registrar", registrarCliente),
    path("cliente/eliminar/<int:cedula>", eliminarCliente, name="eliminarCliente"),
    path("cliente/actualizar/<int:cedula>", actualizarCliente, name="actualizarCliente"),
    path("porcino/registrar/<int:cedula>",registrarPorcino, name="registrarPorcino"),
    path("porcino/save", savePorcino, name="savePorcino"),
    path("porcino/all", todosPorcino, name="allPorcinos"),
    path("porcino/delete/<int:idPorcino>", deletePorcino, name="deletePorcino"),
    path("alimentos/all", listarAlimentos),
    path("alimentos/registrar", registrarAlimento),
    path("alimentos/save", saveAlimento),
    path("alimento/delete/<int:idalimentacion>", deleteAlimento, name="deleteAlimento"),
    path("porcino/profile/<int:idPorcino>", profilePorcino, name="profilePorcino"),
    path("porcino/profile/addalimento/<int:idPorcino>", porcinoHasAlimento, name="addAlimentoPorcino"),
    path("porcino/profile/deletealimento/<int:idPorcino>/<int:idAlimento>/", deletePorcinoHasAlimento, name="delete_alimento_porcino"),
    path("report", reportClientes)

]
