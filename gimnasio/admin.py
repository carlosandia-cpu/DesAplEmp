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
    fields = ("clase", "fecha_inscripcion", "estado")


# Primer ModelAdmin
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "dni",
        "correo",
        "telefono",
    )

    search_fields = (
        "nombre",
        "dni",
        "correo",
    )

    inlines = (
        PerfilClienteInline,
        InscripcionClaseInline,
    )


# Segundo ModelAdmin
@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "especialidad",
        "telefono",
    )

    search_fields = (
        "nombre",
        "especialidad",
    )

    list_filter = (
        "especialidad",
    )


# Tercer ModelAdmin
@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "horario",
        "entrenador",
        "sala",
    )

    search_fields = (
        "nombre",
        "entrenador__nombre",
    )

    list_filter = (
        "entrenador",
        "sala",
    )


# Registro simple de los demás modelos
admin.site.register(Membresia)
admin.site.register(Pago)
admin.site.register(PerfilCliente)
admin.site.register(InscripcionClase)
admin.site.register(Ejercicio)
admin.site.register(Sala)
admin.site.register(Asistencia)
admin.site.register(EvaluacionFisica)
admin.site.register(HorarioClase)
admin.site.register(ObjetivoCliente)
admin.site.register(Rutina)
admin.site.register(RutinaEjercicio)