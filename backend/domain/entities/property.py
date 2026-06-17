from dataclasses import dataclass
from typing import Optional

@dataclass
class Property:
    """
    Entidad de dominio que representa una propiedad inmobiliaria.
    No tiene dependencias de infraestructura.
    """
    id: Optional[int] = None
    user_id: Optional[int] = None
    latitud: float = 0.0
    longitud: float = 0.0
    area_m2: float = 0.0
    habitaciones: int = 0
    banos: int = 0
    distancia_centro_km: float = 0.0
    antiguedad_anos: float = 0.0
    tiene_piscina: int = 0
    precio_lista: float = 0.0
    precio_predicho: float = 0.0
    diferencia: float = 0.0
    es_oportunidad: bool = False
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "area_m2": self.area_m2,
            "habitaciones": self.habitaciones,
            "banos": self.banos,
            "distancia_centro_km": self.distancia_centro_km,
            "antiguedad_anos": self.antiguedad_anos,
            "tiene_piscina": self.tiene_piscina,
            "precio_lista": self.precio_lista,
            "precio_predicho": self.precio_predicho,
            "diferencia": self.diferencia,
            "es_oportunidad": self.es_oportunidad,
            "updated_at": self.updated_at,
        }
