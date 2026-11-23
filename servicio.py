"""Clase abstracta y validaciones comunes de los servicios."""

# Permite exigir métodos propios en las clases derivadas.
from abc import abstractmethod

# Permite rechazar valores infinitos y valores numéricos no definidos.
from math import isfinite

# Importa la clase base y las excepciones del sistema.
from entidad import Entidad
from excepciones import DatosInvalidosError, CalculoCostoError


def validar_numero(valor, nombre, minimo=0, maximo=None, estricto=False):
    """Convierte un valor a número y comprueba su rango."""

    # Los booleanos no se aceptan como tarifas, cantidades o porcentajes.
    if isinstance(valor, bool):
        raise DatosInvalidosError(f"{nombre} debe ser un número.")

    # Intenta convertir el valor recibido a un número decimal.
    try:
        numero = float(valor)
    except (TypeError, ValueError, OverflowError) as error:
        # Conserva la causa original mediante encadenamiento.
        raise DatosInvalidosError(
            f"{nombre} debe ser un número válido."
        ) from error

    # Rechaza infinito y NaN.
    if not isfinite(numero):
        raise DatosInvalidosError(f"{nombre} debe ser un número finito.")

    # Comprueba el límite inferior.
    if numero < minimo or (estricto and numero == minimo):
        condicion = "mayor que" if estricto else "mayor o igual que"
        raise DatosInvalidosError(
            f"{nombre} debe ser {condicion} {minimo}."
        )

    # Comprueba el límite superior cuando se indique.
    if maximo is not None and numero > maximo:
        raise DatosInvalidosError(
            f"{nombre} debe ser menor o igual que {maximo}."
        )

    return numero


class Servicio(Entidad):
    """Define los datos comunes de salas, equipos y asesorías."""

    def __init__(self, identificador, nombre, tarifa_base):
        """Inicializa los datos generales del servicio."""

        # Valida el identificador mediante la clase Entidad.
        super().__init__(identificador)

        # Valida y normaliza el nombre antes de almacenarlo.
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError(
                "El nombre del servicio debe ser un texto no vacío."
            )

        self.__nombre = nombre.strip()

        # Solo permite tarifas positivas y finitas.
        self.__tarifa_base = validar_numero(
            tarifa_base, "La tarifa base", estricto=True
        )

        # Los servicios nuevos comienzan disponibles.
        self.__disponible = True

    @property
    def nombre(self):
        """Devuelve el nombre del servicio."""
        return self.__nombre

    @property
    def tarifa_base(self):
        """Devuelve la tarifa por hora."""
        return self.__tarifa_base

    @property
    def disponible(self):
        """Permite consultar la disponibilidad."""
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        """Permite cambiar la disponibilidad usando True o False."""

        # Evita asignar textos o números como estados de disponibilidad.
        if not isinstance(valor, bool):
            raise DatosInvalidosError(
                "La disponibilidad debe ser True o False."
            )

        self.__disponible = valor

    def validar(self):
        """Comprueba los datos comunes del servicio."""

        if not isinstance(self.nombre, str) or not self.nombre.strip():
            raise DatosInvalidosError(
                "El nombre del servicio no puede estar vacío."
            )

        validar_numero(
            self.tarifa_base, "La tarifa base", estricto=True
        )

        if not isinstance(self.disponible, bool):
            raise DatosInvalidosError("La disponibilidad es inválida.")

        return True

    def _calcular_total(self, subtotal, impuesto=0, descuento=0):
        """Aplica descuento e impuesto a un subtotal."""

        try:
            # Comprueba el subtotal y las proporciones recibidas.
            base = validar_numero(subtotal, "El subtotal")
            tasa = validar_numero(impuesto, "El impuesto", maximo=1)
            rebaja = validar_numero(descuento, "El descuento", maximo=1)

            # Aplica primero el descuento y después el impuesto.
            total = base * (1 - rebaja) * (1 + tasa)

            # Comprueba que el cálculo no haya producido un desbordamiento.
            if not isfinite(total):
                raise ArithmeticError("El total calculado no es finito.")

            return round(total, 2)

        except (DatosInvalidosError, ArithmeticError) as error:
            # Informa del problema y conserva el error que lo originó.
            raise CalculoCostoError(
                f"No se pudo calcular el costo: {error}"
            ) from error

    @abstractmethod
    def validar_parametros(self, duracion):
        """Valida la duración y los datos del servicio especializado."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """Calcula el costo según el tipo de servicio."""
        pass

    @abstractmethod
    def describir(self):
        """Describe las características del servicio especializado."""
        pass
