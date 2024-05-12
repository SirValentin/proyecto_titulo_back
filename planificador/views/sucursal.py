from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from planificador.serializers.sucursal import SucursalSerializer
from planificador.models import Admin, Sucursal
from planificador.global_funtions import getEmpresa


class SucursalView(ModelViewSet):
    serializer_class = SucursalSerializer

    def create(self, request):
        if request.user.is_authenticated:
            empresa = getEmpresa(request)

            serializer = self.get_serializer(
                Sucursal(empresa=empresa), data=request.data
            )

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
        sucursales = Sucursal.objects.filter(empresa=empresa)
        serializer = SucursalSerializer(sucursales, many=True)
        return Response(serializer.data)

    # def detail(request, pk):
    #     empresa = Empresa.objects.get(pk=pk)
    #     serializer = EmpresaSerializer(empresa)
    #     return Response(serializer.data)

    # def update(request, pk):
    #     sucursal = Sucursal.objects.get(pk=pk)
    #     serializer = SucursalSerializer(instance=sucursal, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        sucursal = Sucursal.objects.get(pk=pk)
        if sucursal:
            sucursal.delete()
            return Response(pk, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
