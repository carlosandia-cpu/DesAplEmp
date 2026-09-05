from django import forms
from .models import Cliente, Membresia, Pago, Entrenador, Clase


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