from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """
    Entidad de dominio que representa un usuario del sistema.
    """
    nombre: str
    email: str
    id: Optional[int] = None
    created_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "created_at": self.created_at,
        }
