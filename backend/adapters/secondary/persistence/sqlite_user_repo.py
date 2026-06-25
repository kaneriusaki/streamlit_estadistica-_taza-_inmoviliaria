import sqlite3
from typing import List, Optional

from domain.entities.user import User
from domain.ports.user_repository import UserRepository
from adapters.secondary.persistence.database import get_connection


class SQLiteUserRepository(UserRepository):
    """
    Adaptador de salida: implementación concreta de UserRepository usando SQLite.
    """

    def create(self, user: User) -> Optional[User]:
        conn = get_connection()
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
        conn = get_connection()
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
