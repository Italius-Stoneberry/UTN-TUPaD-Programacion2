#linea para probar desde el ide
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from food_store.enums import Rol, FormaPago
from food_store.excepciones import CredencialesInvalidasError
from food_store.entidades.Usuario import Usuario
from food_store.consola.menu import Menu
from food_store.consola.menu_administrador import MenuAdministrador
from food_store.consola.menu_cliente import MenuCliente
from food_store.servicios import (
    CategoriaServicio,
    ProductoServicio,
    UsuarioServicio,
    PedidoServicio,
)


def crear_menu(
    usuario: Usuario,
    cat_srv: CategoriaServicio,
    prod_srv: ProductoServicio,
    usr_srv: UsuarioServicio,
    ped_srv: PedidoServicio,
) -> Menu:
    """Factory: devuelve el menú según el rol."""
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(usuario, cat_srv, prod_srv, usr_srv, ped_srv)
    return MenuCliente(usuario, cat_srv, prod_srv, usr_srv, ped_srv)


def cargar_datos_ejemplo(cat_srv, prod_srv, usr_srv, ped_srv) -> None:
    """Carga datos iniciales para probar."""
    cat1 = cat_srv.crear("Hamburguesas", "Variedad de hamburguesas artesanales")
    cat2 = cat_srv.crear("Bebidas", "Gaseosas, jugos y agua")
    cat3 = cat_srv.crear("Postres", "Dulces y helados")

    prod_srv.crear("Burger Clásica", 3500.0, "Con cheddar y bacon", 20, "burger_clasica.png", True, cat1)
    prod_srv.crear("Burger Veggie", 3200.0, "Con medallón de lentejas", 15, "burger_veggie.png", True, cat1)
    prod_srv.crear("Coca-Cola 500ml", 1500.0, "Gaseosa", 50, "coca.png", True, cat2)
    prod_srv.crear("Agua Mineral 500ml", 1000.0, "Sin gas", 40, "agua.png", True, cat2)
    prod_srv.crear("Brownie", 2000.0, "Brownie con dulce de leche", 10, "brownie.png", True, cat3)

    usr_srv.crear("Juan", "Gómez", "juan@mail.com", "2614567890", "juan123", Rol.USUARIO)


def inicio_sesion(usr_srv: UsuarioServicio) -> Usuario | None:
    """Login con 3 intentos."""
    MAX_INTENTOS = 3
    for intento in range(1, MAX_INTENTOS + 1):
        print("\n=== FOOD STORE – INICIO DE SESIÓN ===")
        mail = input("Mail: ").strip()
        contrasenia = input("Contraseña: ").strip()
        try:
            usuario = usr_srv.autenticar(mail, contrasenia)
            print(f"\nBienvenido/a, {usuario.nombre} {usuario.apellido} [{usuario.rol.value}]")
            return usuario
        except CredencialesInvalidasError:
            restantes = MAX_INTENTOS - intento
            if restantes > 0:
                print(f"Mail o contraseña incorrectos. Intentos restantes: {restantes}")
            else:
                print("Mail o contraseña incorrectos. Se agotaron los intentos.")
    return None


def main() -> None:
    cat_srv = CategoriaServicio()
    prod_srv = ProductoServicio()
    usr_srv = UsuarioServicio()
    ped_srv = PedidoServicio()

    # Admin inicial
    usr_srv.crear("Ana", "Pérez", "admin@foodstore.com", "2611234567", "admin123", Rol.ADMIN)

    # Datos de ejemplo
    cargar_datos_ejemplo(cat_srv, prod_srv, usr_srv, ped_srv)

    print("╔══════════════════════════════════════╗")
    print("║     FOOD STORE – Gestión de Pedidos  ║")
    print("╚══════════════════════════════════════╝")

    while True:
        usuario = inicio_sesion(usr_srv)
        if usuario is None:
            print("\nPrograma finalizado por intentos agotados.")
            sys.exit(0)

        menu = crear_menu(usuario, cat_srv, prod_srv, usr_srv, ped_srv)
        cerro_sesion = menu.mostrar()

        if cerro_sesion:
            print("\nSesión cerrada. Volviendo al inicio de sesión...")
            continue
        else:
            print("\n¡Hasta luego!")
            sys.exit(0)


if __name__ == "__main__":
    main()