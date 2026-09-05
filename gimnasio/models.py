from django.db import models


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


class Membresia(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.tipo


class Pago(models.Model):
    id = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateField()
    metodo_pago = models.CharField(max_length=50)

    def __str__(self):
        return f"S/ {self.monto}"


class Entrenador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


class Clase(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    horario = models.DateTimeField()
    entrenador = models.ForeignKey(
        Entrenador,
        on_delete=models.CASCADE,
        related_name='clases'
    )

    def __str__(self):
        return self.nombre