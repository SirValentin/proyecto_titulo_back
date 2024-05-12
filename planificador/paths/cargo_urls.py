from django.urls import path
from planificador.views import cargo

urlpatterns = [
    path("create/", cargo.CargoView.as_view({"post": "create"})),
    path("list/", cargo.CargoView.as_view({"get": "list"})),
    path("<int:pk>/delete/", cargo.CargoView.as_view({"post": "delete"})),
]
