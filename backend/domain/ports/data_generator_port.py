from abc import ABC, abstractmethod
import pandas as pd


class AbstractDataGenerator(ABC):
    """
    Puerto de dominio (interfaz) para la generación de datos de propiedades.
    """

    @abstractmethod
    def generate(self, n_samples: int = 800) -> pd.DataFrame:
        """
        Genera un DataFrame conteniendo las propiedades inmobiliarias sintéticas.
        """
        pass
