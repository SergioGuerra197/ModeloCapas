from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django import forms
from mi_app.models import Alimentacion, Clientes, Porcinos, PorcinosHasAlimentacion, Razas


from datetime import datetime
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from reportlab.lib.units import cm

def index(request):
    clientes = Clientes.objects.all()
    razas = Razas.objects.all()
    alimentacion = Alimentacion.objects.all()
    return render(request, 'mi_app/index.html', {'clientes': clientes, 'razas':razas, 'alimentaciones':alimentacion})

def porcinos(request):
    porcinos = Porcinos.objects.all()
    alimentacion = Alimentacion.objects.all()
    return render(request, 'mi_app/porcinos.html', {'porcinos': porcinos, 'alimentaciones':alimentacion})

def alimentacion(request):
    alimentaciones = Alimentacion.objects.all()
    return render(request, 'mi_app/alimentacion.html', {'alimentaciones': alimentaciones})

# Define your form class
class MyForm(forms.Form):
    cedula = forms.CharField(label="cedula")
    nombre = forms.CharField(label="nombre")
    apellidos = forms.CharField(label="apellidos")
    direccion = forms.CharField(label="direccion")
    telefono = forms.CharField(label="telefono")

class MyFormAlimentacion(forms.Form):
    idalimentacion = forms.CharField(label="idalimentacion")
    descripcion = forms.CharField(label="descripcion")
    dosis = forms.CharField(label="dosis")

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
    # Obtener los cerdos asociados a este cliente
    cerdos = Porcinos.objects.filter(clientes_cedula=cedula)

    # Preparar la información del cliente
    data = {
        'cedula': cliente.cedula,
        'nombre': cliente.nombre,
        'apellidos': cliente.apellidos,
        'direccion': cliente.direccion,
        'telefono': cliente.telefono,
        'cerdos': [
            {
                'id': cerdo.idporcinos,
                'edad': cerdo.edad,
                'peso': cerdo.peso,
                'raza': cerdo.razas_idrazas.name  # Asumiendo que tienes un campo 'razas_idrazas' con 'name'
            } for cerdo in cerdos
        ]
    }

    print(data)
    return JsonResponse(data)

def eliminarCliente(request, cedula):
    cliente = Clientes.objects.get(cedula = cedula)
    if(cliente):
        porcinos = Porcinos.objects.filter(clientes_cedula = cliente)
        for porcino in porcinos:
            alimentosPorcino = PorcinosHasAlimentacion.objects.filter(porcinos_idporcinos = porcino)

            alimentosPorcino.delete()
        porcinos.delete()
        cliente.delete()

        return redirect("index")
    return redirect("index")


def actualizarCliente(request, cedula):
    # Obtener el cliente por su cédula
    cliente = get_object_or_404(Clientes, cedula=cedula)
    
    if request.method == 'POST':
        # Actualizar los campos del cliente con los datos enviados en el formulario
        cliente.nombre = request.POST.get('nombre')
        cliente.apellidos = request.POST.get('apellidos')
        cliente.direccion = request.POST.get('direccion')
        cliente.telefono = request.POST.get('telefono')
        
        # Guardar los cambios en la base de datos
        cliente.save()

        # Redirigir a la página principal después de actualizar
        return redirect('index')

    return HttpResponse("Método no permitido", status=405)


# Agregar porcino desde cliente 
def agregar_porcino(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        cliente_cedula = request.POST.get('cliente_cedula')
        edad = request.POST.get('edad')
        peso = request.POST.get('peso')
        raza_id = request.POST.get('razas_idrazas')  # Obtener el ID de la raza seleccionada
        alimentacionForm = request.POST.get('alimentacion')

        # Buscar el cliente en la base de datos
        cliente = get_object_or_404(Clientes, cedula=cliente_cedula)
        print(cliente)
        # Buscar la raza seleccionada en la base de datos usando el ID
        raza = get_object_or_404(Razas, idrazas=raza_id)
        print(raza)
        # Crear un nuevo porcino y asociarlo al cliente y la raza
        porcino = Porcinos(edad=edad, peso=peso, razas_idrazas=raza, clientes_cedula=cliente)
        porcino.save()


        alimentacion = get_object_or_404(Alimentacion, idalimentacion = alimentacionForm)
        alimentosPorcino = PorcinosHasAlimentacion(porcinos_idporcinos = porcino, alimentacion_idalimentacion = alimentacion)
        alimentosPorcino.save()

        

        # Redirigir a la página de porcinos o a donde prefieras
        return redirect('index')

    return HttpResponse('Método no permitido', status=405)


def reportClientes(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Clientes-report.pdf'

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setLineWidth(.3)
    c.setFont('Helvetica', 22)
    c.drawString(30,750,'Granjas SA')
    c.setFont('Helvetica', 12)
    c.drawString(30, 735, 'Reporte')

    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime("%Y-%m-%d")

    c.setFont('Helvetica-Bold', 12)
    c.drawString(480, 750, fecha_formateada)

    c.line(460, 747, 560, 747)

    #Table header
    styles = getSampleStyleSheet()
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSyze = 10

    numero = Paragraph('''No. ''', styleBH)
    cliente = Paragraph('''Nombre completo ''', styleBH)
    cedula = Paragraph('''C.C. ''', styleBH)
    direccion = Paragraph('''direccion ''', styleBH)
    telefono = Paragraph('''telefono ''', styleBH)
    numeroPorcinos = Paragraph('''No. Porcinos ''', styleBH)

    data = []
    data.append([numero, cliente, cedula, direccion, telefono, numeroPorcinos])

    styles = getSampleStyleSheet()
    styleBH = styles["BodyText"]
    styleBH.alignment = TA_CENTER
    styleBH.fontSyze = 7

    width, height = A4
    high = 650

    clientes = Clientes.objects.all()

    counter = 0
    for cliente in clientes:
        porcinos = Porcinos.objects.filter(clientes_cedula = cliente)
        this_cliente = [str(counter+1) + ".", 
                        cliente.nombre + " " + cliente.apellidos, 
                        cliente.cedula,
                        cliente.direccion,
                        cliente.telefono,
                        len(porcinos)
                        ]
        counter += 1
        data.append(this_cliente)

        high = high-18

    #tabla size
    width, height = A4
    table = Table(data, colWidths=[1.9*cm, 5.5*cm, 2.9*cm,2.9*cm,2.9*cm,2.9*cm])
    table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1, -1), 0.25, colors.black),
                               ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 30, high)
    c.showPage()

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


