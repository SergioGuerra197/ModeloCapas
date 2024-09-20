from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from mi_app.models import Clientes, Razas, Porcinos


# Create your views here.
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


##------------------------------CLIENTE------------------------------------------##

def registrarCliente(request):
   return render(
      request,
      "mi_app/Clientes/registrar.html"
   )

# Define your form class
class ClienteValidate(forms.Form):
    cedula = forms.CharField(label="cedula")
    nombre = forms.CharField(label="nombre")
    apellidos = forms.CharField(label="apellidos")
    direccion = forms.CharField(label="direccion")
    telefono = forms.CharField(label="telefono")

def add(request):
   if(request.method == 'POST'):
      form = ClienteValidate(request.POST)
      if form.is_valid():
        cedula = form.cleaned_data.get('cedula')
        nombre = form.cleaned_data.get('nombre')
        apellidos = form.cleaned_data.get('apellidos')
        direccion = form.cleaned_data.get('direccion')
        telefono = form.cleaned_data.get('telefono')
        cliente = Clientes(cedula, nombre, apellidos, direccion, telefono)
        cliente.save()
        return redirect('home')
        
      pass
   
   return redirect('home')

def get(request, cedula):
   
   cliente = Clientes.objects.get(cedula=cedula)
   porcinos = Porcinos.objects.filter(clientes_cedula = cedula)
   print(porcinos)
   return render(request, "mi_app/clientes/cliente.html", {"cliente": cliente, "porcinos": porcinos})


#-------------------------------------- PORCINOS ----------------------------------
def registrarPorcino(request, cedula):
   cliente = Clientes.objects.get(cedula = cedula)
   razas = Razas.objects.all()
   return render(request, "mi_app/porcinos/registrar.html", {"razas": razas, "cliente": cliente})

class PorcinoValidate(forms.Form):
    cedula = forms.IntegerField(label="Cédula del cliente", widget=forms.HiddenInput())  # Campo cedula agregado
    identificacion = forms.IntegerField(label="Identificación del porcino", min_value=1, error_messages={'required': 'La identificación del porcino es obligatoria.'})
    edad = forms.IntegerField(label="Edad", min_value=0, error_messages={'required': 'La edad del porcino es obligatoria.'})
    peso = forms.IntegerField(label="Peso", min_value=0, error_messages={'required': 'El peso del porcino es obligatorio.'})
    razas = forms.ModelChoiceField(queryset=Razas.objects.all(), label="Raza", error_messages={'required': 'Debes seleccionar una raza.'})

    # Validación personalizada para edad
    def clean_edad(self):
        edad = self.cleaned_data.get('edad')
        if edad < 0:
            raise forms.ValidationError("La edad no puede ser negativa.")
        return edad

    # Validación personalizada para peso
    def clean_peso(self):
        peso = self.cleaned_data.get('peso')
        if peso <= 0:
            raise forms.ValidationError("El peso debe ser mayor a cero.")
        return peso
    
def savePorcino(request):
   if(request.method == 'POST'):
         form = PorcinoValidate(request.POST)
         if form.is_valid():
             cliente = Clientes.objects.get(cedula = cedula)
             if (cliente):
                 idPorcino = form.cleaned_data.get("identificacion")
                 edad = form.cleaned_data.get("edad")
                 peso = form.cleaned_data.get("peso")
                 raza = form.cleaned_data.get('razas')
                 
                 porcino = Porcinos(
                     idporcinos = idPorcino,
                     edad = edad,
                     peso = peso,
                     razas_idrazas = raza,
                     clientes_cedula = cliente,
                 )

                 porcino.save()
                 return redirect('/consulta/'+str(cliente.cedula))

         else:
            cedula = request.POST.get("cedula")  # Recupera la cédula de los datos POST
            cliente = Clientes.objects.get(cedula=cedula)
            razas = Razas.objects.all()
            context = {
                "form": form,  # Renderizar el formulario con los errores
                "cliente": cliente,
                "razas": razas,
            }
            # Renderizar la plantilla con el formulario y los datos del cliente y razas
            return render(request, 'mi_app/porcinos/registrar.html', context)
             
   
   return redirect('/')

def todosPorcino(request):
    porcinos = Porcinos.objects.all()
    return render(request, "mi_app/porcinos/all.html", {"porcinos": porcinos})
             
