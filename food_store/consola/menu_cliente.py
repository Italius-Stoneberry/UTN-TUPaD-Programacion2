from food_store.consola.menu import Menu
from food_store.consola import lectura
from food_store.excepciones import FoodStoreError


class MenuCliente(Menu):
    """Menú de solo consulta para el rol USUARIO."""

    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE – CLIENTE ({self._usuario.nombre} {self._usuario.apellido}) ===")
            print("1. Ver categorías")
            print("2. Ver productos disponibles")
            print("3. Mis pedidos")
            print("4. Mis datos")
            print("9. Cerrar sesión")
            print("0. Salir")
            opcion = input("Seleccione: ").strip()

            try:
                if opcion == "1":
                    self._ver_categorias()
                elif opcion == "2":
                    self._ver_productos()
                elif opcion == "3":
                    self._mis_pedidos()
                elif opcion == "4":
                    self._mis_datos()
                elif opcion == "9":
                    return True   # cerrar sesión
                elif opcion == "0":
                    return False  # salir
                else:
                    print("Opción no válida.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Error de entrada: {e}")

    # ── Categorías ───────────────────────────────────────────────

    def _ver_categorias(self) -> None:
        categorias = self._cat_srv.listar()
        if not categorias:
            print("No hay categorías cargadas.")
            return
        for c in categorias:
            print(c)

    # ── Productos (solo disponibles con stock) ───────────────────

    def _ver_productos(self) -> None:
        productos = self._prod_srv.listar_disponibles()
        if not productos:
            print("No hay productos disponibles.")
            return
        for p in productos:
            print(p)

    # ── Mis pedidos ──────────────────────────────────────────────

    def _mis_pedidos(self) -> None:
        pedidos = self._ped_srv.listar_por_usuario(self._usuario)
        if not pedidos:
            print("No tiene pedidos registrados.")
            return
        for p in pedidos:
            print(p)

        ver = lectura.leer_bool("\n¿Desea ver los detalles de un pedido? (S/N): ")
        if ver:
            id_ped = lectura.leer_entero("ID del pedido: ")
            pedido = self._ped_srv.buscar_por_id_y_usuario(id_ped, self._usuario)
            print(f"\n{pedido}")
            for d in pedido.detalles:
                print(d)
            print(f"  TOTAL: ${pedido.total:.2f}")

    # ── Mis datos ────────────────────────────────────────────────

    def _mis_datos(self) -> None:
        u = self._usuario
        print(f"  Nombre:   {u.nombre}")
        print(f"  Apellido: {u.apellido}")
        print(f"  Mail:     {u.mail}")
        print(f"  Celular:  {u.celular}")
        print(f"  Rol:      {u.rol.value}")