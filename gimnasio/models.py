from django.db import models
from django.db.models import Count
from django.utils import timezone


# =========================================================
# LAB 07 - EJERCICIO 7
# QUERYSET PERSONALIZADO PARA LA ENTIDAD PRINCIPAL (CLIENTE)
# Cada método devuelve un QuerySet, por eso se pueden encadenar.
# =========================================================
class ClienteQuerySet(models.QuerySet):

    def con_inscripciones_activas(self):
        # Regla de negocio: clientes con al menos una inscripción 'Activa'.
        return self.filter(inscripciones__estado='Activa').distinct()

    def con_membresia_vigente(self):
        # Regla de negocio: clientes con una membresía que incluye la fecha de hoy.
        hoy = timezone.localdate()
        return self.filter(
            membresias__fecha_inicio__lte=hoy,
            membresias__fecha_fin__gte=hoy
        ).distinct()

    def con_pagos_del_mes(self):
        # Regla de negocio: clientes con pagos registrados en el mes actual.
        hoy = timezone.localdate()
        return self.filter(
            pagos__fecha__year=hoy.year,
            pagos__fecha__month=hoy.month
        ).distinct()

    def con_total_inscripciones(self):
        # Agrega a cada cliente el número de inscripciones que tiene.
        return self.annotate(
            total_inscripciones=Count('inscripciones', distinct=True)
        )
# =========================================================
# LAB 07 - EJERCICIO 12
# QUERYSET PERSONALIZADO PARA CLASE
# =========================================================
from django.db.models import Sum, F, DecimalField


class ClaseQuerySet(models.QuerySet):

    def proximas(self):
        # Regla de negocio: clases cuyo horario aún no ha pasado.
        return self.filter(horario__gte=timezone.now())

    def con_cupos(self):
        # Regla de negocio: clases que todavía tienen cupos libres.
        return self.filter(cupos_disponibles__gt=0)

    def con_ocupacion(self):
        # Agrega a cada clase cuántos inscritos tiene y cuánto ingresa.
        return self.annotate(
            inscritos=Count('inscripciones'),
            ingresos=Sum(
                F('inscripciones__sesiones') * F('inscripciones__precio_sesion'),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )

# =========================================================
# 1. MODELO CLIENTE
# =========================================================
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)

    # as_manager() copia los métodos del QuerySet al manager:
    # Cliente.objects.con_inscripciones_activas() funciona directamente.
    objects = ClienteQuerySet.as_manager()

    def __str__(self):
        return self.nombre


# =========================================================
# 2. PERFIL DEL CLIENTE (RELACIÓN 1 A 1)
# =========================================================
class PerfilCliente(models.Model):
    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    contacto_emergencia = models.CharField(max_length=100)
    telefono_emergencia = models.CharField(max_length=15)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Perfil de cliente'
        verbose_name_plural = 'Perfiles de clientes'

    def __str__(self):
        return f"Perfil de {self.cliente.nombre}"


# =========================================================
# 3. MODELO MEMBRESÍA (Cliente 1 ---- N Membresia)
# =========================================================
class Membresia(models.Model):
    id = models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='membresias',
        null=True,
        blank=True
    )

    tipo = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        verbose_name = 'Membresía'
        verbose_name_plural = 'Membresías'

    def __str__(self):
        return self.tipo


# =========================================================
# 4. MODELO PAGO
# Cliente 1 ---- N Pago
# Membresia 1 ---- N Pago
# =========================================================
class Pago(models.Model):
    id = models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='pagos',
        null=True,
        blank=True
    )

    membresia = models.ForeignKey(
        Membresia,
        on_delete=models.SET_NULL,
        related_name='pagos',
        null=True,
        blank=True
    )

    monto = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateField()
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"S/ {self.monto}"


# =========================================================
# 5. MODELO ENTRENADOR
# =========================================================
class Entrenador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'Entrenador'
        verbose_name_plural = 'Entrenadores'

    def __str__(self):
        return self.nombre


