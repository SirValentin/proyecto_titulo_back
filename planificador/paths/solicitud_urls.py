from django.urls import path
from planificador.views import solicitud

urlpatterns = [
    path(
        "cambio_turno/", solicitud.SolicitudView.as_view({"post": "crear_cambio_turno"})
    ),
    path(
        "borrar/<int:pk>/",
        solicitud.SolicitudView.as_view({"post": "borrar_solicitud"}),
    ),
    path("aprobar/", solicitud.SolicitudView.as_view({"post": "aprobar_solicitud"})),
    path("rechazar/", solicitud.SolicitudView.as_view({"post": "rechazar_solicitud"})),
    path(
        "lista_solicitudes/<int:pk>/",
        solicitud.SolicitudView.as_view({"get": "lista_solicitudes_empleado"}),
    ),
    path(
        "lista_solicitudes/",
        solicitud.SolicitudView.as_view({"get": "lista_solicitudes"}),
    ),
    # path("borrar_turno/", turno.TurnoView.as_view({"post": "borrar_turno"})),
    # path("asignar_turno/", turno.TurnoView.as_view({"post": "asignar_turno"})),
]
