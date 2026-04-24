from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from statistical_middleware import stats_engine

app = FastAPI(
    title="Tasador Automático de Bienes Raíces API",
    description="API que conecta el middleware estadístico con el frontend.",
    version="1.0.0"
)

class PropertyParams(BaseModel):
    area_m2: float
    habitaciones: int
    banos: int
    distancia_centro_km: float
    antiguedad_anos: float
    tiene_piscina: int

@app.get("/")
def root():
    return {"message": "API de Tasador funcionando. Ve a /docs para más detalles."}

@app.get("/api/properties")
def get_properties():
    """Devuelve todas las propiedades catalogadas en el mercado."""
    return stats_engine.get_all_properties()

@app.get("/api/opportunities")
def get_opportunities():
    """Devuelve las propiedades infravaloradas (oportunidades)."""
    return stats_engine.get_opportunities()

@app.get("/api/stats_insight")
def get_stats_insight():
    """Devuelve la importancia de las variables y métricas del modelo."""
    return {
        "feature_importance": stats_engine.get_feature_importance(),
        "model_metrics": stats_engine.get_model_metrics()
    }

@app.post("/api/predict")
def predict_price(params: PropertyParams):
    """Predice el precio basado en características."""
    try:
        prediction = stats_engine.predict_price(params.dict())
        return prediction
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
