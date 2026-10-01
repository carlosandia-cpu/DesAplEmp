from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import (
    Cliente,
    Membresia,
    Pago,
    Entrenador,
    Clase,
    PerfilCliente,
    InscripcionClase
)

from .forms import (
    ClienteForm,
    MembresiaForm,
    PagoForm,
    EntrenadorForm,
    ClaseForm,
    InscripcionClaseForm,
    PerfilClienteForm
)


# =========================
# FUNCIONES AUXILIARES
# =========================

def _guardar_form(request, form_class, instancia, destino, titulo):
    # Sirve para CREATE (instancia=None) y para UPDATE (instancia=objeto).
    form = form_class(request.POST or None, instance=instancia)

    if form.is_valid():
        form.save()
        return redirect(destino)

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': titulo,
        'volver': destino
    })


def _confirmar_eliminar(request, objeto, tipo, destino):
    # DELETE: primero pide confirmación (GET) y elimina al confirmar (POST).
    if request.method == 'POST':
        objeto.delete()
        return redirect(destino)

    return render(request, 'gimnasio/confirmar_eliminar.html', {
        'objeto': objeto,
        'tipo': tipo,
        'volver': destino
    })


# =========================
# CLIENTES
# =========================

def lista_clientes(request):
    clientes = Cliente.objects.prefetch_related('inscripciones__clase')
    return render(request, 'gimnasio/lista_clientes.html', {'clientes': clientes})


def crear_cliente(request):
    return _guardar_form(request, ClienteForm, None, 'lista_clientes', 'Registrar cliente')


def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return _guardar_form(request, ClienteForm, cliente, 'lista_clientes', 'Editar cliente')


def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    return _confirmar_eliminar(request, cliente, 'cliente', 'lista_clientes')


def detalle_cliente(request, id):
    # Trae al cliente con sus relaciones en pocas consultas.
    cliente = get_object_or_404(
        Cliente.objects.prefetch_related('membresias', 'pagos', 'inscripciones__clase'),
        id=id
    )
    # RELACIÓN 1 A 1: puede que el cliente todavía no tenga perfil.
    perfil = PerfilCliente.objects.filter(cliente=cliente).first()

    return render(request, 'gimnasio/detalle_cliente.html', {
        'cliente': cliente,
        'perfil': perfil
    })


def editar_perfil(request, id):
    # Sirve para crear el perfil si no existe y para editarlo si ya existe.
    cliente = get_object_or_404(Cliente, id=id)
    perfil = PerfilCliente.objects.filter(cliente=cliente).first()

    form = PerfilClienteForm(request.POST or None, instance=perfil)

    if form.is_valid():
        nuevo = form.save(commit=False)
        nuevo.cliente = cliente
        nuevo.save()
        return redirect('detalle_cliente', id=cliente.id)

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': f'Perfil de {cliente.nombre}',
        'volver_url': reverse('detalle_cliente', args=[cliente.id])
    })


# =========================
# MEMBRESÍAS
# =========================

def lista_membresias(request):
    membresias = Membresia.objects.all()
    return render(request, 'gimnasio/lista_membresias.html', {'membresias': membresias})


def crear_membresia(request):
    return _guardar_form(request, MembresiaForm, None, 'lista_membresias', 'Registrar membresía')


def editar_membresia(request, id):
    membresia = get_object_or_404(Membresia, id=id)
    return _guardar_form(request, MembresiaForm, membresia, 'lista_membresias', 'Editar membresía')


def eliminar_membresia(request, id):
    membresia = get_object_or_404(Membresia, id=id)
    return _confirmar_eliminar(request, membresia, 'membresía', 'lista_membresias')


# =========================
# PAGOS
# =========================

def lista_pagos(request):
    pagos = Pago.objects.all()
    return render(request, 'gimnasio/lista_pagos.html', {'pagos': pagos})


def crear_pago(request):
    return _guardar_form(request, PagoForm, None, 'lista_pagos', 'Registrar pago')


def editar_pago(request, id):
    pago = get_object_or_404(Pago, id=id)
    return _guardar_form(request, PagoForm, pago, 'lista_pagos', 'Editar pago')


def eliminar_pago(request, id):
    pago = get_object_or_404(Pago, id=id)
    return _confirmar_eliminar(request, pago, 'pago', 'lista_pagos')


# =========================
# ENTRENADORES
# =========================

def lista_entrenadores(request):
    entrenadores = Entrenador.objects.all()
    return render(request, 'gimnasio/lista_entrenadores.html', {'entrenadores': entrenadores})


def crear_entrenador(request):
    return _guardar_form(request, EntrenadorForm, None, 'lista_entrenadores', 'Registrar entrenador')


def editar_entrenador(request, id):
    entrenador = get_object_or_404(Entrenador, id=id)
    return _guardar_form(request, EntrenadorForm, entrenador, 'lista_entrenadores', 'Editar entrenador')


def eliminar_entrenador(request, id):
    entrenador = get_object_or_404(Entrenador, id=id)
    return _confirmar_eliminar(request, entrenador, 'entrenador', 'lista_entrenadores')


# =========================
# CLASES
# =========================

def lista_clases(request):
    clases = Clase.objects.select_related('entrenador')
    return render(request, 'gimnasio/lista_clases.html', {'clases': clases})


def crear_clase(request):
    return _guardar_form(request, ClaseForm, None, 'lista_clases', 'Registrar clase')


def editar_clase(request, id):
    clase = get_object_or_404(Clase, id=id)
    return _guardar_form(request, ClaseForm, clase, 'lista_clases', 'Editar clase')


def eliminar_clase(request, id):
    clase = get_object_or_404(Clase, id=id)
    return _confirmar_eliminar(request, clase, 'clase', 'lista_clases')


# =========================
# INSCRIPCIONES (MODELO INTERMEDIO N:M)
# =========================

def lista_inscripciones(request):
    inscripciones = InscripcionClase.objects.select_related('cliente', 'clase')
    return render(request, 'gimnasio/lista_inscripciones.html', {'inscripciones': inscripciones})


def crear_inscripcion(request):
    return _guardar_form(request, InscripcionClaseForm, None, 'lista_inscripciones', 'Registrar inscripción')


def editar_inscripcion(request, id):
    inscripcion = get_object_or_404(InscripcionClase, id=id)
    return _guardar_form(request, InscripcionClaseForm, inscripcion, 'lista_inscripciones', 'Editar inscripción')


def eliminar_inscripcion(request, id):
    inscripcion = get_object_or_404(InscripcionClase, id=id)
    return _confirmar_eliminar(request, inscripcion, 'inscripción', 'lista_inscripciones')