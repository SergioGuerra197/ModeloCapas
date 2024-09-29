from rest_framework import viewsets
from .models import *
from .serializer import clienteSerializer, porcinoSerializer, alimentosSerializer, porcinosHasAlimentacionSerializer, razasSerializer

# Create your views here.


class clienteViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = clienteSerializer

class porcinosViewSet(viewsets.ModelViewSet):
    queryset = Porcinos.objects.all()
    serializer_class = porcinoSerializer

class alimentosViewSet(viewsets.ModelViewSet):
    queryset = Alimentacion.objects.all()
    serializer_class = alimentosSerializer

class porcinosHasAlimentacionViewSet(viewsets.ModelViewSet):
    queryset = PorcinosHasAlimentacion.objects.all()
    serializer_class = porcinosHasAlimentacionSerializer

class razasViewSet(viewsets.ModelViewSet):
    queryset = Razas.objects.all()
    serializer_class = razasSerializer