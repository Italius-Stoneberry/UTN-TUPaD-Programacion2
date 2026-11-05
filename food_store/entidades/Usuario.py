from food_store.entidades.Base import Base
from food_store.enums import Rol
from food_store.excepciones import DatoInvalidoError


class Usuario(Base):
    """Representa un usuario del sistema."""

    def __init__(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.__contrasenia: str = contrasenia
        self.__rol: Rol = rol

    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El nombre del producto no puede estar vacío.")
        self.__nombre = valor.strip()
    
    @property
    def apellido(self) -> str:
        return self.__apellido
    
    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El apellido del producto no puede estar vacío.")
        self.__apellido = valor.strip()

    @property
    def mail(self) -> str:
        return self.__mail
    
    @mail.setter
    def mail(self, valor: str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El mail del producto no puede estar vacío.")
        self.__mail = valor.strip()

    @property
    def rol(self) -> str:
        return self.__rol
    
    @rol.setter
    def rol(self, valor: str) -> None:
        self.__rol = valor


    '''como contraseña no deberia tener ni setter ni getter, le vamos a dar 2 funciones para setear la contrasenia y cambiarla'''
    def verificar_contrasenia(self, contrasenia: str) -> bool:
        return self.__contrasenia == contrasenia

    def set_contrasenia(self, nueva: str) -> None:
        self.__contrasenia = nueva
    
    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.nombre} {self.apellido} | "
            f"{self.mail} | {self.celular} | {self.rol.value}"
        )