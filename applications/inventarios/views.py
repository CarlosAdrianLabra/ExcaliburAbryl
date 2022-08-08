import csv
from datetime import datetime
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib import messages
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
from applications.codigobarras.models import Etiqueta
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
    ArchivoSubido,
    Color,
    Talla,
    Sublinea
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
    success_message = '¡El producto fue creado exitosamente!'
    success_url = reverse_lazy('index_calzado')

# Actualizar producto de calzado
class ActualizarCalzadoVista(InventarioPermisionMixin, BSModalUpdateView):
    template_name = 'inventarios/almacen_1/calzado/accion_actualizar_calzado.html'
    model = Productos
    form_class = CalzadoFormulario
    success_message = '¡El producto fue actualizado exitosamente!'
    success_url = reverse_lazy('index_calzado')

# Eliminar producto de calzado
class EliminarCalzadoVista(InventarioPermisionMixin, BSModalDeleteView):
    template_name = 'inventarios/almacen_1/calzado/accion_eliminar_calzado.html'
    model = Productos
    success_message = '¡El producto fue eliminado exitosamente!'
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
        writer.writerow([c.barcode, c.proveedor, c.marca,  c.modelo, c.get_genero_display(), c.sublinea, c.color, c.talla, c.stock, c.precio_compra, c.precio_venta,])

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
        writer.writerow([c.barcode, c.proveedor, c.marca,  c.modelo, c.get_genero_display(), c.sublinea, c.color, c.talla, c.stock, c.precio_compra, c.precio_venta,])

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
    success_message = '¡El producto fue creado exitosamente!'
    success_url = reverse_lazy('index_ropa')

# Actualizar producto de ropa
class ActualizarRopaVista(InventarioPermisionMixin, BSModalUpdateView):
    template_name = 'inventarios/almacen_1/ropa/accion_actualizar_ropa.html'
    model = Productos
    form_class = RopaFormulario
    success_message = '¡El producto fue actualizado exitosamente!'
    success_url = reverse_lazy('index_ropa')

# Eliminar producto de ropa
class EliminarRopaVista(InventarioPermisionMixin, BSModalDeleteView):
    template_name = 'inventarios/almacen_1/ropa/accion_eliminar_ropa.html'
    model = Productos
    success_message = '¡El producto fue eliminado exitosamente!'
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
        writer.writerow([r.barcode, r.proveedor, r.marca,  r.modelo, r.get_genero_display(), r.sublinea, r.color, r.talla, r.stock, r.precio_compra, r.precio_venta,])

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
        writer.writerow([r.barcode, r.proveedor, r.marca,  r.modelo, r.get_genero_display(), r.sublinea, r.color, r.talla, r.stock, r.precio_compra, r.precio_venta,])

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
    success_message = '¡El producto fue creado exitosamente!'
    success_url = reverse_lazy('index_accesorios')

# Actualizar producto de accesorios
class ActualizarAccesoriosVista(InventarioPermisionMixin, BSModalUpdateView):
    template_name = 'inventarios/almacen_1/accesorios/accion_actualizar_accesorios.html'
    model = Productos
    form_class = AccesoriosFormulario
    success_message = '¡El producto fue actualizado exitosamente!'
    success_url = reverse_lazy('index_accesorios')

# Eliminar producto de accesorios
class EliminarAccesoriosVista(InventarioPermisionMixin, BSModalDeleteView):
    template_name = 'inventarios/almacen_1/accesorios/accion_eliminar_accesorios.html'
    model = Productos
    success_message = '¡El producto fue eliminado exitosamente!'
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
        writer.writerow([a.barcode, a.proveedor, a.marca,  a.modelo, a.get_genero_display(), a.sublinea, a.color, a.talla, a.stock, a.precio_compra, a.precio_venta,])

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
        writer.writerow([a.barcode, a.proveedor, a.marca,  a.modelo, a.get_genero_display(), a.sublinea, a.color, a.talla, a.stock, a.precio_compra, a.precio_venta,])

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
    success_url = reverse_lazy('lista_archivos')

    def form_valid(self, form):
        form.save()
        return super(SubirArchivo, self).form_valid(form)

