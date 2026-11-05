from enum import Enum


def leer_texto(mensaje: str, permitir_vacio: bool = False) -> str | None:
    """Lee texto. Si permitir_vacio=True y el usuario apreta Enter, devuelve None."""
    valor = input(mensaje).strip()
    if not valor:
        if permitir_vacio:
            return None
        raise ValueError("El campo no puede estar vacío.")
    return valor


def leer_entero(mensaje: str, permitir_vacio: bool = False) -> int | None:
    valor = input(mensaje).strip()
    if not valor:
        if permitir_vacio:
            return None
        raise ValueError("Debe ingresar un número entero.")
    return int(valor)


def leer_float(mensaje: str, permitir_vacio: bool = False) -> float | None:
    valor = input(mensaje).strip()
    if not valor:
        if permitir_vacio:
            return None
        raise ValueError("Debe ingresar un número.")
    return float(valor)


def leer_bool(mensaje: str, permitir_vacio: bool = False) -> bool | None:
    valor = input(mensaje).strip().upper()
    if not valor:
        if permitir_vacio:
            return None
        raise ValueError("Debe ingresar S o N.")
    if valor not in ("S", "N"):
        raise ValueError("Debe ingresar S o N.")
    return valor == "S"


def leer_enum(enum_class: type[Enum], permitir_vacio: bool = False) -> Enum | None:
    """Muestra las opciones numeradas de un Enum y devuelve la seleccionada."""
    opciones = list(enum_class)
    for i, opcion in enumerate(opciones, 1):
        print(f"  {i}. {opcion.value}")
    valor = input("Seleccione: ").strip()
    if not valor:
        if permitir_vacio:
            return None
        raise ValueError("Debe seleccionar una opción.")
    indice = int(valor) - 1
    if indice < 0 or indice >= len(opciones):
        raise ValueError("Opción fuera de rango.")
    return opciones[indice]


def confirmar() -> bool:
    """Pide confirmación S/N."""
    return leer_bool("¿Confirmar? (S/N): ") or False