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
from django.views.generic import (
    TemplateView,
    ListView,
    View
)
from .forms import (
    MarcaFormulario,
    CalzadoFormulario,
    RopaFormulario
)
from .models import (
    Productos,
    Marca,
    Proveedor
)

""" **************************************** REGISTROS **************************************** """

"""
    ********************        ********************
                         MARCAS
    ********************        ********************
"""

class IndexMarca(ListView):
    template_name = 'inventarios/registros/marcas/index_marcas.html'
    model = Marca
    context_object_name = 'marcas'

class CrearMarcaVista(View):
    def  get(self, request):
        nombre1 = request.GET.get('nombre', None)

        obj = Marca.objects.create(
            nombre = nombre1
        )

        marca = {'id':obj.id,'nombre':obj.nombre}

        data = {
            'marca': marca
        }
        return JsonResponse(data)

class ActualizarMarcaVista(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        nombre1 = request.GET.get('nombre', None)

        obj = Marca.objects.get(id=id1)
        obj.nombre = nombre1
        obj.save()

        marca = {'id':obj.id,'nombre':obj.nombre}

        data = {
            'marca': marca
        }
        return JsonResponse(data)

class EliminarMarcaVista(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Marca.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

"""
    ********************            ********************
                         PROVEEDORES
    ********************            ********************
"""

class IndexProveedor(ListView):
    template_name = 'inventarios/registros/proveedores/index_proveedores.html'
    model = Proveedor
    context_object_name = 'proveedores'

class CrearProveedorVista(View):
    def  get(self, request):
        nombre1 = request.GET.get('nombre', None)
        correo1 = request.GET.get('correo', None)
        telefono1 = request.GET.get('telefono', None)
        direccion1 = request.GET.get('direccion', None)
        nombre_benefactor1 = request.GET.get('nombre_benefactor', None)
        nombre_banco1 = request.GET.get('nombre_banco', None)
        clabe1 = request.GET.get('clabe', None)

        obj = Proveedor.objects.create(
            nombre = nombre1,
            correo = correo1,
            telefono = telefono1,
            direccion = direccion1,
            nombre_benefactor = nombre_benefactor1,
            nombre_banco = nombre_banco1,
            clabe = clabe1
        )

        proveedor = {
            'id':obj.id,'nombre':obj.nombre,'correo':obj.correo,'telefono':obj.telefono,'direccion':obj.direccion,
            'nombre_benefactor':obj.nombre_benefactor,'nombre_banco':obj.nombre_banco,'clabe':obj.clabe
        }

        data = {
            'proveedor': proveedor
        }
        return JsonResponse(data)

class ActualizarProveedorVista(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        nombre1 = request.GET.get('nombre', None)
        correo1 = request.GET.get('correo', None)
        telefono1 = request.GET.get('telefono', None)
        direccion1 = request.GET.get('direccion', None)
        nombre_benefactor1 = request.GET.get('nombre_benefactor', None)
        nombre_banco1 = request.GET.get('nombre_banco', None)
        clabe1 = request.GET.get('clabe', None)

        obj = Proveedor.objects.get(id=id1)
        obj.nombre = nombre1
        obj.correo = correo1
        obj.telefono = telefono1
        obj.direccion = direccion1
        obj.nombre_benefactor = nombre_benefactor1
        obj.nombre_banco = nombre_banco1
        obj.clabe = clabe1
        obj.save()

        proveedor = {
            'id':obj.id,'nombre':obj.nombre,'correo':obj.correo,'telefono':obj.telefono,'direccion':obj.direccion,
            'nombre_benefactor':obj.nombre_benefactor,'nombre_banco':obj.nombre_banco,'clabe':obj.clabe
        }

        data = {
            'proveedor': proveedor
        }
        return JsonResponse(data)

class EliminarProveedorVista(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Proveedor.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

""" **************************************** INVENTARIO **************************************** """

# Index inventario
class IndexInventario(TemplateView):
    template_name = 'inventarios/a_rchivos_base/a_index_inventarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """
        # Calzado contadores
        context["calzado_por_terminarse"] = Productos.objects.calzado_por_terminarse().count()
        context["calzado_mas_vendido"] = Productos.objects.calzado_mas_vendido().count()
        context["calzado_promedio"] = Productos.objects.calzado_promedio()
        # Calzado tablas
        context["tabla_calzado_por_terminarse"] = Productos.objects.calzado_por_terminarse()
        context["tabla_calzado_mas_vendido"] = Productos.objects.calzado_mas_vendido()
        
        # Ropa contadores
        context["ropa_por_terminarse"] = Productos.objects.ropa_por_terminarse().count()
        context["ropa_mas_vendida"] = Productos.objects.ropa_mas_vendida().count()
        context["ropa_promedio"] = Productos.objects.ropa_promedio()
        # Calzado tablas
        context["tabla_ropa_por_terminarse"] = Productos.objects.ropa_por_terminarse()
        context["tabla_ropa_mas_vendida"] = Productos.objects.ropa_mas_vendida()
        """

        return context

""" **************************************** ALMACEN 1 **************************************** """

"""
    ********************        ********************
                        CALZADO
    ********************        ********************
"""

# Index calzado
class IndexCalzado(generic.ListView):
    template_name = 'inventarios/almacen_1/calzado/index_calzado.html'
    paginate_by = 10
    context_object_name = 'producto_calzado'

    def get_queryset(self):
        qs = self.request.GET.get("filtro", '')
        return Productos.objects.almacen_tipo_calzado(qs)

# Crear producto de calzado
class CrearCalzadoVista(BSModalCreateView):
    template_name = 'inventarios/almacen_1/calzado/accion_crear_calzado.html'
    form_class = CalzadoFormulario
    success_message = '¡Mensaje: El producto fue creado exitosamente!'
    success_url = reverse_lazy('index_calzado')

# Actualizar producto de calzado
class ActualizarCalzadoVista(BSModalUpdateView):
    template_name = 'inventarios/almacen_1/calzado/accion_actualizar_calzado.html'
    model = Productos
    form_class = CalzadoFormulario
    success_message = '¡Mensaje: El producto fue actualizado exitosamente!'
    success_url = reverse_lazy('index_calzado')

# Eliminar producto de calzado
class EliminarCalzadoVista(BSModalDeleteView):
    template_name = 'inventarios/almacen_1/calzado/accion_eliminar_calzado.html'
    model = Productos
    success_message = '¡Mensaje: El producto fue eliminado exitosamente!'
    success_url = reverse_lazy('index_calzado')

# Ver registro completo del producto calzado
class LeerCalzadoVista(BSModalReadView):
    template_name = 'inventarios/almacen_1/calzado/accion_leer_calzado.html'
    model = Productos

# Funcion para llenar registros de la tabla de calzado
def producto_calzado(request):
    data = dict()
    if request.method == 'GET':
        producto_calzado = Productos.objects.all()
        data['table'] = render_to_string(
            'inventarios/almacen_1/calzado/producto_calzado_tabla.html',
            {'producto_calzado': producto_calzado},
            request=request
        )
        return JsonResponse(data)

"""
    ********************    ********************
                        ROPA
    ********************    ********************

"""

# Index ropa
class IndexRopa(generic.ListView):
    template_name = 'inventarios/almacen_1/ropa/index_ropa.html'
    paginate_by = 10
    context_object_name = 'producto_ropa'

    def get_queryset(self):
        qs = self.request.GET.get("filtro", '')
        return Productos.objects.almacen_tipo_ropa(qs)

# Crear producto de ropa
class CrearRopaVista(BSModalCreateView):
    template_name = 'inventarios/almacen_1/ropa/accion_crear_ropa.html'
    form_class = RopaFormulario
    success_message = '¡Mensaje: El producto fue creado exitosamente!'
    success_url = reverse_lazy('index_ropa')

# Actualizar producto de ropa
class ActualizarRopaVista(BSModalUpdateView):
    template_name = 'inventarios/almacen_1/ropa/accion_actualizar_ropa.html'
    model = Productos
    form_class = RopaFormulario
    success_message = '¡Mensaje: El producto fue actualizado exitosamente!'
    success_url = reverse_lazy('index_ropa')

# Eliminar producto de ropa
class EliminarRopaVista(BSModalDeleteView):
    template_name = 'inventarios/almacen_1/ropa/accion_eliminar_ropa.html'
    model = Productos
    success_message = '¡Mensaje: El producto fue eliminado exitosamente!'
    success_url = reverse_lazy('index_ropa')

# Ver registro completo del producto ropa
class LeerRopaVista(BSModalReadView):
    template_name = 'inventarios/almacen_1/ropa/accion_leer_ropa.html'
    model = Productos

# Funcion para llenar registros de la tabla de ropa
def producto_ropa(request):
    data = dict()
    if request.method == 'GET':
        producto_ropa = Productos.objects.all()
        data['table'] = render_to_string(
            'inventarios/almacen_1/ropa/producto_ropa_tabla.html',
            {'producto_ropa': producto_ropa},
            request=request
        )
        return JsonResponse(data)

""" **************************************** ALMACEN 2 **************************************** """