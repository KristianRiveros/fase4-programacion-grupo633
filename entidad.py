"""Clase abstracta base para las entidades de Software FJ."""

# Importa las herramientas para definir clases y métodos abstractos.
from abc import ABC, abstractmethod

# Importa la excepción que representa datos incorrectos.
from excepciones import DatosInvalidosError


# ABC permite declarar esta clase como una base abstracta.
class Entidad(ABC):
    """Define la estructura común de clientes, servicios y reservas."""

    def __init__(self, identificador):
        """Valida y almacena el identificador de la entidad."""

        # El identificador debe ser una cadena de texto.
        if not isinstance(identificador, str):
            raise DatosInvalidosError(
                "El identificador debe ser una cadena de texto."
            )

        # Elimina espacios al principio y al final.
        identificador = identificador.strip()

        # Rechaza cadenas vacías o compuestas únicamente por espacios.
        if not identificador:
            raise DatosInvalidosError(
                "El identificador no puede estar vacío."
            )

        # Guarda el identificador como atributo privado.
        self.__identificador = identificador

    # Permite consultar el identificador sin ofrecer un setter público.
    @property
    def identificador(self):
        """Devuelve el identificador de la entidad."""
        return self.__identificador

    # Cada clase concreta deberá implementar sus propias validaciones.
    @abstractmethod
    def validar(self):
        """Comprueba que los datos de la entidad sean correctos."""
        pass

    # Cada clase concreta deberá implementar su propia descripción.
    @abstractmethod
    def describir(self):
        """Devuelve una descripción de la entidad."""
        pass
