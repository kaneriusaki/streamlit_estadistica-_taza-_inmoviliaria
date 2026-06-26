"""
Caso de uso: inicialización del sistema.

Responsabilidad única: orquestar la generación de datos iniciales y el entrenamiento inicial del modelo ML.
Se ejecuta una sola vez al arrancar la aplicación.
"""

from domain.ports.property_repository import PropertyQueryRepository, MLDataRepository
from domain.ports.ml_model_port import MLPredictor, MLTrainable
from domain.ports.data_generator_port import AbstractDataGenerator


class DataInitializer:
    """
    Separa la responsabilidad de inicialización de la consulta de propiedades.
    Depende exclusivamente de puertos (abstracciones), cumpliendo con DIP e ISP.
    """

    def __init__(
        self,
        query_repo: PropertyQueryRepository,
        ml_repo: MLDataRepository,
        ml_model: MLPredictor,
        trainer: MLTrainable,
        data_generator: AbstractDataGenerator,
    ):
        self._query_repo = query_repo
        self._ml_repo = ml_repo
        self._model = ml_model
        self._trainer = trainer
        self._data_generator = data_generator

    def run(self) -> None:
        """
        Ejecuta la inicialización:
        1. Genera y guarda propiedades de prueba si la base de datos está vacía.
        2. Entrena el modelo ML.
        3. Enriquece los datos de propiedades con las predicciones del modelo.
        """
        if self._query_repo.count() == 0:
            df = self._data_generator.generate(800)
            df["precio_predicho"] = 0.0
            df["diferencia"] = 0.0
            df["es_oportunidad"] = 0
            self._ml_repo.save_all(df)

        df = self._ml_repo.load_as_dataframe()
        
        # El entrenamiento se realiza a través de la interfaz del Trainer (SRP / ISP)
        self._trainer.train(self._model, df)

        df_enriched = self._model.compute_undervalued(df)
        self._ml_repo.save_all(df_enriched)
