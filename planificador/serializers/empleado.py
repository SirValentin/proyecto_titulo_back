from rest_framework.serializers import (
    ModelSerializer,
)

from planificador.models import Empleado


class EmpleadoSerializer(ModelSerializer):

    class Meta:
        model = Empleado
        fields = "__all__"
