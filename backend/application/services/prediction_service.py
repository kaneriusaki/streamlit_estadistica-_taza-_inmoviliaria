from typing import List, Optional

from domain.entities.prediction import Prediction
from domain.ports.prediction_repository import PredictionRepository
from domain.ports.ml_model_port import MLPredictor


class PredictionService:
    """
    Caso de uso: predicción de precio y gestión del historial.

    Orquesta la predicción usando el modelo ML y la persistencia
    del resultado en el repositorio.
    """

    def __init__(
        self,
        prediction_repo: PredictionRepository,
        ml_model: MLPredictor,
    ):
        self._repo = prediction_repo
        self._model = ml_model

    def predict(self, params: dict) -> dict:
        """
        Predice el precio para los parámetros dados.
        No persiste el resultado.
        """
        return self._model.predict(params)

    def predict_and_save(self, params: dict, user_id: Optional[int] = None, property_id: Optional[int] = None) -> dict:
        """
        Predice el precio y guarda la predicción en el historial.
        Devuelve el resultado de la predicción.
        """
        result = self._model.predict(params)

        prediction = Prediction(
            user_id=user_id,
            property_id=property_id,
            area_m2=params["area_m2"],
            habitaciones=params["habitaciones"],
            banos=params["banos"],
            distancia_centro_km=params["distancia_centro_km"],
            antiguedad_anos=params["antiguedad_anos"],
            tiene_piscina=params["tiene_piscina"],
            predicted_price=result["predicted_price"],
            margin_of_error=result["margin_of_error"],
        )
        self._repo.save(prediction)

        return result

    def get_history(self, user_id: Optional[int] = None) -> List[dict]:
        """
        Devuelve el historial de predicciones.
        Opcionalmente filtrado por usuario.
        """
        predictions = self._repo.find_all(user_id=user_id)
        return [p.to_dict() for p in predictions]
