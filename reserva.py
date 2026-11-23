"""Gestión de los estados y las operaciones de una reserva."""

# Importa las clases que participan en una reserva.
from entidad import Entidad
from cliente import Cliente
from servicio import Servicio, validar_numero

# Importa los errores que pueden presentarse en sus operaciones.
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    EstadoReservaError,
)


class Reserva(Entidad):
    """Relaciona un cliente con un servicio y controla su estado."""

    def __init__(self, identificador, cliente, servicio, duracion):
        """Inicializa una reserva pendiente y valida sus datos."""

        # Valida y guarda el identificador mediante la clase base.
        super().__init__(identificador)

        # Comprueba los tipos antes de utilizar los objetos recibidos.
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError(
                "La reserva debe estar asociada a un objeto Cliente."
            )

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError(
                "La reserva debe estar asociada a un objeto Servicio."
            )

        # Guarda las referencias al cliente y al servicio.
        self.__cliente = cliente
        self.__servicio = servicio

        # Normaliza la duración y exige un valor positivo y finito.
        self.__duracion = validar_numero(
            duracion, "La duración en horas", estricto=True
        )

        # El estado y el total solo se modifican mediante operaciones.
        self.__estado = "pendiente"
        self.__total = None

        # Comprueba los datos antes de finalizar la creación.
        self.validar()

    @property
    def cliente(self):
        """Devuelve el cliente asociado."""
        return self.__cliente

    @property
    def servicio(self):
        """Devuelve el servicio asociado."""
        return self.__servicio

    @property
    def duracion(self):
        """Devuelve la duración en horas."""
        return self.__duracion

    @property
    def estado(self):
        """Permite consultar el estado sin modificarlo directamente."""
        return self.__estado

    @property
    def total(self):
        """Devuelve el total, o None si todavía no se ha procesado."""
        return self.__total

    def validar(self):
        """Comprueba los datos del cliente y los parámetros del servicio."""

        self.cliente.validar()
        self.servicio.validar_parametros(self.duracion)

        return True

    def confirmar(self):
        """Confirma una reserva pendiente y ocupa el servicio."""

        # Una reserva confirmada, cancelada o procesada no puede confirmarse.
        if self.estado != "pendiente":
            raise EstadoReservaError(
                f"No se puede confirmar una reserva {self.estado}."
            )

        # Revisa los datos antes de modificar el estado.
        self.validar()

        # Impide confirmar otra reserva sobre un servicio ocupado.
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.servicio.identificador} no está disponible."
            )

        # Solo cambia los datos cuando todas las comprobaciones terminan.
        self.servicio.disponible = False
        self.__estado = "confirmada"

        return f"Reserva {self.identificador} confirmada."

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""

        # Las reservas canceladas o procesadas no pueden cancelarse.
        if self.estado not in ("pendiente", "confirmada"):
            raise EstadoReservaError(
                f"No se puede cancelar una reserva {self.estado}."
            )

        # Solo libera el servicio si esta reserva lo había ocupado.
        if self.estado == "confirmada":
            self.servicio.disponible = True

        # Cancelar una reserva pendiente no altera la disponibilidad.
        self.__estado = "cancelada"

        return f"Reserva {self.identificador} cancelada."

    def procesar(self, impuesto=0, descuento=0):
        """Calcula el total y finaliza una reserva confirmada."""

        # Impide procesar reservas pendientes, canceladas o ya procesadas.
        if self.estado != "confirmada":
            raise EstadoReservaError(
                f"No se puede procesar una reserva {self.estado}."
            )

        # Comprueba nuevamente los datos antes de calcular.
        self.validar()

        # Usa el cálculo específico del servicio: sala, equipo o asesoría.
        # Si ocurre una excepción, las líneas posteriores no se ejecutan.
        total_calculado = self.servicio.calcular_costo(
            self.duracion,
            impuesto=impuesto,
            descuento=descuento,
        )

        # Guarda el resultado y libera el servicio tras un cálculo exitoso.
        self.__total = total_calculado
        self.servicio.disponible = True
        self.__estado = "procesada"

        return self.total

    def describir(self):
        """Devuelve un resumen de la reserva y de su valor."""

        # Distingue un total aún no calculado de un costo igual a cero.
        valor = (
            "sin calcular"
            if self.total is None
            else f"${self.total:,.2f}"
        )

        return (
            f"Reserva {self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} horas | "
            f"Estado: {self.estado} | Total: {valor}"
        )
