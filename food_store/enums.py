from enum import Enum


class Rol(Enum):
    """Roles disponibles en el sistema."""
    ADMIN = "ADMIN"
    USUARIO = "USUARIO"


class Estado(Enum):
    """Estados posibles de un pedido."""
    PENDIENTE = "PENDIENTE"
    CONFIRMADO = "CONFIRMADO"
    TERMINADO = "TERMINADO"
    CANCELADO = "CANCELADO"


class FormaPago(Enum):
    """Formas de pago aceptadas."""
    TARJETA = "TARJETA"
    TRANSFERENCIA = "TRANSFERENCIA"
    EFECTIVO = "EFECTIVO"
