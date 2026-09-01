from django.shortcuts import render, redirect
from .models import obtener_productos, agregar_producto
from .forms import ProductoForm

def lista_productos(request):
    productos = obtener_productos()
    return render(request, 'store/lista.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            agregar_producto(
                form.cleaned_data['nombre'],
                form.cleaned_data['precio'],
                form.cleaned_data['stock'],
                form.cleaned_data['categoria'],
            )
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'store/formulario.html', {'form': form})