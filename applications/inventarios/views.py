import csv
from datetime import datetime
from distutils import archive_util
from applications.ventas.managers import SaleDetailManager
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.db.models import Q
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView,
)
from applications.utils import render_to_pdf
from applications.ventas.models import DetalleVenta
from applications.users.mixins import InventarioPermisionMixin
from django.views.generic import (
    TemplateView,
    ListView,
    View,
    CreateView
)
from .forms import (
    CalzadoFormulario,
    RopaFormulario,
    AccesoriosFormulario,
    ArchivoForm
)
from .models import (
    Productos,
    Marca,
    Proveedor,
    ArchivoSubido
)

""" **************************************** REGISTROS **************************************** """

"""
    ********************        ********************
                         MARCAS
    ********************        ********************
"""

class IndexMarca(InventarioPermisionMixin, ListView):
    template_name = 'inventarios/registros/marcas/index_marcas.html'
    model = Marca
    context_object_name = 'marcas'

class CrearMarcaVista(InventarioPermisionMixin, View):
    def get(self, request):
        nombre1 = request.GET.get('nombre', None)
        obj = Marca.objects.create(nombre = nombre1)
        marca = {'id':obj.id,'nombre':obj.nombre}
        data = {'marca': marca}

        return JsonResponse(data)

class ActualizarMarcaVista(InventarioPermisionMixin, View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        nombre1 = request.GET.get('nombre', None)
        obj = Marca.objects.get(id=id1)
        obj.nombre = nombre1
        obj.save()
        marca = {'id':obj.id,'nombre':obj.nombre}
        data = {'marca': marca}

        return JsonResponse(data)

class EliminarMarcaVista(InventarioPermisionMixin, View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Marca.objects.get(id=id1).delete()
        data = {'deleted': True}

        return JsonResponse(data)

"""
    ********************            ********************
                         PROVEEDORES
    ********************            ********************
"""

class IndexProveedor(InventarioPermisionMixin, ListView):
    template_name = 'inventarios/registros/proveedores/index_proveedores.html'
    model = Proveedor
    context_object_name = 'proveedores'

class CrearProveedorVista(InventarioPermisionMixin, View):
    def get(self, request):
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
        data = {'proveedor': proveedor}

        return JsonResponse(data)

class ActualizarProveedorVista(InventarioPermisionMixin, View):
    def get(self, request):
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
        data = {'proveedor': proveedor}

        return JsonResponse(data)

class EliminarProveedorVista(InventarioPermisionMixin, View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Proveedor.objects.get(id=id1).delete()
        data = {'deleted': True}

        return JsonResponse(data)

""" **************************************** INVENTARIO **************************************** """

# Index inventario
class IndexInventario(InventarioPermisionMixin, TemplateView):
    template_name = 'inventarios/a_rchivos_base/a_index_inventarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["calzado_cantidad"] = Productos.objects.calzado_cantidad()
        context["ropa_cantidad"] = Productos.objects.ropa_cantidad()
        context["accesorios_cantidad"] = Productos.objects.accesorios_cantidad()

        return context

""" **************************************** ALMACEN 1 **************************************** """

"""
    ********************        ********************
                        CALZADO
    ********************        ********************
"""

# Index calzado
class IndexCalzado(InventarioPermisionMixin, generic.ListView):
    template_name = 'inventarios/almacen_1/calzado/index_calzado.html'
    paginate_by = 100
    context_object_name = 'producto_calzado'

    def get_queryset(self):
        queryset = Productos.objects.filtros_calzado(
            filtro = self.request.GET.get("filtro", ''),
        )

        return queryset

# Crear producto de calzado
class CrearCalzadoVista(InventarioPermisionMixin, BSModalCreateView):
    template_name = 'inventarios/almacen_1/calzado/accion_crear_calzado.html'
    form_class = CalzadoFormulario
    success_message = '¡Mensaje: El producto fue creado exitosamente!'
    success_url = reverse_lazy('index_calzado')

# Actualizar producto de calzado
class ActualizarCalzadoVista(InventarioPermisionMixin, BSModalUpdateView):
    template_name = 'inventarios/almacen_1/calzado/accion_actualizar_calzado.html'
    model = Productos
    form_class = CalzadoFormulario
    success_message = '¡Mensaje: El producto fue actualizado exitosamente!'
    success_url = reverse_lazy('index_calzado')

# Eliminar producto de calzado
class EliminarCalzadoVista(InventarioPermisionMixin, BSModalDeleteView):
    template_name = 'inventarios/almacen_1/calzado/accion_eliminar_calzado.html'
    model = Productos
    success_message = '¡Mensaje: El producto fue eliminado exitosamente!'
    success_url = reverse_lazy('index_calzado')

# Ver registro completo del producto calzado
class LeerCalzadoVista(InventarioPermisionMixin, BSModalReadView):
    template_name = 'inventarios/almacen_1/calzado/accion_leer_calzado.html'
    model = Productos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ventas_del_mes'] = DetalleVenta.objects.ventas_mes_producto(
            self.kwargs['pk']
        )

        return context

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

# Exportar inventario de calzado completo
def export_calzado_csv(request):
    fecha_hoy = datetime.now()
    dia = fecha_hoy.day
    mes = fecha_hoy.month
    ano = fecha_hoy.year
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inventario calzado completo ({dia}-{mes}-{ano}).csv"'

    writer = csv.writer(response)
    writer.writerow(['Barcode', 'Proveedor', 'Marca', 'Modelo', 'Linea', 'Sublinea', 'Color', 'Talla', 'Existencias', 'Precio Costo', 'Precio Venta'])

    calzado = Productos.objects.filter(tipo='100')
    for c in calzado:
        writer.writerow([c.barcode, c.proveedor, c.marca,  c.modelo, c.get_genero_display(), c.get_linea_c_display(), c.get_color_display(), c.get_medida_display(), c.stock, c.precio_compra, c.precio_venta,])

    return response

# Exportar inventario de calzado con stock
def export_calzado_csv_stock(request):
    fecha_hoy = datetime.now()
    dia = fecha_hoy.day
    mes = fecha_hoy.month
    ano = fecha_hoy.year
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inventario calzado con stock ({dia}-{mes}-{ano}).csv"'

    writer = csv.writer(response)
    writer.writerow(['Barcode', 'Proveedor', 'Marca', 'Modelo', 'Linea', 'Sublinea', 'Color', 'Talla', 'Existencias', 'Precio Costo', 'Precio Venta'])

    calzado = Productos.objects.filter(tipo='100', stock__gt=0)
    for c in calzado:
        writer.writerow([c.barcode, c.proveedor, c.marca,  c.modelo, c.get_genero_display(), c.get_linea_c_display(), c.get_color_display(), c.get_medida_display(), c.stock, c.precio_compra, c.precio_venta,])

    return response

"""
    ********************    ********************
                        ROPA
    ********************    ********************

"""

# Index ropa
class IndexRopa(InventarioPermisionMixin, generic.ListView):
    template_name = 'inventarios/almacen_1/ropa/index_ropa.html'
    paginate_by = 100
    context_object_name = 'producto_ropa'

    def get_queryset(self):
        queryset = Productos.objects.filtros_ropa(
            filtro = self.request.GET.get("filtro", ''),
        )

        return queryset

# Crear producto de ropa
class CrearRopaVista(InventarioPermisionMixin, BSModalCreateView):
    template_name = 'inventarios/almacen_1/ropa/accion_crear_ropa.html'
    form_class = RopaFormulario
    success_message = '¡Mensaje: El producto fue creado exitosamente!'
    success_url = reverse_lazy('index_ropa')

# Actualizar producto de ropa
class ActualizarRopaVista(InventarioPermisionMixin, BSModalUpdateView):
    template_name = 'inventarios/almacen_1/ropa/accion_actualizar_ropa.html'
    model = Productos
    form_class = RopaFormulario
    success_message = '¡Mensaje: El producto fue actualizado exitosamente!'
    success_url = reverse_lazy('index_ropa')

# Eliminar producto de ropa
class EliminarRopaVista(InventarioPermisionMixin, BSModalDeleteView):
    template_name = 'inventarios/almacen_1/ropa/accion_eliminar_ropa.html'
    model = Productos
    success_message = '¡Mensaje: El producto fue eliminado exitosamente!'
    success_url = reverse_lazy('index_ropa')

# Ver registro completo del producto ropa
class LeerRopaVista(InventarioPermisionMixin, BSModalReadView):
    template_name = 'inventarios/almacen_1/ropa/accion_leer_ropa.html'
    model = Productos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ventas_del_mes'] = DetalleVenta.objects.ventas_mes_producto(
            self.kwargs['pk']
        )

        return context

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

# Exportar inventario de ropa completo
def export_ropa_csv(request):
    fecha_hoy = datetime.now()
    dia = fecha_hoy.day
    mes = fecha_hoy.month
    ano = fecha_hoy.year
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inventario ropa completo ({dia}-{mes}-{ano}).csv"'

    writer = csv.writer(response)
    writer.writerow(['Barcode', 'Proveedor', 'Marca', 'Modelo', 'Linea', 'Sublinea', 'Color', 'Talla', 'Existencias', 'Precio Costo', 'Precio Venta'])

    ropa = Productos.objects.filter(tipo='200')
    for r in ropa:
        writer.writerow([r.barcode, r.proveedor, r.marca,  r.modelo, r.get_genero_display(), r.get_linea_r_display(), r.get_color_display(), r.get_talla_display(), r.stock, r.precio_compra, r.precio_venta,])

    return response

# Exportar inventario de ropa con stock
def export_ropa_csv_stock(request):
    fecha_hoy = datetime.now()
    dia = fecha_hoy.day
    mes = fecha_hoy.month
    ano = fecha_hoy.year
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inventario ropa con stock ({dia}-{mes}-{ano}).csv"'

    writer = csv.writer(response)
    writer.writerow(['Barcode', 'Proveedor', 'Marca', 'Modelo', 'Linea', 'Sublinea', 'Color', 'Talla', 'Existencias', 'Precio Costo', 'Precio Venta'])

    ropa = Productos.objects.filter(tipo='200', stock__gt=0)
    for r in ropa:
        writer.writerow([r.barcode, r.proveedor, r.marca,  r.modelo, r.get_genero_display(), r.get_linea_r_display(), r.get_color_display(), r.get_talla_display(), r.stock, r.precio_compra, r.precio_venta,])

    return response

"""
    ********************          ********************
                        ACCESORIOS
    ********************          ********************

"""

# Index accesorios
class IndexAccesorios(InventarioPermisionMixin, generic.ListView):
    template_name = 'inventarios/almacen_1/accesorios/index_accesorios.html'
    paginate_by = 100
    context_object_name = 'producto_accesorios'

    def get_queryset(self):
        queryset = Productos.objects.filtros_accesorios(
            filtro = self.request.GET.get("filtro", ''),
        )

        return queryset

# Crear producto de accesorios
class CrearAccesoriosVista(InventarioPermisionMixin, BSModalCreateView):
    template_name = 'inventarios/almacen_1/accesorios/accion_crear_accesorios.html'
    form_class = AccesoriosFormulario
    success_message = '¡Mensaje: El producto fue creado exitosamente!'
    success_url = reverse_lazy('index_accesorios')

# Actualizar producto de accesorios
class ActualizarAccesoriosVista(InventarioPermisionMixin, BSModalUpdateView):
    template_name = 'inventarios/almacen_1/accesorios/accion_actualizar_accesorios.html'
    model = Productos
    form_class = AccesoriosFormulario
    success_message = '¡Mensaje: El producto fue actualizado exitosamente!'
    success_url = reverse_lazy('index_accesorios')

# Eliminar producto de accesorios
class EliminarAccesoriosVista(InventarioPermisionMixin, BSModalDeleteView):
    template_name = 'inventarios/almacen_1/accesorios/accion_eliminar_accesorios.html'
    model = Productos
    success_message = '¡Mensaje: El producto fue eliminado exitosamente!'
    success_url = reverse_lazy('index_accesorios')

# Ver registro completo del producto accesorios
class LeerAccesoriosVista(InventarioPermisionMixin, BSModalReadView):
    template_name = 'inventarios/almacen_1/accesorios/accion_leer_accesorios.html'
    model = Productos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ventas_del_mes'] = DetalleVenta.objects.ventas_mes_producto(
            self.kwargs['pk']
        )

        return context

