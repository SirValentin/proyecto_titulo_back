from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from planificador.serializers.empleado import EmpleadoSerializer
from planificador.models import Admin, Empleado, Cargo, Sucursal, Contrato
from planificador.global_funtions import getEmpresa


class EmpleadoView(ModelViewSet):
    serializer_class = EmpleadoSerializer

    def create(self, request):
        if request.user.is_authenticated:
            cargo_id = request.data.pop("cargo")
            sucursal_id = request.data.pop("sucursal")
            contrato_id = request.data.pop("contrato")
            email = request.data.pop("email")

            cargo = Cargo.objects.filter(id=cargo_id).first()
            sucursal = Sucursal.objects.filter(id=sucursal_id).first()
            contrato = Contrato.objects.filter(id=contrato_id).first()

            serializer = self.get_serializer(
                Empleado(cargo=cargo, sucursal=sucursal, contrato=contrato),
                data=request.data,
            )

            if serializer.is_valid():
                empleado = Empleado.objects.create(
                    nombre=request.data.get("nombre"),
                    apellido=request.data.get("apellido"),
                    rut=request.data.get("rut"),
                    cargo=cargo,
                    sucursal=sucursal,
                    contrato=contrato,
                )
                empleado.create_usuario_empleado(email)
                empleado.save()
                return Response(
                    EmpleadoSerializer(empleado).data, status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "Por favor, inicia sesión para acceder a esta vista", status=401
            )

    def list(self, request):
        empresa = getEmpresa(request)
        sucursales = Sucursal.objects.filter(empresa=empresa).values("id")
        empleados = Empleado.objects.filter(sucursal__in=sucursales)
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        empleado = Empleado.objects.get(pk=pk)
        if empleado:
            empleado.delete()
            return Response(pk, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
