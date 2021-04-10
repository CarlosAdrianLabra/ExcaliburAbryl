from django.shortcuts import render
from django.views.generic import (
    CreateView,
    ListView,
    TemplateView,
    DetailView,
    UpdateView,
    DeleteView
    )
from django.urls import reverse_lazy

# Import
from .models import Productos
from .forms import NProductos

# Create your views here.
class PaginaPrincipal(TemplateView):
    template_name = 'inventarios/productos/inventario-inicio.html'


class RegistrarProductos(CreateView):
    template_name = "inventarios/productos/accion-registrar-productos.html"
    model = Productos
    form_class = NProductos
    success_url = reverse_lazy('inventarios:inventario_productos')


class InventarioProductos(ListView):
    template_name = 'inventarios/productos/inventario-productos.html'
    paginate_by = 5
    ordering = 'id'
    context_object_name = 'listar_productos'
    #model = Productos

    def get_queryset(self):
        filtro = self.request.GET.get("fnombre", '')
        lista = Productos.objects.filter(
            #nombreP=filtro
            nombreP__icontains=filtro
        )
        return lista


class VisualizarProductos(DetailView):
    template_name = 'inventarios/productos/accion-visualizar-productos.html'
    model = Productos
    
    def get_context_data(self, **kwargs):
        context = super(VisualizarProductos, self).get_context_data(**kwargs)
        return context


class AdministrarProductos(ListView):
    template_name = 'inventarios/productos/inventario-administrar-productos.html'
    paginate_by = 5
    ordering = 'id'
    context_object_name = 'administrar_productos'
    #model = Productos

    def get_queryset(self):
        filtro = self.request.GET.get("fnombre", '')
        lista = Productos.objects.filter(
            #nombreP=filtro
            nombreP__icontains=filtro  
        )
        return lista


class ActualizarProductos(UpdateView):
    template_name = 'inventarios/productos/accion-actualizar-productos.html'
    model = Productos
    fields = [
        'nombreP',
        'marcaP',
        'modeloP',
        'cantidadP',
        'precioP',
        'imagenP',
    ]
    success_url = reverse_lazy('inventarios:administrar_productos')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        return super(ActualizarProductos, self).form_valid(form)
    

class EliminarProductos(DeleteView):
    template_name = 'inventarios/productos/accion-eliminar-productos.html'
    model = Productos
    success_url = reverse_lazy('inventarios:administrar_productos')