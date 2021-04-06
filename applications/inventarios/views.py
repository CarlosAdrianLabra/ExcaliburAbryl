from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Import
from .models import Productos
from .forms import NProductos

# Create your views here.
class NuevoProducto(CreateView):
    template_name = "inventarios/productos/registrar-nuevo-producto.html"
    model = Productos
    form_class = NProductos

    success_url = reverse_lazy('inventarios_app:rnp')