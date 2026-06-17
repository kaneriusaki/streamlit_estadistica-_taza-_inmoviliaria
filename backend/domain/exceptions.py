class DomainError(Exception):
    """Clase base para excepciones del dominio."""
    pass


class UserAlreadyExistsError(DomainError):
    """Excepción cuando un usuario ya existe con ese email."""
    pass


class DatosNoEncontradosError(DomainError):
    """Excepción cuando no se encuentran los datos solicitados."""
    pass


class ApiCaidaError(DomainError):
    """Excepción para cuando la conexión con la API falla en el cliente."""
    pass
