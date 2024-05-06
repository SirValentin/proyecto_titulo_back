from django.urls import path
from planificador.views import empresa

urlpatterns = [
    path("create/", empresa.EmpresaView.as_view({"post": "create"})),
]
