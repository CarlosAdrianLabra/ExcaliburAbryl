from django.shortcuts import render
from django.views.generic import (
    CreateView,
    TemplateView
    )
from django.urls import reverse_lazy

# Import
from .models import Productos
from .forms import NProductos

# Create your views here.
class NuevoProducto(CreateView):
    template_name = "inventarios/productos/registrar-nuevo-producto.html"
    model = Productos
    form_class = NProductos

    success_url = reverse_lazy('inventarios:registro_producto')


class PaginaPrincipal(TemplateView):
    template_name = 'inventarios/productos/principal.html'