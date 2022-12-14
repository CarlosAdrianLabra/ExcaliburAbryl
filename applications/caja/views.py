from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    View,
    TemplateView
    )
#
from applications.ventas.models import Venta, DetalleVenta
#
from .models import CerrarCaja
from .functions import detalle_ventas_no_cerradas, detalle_ventas_no_cerradas_2
from applications.users.mixins import PuntodeventaPermisoMixin

# Create your views here.
class ReporteCierreCajaView(PuntodeventaPermisoMixin,TemplateView):
    template_name = 'caja/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ventas = Venta.objects.ventas_no_cerradas()
        context["ventas_dia"] = detalle_ventas_no_cerradas().order_by('-id')
        context['detalle'] = DetalleVenta.objects.filter(sale__id__in=ventas)
        context["total_vendido"] = Venta.objects.total_ventas_dia()
        context["total_anulado"] = Venta.objects.total_ventas_anuladas_dia()
        context["num_ventas_hoy"] = Venta.objects.ventas_no_cerradas().count()
        return context


class ProcesoCerrarCajaView(PuntodeventaPermisoMixin,View):

    def post(self, request, *args, **kwargs):
        # cerramos las ventas
        num_cerradas, total = Venta.objects.cerrar_ventas()
        if num_cerradas > 0:
            CerrarCaja.objects.create(
                date_close=timezone.now(),
                count=num_cerradas,
                amount= total,
                user=self.request.user
            )
        
        return HttpResponseRedirect(reverse('caja_app:caja-index'))


class ReporteCierreCaja2View(PuntodeventaPermisoMixin,TemplateView):
    template_name = 'caja/index_caja2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ventas = Venta.objects.ventas_no_cerradas_2()
        context["ventas_dia"] = detalle_ventas_no_cerradas_2().order_by('-id')
        context['detalle'] = DetalleVenta.objects.filter(sale__id__in=ventas)
        context["total_vendido"] = Venta.objects.total_ventas_dia_2()
        context["total_anulado"] = Venta.objects.total_ventas_anuladas_dia_2()
        context["num_ventas_hoy"] = Venta.objects.ventas_no_cerradas_2().count()
        return context


class ProcesoCerrarCaja2View(PuntodeventaPermisoMixin,View):

    def post(self, request, *args, **kwargs):
        # cerramos las ventas
        num_cerradas, total = Venta.objects.cerrar_ventas_2()
        if num_cerradas > 0:
            CerrarCaja.objects.create(
                date_close=timezone.now(),
                count=num_cerradas,
                amount= total,
                user=self.request.user
            )
        
        return HttpResponseRedirect(reverse('caja_app:caja2-index'))