from typing import List, Optional

from domain.entities.prediction import Prediction
from domain.ports.prediction_repository import IPredictionRepository
from infrastructure.persistence.database import get_connection


class SQLitePredictionRepository(IPredictionRepository):
    """
    Adaptador de salida: implementación concreta de IPredictionRepository usando SQLite.
    """

    def save(self, prediction: Prediction) -> None:
        conn = get_connection()
        conn.execute(
            """
            INSERT INTO predictions (
                user_id, property_id, area_m2, habitaciones, banos,
                distancia_centro_km, antiguedad_anos, tiene_piscina,
                predicted_price, margin_of_error
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                prediction.user_id,
                prediction.property_id,
                prediction.area_m2,
                prediction.habitaciones,
                prediction.banos,
                prediction.distancia_centro_km,
                prediction.antiguedad_anos,
                prediction.tiene_piscina,
                prediction.predicted_price,
                prediction.margin_of_error,
            ),
        )
        conn.commit()
        conn.close()

    def find_all(self, user_id: Optional[int] = None) -> List[Prediction]:
        conn = get_connection()
        if user_id:
            rows = conn.execute(
                """
                SELECT p.*, u.nombre as user_name
                FROM predictions p
                LEFT JOIN users u ON p.user_id = u.id
                WHERE p.user_id = ?
                ORDER BY p.created_at DESC
                """,
                (user_id,),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT p.*, u.nombre as user_name
                FROM predictions p
                LEFT JOIN users u ON p.user_id = u.id
                ORDER BY p.created_at DESC
                """
            ).fetchall()
        conn.close()

        return [
            Prediction(
                id=r["id"],
                user_id=r["user_id"],
                property_id=r["property_id"],
                user_name=r["user_name"],
                area_m2=r["area_m2"],
                habitaciones=r["habitaciones"],
                banos=r["banos"],
                distancia_centro_km=r["distancia_centro_km"],
                antiguedad_anos=r["antiguedad_anos"],
                tiene_piscina=r["tiene_piscina"],
                predicted_price=r["predicted_price"],
                margin_of_error=r["margin_of_error"],
                created_at=r["created_at"],
            )
            for r in rows
        ]
