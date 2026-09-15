from django.db import models


# =========================
# MODELO CLIENTE
# =========================
# Guarda la información principal de cada cliente del gimnasio.
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


# =========================
# PERFIL COMPLEMENTARIO DEL CLIENTE
# RELACIÓN 1 A 1
# =========================
# Cada cliente puede tener un solo perfil complementario.
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


# =========================
# MODELO MEMBRESÍA
# =========================
# Guarda los diferentes tipos de membresía del gimnasio.
class Membresia(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.tipo


# =========================
# MODELO PAGO
# =========================
# Guarda la información de los pagos registrados.
class Pago(models.Model):
    id = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateField()
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"S/ {self.monto}"


# =========================
# MODELO ENTRENADOR
# =========================
# Guarda los datos de los entrenadores del gimnasio.
class Entrenador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


# =========================
# MODELO CLASE
# RELACIÓN 1 A MUCHOS
# RELACIÓN MUCHOS A MUCHOS
# =========================
# Un entrenador puede tener varias clases.
# Cada clase pertenece a un solo entrenador.
# Una clase puede tener varios clientes inscritos.
class Clase(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    horario = models.DateTimeField()

    # Relación 1:N con Entrenador
    entrenador = models.ForeignKey(
        Entrenador,
        on_delete=models.CASCADE,
        related_name='clases'
    )

    # Relación N:M con Cliente mediante InscripcionClase
    clientes = models.ManyToManyField(
        Cliente,
        through='InscripcionClase',
        related_name='clases_inscritas'
    )

    def __str__(self):
        return self.nombre

# =========================
# MODELO INSCRIPCIÓN DE CLASE
# MODELO INTERMEDIO N:M
# =========================
# Representa la inscripción de un cliente en una clase.
# Guarda información propia de la relación.
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