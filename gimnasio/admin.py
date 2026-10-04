from django.contrib import admin

from .models import (
    Cliente,
    Membresia,
    Pago,
    Entrenador,
    Clase,
    PerfilCliente,
    InscripcionClase,
    Ejercicio,
    Sala,
    Asistencia,
    EvaluacionFisica,
    HorarioClase,
    ObjetivoCliente,
    Rutina,
    RutinaEjercicio,
)


# Relación uno a uno: Cliente - PerfilCliente
class PerfilClienteInline(admin.StackedInline):
    model = PerfilCliente
    extra = 1
    max_num = 1


# Relación muchos a muchos mediante InscripcionClase
class InscripcionClaseInline(admin.TabularInline):
    model = InscripcionClase
    extra = 1
    fields = ("clase", "fecha_inscripcion", "estado", "sesiones", "precio_sesion")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "dni", "correo", "telefono")
    search_fields = ("nombre", "dni", "correo")
    inlines = (PerfilClienteInline, InscripcionClaseInline)


@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "especialidad", "telefono")
    search_fields = ("nombre", "especialidad")
    list_filter = ("especialidad",)


@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "horario", "cupos_disponibles", "entrenador", "sala")
    search_fields = ("nombre", "entrenador__nombre")
    list_filter = ("entrenador", "sala")


@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "tipo", "precio", "fecha_inicio", "fecha_fin")
    list_filter = ("tipo",)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "membresia", "monto", "fecha", "metodo_pago")
    list_filter = ("metodo_pago",)


@admin.register(InscripcionClase)
class InscripcionClaseAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "clase", "fecha_inscripcion", "estado", "sesiones", "precio_sesion", "total")
    list_filter = ("estado", "clase")


# Registro simple de los demás modelos
admin.site.register(PerfilCliente)
admin.site.register(Ejercicio)
admin.site.register(Sala)
admin.site.register(Asistencia)
admin.site.register(EvaluacionFisica)
admin.site.register(HorarioClase)
admin.site.register(ObjetivoCliente)
admin.site.register(Rutina)
admin.site.register(RutinaEjercicio)