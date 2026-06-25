import requests
from exceptions import UserAlreadyExistsError, ApiCaidaError, DatosNoEncontradosError


class DataClient:
    """
    Cliente unificado de datos para el Frontend (Streamlit).
    Consume de manera exclusiva la API REST del backend.
    """

    def __init__(self, api_url: str, local_mode: bool = False):
        self.api_url = api_url
        self.local_mode = False  # El fallback ahora se maneja del lado del servidor.

    def _get(self, endpoint: str) -> list | dict:
        try:
            res = requests.get(f"{self.api_url}{endpoint}", timeout=5)
            if res.status_code != 200:
                raise DatosNoEncontradosError(f"No se pudieron obtener los datos de {endpoint}")
            return res.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise ApiCaidaError("El servidor de la API no está disponible.")

    def get_properties(self) -> list:
        return self._get("/properties")

    def get_opportunities(self) -> list:
        return self._get("/opportunities")

    def get_stats_insight(self) -> dict:
        return self._get("/stats_insight")

    def get_users(self) -> list:
        return self._get("/users")

    def create_user(self, nombre: str, email: str) -> dict:
        try:
            res = requests.post(
                f"{self.api_url}/users",
                json={"nombre": nombre, "email": email},
                timeout=5
            )
            if res.status_code == 409:
                raise UserAlreadyExistsError(res.json().get("detail", "El email ya está registrado"))
            elif res.status_code != 200:
                raise DatosNoEncontradosError("Error en la creación del usuario en el servidor")
            return res.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise ApiCaidaError("El servidor de la API no está disponible.")

    def predict_and_save(self, params: dict, user_id: int | None = None, property_id: int | None = None) -> dict:
        try:
            payload = {
                **params,
                "user_id": user_id,
                "property_id": property_id
            }
            res = requests.post(
                f"{self.api_url}/predict_and_save",
                json=payload,
                timeout=5
            )
            if res.status_code != 200:
                raise DatosNoEncontradosError("Error en la estimación de precio del servidor")
            return res.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            raise ApiCaidaError("El servidor de la API no está disponible.")

    def get_predictions(self) -> list:
        return self._get("/predictions")
