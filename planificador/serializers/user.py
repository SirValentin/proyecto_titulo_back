from rest_framework.serializers import ModelSerializer, SerializerMethodField
from planificador.models import User, Empleado


class UserSerializer(ModelSerializer):
    id_empleado = SerializerMethodField(required=False, read_only=True)

    class Meta:
        model = User()
        fields = (
            "id",
            "email",
            "es_empleado",
            "es_superuser",
            "id_empleado",
        )

    def get_id_empleado(self, instance):
        empleado = Empleado.objects.filter(user_id=instance.id).first()
        if empleado:
            return empleado.id
        return ""
