from rest_framework.serializers import ModelSerializer
from planificador.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User()
        fields = (
            "id",
            "email",
            "es_empleado",
            "es_superuser",
        )
