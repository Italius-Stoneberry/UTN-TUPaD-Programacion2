from __future__ import annotations
from typing import TYPE_CHECKING

from food_store.entidades.Base import Base

if TYPE_CHECKING:
    from food_store.entidades.Producto import Producto


class DetallePedido(Base):
    """Línea de detalle de un pedido (composición)."""

    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        self.__producto: Producto = producto
        self.__cantidad: int = cantidad
        self.__subtotal: float = cantidad * producto.precio
       
    @property
    def producto(self) -> Producto:
        return self.__producto
    
    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        self.__cantidad = valor
        self.__subtotal = valor * self.__producto.precio
    
    def __str__(self) -> str:
        return (
            f"  {self.__producto.nombre} x{self.__cantidad} "
            f"| ${self.__producto.precio:.2f} c/u "
            f"| Subtotal: ${self.__subtotal:.2f}"
        )