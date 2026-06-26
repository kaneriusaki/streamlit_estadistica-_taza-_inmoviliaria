from typing import List, Callable
import sqlite3
import pandas as pd

from domain.entities.property import Property
from domain.ports.property_repository import PropertyQueryRepository, MLDataRepository


class SQLitePropertyRepository(PropertyQueryRepository, MLDataRepository):
    """
    Adaptador de salida: implementación concreta de PropertyQueryRepository y MLDataRepository usando SQLite.
    Las dependencias de conexión a base de datos se inyectan a través de una factory.
    """

    def __init__(self, connection_factory: Callable[[], sqlite3.Connection]):
        self._connection_factory = connection_factory

    def count(self) -> int:
        conn = self._connection_factory()
        count = conn.execute("SELECT COUNT(*) FROM properties").fetchone()[0]
        conn.close()
        return count

    def save_all(self, df: pd.DataFrame) -> None:
        conn = self._connection_factory()
        conn.execute("DELETE FROM properties")
        
        # Copiar dataframe para no modificar el original
        df_to_save = df.copy()
        if "user_id" not in df_to_save.columns:
            df_to_save["user_id"] = 1
            
        # Filtrar solo columnas válidas del esquema para evitar errores de to_sql
        valid_cols = {
            "id", "user_id", "latitud", "longitud", "area_m2", "habitaciones",
            "banos", "distancia_centro_km", "antiguedad_anos", "tiene_piscina",
            "precio_lista", "precio_predicho", "diferencia", "es_oportunidad",
            "created_at", "updated_at"
        }
        cols_to_keep = [col for col in df_to_save.columns if col in valid_cols]
        df_to_save = df_to_save[cols_to_keep]
        
        # Usar "append" en lugar de "replace" para no eliminar el esquema, CHECKs, PKs y FKs definidos
        df_to_save.to_sql("properties", conn, if_exists="append", index=False)
        conn.commit()
        conn.close()

    def load_as_dataframe(self) -> pd.DataFrame:
        conn = self._connection_factory()
        df = pd.read_sql("SELECT * FROM properties", conn)
        conn.close()
        return df

    def find_all(self) -> List[Property]:
        conn = self._connection_factory()
        rows = conn.execute("SELECT * FROM properties").fetchall()
        conn.close()
        return [self._row_to_entity(dict(r)) for r in rows]

    def find_opportunities(self) -> List[Property]:
        conn = self._connection_factory()
        rows = conn.execute(
            "SELECT * FROM properties WHERE es_oportunidad = 1"
        ).fetchall()
        conn.close()
        return [self._row_to_entity(dict(r)) for r in rows]

    @staticmethod
    def _row_to_entity(row: dict) -> Property:
        return Property(
            id=row.get("id"),
            user_id=row.get("user_id"),
            latitud=row.get("latitud", 0.0),
            longitud=row.get("longitud", 0.0),
            area_m2=row.get("area_m2", 0.0),
            habitaciones=row.get("habitaciones", 0),
            banos=row.get("banos", 0),
            distancia_centro_km=row.get("distancia_centro_km", 0.0),
            antiguedad_anos=row.get("antiguedad_anos", 0.0),
            tiene_piscina=row.get("tiene_piscina", 0),
            precio_lista=row.get("precio_lista", 0.0),
            precio_predicho=row.get("precio_predicho", 0.0),
            diferencia=row.get("diferencia", 0.0),
            es_oportunidad=bool(row.get("es_oportunidad", False)),
            updated_at=row.get("updated_at"),
        )
