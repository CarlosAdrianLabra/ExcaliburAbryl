from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from .forms import ProductosFormulario
from .models import Productos

# Index Productos
class IndexProductos(generic.ListView):
    template_name = 'inventarios/productos/index_productos.html'
    model = Productos
    paginate_by = 10
    context_object_name = 'productos'

    def get_queryset(self):
        filtro = self.request.GET.get("filtro_nombre", '')
        lista = Productos.objects.filter(
            Q(nombreP__icontains=filtro) | Q(marcaP__icontains=filtro) | Q(modeloP__icontains=filtro)
        )
        return lista


# Crear productos
class ProductosCrearVista(BSModalCreateView):
    template_name = 'inventarios/productos/accion_crear_productos.html'
    form_class = ProductosFormulario
    success_message = '¡El producto fue creado correctamente!'
    success_url = reverse_lazy('index_productos')


# Actualizar productos
class ProductosActualizarVista(BSModalUpdateView):
    template_name = 'inventarios/productos/accion_actualizar_productos.html'
    model = Productos
    form_class = ProductosFormulario
    success_message = '¡El producto fue actualizado correctamente!'
    success_url = reverse_lazy('index_productos')


# Eliminar productos
class ProductosEliminarVista(BSModalDeleteView):
    template_name = 'inventarios/productos/accion_eliminar_productos.html'
    model = Productos
    success_message = '¡El producto fue eliminado correctamente!'
    success_url = reverse_lazy('index_productos')


# Leer productos
class ProductosLeerVista(BSModalReadView):
    template_name = 'inventarios/productos/accion_leer_productos.html'
    model = Productos


# Funcion para llenar registros de la tabla
def producto(request):
    data = dict()
    if request.method == 'GET':
        producto = Productos.objects.all()
        data['table'] = render_to_string(
            'inventarios/productos/productos_tabla.html',
            {'producto': producto},
            request=request
        )
        return JsonResponse(data)