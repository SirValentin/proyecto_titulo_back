from django.urls import path
from planificador.views import sucursal

urlpatterns = [
    path("create/", sucursal.SucursalView.as_view({"post": "create"})),
    path("list/", sucursal.SucursalView.as_view({"get": "list"})),
    path("<int:pk>/delete/", sucursal.SucursalView.as_view({"post": "delete"})),
]
