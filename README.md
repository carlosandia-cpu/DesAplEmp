## Laboratorio 05 - Django Admin

En este laboratorio se configuró y personalizó el panel administrativo de Django para gestionar los modelos del sistema de gimnasio.

### Modelos registrados

Los modelos registrados en Django Admin son:

- Cliente
- Membresia
- Pago
- Entrenador
- Clase
- PerfilCliente
- InscripcionClase
- Ejercicio
- Sala
- Asistencia
- EvaluacionFisica
- HorarioClase
- ObjetivoCliente
- Rutina
- RutinaEjercicio

### Personalización de ModelAdmin

Se configuraron clases ModelAdmin para los siguientes modelos:

- ClienteAdmin:
  - list_display para mostrar ID, nombre, DNI, correo y teléfono.
  - search_fields para buscar por nombre, DNI o correo.
  - StackedInline para administrar PerfilCliente.
  - TabularInline para administrar InscripcionClase.

- EntrenadorAdmin:
  - list_display para mostrar ID, nombre, especialidad y teléfono.
  - search_fields para buscar por nombre o especialidad.
  - list_filter para filtrar por especialidad.

- ClaseAdmin:
  - list_display para mostrar ID, nombre, horario, entrenador y sala.
  - search_fields para buscar por nombre de clase o entrenador.
  - list_filter para filtrar por entrenador y sala.

### Relaciones administradas

- Relación 1:1 entre Cliente y PerfilCliente mediante StackedInline.
- Relación N:M entre Cliente y Clase mediante el modelo intermedio InscripcionClase y un TabularInline.
- Relación 1:N entre Entrenador y Clase.

La información administrada mediante Django Admin se almacena de manera persistente en la base de datos SQLite.

## Refactorización de Templates (Laboratorio 6)

Se refactorizó la capa de presentación del **Sistema de Gestión del Gimnasio** aplicando modularización y principios DRY:

- **Herencia de Plantillas (`base.html`):** Integración de `{% extends %}` y `{% block content %}` en las plantillas de todas las entidades (*Clientes, Clases, Entrenadores, Inscripciones, Membresías, Pagos*).
- **Filtros de Formateo:** Aplicación del filtro `|upper` en `lista_clientes.html` para estandarizar la visualización de datos.
- **Componentes Reutilizables:** Creación del parcial `mensaje_vacio.html` cargado con `{% include %}` en los listados del sistema.
- **Seguridad:** Verificación del autoescapado de caracteres (*auto-escaping*) nativo en Django contra inyecciones XSS.

## Laboratorio 07: transacciones, consultas avanzadas y optimización

Sistema de gestión de gimnasio. La entidad principal es **Cliente**, con relaciones 1:1 (`PerfilCliente`), 1:N (`Membresia` y `Pago`) y N:M con `Clase` mediante el modelo intermedio `InscripcionClase`.

### Cambios en el modelo
- `Clase.cupos_disponibles`: campo entero que se descuenta al inscribir.
- `InscripcionClase.estado` (Activa, Completada o Cancelada), `sesiones` y `precio_sesion`.
- Migración `0004` con los campos nuevos.

### Operación transaccional
- **Vista:** `inscribir_cliente`, en `/gimnasio/inscripciones/inscribir/`.
- **Entidades que modifica:** `InscripcionClase`, `Pago` y `Clase`.
- Dentro de `transaction.atomic()` crea la inscripción, registra el pago y descuenta un cupo con `F()`. Si no hay cupos, se hace rollback completo y el template muestra el error. Si todo sale bien, se aplica Post/Redirect/Get.

### Reportes
| Reporte | URL | Entidades | Técnicas |
|---|---|---|---|
| Inscripciones | `/gimnasio/reporte/` | InscripcionClase y Cliente | `aggregate()`, `values().annotate()` y `annotate()` |
| Pagos y clases | `/gimnasio/reporte/pagos-clases/` | Pago y Clase | `aggregate()`, `values().annotate()` y `annotate()` |

### QuerySets personalizados (con `as_manager()`)
| QuerySet | Métodos | Usado en |
|---|---|---|
| `ClienteQuerySet` | `con_inscripciones_activas()`, `con_membresia_vigente()`, `con_pagos_del_mes()` y `con_total_inscripciones()` | `lista_clientes` y `reporte` |
| `ClaseQuerySet` | `proximas()`, `con_cupos()` y `con_ocupacion()` | `lista_clases` y `reporte_pagos_clases` |

### Optimización del problema N+1
| Pantalla | Técnica | Consultas antes | Consultas después |
|---|---|---|---|
| Membresías | `select_related('cliente')` | 5 | 1 |
| Clases | `select_related('entrenador').prefetch_related('entrenador__clases')` | 5 | 2 |