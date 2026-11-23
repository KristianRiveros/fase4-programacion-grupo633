"""Servicios especializados de salas, equipos y asesorías."""

# Importa la clase común y la validación de números.
from servicio import Servicio, validar_numero

# Importa la excepción utilizada para rechazar datos incorrectos.
from excepciones import DatosInvalidosError


def validar_entero_positivo(valor, nombre):
    """Comprueba que una cantidad sea un entero mayor que cero."""

    # Rechaza booleanos, decimales, textos y cantidades no positivas.
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise DatosInvalidosError(
            f"{nombre} debe ser un número entero mayor que cero."
        )

    return valor


def validar_texto(valor, nombre):
    """Comprueba un texto obligatorio y elimina espacios externos."""

    if not isinstance(valor, str) or not valor.strip():
        raise DatosInvalidosError(f"{nombre} debe ser un texto no vacío.")

    return valor.strip()


class ServicioSala(Servicio):
    """Representa el alquiler de una sala por horas."""

    def __init__(
        self, identificador, nombre, tarifa_base, capacidad, asistentes
    ):
        """Inicializa la sala y comprueba su capacidad."""

        # Inicializa los datos comunes mediante la clase Servicio.
        super().__init__(identificador, nombre, tarifa_base)

        # Almacena las características específicas de la sala.
        self.capacidad = capacidad
        self.asistentes = asistentes

        # Comprueba todos los datos antes de finalizar la creación.
        self.validar()

    def validar(self):
        """Valida los datos generales y la cantidad de asistentes."""

        super().validar()
        validar_entero_positivo(self.capacidad, "La capacidad")
        validar_entero_positivo(self.asistentes, "El número de asistentes")

        # Impide superar el límite de ocupación de la sala.
        if self.asistentes > self.capacidad:
            raise DatosInvalidosError(
                "Los asistentes no pueden superar la capacidad de la sala."
            )

        return True

    def validar_parametros(self, duracion):
        """Comprueba la sala y devuelve una duración válida."""

        self.validar()
        return validar_numero(
            duracion, "La duración en horas", estricto=True
        )

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """Calcula la tarifa por las horas de uso de la sala."""

        horas = self.validar_parametros(duracion)
        subtotal = self.tarifa_base * horas

        # Reutiliza el cálculo común de descuento e impuesto.
        return self._calcular_total(subtotal, impuesto, descuento)

    def describir(self):
        """Presenta las características de la sala."""

        return (
            f"Sala {self.identificador}: {self.nombre} | "
            f"Capacidad: {self.capacidad} | Asistentes: {self.asistentes} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f}"
        )


class ServicioEquipo(Servicio):
    """Representa el alquiler de una cantidad de equipos por horas."""

    def __init__(
        self, identificador, nombre, tarifa_base,
        tipo_equipo, cantidad_disponible, cantidad_solicitada
    ):
        """Inicializa el servicio y comprueba las cantidades."""

        super().__init__(identificador, nombre, tarifa_base)

        # Normaliza el texto y almacena las cantidades del servicio.
        self.tipo_equipo = validar_texto(tipo_equipo, "El tipo de equipo")
        self.cantidad_disponible = cantidad_disponible
        self.cantidad_solicitada = cantidad_solicitada

        self.validar()

    def validar(self):
        """Comprueba el tipo de equipo y las unidades solicitadas."""

        super().validar()
        validar_texto(self.tipo_equipo, "El tipo de equipo")
        validar_entero_positivo(
            self.cantidad_disponible, "La cantidad disponible"
        )
        validar_entero_positivo(
            self.cantidad_solicitada, "La cantidad solicitada"
        )

        # Impide solicitar más unidades de las disponibles.
        if self.cantidad_solicitada > self.cantidad_disponible:
            raise DatosInvalidosError(
                "La cantidad solicitada supera la cantidad disponible."
            )

        return True

    def validar_parametros(self, duracion):
        """Comprueba los equipos y devuelve una duración válida."""

        self.validar()
        return validar_numero(
            duracion, "La duración en horas", estricto=True
        )

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """Calcula el costo por horas y por cantidad de equipos."""

        horas = self.validar_parametros(duracion)

        # Valida que la cantidad pueda utilizarse en el cálculo decimal.
        cantidad = validar_numero(
            self.cantidad_solicitada, "La cantidad solicitada",
            estricto=True
        )
        subtotal = self.tarifa_base * horas * cantidad

        return self._calcular_total(subtotal, impuesto, descuento)

    def describir(self):
        """Presenta las características del alquiler de equipos."""

        return (
            f"Equipo {self.identificador}: {self.nombre} | "
            f"Tipo: {self.tipo_equipo} | "
            f"Unidades solicitadas: {self.cantidad_solicitada} | "
            f"Unidades disponibles: {self.cantidad_disponible} | "
            f"Tarifa por unidad y hora: ${self.tarifa_base:,.2f}"
        )


class ServicioAsesoria(Servicio):
    """Representa una asesoría especializada por horas."""

    def __init__(
        self, identificador, nombre, tarifa_base, especialidad, asesor
    ):
        """Inicializa la asesoría y valida sus datos específicos."""

        super().__init__(identificador, nombre, tarifa_base)

        # Comprueba y normaliza los textos obligatorios.
        self.especialidad = validar_texto(especialidad, "La especialidad")
        self.asesor = validar_texto(asesor, "El nombre del asesor")

        self.validar()

    def validar(self):
        """Comprueba los datos generales y los de la asesoría."""

        super().validar()
        validar_texto(self.especialidad, "La especialidad")
        validar_texto(self.asesor, "El nombre del asesor")

        return True

    def validar_parametros(self, duracion):
        """Comprueba la asesoría y devuelve una duración válida."""

        self.validar()
        return validar_numero(
            duracion, "La duración en horas", estricto=True
        )

    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """Calcula el costo de la asesoría según las horas contratadas."""

        horas = self.validar_parametros(duracion)
        subtotal = self.tarifa_base * horas

        return self._calcular_total(subtotal, impuesto, descuento)

    def describir(self):
        """Presenta la especialidad y el asesor responsable."""

        return (
            f"Asesoría {self.identificador}: {self.nombre} | "
            f"Especialidad: {self.especialidad} | Asesor: {self.asesor} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f}"
        )
