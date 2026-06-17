from typing import List, Optional

from domain.entities.user import User
from domain.ports.user_repository import IUserRepository


class UserService:
    """
    Caso de uso: gestión de usuarios del sistema.

    Orquesta la creación y listado de usuarios a través del repositorio.
    """

    def __init__(self, user_repo: IUserRepository):
        self._repo = user_repo

    def create_user(self, nombre: str, email: str) -> Optional[dict]:
        """
        Crea un nuevo usuario.
        Devuelve el usuario creado o None si el email ya está registrado.
        """
        user = User(nombre=nombre, email=email)
        created = self._repo.create(user)
        return created.to_dict() if created else None

    def list_users(self) -> List[dict]:
        """Devuelve todos los usuarios registrados."""
        return [u.to_dict() for u in self._repo.find_all()]
