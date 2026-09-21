from django.db import models


# =========================================================
# 1. MODELO CLIENTE
# =========================================================
# Guarda la información principal de cada cliente.
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


# =========================================================
# 2. PERFIL DEL CLIENTE
# RELACIÓN 1 A 1
# Cliente 1 ---- 1 PerfilCliente
# =========================================================
# Guarda información complementaria del cliente.
class PerfilCliente(models.Model):
    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    contacto_emergencia = models.CharField(max_length=100)
    telefono_emergencia = models.CharField(max_length=15)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.cliente.nombre}"


# =========================================================
# 3. MODELO MEMBRESÍA
# Cliente 1 ---- N Membresia
# =========================================================
# Registra las membresías adquiridas por los clientes.
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

    def __str__(self):
        return self.tipo


# =========================================================
# 4. MODELO PAGO
# Cliente 1 ---- N Pago
# Membresia 1 ---- N Pago
# =========================================================
# Registra los pagos realizados por los clientes.
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

    def __str__(self):
        return self.nombre


# =========================================================
# 6. MODELO SALA
# Sala 1 ---- N Clase
# =========================================================
# Representa los ambientes físicos del gimnasio.
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

    def __str__(self):
        return self.nombre


# =========================================================
# 8. MODELO INSCRIPCIÓN DE CLASE
# MODELO INTERMEDIO N:M
# Cliente N ---- M Clase
# =========================================================
class InscripcionClase(models.Model):
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
    estado = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.cliente.nombre} - {self.clase.nombre}"


# =========================================================
# 9. MODELO ASISTENCIA
# InscripcionClase 1 ---- N Asistencia
# =========================================================
# Permite controlar la asistencia del cliente a sus clases.
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
# Clase 1 ---- N HorarioClase
# =========================================================
# Permite que una clase pueda tener más de un horario.
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

    def __str__(self):
        return f"{self.clase.nombre} - {self.dia_semana}"


# =========================================================
# 11. MODELO RUTINA
# Cliente 1 ---- N Rutina
# Entrenador 1 - N Rutina
# =========================================================
# Rutina de entrenamiento asignada a un cliente.
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
# Catálogo de ejercicios disponibles.
class Ejercicio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    grupo_muscular = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


# =========================================================
# 13. MODELO RUTINA-EJERCICIO
# MODELO INTERMEDIO N:M
# Rutina N ---- M Ejercicio
# =========================================================
# Guarda los datos específicos de un ejercicio dentro
# de una determinada rutina.
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
# Cliente 1 ---- N EvaluacionFisica
# =========================================================
# Guarda la evolución física de un cliente.
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

    def __str__(self):
        return f"{self.cliente.nombre} - {self.fecha}"


# =========================================================
# 15. MODELO OBJETIVO DEL CLIENTE
# Cliente 1 ---- N ObjetivoCliente
# =========================================================
# Permite registrar objetivos personales de entrenamiento.
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
    estado = models.CharField(max_length=20, default='Activo')

    def __str__(self):
        return f"{self.cliente.nombre} - {self.descripcion}"