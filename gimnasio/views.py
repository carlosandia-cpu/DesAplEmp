from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Membresia, Pago, Entrenador, Clase
from .forms import ClienteForm, MembresiaForm, PagoForm, EntrenadorForm, ClaseForm


def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'gimnasio/lista_clientes.html', {'clientes': clientes})


def crear_cliente(request):
    form = ClienteForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_clientes')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Registrar cliente'
    })
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    form = ClienteForm(request.POST or None, instance=cliente)

    if form.is_valid():
        form.save()
        return redirect('lista_clientes')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Editar cliente'
    })
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')

    return render(request, 'gimnasio/confirmar_eliminar.html', {
        'objeto': cliente,
        'tipo': 'cliente'
    })


def lista_membresias(request):
    membresias = Membresia.objects.all()
    return render(request, 'gimnasio/lista_membresias.html', {'membresias': membresias})


def crear_membresia(request):
    form = MembresiaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_membresias')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Registrar membresía'
    })


def lista_pagos(request):
    pagos = Pago.objects.all()
    return render(request, 'gimnasio/lista_pagos.html', {'pagos': pagos})


def crear_pago(request):
    form = PagoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_pagos')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Registrar pago'
    })


def lista_entrenadores(request):
    entrenadores = Entrenador.objects.all()
    return render(request, 'gimnasio/lista_entrenadores.html', {'entrenadores': entrenadores})


def crear_entrenador(request):
    form = EntrenadorForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_entrenadores')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Registrar entrenador'
    })


def lista_clases(request):
    clases = Clase.objects.all()
    return render(request, 'gimnasio/lista_clases.html', {'clases': clases})


def crear_clase(request):
    form = ClaseForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('lista_clases')

    return render(request, 'gimnasio/formulario.html', {
        'form': form,
        'titulo': 'Registrar clase'
    })