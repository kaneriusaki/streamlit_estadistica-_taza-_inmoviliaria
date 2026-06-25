from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.prediction import Prediction


class PredictionRepository(ABC):
    """
    Puerto de salida: contrato abstracto para el acceso a datos de predicciones.
    """

    @abstractmethod
    def save(self, prediction: Prediction) -> None:
        """Persiste una predicción en el almacenamiento."""
        ...

    @abstractmethod
    def find_all(self, user_id: Optional[int] = None) -> List[Prediction]:
        """
        Devuelve todas las predicciones.
        Si se provee user_id, filtra por ese usuario.
        """
        ...
