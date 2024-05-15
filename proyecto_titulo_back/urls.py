from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("djoser.urls")),
    path("api/v1/", include("djoser.urls.authtoken")),
    path("api/v1/empresa/", include("planificador.paths.empresa_urls")),
    path("api/v1/sucursal/", include("planificador.paths.sucursal_urls")),
    path("api/v1/cargo/", include("planificador.paths.cargo_urls")),
    path("api/v1/contrato/", include("planificador.paths.contrato_urls")),
    path("api/v1/empleado/", include("planificador.paths.empleado_urls")),
    path("api/v1/turno/", include("planificador.paths.turno_urls")),
    path("api/v1/solicitud/", include("planificador.paths.solicitud_urls")),
]
