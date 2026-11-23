"""Ejecución controlada de operaciones y registro de eventos."""

# Permite incluir la fecha y la hora en cada evento.
from datetime import datetime

# Permite construir la ruta del archivo de log.
from pathlib import Path

# Permite conservar el detalle y las causas de las excepciones.
import traceback

# Importa la excepción base de los errores propios del sistema.
from excepciones import ErrorSistema


class RegistroEventos:
    """Escribe los eventos del programa en un archivo de texto."""

    def __init__(self, ruta=None):
        """Define la ubicación del log sin crear archivos de datos."""

        # Por defecto, el log queda junto a este archivo de Python.
        if ruta is None:
            self.ruta = Path(__file__).resolve().with_name("software_fj.log")
        else:
            self.ruta = Path(ruta)

    def escribir(self, nivel, mensaje):
        """Agrega un evento y controla posibles errores de escritura."""

        # Obtiene la fecha y la hora local con su zona horaria.
        fecha = datetime.now().astimezone().isoformat(timespec="seconds")

        # Construye el texto que se agregará al archivo.
        entrada = f"{fecha} | {nivel} | {mensaje}\n"

        try:
            # El modo append conserva los registros de ejecuciones anteriores.
            # El bloque with cierra el archivo incluso si ocurre un error.
            with self.ruta.open("a", encoding="utf-8") as archivo:
                archivo.write(entrada)

        except OSError as error:
            # Si el archivo no puede escribirse, informa en la consola.
            # No intenta registrar este fallo en el mismo archivo.
            print(f"[AVISO] No se pudo escribir en el log: {error}")
            return False

        else:
            # Confirma que el evento se escribió correctamente.
            return True


class EjecutorOperaciones:
    """Controla cada operación para que sus errores no detengan las demás."""

    def __init__(self, registro):
        """Recibe el objeto encargado de escribir los eventos."""

        self.registro = registro

        # Conserva los resultados de esta ejecución únicamente en memoria.
        self.resultados = []

    def ejecutar(self, descripcion, accion, *args, **kwargs):
        """Ejecuta una función y devuelve un resumen de su resultado."""

        # Registra el comienzo antes de intentar la operación.
        self.registro.escribir("INICIO", descripcion)

        try:
            # Llama a la función recibida con sus argumentos.
            resultado = accion(*args, **kwargs)

        except ErrorSistema as error:
            # Controla los errores previstos por las reglas del sistema.
            detalle = traceback.format_exc()
            self.registro.escribir(
                "ERROR",
                f"{descripcion} | {type(error).__name__}: {error}\n{detalle}",
            )

            print(f"[ERROR CONTROLADO] {descripcion}: {error}")

            respuesta = {
                "operacion": descripcion,
                "exito": False,
                "resultado": None,
                "error": type(error).__name__,
                "mensaje": str(error),
            }

        except Exception as error:
            # Captura errores inesperados en el límite de cada operación.
            # Conserva su detalle para investigarlos durante las pruebas.
            detalle = traceback.format_exc()
            self.registro.escribir(
                "ERROR INESPERADO",
                f"{descripcion} | {type(error).__name__}: {error}\n{detalle}",
            )

            print(
                f"[ERROR INESPERADO] {descripcion}: "
                f"{type(error).__name__}: {error}"
            )

            respuesta = {
                "operacion": descripcion,
                "exito": False,
                "resultado": None,
                "error": type(error).__name__,
                "mensaje": str(error),
            }

        else:
            # Este bloque solo se ejecuta si la operación no lanzó errores.
            self.registro.escribir("EXITO", descripcion)
            print(f"[CORRECTO] {descripcion}")

            respuesta = {
                "operacion": descripcion,
                "exito": True,
                "resultado": resultado,
                "error": None,
                "mensaje": "",
            }

        finally:
            # Se ejecuta tanto si la operación funciona como si falla.
            self.registro.escribir("FIN", descripcion)

        # Guarda el resumen para consultar los resultados de la simulación.
        self.resultados.append(respuesta)
        return respuesta
