from rest_framework import viewsets
from .models import Clientes
from .serializer import clienteSerializer

# Create your views here.


class clienteViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = clienteSerializer