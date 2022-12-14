from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import View, DeleteView, ListView
from django.views.generic.edit import FormView
from applications.users.mixins import PuntodeventaPermisoMixin, PromocionesPermisoMixin
from applications.ventas.forms import VentaForm, VentaVoucherForm
from .forms import EfectivoFormTezoncoCaja2
from applications.ventas.functions import procesar_venta
from applications.caja.functions import detalle_ventas_no_cerradas_2
from applications.ventas.models import Venta, DetalleVenta
from applications.inventarios.models import Productos
from applications.inventarios.num2word import word
from applications.utils import render_to_pdf
from .models import Carritotezoncocaja2, Efectivotezoncocaja2

# Create your views here.
class Tezoncocaja2view(PuntodeventaPermisoMixin, FormView):
    template_name = "ventas/tezonco/index_caja2.html"
    form_class = VentaForm
    success_url = '.'

    def get_context_data(self, **kwargs):
        fecha_hoy = datetime.now()
        fecha_hoy = str(fecha_hoy)
        if Productos.objects.filter(fecha_final_promocion__lte=fecha_hoy):
            Productos.objects.filter(fecha_final_promocion__lte=fecha_hoy).update(promocion='0')
        #
        context = super().get_context_data(**kwargs)
        context["productos"] = Carritotezoncocaja2.objects.all()
        context["total_cobrar"] = Carritotezoncocaja2.objects.total_cobrar()
        context["cambio"] = Efectivotezoncocaja2.objects.all()
        # Formulario para venta con voucher
        context['form_voucher'] = VentaVoucherForm
        context['form_efectivo'] = EfectivoFormTezoncoCaja2
        return context
    
    def form_valid(self, form):
        barcode = form.cleaned_data['barcode']
        count = form.cleaned_data['count']
        producto = Productos.objects.get(barcode=barcode)
        p_stock = producto.stock
        if p_stock != 0:
            obj, created = Carritotezoncocaja2.objects.get_or_create(
                barcode=barcode,
                defaults={
                    'producto': Productos.objects.get(barcode=barcode),
                    'count': count
                }
            )

            if not created:
                obj.count = obj.count + count
                obj.save()

        else:
            messages.add_message(self.request, messages.INFO, '¡El producto ingresado no cuenta con existencias. Revisar el inventario!')

        return super(Tezoncocaja2view, self).form_valid(form)


class CarShopTezoncocaja2UpdateView(PuntodeventaPermisoMixin, View):

    def post(self, request, *args, **kwargs):
        car = Carritotezoncocaja2.objects.get(id=self.kwargs['pk'])
        if car.count > 1:
            car.count = car.count - 1
            car.save()
        
        return HttpResponseRedirect(reverse('tezoncocaja2_app:caja2'))


class CarShopTezoncocaja2Update2View(PuntodeventaPermisoMixin, View):

    def post(self, request, *args, **kwargs):
        car = Carritotezoncocaja2.objects.get(id=self.kwargs['pk'])
        if car.count > 0:
            car.count = car.count + 1
            car.save()
        
        return HttpResponseRedirect(reverse('tezoncocaja2_app:caja2'))


class CarShopTezoncocaja2DeleteView(PuntodeventaPermisoMixin, DeleteView):
    model = Carritotezoncocaja2
    success_url = reverse_lazy('tezoncocaja2_app:caja2')


class CarShopTezoncocaja2DeleteAll(View):
    
    def post(self, request, *args, **kwargs):
        Carritotezoncocaja2.objects.all().delete()
        Efectivotezoncocaja2.objects.all().delete()
        
        return HttpResponseRedirect(reverse('tezoncocaja2_app:caja2'))


class ProcesoVentaVoucherTezoncoCaja2View(PuntodeventaPermisoMixin, FormView):
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
            caja=2
        )
        
        if venta: 
            return HttpResponseRedirect(reverse('tezoncocaja2_app:venta-voucher_pdf', kwargs={'pk': venta.pk },))
        else:
            return HttpResponseRedirect(reverse('tezoncocaja2_app:caja2'))


class VentaVoucherPdfTezoncoCaja2(PuntodeventaPermisoMixin, View):
    
    def get(self, request, *args, **kwargs):
        venta = Venta.objects.get(id=self.kwargs['pk'])
        variable = detalle_ventas_no_cerradas_2()
        num2word = word(int(venta.amount))
        decimal = str(Decimal(venta.amount) % 1)[2:]
        user = str(request.user.nombres) + ' ' + str(request.user.apellidos)
        efectivo2 = Efectivotezoncocaja2.objects.all()

        data = {
            'venta': venta,
            'detalle_productos': DetalleVenta.objects.filter(sale__id=self.kwargs['pk']),
            'subtotal': variable.filter(id=self.kwargs['pk']),
            'num2word': num2word,
            'decimal': decimal,
            'user': user,
            'efectivo': efectivo2
        }
        pdf = render_to_pdf('ventas/tezonco/voucher_caja2.html', data)

        return HttpResponse(pdf, content_type='application/pdf')


class Efectivotezoncocaja2View(PuntodeventaPermisoMixin, FormView):
    form_class = EfectivoFormTezoncoCaja2
    success_url = '/punto_de_venta/caja/2'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = Carritotezoncocaja2.objects.total_cobrar()
        context["cambio"] = Efectivotezoncocaja2.objects.all()
        return context

    def form_valid(self, form):
        cash = form.cleaned_data['cash']
        monto = Carritotezoncocaja2.objects.total_cobrar()

        obj, created = Efectivotezoncocaja2.objects.get_or_create(
            defaults={
               'cash': cash,
               'change': round(float(cash) - monto,2)
            }
        )

        if not created:
            obj.cash = cash
            obj.change = float(cash) - monto
            obj.save()

        return super(Efectivotezoncocaja2View, self).form_valid(form)


class Efectivotezoncocaja2DeleteAll(PuntodeventaPermisoMixin, View):
    
    def post(self, request, *args, **kwargs):
        Efectivotezoncocaja2.objects.all().delete()
        
        return HttpResponseRedirect(reverse('tezoncocaja2_app:caja2'))


class PromocionFamiliarTezoncoCaja2(PuntodeventaPermisoMixin, View):
    
    def get(self, request, *args, **kwargs):
        end_date = timezone.now()
        fecha_final_promocion = end_date + timedelta(minutes=5)
        promocion_familiar = self.request.GET.get("promocion",)
        producto = Carritotezoncocaja2.objects.all()

        for p in producto:
            producto = p.barcode
            if producto:
                Productos.objects.filter(barcode=producto).update(promocion=promocion_familiar, fecha_final_promocion=fecha_final_promocion)
        
        return HttpResponseRedirect(reverse('tezoncocaja2_app:caja2'))


class VentasListaView(PuntodeventaPermisoMixin, ListView):
    template_name = 'ventas/tezonco/ventas.html'
    paginate_by = 20
    context_object_name = "ventas" 

    def get_queryset(self):
        return Venta.objects.ventas_no_cerradas_2().order_by('-id')


class VentasEliminarView(PuntodeventaPermisoMixin, DeleteView):
    template_name = "ventas/tezonco/delete.html"
    model = Venta
    success_url = reverse_lazy('tezoncocaja2_app:ventas_caja2')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.anulate = True
        self.object.save()
        # Actualizamos el stock y ventas
        DetalleVenta.objects.restablecer_stok_num_ventas(self.object.id)
        success_url = self.get_success_url()

        return HttpResponseRedirect(success_url)