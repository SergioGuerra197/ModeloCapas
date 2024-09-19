from django.shortcuts import render
from django.http import HttpResponse
from django import forms

# Create your views here.
def my_view(request):
   return render(
    request,
    "mi_app/index.html",
    {
        "foo": "bar",
    })

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
        nombre = form.cleaned_data.get('nombre')
        print(f'Nombre: {nombre}')
        return render(request, "mi_app/index.html", {"foo": nombre})
        
      pass
   
   return render(request, "mi_app/index.html")
