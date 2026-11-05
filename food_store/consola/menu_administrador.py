from food_store.consola.menu import Menu
from food_store.consola import lectura
from food_store.enums import Estado, FormaPago, Rol
from food_store.excepciones import FoodStoreError


class MenuAdministrador(Menu):
    """Menú completo para el rol ADMIN."""

    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE – ADMINISTRADOR ({self._usuario.nombre} {self._usuario.apellido}) ===")
            print("1. Categorías")
            print("2. Productos")
            print("3. Usuarios")
            print("4. Pedidos")
            print("9. Cerrar sesión")
            print("0. Salir")
            opcion = input("Seleccione: ").strip()

            if opcion == "1":
                self._menu_categorias()
            elif opcion == "2":
                self._menu_productos()
            elif opcion == "3":
                self._menu_usuarios()
            elif opcion == "4":
                self._menu_pedidos()
            elif opcion == "9":
                return True
            elif opcion == "0":
                return False
            else:
                print("Opción no válida.")

    # ═══════════════════════ CATEGORÍAS ═══════════════════════════

    def _menu_categorias(self) -> None:
        while True:
            print("\n--- CATEGORÍAS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            opcion = input("Seleccione: ").strip()

            try:
                if opcion == "1":
                    self._listar_categorias()
                elif opcion == "2":
                    self._crear_categoria()
                elif opcion == "3":
                    self._editar_categoria()
                elif opcion == "4":
                    self._eliminar_categoria()
                elif opcion == "0":
                    return
                else:
                    print("Opción no válida.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Error de entrada: {e}")

    def _listar_categorias(self) -> None:
        categorias = self._cat_srv.listar()
        if not categorias:
            print("No hay categorías cargadas.")
            return
        for c in categorias:
            print(c)

    def _crear_categoria(self) -> None:
        nombre = lectura.leer_texto("Nombre: ")
        descripcion = lectura.leer_texto("Descripción: ")
        categoria = self._cat_srv.crear(nombre, descripcion)
        print(f"Categoría creada con id {categoria.id}.")

    def _editar_categoria(self) -> None:
        self._listar_categorias()
        id_cat = lectura.leer_entero("ID de la categoría a editar: ")
        cat = self._cat_srv.buscar_por_id(id_cat)
        print(f"Editando: {cat}")
        print("(Presione Enter para conservar el valor actual)")
        nombre = lectura.leer_texto(f"Nombre [{cat.nombre}]: ", permitir_vacio=True)
        descripcion = lectura.leer_texto(f"Descripción [{cat.descripcion}]: ", permitir_vacio=True)
        self._cat_srv.editar(id_cat, nombre, descripcion)
        print("Categoría actualizada.")

    def _eliminar_categoria(self) -> None:
        self._listar_categorias()
        id_cat = lectura.leer_entero("ID de la categoría a eliminar: ")
        self._cat_srv.buscar_por_id(id_cat)
        if not lectura.confirmar():
            print("Operación cancelada.")
            return
        productos_activos = self._prod_srv.contar_por_categoria(
            self._cat_srv.buscar_por_id(id_cat)
        )
        self._cat_srv.eliminar(id_cat, productos_activos)
        print("Categoría eliminada.")

    # ═══════════════════════ PRODUCTOS ════════════════════════════

    def _menu_productos(self) -> None:
        while True:
            print("\n--- PRODUCTOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            opcion = input("Seleccione: ").strip()

            try:
                if opcion == "1":
                    self._listar_productos()
                elif opcion == "2":
                    self._crear_producto()
                elif opcion == "3":
                    self._editar_producto()
                elif opcion == "4":
                    self._eliminar_producto()
                elif opcion == "0":
                    return
                else:
                    print("Opción no válida.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Error de entrada: {e}")

    def _listar_productos(self) -> None:
        productos = self._prod_srv.listar()
        if not productos:
            print("No hay productos cargados.")
            return
        for p in productos:
            print(p)

    def _crear_producto(self) -> None:
        nombre = lectura.leer_texto("Nombre: ")
        descripcion = lectura.leer_texto("Descripción: ")
        precio = lectura.leer_float("Precio: ")
        stock = lectura.leer_entero("Stock: ")
        imagen = lectura.leer_texto("Imagen (nombre archivo): ")
        disponible = lectura.leer_bool("Disponible (S/N): ")

        categorias = self._cat_srv.listar()
        if not categorias:
            print("Debe crear al menos una categoría primero.")
            return
        print("Categorías disponibles:")
        for c in categorias:
            print(f"  {c}")
        id_cat = lectura.leer_entero("ID de categoría: ")
        categoria = self._cat_srv.buscar_por_id(id_cat)

        producto = self._prod_srv.crear(nombre, precio, descripcion, stock, imagen, disponible, categoria)
        print(f"Producto creado con id {producto.id}.")

    def _editar_producto(self) -> None:
        self._listar_productos()
        id_prod = lectura.leer_entero("ID del producto a editar: ")
        prod = self._prod_srv.buscar_por_id(id_prod)
        print(f"Editando: {prod}")
        print("(Presione Enter para conservar el valor actual)")

        nombre = lectura.leer_texto(f"Nombre [{prod.nombre}]: ", permitir_vacio=True)
        precio = lectura.leer_float(f"Precio [{prod.precio}]: ", permitir_vacio=True)
        descripcion = lectura.leer_texto(f"Descripción [{prod.descripcion}]: ", permitir_vacio=True)
        stock = lectura.leer_entero(f"Stock [{prod.stock}]: ", permitir_vacio=True)
        imagen = lectura.leer_texto(f"Imagen [{prod.imagen}]: ", permitir_vacio=True)
        disponible = lectura.leer_bool(f"Disponible [{('S' if prod.disponible else 'N')}] (S/N): ", permitir_vacio=True)

        print(f"Categoría actual: {prod.categoria.nombre}")
        cambiar_cat = lectura.leer_bool("¿Cambiar categoría? (S/N): ")
        categoria = None
        if cambiar_cat:
            for c in self._cat_srv.listar():
                print(f"  {c}")
            id_cat = lectura.leer_entero("ID nueva categoría: ")
            categoria = self._cat_srv.buscar_por_id(id_cat)

        self._prod_srv.editar(id_prod, nombre, precio, descripcion, stock, imagen, disponible, categoria)
        print("Producto actualizado.")

    def _eliminar_producto(self) -> None:
        self._listar_productos()
        id_prod = lectura.leer_entero("ID del producto a eliminar: ")
        self._prod_srv.buscar_por_id(id_prod)
        if not lectura.confirmar():
            print("Operación cancelada.")
            return
        self._prod_srv.eliminar(id_prod)
        print("Producto eliminado.")

    # ═══════════════════════ USUARIOS ═════════════════════════════

    def _menu_usuarios(self) -> None:
        while True:
            print("\n--- USUARIOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            opcion = input("Seleccione: ").strip()

            try:
                if opcion == "1":
                    self._listar_usuarios()
                elif opcion == "2":
                    self._crear_usuario()
                elif opcion == "3":
                    self._editar_usuario()
                elif opcion == "4":
                    self._eliminar_usuario()
                elif opcion == "0":
                    return
                else:
                    print("Opción no válida.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Error de entrada: {e}")

    def _listar_usuarios(self) -> None:
        usuarios = self._usr_srv.listar()
        if not usuarios:
            print("No hay usuarios cargados.")
            return
        for u in usuarios:
            print(u)

    def _crear_usuario(self) -> None:
        nombre = lectura.leer_texto("Nombre: ")
        apellido = lectura.leer_texto("Apellido: ")
        mail = lectura.leer_texto("Mail: ")
        celular = lectura.leer_texto("Celular: ")
        contrasenia = lectura.leer_texto("Contraseña: ")
        print("Rol:")
        rol = lectura.leer_enum(Rol)
        usuario = self._usr_srv.crear(nombre, apellido, mail, celular, contrasenia, rol)
        print(f"Usuario creado con id {usuario.id}.")

    def _editar_usuario(self) -> None:
        self._listar_usuarios()
        id_usr = lectura.leer_entero("ID del usuario a editar: ")
        usr = self._usr_srv.buscar_por_id(id_usr)
        print(f"Editando: {usr}")
        print("(Presione Enter para conservar el valor actual)")

        nombre = lectura.leer_texto(f"Nombre [{usr.nombre}]: ", permitir_vacio=True)
        apellido = lectura.leer_texto(f"Apellido [{usr.apellido}]: ", permitir_vacio=True)
        mail = lectura.leer_texto(f"Mail [{usr.mail}]: ", permitir_vacio=True)
        celular = lectura.leer_texto(f"Celular [{usr.celular}]: ", permitir_vacio=True)
        contrasenia = lectura.leer_texto("Nueva contraseña (Enter = no cambiar): ", permitir_vacio=True)
        print("Rol (Enter = no cambiar):")
        rol = lectura.leer_enum(Rol, permitir_vacio=True)

        self._usr_srv.editar(id_usr, nombre, apellido, mail, celular, contrasenia, rol)
        print("Usuario actualizado.")

    def _eliminar_usuario(self) -> None:
        self._listar_usuarios()
        id_usr = lectura.leer_entero("ID del usuario a eliminar: ")
        self._usr_srv.buscar_por_id(id_usr)
        if not lectura.confirmar():
            print("Operación cancelada.")
            return
        self._usr_srv.eliminar(id_usr, self._usuario)
        print("Usuario eliminado.")

    # ═══════════════════════ PEDIDOS ══════════════════════════════

    def _menu_pedidos(self) -> None:
        while True:
            print("\n--- PEDIDOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Cambiar estado / forma de pago")
            print("4. Eliminar")
            print("5. Ver detalles de un pedido")
            print("0. Volver")
            opcion = input("Seleccione: ").strip()

            try:
                if opcion == "1":
                    self._listar_pedidos()
                elif opcion == "2":
                    self._crear_pedido()
                elif opcion == "3":
                    self._actualizar_pedido()
                elif opcion == "4":
                    self._eliminar_pedido()
                elif opcion == "5":
                    self._ver_detalles_pedido()
                elif opcion == "0":
                    return
                else:
                    print("Opción no válida.")
            except FoodStoreError as e:
                print(f"Error: {e}")
            except ValueError as e:
                print(f"Error de entrada: {e}")

    def _listar_pedidos(self) -> None:
        pedidos = self._ped_srv.listar()
        if not pedidos:
            print("No hay pedidos cargados.")
            return
        for p in pedidos:
            print(p)

    def _crear_pedido(self) -> None:
        print("Usuarios disponibles:")
        self._listar_usuarios()
        id_usr = lectura.leer_entero("ID del usuario para el pedido: ")
        usuario = self._usr_srv.buscar_por_id(id_usr)

        print("Forma de pago:")
        forma_pago = lectura.leer_enum(FormaPago)

        pedido = self._ped_srv.crear(usuario, forma_pago)

        print("\n-- Agregar productos al pedido (ingrese 0 para terminar) --")
        productos = self._prod_srv.listar()
        if not productos:
            print("No hay productos disponibles.")
            return
        for p in productos:
            print(f"  {p}")

        while True:
            id_prod = lectura.leer_entero("\nID del producto (0 para finalizar): ")
            if id_prod == 0:
                break
            producto = self._prod_srv.buscar_por_id(id_prod)
            cantidad = lectura.leer_entero("Cantidad: ")
            try:
                pedido.agregar_detalle(cantidad, producto)
                print(f"  Agregado: {producto.nombre} x{cantidad}")
            except FoodStoreError as e:
                print(f"Error: {e}")
                print("Se canceló la creación del pedido.")
                return

        if not pedido.detalles:
            print("El pedido debe tener al menos un detalle. Creación cancelada.")
            return

        pedido.calcular_total()
        self._ped_srv.registrar(pedido)
        print(f"Pedido creado con id {pedido.id}. Total: ${pedido.total:.2f}")

    def _actualizar_pedido(self) -> None:
        self._listar_pedidos()
        id_ped = lectura.leer_entero("ID del pedido: ")
        pedido = self._ped_srv.buscar_por_id(id_ped)
        print(f"Pedido actual: {pedido}")

        print("\n¿Qué desea cambiar?")
        print("1. Estado")
        print("2. Forma de pago")
        print("3. Ambos")
        sub = input("Seleccione: ").strip()

        if sub in ("1", "3"):
            print(f"Estado actual: {pedido.estado.value}")
            print("Nuevo estado:")
            nuevo_estado = lectura.leer_enum(Estado)
            self._ped_srv.cambiar_estado(id_ped, nuevo_estado)
            print(f"Estado actualizado a {nuevo_estado.value}.")

        if sub in ("2", "3"):
            print(f"Forma de pago actual: {pedido.forma_pago.value}")
            print("Nueva forma de pago:")
            nueva_fp = lectura.leer_enum(FormaPago)
            self._ped_srv.cambiar_forma_pago(id_ped, nueva_fp)
            print(f"Forma de pago actualizada a {nueva_fp.value}.")

    def _eliminar_pedido(self) -> None:
        self._listar_pedidos()
        id_ped = lectura.leer_entero("ID del pedido a eliminar: ")
        self._ped_srv.buscar_por_id(id_ped)
        if not lectura.confirmar():
            print("Operación cancelada.")
            return
        self._ped_srv.eliminar(id_ped)
        print("Pedido eliminado.")

    def _ver_detalles_pedido(self) -> None:
        self._listar_pedidos()
        id_ped = lectura.leer_entero("ID del pedido: ")
        pedido = self._ped_srv.buscar_por_id(id_ped)
        print(f"\n{pedido}")
        if not pedido.detalles:
            print("  (sin detalles)")
        for d in pedido.detalles:
            print(d)
        print(f"  TOTAL: ${pedido.total:.2f}")