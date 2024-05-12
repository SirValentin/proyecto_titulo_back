from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from planificador.serializers.cargo import CargoSerializer
from planificador.models import Admin, Cargo
from planificador.global_funtions import getEmpresa


class CargoView(ModelViewSet):
    serializer_class = CargoSerializer

    def create(self, request):
        if request.user.is_authenticated:
            empresa = getEmpresa(request)

            serializer = self.get_serializer(Cargo(empresa=empresa), data=request.data)

            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "Por favor, inicia sesión para acceder a esta vista", status=401
            )

    def list(self, request):
        empresa = getEmpresa(request)
        cargos = Cargo.objects.filter(empresa=empresa)
        serializer = CargoSerializer(cargos, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        cargo = Cargo.objects.get(pk=pk)
        if cargo:
            cargo.delete()
            return Response(pk, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
