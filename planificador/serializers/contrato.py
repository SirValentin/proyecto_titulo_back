from rest_framework.serializers import (
    ModelSerializer,
)

from planificador.models import Contrato, TipoJornada


class ContratoSerializer(ModelSerializer):

    class Meta:
        model = Contrato
        fields = ("id", "nombre", "horas_semanales", "tipo")
        read_only_fields = ("id", "empresa", "tipo")


class TipoJornadaSerializer(ModelSerializer):

    class Meta:
        model = TipoJornada
        fields = "__all__"
