"""Organización de clientes, servicios y reservas en listas internas."""

# Importa las entidades que administra el gestor.
from cliente import Cliente
from servicio import Servicio
from reserva import Reserva

# Importa la excepción para registros y búsquedas incorrectos.
from excepciones import DatosInvalidosError


class GestorReservas:
    """Administra los registros del sistema sin utilizar bases de datos."""

    def __init__(self):
        """Crea las listas privadas de registros."""

        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

    @property
    def clientes(self):
        """Devuelve una copia de la lista de clientes."""
        return self.__clientes.copy()

    @property
    def servicios(self):
        """Devuelve una copia de la lista de servicios."""
        return self.__servicios.copy()

    @property
    def reservas(self):
        """Devuelve una copia de la lista de reservas."""
        return self.__reservas.copy()

    @staticmethod
    def _normalizar_identificador(identificador):
        """Comprueba un identificador y elimina espacios externos."""

        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError(
                "El identificador debe ser un texto no vacío."
            )

        return identificador.strip()

    @staticmethod
    def _verificar_duplicado(lista, identificador, tipo):
        """Rechaza identificadores repetidos dentro de una lista."""

        for elemento in lista:
            if elemento.identificador == identificador:
                raise DatosInvalidosError(
                    f"Ya existe un registro de {tipo} "
                    f"con el identificador {identificador}."
                )

    def _buscar(self, lista, identificador, tipo):
        """Busca una entidad y genera un error si no existe."""

        identificador = self._normalizar_identificador(identificador)

        # Recorre los registros hasta encontrar el identificador.
        for elemento in lista:
            if elemento.identificador == identificador:
                return elemento

        # Evita devolver un valor vacío que provoque errores posteriores.
        raise DatosInvalidosError(
            f"No existe un registro de {tipo} "
            f"con el identificador {identificador}."
        )

    def registrar_cliente(self, cliente):
        """Valida y registra un cliente sin duplicar su identificador."""

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError(
                "Solo se pueden registrar objetos de tipo Cliente."
            )

        # Comprueba los datos y la unicidad antes de modificar la lista.
        cliente.validar()
        self._verificar_duplicado(
            self.__clientes, cliente.identificador, "cliente"
        )

        self.__clientes.append(cliente)
        return cliente

    def registrar_servicio(self, servicio):
        """Valida y registra un servicio sin duplicar su identificador."""

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError(
                "Solo se pueden registrar objetos de tipo Servicio."
            )

        servicio.validar()
        self._verificar_duplicado(
            self.__servicios, servicio.identificador, "servicio"
        )

        self.__servicios.append(servicio)
        return servicio

    def buscar_cliente(self, identificador):
        """Devuelve un cliente registrado."""
        return self._buscar(self.__clientes, identificador, "cliente")

    def buscar_servicio(self, identificador):
        """Devuelve un servicio registrado."""
        return self._buscar(self.__servicios, identificador, "servicio")

    def buscar_reserva(self, identificador):
        """Devuelve una reserva registrada."""
        return self._buscar(self.__reservas, identificador, "reserva")

    def crear_reserva(
        self, identificador, id_cliente, id_servicio, duracion
    ):
        """Crea una reserva usando un cliente y un servicio registrados."""

        identificador = self._normalizar_identificador(identificador)

        # Impide registrar dos reservas con el mismo identificador.
        self._verificar_duplicado(
            self.__reservas, identificador, "reserva"
        )

        # Las búsquedas fallan si el cliente o el servicio no existen.
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(id_servicio)

        # El constructor de Reserva comprueba los datos de la operación.
        reserva = Reserva(
            identificador, cliente, servicio, duracion
        )

        # Solo agrega la reserva si su creación finalizó correctamente.
        self.__reservas.append(reserva)
        return reserva

    def confirmar_reserva(self, identificador):
        """Busca la reserva y solicita su confirmación."""

        reserva = self.buscar_reserva(identificador)
        return reserva.confirmar()

    def cancelar_reserva(self, identificador):
        """Busca la reserva y solicita su cancelación."""

        reserva = self.buscar_reserva(identificador)
        return reserva.cancelar()

    def procesar_reserva(self, identificador, impuesto=0, descuento=0):
        """Busca la reserva y procesa su costo con ajustes opcionales."""

        reserva = self.buscar_reserva(identificador)

        return reserva.procesar(
            impuesto=impuesto,
            descuento=descuento,
        )
