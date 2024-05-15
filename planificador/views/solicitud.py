from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from planificador.serializers.turno import TurnoSerializer
from planificador.models import Admin, Empleado, Cargo, Sucursal, Turno, Solicitud
from planificador.global_funtions import getEmpresa
from planificador.serializers.solicitud import SolicitudSerializer


class SolicitudView(ModelViewSet):
    serializer_class = SolicitudSerializer

    def crear_cambio_turno(self, request):
        turno1 = request.data.get("turno1")
        turno2 = request.data.get("turno2")
        tipo = request.data.get("tipo")
        empleado_id = request.data.get("empleado")
        comentario = request.data.get("comentario")

        empleado = Empleado.objects.filter(id=empleado_id).first()
        turnos = Turno.objects.filter(
            empleado_id=empleado, fecha__in=[turno1, turno2]
        ).values_list("id", flat=True)

        solicitud_creada = Solicitud.objects.create(
            empleado=empleado,
            tipo=tipo,
            comentario=comentario,
        )
        solicitud_creada.turno.set(turnos)
        return Response(
            SolicitudSerializer(solicitud_creada).data, status=status.HTTP_201_CREATED
        )
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def lista_solicitudes_empleado(self, request, pk):
        solicitudes_empleado = Solicitud.objects.filter(empleado=pk)
        serializer = SolicitudSerializer(solicitudes_empleado, many=True)
        return Response(serializer.data)

    def lista_solicitudes(self, request):
        empresa = getEmpresa(request)
        empleados = Empleado.objects.filter(sucursal__empresa=empresa)
        solicitudes = Solicitud.objects.filter(empleado__in=empleados)
        serializer = SolicitudSerializer(solicitudes, many=True)
        return Response(serializer.data)

    def aprobar_solicitud(self, request):
        id_solicitud = request.data.get("solicitud")
        estado = request.data.get("estado")
        solicitud = Solicitud.objects.filter(id=id_solicitud).first()
        solicitud.estado = estado
        solicitud.save()

        turnos = Turno.objects.filter(id__in=solicitud.turno.all().values("id"))
        turno1 = turnos[0]
        fecha_turno1 = turno1.fecha
        turno2 = turnos[1]
        fecha_turno2 = turno2.fecha

        turno1.fecha = fecha_turno2
        turno1.save()
        turno2.fecha = fecha_turno1
        turno2.save()

        return Response(SolicitudSerializer(solicitud).data)

    def rechazar_solicitud(self, request):
        id_solicitud = request.data.get("solicitud")
        estado = request.data.get("estado")

        solicitud = Solicitud.objects.filter(id=id_solicitud).first()
        solicitud.estado = estado
        solicitud.save()

        return Response(SolicitudSerializer(solicitud).data)

    def borrar_solicitud(self, request, pk):
        solicitud = Solicitud.objects.filter(id=pk).first()
        if solicitud:
            solicitud.delete()
            return Response(pk, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
