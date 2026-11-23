"""Simulación y comprobación del sistema Software FJ."""

# Importa las clases necesarias para ejecutar las operaciones.
from cliente import Cliente
from servicios import ServicioSala, ServicioEquipo, ServicioAsesoria
from gestor import GestorReservas
from registro import RegistroEventos, EjecutorOperaciones


def main():
    """Ejecuta casos válidos e inválidos y comprueba sus resultados."""

    # Cada ejecución comienza con listas nuevas en memoria.
    gestor = GestorReservas()
    registro = RegistroEventos()
    ejecutor = EjecutorOperaciones(registro)

    # Guarda las comprobaciones únicamente durante esta ejecución.
    comprobaciones = []

    def comprobar(descripcion, accion, error_esperado=None, verificar=None):
        """Compara lo ocurrido con el resultado esperado de una operación."""

        # Toda acción se ejecuta dentro del controlador de excepciones.
        respuesta = ejecutor.ejecutar(descripcion, accion)

        # Una operación válida debe terminar sin errores.
        if error_esperado is None:
            cumple = respuesta["exito"]
        else:
            # Un caso inválido debe producir exactamente el error previsto.
            cumple = (
                not respuesta["exito"]
                and respuesta["error"] == error_esperado
            )

        # Algunas pruebas también revisan valores y cambios de estado.
        if cumple and verificar is not None:
            try:
                cumple = bool(verificar(respuesta["resultado"]))
            except Exception as error:
                # Un fallo de la comprobación se informa, no se oculta.
                cumple = False
                registro.escribir(
                    "FALLO DE VERIFICACION",
                    f"{descripcion}: {type(error).__name__}: {error}",
                )

        # Registra si el comportamiento coincide con lo esperado.
        etiqueta = "APROBADA" if cumple else "FALLIDA"
        print(f"  Comprobación: {etiqueta}\n")
        registro.escribir("PRUEBA", f"{descripcion} | {etiqueta}")
        comprobaciones.append(cumple)

    print("SIMULACIÓN DEL SISTEMA SOFTWARE FJ\n")

    # Las construcciones se hacen dentro de las funciones lambda:
    # así también se controlan los errores de los constructores.

    # 1. Registra un cliente con datos ficticios válidos.
    comprobar(
        "Registrar cliente válido",
        lambda: gestor.registrar_cliente(
            Cliente("C01", "Ana Prueba", "ana@example.com", "3001234567")
        ),
        verificar=lambda cliente: cliente.identificador == "C01",
    )

    # 2. Rechaza un correo sin la estructura requerida.
    comprobar(
        "Rechazar correo inválido",
        lambda: gestor.registrar_cliente(
            Cliente("C02", "Luis Prueba", "correo-invalido", "3007654321")
        ),
        error_esperado="DatosInvalidosError",
        verificar=lambda _: len(gestor.clientes) == 1,
    )

    # 3. Rechaza el identificador de un cliente ya registrado.
    comprobar(
        "Rechazar cliente duplicado",
        lambda: gestor.registrar_cliente(
            Cliente("C01", "Otra Persona", "otra@example.com", "3007654321")
        ),
        error_esperado="DatosInvalidosError",
        verificar=lambda _: len(gestor.clientes) == 1,
    )

    # 4. Comprueba que una actualización inválida conserve el dato anterior.
    comprobar(
        "Conservar correo después de una actualización inválida",
        lambda: setattr(gestor.buscar_cliente("C01"), "correo", "incorrecto"),
        error_esperado="DatosInvalidosError",
        verificar=lambda _: (
            gestor.buscar_cliente("C01").correo == "ana@example.com"
        ),
    )

    # 5. Registra una sala con capacidad suficiente.
    comprobar(
        "Registrar sala válida",
        lambda: gestor.registrar_servicio(
            ServicioSala("S01", "Sala de reuniones", 50000, 10, 6)
        ),
    )

    # 6. Rechaza una sala con más asistentes que capacidad.
    comprobar(
        "Rechazar sala con exceso de asistentes",
        lambda: gestor.registrar_servicio(
            ServicioSala("S02", "Sala pequeña", 30000, 4, 8)
        ),
        error_esperado="DatosInvalidosError",
    )

    # 7. Registra el alquiler de dos equipos.
    comprobar(
        "Registrar equipos válidos",
        lambda: gestor.registrar_servicio(
            ServicioEquipo("E01", "Portátiles", 10000, "Computador", 5, 2)
        ),
    )

    # 8. Rechaza una cantidad superior a las existencias.
    comprobar(
        "Rechazar equipos insuficientes",
        lambda: gestor.registrar_servicio(
            ServicioEquipo("E02", "Proyectores", 15000, "Proyector", 1, 3)
        ),
        error_esperado="DatosInvalidosError",
    )

    # 9. Registra una asesoría.
    comprobar(
        "Registrar asesoría válida",
        lambda: gestor.registrar_servicio(
            ServicioAsesoria(
                "A01", "Asesoría técnica", 80000, "Python", "Laura Prueba"
            )
        ),
    )

    # 10. Rechaza una tarifa negativa.
    comprobar(
        "Rechazar tarifa negativa",
        lambda: gestor.registrar_servicio(
            ServicioAsesoria(
                "A02", "Asesoría inválida", -100, "Redes", "Pedro Prueba"
            )
        ),
        error_esperado="DatosInvalidosError",
    )

    # 11. Comprueba que un cliente inexistente no pueda crear una reserva.
    comprobar(
        "Rechazar reserva de cliente inexistente",
        lambda: gestor.crear_reserva("R00", "C99", "S01", 2),
        error_esperado="DatosInvalidosError",
        verificar=lambda _: len(gestor.reservas) == 0,
    )

    # 12. Rechaza una duración que no puede convertirse a número.
    comprobar(
        "Rechazar duración no numérica",
        lambda: gestor.crear_reserva("R00", "C01", "S01", "dos"),
        error_esperado="DatosInvalidosError",
    )

    # 13. Crea una reserva pendiente para la sala.
    comprobar(
        "Crear reserva de sala",
        lambda: gestor.crear_reserva("R01", "C01", "S01", 2),
        verificar=lambda reserva: reserva.estado == "pendiente",
    )

    # 14. Confirma la reserva y comprueba que el servicio quede ocupado.
    comprobar(
        "Confirmar reserva de sala",
        lambda: gestor.confirmar_reserva("R01"),
        verificar=lambda _: (
            gestor.buscar_reserva("R01").estado == "confirmada"
            and not gestor.buscar_servicio("S01").disponible
        ),
    )

    # 15. Puede existir otra solicitud pendiente para el mismo servicio.
    comprobar(
        "Crear segunda solicitud de sala",
        lambda: gestor.crear_reserva("R02", "C01", "S01", 1),
    )

    # 16. La segunda solicitud no puede confirmarse mientras esté ocupado.
    comprobar(
        "Rechazar confirmación de servicio ocupado",
        lambda: gestor.confirmar_reserva("R02"),
        error_esperado="ServicioNoDisponibleError",
        verificar=lambda _: gestor.buscar_reserva("R02").estado == "pendiente",
    )

    # 17. Cancelar la solicitud pendiente no debe liberar el servicio ajeno.
    comprobar(
        "Cancelar solicitud pendiente sin liberar servicio ocupado",
        lambda: gestor.cancelar_reserva("R02"),
        verificar=lambda _: (
            gestor.buscar_reserva("R02").estado == "cancelada"
            and not gestor.buscar_servicio("S01").disponible
        ),
    )

    # 18. Un descuento fuera de rango debe conservar la reserva confirmada.
    comprobar(
        "Rechazar descuento inválido sin alterar la reserva",
        lambda: gestor.procesar_reserva("R01", descuento=1.5),
        error_esperado="CalculoCostoError",
        verificar=lambda _: (
            gestor.buscar_reserva("R01").estado == "confirmada"
            and gestor.buscar_reserva("R01").total is None
            and not gestor.buscar_servicio("S01").disponible
        ),
    )

    # 19. Reintenta con datos correctos: 50000 × 2 × 0.90 × 1.19.
    comprobar(
        "Procesar sala con descuento e impuesto",
        lambda: gestor.procesar_reserva(
            "R01", impuesto=0.19, descuento=0.10
        ),
        verificar=lambda total: (
            total == 107100.0
            and gestor.buscar_reserva("R01").estado == "procesada"
            and gestor.buscar_servicio("S01").disponible
        ),
    )

    # 20. Una reserva ya procesada no puede cobrarse otra vez.
    comprobar(
        "Rechazar procesamiento repetido",
        lambda: gestor.procesar_reserva("R01"),
        error_esperado="EstadoReservaError",
    )

    # 21. Crea una reserva para dos equipos durante tres horas.
    comprobar(
        "Crear reserva de equipos",
        lambda: gestor.crear_reserva("R03", "C01", "E01", 3),
    )

    # 22. Confirma el alquiler.
    comprobar(
        "Confirmar reserva de equipos",
        lambda: gestor.confirmar_reserva("R03"),
    )

    # 23. Comprueba el cálculo: 10000 × 3 × 2.
    comprobar(
        "Procesar equipos sin ajustes",
        lambda: gestor.procesar_reserva("R03"),
        verificar=lambda total: total == 60000.0,
    )

    # 24. Crea una reserva de asesoría.
    comprobar(
        "Crear reserva de asesoría",
        lambda: gestor.crear_reserva("R04", "C01", "A01", 1.5),
    )

    # 25. Confirma la asesoría.
    comprobar(
        "Confirmar reserva de asesoría",
        lambda: gestor.confirmar_reserva("R04"),
    )

    # 26. Cancela una reserva confirmada y comprueba la liberación.
    comprobar(
        "Cancelar asesoría confirmada",
        lambda: gestor.cancelar_reserva("R04"),
        verificar=lambda _: (
            gestor.buscar_reserva("R04").estado == "cancelada"
            and gestor.buscar_servicio("A01").disponible
        ),
    )

    # 27. Impide procesar una reserva cancelada.
    comprobar(
        "Rechazar procesamiento de reserva cancelada",
        lambda: gestor.procesar_reserva("R04"),
        error_esperado="EstadoReservaError",
    )

    # 28. Crea otra asesoría para demostrar continuidad después del error.
    comprobar(
        "Crear nueva reserva después de un error",
        lambda: gestor.crear_reserva("R05", "C01", "A01", 1.5),
    )

    # 29. Confirma la nueva reserva.
    comprobar(
        "Confirmar nueva asesoría",
        lambda: gestor.confirmar_reserva("R05"),
    )

    # 30. Comprueba el cálculo: 80000 × 1.5 × 1.19.
    comprobar(
        "Procesar asesoría con impuesto",
        lambda: gestor.procesar_reserva("R05", impuesto=0.19),
        verificar=lambda total: total == 142800.0,
    )

    # Cuenta las operaciones ejecutadas y las comprobaciones aprobadas.
    total_pruebas = len(comprobaciones)
    aprobadas = sum(comprobaciones)
    fallidas = total_pruebas - aprobadas
    operaciones_exitosas = sum(
        resultado["exito"] for resultado in ejecutor.resultados
    )
    errores_detectados = len(ejecutor.resultados) - operaciones_exitosas

    # Muestra un resumen para revisar el comportamiento del programa.
    print("\nRESUMEN DE LA SIMULACIÓN")
    print(f"Operaciones ejecutadas: {len(ejecutor.resultados)}")
    print(f"Operaciones exitosas: {operaciones_exitosas}")
    print(f"Operaciones con error: {errores_detectados}")
    print(f"Comprobaciones aprobadas: {aprobadas}/{total_pruebas}")
    print(f"Comprobaciones fallidas: {fallidas}")
    print(f"Archivo de eventos: {registro.ruta}")

    # Conserva también el resumen como un evento del log.
    registro.escribir(
        "RESUMEN",
        f"Pruebas: {total_pruebas} | "
        f"Aprobadas: {aprobadas} | Fallidas: {fallidas}",
    )

    # Devuelve los objetos para permitir revisiones posteriores.
    return gestor, ejecutor, comprobaciones


# Ejecuta la simulación solo al iniciar este archivo directamente.
if __name__ == "__main__":
    main()