# Funcion para llenar registros de la tabla de accesorios
def producto_accesorios(request):
    data = dict()
    if request.method == 'GET':
        producto_accesorios = Productos.objects.all()
        data['table'] = render_to_string(
            'inventarios/almacen_1/accesorios/producto_accesorios_tabla.html',
            {'producto_accesorios': producto_accesorios},
            request=request
        )

        return JsonResponse(data)

# Exportar inventario de accesorios completo
def export_accesorios_csv(request):
    fecha_hoy = datetime.now()
    dia = fecha_hoy.day
    mes = fecha_hoy.month
    ano = fecha_hoy.year
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inventario accesorios completo ({dia}-{mes}-{ano}).csv"'

    writer = csv.writer(response)
    writer.writerow(['Barcode', 'Proveedor', 'Marca', 'Modelo', 'Linea', 'Sublinea', 'Color', 'Talla', 'Existencias', 'Precio Costo', 'Precio Venta'])

    accesorios = Productos.objects.filter(tipo='300')
    for a in accesorios:
        writer.writerow([a.barcode, a.proveedor, a.marca,  a.modelo, a.get_genero_display(), a.get_linea_a_display(), a.get_color_display(), a.get_pieza_display(), a.stock, a.precio_compra, a.precio_venta,])

    return response

