from food_store.entidades.Usuario import Usuario
from food_store.enums import Rol
from food_store.excepciones import (
    EntidadNoEncontradaError,
    DuplicadoError,
    CredencialesInvalidasError,
    OperacionNoPermitidaError,
)


class UsuarioServicio:
    """Servicio que gestiona la colección de usuarios."""

    def __init__(self) -> None:
        self.__usuarios: list[Usuario] = []

    # ── Alta ─────────────────────────────────────────────────────

    def crear(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> Usuario:
        self._validar_mail_unico(mail)
        usuario = Usuario(nombre, apellido, mail, celular, contrasenia, rol)
        self.__usuarios.append(usuario)
        return usuario

    # ── Baja lógica ──────────────────────────────────────────────

    def eliminar(self, id_usuario: int, usuario_sesion: Usuario) -> None:
        usuario = self.buscar_por_id(id_usuario)
        if usuario == usuario_sesion:
            raise OperacionNoPermitidaError(
                "No puede eliminarse a sí mismo mientras tiene la sesión iniciada."
            )
        usuario.eliminado = True

    # ── Modificación ─────────────────────────────────────────────

    def editar(
        self,
        id_usuario: int,
        nombre: str | None = None,
        apellido: str | None = None,
        mail: str | None = None,
        celular: str | None = None,
        contrasenia: str | None = None,
        rol: Rol | None = None,
    ) -> Usuario:
        usuario = self.buscar_por_id(id_usuario)
        if nombre is not None:
            usuario.nombre = nombre
        if apellido is not None:
            usuario.apellido = apellido
        if mail is not None:
            if mail.strip().lower() != usuario.mail.lower():
                self._validar_mail_unico(mail)
            usuario.mail = mail
        if celular is not None:
            usuario.celular = celular
        if contrasenia is not None:
            usuario.set_contrasenia(contrasenia)
        if rol is not None:
            usuario.rol = rol
        return usuario

    # ── Consultas ────────────────────────────────────────────────

    def listar(self) -> list[Usuario]:
        return [u for u in self.__usuarios if not u.eliminado]

    def buscar_por_id(self, id_usuario: int) -> Usuario:
        for u in self.__usuarios:
            if u.id == id_usuario and not u.eliminado:
                return u
        raise EntidadNoEncontradaError(f"Usuario con id {id_usuario} no encontrado.")

    # ── Autenticación ────────────────────────────────────────────

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        for u in self.__usuarios:
            if u.mail.lower() == mail.strip().lower():
                if u.eliminado or not u.verificar_contrasenia(contrasenia):
                    raise CredencialesInvalidasError("Mail o contraseña incorrectos.")
                return u
        raise CredencialesInvalidasError("Mail o contraseña incorrectos.")

    # ── Validaciones internas ────────────────────────────────────

    def _validar_mail_unico(self, mail: str) -> None:
        for u in self.__usuarios:
            if not u.eliminado and u.mail.lower() == mail.strip().lower():
                raise DuplicadoError(f"Ya existe un usuario con el mail '{mail}'.")