from rest_framework.serializers import (
    ModelSerializer,
)

from planificador.models import Cargo


class CargoSerializer(ModelSerializer):

    class Meta:
        model = Cargo
        fields = ("id", "nombre", "descripcion")
        read_only_fields = ("id", "empresa")
