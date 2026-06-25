from typing import List, Optional

from domain.entities.user import User
from domain.ports.user_repository import UserRepository


from domain.exceptions import UserAlreadyExistsError


class UserService:
    """
    Caso de uso: gestión de usuarios del sistema.

    Orquesta la creación y listado de usuarios a través del repositorio.
    """

    def __init__(self, user_repo: UserRepository):
        self._repo = user_repo

    def create_user(self, nombre: str, email: str) -> dict:
        """
        Crea un nuevo usuario.
        Devuelve el usuario creado o lanza UserAlreadyExistsError si el email ya está registrado.
        """
        user = User(nombre=nombre, email=email)
        created = self._repo.create(user)
        if created is None:
            raise UserAlreadyExistsError(f"El email '{email}' ya está registrado.")
        return created.to_dict()

    def list_users(self) -> List[dict]:
        """Devuelve todos los usuarios registrados."""
        return [u.to_dict() for u in self._repo.find_all()]
