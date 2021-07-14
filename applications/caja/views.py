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
from .functions import detalle_ventas_no_cerradas
# Create your views here.
class ReporteCierreCajaView(TemplateView):

    template_name = 'caja/index.html'

    def get_context_data(self, **kwargs):
        ventas = Venta.objects.ventas_no_cerradas()

        context = super().get_context_data(**kwargs)
        context["ventas_dia"] = detalle_ventas_no_cerradas()
        context['detalle'] = DetalleVenta.objects.filter(sale__id__in=ventas)
        context["total_vendido"] = Venta.objects.total_ventas_dia()
        context["total_anulado"] = Venta.objects.total_ventas_anuladas_dia()
        context["num_ventas_hoy"] = Venta.objects.ventas_no_cerradas().count()
        return context


class ProcesoCerrarCajaView(View):

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
        
        return HttpResponseRedirect(
            reverse(
                'caja_app:caja-index'
            )
        )