class ListarArchivo(ListView):
    template_name = 'inventarios/almacen_1/subir/listar_archivo.html'
    model = ArchivoSubido
    context_object_name = "archivo"

    def get_queryset(self):
        queryset = super(ListarArchivo, self).get_queryset()
        queryset = ArchivoSubido.objects.all().order_by('-id')
        return queryset

class ActualizarArchivo(View):
    def get(self, request, *args, **kwargs):
        archivo = ArchivoSubido.objects.get(id=self.kwargs['pk'])
        actualizar_stock(request, archivo)
        messages.add_message(request, messages.SUCCESS , '¡Cambios realizados exitosamente!', extra_tags='cambios_realizados')
        
        return HttpResponseRedirect(reverse_lazy('lista_archivos'))

class EliminarArchivo(View):
    def post(self, request, *args, **kwargs):
        archivo = ArchivoSubido.objects.get(id=self.kwargs['pk'])
        archivo.delete()
        messages.add_message(request, messages.SUCCESS , '¡Archivo eliminado exitosamente!', extra_tags='eliminar')
        
        return HttpResponseRedirect(reverse_lazy('lista_archivos'))

def actualizar_stock(request, file):
    # Marca
    if file.tipo == '1':
        lista = []
        with open(f'/webapps/excalibur/ExcaliburAbryl/media/{file}', "r") as archivo:
            info = list(csv.reader(archivo, delimiter=","))
            for linea in info[1:]: lista.append(Marca(nombre=linea[1],))
        if len(lista) > 0: Marca.objects.bulk_create(lista)
    
    # Color
    if file.tipo == '6':
        lista = []
        with open(f'/webapps/excalibur/ExcaliburAbryl/media/{file}', "r") as archivo:
            info = list(csv.reader(archivo, delimiter=","))
            for linea in info[1:]: lista.append(Color(nombre=linea[1],))
        if len(lista) > 0: Color.objects.bulk_create(lista)

    # Talla
    if file.tipo == '7':
        lista = []
        with open(f'/webapps/excalibur/ExcaliburAbryl/media/{file}', "r") as archivo:
            info = list(csv.reader(archivo, delimiter=","))
            for linea in info[1:]: lista.append(Talla(nombre=linea[1],))
        if len(lista) > 0: Talla.objects.bulk_create(lista)

    # Sublinea
    if file.tipo == '8':
        lista = []
        with open(f'/webapps/excalibur/ExcaliburAbryl/media/{file}', "r") as archivo:
            info = list(csv.reader(archivo, delimiter=","))
            for linea in info[1:]: lista.append(Sublinea(nombre=linea[1],))
        if len(lista) > 0: Sublinea.objects.bulk_create(lista)

    # Accesorios
    elif file.tipo == '3' and Productos.objects.filter(tipo='300'):
        dic_modelo = {}    
        dic_archivo = {}
        dic_stock = {}
        dic_no_creados = {}
        dic_actualizados = {}
        with open(f'/webapps/excalibur/ExcaliburAbryl/media/{file}', "r") as archivo:
            producto = Productos.objects.all().latest('id')
            barcode = int(producto.barcode)
            renglon_archivo = archivo.readlines()
            lista = []
            lista_update = []
            marcas = []
            for i, renglon in enumerate(renglon_archivo[1:]):
                r = renglon.strip()
                dic_archivo[i] = r
                dic_stock[i] = r
            
            for i in dic_archivo:
                archivo = str(dic_archivo[i]).split(',')
                if str(archivo[0]) not in marcas:
                    marcas.append(archivo[0])
            
            for i in marcas:
                producto = Productos.objects.filter(tipo='300', marca__nombre=i)
                for p in producto:
                    dic_modelo[p.barcode] = str(p.marca)+','+str(p.modelo)+','+str(p.get_genero_display())+','+str(p.sublinea)+','+str(p.color)+','+str(p.talla)+','+str(p.stock)+','+str(p.precio_compra)+','+str(p.precio_venta)+','+str(p.proveedor)

            for i in dic_archivo:
                for j in dic_modelo:
                    modelo = str(dic_modelo[j]).split(',')
                    archivo = str(dic_archivo[i]).split(',')
                    dic_archivo.update({i: str(archivo[0])+','+str(archivo[1])+','+str(archivo[2])+','+str(archivo[3])+','+str(archivo[4])+','+str(archivo[5])+','+str(modelo[6])+','+str(modelo[7])+','+str(modelo[8])+','+str(archivo[9])})

                    if str(dic_archivo[i]) == str(dic_modelo[j]):
                        archivo_stock = str(dic_stock[i]).split(',')
                        producto = Productos.objects.get(barcode=j)
                        producto.stock = producto.stock+int(archivo_stock[6])
                        producto.precio_compra = archivo_stock[7]
                        producto.precio_venta = archivo_stock[8]
                        lista_update.append(producto)
                        # Productos.objects.filter(barcode=producto.barcode).update(stock=producto.stock+int(archivo_stock[6]))
                        dic_actualizados[i] = dic_archivo[i]
                        break
                else:
                    dic_no_creados[i] = dic_stock[i]
                    linea = get_datos_accesorios_nuevo(request, dic_no_creados, i)
                    barcode = barcode + 1
                    datos = str(dic_no_creados[i]).split(',')
                    color, created = Color.objects.get_or_create(nombre=datos[4])
                    if created: color.save()
                    talla, created = Talla.objects.get_or_create(nombre=datos[5])
                    if created: talla.save()
                    sublinea, created = Sublinea.objects.get_or_create(nombre=datos[3])
                    if created: sublinea.save()
                    marca, created = Marca.objects.get_or_create(nombre=datos[0])
                    if created: marca.save()
                    proveedor, created = Proveedor.objects.get_or_create(nombre=datos[9])
                    if created: proveedor.save()

                    lista.append(Productos(
                        barcode=barcode,nombre="ACCESORIOS",marca=marca,modelo=datos[1],genero=linea,sublinea=sublinea,
                        color=color,talla=talla,stock=datos[6],precio_compra=datos[7],precio_venta=datos[8],
                        proveedor=proveedor,tipo="300",almacen="1000",promocion="0",num_venta="0",
                        )
                    )
        if len(lista_update) > 0:
            Productos.objects.bulk_update(lista_update, ['precio_venta', 'precio_compra', 'stock'])
        if len(lista) > 0:
            Productos.objects.bulk_create(lista)
        if len(dic_actualizados) > 0:
            producto_actualizado(request, dic_actualizados)
        if len(dic_no_creados) > 0:
            producto_no_encontrado(request, dic_no_creados)

    elif file.tipo == '3':
        lista = []
        dic_archivo = {}
        with open(f'/webapps/excalibur/ExcaliburAbryl/media/{file}', "r") as archivo:
            if Productos.objects.all():
                producto = Productos.objects.all().latest('id')
                barcode = int(producto.barcode)
            else:
                barcode = 1000100000000
            renglon_archivo = archivo.readlines()
            for i, renglon in enumerate(renglon_archivo[1:]):
                r = renglon.strip()
                dic_archivo[i] = r
                barcode = barcode + 1
                linea = get_datos_accesorios_nuevo(request, dic_archivo, i)
                datos = str(dic_archivo[i]).split(',')
                color, created = Color.objects.get_or_create(nombre=datos[4])
                if created: color.save()
                talla, created = Talla.objects.get_or_create(nombre=datos[5])
                if created: talla.save()
                sublinea, created = Sublinea.objects.get_or_create(nombre=datos[3])
                if created: sublinea.save()
                marca, created = Marca.objects.get_or_create(nombre=datos[0])
                if created: marca.save()
                proveedor, created = Proveedor.objects.get_or_create(nombre=datos[9])
                if created: proveedor.save()

                lista.append(Productos(
                    barcode=barcode,nombre="ACCESORIOS",marca=marca,modelo=datos[1],genero=linea,sublinea=sublinea,
                    color=color,talla=talla,stock=datos[6],precio_compra=datos[7],precio_venta=datos[8],num_venta="0",
                    proveedor=proveedor,tipo="300",almacen="1000",promocion="0",
                    )
                )
        if len(lista) > 0:
            Productos.objects.bulk_create(lista)

    # Calzado
    elif file.tipo == '4' and Productos.objects.filter(tipo='100'):
        dic_modelo = {}
        dic_archivo = {}
        dic_stock = {}
        dic_no_creados = {}
        dic_actualizados = {}
        with open(f'/webapps/excalibur/ExcaliburAbryl/media/{file}', "r") as archivo:
            producto = Productos.objects.all().latest('id')
            barcode = int(producto.barcode)
            renglon_archivo = archivo.readlines()
            lista = []
            lista_update = []
            marcas = []
            for i, renglon in enumerate(renglon_archivo[1:]):
                r = renglon.strip()
                dic_archivo[i] = r
                dic_stock[i] = r

            for i in dic_archivo:
                archivo = str(dic_archivo[i]).split(',')
                if str(archivo[0]) not in marcas:
                    marcas.append(archivo[0])
            
            for i in marcas:
                producto = Productos.objects.filter(tipo='100', marca__nombre=i)
                for p in producto:
                    dic_modelo[p.barcode] = str(p.marca)+','+str(p.modelo)+','+str(p.get_genero_display())+','+str(p.sublinea)+','+str(p.color)+','+str(p.talla)+','+str(p.stock)+','+str(p.precio_compra)+','+str(p.precio_venta)+','+str(p.proveedor)

            for i in dic_archivo:
                for j in dic_modelo:
                    modelo = str(dic_modelo[j]).split(',')
                    archivo = str(dic_archivo[i]).split(',')
                    dic_archivo.update({i: str(archivo[0])+','+str(archivo[1])+','+str(archivo[2])+','+str(archivo[3])+','+str(archivo[4])+','+str(archivo[5])+','+str(modelo[6])+','+str(modelo[7])+','+str(modelo[8])+','+str(archivo[9])})

                    if str(dic_archivo[i]) == str(dic_modelo[j]):
                        archivo_stock = str(dic_stock[i]).split(',')
                        producto = Productos.objects.get(barcode=j)
                        producto.stock = producto.stock+int(archivo_stock[6])
                        producto.precio_compra = archivo_stock[7]
                        producto.precio_venta = archivo_stock[8]
                        lista_update.append(producto)
                        dic_actualizados[i] = dic_archivo[i]
                        break
                else:
                    dic_no_creados[i] = dic_stock[i]
                    linea = get_datos_calzado_nuevo(request, dic_no_creados, i)
                    barcode = barcode + 1
                    datos = str(dic_no_creados[i]).split(',')
                    color, created = Color.objects.get_or_create(nombre=datos[4])
                    if created: color.save()
                    talla, created = Talla.objects.get_or_create(nombre=datos[5])
                    if created: talla.save()
                    sublinea, created = Sublinea.objects.get_or_create(nombre=datos[3])
                    if created: sublinea.save()
                    marca, created = Marca.objects.get_or_create(nombre=datos[0])
                    if created: marca.save()
                    proveedor, created = Proveedor.objects.get_or_create(nombre=datos[9])
                    if created: proveedor.save()

                    lista.append(Productos(
                        barcode=barcode,nombre="CALZADO",marca=marca,modelo=datos[1],genero=linea,sublinea=sublinea,
                        color=color,talla=talla,stock=datos[6],precio_compra=datos[7],precio_venta=datos[8],
                        proveedor=proveedor,tipo="100",almacen="1000",promocion="0",num_venta="0",
                        )
                    )
        if len(lista_update) > 0:
            Productos.objects.bulk_update(lista_update, ['precio_venta', 'precio_compra', 'stock'])
        if len(lista) > 0:
            Productos.objects.bulk_create(lista)
        if len(dic_actualizados) > 0:
            producto_actualizado(request, dic_actualizados)
        if len(dic_no_creados) > 0:
            producto_no_encontrado(request, dic_no_creados)

    elif file.tipo == '4':
        lista = []
        dic_archivo = {}
        
        with open(f'/webapps/excalibur/ExcaliburAbryl/media/{file}', "r") as archivo:
            if Productos.objects.all():
                producto = Productos.objects.all().latest('id')
                barcode = int(producto.barcode)
            else:
                barcode = 1000100000000
            renglon_archivo = archivo.readlines()
            for i, renglon in enumerate(renglon_archivo[1:]):
                r = renglon.strip()
                dic_archivo[i] = r
                barcode = barcode + 1
                linea = get_datos_calzado_nuevo(request, dic_archivo, i)
                datos = str(dic_archivo[i]).split(',')
                color, created = Color.objects.get_or_create(nombre=datos[4])
                if created: color.save()
                talla, created = Talla.objects.get_or_create(nombre=datos[5])
                if created: talla.save()
                sublinea, created = Sublinea.objects.get_or_create(nombre=datos[3])
                if created: sublinea.save()
                marca, created = Marca.objects.get_or_create(nombre=datos[0])
                if created: marca.save()
                proveedor, created = Proveedor.objects.get_or_create(nombre=datos[9])
                if created: proveedor.save()

                lista.append(Productos(
                    barcode=barcode,nombre="CALZADO",marca=marca,modelo=datos[1],genero=linea,sublinea=sublinea,
                    color=color,talla=talla,stock=datos[6],precio_compra=datos[7],precio_venta=datos[8],num_venta="0",
                    proveedor=proveedor,tipo="100",almacen="1000",promocion="0",
                    )
                )
        if len(lista) > 0:
            Productos.objects.bulk_create(lista)

    # Ropa
    elif file.tipo == '5' and Productos.objects.filter(tipo='200'):
        dic_modelo = {}    
        dic_archivo = {}
        dic_stock = {}
        dic_no_creados = {}
        dic_actualizados = {}
        with open(f'/webapps/excalibur/ExcaliburAbryl/media/{file}', "r") as archivo:
            producto = Productos.objects.all().latest('id')
            barcode = int(producto.barcode)
            renglon_archivo = archivo.readlines()
            lista = []
            lista_update = []
            marcas = []
            for i, renglon in enumerate(renglon_archivo[1:]):
                r = renglon.strip()
                dic_archivo[i] = r
                dic_stock[i] = r

            for i in dic_archivo:
                archivo = str(dic_archivo[i]).split(',')
                if str(archivo[0]) not in marcas:
                    marcas.append(archivo[0])
            
            for i in marcas:
                producto = Productos.objects.filter(tipo='200', marca__nombre=i)
                for p in producto:
                    dic_modelo[p.barcode] = str(p.marca)+','+str(p.modelo)+','+str(p.get_genero_display())+','+str(p.sublinea)+','+str(p.color)+','+str(p.talla)+','+str(p.stock)+','+str(p.precio_compra)+','+str(p.precio_venta)+','+str(p.proveedor)

            for i in dic_archivo:
                for j in dic_modelo:
                    modelo = str(dic_modelo[j]).split(',')
                    archivo = str(dic_archivo[i]).split(',')
                    dic_archivo.update({i: str(archivo[0])+','+str(archivo[1])+','+str(archivo[2])+','+str(archivo[3])+','+str(archivo[4])+','+str(archivo[5])+','+str(modelo[6])+','+str(modelo[7])+','+str(modelo[8])+','+str(archivo[9])})

                    if str(dic_archivo[i]) == str(dic_modelo[j]):
                        archivo_stock = str(dic_stock[i]).split(',')
                        producto = Productos.objects.get(barcode=j)
                        producto.stock = producto.stock+int(archivo_stock[6])
                        producto.precio_compra = archivo_stock[7]
                        producto.precio_venta = archivo_stock[8]
                        lista_update.append(producto)
                        dic_actualizados[i] = dic_archivo[i]
                        break
                else:
                    dic_no_creados[i] = dic_stock[i]
                    linea = get_datos_ropa_nuevo(request, dic_no_creados, i)
                    barcode = barcode + 1
                    datos = str(dic_no_creados[i]).split(',')
                    color, created = Color.objects.get_or_create(nombre=datos[4])
                    if created: color.save()
                    talla, created = Talla.objects.get_or_create(nombre=datos[5])
                    if created: talla.save()
                    sublinea, created = Sublinea.objects.get_or_create(nombre=datos[3])
                    if created: sublinea.save()
                    marca, created = Marca.objects.get_or_create(nombre=datos[0])
                    if created: marca.save()
                    proveedor, created = Proveedor.objects.get_or_create(nombre=datos[9])
                    if created: proveedor.save()

                    lista.append(Productos(
                        barcode=barcode,nombre="ROPA",marca=marca,modelo=datos[1],genero=linea,sublinea=sublinea,
                        color=color,talla=talla,stock=datos[6],precio_compra=datos[7],precio_venta=datos[8],
                        proveedor=proveedor,tipo="200",almacen="1000",promocion="0",num_venta="0",
                        )
                    )
        if len(lista_update) > 0:
            Productos.objects.bulk_update(lista_update, ['precio_venta', 'precio_compra', 'stock'])
        if len(lista) > 0:
            Productos.objects.bulk_create(lista)
        if len(dic_actualizados) > 0:
            producto_actualizado(request, dic_actualizados)
        if len(dic_no_creados) > 0:
            producto_no_encontrado(request, dic_no_creados)

    elif file.tipo == '5':
        lista = []
        dic_archivo = {}
        with open(f'/webapps/excalibur/ExcaliburAbryl/media/{file}', "r") as archivo:
            if Productos.objects.all():
                producto = Productos.objects.all().latest('id')
                barcode = int(producto.barcode)
            else:
                barcode = 1000100000000
            renglon_archivo = archivo.readlines()
            for i, renglon in enumerate(renglon_archivo[1:]):
                r = renglon.strip()
                dic_archivo[i] = r
                barcode = barcode + 1
                linea = get_datos_ropa_nuevo(request, dic_archivo, i)
                datos = str(dic_archivo[i]).split(',')
                color, created = Color.objects.get_or_create(nombre=datos[4])
                if created: color.save()
                talla, created = Talla.objects.get_or_create(nombre=datos[5])
                if created: talla.save()
                sublinea, created = Sublinea.objects.get_or_create(nombre=datos[3])
                if created: sublinea.save()
                marca, created = Marca.objects.get_or_create(nombre=datos[0])
                if created: marca.save()
                proveedor, created = Proveedor.objects.get_or_create(nombre=datos[9])
                if created: proveedor.save()

                lista.append(Productos(
                    barcode=barcode,nombre="ROPA",marca=marca,modelo=datos[1],genero=linea,sublinea=sublinea,
                    color=color,talla=talla,stock=datos[6],precio_compra=datos[7],precio_venta=datos[8],num_venta="0",
                    proveedor=proveedor,tipo="200",almacen="1000",promocion="0",
                    )
                )
        if len(lista) > 0:
            Productos.objects.bulk_create(lista)

