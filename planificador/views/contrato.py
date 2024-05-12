from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from planificador.serializers.contrato import ContratoSerializer, TipoJornadaSerializer
from planificador.models import Admin, Contrato, TipoJornada
from planificador.global_funtions import getEmpresa


class ContratoView(ModelViewSet):
    serializer_class = ContratoSerializer

    def create(self, request):
        if request.user.is_authenticated:
            empresa = getEmpresa(request)
            id_jornada = request.data.pop("jornada", None)
            jornada = TipoJornada.objects.filter(id=id_jornada).first()
            serializer = self.get_serializer(
                Contrato(empresa=empresa, tipo=jornada), data=request.data
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
        contrato = Contrato.objects.filter(empresa=empresa)
        serializer = ContratoSerializer(contrato, many=True)
        return Response(serializer.data)

    def list_jornadas(self, request):
        jornadas = TipoJornada.objects.all()
        serializer = TipoJornadaSerializer(jornadas, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        contrato = Contrato.objects.get(pk=pk)
        if contrato:
            contrato.delete()
            return Response(pk, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
