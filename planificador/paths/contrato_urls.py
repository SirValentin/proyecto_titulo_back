from django.urls import path
from planificador.views import contrato

urlpatterns = [
    path("create/", contrato.ContratoView.as_view({"post": "create"})),
    path("list/", contrato.ContratoView.as_view({"get": "list"})),
    path("list_jornadas/", contrato.ContratoView.as_view({"get": "list_jornadas"})),
    path("<int:pk>/delete/", contrato.ContratoView.as_view({"post": "delete"})),
]
