from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd


class MLModel(ABC):
    """
    Puerto de salida: contrato abstracto para el modelo de Machine Learning.
    El dominio depende de esta interfaz, no de scikit-learn directamente.
    """

    @abstractmethod
    def train(self, df: pd.DataFrame) -> None:
        """Entrena el modelo con el DataFrame de propiedades."""
        ...

    @abstractmethod
    def predict(self, params: dict) -> dict:
        """
        Predice el precio para los parámetros dados.
        Devuelve: { predicted_price, margin_of_error, lower_bound, upper_bound }
        """
        ...

    @abstractmethod
    def compute_undervalued(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Añade columnas precio_predicho, diferencia, es_oportunidad al DataFrame.
        Devuelve el DataFrame enriquecido.
        """
        ...

    @abstractmethod
    def get_feature_importance(self) -> Dict[str, float]:
        """Devuelve el impacto por unidad de cada característica."""
        ...

    @abstractmethod
    def get_metrics(self) -> Dict[str, float]:
        """Devuelve métricas del modelo: r2_score, mean_absolute_error."""
        ...
