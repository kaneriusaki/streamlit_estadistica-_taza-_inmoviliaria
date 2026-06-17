from dataclasses import dataclass
from typing import Optional

@dataclass
class Prediction:
    """Entidad de dominio que representa una predicción de precio realizada por el sistema."""
    id: Optional[int] = None
    user_id: Optional[int] = None
    property_id: Optional[int] = None
    area_m2: float = 0.0
    habitaciones: int = 0
    banos: int = 0
    distancia_centro_km: float = 0.0
    antiguedad_anos: float = 0.0
    tiene_piscina: int = 0
    predicted_price: float = 0.0
    margin_of_error: float = 0.0
    user_name: Optional[str] = None
    created_at: Optional[str] = None

    @property
    def lower_bound(self) -> float:
        return self.predicted_price - self.margin_of_error

    @property
    def upper_bound(self) -> float:
        return self.predicted_price + self.margin_of_error

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "property_id": self.property_id,
            "user_name": self.user_name,
            "area_m2": self.area_m2,
            "habitaciones": self.habitaciones,
            "banos": self.banos,
            "distancia_centro_km": self.distancia_centro_km,
            "antiguedad_anos": self.antiguedad_anos,
            "tiene_piscina": self.tiene_piscina,
            "predicted_price": self.predicted_price,
            "margin_of_error": self.margin_of_error,
            "lower_bound": self.lower_bound,
            "upper_bound": self.upper_bound,
            "created_at": self.created_at,
        }
