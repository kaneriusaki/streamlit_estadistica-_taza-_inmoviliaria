import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from data_generator import generate_real_estate_data

class RealEstateStatsMiddleware:
    def __init__(self):
        self.model = LinearRegression()
        self.df = generate_real_estate_data(800)
        
        self.features = ['area_m2', 'habitaciones', 'banos', 'distancia_centro_km', 'antiguedad_anos', 'tiene_piscina']
        self.target = 'precio_lista'
        
        self._train_model()
        self._calculate_undervalued()
        
    def _train_model(self):
        X = self.df[self.features]
        y = self.df[self.target]
        self.model.fit(X, y)
        
        self.r2 = r2_score(y, self.model.predict(X))
        self.mae = mean_absolute_error(y, self.model.predict(X))
        
        # Guardar coeficientes
        self.coeficientes = dict(zip(self.features, self.model.coef_))
        
    def _calculate_undervalued(self):
        """
        Calcula qué propiedades están infravaloradas.
        Una propiedad está infravalorada si su precio de lista es significativamente
        menor al precio que el modelo estadístico predice para ella.
        """
        X = self.df[self.features]
        self.df['precio_predicho'] = self.model.predict(X)
        self.df['diferencia'] = self.df['precio_predicho'] - self.df['precio_lista']
        
        # Infravalorada si el precio predicho es por lo menos 15,000 mayor al de lista
        self.df['es_oportunidad'] = self.df['diferencia'] > 15000
        
    def get_feature_importance(self):
        """
        Devuelve el impacto esperado en el precio por cada unidad de incremento en la característica.
        (Ej: +1 m2, +1 habitación, etc.)
        """
        return self.coeficientes
        
    def get_model_metrics(self):
        return {
            "r2_score": self.r2,
            "mean_absolute_error": self.mae
        }
        
    def predict_price(self, params: dict):
        """
        Predice el precio basado en parámetros.
        """
        x_new = pd.DataFrame([params])[self.features]
        predicted_price = self.model.predict(x_new)[0]
        # El margen de error base
        margin_of_error = self.mae
        return {
            "predicted_price": predicted_price,
            "margin_of_error": margin_of_error,
            "lower_bound": predicted_price - margin_of_error,
            "upper_bound": predicted_price + margin_of_error
        }
        
    def get_all_properties(self):
        return self.df.to_dict(orient='records')
        
    def get_opportunities(self):
        return self.df[self.df['es_oportunidad']].to_dict(orient='records')

# Instancia global para usar en la API
stats_engine = RealEstateStatsMiddleware()
