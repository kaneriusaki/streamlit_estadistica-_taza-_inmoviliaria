"""
Caso de uso: inicialización del sistema.

Responsabilidad única: orquestar el seeding de datos sintéticos
y el entrenamiento inicial del modelo ML.
Se ejecuta una sola vez al arrancar la aplicación.
"""

from domain.ports.property_repository import PropertyRepository
from domain.ports.ml_model_port import MLModel


class DataInitializer:
    """
    Separa la responsabilidad de inicialización (data seeding + training)
    de la consulta de propiedades (PropertyService).

    - S: única razón de cambio: la lógica de bootstrap del sistema.
    - D: depende de interfaces (PropertyRepository, MLModel), no de concretions.
    """

    def __init__(
        self,
        property_repo: PropertyRepository,
        ml_model: MLModel,
        data_generator,
    ):
        self._repo = property_repo
        self._model = ml_model
        self._data_generator = data_generator

    def run(self) -> None:
        """Ejecuta la inicialización: genera datos si no existen y entrena el modelo."""
        if self._repo.count() == 0:
            df = self._data_generator.generate(800)
            df["precio_predicho"] = 0.0
            df["diferencia"] = 0.0
            df["es_oportunidad"] = 0
            self._repo.save_all(df)

        df = self._repo.load_as_dataframe()
        self._model.train(df)

        df_enriched = self._model.compute_undervalued(df)
        self._repo.save_all(df_enriched)
