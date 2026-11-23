"""Registro y validación de clientes del sistema Software FJ."""

# Permite comprobar el formato del correo y del teléfono.
import re

# Importa la clase base y la excepción para datos incorrectos.
from entidad import Entidad
from excepciones import DatosInvalidosError


class Cliente(Entidad):
    """Representa un cliente con datos personales encapsulados."""

    def __init__(self, identificador, nombre, correo, telefono):
        """Inicializa el cliente y valida cada dato antes de guardarlo."""

        # La clase base valida y almacena el identificador.
        super().__init__(identificador)

        # Las propiedades ejecutan sus validaciones al asignar los datos.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @staticmethod
    def _validar_nombre(valor):
        """Comprueba el nombre y devuelve el texto sin espacios externos."""

        # Rechaza valores que no sean texto o que estén vacíos.
        if not isinstance(valor, str) or not valor.strip():
            raise DatosInvalidosError(
                "El nombre debe ser un texto no vacío."
            )

        return valor.strip()

    @staticmethod
    def _validar_correo(valor):
        """Comprueba una estructura básica de correo electrónico."""

        # Verifica el tipo antes de utilizar operaciones de texto.
        if not isinstance(valor, str):
            raise DatosInvalidosError(
                "El correo electrónico debe ser una cadena de texto."
            )

        # Elimina espacios externos sin modificar el contenido interno.
        valor = valor.strip()

        # Exige usuario, arroba y dominio con un punto, sin espacios.
        if re.fullmatch(r"[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+", valor) is None:
            raise DatosInvalidosError(
                "El correo debe tener un formato como usuario@dominio.com."
            )

        return valor

    @staticmethod
    def _validar_telefono(valor):
        """Comprueba entre 7 y 15 dígitos y un signo + inicial opcional."""

        # Se conserva como texto para mantener ceros iniciales.
        if not isinstance(valor, str):
            raise DatosInvalidosError(
                "El teléfono debe escribirse como texto."
            )

        valor = valor.strip()

        # Solo permite dígitos y, opcionalmente, un + al principio.
        if re.fullmatch(r"\+?[0-9]{7,15}", valor) is None:
            raise DatosInvalidosError(
                "El teléfono debe contener entre 7 y 15 dígitos, "
                "sin espacios ni guiones, con un + inicial opcional."
            )

        return valor

    @property
    def nombre(self):
        """Permite consultar el nombre."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        """Valida el nuevo nombre antes de reemplazar el anterior."""
        self.__nombre = self._validar_nombre(valor)

    @property
    def correo(self):
        """Permite consultar el correo."""
        return self.__correo

    @correo.setter
    def correo(self, valor):
        """Valida el nuevo correo antes de reemplazar el anterior."""
        self.__correo = self._validar_correo(valor)

    @property
    def telefono(self):
        """Permite consultar el teléfono."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        """Valida el nuevo teléfono antes de reemplazar el anterior."""
        self.__telefono = self._validar_telefono(valor)

    def validar(self):
        """Comprueba nuevamente los datos actuales del cliente."""

        # Reutiliza las validaciones sin modificar los datos almacenados.
        self._validar_nombre(self.__nombre)
        self._validar_correo(self.__correo)
        self._validar_telefono(self.__telefono)

        # Si alguna validación falla, se lanza DatosInvalidosError.
        return True

    def describir(self):
        """Devuelve un resumen de los datos del cliente."""
        return (
            f"Cliente {self.identificador}: {self.nombre} | "
            f"Correo: {self.correo} | Teléfono: {self.telefono}"
        )
