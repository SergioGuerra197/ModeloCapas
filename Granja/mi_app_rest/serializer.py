from rest_framework import serializers
from .models import *


class clienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        # fields = ('fullname', 'nickname')
        fields = '__all__'