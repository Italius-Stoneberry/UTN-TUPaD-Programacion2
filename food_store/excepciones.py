class FoodStoreError(Exception):
    """Excepción base del sistema Food Store."""
    pass


class EntidadNoEncontradaError(FoodStoreError):
    """Se lanza cuando un id no existe o la entidad está eliminada."""
    pass


class DatoInvalidoError(FoodStoreError):
    """Se lanza cuando un dato tiene texto vacío o formato incorrecto."""
    pass


class PrecioInvalidoError(DatoInvalidoError):
    """Se lanza cuando el precio es negativo."""
    pass


class StockInsuficienteError(FoodStoreError):
    """Se lanza cuando la cantidad pedida supera el stock disponible."""
    pass


class DuplicadoError(FoodStoreError):
    """Se lanza cuando un mail o nombre de categoría ya existe."""
    pass


class OperacionNoPermitidaError(FoodStoreError):
    """Se lanza ante transiciones de estado inválidas u operaciones prohibidas."""
    pass


class CredencialesInvalidasError(FoodStoreError):
    """Se lanza cuando el mail o la contraseña son incorrectos, o el usuario está eliminado."""
    pass