def producto_actualizado(request, dic_actualizados):
    for i in dic_actualizados:
        datos = str(dic_actualizados[i]).split(',')
        archivo = str(datos[0])+' - '+str(datos[1])+' - '+str(datos[2])+' - '+str(datos[3])+' - '+str(datos[4])+' - '+str(datos[5])+' - '+str(datos[6])+' - '+str(datos[7])+' - '+str(datos[8])+' - '+str(datos[9])
        messages.add_message(request, messages.SUCCESS, archivo, extra_tags='actualizados')

def producto_no_encontrado(request, dic_no_creados):
    for i in dic_no_creados:
        datos = str(dic_no_creados[i]).split(',')
        archivo = str(datos[0])+' - '+str(datos[1])+' - '+str(datos[2])+' - '+str(datos[3])+' - '+str(datos[4])+' - '+str(datos[5])+' - '+str(datos[6])+' - '+str(datos[7])+' - '+str(datos[8])+' - '+str(datos[9])
        messages.add_message(request, messages.INFO, archivo, extra_tags='creados')

def get_datos_accesorios_nuevo(request, dic, i):
    dl = {}
    linea = 0
    datos = str(dic[i]).split(',')

    for k, v in Productos.OPCIONES_GENERO:
        dl[k] = v
    for k, v in dl.items():
        if str(datos[2]) == str(dl[k]):
            linea = k
            break

    return linea

