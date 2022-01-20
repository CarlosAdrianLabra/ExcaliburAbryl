from decimal import Decimal
from datetime import datetime, timedelta, date
#
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    View,
    UpdateView,
    DeleteView,
    ListView,
    TemplateView,
)
from django.views.generic.edit import (
    FormView
)
#applicaciones locales
from applications.inventarios.models import Productos
from applications.users.models import User
from applications.inventarios.num2word import word
from applications.utils import render_to_pdf
from .models import Efectivo, Venta, DetalleVenta, Carrito, PreciosFijos
from .forms import EfectivoForm, VentaForm, VentaVoucherForm, PromocionesForm
from .functions import procesar_venta
from applications.caja.functions import detalle_ventas_no_cerradas
from applications.users.mixins import PuntodeventaPermisoMixin, PromocionesPermisoMixin

# Create your views here.
class AddCarView(PuntodeventaPermisoMixin, FormView):
    template_name = "ventas/index.html"
    form_class = VentaForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos"] = Carrito.objects.all()
        context["total_cobrar"] = Carrito.objects.total_cobrar()
        context["cambio"] = Efectivo.objects.all()
        # formulario para venta con voucher
        context['form_voucher'] = VentaVoucherForm
        context['form_efectivo'] = EfectivoForm
        return context
    
    def form_valid(self, form):
        barcode = form.cleaned_data['barcode']
        count = form.cleaned_data['count']
        obj, created = Carrito.objects.get_or_create(
            barcode=barcode,
            defaults={
                'producto': Productos.objects.get(barcode=barcode),
                'count': count
            }
        )
        #
        if not created:
            obj.count = obj.count + count
            obj.save()
        return super(AddCarView, self).form_valid(form)

class CarShopUpdateView(PuntodeventaPermisoMixin, View):
    """ quita en 1 la cantidad en un carshop """

    def post(self, request, *args, **kwargs):
        car = Carrito.objects.get(id=self.kwargs['pk'])
        if car.count > 1:
            car.count = car.count - 1
            car.save()
        
        return HttpResponseRedirect(
            reverse(
                'ventas_app:venta-index'
            )
        )

class CarShopUpdate2View(PuntodeventaPermisoMixin, View):
    """ agrega en 1 la cantidad en un carshop """

    def post(self, request, *args, **kwargs):
        car = Carrito.objects.get(id=self.kwargs['pk'])
        if car.count > 0:
            car.count = car.count + 1
            car.save()
        
        return HttpResponseRedirect(
            reverse(
                'ventas_app:venta-index'
            )
        )

class CarShopDeleteView(PuntodeventaPermisoMixin, DeleteView):
    model = Carrito
    success_url = reverse_lazy('ventas_app:venta-index')

class CarShopDeleteAll(View):
    
    def post(self, request, *args, **kwargs):
        
        Carrito.objects.all().delete()
        Efectivo.objects.all().delete()
        
        return HttpResponseRedirect(
            reverse(
                'ventas_app:venta-index'
            )
        )

class ProcesoVentaSimpleView(PuntodeventaPermisoMixin, View):
    """ Procesa una venta simple """

    def post(self, request, *args, **kwargs):
        
        procesar_venta(
            self=self,
            type_invoice=Venta.SIN_COMPROBANTE,
            type_payment=Venta.EFECTIVO,
            user=self.request.user,
        )
        
        return HttpResponseRedirect(
            reverse(
                'ventas_app:venta-index'
            )
        )

class ProcesoVentaVoucherView(PuntodeventaPermisoMixin, FormView):
    form_class = VentaVoucherForm
    success_url = '.'
    
    def form_valid(self, form):
        type_payment = form.cleaned_data['type_payment']
        type_invoice = form.cleaned_data['type_invoice']
        
        venta = procesar_venta(
            self=self,
            type_invoice=type_invoice,
            type_payment=type_payment,
            user=self.request.user,
        )
        
        if venta: 
            return HttpResponseRedirect(
                reverse(
                    'ventas_app:venta-voucher_pdf',
                    kwargs={'pk': venta.pk },
                )
            )
        else:
            return HttpResponseRedirect(
                reverse(
                    'ventas_app:venta-index'
                )
            )

class VentaVoucherPdf(PuntodeventaPermisoMixin, View):
    
    def get(self, request, *args, **kwargs):
        venta = Venta.objects.get(id=self.kwargs['pk'])
        variable = detalle_ventas_no_cerradas()
        num2word = word(int(venta.amount))
        decimal = str(Decimal(venta.amount) % 1)[2:]
        user = str(User.objects.get(id='1')).upper()
        efectivo = Efectivo.objects.all()

        data = {
            'venta': venta,
            'detalle_productos': DetalleVenta.objects.filter(sale__id=self.kwargs['pk']),
            'subtotal': variable.filter(id=self.kwargs['pk']),
            'num2word': num2word,
            'decimal': decimal,
            'user': user,
            'efectivo': efectivo
        }
        pdf = render_to_pdf('ventas/voucher.html', data)

        return HttpResponse(pdf, content_type='application/pdf')

