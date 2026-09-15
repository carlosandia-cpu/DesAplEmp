# Laboratorio 03 - Desarrollo de Aplicaciones Empresariales

## Sistema de Gestión de Gimnasio

Aplicación web desarrollada con Django para gestionar información básica de un gimnasio utilizando Django ORM y SQLite.

## Problemática

Un gimnasio realiza de forma manual el registro de clientes, membresías, entrenadores, clases y pagos, lo que puede generar pérdida de información, errores y dificultad para consultar los datos.

La solución propuesta consiste en una aplicación web que permita almacenar y gestionar esta información de manera organizada y persistente.

## Usuarios involucrados

- Administradores
- Entrenadores
- Clientes

## Requisitos funcionales

1. Registrar nuevos clientes.
2. Listar los clientes registrados.
3. Actualizar la información de un cliente.
4. Eliminar clientes registrados.
5. Registrar membresías.
6. Registrar entrenadores.
7. Registrar clases y asignarles un entrenador.
8. Consultar las clases disponibles.
9. Registrar pagos.
10. Consultar la información almacenada.

## Entidades

La aplicación utiliza los siguientes Models:

- Cliente
- Membresia
- Pago
- Entrenador
- Clase

Existe una relación de uno a muchos entre `Entrenador` y `Clase`, implementada mediante `ForeignKey`.

## Operaciones CRUD

Se implementaron las siguientes operaciones utilizando Django ORM:

- CREATE: Registro de nuevos datos.
- READ: Consulta y listado mediante QuerySets.
- UPDATE: Modificación de registros existentes.
- DELETE: Eliminación de registros mediante confirmación y petición POST.

## Tecnologías utilizadas

- Python
- Django
- Django ORM
- SQLite
- HTML
- Git
- GitHub

## Ejecución

Activar el entorno virtual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1

Ejecutar el servidor:

python manage.py runserver

Ingresar a:

http://127.0.0.1:8000/gimnasio/clientes/
Aplicación Django

La nueva aplicación desarrollada para la Parte 2 del laboratorio se encuentra en:

gimnasio/

Esta aplicación contiene los Models, Forms, Views, URLs y Templates necesarios para implementar la gestión persistente de los datos.

## Laboratorio 04 - Relaciones entre modelos en Django

En este laboratorio se amplió la aplicación de gestión de gimnasio implementando los tres tipos principales de relaciones disponibles en Django ORM.

### Relaciones implementadas

- Relación uno a uno:
  - Cliente -> PerfilCliente
  - Implementada mediante OneToOneField.

- Relación uno a muchos:
  - Entrenador -> Clase
  - Implementada mediante ForeignKey.

- Relación muchos a muchos:
  - Cliente <-> Clase
  - Implementada mediante ManyToManyField utilizando el modelo intermedio InscripcionClase.

### Modelo intermedio

El modelo InscripcionClase almacena información propia de la relación:

- fecha_inscripcion
- estado

También se implementó un CRUD para registrar, editar y eliminar inscripciones.

### Consultas relacionadas

Se utilizaron:

- select_related() para consultar clases junto con sus entrenadores.
- prefetch_related() para consultar clientes, inscripciones y clases relacionadas.

### Tecnologías utilizadas

- Python
- Django
- Django ORM
- SQLite
- HTML
- Git
- GitHub