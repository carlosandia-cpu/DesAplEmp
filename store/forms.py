from django import forms

class ProductoForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    precio = forms.FloatField(required=True, min_value=0.01)
    stock = forms.IntegerField(required=True, min_value=0)
    categoria = forms.CharField(max_length=50, required=True)