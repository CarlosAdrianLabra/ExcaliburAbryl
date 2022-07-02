from decimal import Decimal
from django.db import IntegrityError
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
from applications.inventarios.models import Productos
from applications.users.models import User
from applications.inventarios.num2word import word
from applications.utils import render_to_pdf
from applications.ventas.models import Carrito, Venta
from .forms import ApartadosForm, ApartadosUpdateForm
from .models import Apartados
from .functions import pre_apartado, procesar_venta_apartado, cancelar_venta_apartado, eliminar_venta_apartado
from applications.users.mixins import PuntodeventaPermisoMixin

# Create your views here.
class CrearApartado(PuntodeventaPermisoMixin,FormView):
    template_name = 'apartados/index.html'
    form_class = ApartadosForm
    success_url = reverse_lazy('ventas_app:venta-index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos_pos'] = Carrito.objects.all()
        context['total_cobrar'] = Carrito.objects.total_cobrar()

        return context
    
    def form_valid(self, form):
        monto_pagado = form.cleaned_data['monto_pagado']
        
        apartado = pre_apartado(
            self=self,
            monto_pagado=monto_pagado
        )

        if apartado: 
            return HttpResponseRedirect(reverse('apartados_app:apartados_lista'))

        else:
            return HttpResponseRedirect(reverse('ventas_app:venta-index'))


class ApartadosLista(PuntodeventaPermisoMixin,ListView):
    template_name = 'apartados/apartados_lista.html'
    model = Apartados
    context_object_name = "apartados_lista"
    

class ApartadosUpdateView(PuntodeventaPermisoMixin,UpdateView):
    template_name = "apartados/apartados_update.html"
    form_class = ApartadosUpdateForm
    model = Apartados
    success_url=reverse_lazy('apartados_app:apartados_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apartados'] = Apartados.objects.get(id=self.kwargs['pk'])

        return context

    def form_valid(self, form):
        monto_actualizar = form.cleaned_data['monto_actualizar']

        apartados = form.save(commit=False)
        apartados.monto_pagado = float(apartados.monto_pagado) + float(monto_actualizar)
        if apartados.cambio < apartados.precio_producto:
            apartados.cambio = float(apartados.cambio) + float(monto_actualizar)
        if apartados.cambio > apartados.precio_producto:
            apartados.cambio = float(apartados.cambio) - float(apartados.precio_producto)
        apartados.save()

        return super(ApartadosUpdateView, self).form_valid(form)


class ApartadosProcesarVenta(PuntodeventaPermisoMixin,View):

    def post(self, request, *args, **kwargs):
        
        procesar_venta_apartado(
            self=self,
            type_invoice=Venta.APARTADO,
            type_payment=Venta.EFECTIVO,
            user=self.request.user
        )
        
        return HttpResponseRedirect(
            reverse(
                'apartados_app:apartados_lista'
            )
        )


class ApartadosCancelarVenta(PuntodeventaPermisoMixin,View):

    def post(self, request, *args, **kwargs):

        try:
            apartado = Apartados.objects.get(id=kwargs['pk'])
            Carrito.objects.create(
                barcode=apartado.barcode,
                producto=Productos.objects.get(barcode=apartado.barcode),
                count='1'
            )

        except IntegrityError:
            return []
        
        cancelar_venta_apartado(
            self=self,
            type_invoice=Venta.APARTADO_ANULADO,
            type_payment=Venta.EFECTIVO,
            user=self.request.user,
            monto_pagado=apartado.monto_pagado
        )
        
        return HttpResponseRedirect(
            reverse(
                'apartados_app:apartados_lista'
            )
        )


class ApartadosEliminarVenta(PuntodeventaPermisoMixin,DeleteView):
    model = Apartados
    success_url = reverse_lazy('apartados_app:apartados_lista')

    def delete(self, request, *args, **kwargs):

        try:
            apartado = Apartados.objects.get(id=kwargs['pk'])
            Carrito.objects.create(
                barcode=apartado.barcode,
                producto=Productos.objects.get(barcode=apartado.barcode),
                count='1'
            )

        except IntegrityError:
            return []
        
        eliminar_venta_apartado(
            self=self
        )

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        
        return HttpResponseRedirect(success_url)


class ApartadoVoucherPdf(View):
    
    def get(self, request, *args, **kwargs):
        apartado = Apartados.objects.get(id=self.kwargs['pk'])
        producto = Productos.objects.get(barcode=apartado.barcode)
        num2word = word(int(apartado.precio_producto))
        decimal = str(Decimal(apartado.precio_producto) % 1)[2:]
        user = str(request.user.nombres) + ' ' + str(request.user.apellidos)
        efectivo = apartado.monto_pagado

        data = {
            'apartado': apartado,
            'producto': producto,
            'num2word': num2word,
            'decimal': decimal,
            'user': user,
            'efectivo': efectivo
        }
        pdf = render_to_pdf('apartados/voucher.html', data)

        return HttpResponse(pdf, content_type='application/pdf')