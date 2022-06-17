from django.shortcuts import render
from django.contrib import messages
from django.views.generic import (
    TemplateView,
    ListView,
    View,
)
from applications.inventarios.models import Productos
from .models import Etiqueta
from applications.utils import render_to_pdf
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from applications.users.mixins import CodigodebarrasPermisoMixin

# Create your views here.
class codigobarrasview(CodigodebarrasPermisoMixin,ListView):
    template_name = "codigobarras/Tabla_barras.html"
    paginate_by = 100
    context_object_name = 'Barras'
    model= Productos

    def get_queryset(self, *args):
        barcode = str(*args)

        if barcode:
            queryset = Productos.objects.filtros_para_etiqueta(
                filtro = barcode,
            )
        else:
            queryset = Productos.objects.filtros_para_etiqueta(
                filtro = self.request.GET.get("filtro", ''),
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(codigobarrasview, self).get_context_data(**kwargs)
        context['peticion'] = self.request.GET
        context['pros'] = Productos.objects.order_by('modelo')
        return context


# class BarrasPDF(CodigodebarrasPermisoMixin,View):

#     def get(self, request, *args, **kwargs):
#         productos = Productos.objects.get(barcode=self.kwargs['pk'])
#         data = {
#             'productos': productos
#         }
#         pdf = render_to_pdf('codigobarras/codigobarraspdf.html', data)

#         return HttpResponse(pdf, content_type='application/pdf')


class ProductosFiltradosPDFVista(View):

    def get(self, request, *args, **kwargs):
        productos = Etiqueta.objects.all()
        data = {
            'productos': productos
        }
        pdf = render_to_pdf('codigobarras/codigo.html', data)

        return HttpResponse(pdf, content_type='application/pdf')


class AgregarUnoVista(View):

    def get(self, request, *args, **kwargs):
        resultado={}
        cont=0
        productos = Productos.objects.get(barcode=self.kwargs['pk'])
        productos = productos.barcode
        queryset = codigobarrasview.get_queryset(self, productos)
        
        for q in queryset:
            cont += 1
            if q.pieza:
                resultado[cont] = q.barcode, q.nombre, q.marca.nombre, q.modelo, q.get_genero_display(), q.get_linea_a_display(), q.get_pieza_display(), q.get_color_display()
            if q.medida:
                resultado[cont] = q.barcode, q.nombre, q.marca.nombre, q.modelo, q.get_genero_display(), q.get_linea_c_display(), q.get_medida_display(), q.get_color_display()
            if q.talla:
                resultado[cont] = q.barcode, q.nombre, q.marca.nombre, q.modelo, q.get_genero_display(), q.get_linea_r_display(), q.get_talla_display(), q.get_color_display()

        for key in resultado:
            create = Etiqueta.objects.create(
                barcode=resultado[key][0],nombre=resultado[key][1],marca=resultado[key][2],modelo=resultado[key][3],
                linea=resultado[key][4],sublinea=resultado[key][5],talla=resultado[key][6],color=resultado[key][7]
            )
        create.save()

        messages.add_message(self.request, messages.SUCCESS, '¡Se ha agregado el producto a la lista de etiquetas!')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


class EliminarEtiquetaVista(View):
    
    def post(self, request, *args, **kwargs):
        Etiqueta.objects.all().delete()
        messages.add_message(self.request, messages.SUCCESS, '¡Se ha eliminado la lista de etiquetas!')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


# class AgregarTodosVista(View):

#     def post(self, request, *args, **kwargs):
#         resultado={}
#         cont=0

#         queryset = codigobarrasview.get_queryset(self)
#         if request.method == 'POST':
#             for q in queryset:
#                 cont += 1
#                 if q.pieza:
#                     resultado[cont] = q.barcode, q.nombre, q.marca.nombre, q.modelo, q.get_genero_display(), q.get_linea_a_display(), q.get_pieza_display(), q.get_color_display()
#                 if q.medida:
#                     resultado[cont] = q.barcode, q.nombre, q.marca.nombre, q.modelo, q.get_genero_display(), q.get_linea_c_display(), q.get_medida_display(), q.get_color_display()
#                 if q.talla:
#                     resultado[cont] = q.barcode, q.nombre, q.marca.nombre, q.modelo, q.get_genero_display(), q.get_linea_r_display(), q.get_talla_display(), q.get_color_display()

#             for key in resultado:
#                 create = Etiqueta.objects.create(
#                     barcode=resultado[key][0],nombre=resultado[key][1],marca=resultado[key][2],modelo=resultado[key][3],
#                     linea=resultado[key][4],sublinea=resultado[key][5],talla=resultado[key][6],color=resultado[key][7]
#                 )
#                 create.save()

#         return HttpResponseRedirect(reverse('codigobarras_app:codigo_de_barras_index'))