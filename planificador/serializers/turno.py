from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)

from planificador.models import Turno


class TurnoSerializer(ModelSerializer):
    hora_inicio = SerializerMethodField(required=False, read_only=True)
    hora_final = SerializerMethodField(required=False, read_only=True)
    nombre_sucursal = SerializerMethodField(required=False, read_only=True)
    nombre_cargo = SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = Turno
        fields = (
            "id",
            "empleado",
            "cargo",
            "nombre_cargo",
            "sucursal",
            "nombre_sucursal",
            "fecha",
            "hora_inicio",
            "hora_final",
            "colacion",
            "tipo",
            "estado",
        )
        read_only_fields = ["id"]

    def get_hora_inicio(self, instance):
        return instance.hora_inicio.strftime("%H:%M")

    def get_hora_final(self, instance):
        return instance.hora_final.strftime("%H:%M")

    def get_nombre_sucursal(self, instance):
        return instance.sucursal.nombre

    def get_nombre_cargo(self, instance):
        return instance.cargo.nombre
