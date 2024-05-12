from django.urls import path
from planificador.views import turno

urlpatterns = [
    path("create/", turno.TurnoView.as_view({"post": "create"})),
    path("lista_turnos/", turno.TurnoView.as_view({"post": "lista_turnos"})),
    path("borrar_turno/", turno.TurnoView.as_view({"post": "borrar_turno"})),
    path("asignar_turno/", turno.TurnoView.as_view({"post": "asignar_turno"})),
]
