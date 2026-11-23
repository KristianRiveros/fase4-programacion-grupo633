# Diseño de clases del sistema Software FJ

Autor: Kristian Samuel Riveros Mojica
Curso: Programación — Fase 4
Grupo: 633

## 1. Propósito

Organizar las clases del sistema de gestión de clientes, servicios y reservas antes de implementar el programa.

Este documento presenta las decisiones iniciales de diseño para desarrollar los requisitos del Anexo 3. Los nombres de las clases, los atributos y los métodos son una propuesta de implementación.

## 2. Clase abstracta Entidad

Responsabilidad:
Establecer una estructura común para las entidades del sistema.

Atributo:
- Identificador: permite distinguir cada entidad.

Métodos abstractos:
- validar(): comprueba que los datos sean correctos.
- describir(): devuelve una descripción de la entidad.

Cliente, Servicio y Reserva heredarán de esta clase.

## 3. Clase Cliente

Responsabilidad:
Representar al cliente y proteger sus datos mediante encapsulación.

Atributos:
- Identificador.
- Nombre.
- Correo electrónico.
- Teléfono.

Métodos:
- validar(): verifica los datos personales.
- describir(): presenta la información del cliente.
- Propiedades para consultar y actualizar los datos con validación.

Validaciones propuestas:
- No aceptar identificadores ni nombres vacíos.
- Comprobar una estructura básica del correo electrónico.
- Guardar el teléfono como texto y comprobar su formato.
- Impedir que una actualización inválida reemplace datos correctos.

## 4. Clase abstracta Servicio

Responsabilidad:
Definir los datos y las operaciones comunes de los servicios.

Atributos:
- Identificador.
- Nombre.
- Tarifa base por hora.
- Disponibilidad.

Métodos:
- validar(): comprueba los datos generales.
- validar_parametros(duracion): verifica las condiciones del servicio.
- calcular_costo(duracion, impuesto=0, descuento=0).
- describir(): explica las características del servicio.

Las clases derivadas implementarán el cálculo del costo, la descripción y la validación de sus parámetros.

Los parámetros opcionales de impuesto y descuento permitirán distintas formas de llamar al método de cálculo en Python.

## 5. Servicios especializados

### ServicioSala

Atributos adicionales:
- Capacidad.
- Número de asistentes.

Validaciones:
- Capacidad y asistentes deben ser enteros positivos.
- Los asistentes no pueden superar la capacidad.
- La duración debe ser positiva.

Costo propuesto:
Tarifa por hora multiplicada por la duración, con los ajustes de impuesto y descuento.

### ServicioEquipo

Atributos adicionales:
- Tipo de equipo.
- Cantidad disponible.
- Cantidad solicitada.

Validaciones:
- El tipo de equipo no puede estar vacío.
- Las cantidades deben ser enteros positivos.
- La cantidad solicitada no puede superar la disponible.
- La duración debe ser positiva.

Costo propuesto:
Tarifa por hora multiplicada por la duración y la cantidad solicitada, con los ajustes de impuesto y descuento.

### ServicioAsesoria

Atributos adicionales:
- Especialidad.
- Nombre del asesor.

Validaciones:
- La especialidad y el nombre del asesor no pueden estar vacíos.
- La duración debe ser positiva.

Costo propuesto:
Tarifa por hora multiplicada por la duración, con los ajustes de impuesto y descuento.

### Reglas comunes del cálculo

- Las tarifas deben ser positivas.
- Los valores numéricos deben ser finitos.
- Impuesto y descuento se expresarán como proporciones entre 0 y 1.
- Primero se aplicará el descuento al subtotal y después el impuesto.
- El resultado monetario se redondeará a dos decimales.

Estas reglas son decisiones de implementación del proyecto.

## 6. Clase Reserva

Responsabilidad:
Relacionar un cliente con un servicio y controlar el estado de la operación.

Atributos:
- Identificador.
- Cliente.
- Servicio.
- Duración.
- Estado.
- Total calculado.

Estados propuestos:
- Pendiente.
- Confirmada.
- Cancelada.
- Procesada.

Métodos:
- validar(): comprueba el cliente, el servicio y la duración.
- confirmar(): valida la disponibilidad y confirma la reserva.
- cancelar(): cancela una reserva pendiente o confirmada.
- procesar(): calcula el total y completa una reserva confirmada.
- describir(): presenta un resumen de la reserva.

Reglas:
- Una reserva nueva comienza pendiente.
- Solo una reserva pendiente puede confirmarse.
- Solo una reserva confirmada puede procesarse.
- Una reserva cancelada o procesada no puede volver a procesarse.
- Los cambios de estado se realizan únicamente si las validaciones terminan correctamente.

Para esta simulación, un servicio confirmado quedará ocupado y se liberará al cancelar o finalizar su procesamiento. No se implementará un calendario de reservas.

## 7. Excepciones personalizadas

Se propone una excepción general ErrorSistema y las siguientes excepciones derivadas:

- DatosInvalidosError: datos incompletos, incorrectos o fuera de rango.
- ServicioNoDisponibleError: servicio que no puede reservarse.
- EstadoReservaError: operación no permitida para el estado actual.
- CalculoCostoError: error al calcular el valor del servicio.

Cuando una conversión o un cálculo produzca un error original, se utilizará encadenamiento de excepciones para conservar su causa.

## 8. Organización del sistema

Una clase GestorReservas coordinará las operaciones.

Mantendrá listas internas de:
- Clientes.
- Servicios.
- Reservas.

Sus responsabilidades serán:
- Registrar y buscar entidades.
- Evitar identificadores duplicados dentro de cada lista.
- Verificar que el cliente y el servicio estén registrados.
- Coordinar la creación y gestión de reservas.

Los datos permanecerán en memoria mediante objetos y listas. No se utilizarán bases de datos ni archivos para guardar clientes, servicios o reservas.

## 9. Manejo y registro de errores

Se utilizarán:
- try/except para controlar errores esperados.
- try/except/else para ejecutar acciones posteriores a una operación exitosa.
- try/except/finally para registrar el cierre de un intento.
- Encadenamiento de excepciones para conservar la causa original.

Los errores detectados y los eventos relevantes se registrarán en un archivo de log.

Cada operación de la simulación tendrá manejo de errores para que un fallo no detenga las operaciones siguientes.

## 10. Verificación prevista

Se ejecutarán al menos diez operaciones que incluyan:

- Registro correcto de clientes.
- Rechazo de datos de clientes inválidos.
- Rechazo de identificadores duplicados.
- Creación correcta de los tres tipos de servicio.
- Rechazo de parámetros de servicio incorrectos.
- Confirmación y procesamiento de reservas válidas.
- Intentos de reservar servicios no disponibles.
- Cancelaciones válidas.
- Intentos de realizar operaciones incompatibles con el estado.
- Cálculos con impuestos y descuentos.
- Rechazo de valores de cálculo inválidos.

Se comprobarán los resultados, el contenido del log y la continuidad del programa después de los errores.

## 11. Estado del desarrollo

Diseño inicial propuesto. La implementación y las pruebas están pendientes.