class SaleListView(PuntodeventaPermisoMixin, ListView):
    template_name = 'ventas/ventas.html'
    context_object_name = "ventas" 

    def get_queryset(self):
        return Venta.objects.ventas_no_cerradas()

class SaleDeleteView(PuntodeventaPermisoMixin, DeleteView):
    template_name = "ventas/delete.html"
    model = Venta
    success_url = reverse_lazy('ventas_app:venta-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.save()
        # actualizmos el stok y ventas
        DetalleVenta.objects.restablecer_stok_num_ventas(self.object.id)
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)

class EfectivoView(PuntodeventaPermisoMixin, FormView):
    form_class = EfectivoForm
    success_url = '/venta/index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = Carrito.objects.total_cobrar()
        context["cambio"] = Efectivo.objects.all()
        return context

    def form_valid(self, form):
        cash = form.cleaned_data['cash']
        monto = Carrito.objects.total_cobrar()

        obj, created = Efectivo.objects.get_or_create(
            defaults={
               'cash': cash,
               'change': round(float(cash) - monto,2)
            }
        )

        if not created:
            obj.cash = cash
            obj.change = float(cash) - monto
            obj.save()

        return super(EfectivoView, self).form_valid(form)

class EfectivoDeleteAll(PuntodeventaPermisoMixin, View):
    
    def post(self, request, *args, **kwargs):
        
        Efectivo.objects.all().delete()
        
        return HttpResponseRedirect(
            reverse(
                'ventas_app:venta-index'
            )
        )

class Promociones(PromocionesPermisoMixin, FormView):
    template_name = 'promociones/index_promociones.html'
    form_class = PromocionesForm
    success_url = reverse_lazy('ventas_app:promociones_activas')

    def form_valid(self, form):
        # fecha_hoy = datetime.now()
        # fecha_hoy = str(fecha_hoy)

        marca = form.cleaned_data['marca']
        genero = form.cleaned_data['genero']
        precio = form.cleaned_data['precio_asignado']
        linea_a = form.cleaned_data['linea_a']
        linea_c = form.cleaned_data['linea_c']
        linea_r = form.cleaned_data['linea_r']
        barcode = form.cleaned_data['barcode']
        barcode_solo = form.cleaned_data['barcode_solo']
        promocion = form.cleaned_data['promocion']
        fecha_final_promocion = form.cleaned_data['fecha_final_promocion']

        # if Productos.objects.filter(fecha_final_promocion__lte=fecha_hoy):
        #     Productos.objects.filter(fecha_final_promocion__lte=fecha_hoy).update(
        #         promocion='0'
        #     )

        #  UN SOLO PRODUCTO
        if barcode_solo != '':
            Productos.objects.filter(barcode=barcode_solo).update(
                promocion=promocion,
                fecha_final_promocion=fecha_final_promocion
            )
        
        #  CREAR DESCUENTO PARA UN PRODUCTO
        if barcode and precio != '':
            Productos.objects.filter(barcode=barcode).update(
                promocion=promocion,
                fecha_final_promocion=fecha_final_promocion
            )
            try:
                producto = PreciosFijos.objects.get(barcode=barcode)
                if producto:
                    PreciosFijos.objects.update(
                        barcode=barcode,
                        precio_fijo=precio,
                        fecha_final_promocion=fecha_final_promocion
                    )
            except PreciosFijos.DoesNotExist:
                PreciosFijos.objects.create(
                    barcode=barcode,
                    precio_fijo=precio,
                    fecha_final_promocion=fecha_final_promocion
                )
        
        # POR MARCA Y LINEA
        # if marca and linea_a != '':
        #     Productos.objects.filter(marca=marca, linea_a=linea_a).update(
        #         promocion=promocion
        #     )
        # if marca and linea_c != '':
        #     Productos.objects.filter(marca=marca, linea_c=linea_c).update(
        #         promocion=promocion
        #     )
        # if marca and linea_r != '':
        #     Productos.objects.filter(marca=marca, linea_r=linea_r).update(
        #         promocion=promocion
        #     )

        # A VARIOS PRODUCTOS
        if genero and marca and linea_a != '':
            Productos.objects.filter(genero=genero, marca=marca, linea_a=linea_a).update(
                promocion=promocion,
                fecha_final_promocion=fecha_final_promocion
            )
        if genero and marca and linea_c != '':
            Productos.objects.filter(genero=genero, marca=marca, linea_c=linea_c).update(
                promocion=promocion,
                fecha_final_promocion=fecha_final_promocion
            )
        if genero and marca and linea_r != '':
            Productos.objects.filter(genero=genero, marca=marca, linea_r=linea_r).update(
                promocion=promocion,
                fecha_final_promocion=fecha_final_promocion
            )

        return super(Promociones, self).form_valid(form)


class ListaPromociones(PromocionesPermisoMixin, ListView):
    template_name = 'promociones/lista_promociones.html'
    model = Productos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["p_activas"] = Productos.objects.promociones_activas()

        return context