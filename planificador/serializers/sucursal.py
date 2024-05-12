from rest_framework.serializers import (
    ModelSerializer,
)

from planificador.models import Sucursal


class SucursalSerializer(ModelSerializer):

    class Meta:
        model = Sucursal
        fields = ("id", "nombre", "direccion")
        read_only_fields = ("id", "empresa")
