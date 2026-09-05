from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm


def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'store/lista.html', {'productos': productos})


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)

        if form.is_valid():
            Producto.objects.create(
                nombre=form.cleaned_data['nombre'],
                precio=form.cleaned_data['precio'],
                stock=form.cleaned_data['stock'],
                categoria=form.cleaned_data['categoria'],
            )

            return redirect('lista_productos')

    else:
        form = ProductoForm()

    return render(request, 'store/formulario.html', {'form': form})