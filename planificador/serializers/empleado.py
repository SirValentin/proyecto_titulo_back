from rest_framework.serializers import ModelSerializer, SerializerMethodField

from planificador.models import Empleado, User


class EmpleadoSerializer(ModelSerializer):
    email = SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = Empleado
        fields = (
            "id",
            "nombre",
            "apellido",
            "rut",
            "sucursal",
            "cargo",
            "contrato",
            "email",
        )
        read_only_fields = ("id", "email")

    def get_email(self, instance):
        usuario = User.objects.filter(id=instance.user_id).first()
        if usuario:
            return usuario.email
        return ""