# Exportar inventario de accesorios con stock
def export_accesorios_csv_stock(request):
    fecha_hoy = datetime.now()
    dia = fecha_hoy.day
    mes = fecha_hoy.month
    ano = fecha_hoy.year
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inventario accesorios con stock ({dia}-{mes}-{ano}).csv"'

    writer = csv.writer(response)
    writer.writerow(['Barcode', 'Proveedor', 'Marca', 'Modelo', 'Linea', 'Sublinea', 'Color', 'Talla', 'Existencias', 'Precio Costo', 'Precio Venta'])

    accesorios = Productos.objects.filter(tipo='300', stock__gt=0)
    for a in accesorios:
        writer.writerow([a.barcode, a.proveedor, a.marca,  a.modelo, a.get_genero_display(), a.get_linea_a_display(), a.get_color_display(), a.get_pieza_display(), a.stock, a.precio_compra, a.precio_venta,])

    return response


"""
    ********************              ********************
                        SUBIR ARCHIVOS
    ********************              ********************

"""

class SubirArchivo(CreateView):
    template_name = "inventarios/almacen_1/subir/crear_archivo.html"
    model = ArchivoSubido
    form_class = ArchivoForm
    success_url = '.'

    def form_valid(self, form):
        form.save()
        return super(SubirArchivo, self).form_valid(form)


