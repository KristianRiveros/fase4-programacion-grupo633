"""Excepciones personalizadas del sistema Software FJ."""


# Todos los errores propios del sistema tendrán esta clase como base.
class ErrorSistema(Exception):
    """Representa un error controlado del sistema Software FJ."""


# Identifica datos incompletos, incorrectos o fuera del rango permitido.
class DatosInvalidosError(ErrorSistema):
    """Indica que los datos recibidos no cumplen las validaciones."""


# Identifica un intento de reservar un servicio que no está disponible.
class ServicioNoDisponibleError(ErrorSistema):
    """Indica que el servicio solicitado no puede reservarse."""


# Identifica operaciones incompatibles con el estado de una reserva.
class EstadoReservaError(ErrorSistema):
    """Indica que la reserva no permite la operación solicitada."""


# Identifica problemas durante el cálculo del valor de un servicio.
class CalculoCostoError(ErrorSistema):
    """Indica que no fue posible calcular correctamente el costo."""
