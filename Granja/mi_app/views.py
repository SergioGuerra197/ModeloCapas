from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from mi_app.models import Clientes, Razas, Porcinos, Alimentacion, PorcinosHasAlimentacion


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
         
         cedula = request.POST.get("cedula")

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

def deletePorcino(request, idPorcino):
    porcino = Porcinos.objects.get(idporcinos = idPorcino)
    if(porcino):
        alimentosPorcino = PorcinosHasAlimentacion.objects.filter(porcinos_idporcinos = porcino)

        alimentosPorcino.delete()

        Porcinos.delete(porcino)

    return redirect('/')

def profilePorcino(request, idPorcino):
    porcino = Porcinos.objects.get(idporcinos = idPorcino)
    if(porcino):
        Alimentos = Alimentacion.objects.all()
        AlimentosPorcino = PorcinosHasAlimentacion.objects.filter(porcinos_idporcinos = porcino.idporcinos)
        return render(request, "mi_app/porcinos/porcino.html", {
            "porcino": porcino, 
            "alimentos": Alimentos, 
            "alimentosPorcino": AlimentosPorcino
            })
    
    return redirect("/")

def porcinoHasAlimento(request, idPorcino):
    if(request.method == 'POST'):
        alimentacion_id = request.POST.get('alimentacion')

        try:
            alimentacion = Alimentacion.objects.get(idalimentacion = alimentacion_id)
        except:
            return redirect("/")
        
        try:
            porcino = Porcinos.objects.get(idporcinos = idPorcino)
        except:
            return redirect("/")
        
        porcinohasalimento = PorcinosHasAlimentacion(porcinos_idporcinos = porcino, alimentacion_idalimentacion = alimentacion)
        
        Alimentos = Alimentacion.objects.all()
        AlimentosPorcino = PorcinosHasAlimentacion.objects.filter(porcinos_idporcinos = porcino.idporcinos)
            
        try:
            porcinohasalimento.save()
            msg = "Actualizacion realizada"
            return render(request, "mi_app/porcinos/porcino.html", {
                "porcino": porcino, 
                "alimentos": Alimentos, 
                "alimentosPorcino": AlimentosPorcino,
                "msg": msg,
                }) 

        except:
            msg = "No se puede guardar la opcion seleccionada"
            return render(request, "mi_app/porcinos/porcino.html", {
                "porcino": porcino, 
                "alimentos": Alimentos, 
                "alimentosPorcino": AlimentosPorcino,
                "msg": msg,
                }) 

    
    return redirect("/")

def deletePorcinoHasAlimento(request, idPorcino, idAlimento):
    porcino = Porcinos.objects.get(idporcinos = idPorcino)
    alimento = Alimentacion.objects.get(idalimentacion = idAlimento)

    Alimentos = Alimentacion.objects.all()
    AlimentosPorcino = PorcinosHasAlimentacion.objects.filter(porcinos_idporcinos = porcino.idporcinos)

    porcinoHasAlimento = PorcinosHasAlimentacion.objects.get(porcinos_idporcinos = porcino, alimentacion_idalimentacion = alimento)
    if(porcinoHasAlimento):
           
        try:
            porcinoHasAlimento.delete()
            msg = "eliminacion realizada"

            return render(request, "mi_app/porcinos/porcino.html", {
                "porcino": porcino, 
                "alimentos": Alimentos, 
                "alimentosPorcino": AlimentosPorcino,
                "msg": msg,
                }) 
        
        except:
            msg = "No se puede eliminar la opcion seleccionada"
            return render(request, "mi_app/porcinos/porcino.html", {
                "porcino": porcino, 
                "alimentos": Alimentos, 
                "alimentosPorcino": AlimentosPorcino,
                "msg": msg,
                }) 
    
    msg="error al eliminar"
    return render(request, "mi_app/porcinos/porcino.html", {
                "porcino": porcino, 
                "alimentos": Alimentos, 
                "alimentosPorcino": AlimentosPorcino,
                "msg": msg,
                }) 


#------------------------------ ALIMENTACION -----------------------------------
def listarAlimentos(request):
    alimentos = Alimentacion.objects.all()
    return render(request, "mi_app/alimentacion/all.html", {"alimentos": alimentos})

def registrarAlimento(request):
    return render(request, "mi_app/alimentacion/registrar.html")

class AlimentacionValidate(forms.Form):
    descripcion = forms.CharField(
        label="Descripción", 
        max_length=1000, 
        error_messages={'required': 'La descripción es obligatoria.'}
    )
    dosis = forms.FloatField(
        label="Dosis", 
        min_value=0.1,  # La dosis no puede ser menor o igual a cero
        error_messages={'required': 'La dosis es obligatoria.'}
    )

    # Validación personalizada para descripción
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if len(descripcion) < 10:
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return descripcion

    # Validación personalizada para dosis
    def clean_dosis(self):
        dosis = self.cleaned_data.get('dosis')
        if dosis <= 0:
            raise forms.ValidationError("La dosis debe ser mayor a cero.")
        return dosis

def saveAlimento(request):
    if(request.method == 'POST'):
        form = AlimentacionValidate(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data.get('descripcion')
            dosis = form.cleaned_data.get('dosis')

            alimentacion = Alimentacion(descripcion = descripcion, dosis = dosis)
            alimentacion.save()

            return redirect("/alimentos/all")
        else:
            return render(request, 'mi_app/alimentacion/registrar.html', {"form": form})
        
    return redirect("/alimentos/all", {"msg": "Error de peticion al guardar el alimento"})

def deleteAlimento(request, idalimentacion):
    alimento = Alimentacion.objects.get(idalimentacion = idalimentacion)
    if(alimento):
        alimento.delete()
        return render(request, "mi_app/alimentacion/all.html", {"msg": "Eliminacion completa"})
    
    return render(request, "mi_app/alimentacion/all.html", {"msg": "Error al eliminar el alimento"})
            
