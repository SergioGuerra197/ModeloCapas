from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from mi_app.models import Clientes


def my_view(request):
    
    clientes = Clientes.objects.all()
    
    return render(
        request,
        "mi_app/index.html",
        {
            "form": "form",
            "clientes": clientes
        }

    )




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
        return render(request, "mi_app/index.html", {"foo": nombre})
        
      pass
   
   return render(request, "mi_app/index.html")
