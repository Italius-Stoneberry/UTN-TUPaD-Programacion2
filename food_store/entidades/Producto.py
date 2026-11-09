from __future__ import annotations
from typing import TYPE_CHECKING

from food_store.entidades.Base import Base
from food_store.excepciones import DatoInvalidoError, PrecioInvalidoError

if TYPE_CHECKING:
    from food_store.entidades.Categoria import Categoria


class Producto(Base):
    """Representa un producto del catálogo."""

    def __init__(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        stock: int,
        imagen: str,
        disponible: bool,
        categoria: Categoria,
    ) -> None:
    # esto es igual pero ordenado mas bonito por que por ahi en una sola linea queda algo confuso


        super().__init__()
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        self.__categoria: Categoria = categoria
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El nombre del producto no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self.__precio
    
    @precio.setter
    def precio(self, valor: float) -> None:
        if valor <0:
            raise PrecioInvalidoError("El precio del producto no puede ser  negativo.")
        self.__precio = valor

    @property
    def descripcion(self) -> str:
        return self.__descripcion
    
    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("La descripcion del producto no puede estar vacío.")
        self.__descripcion = valor.strip()

    @property
    def stock(self) -> int:
        return self.__stock
    
    @stock.setter
    def stock(self, valor: int) -> None:
        if valor <0:
            raise DatoInvalidoError("El stock del producto no puede ser  negativo.")
        self.__stock = valor

    @property
    def imagen(self) -> str:
        return self.__imagen
    
    @imagen.setter
    def imagen(self, valor: str) -> None:
        self.__imagen = valor

    @property
    def disponible(self) -> str:
        return self.__disponible
    
    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self.__disponible = valor
    
    @property
    def categoria(self) -> Categoria:
        return self.__categoria

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        self.__categoria = valor
    

    def __str__(self) -> str:
        estado = "Disponible" if self.__disponible else "No disponible"
        return (
            f"[{self.id}] {self.__nombre} | ${self.__precio:.2f} | "
            f"Stock: {self.__stock} | {estado} | Cat: {self.__categoria.nombre}")

    
    
    
    
    