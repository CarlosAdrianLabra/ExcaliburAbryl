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
from applications.utils import render_to_pdf
from .models import Venta, DetalleVenta, Carrito
from .forms import VentaForm, VentaVoucherForm
from .functions import procesar_venta
from applications.caja.functions import detalle_ventas_no_cerradas
# Create your views here.



class AddCarView(FormView):
    template_name = "ventas/index.html"
    form_class = VentaForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos"] = Carrito.objects.all()
        context["total_cobrar"] = Carrito.objects.total_cobrar()
        # formulario para venta con voucher
        context['form_voucher'] = VentaVoucherForm
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


class CarShopUpdateView(View):
    """ quita en 1 la cantidad en un carshop """

    def post(self, request, *args, **kwargs):
        car = Carrito.objects.get(id=self.kwargs['pk'])
        if car.count > 1:
            car.count = car.count - 1
            car.save()
        #
        return HttpResponseRedirect(
            reverse(
                'ventas_app:venta-index'
            )
        )

class CarShopUpdate2View(View):
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

class CarShopDeleteView(DeleteView):
    model = Carrito
    success_url = reverse_lazy('ventas_app:venta-index')

class CarShopDeleteAll(View):
    
    def post(self, request, *args, **kwargs):
        #
        Carrito.objects.all().delete()
        #
        return HttpResponseRedirect(
            reverse(
                'ventas_app:venta-index'
            )
        )


class ProcesoVentaSimpleView(View):
    """ Procesa una venta simple """

    def post(self, request, *args, **kwargs):
        #
        procesar_venta(
            self=self,
            type_invoice=Venta.SIN_COMPROBANTE,
            type_payment=Venta.EFECTIVO,
            user=self.request.user,
        )
        #
        return HttpResponseRedirect(
            reverse(
                'ventas_app:venta-index'
            )
        )


class ProcesoVentaVoucherView(FormView):
    form_class = VentaVoucherForm
    success_url = '.'
    
    def form_valid(self, form):
        type_payment = form.cleaned_data['type_payment']
        type_invoice = form.cleaned_data['type_invoice']
        #
        venta = procesar_venta(
            self=self,
            type_invoice=type_invoice,
            type_payment=type_payment,
            user=self.request.user,
        )
        #
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

class VentaVoucherPdf(View):
    
    def get(self, request, *args, **kwargs):
        venta = Venta.objects.get(id=self.kwargs['pk'])
        variable = detalle_ventas_no_cerradas()
        data = {
            'venta': venta,
            'detalle_productos': DetalleVenta.objects.filter(sale__id=self.kwargs['pk']),
            'subtotal': variable.filter(id=self.kwargs['pk'])
        }
        pdf = render_to_pdf('ventas/voucher.html', data)
        return HttpResponse(pdf, content_type='application/pdf')



class SaleListView(ListView):
    template_name = 'ventas/ventas.html'
    context_object_name = "ventas" 

    def get_queryset(self):
        return Venta.objects.ventas_no_cerradas()


class SaleDeleteView(DeleteView):
    template_name = "ventas/delete.html"
    model = Venta
    success_url = reverse_lazy('ventas_app:venta-index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.save()
        # actualizmos el stok y ventas
        DetalleVenta.objects.restablecer_stok_num_ventas(self.object.id)
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)