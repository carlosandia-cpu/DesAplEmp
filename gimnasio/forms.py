from django import forms
from .models import Cliente, Membresia, Pago, Entrenador, Clase, InscripcionClase, PerfilCliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'


class MembresiaForm(forms.ModelForm):
    class Meta:
        model = Membresia
        fields = '__all__'


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'


class EntrenadorForm(forms.ModelForm):
    class Meta:
        model = Entrenador
        fields = '__all__'


class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = '__all__'


# =========================
# FORMULARIO DE INSCRIPCIONES
# =========================

class InscripcionClaseForm(forms.ModelForm):
    class Meta:
        model = InscripcionClase
        fields = [
            'cliente',
            'clase',
            'fecha_inscripcion',
            'estado',
            'sesiones',
            'precio_sesion'
        ]


# =========================
# FORMULARIO DEL PERFIL (RELACIÓN 1 A 1)
# =========================

class PerfilClienteForm(forms.ModelForm):
    class Meta:
        model = PerfilCliente
        fields = ['contacto_emergencia', 'telefono_emergencia', 'observaciones']


# =========================
# LAB 07: FORMULARIO DE LA OPERACIÓN TRANSACCIONAL
# No es ModelForm porque la operación toca varios modelos.
# =========================

class InscribirClienteForm(forms.Form):
    METODOS = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Yape/Plin', 'Yape/Plin'),
    ]

    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())
    clase = forms.ModelChoiceField(queryset=Clase.objects.all())
    sesiones = forms.IntegerField(min_value=1, initial=1)
    precio_sesion = forms.DecimalField(min_value=0, max_digits=8, decimal_places=2)
    metodo_pago = forms.ChoiceField(choices=METODOS)