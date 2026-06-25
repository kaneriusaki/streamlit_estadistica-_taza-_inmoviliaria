from typing import Dict

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

from domain.ports.ml_model_port import MLModel


FEATURES = [
    "area_m2",
    "habitaciones",
    "banos",
    "distancia_centro_km",
    "antiguedad_anos",
    "tiene_piscina",
]
TARGET = "precio_lista"
UNDERVALUED_THRESHOLD = 15_000


class SklearnLinearModel(MLModel):
    """
    Adaptador de salida: implementación concreta de MLModel.

    - O: abierto a extensión (nuevos modelos via MLModel), cerrado a modificación.
    - L: cualquier implementación de MLModel puede sustituir esta clase.
    - D: la capa de dominio depende de MLModel, no de esta implementación.
    """

    def __init__(self):
        self._model = LinearRegression()
        self._r2: float = 0.0
        self._mae: float = 0.0
        self._coeficientes: Dict[str, float] = {}
        self._trained: bool = False
        self._training_df: pd.DataFrame | None = None

    def train(self, df: pd.DataFrame) -> None:
        X = df[FEATURES]
        y = df[TARGET]
        self._model.fit(X, y)

        predictions = self._model.predict(X)
        self._r2 = r2_score(y, predictions)
        self._mae = mean_absolute_error(y, predictions)
        self._coeficientes = dict(zip(FEATURES, self._model.coef_))
        self._training_df = df
        self._trained = True

    def _ensure_trained(self) -> None:
        """
        Lazy training: si el modelo no está entrenado pero hay datos
        disponibles del último compute_undervalued, se entrena solo.
        Esto elimina el acoplamiento temporal entre servicios.
        """
        if not self._trained:
            if self._training_df is not None:
                self.train(self._training_df)
            else:
                raise RuntimeError(
                    "El modelo no ha sido entrenado. Debes llamar train() "
                    "o pasar un DataFrame a compute_undervalued primero."
                )

    def predict(self, params: dict) -> dict:
        self._ensure_trained()
        x_new = pd.DataFrame([params])[FEATURES]
        predicted_price = float(self._model.predict(x_new)[0])
        return {
            "predicted_price": predicted_price,
            "margin_of_error": self._mae,
            "lower_bound": predicted_price - self._mae,
            "upper_bound": predicted_price + self._mae,
        }

    def compute_undervalued(self, df: pd.DataFrame) -> pd.DataFrame:
        self._ensure_trained()
        df = df.copy()
        df["precio_predicho"] = self._model.predict(df[FEATURES])
        df["diferencia"] = df["precio_predicho"] - df[TARGET]
        df["es_oportunidad"] = df["diferencia"] > UNDERVALUED_THRESHOLD
        return df

    def get_feature_importance(self) -> Dict[str, float]:
        self._ensure_trained()
        return self._coeficientes

    def get_metrics(self) -> Dict[str, float]:
        self._ensure_trained()
        return {
            "r2_score": self._r2,
            "mean_absolute_error": self._mae,
        }
