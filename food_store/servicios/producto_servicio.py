from food_store.entidades.Producto import Producto
from food_store.entidades.Categoria import Categoria
from food_store.excepciones import EntidadNoEncontradaError
""" Gran parte de aca lo hice con ia por que se escaba un poco de mis conocimientos o de conocimientos dados ,
 por ahi por eso esta un poco mas ordenado por el hecho de que teniamos que ser ordenando el codigo a medida que fuimos pediendo ayuda """

class ProductoServicio:
    """Servicio que gestiona la colección de productos."""

    def __init__(self) -> None:
        self.__productos: list[Producto] = []

    # ── Alta ─────────────────────────────────────────────────────

    def crear(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        stock: int,
        imagen: str,
        disponible: bool,
        categoria: Categoria,
    ) -> Producto:
        producto = Producto(nombre, precio, descripcion, stock, imagen, disponible, categoria)
        self.__productos.append(producto)
        return producto

    # ── Baja lógica ──────────────────────────────────────────────

    def eliminar(self, id_producto: int) -> None:
        producto = self.buscar_por_id(id_producto)
        producto.eliminado = True

    # ── Modificación ─────────────────────────────────────────────

    def editar(
        self,
        id_producto: int,
        nombre: str | None = None,
        precio: float | None = None,
        descripcion: str | None = None,
        stock: int | None = None,
        imagen: str | None = None,
        disponible: bool | None = None,
        categoria: Categoria | None = None,
    ) -> Producto:
        producto = self.buscar_por_id(id_producto)
        if nombre is not None:
            producto.nombre = nombre
        if precio is not None:
            producto.precio = precio
        if descripcion is not None:
            producto.descripcion = descripcion
        if stock is not None:
            producto.stock = stock
        if imagen is not None:
            producto.imagen = imagen
        if disponible is not None:
            producto.disponible = disponible
        if categoria is not None:
            producto.categoria = categoria
        return producto

    # ── Consultas ────────────────────────────────────────────────

    def listar(self) -> list[Producto]:
        return [p for p in self.__productos if not p.eliminado]

    def listar_disponibles(self) -> list[Producto]:
        """Vista cliente: solo disponibles y con stock."""
        return [
            p for p in self.__productos
            if not p.eliminado and p.disponible and p.stock > 0
        ]

    def buscar_por_id(self, id_producto: int) -> Producto:
        for p in self.__productos:
            if p.id == id_producto and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"Producto con id {id_producto} no encontrado.")

    def contar_por_categoria(self, categoria: Categoria) -> int:
        """Cuenta productos activos de una categoría."""
        return sum(
            1 for p in self.__productos
            if not p.eliminado and p.categoria == categoria
        )

    