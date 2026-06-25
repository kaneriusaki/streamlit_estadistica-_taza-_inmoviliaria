"""
Composition Root: wire up de todas las capas.

- D: todas las dependencias se inyectan desde aquí, ningún módulo
     concreto es instanciado dentro de domain o application.
- La inicialización de datos (DataInitializer) está separada de
  PropertyService para cumplir SRP.
"""

from adapters.secondary.ml.sklearn_model import SklearnLinearModel
from adapters.secondary.ml.data_generator import RealEstateDataGenerator
from adapters.secondary.persistence.database import init_db
from adapters.secondary.persistence.sqlite_property_repo import SQLitePropertyRepository
from adapters.secondary.persistence.sqlite_user_repo import SQLiteUserRepository
from adapters.secondary.persistence.sqlite_prediction_repo import SQLitePredictionRepository
from application.services.property_service import PropertyService
from application.services.user_service import UserService
from application.services.prediction_service import PredictionService
from application.initializer import DataInitializer


_property_service: PropertyService | None = None
_user_service: UserService | None = None
_prediction_service: PredictionService | None = None


def _init_services():
    global _property_service, _user_service, _prediction_service
    if _property_service is not None:
        return

    init_db()

    property_repo = SQLitePropertyRepository()
    user_repo = SQLiteUserRepository()
    prediction_repo = SQLitePredictionRepository()
    ml_model = SklearnLinearModel()
    data_generator = RealEstateDataGenerator()

    initializer = DataInitializer(property_repo, ml_model, data_generator)
    initializer.run()

    _property_service = PropertyService(property_repo, ml_model)
    _user_service = UserService(user_repo)
    _prediction_service = PredictionService(prediction_repo, ml_model)


def get_property_service() -> PropertyService:
    _init_services()
    return _property_service


def get_user_service() -> UserService:
    _init_services()
    return _user_service


def get_prediction_service() -> PredictionService:
    _init_services()
    return _prediction_service
