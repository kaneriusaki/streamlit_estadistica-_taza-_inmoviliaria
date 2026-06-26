from typing import Dict, List
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

from domain.ports.ml_model_port import MLPredictor, MLTrainable


class SklearnLinearModel(MLPredictor):
    """
    Adaptador de salida: implementación de MLPredictor usando scikit-learn.
    Se inyectan las configuraciones del modelo en el constructor (OCP).
    No contiene lógica de lazy training ni automanejo del estado (SRP).
    """

    def __init__(self, features: List[str], target: str, undervalued_threshold: float):
        self._features = features
        self._target = target
        self._undervalued_threshold = undervalued_threshold
        self._model = LinearRegression()
        self._r2: float = 0.0
        self._mae: float = 0.0
        self._coeficientes: Dict[str, float] = {}

    def predict(self, params: dict) -> dict:
        x_new = pd.DataFrame([params])[self._features]
        predicted_price = float(self._model.predict(x_new)[0])
        return {
            "predicted_price": predicted_price,
            "margin_of_error": self._mae,
            "lower_bound": predicted_price - self._mae,
            "upper_bound": predicted_price + self._mae,
        }

    def compute_undervalued(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["precio_predicho"] = self._model.predict(df[self._features])
        df["diferencia"] = df["precio_predicho"] - df[self._target]
        df["es_oportunidad"] = (df["diferencia"] > self._undervalued_threshold).astype(int)
        return df

    def get_feature_importance(self) -> Dict[str, float]:
        return self._coeficientes

    def get_metrics(self) -> Dict[str, float]:
        return {
            "r2_score": self._r2,
            "mean_absolute_error": self._mae,
        }


class Trainer(MLTrainable):
    """
    Adaptador de salida: implementa MLTrainable para entrenar el predictor SklearnLinearModel.
    Separación de la lógica de entrenamiento (SRP).
    """

    def __init__(self, features: List[str], target: str):
        self._features = features
        self._target = target

    def train(self, model: SklearnLinearModel, df: pd.DataFrame) -> None:
        X = df[self._features]
        y = df[self._target]
        model._model.fit(X, y)

        predictions = model._model.predict(X)
        model._r2 = r2_score(y, predictions)
        model._mae = mean_absolute_error(y, predictions)
        model._coeficientes = dict(zip(self._features, model._model.coef_))
