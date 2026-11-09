from abc import ABC, abstractmethod
from datetime import datetime

class Base(ABC):
    """"Clase base abstracta para todas las entidades."""

    _id_counter: int = 0

    def __init__(self) -> None:
        Base._id_counter += 1
        self.__id :int= Base._id_counter
        self.__creado_en: datetime = datetime.now()
        self.__eliminado: bool = False        
    
    @property
    def id(self) -> int:
        return self.__id
    @property
    def eliminado(self) -> bool:
        return self.__eliminado
    @eliminado.setter
    def eliminado(self,valor:bool) -> None:
        self.__eliminado = valor
    @property
    def creado_en(self) -> datetime:
        return self.__creado_en
    
    #lineas de eq y hash
    
    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro,Base):
            return False
        return self.__id == otro.__id
    def __hash__(self) -> int:
        return hash(self.__id)
    