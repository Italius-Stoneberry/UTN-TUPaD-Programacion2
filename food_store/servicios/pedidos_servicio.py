from food_store.entidades.Pedido import Pedido
from food_store.entidades.Usuario import Usuario
from food_store.enums import Estado, FormaPago
from food_store.excepciones import (
    EntidadNoEncontradaError,
    OperacionNoPermitidaError,
    DatoInvalidoError,
)


# Transiciones de estado válidas
_TRANSICIONES: dict[Estado, list[Estado]] = {
    Estado.PENDIENTE: [Estado.CONFIRMADO, Estado.CANCELADO],
    Estado.CONFIRMADO: [Estado.TERMINADO, Estado.CANCELADO],
    Estado.TERMINADO: [],
    Estado.CANCELADO: [],
}


class PedidoServicio:
    """Servicio que gestiona la colección de pedidos."""

    def __init__(self) -> None:
        self.__pedidos: list[Pedido] = []

    # ── Alta ─────────────────────────────────────────────────────

    def crear(self, usuario: Usuario, forma_pago: FormaPago) -> Pedido:
        if usuario.eliminado:
            raise DatoInvalidoError("No se puede crear un pedido para un usuario eliminado.")
        pedido = Pedido(usuario, forma_pago)
        return pedido

    def registrar(self, pedido: Pedido) -> None:
        """Agrega el pedido a la colección y descuenta stock."""
        for detalle in pedido.detalles:
            detalle.producto.stock -= detalle.cantidad
        self.__pedidos.append(pedido)

    # ── Baja lógica ──────────────────────────────────────────────

    def eliminar(self, id_pedido: int) -> None:
        pedido = self.buscar_por_id(id_pedido)
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            self._devolver_stock(pedido)
        pedido.eliminado = True
        for detalle in pedido.detalles:
            detalle.eliminado = True

    # ── Cambio de estado ─────────────────────────────────────────

    def cambiar_estado(self, id_pedido: int, nuevo_estado: Estado) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        estados_permitidos = _TRANSICIONES.get(pedido.estado, [])
        if nuevo_estado not in estados_permitidos:
            raise OperacionNoPermitidaError(
                f"No se puede pasar de {pedido.estado.value} a {nuevo_estado.value}."
            )
        if nuevo_estado == Estado.CANCELADO:
            self._devolver_stock(pedido)
        pedido.estado = nuevo_estado
        return pedido

    # ── Cambio de forma de pago ──────────────────────────────────

    def cambiar_forma_pago(self, id_pedido: int, forma_pago: FormaPago) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        pedido.forma_pago = forma_pago
        return pedido

    # ── Consultas ────────────────────────────────────────────────

    def listar(self) -> list[Pedido]:
        return [p for p in self.__pedidos if not p.eliminado]

    def listar_por_usuario(self, usuario: Usuario) -> list[Pedido]:
        return [
            p for p in self.__pedidos
            if not p.eliminado and p.usuario == usuario
        ]

    def buscar_por_id(self, id_pedido: int) -> Pedido:
        for p in self.__pedidos:
            if p.id == id_pedido and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"Pedido con id {id_pedido} no encontrado.")

    def buscar_por_id_y_usuario(self, id_pedido: int, usuario: Usuario) -> Pedido:
        """Para clientes: solo pueden ver sus propios pedidos."""
        pedido = self.buscar_por_id(id_pedido)
        if pedido.usuario != usuario:
            raise EntidadNoEncontradaError(f"Pedido con id {id_pedido} no encontrado.")
        return pedido

    # ── Internos ─────────────────────────────────────────────────

    @staticmethod
    def _devolver_stock(pedido: Pedido) -> None:
        for detalle in pedido.detalles:
            detalle.producto.stock += detalle.cantidad
            