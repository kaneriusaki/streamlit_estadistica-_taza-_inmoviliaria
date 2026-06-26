import sqlite3
from typing import List, Optional, Callable

from domain.entities.user import User
from domain.ports.user_repository import UserRepository


class SQLiteUserRepository(UserRepository):
    """
    Adaptador de salida: implementación concreta de UserRepository usando SQLite.
    Las dependencias de conexión a base de datos se inyectan a través de una factory.
    """

    def __init__(self, connection_factory: Callable[[], sqlite3.Connection]):
        self._connection_factory = connection_factory

    def create(self, user: User) -> Optional[User]:
        conn = self._connection_factory()
        try:
            cursor = conn.execute(
                "INSERT INTO users (nombre, email) VALUES (?, ?)",
                (user.nombre, user.email),
            )
            conn.commit()
            user_id = cursor.lastrowid
            return User(
                id=user_id,
                nombre=user.nombre,
                email=user.email,
            )
        except sqlite3.IntegrityError:
            # Email duplicado
            return None
        finally:
            conn.close()

    def find_all(self) -> List[User]:
        conn = self._connection_factory()
        rows = conn.execute(
            "SELECT * FROM users ORDER BY created_at DESC"
        ).fetchall()
        conn.close()
        return [
            User(
                id=r["id"],
                nombre=r["nombre"],
                email=r["email"],
                created_at=r["created_at"],
            )
            for r in rows
        ]
