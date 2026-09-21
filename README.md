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