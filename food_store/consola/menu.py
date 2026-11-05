from abc import ABC, abstractmethod

from food_store.entidades.Usuario import Usuario
from food_store.servicios.categoria_servicio import CategoriaServicio
from food_store.servicios.producto_servicio import ProductoServicio
from food_store.servicios.usuario_servicio import UsuarioServicio
from food_store.servicios.pedidos_servicio import PedidoServicio


class Menu(ABC):
    """Clase abstracta del menú. Cada rol tiene su subclase."""

    def __init__(
        self,
        usuario: Usuario,
        categoria_servicio: CategoriaServicio,
        producto_servicio: ProductoServicio,
        usuario_servicio: UsuarioServicio,
        pedidos_servicio: PedidoServicio,
    ) -> None:
        self._usuario = usuario
        self._cat_srv = categoria_servicio
        self._prod_srv = producto_servicio
        self._usr_srv = usuario_servicio
        self._ped_srv = pedidos_servicio

    @abstractmethod
    def mostrar(self) -> bool:
        """Muestra el menú y procesa opciones.
        Retorna True si se cerró sesión, False si se quiere salir del programa."""
        pass