from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING

from food_store.entidades.Base import Base
from food_store.entidades.Calculable import Calculable
from food_store.entidades.DetallePedido import DetallePedido
from food_store.enums import Estado, FormaPago
from food_store.excepciones import DatoInvalidoError, StockInsuficienteError

if TYPE_CHECKING:
    from food_store.entidades.Producto import Producto
    from food_store.entidades.Usuario import Usuario


class Pedido(Base, Calculable):
    """Representa un pedido con sus detalles. Implementa Calculable."""

    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__total: float = 0.0
        self.__forma_pago: FormaPago = forma_pago
        self.__usuario: Usuario = usuario
        self.__detalles: list[DetallePedido] = []

   

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @property
    def total(self) -> float:
        return self.__total

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        self.__forma_pago = valor

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        return tuple(self.__detalles)

    @estado.setter
    def estado(self, valor: Estado) -> None:
        self.__estado = valor

    # ── Métodos ─────────────────────────────────────────────────

    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        """Agrega un detalle. Si el producto ya existe, suma la cantidad."""
        if cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a 0.")
        if cantidad > producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente para '{producto.nombre}'. "
                f"Disponible: {producto.stock}, pedido: {cantidad}."
            )

        detalle_existente = self.buscar_detalle_por_producto(producto)
        if detalle_existente is not None:
            nueva_cantidad = detalle_existente.cantidad + cantidad
            if nueva_cantidad > producto.stock:
                raise StockInsuficienteError(
                    f"Stock insuficiente para '{producto.nombre}'. "
                    f"Disponible: {producto.stock}, total pedido: {nueva_cantidad}."
                )
            detalle_existente.cantidad = nueva_cantidad
        else:
            detalle = DetallePedido(cantidad, producto)
            self.__detalles.append(detalle)

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        """Busca un detalle por producto. Devuelve None si no lo encuentra."""
        for detalle in self.__detalles:
            if detalle.producto == producto:
                return detalle
        return None

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        """Elimina el detalle que corresponde al producto dado."""
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is not None:
            self.__detalles.remove(detalle)

    def calcular_total(self) -> None:
        """Implementación de Calculable. Suma los subtotales."""
        self.__total = sum(d.subtotal for d in self.__detalles)

    # ── __str__ ─────────────────────────────────────────────────

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.__fecha} | {self.__usuario.nombre} {self.__usuario.apellido} | "
            f"{self.__estado.value} | {self.__forma_pago.value} | Total: ${self.__total:.2f}"
        )