# Sección porcinos


def deletePorcino(request, idPorcino):
    porcino = Porcinos.objects.get(idporcinos = idPorcino)
    if(porcino):
        alimentosPorcino = PorcinosHasAlimentacion.objects.filter(porcinos_idporcinos = porcino)

        alimentosPorcino.delete()

        Porcinos.delete(porcino)
        return redirect('porcinos')
    return redirect('porcinos')



def getPorcino(request, idPorcino):
    porcino = Porcinos.objects.get(idporcinos = idPorcino)
    if(porcino):

        AlimentosPorcino = PorcinosHasAlimentacion.objects.filter(porcinos_idporcinos = porcino.idporcinos)

        alimentaciones = []
        for relacion in AlimentosPorcino:
        # Obtener el objeto de Alimentacion usando la relación
            alimentacion = relacion.alimentacion_idalimentacion
            alimentaciones.append({
            'descripcion': alimentacion.descripcion,
            'dosis': alimentacion.dosis
        })

        print(alimentaciones)
      

        data = {
            'idporcinos': porcino.idporcinos,
            'edad': porcino.edad,
            'peso': porcino.peso,
            'razas_idrazas': porcino.razas_idrazas.name,
            'clientes_cedula': porcino.clientes_cedula.cedula,
            'alimentacion': alimentaciones
        }
        return JsonResponse(data)
    
    return redirect("/")

def actualizarPorcino(request, idPorcino):
     
    porcino = get_object_or_404(Porcinos, idporcinos=idPorcino)
    
    if request.method == 'POST':
            # Actualizar los campos del cliente con los datos enviados en el formulario
            porcino.edad = request.POST.get('edad')
            porcino.peso = request.POST.get('peso')
            # Guardar los cambios en la base de datos
            porcino.save()

            # Redirigir a la página principal después de actualizar
            return redirect('porcinos')

    return HttpResponse("Método no permitido", status=405)

def agregarAlimentacion(request):
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        dosis = request.POST.get('dosis')

        # Crear un nuevo objeto de Alimentacion y guardarlo en la base de datos
        nueva_alimentacion = Alimentacion(descripcion=descripcion, dosis=dosis)
        nueva_alimentacion.save()

        # Redirigir a una página de éxito o a donde desees
        return redirect('alimentacion')  # Cambia esto al nombre de la vista

    return HttpResponse("Método no permitido", status=405)

def deleteAlimento(request, idalimentacion):

    alimento = Alimentacion.objects.get(idalimentacion = idalimentacion)
    if(alimento):

        alimentosPorcino = PorcinosHasAlimentacion.objects.filter(alimentacion_idalimentacion = idalimentacion)

        alimentosPorcino.delete()

        alimento.delete()

        return redirect('alimentacion')
    
    return render(request, "mi_app/alimentacion/all.html", {"msg": "Error al eliminar el alimento"})

def editarDosis(request, idalimentacion):
    alimento = get_object_or_404(Alimentacion, idalimentacion = idalimentacion )
    if request.method == 'POST':
        # Actualizar los campos del cliente con los datos enviados en el formulario
        alimento.dosis = request.POST.get('dosis')  
        print(alimento.dosis)        # Guardar los cambios en la base de datos
        alimento.save()

        # Redirigir a la página principal después de actualizar
        return redirect('alimentacion')

    return HttpResponse("Método no permitido", status=405)


def getAlimento(request, idalimentacion):
    # Obtener el cliente de la base de datos según la cédula

    alimento = get_object_or_404(Alimentacion, idalimentacion = idalimentacion )
    data = {
        'idalimentacion': alimento.idalimentacion,
        'descripcion': alimento.descripcion,
        'dosis': alimento.dosis,
    }
    return JsonResponse(data)