class ListarArchivo(ListView):
    template_name = 'inventarios/almacen_1/subir/listar_archivo.html'
    model = ArchivoSubido
    context_object_name = "archivo"


class SubirArchivoInventario(View):
    def get(self, request, *args, **kwargs):
        archivo = ArchivoSubido.objects.get(id=self.kwargs['pk'])
        importar(request, archivo)
        
        return HttpResponseRedirect(reverse_lazy('lista_archivos'))


def importar(request, file):
    # Marca
    if file.tipo == '1':
        lista = []
        with open(f"http://165.227.76.32/media/{file}", "r") as archivo:
            info = list(csv.reader(archivo, delimiter=","))
            for posicion in info[1:]:
                lista.append(Marca(id=posicion[0],nombre=posicion[1],))

        if len(lista) > 0:
            Marca.objects.bulk_create(lista)

    # Accesorios
    if file.tipo == '3':
        lista = []
        with open(f"http://165.227.76.32/media/{file}", "r") as archivo:
            info = list(csv.reader(archivo, delimiter=","))
            for posicion in info[1:]:
                lista.append(Productos(
                    id=posicion[0],barcode=posicion[1],nombre=posicion[2],
                    marca=Marca.objects.get(id=posicion[3]),proveedor=Proveedor.objects.get(id=posicion[4]),
                    tipo=posicion[5],almacen=posicion[6],pieza=posicion[7],linea_a=posicion[8],color=posicion[9],
                    genero=posicion[10],promocion=posicion[11],modelo=posicion[12],stock=posicion[13],
                    precio_compra=posicion[14],precio_venta=posicion[15],num_venta=posicion[16],
                    )
                )
        if len(lista) > 0:
            Productos.objects.bulk_create(lista)


    # Calzado
    if file.tipo == '4':
        lista = []
        with open(f"http://165.227.76.32/media/{file}", "r") as archivo:
            info = list(csv.reader(archivo, delimiter=","))
            for posicion in info[1:]:
                lista.append(Productos(
                    id=posicion[0],barcode=posicion[1],nombre=posicion[2],
                    marca=Marca.objects.get(id=posicion[3]),proveedor=Proveedor.objects.get(id=posicion[4]),
                    tipo=posicion[5],almacen=posicion[6],medida=posicion[7],linea_c=posicion[8],color=posicion[9],
                    genero=posicion[10],promocion=posicion[11],modelo=posicion[12],stock=posicion[13],
                    precio_compra=posicion[14],precio_venta=posicion[15],num_venta=posicion[16],
                    )
                )
        if len(lista) > 0:
            Productos.objects.bulk_create(lista)


    # Ropa
    if file.tipo == '5':
        lista = []
        with open(f"http://165.227.76.32/media/{file}", "r") as archivo:
            info = list(csv.reader(archivo, delimiter=","))
            for posicion in info[1:]:
                lista.append(Productos(
                    id=posicion[0],barcode=posicion[1],nombre=posicion[2],
                    marca=Marca.objects.get(id=posicion[3]),proveedor=Proveedor.objects.get(id=posicion[4]),
                    tipo=posicion[5],almacen=posicion[6],talla=posicion[7],linea_r=posicion[8],color=posicion[9],
                    genero=posicion[10],promocion=posicion[11],modelo=posicion[12],stock=posicion[13],
                    precio_compra=posicion[14],precio_venta=posicion[15],num_venta=posicion[16],
                    )
                )
        if len(lista) > 0:
            Productos.objects.bulk_create(lista)


""" **************************************** ALMACEN 2 **************************************** """