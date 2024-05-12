from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from planificador.serializers.turno import TurnoSerializer
from planificador.models import Admin, Empleado, Cargo, Sucursal, Turno
from planificador.global_funtions import getEmpresa


class TurnoView(ModelViewSet):
    serializer_class = TurnoSerializer

    def create(self, request):
        if request.user.is_authenticated:
            hora_inicio = datetime.strptime(request.data["hora_inicio"], "%H:%M")
            hora_final = datetime.strptime(request.data["hora_final"], "%H:%M")
            colacion = request.data.get("colacion")
            seleccionados = request.data.get("seleccionados")
            lista_turnos = []
            for item in seleccionados:
                objeto_empleado = Empleado.objects.filter(id=item["empleado"]).first()
                sucursal = Sucursal.objects.filter(
                    id=objeto_empleado.sucursal.id
                ).first()
                cargo = Cargo.objects.filter(id=objeto_empleado.cargo.id).first()
                for fecha in item["fechas"]:
                    try:
                        turno_creado = Turno(
                            empleado=objeto_empleado,
                            cargo=cargo,
                            sucursal=sucursal,
                            fecha=fecha,
                            hora_inicio=hora_inicio,
                            hora_final=hora_final,
                            colacion=colacion,
                        )
                        lista_turnos.append(turno_creado)
                    except:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
            turnos = Turno.objects.bulk_create(lista_turnos)
            return Response(
                TurnoSerializer(turnos, many=True).data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                "Por favor, inicia sesión para acceder a esta vista", status=401
            )

    def lista_turnos(self, request):
        # empresa = getEmpresa(request)
        # sucursales = Sucursal.objects.filter(empresa=empresa).values("id")
        empleados_ids = request.data.get("empleados")

        fecha_inicio = request.data.get("fecha_inicio")
        fecha_final = request.data.get("fecha_final")
        # lista_empleados = Empleado.objects.filter(sucursal__in=sucursales)
        turnos = Turno.objects.filter(
            empleado__in=empleados_ids, fecha__range=[fecha_inicio, fecha_final]
        )
        serializer = TurnoSerializer(turnos, many=True)
        return Response(serializer.data)

    def borrar_turno(self, request):
        ids_turnos = request.data.get("turnos")
        turnos = Turno.objects.filter(id__in=ids_turnos)
        if turnos:
            turnos.delete()
            return Response(ids_turnos, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def asignar_turno(self, request):
        ids_turnos = request.data.get("turnos")
        turnos = Turno.objects.filter(id__in=ids_turnos)
        if turnos:
            turnos.update(estado=2)
            return Response(
                TurnoSerializer(turnos, many=True).data, status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
