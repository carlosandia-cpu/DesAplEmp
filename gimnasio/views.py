from django.shortcuts import render, redirect, get_object_or_404

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
    InscripcionClaseForm
)


# =========================
# CRUD COMPLETO DE CLIENTES
# CREATE - READ - UPDATE - DELETE
# =========================

def lista_clientes(request):
    # READ
    # Obtiene los clientes junto con sus inscripciones
    # y las clases relacionadas.
    clientes = Cliente.objects.prefetch_related(
        'inscripciones__clase'
    )

    return render(
        request,
        'gimnasio/lista_clientes.html',
        {'clientes': clientes}
    )


def crear_cliente(request):
    # CREATE
    form = ClienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_clientes')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Registrar cliente'
    })


def editar_cliente(request, id):
    # UPDATE
    cliente = get_object_or_404(Cliente, id=id)

    form = ClienteForm(
        request.POST or None,
        instance=cliente
    )

    if form.is_valid():
        form.save()
        return redirect('lista_clientes')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Editar cliente'
    })


def eliminar_cliente(request, id):
    # DELETE
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')

    return render(request, 'gimnasio/confirmar_eliminar.html', {
        'objeto': cliente,
        'tipo': 'cliente'
    })


# =========================
# MEMBRESÍAS
# READ Y CREATE
# =========================

def lista_membresias(request):
    # READ
    membresias = Membresia.objects.all()

    return render(
        request,
        'gimnasio/lista_membresias.html',
        {'membresias': membresias}
    )


def crear_membresia(request):
    # CREATE
    form = MembresiaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_membresias')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Registrar membresía'
    })


# =========================
# PAGOS
# READ Y CREATE
# =========================

def lista_pagos(request):
    # READ
    pagos = Pago.objects.all()

    return render(
        request,
        'gimnasio/lista_pagos.html',
        {'pagos': pagos}
    )


def crear_pago(request):
    # CREATE
    form = PagoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_pagos')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Registrar pago'
    })


# =========================
# ENTRENADORES
# READ Y CREATE
# =========================

def lista_entrenadores(request):
    # READ
    entrenadores = Entrenador.objects.all()

    return render(
        request,
        'gimnasio/lista_entrenadores.html',
        {'entrenadores': entrenadores}
    )


def crear_entrenador(request):
    # CREATE
    form = EntrenadorForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_entrenadores')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Registrar entrenador'
    })


# =========================
# CLASES
# READ Y CREATE
# RELACIÓN CON ENTRENADOR
# =========================

def lista_clases(request):
    # READ
    # Obtiene cada clase junto con su entrenador.
    clases = Clase.objects.select_related(
        'entrenador'
    )

    return render(
        request,
        'gimnasio/lista_clases.html',
        {'clases': clases}
    )


def crear_clase(request):
    # CREATE
    form = ClaseForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_clases')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Registrar clase'
    })


# =========================
# CRUD COMPLETO DE INSCRIPCIONES
# MODELO INTERMEDIO N:M
# CREATE - READ - UPDATE - DELETE
# =========================

def lista_inscripciones(request):
    # READ
    # Obtiene cada inscripción junto con
    # el cliente y la clase relacionados.
    inscripciones = InscripcionClase.objects.select_related(
        'cliente',
        'clase'
    )

    return render(
        request,
        'gimnasio/lista_inscripciones.html',
        {'inscripciones': inscripciones}
    )


def crear_inscripcion(request):
    # CREATE
    form = InscripcionClaseForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_inscripciones')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Registrar inscripción'
    })


def editar_inscripcion(request, id):
    # UPDATE
    inscripcion = get_object_or_404(
        InscripcionClase,
        id=id
    )

    form = InscripcionClaseForm(
        request.POST or None,
        instance=inscripcion
    )

    if form.is_valid():
        form.save()
        return redirect('lista_inscripciones')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Editar inscripción'
    })


def eliminar_inscripcion(request, id):
    # DELETE
    inscripcion = get_object_or_404(
        InscripcionClase,
        id=id
    )

    if request.method == 'POST':
        inscripcion.delete()
        return redirect('lista_inscripciones')

    return render(
        request,
        'gimnasio/confirmar_eliminar.html',
        {
            'objeto': inscripcion,
            'tipo': 'inscripción'
        }
    )