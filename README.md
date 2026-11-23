# Sistema de gestión de clientes, servicios y reservas — Software FJ

Proyecto de la Fase 4 — Componente práctico — Prácticas simuladas.

- Universidad: Universidad Nacional Abierta y a Distancia — UNAD.
- Curso: Programación.
- Código: 213023.
- Grupo: 633.
- Autor: Kristian Samuel Riveros Mojica.
- Usuario de GitHub: KristianRiveros.

## Descripción

Aplicación en Python que simula la gestión de clientes, servicios y reservas de Software FJ.

Utiliza programación orientada a objetos, clases abstractas, herencia, encapsulación, polimorfismo y excepciones personalizadas.

Los datos se mantienen en memoria mediante objetos y listas internas. No se utilizan bases de datos ni archivos para almacenar clientes, servicios o reservas. El archivo de log registra eventos y errores.

## Funcionalidades

- Registro y validación de clientes.
- Control de identificadores duplicados.
- Servicios de salas, equipos y asesorías.
- Cálculo de costos con impuestos y descuentos opcionales.
- Creación, confirmación, cancelación y procesamiento de reservas.
- Control de disponibilidad de los servicios.
- Manejo y encadenamiento de excepciones.
- Registro de eventos y errores.
- Simulación de 30 operaciones con comprobación de resultados.

## Archivos del proyecto

| Archivo | Función |
| --- | --- |
| `excepciones.py` | Define los errores personalizados. |
| `entidad.py` | Define la clase abstracta común. |
| `cliente.py` | Implementa clientes y validación de datos personales. |
| `servicio.py` | Define la base de los servicios y las reglas comunes de cálculo. |
| `servicios.py` | Implementa salas, equipos y asesorías. |
| `reserva.py` | Controla los estados y las operaciones de las reservas. |
| `gestor.py` | Administra las listas internas y evita registros duplicados. |
| `registro.py` | Ejecuta operaciones de forma controlada y registra eventos. |
| `main.py` | Ejecuta la simulación y comprueba los resultados. |
| `docs/diseno_clases.md` | Documenta el diseño inicial. |
| `Fase4_SoftwareFJ_KristianRiveros.ipynb` | Contiene la ejecución y los resultados de la simulación en Google Colab. |

El archivo `software_fj.log` se genera al ejecutar la simulación.

## Requisitos

- Python 3.
- Todos los archivos `.py` en la misma carpeta.
- Permiso de escritura en esa carpeta para generar el log.

El programa utiliza únicamente módulos de la biblioteca estándar de Python. No requiere instalar paquetes adicionales.

## Ejecución en un computador

Descargar el repositorio y descomprimirlo, o clonarlo mediante Git.

Abrir una terminal en la carpeta que contiene `main.py` y ejecutar:

```bash
python main.py
```

En Windows, si Python está disponible mediante el lanzador `py`, también puede ejecutarse:

```powershell
py main.py
```

La simulación funciona automáticamente y no solicita datos por teclado.

## Ejecución en Google Colab

En un entorno nuevo de Colab, ejecutar:

```python
!git clone https://github.com/KristianRiveros/fase4-programacion-grupo633.git
%cd /content/fase4-programacion-grupo633
!python main.py
```

Si el repositorio ya está descargado en ese entorno, basta con ejecutar:

```python
%cd /content/fase4-programacion-grupo633
!python main.py
```

Esta segunda opción vuelve a ejecutar la copia descargada; no actualiza sus archivos desde GitHub.

## Resultados verificados

La simulación se ejecutó en Google Colab y produjo:

| Resultado | Cantidad |
| --- | ---: |
| Operaciones ejecutadas | 30 |
| Operaciones exitosas | 18 |
| Operaciones con errores intencionales controlados | 12 |
| Comprobaciones aprobadas | 30 |
| Comprobaciones fallidas | 0 |

Los errores intencionales corresponden a situaciones que el sistema debe rechazar, como correos inválidos, registros duplicados, servicios ocupados y operaciones incompatibles con el estado de una reserva.

Una comprobación se aprueba cuando el comportamiento coincide con lo esperado, incluyendo el rechazo correcto de una operación inválida.

Estos resultados corresponden a los casos implementados en la simulación.

## Registro de eventos

El archivo `software_fj.log` se crea junto a los archivos del programa.

Registra:
- Inicio y finalización de cada operación.
- Operaciones exitosas.
- Errores y sus causas.
- Resultados de las comprobaciones.
- Resumen de la simulación.

Cada ejecución agrega registros al archivo existente.

Las fechas utilizan la zona horaria del entorno de ejecución. En la ejecución verificada en Colab se registraron en UTC.

## Reglas de la simulación

- Las tarifas son valores positivos por hora.
- La duración debe ser positiva y finita.
- Los equipos se cobran por cantidad y duración.
- Impuestos y descuentos se expresan como proporciones entre 0 y 1.
- Primero se aplica el descuento y después el impuesto.
- Una reserva confirmada ocupa el servicio completo.
- El servicio se libera al cancelar la reserva confirmada o finalizar su procesamiento.
- No se implementa un calendario ni la asignación simultánea de unidades de un mismo servicio.
- Al finalizar el programa, los registros en memoria no se conservan.

## Desarrollo y autoría

El trabajo se desarrolló de manera individual siguiendo la indicación del docente en el foro, ante la ausencia de aportes de los demás integrantes.

Los avances se registraron mediante commits descriptivos. Para la documentación inicial también se utilizaron ramas, una tarea y solicitudes de integración.

## Estado del proyecto

Implementación y simulación ejecutadas, con 30 comprobaciones aprobadas y verificación del archivo de log.
