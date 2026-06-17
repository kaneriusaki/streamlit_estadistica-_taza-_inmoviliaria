from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.user import User


class IUserRepository(ABC):
    """
    Puerto de salida: contrato abstracto para el acceso a datos de usuarios.
    """

    @abstractmethod
    def create(self, user: User) -> Optional[User]:
        """
        Crea un nuevo usuario. Devuelve el usuario con ID asignado,
        o None si el email ya existe.
        """
        ...

    @abstractmethod
    def find_all(self) -> List[User]:
        """Devuelve todos los usuarios registrados."""
        ...
