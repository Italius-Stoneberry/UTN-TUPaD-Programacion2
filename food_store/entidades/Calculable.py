from abc import ABC, abstractmethod


class Calculable(ABC):
    """Interfaz que obliga a implementar calcular_total."""

    @abstractmethod
    def calcular_total(self) -> None:
        pass