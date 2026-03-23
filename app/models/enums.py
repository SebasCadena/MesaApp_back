from enum import Enum


class MesaEstado(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    OCUPADA = "OCUPADA"
    RESERVADA = "RESERVADA"
    MANTENIMIENTO = "MANTENIMIENTO"


class ReservaEstado(str, Enum):
    ACTIVA = "ACTIVA"
    CANCELADA = "CANCELADA"
    FINALIZADA = "FINALIZADA"


class PedidoEstado(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PREPARACION = "EN_PREPARACION"
    LISTO = "LISTO"
    ENTREGADO = "ENTREGADO"
    PAGADO = "PAGADO"
    CANCELADO = "CANCELADO"


class PedidoTipo(str, Enum):
    MESA = "MESA"
    DOMICILIO = "DOMICILIO"


class MetodoPago(str, Enum):
    EFECTIVO = "EFECTIVO"
    TARJETA = "TARJETA"
    TRANSFERENCIA = "TRANSFERENCIA"
    QR = "QR"


class TipoMovimientoInventario(str, Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"
    AJUSTE = "AJUSTE"
