from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import (
    CharField,
    BooleanField,
    Model,
    ForeignKey,
    CASCADE,
    SET_NULL,
    IntegerField,
    TimeField,
    DateField,
    TextField,
    SmallIntegerField,
    ManyToManyField,
    OneToOneField,
    EmailField,
)

from planificador.enums import TipoTurno, TipoSolicitud, EstadoSolicitud, EstadoTurno


class UsuarioManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            email = ""
            raise ValueError("El email es obligatorio")
        else:
            user = self.model(
                email=self.normalize_email(email),
                es_empleado=False,
                es_superuser=False,
            )
        user.set_password(password)
        user.save()
        # empresa = Empresa.objects.create(nombre=nombre, rubro=rubro)
        # admin = Admin.objects.create(admin_email=user.email, empresa=empresa)
        # admin.user = user
        # admin.save()
        return user

    def create_superuser(self, email, password):
        if not email:
            email = ""
            raise ValueError("El email es obligatorio")
        else:
            user = self.model(
                email=self.normalize_email(email),
                es_empleado=False,
                es_superuser=True,
            )
        user.set_password(password)
        user.save()
        return user

    def create_empleado(self, email, es_empleado, es_superuser):
        user = self.model(
            email=self.normalize_email(email),
            es_empleado=es_empleado,
            es_superuser=es_superuser,
        )
        user.save()
        return user


class User(AbstractBaseUser):
    email = EmailField(verbose_name="correo electronico", unique=True)
    es_empleado = BooleanField(default=False)
    es_superuser = BooleanField(default=False)
    objects = UsuarioManager()

    def set_password_empleado(self, new_password):
        self.set_password(new_password)
        self.save()
        return True

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Admin(Model):
    rol = CharField(verbose_name="rol", max_length=50, blank=True, null=True)
    user = ForeignKey(
        "User",
        blank=False,
        null=True,
        verbose_name="Usuario al que esta vinculado",
        related_name="usuario_admin",
        on_delete=CASCADE,
    )
    empresa = ForeignKey("Empresa", on_delete=CASCADE)

    # def create_admin(self, email, password, rol, empresa):
    #     if email is None or email == "":
    #         return False
    #     user = User.objects.create_user(
    #         email=email, password=password, es_empleado=False, es_superuser=True
    #     )
    #     admin = Admin.objects.create(admin_email=user.email, rol=rol, empresa=empresa)
    #     return admin


class Empleado(Model):
    nombre = CharField(verbose_name="nombre", max_length=100, blank=True, null=True)
    apellido = CharField(verbose_name="apellido", max_length=100, blank=True, null=True)
    rut = CharField(verbose_name="rut", max_length=50, blank=True, null=False)
    sucursal = ForeignKey(
        "Sucursal", related_name="sucursal", blank=True, null=True, on_delete=SET_NULL
    )
    cargo = ForeignKey(
        "Cargo", related_name="cargo", blank=True, null=True, on_delete=SET_NULL
    )
    contrato = ForeignKey(
        "Contrato", related_name="contrato", blank=True, null=True, on_delete=SET_NULL
    )
    user = ForeignKey(
        "User",
        blank=False,
        null=True,
        verbose_name="Usuario al que esta vinculado",
        related_name="usuario_empleado",
        on_delete=CASCADE,
    )

    def create_usuario_empleado(self, email):
        if email is None or email == "":
            return False

        user = User.objects.create_empleado(
            email=email, es_empleado=True, es_superuser=False
        )
        user.set_password_empleado(self.rut.replace(".", "").replace("-", "")[:4])
        user.save()
        self.user = user
        self.save()

        return True


class Empresa(Model):
    nombre = CharField(
        verbose_name="nombre de empresa", max_length=100, blank=False, null=False
    )
    rubro = CharField(verbose_name="rubro", max_length=100, blank=True, null=True)


class Contrato(Model):
    empresa = ForeignKey(Empresa, on_delete=CASCADE)
    name = CharField(verbose_name="Nombre de contrato", max_length=80)
    tipo = ForeignKey(
        "TipoJornada", related_name="jornada", blank=True, null=True, on_delete=SET_NULL
    )
    horas_semanales = IntegerField()


class TipoJornada(Model):
    nombre_tipo = CharField(verbose_name="nombre tipo jornada", max_length=100)


class Cargo(Model):
    empresa = ForeignKey(Empresa, on_delete=CASCADE)
    nombre = CharField(verbose_name="Nombre de cargo", max_length=100)
    descripcion = CharField(
        verbose_name="Descripcion de cargo", max_length=200, blank=True, null=True
    )


class Sucursal(Model):
    empresa = ForeignKey(Empresa, on_delete=CASCADE)
    nombre = CharField(verbose_name="Nombre de sucursal", max_length=100)
    direccion = CharField(verbose_name="Direccion de sucursal", max_length=200)


class Turno(Model):
    empleado = ForeignKey(Empleado, on_delete=CASCADE)
    cargo = ForeignKey(Cargo, on_delete=CASCADE)
    sucursal = ForeignKey(Sucursal, on_delete=CASCADE)
    fecha = DateField()
    hora_inicio = TimeField()
    hora_final = TimeField()
    colacion = IntegerField()
    tipo = SmallIntegerField(
        choices=[(tag.value, tag.value) for tag in TipoTurno],
        default=TipoTurno.Turno.value,
        null=False,
        blank=False,
    )
    estado = SmallIntegerField(
        choices=[(tag.value, tag.value) for tag in EstadoTurno],
        default=EstadoTurno.Planificado.value,
        null=False,
        blank=False,
    )


class Solicitud(Model):
    empleado = ForeignKey(Empleado, on_delete=CASCADE)
    turno = ManyToManyField(Turno, related_name="turnos", blank=True)
    tipo = SmallIntegerField(
        choices=[(tag.value, tag.value) for tag in TipoSolicitud],
        default=TipoSolicitud.CambioTurno.value,
        null=False,
        blank=False,
    )
    fecha = DateField()
    estado = SmallIntegerField(
        choices=[(tag.value, tag.value) for tag in EstadoSolicitud],
        default=EstadoSolicitud.EnRevision.value,
        null=False,
        blank=False,
    )
    comentario = TextField()
