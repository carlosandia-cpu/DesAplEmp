from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),

    path('membresias/', views.lista_membresias, name='lista_membresias'),
    path('membresias/nueva/', views.crear_membresia, name='crear_membresia'),

    path('pagos/', views.lista_pagos, name='lista_pagos'),
    path('pagos/nuevo/', views.crear_pago, name='crear_pago'),

    path('entrenadores/', views.lista_entrenadores, name='lista_entrenadores'),
    path('entrenadores/nuevo/', views.crear_entrenador, name='crear_entrenador'),

    path('clases/', views.lista_clases, name='lista_clases'),
    path('clases/nueva/', views.crear_clase, name='crear_clase'),
]