def get_datos_calzado_nuevo(request, dic, i):
    dl = {}
    linea = 0
    datos = str(dic[i]).split(',')

    for k, v in Productos.OPCIONES_GENERO:
        dl[k] = v
    for k, v in dl.items():
        if str(datos[2]) == str(dl[k]):
            linea = k
            break

    return linea

def get_datos_ropa_nuevo(request, dic, i):
    dl = {}
    linea = 0
    datos = str(dic[i]).split(',')

    for k, v in Productos.OPCIONES_GENERO:
        dl[k] = v
    for k, v in dl.items():
        if str(datos[2]) == str(dl[k]):
            linea = k
            break

    return linea

class EtiquetasArchivo(View):
    def get(self, request, *args, **kwargs):
        archivo = ArchivoSubido.objects.get(id=self.kwargs['pk'])
        crear_etiquetas(request, archivo)
        messages.add_message(request, messages.SUCCESS , '¡Etiquetas creadas exitosamente!', extra_tags='etiquetas_creadas')
        
        return HttpResponseRedirect(reverse_lazy('lista_archivos'))

def crear_etiquetas(request, file):
    Etiqueta.objects.all().delete()

    # Calzado
    if file.tipo == '4' and Productos.objects.filter(tipo='100'):
        dic_modelo = {}    
        dic_archivo = {}
        dic_stock = {}
        with open(f'D:/proyecto/ExcaliburAbryl/media/{file}', "r") as archivo:
            renglon_archivo = archivo.readlines()
            lista = []
            marcas = []
            for i, renglon in enumerate(renglon_archivo[1:]):
                r = renglon.strip()
                dic_archivo[i] = r
                dic_stock[i] = r
            
            for i in dic_archivo:
                archivo = str(dic_archivo[i]).split(',')
                if str(archivo[0]) not in marcas:
                    marcas.append(archivo[0])
            
            for i in marcas:
                producto = Productos.objects.filter(tipo='100', marca__nombre=i)
                for p in producto:
                    dic_modelo[p.barcode] = str(p.marca)+','+str(p.modelo)+','+str(p.get_genero_display())+','+str(p.sublinea)+','+str(p.color)+','+str(p.talla)+','+str(p.stock)+','+str(p.precio_compra)+','+str(p.precio_venta)+','+str(p.proveedor)

            for i in dic_archivo:
                for j in dic_modelo:
                    modelo = str(dic_modelo[j]).split(',')
                    archivo = str(dic_archivo[i]).split(',')
                    dic_archivo.update({i: str(archivo[0])+','+str(archivo[1])+','+str(archivo[2])+','+str(archivo[3])+','+str(archivo[4])+','+str(archivo[5])+','+str(modelo[6])+','+str(archivo[7])+','+str(archivo[8])+','+str(archivo[9])})

                    if str(dic_archivo[i]) == str(dic_modelo[j]):
                        archivo_stock = str(dic_stock[i]).split(',')
                        producto = Productos.objects.get(barcode=j)
                        modelo = str(dic_modelo[j]).split(',')
                        
                        for r in range(0, int(archivo_stock[6])):
                            lista.append(Etiqueta(
                                barcode=producto.barcode,nombre=producto.nombre,marca=producto.marca.nombre,modelo=producto.modelo,linea=producto.get_genero_display(),
                                sublinea=producto.sublinea.nombre,color=producto.color.nombre,talla=producto.talla.nombre
                                )
                            )

            if len(lista) > 0:
                Etiqueta.objects.bulk_create(lista)
                        
class EtiquetasVista(View):
    def get(self, request, *args, **kwargs):
        productos = Etiqueta.objects.all()
        data = {
            'productos': productos
        }
        pdf = render_to_pdf('codigobarras/codigo.html', data)

        return HttpResponse(pdf, content_type='application/pdf')

""" **************************************** ALMACEN 2 **************************************** """