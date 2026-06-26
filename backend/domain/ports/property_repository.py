from abc import ABC, abstractmethod
from typing import List
import pandas as pd

from domain.entities.property import Property


class PropertyQueryRepository(ABC):
    """
    Puerto de salida: Contrato abstracto para consultar propiedades en el dominio de negocio.
    Evita la dependencia directa con pandas o estructuras de datos específicas de ML.
    """

    @abstractmethod
    def count(self) -> int:
        """Devuelve el número de propiedades almacenadas."""
        pass

    @abstractmethod
    def find_all(self) -> List[Property]:
        """Devuelve todas las propiedades como entidades de dominio."""
        pass

    @abstractmethod
    def find_opportunities(self) -> List[Property]:
        """Devuelve solo las propiedades marcadas como oportunidad."""
        pass


class MLDataRepository(ABC):
    """
    Puerto de salida: Contrato abstracto para la persistencia e intercambio de datos del pipeline de ML.
    """

    @abstractmethod
    def save_all(self, df: pd.DataFrame) -> None:
        """Persiste todas las propiedades desde un DataFrame."""
        pass

    @abstractmethod
    def load_as_dataframe(self) -> pd.DataFrame:
        """Carga todas las propiedades como DataFrame para cálculos/entrenamiento de ML."""
        pass
