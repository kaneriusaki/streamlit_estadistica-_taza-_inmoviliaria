from abc import ABC, abstractmethod
from typing import List
import pandas as pd

from domain.entities.property import Property


class IPropertyRepository(ABC):
    """
    Puerto de salida: contrato abstracto para el acceso a datos de propiedades.
    El dominio depende de esta interfaz, NO de la implementación concreta.
    """

    @abstractmethod
    def count(self) -> int:
        """Devuelve el número de propiedades almacenadas."""
        ...

    @abstractmethod
    def save_all(self, df: pd.DataFrame) -> None:
        """Persiste todas las propiedades desde un DataFrame."""
        ...

    @abstractmethod
    def load_as_dataframe(self) -> pd.DataFrame:
        """Carga todas las propiedades como DataFrame para cálculos ML."""
        ...

    @abstractmethod
    def find_all(self) -> List[Property]:
        """Devuelve todas las propiedades como entidades de dominio."""
        ...

    @abstractmethod
    def find_opportunities(self) -> List[Property]:
        """Devuelve solo las propiedades marcadas como oportunidad."""
        ...
