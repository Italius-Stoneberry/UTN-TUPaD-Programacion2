import sys
import os

# Aseguramos que Python encuentra el módulo food_store para las importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


try:
    from food_store.enums import Rol, FormaPago, Estado
    from food_store.servicios.usuario_servicio import UsuarioServicio
    from food_store.servicios.categoria_servicio import CategoriaServicio
    from food_store.servicios.producto_servicio import ProductoServicio
    from food_store.servicios.pedidos_servicio import PedidoServicio
    from food_store.excepciones import PrecioInvalidoError
except ModuleNotFoundError as e:
    print(f"Error de importación: {e},Asegúrate de ejecutar este archivo desde la raíz del proyecto (donde está la carpeta food_store).")
  
    sys.exit(1)

def ejecutar_pruebas():
    print("="*60)
    print("   INICIANDO PRUEBAS AUTOMÁTICAS DEL SISTEMA FOOD STORE")
    print("="*60 + "\n")

    try:
        
        print("[1] Inicializando servicios...")
        usr_srv = UsuarioServicio()
        cat_srv = CategoriaServicio()
        prod_srv = ProductoServicio()
        ped_srv = PedidoServicio()
        print(" ->  Servicios instanciados correctamente.\n")

        
        print("[2] Probando creación de usuarios...")
        usr_cliente = usr_srv.crear("Carlos", "Prueba", "carlos@test.com", "123456", "clave123", Rol.USUARIO)
        usr_admin = usr_srv.crear("Admin", "Prueba", "admin@test.com", "654321", "admin123", Rol.ADMIN)
        assert usr_cliente.mail == "carlos@test.com", "Fallo al validar el email del cliente creado."
        print(" ->  Usuarios creados con éxito en memoria.\n")

        
        print("[3] Probando creación de categorías y productos...")
        cat_hamburguesas = cat_srv.crear("Hamburguesas", "Hamburguesas caseras")
        prod_hamburguesa = prod_srv.crear("Hamburguesa Completa", 5000.0, "Carne, queso, tomate", 15, "url.jpg", True, cat_hamburguesas)
        
        assert prod_hamburguesa.stock == 15, "El stock inicial del producto no es correcto."
        print(" ->  Producto creado con un stock inicial de 15.\n")

        
        print("[4] Probando validaciones (evitar precios negativos):")
        try:
            prod_hamburguesa.precio = -1000.0
            print(" -> ERROR: El sistema permitió asignar un precio negativo.")
        except PrecioInvalidoError as e:
            print(f" ->  Excepción de dominio capturada correctamente -> {e}")
        except Exception as e:
            print(f" ->  Excepción capturada (Validación funcionó) -> {e}")
        print()

        
        print("[5] Creando pedido y verificando el descuento de stock...")
        pedido_1 = ped_srv.crear(usr_cliente, FormaPago.EFECTIVO)
        pedido_1.agregar_detalle(5, prod_hamburguesa) 
        pedido_1.calcular_total()
        
        
        ped_srv.registrar(pedido_1)
        
        assert prod_hamburguesa.stock == 10, f"Error en descuento de stock. Esperado 10, Actual: {prod_hamburguesa.stock}"
        assert pedido_1.total == 25000.0, "Error en el cálculo matemático del subtotal/total"
        print(f" ->  Pedido #{pedido_1.id} creado con éxito. Total calculado: ${pedido_1.total}")
        print(f" ->  El stock bajó correctamente de 15 a 10.\n")

        
        print("[6] Cancelando el pedido para probar devolución de stock (reintegro)...")
        ped_srv.cambiar_estado(pedido_1.id, Estado.CANCELADO)
        
        assert prod_hamburguesa.stock == 15, f"Error al devolver stock. Esperado 15, Actual: {prod_hamburguesa.stock}"
        print(f" ->  Pedido cancelado exitosamente. El stock volvió de 10 a 15.\n")

        print("="*60)
        print(" TODAS LAS PRUEBAS SE EJECUTARON CORRECTAMENTE")
        print("="*60)

    except AssertionError as ae:
        print(f"\n[!] ERROR EN LA PRUEBA (Fallo de Aserción): {ae}")
    except Exception as e:
        print(f"\n[!] ERROR INESPERADO: {e}")

if __name__ == '__main__':
    ejecutar_pruebas()
