from enum import Enum


class TipoTurno(Enum):
    Turno = 1
    Permiso = 2
    DiaLibre = 3


class EstadoTurno(Enum):
    Planificado = 1
    Asignado = 2


class TipoSolicitud(Enum):
    CambioTurno = 1
    DiaLibre = 2
    Ausencia = 3


class EstadoSolicitud(Enum):
    EnRevision = 1
    Aceptado = 2
    Rechazado = 3
