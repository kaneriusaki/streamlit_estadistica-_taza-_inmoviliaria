import sys
import os
import requests
import pandas as pd

# Añadir el directorio del backend al sys.path para poder importar las clases de dominio e infraestructura
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.append(backend_path)

from domain.exceptions import UserAlreadyExistsError, ApiCaidaError, DatosNoEncontradosError


class DataClient:
    """
    Cliente unificado de datos para el Frontend (Streamlit).
    Implementa el mecanismo de fallback automático:
    Intenta consumir el backend FastAPI (vía REST API), y si no se encuentra disponible,
    conecta directamente a la base de datos SQLite y ejecuta los modelos ML de forma local.
    """

    def __init__(self, api_url: str):
        self.api_url = api_url
        self.local_mode = False
        
        # Servicios locales perezosos (lazy initialization)
        self._property_service = None
        self._user_service = None
        self._prediction_service = None

    def _init_local_services(self):
        if self._property_service is not None:
            return

        # Importaciones locales tardías de la infraestructura y servicios del backend
        from infrastructure.persistence.database import init_db
        from infrastructure.persistence.sqlite_property_repo import SQLitePropertyRepository
        from infrastructure.persistence.sqlite_user_repo import SQLiteUserRepository
        from infrastructure.persistence.sqlite_prediction_repo import SQLitePredictionRepository
        from infrastructure.ml.sklearn_model import SklearnLinearModel
        from infrastructure.ml.data_generator import RealEstateDataGenerator
        from application.initializer import DataInitializer
        from application.services.property_service import PropertyService
        from application.services.user_service import UserService
        from application.services.prediction_service import PredictionService

        # Inicializar base de datos local
        init_db()

        # Instanciar repositorios y modelo
        property_repo = SQLitePropertyRepository()
        user_repo = SQLiteUserRepository()
        prediction_repo = SQLitePredictionRepository()
        ml_model = SklearnLinearModel()
        data_generator = RealEstateDataGenerator()

        # Ejecutar inicialización y entrenamiento si es necesario
        initializer = DataInitializer(property_repo, ml_model, data_generator)
        initializer.run()

        # Instanciar servicios
        self._property_service = PropertyService(property_repo, ml_model)
        self._user_service = UserService(user_repo)
        self._prediction_service = PredictionService(prediction_repo, ml_model)

    def _execute_with_fallback(self, api_call_fn, local_call_fn):
        """
        Orquesta el fallback: intenta ejecutar la llamada a la API y
        si falla la conexión, conmuta a modo local y ejecuta la función local.
        """
        if not self.local_mode:
            try:
                return api_call_fn()
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                self.local_mode = True

        if self.local_mode:
            self._init_local_services()
            try:
                return local_call_fn()
            except Exception as e:
                # Si falla incluso la base de datos local, lanzar una excepción de dominio limpia
                raise DatosNoEncontradosError(f"Error al acceder a los datos locales: {str(e)}")

    def get_properties(self) -> list:
        def api_fn():
            res = requests.get(f"{self.api_url}/properties")
            if res.status_code != 200:
                raise DatosNoEncontradosError("No se pudieron obtener las propiedades de la API")
            return res.json()

        def local_fn():
            return self._property_service.get_all_properties()

        return self._execute_with_fallback(api_fn, local_fn)

    def get_opportunities(self) -> list:
        def api_fn():
            res = requests.get(f"{self.api_url}/opportunities")
            if res.status_code != 200:
                raise DatosNoEncontradosError("No se pudieron obtener las oportunidades de la API")
            return res.json()

        def local_fn():
            return self._property_service.get_opportunities()

        return self._execute_with_fallback(api_fn, local_fn)

    def get_stats_insight(self) -> dict:
        def api_fn():
            res = requests.get(f"{self.api_url}/stats_insight")
            if res.status_code != 200:
                raise DatosNoEncontradosError("No se pudieron obtener las estadísticas de la API")
            return res.json()

        def local_fn():
            return self._property_service.get_stats_insight()

        return self._execute_with_fallback(api_fn, local_fn)

    def get_users(self) -> list:
        def api_fn():
            res = requests.get(f"{self.api_url}/users")
            if res.status_code != 200:
                raise DatosNoEncontradosError("No se pudieron obtener los usuarios de la API")
            return res.json()

        def local_fn():
            return self._user_service.list_users()

        return self._execute_with_fallback(api_fn, local_fn)

    def create_user(self, nombre: str, email: str) -> dict:
        def api_fn():
            res = requests.post(f"{self.api_url}/users", json={"nombre": nombre, "email": email})
            if res.status_code == 409:
                raise UserAlreadyExistsError(res.json().get("detail", "El email ya está registrado"))
            elif res.status_code != 200:
                raise DatosNoEncontradosError("Error en la creación del usuario en el servidor")
            return res.json()

        def local_fn():
            # UserService en backend lanza UserAlreadyExistsError directamente
            return self._user_service.create_user(nombre, email)

        return self._execute_with_fallback(api_fn, local_fn)

    def predict_and_save(self, params: dict, user_id: int | None = None, property_id: int | None = None) -> dict:
        def api_fn():
            payload = {
                **params,
                "user_id": user_id,
                "property_id": property_id
            }
            res = requests.post(f"{self.api_url}/predict_and_save", json=payload)
            if res.status_code != 200:
                raise DatosNoEncontradosError("Error en la estimación de precio del servidor")
            return res.json()

        def local_fn():
            return self._prediction_service.predict_and_save(params, user_id, property_id)

        return self._execute_with_fallback(api_fn, local_fn)

    def get_predictions(self) -> list:
        def api_fn():
            res = requests.get(f"{self.api_url}/predictions")
            if res.status_code != 200:
                raise DatosNoEncontradosError("No se pudo cargar el historial de la API")
            return res.json()

        def local_fn():
            return self._prediction_service.get_history()

        return self._execute_with_fallback(api_fn, local_fn)
