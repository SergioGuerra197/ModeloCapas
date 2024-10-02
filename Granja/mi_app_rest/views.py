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

    def get_queryset(self):
        queryset = super().get_queryset()
        clientes_cedula = self.request.query_params.get('clientes_cedula', None)
        
        if clientes_cedula is not None:
            queryset = queryset.filter(clientes_cedula=clientes_cedula)
        
        return queryset

class alimentosViewSet(viewsets.ModelViewSet):
    queryset = Alimentacion.objects.all()
    serializer_class = alimentosSerializer

class porcinosHasAlimentacionViewSet(viewsets.ModelViewSet):
    queryset = PorcinosHasAlimentacion.objects.all()
    serializer_class = porcinosHasAlimentacionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        porcinos_id = self.request.query_params.get('porcinos_idporcinos', None)
        alimentacion_id = self.request.query_params.get('alimentacion_idalimentacion', None)

        if porcinos_id is not None:
            queryset = queryset.filter(porcinos_idporcinos=porcinos_id)
        if alimentacion_id is not None:
            queryset = queryset.filter(alimentacion_idalimentacion=alimentacion_id)

        return queryset

class razasViewSet(viewsets.ModelViewSet):
    queryset = Razas.objects.all()
    serializer_class = razasSerializer
