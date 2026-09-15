from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # CLIENTES
    # =========================
    path(
        'clientes/',
        views.lista_clientes,
        name='lista_clientes'
    ),

    path(
        'clientes/nuevo/',
        views.crear_cliente,
        name='crear_cliente'
    ),

    path(
        'clientes/<int:id>/editar/',
        views.editar_cliente,
        name='editar_cliente'
    ),

    path(
        'clientes/<int:id>/eliminar/',
        views.eliminar_cliente,
        name='eliminar_cliente'
    ),


    # =========================
    # MEMBRESÍAS
    # =========================
    path(
        'membresias/',
        views.lista_membresias,
        name='lista_membresias'
    ),

    path(
        'membresias/nueva/',
        views.crear_membresia,
        name='crear_membresia'
    ),


    # =========================
    # PAGOS
    # =========================
    path(
        'pagos/',
        views.lista_pagos,
        name='lista_pagos'
    ),

    path(
        'pagos/nuevo/',
        views.crear_pago,
        name='crear_pago'
    ),


    # =========================
    # ENTRENADORES
    # =========================
    path(
        'entrenadores/',
        views.lista_entrenadores,
        name='lista_entrenadores'
    ),

    path(
        'entrenadores/nuevo/',
        views.crear_entrenador,
        name='crear_entrenador'
    ),


    # =========================
    # CLASES
    # =========================
    path(
        'clases/',
        views.lista_clases,
        name='lista_clases'
    ),

    path(
        'clases/nueva/',
        views.crear_clase,
        name='crear_clase'
    ),


    # =========================
    # INSCRIPCIONES
    # CRUD DEL MODELO INTERMEDIO
    # =========================
    path(
        'inscripciones/',
        views.lista_inscripciones,
        name='lista_inscripciones'
    ),

    path(
        'inscripciones/nueva/',
        views.crear_inscripcion,
        name='crear_inscripcion'
    ),

    path(
        'inscripciones/<int:id>/editar/',
        views.editar_inscripcion,
        name='editar_inscripcion'
    ),

    path(
        'inscripciones/<int:id>/eliminar/',
        views.eliminar_inscripcion,
        name='eliminar_inscripcion'
    ),
]