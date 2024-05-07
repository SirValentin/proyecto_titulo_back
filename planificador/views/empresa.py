from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from planificador.serializers.empresa import EmpresaSerializer
from planificador.models import Admin, User


class EmpresaView(ModelViewSet):
    def create(self, request):
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            empresa = serializer.save()
            usuario = User.objects.filter(id=request.data.get("usuario")).first()
            Admin.objects.create(user=usuario, empresa=empresa)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
