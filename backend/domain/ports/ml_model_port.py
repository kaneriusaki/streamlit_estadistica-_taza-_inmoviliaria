from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd


class MLPredictor(ABC):
    """
    Puerto de salida: Contrato abstracto para la inferencia, evaluación e información del modelo.
    Un predictor externo servido como API solo necesita implementar esta interfaz.
    """

    @abstractmethod
    def predict(self, params: dict) -> dict:
        """
        Predice el precio para los parámetros dados.
        Devuelve: { predicted_price, margin_of_error, lower_bound, upper_bound }
        """
        pass

    @abstractmethod
    def compute_undervalued(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Añade columnas precio_predicho, diferencia, es_oportunidad al DataFrame.
        Devuelve el DataFrame enriquecido.
        """
        pass

    @abstractmethod
    def get_feature_importance(self) -> Dict[str, float]:
        """Devuelve el impacto por unidad de cada característica."""
        pass

    @abstractmethod
    def get_metrics(self) -> Dict[str, float]:
        """Devuelve métricas de rendimiento del modelo: r2_score, mean_absolute_error."""
        pass


class MLTrainable(ABC):
    """
    Puerto de salida: Contrato abstracto para el entrenamiento de modelos de Machine Learning.
    """

    @abstractmethod
    def train(self, model: MLPredictor, df: pd.DataFrame) -> None:
        """Entrena el modelo predictor dado usando el DataFrame de propiedades."""
        pass
