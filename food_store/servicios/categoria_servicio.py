from food_store.entidades.Categoria import Categoria
from food_store.excepciones import (
    EntidadNoEncontradaError,
    DuplicadoError,
    OperacionNoPermitidaError,
)


class CategoriaServicio:
    """Servicio que gestiona la colección de categorías."""

    def __init__(self) -> None:
        self.__categorias: list[Categoria] = []
    
    def crear(self, nombre: str, descripcion: str) -> Categoria:
        self._validar_nombre_unico(nombre)
        categoria = Categoria(nombre, descripcion)
        self.__categorias.append(categoria)
        return categoria
    
    def _validar_nombre_unico(self, nombre: str) -> None:
        for c in self.__categorias:
            if not c.eliminado and c.nombre.lower() == nombre.strip().lower():
                raise DuplicadoError(f"Ya existe una categoría con el nombre '{nombre}'.")

    def buscar_por_id(self, id_categoria: int) -> Categoria:
        for c in self.__categorias:
            if c.id == id_categoria and not c.eliminado:
                return c
        raise EntidadNoEncontradaError(f"Categoría con id {id_categoria} no encontrada.")
    
    def eliminar(self, id_categoria: int, productos_activos: int) -> None:
        categoria = self.buscar_por_id(id_categoria)
        if productos_activos > 0:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar: la categoría tiene {productos_activos} producto(s) activo(s)."
            )
        categoria.eliminado = True
    
    def editar(self, id_categoria: int, nombre: str | None = None, descripcion: str | None = None) -> Categoria:
        categoria = self.buscar_por_id(id_categoria)
        if nombre is not None:
            if nombre.strip().lower() != categoria.nombre.lower():
                self._validar_nombre_unico(nombre)
            categoria.nombre = nombre
        if descripcion is not None:
            categoria.descripcion = descripcion
        return categoria

    def listar(self) -> list[Categoria]:
        return [c for c in self.__categorias if not c.eliminado]

    