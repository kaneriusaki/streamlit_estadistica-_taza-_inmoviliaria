import sqlite3
from typing import Callable


class DataSeeder:
    """
    Responsabilidad única: Sembrar datos iniciales requeridos en la base de datos.
    Permite independizar el esquema DB de la inicialización de datos de prueba/negocio.
    """

    def __init__(self, connection_factory: Callable[[], sqlite3.Connection]):
        self._connection_factory = connection_factory

    def seed(self) -> None:
        """
        Inserta un usuario por defecto si la tabla 'users' está vacía.
        Garantiza que no fallen las foreign keys por falta de usuarios.
        """
        conn = self._connection_factory()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO users (id, nombre, email) VALUES (?, ?, ?)",
                    (1, "Test", "test@test.com")
                )
                conn.commit()
        finally:
            conn.close()
