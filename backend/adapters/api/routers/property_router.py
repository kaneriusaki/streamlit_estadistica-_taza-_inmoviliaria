from fastapi import APIRouter, Depends
from application.services.property_service import PropertyService
from adapters.api.dependencies import get_property_service

router = APIRouter(prefix="/api", tags=["Properties"])


@router.get("/properties")
def get_properties(service: PropertyService = Depends(get_property_service)):
    return service.get_all_properties()


@router.get("/opportunities")
def get_opportunities(service: PropertyService = Depends(get_property_service)):
    return service.get_opportunities()


@router.get("/stats_insight")
def get_stats_insight(service: PropertyService = Depends(get_property_service)):
    return service.get_stats_insight()
