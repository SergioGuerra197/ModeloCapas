from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django import forms
from mi_app.models import Clientes


def index(request):
    clientes = Clientes.objects.all()
    return render(request, 'mi_app/index.html', {'clientes': clientes})

# Define your form class
class MyForm(forms.Form):
    cedula = forms.CharField(label="cedula")
    nombre = forms.CharField(label="nombre")
    apellidos = forms.CharField(label="apellidos")
    direccion = forms.CharField(label="direccion")
    telefono = forms.CharField(label="telefono")

def add(request):
   if(request.method == 'POST'):
      form = MyForm(request.POST)
      if form.is_valid():
        cedula = form.cleaned_data.get('cedula')
        nombre = form.cleaned_data.get('nombre')
        apellidos = form.cleaned_data.get('apellidos')
        direccion = form.cleaned_data.get('direccion')
        telefono = form.cleaned_data.get('telefono')
        cliente = Clientes(cedula, nombre, apellidos, direccion, telefono)
        cliente.save()
        print(f'Nombre: {nombre}')
        return redirect('index')
        
      pass
   
   return render(request, "mi_app/index.html")

def get_cliente(request, cedula):
    # Obtener el cliente de la base de datos según la cédula
    cliente = get_object_or_404(Clientes, cedula=cedula)
    
    # Devolver los datos del cliente en formato JSON
    data = {
        'cedula': cliente.cedula,
        'nombre': cliente.nombre,
        'apellidos': cliente.apellidos,
        'direccion': cliente.direccion,
        'telefono': cliente.telefono,
    }
    print(data)
    return JsonResponse(data)