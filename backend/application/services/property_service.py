from typing import List

from domain.entities.property import Property
from domain.ports.property_repository import PropertyRepository
from domain.ports.ml_model_port import MLModel


class PropertyService:
    """
    Caso de uso: consulta de propiedades del mercado.
    Responsabilidad única: exponer propiedades y oportunidades.
    La inicialización de datos y entrenamiento del modelo es
    responsabilidad de DataInitializer.
    """

    def __init__(
        self,
        property_repo: PropertyRepository,
        ml_model: MLModel,
    ):
        self._repo = property_repo
        self._model = ml_model

    def get_all_properties(self) -> List[dict]:
        return [p.to_dict() for p in self._repo.find_all()]

    def get_opportunities(self) -> List[dict]:
        return [p.to_dict() for p in self._repo.find_opportunities()]

    def get_stats_insight(self) -> dict:
        return {
            "feature_importance": self._model.get_feature_importance(),
            "model_metrics": self._model.get_metrics(),
        }
