from django.urls import path
from planificador.views import empleado

urlpatterns = [
    path("create/", empleado.EmpleadoView.as_view({"post": "create"})),
    path("list/", empleado.EmpleadoView.as_view({"get": "list"})),
    path("<int:pk>/delete/", empleado.EmpleadoView.as_view({"post": "delete"})),
]
