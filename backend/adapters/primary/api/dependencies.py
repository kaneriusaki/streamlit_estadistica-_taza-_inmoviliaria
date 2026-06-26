"""
Composition Root: wire up de todas las capas.

- D: todas las dependencias se inyectan desde aquí.
- La inicialización de datos (DataInitializer) está separada de los servicios.
- Se implementan los principios SOLID al inyectar fábricas de conexión y constantes del modelo.
"""

import config
from adapters.secondary.persistence.database import get_connection, init_schema
from adapters.secondary.persistence.data_seeder import DataSeeder
from adapters.secondary.persistence.sqlite_property_repo import SQLitePropertyRepository
from adapters.secondary.persistence.sqlite_user_repo import SQLiteUserRepository
from adapters.secondary.persistence.sqlite_prediction_repo import SQLitePredictionRepository
from adapters.secondary.persistence.data_generator import RealEstateDataGenerator
from adapters.secondary.ml.sklearn_model import SklearnLinearModel, Trainer
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

    # 1. Inicializar Esquema de la Base de Datos (SRP)
    conn = get_connection()
    try:
        init_schema(conn)
        conn.commit()
    finally:
        conn.close()

    # 2. Ejecutar Sembrado de datos (SRP)
    seeder = DataSeeder(connection_factory=get_connection)
    seeder.seed()

    # 3. Inicializar Repositorios inyectando la factory de conexión (DIP)
    property_repo = SQLitePropertyRepository(connection_factory=get_connection)
    user_repo = SQLiteUserRepository(connection_factory=get_connection)
    prediction_repo = SQLitePredictionRepository(connection_factory=get_connection)

    # 4. Inicializar Adaptadores de ML inyectando configuración (OCP)
    ml_model = SklearnLinearModel(
        features=config.FEATURES,
        target=config.TARGET,
        undervalued_threshold=config.UNDERVALUED_THRESHOLD
    )
    trainer = Trainer(
        features=config.FEATURES,
        target=config.TARGET
    )
    
    data_generator = RealEstateDataGenerator()

    # 5. Ejecutar inicialización del sistema (DataInitializer) usando interfaces segregadas (ISP / DIP)
    initializer = DataInitializer(
        query_repo=property_repo,
        ml_repo=property_repo,
        ml_model=ml_model,
        trainer=trainer,
        data_generator=data_generator
    )
    initializer.run()

    # 6. Crear servicios listos para su uso
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
