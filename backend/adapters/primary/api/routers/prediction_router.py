from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from application.services.prediction_service import PredictionService
from adapters.primary.api.dependencies import get_prediction_service

router = APIRouter(prefix="/api", tags=["Predictions"])


class PropertyParams(BaseModel):
    area_m2: float
    habitaciones: int
    banos: int
    distancia_centro_km: float
    antiguedad_anos: float
    tiene_piscina: int


class PredictAndSave(PropertyParams):
    user_id: Optional[int] = None
    property_id: Optional[int] = None


@router.post("/predict")
def predict_price(params: PropertyParams, service: PredictionService = Depends(get_prediction_service)):
    try:
        return service.predict(params.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/predict_and_save")
def predict_and_save(params: PredictAndSave, service: PredictionService = Depends(get_prediction_service)):
    try:
        return service.predict_and_save(
            params.model_dump(exclude={"user_id", "property_id"}),
            params.user_id,
            params.property_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/predictions")
def list_predictions(user_id: Optional[int] = None, service: PredictionService = Depends(get_prediction_service)):
    return service.get_history(user_id)
