from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django import forms
from mi_app.models import Clientes, Porcinos, PorcinosHasAlimentacion, Razas


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
    return render(request, 'mi_app/index.html', {'clientes': clientes, 'razas':razas})

def porcinos(request):
    porcinos = Porcinos.objects.all()
    print(porcinos)
    return render(request, 'mi_app/porcinos.html', {'porcinos': porcinos})

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

        # Buscar el cliente en la base de datos
        cliente = get_object_or_404(Clientes, cedula=cliente_cedula)
        print(cliente)
        # Buscar la raza seleccionada en la base de datos usando el ID
        raza = get_object_or_404(Razas, idrazas=raza_id)
        print(raza)
        # Crear un nuevo porcino y asociarlo al cliente y la raza
        porcino = Porcinos(edad=edad, peso=peso, razas_idrazas=raza, clientes_cedula=cliente)
        porcino.save()
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


#----------------- REPORTES -------------------------------