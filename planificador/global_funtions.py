from planificador.models import Admin


def getEmpresa(request):
    admin = request.user.usuario_admin.first()
    empresa = Admin.objects.filter(id=admin.id).first().empresa
    if empresa:
        return empresa
    return None
