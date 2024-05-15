from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from planificador.models import Empleado, Solicitud, Turno
from planificador.serializers.turno import TurnoSerializer


class SolicitudSerializer(ModelSerializer):
    turnos = SerializerMethodField(required=False, read_only=True)
    nombre_empleado = SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = Solicitud
        fields = "__all__"
        read_only_fields = ["id"]

    def get_turnos(self, instance):
        turnos = Turno.objects.filter(id__in=instance.turno.all().values("id"))
        serializer = TurnoSerializer(turnos, many=True)
        if serializer:
            return serializer.data
        return instance.turno

    def get_nombre_empleado(self, instance):
        nombre = instance.empleado.nombre
        apellido = instance.empleado.apellido
        nombre_completo = f"{nombre} {apellido}"

        return nombre_completo
