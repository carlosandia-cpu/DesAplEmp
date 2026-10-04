from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.db.models import F, Sum, Count, DecimalField
from django.contrib import messages
from django.utils import timezone

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
    PerfilClienteForm,
    InscribirClienteForm
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
    # LAB 07 - EJERCICIO 7: se usan los métodos del QuerySet personalizado
    # en lugar de escribir filter() repetidos en la vista.
    filtro = request.GET.get('filtro', 'todos')
    clientes = Cliente.objects.all()

    if filtro == 'activos':
        clientes = clientes.con_inscripciones_activas()
    elif filtro == 'vigentes':
        clientes = clientes.con_membresia_vigente()
    elif filtro == 'pagos_mes':
        clientes = clientes.con_pagos_del_mes()
    else:
        filtro = 'todos'

    return render(request, 'gimnasio/lista_clientes.html', {
        'clientes': clientes,
        'filtro': filtro
    })


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
    membresias = Membresia.objects.select_related('cliente')
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
    pagos = Pago.objects.select_related('cliente', 'membresia')
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
    # LAB 07 - EJERCICIO 12: filtros con los métodos del QuerySet personalizado.
    filtro = request.GET.get('filtro', 'todas')

    # LAB 07 - EJERCICIO 13: select_related trae el entrenador con un JOIN y
    # prefetch_related trae las clases de esos entrenadores en una sola consulta.
    clases = Clase.objects.select_related('entrenador').prefetch_related('entrenador__clases')

    if filtro == 'proximas':
        clases = clases.proximas()
    elif filtro == 'con_cupos':
        clases = clases.con_cupos()
    elif filtro == 'proximas_con_cupos':
        clases = clases.proximas().con_cupos()
    else:
        filtro = 'todas'

    return render(request, 'gimnasio/lista_clases.html', {
        'clases': clases,
        'filtro': filtro
    })

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


# =========================
# LAB 07 - EJERCICIO 3
# OPERACIÓN TRANSACCIONAL: inscribir cliente + registrar pago + descontar cupo
# =========================

class SinCupos(Exception):
    """Se lanza dentro de la transacción para forzar el rollback."""
    pass


def inscribir_cliente(request):
    form = InscribirClienteForm(request.POST or None)
    error = None

    if request.method == 'POST' and form.is_valid():
        cliente = form.cleaned_data['cliente']
        clase = form.cleaned_data['clase']
        sesiones = form.cleaned_data['sesiones']
        precio = form.cleaned_data['precio_sesion']
        metodo = form.cleaned_data['metodo_pago']
        hoy = timezone.localdate()

        try:
            # Todo lo que ocurre aquí dentro se confirma junto o se deshace junto.
            with transaction.atomic():
                # 1) Crea la inscripción (modelo 1)
                InscripcionClase.objects.create(
                    cliente=cliente,
                    clase=clase,
                    fecha_inscripcion=hoy,
                    estado='Activa',
                    sesiones=sesiones,
                    precio_sesion=precio
                )

                # 2) Registra el pago (modelo 2)
                Pago.objects.create(
                    cliente=cliente,
                    monto=sesiones * precio,
                    fecha=hoy,
                    metodo_pago=metodo
                )

                # 3) Descuenta un cupo con F() (modelo 3).
                # El filtro cupos_disponibles__gte=1 evita quedar en negativo;
                # update() devuelve cuántas filas cambió.
                filas = Clase.objects.filter(
                    id=clase.id,
                    cupos_disponibles__gte=1
                ).update(cupos_disponibles=F('cupos_disponibles') - 1)

                if filas == 0:
                    # Al lanzar la excepción, atomic() hace ROLLBACK de los pasos 1 y 2.
                    raise SinCupos(
                        f'La clase "{clase.nombre}" no tiene cupos disponibles. '
                        f'No se registró ninguna inscripción ni pago.'
                    )

        except SinCupos as e:
            error = str(e)
        else:
            # PATRÓN POST/REDIRECT/GET: tras el éxito se redirige,
            # así recargar la página no repite la operación.
            messages.success(
                request,
                f'{cliente.nombre} fue inscrito en {clase.nombre}. '
                f'Pago registrado: S/ {sesiones * precio:.2f}.'
            )
            return redirect('lista_inscripciones')

    return render(request, 'gimnasio/inscribir.html', {
        'form': form,
        'error': error,
        'clases': Clase.objects.order_by('nombre')
    })


# =========================
# LAB 07 - EJERCICIO 6
# PÁGINA DE REPORTE (resultados de los ejercicios 4 y 5)
# =========================

def reporte(request):
    # EJERCICIO 4: aggregate() devuelve un diccionario con totales globales.
    totales = InscripcionClase.objects.aggregate(
        total_ingresos=Sum(
            F('sesiones') * F('precio_sesion'),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        ),
        total_sesiones=Sum('sesiones'),
        total_inscripciones=Count('id')
    )

    # EJERCICIO 5 + 7: el annotate() ahora vive en el QuerySet personalizado.
    clientes = Cliente.objects.con_total_inscripciones().order_by(
        '-total_inscripciones', 'nombre'
    )

    # EJERCICIO 5: values().annotate() agrupa por estado.
    por_estado = (
        InscripcionClase.objects
        .values('estado')
        .annotate(cantidad=Count('id'))
        .order_by('-cantidad')
    )

    return render(request, 'gimnasio/reporte.html', {
        'totales': totales,
        'clientes': clientes,
        'por_estado': por_estado
    })

# =========================
# LAB 07 - EJERCICIO 11
# REPORTES DE PAGOS Y CLASES (investigación propia)
# =========================

from django.db.models import Avg


def reporte_pagos_clases(request):
    # REPORTE 1 (aggregate): totales globales de los pagos.
    resumen_pagos = Pago.objects.aggregate(
        total_cobrado=Sum('monto'),
        pago_promedio=Avg('monto'),
        cantidad=Count('id')
    )

    # REPORTE 2 (annotate): inscritos e ingresos de cada clase.
    clases = Clase.objects.con_ocupacion().order_by('-ingresos')

    # REPORTE 3 (values().annotate()): pagos agrupados por método.
    por_metodo = (
        Pago.objects
        .values('metodo_pago')
        .annotate(cantidad=Count('id'), total=Sum('monto'))
        .order_by('-total')
    )

    return render(request, 'gimnasio/reporte_pagos_clases.html', {
        'resumen_pagos': resumen_pagos,
        'clases': clases,
        'por_metodo': por_metodo
    })