class FrontendError(Exception):
    """Clase base para excepciones del Frontend."""
    pass


class UserAlreadyExistsError(FrontendError):
    """Excepción cuando un usuario ya existe con ese email."""
    pass


class DatosNoEncontradosError(FrontendError):
    """Excepción cuando no se encuentran los datos solicitados."""
    pass


class ApiCaidaError(FrontendError):
    """Excepción para cuando la conexión con la API falla en el cliente."""
    pass