# =========================================================
# 6. MODELO SALA
# =========================================================
class Sala(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    ubicacion = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.nombre


# =========================================================
# 7. MODELO CLASE
# Entrenador 1 ---- N Clase
# Sala 1 --------- N Clase
# Cliente N ------ M Clase
# =========================================================
class Clase(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    horario = models.DateTimeField()

    # Campo entero que se descuenta con F() al inscribir (Lab 07)
    cupos_disponibles = models.PositiveIntegerField(default=20)

    entrenador = models.ForeignKey(
        Entrenador,
        on_delete=models.CASCADE,
        related_name='clases'
    )

    sala = models.ForeignKey(
        Sala,
        on_delete=models.SET_NULL,
        related_name='clases',
        null=True,
        blank=True
    )

    clientes = models.ManyToManyField(
        Cliente,
        through='InscripcionClase',
        related_name='clases_inscritas'
    )
    
    # LAB 07 - EJERCICIO 12: manager con los métodos del QuerySet
    objects = ClaseQuerySet.as_manager()

    def __str__(self):
        return self.nombre


# =========================================================
# 8. MODELO INSCRIPCIÓN DE CLASE (MODELO INTERMEDIO N:M)
# =========================================================
class InscripcionClase(models.Model):
    ESTADOS = [
        ('Activa', 'Activa'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )

    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )

    fecha_inscripcion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Activa')

    # Atributos numéricos del modelo intermedio (Lab 07)
    sesiones = models.PositiveIntegerField(default=1)
    precio_sesion = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'

    @property
    def total(self):
        # Subtotal de la inscripción: sesiones x precio por sesión.
        return self.sesiones * self.precio_sesion

    def __str__(self):
        return f"{self.cliente.nombre} - {self.clase.nombre}"


# =========================================================
# 9. MODELO ASISTENCIA
# =========================================================
class Asistencia(models.Model):
    id = models.AutoField(primary_key=True)

    inscripcion = models.ForeignKey(
        InscripcionClase,
        on_delete=models.CASCADE,
        related_name='asistencias'
    )

    fecha = models.DateField()
    asistio = models.BooleanField(default=False)
    observacion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        estado = "Asistió" if self.asistio else "No asistió"
        return f"{self.inscripcion} - {estado}"


# =========================================================
# 10. MODELO HORARIO DE CLASE
# =========================================================
class HorarioClase(models.Model):
    id = models.AutoField(primary_key=True)

    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name='horarios'
    )

    dia_semana = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        verbose_name = 'Horario de clase'
        verbose_name_plural = 'Horarios de clase'

    def __str__(self):
        return f"{self.clase.nombre} - {self.dia_semana}"


# =========================================================
# 11. MODELO RUTINA
# =========================================================
class Rutina(models.Model):
    id = models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='rutinas'
    )

    entrenador = models.ForeignKey(
        Entrenador,
        on_delete=models.SET_NULL,
        related_name='rutinas_creadas',
        null=True,
        blank=True
    )

    nombre = models.CharField(max_length=100)
    objetivo = models.CharField(max_length=200)
    fecha_creacion = models.DateField()

    def __str__(self):
        return f"{self.nombre} - {self.cliente.nombre}"


# =========================================================
# 12. MODELO EJERCICIO
# =========================================================
class Ejercicio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    grupo_muscular = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


# =========================================================
# 13. MODELO RUTINA-EJERCICIO (MODELO INTERMEDIO N:M)
# =========================================================
class RutinaEjercicio(models.Model):
    rutina = models.ForeignKey(
        Rutina,
        on_delete=models.CASCADE,
        related_name='rutina_ejercicios'
    )

    ejercicio = models.ForeignKey(
        Ejercicio,
        on_delete=models.CASCADE,
        related_name='rutina_ejercicios'
    )

    series = models.PositiveIntegerField(default=3)
    repeticiones = models.PositiveIntegerField(default=10)
    descanso_segundos = models.PositiveIntegerField(default=60)

    class Meta:
        verbose_name = 'Ejercicio de rutina'
        verbose_name_plural = 'Ejercicios de rutina'

    def __str__(self):
        return f"{self.rutina.nombre} - {self.ejercicio.nombre}"


# Agregamos la relación N:M después de declarar el modelo intermedio.
Rutina.add_to_class(
    'ejercicios',
    models.ManyToManyField(
        Ejercicio,
        through='RutinaEjercicio',
        related_name='rutinas'
    )
)


# =========================================================
# 14. MODELO EVALUACIÓN FÍSICA
# =========================================================
class EvaluacionFisica(models.Model):
    id = models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='evaluaciones'
    )

    entrenador = models.ForeignKey(
        Entrenador,
        on_delete=models.SET_NULL,
        related_name='evaluaciones_realizadas',
        null=True,
        blank=True
    )

    fecha = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=4, decimal_places=2)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Evaluación física'
        verbose_name_plural = 'Evaluaciones físicas'

    def __str__(self):
        return f"{self.cliente.nombre} - {self.fecha}"


# =========================================================
# 15. MODELO OBJETIVO DEL CLIENTE
# =========================================================
class ObjetivoCliente(models.Model):
    id = models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='objetivos'
    )

    descripcion = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_meta = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='Activa')

    class Meta:
        verbose_name = 'Objetivo del cliente'
        verbose_name_plural = 'Objetivos de clientes'

    def __str__(self):
        return f"{self.cliente.nombre} - {self.descripcion}"