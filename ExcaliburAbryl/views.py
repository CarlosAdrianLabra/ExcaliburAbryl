from applications.inventarios.views import producto_calzado
from django.shortcuts import render
from django.views.generic import TemplateView
from applications.inventarios.models import Productos
from applications.ventas.models import Venta

# Create your views here.
class PanelControlInicio(TemplateView):
    template_name = 'panel_control_inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta = Venta.objects.all()
        producto = Productos.objects.filter(stock__lt=10)
        if producto:
            context['productos_por_terminarse'] = Productos.objects.productos_por_terminarse().count()
        else:
            context['productos_por_terminarse'] = 0
        if venta:
            # Inventario
            context['num_productos'] = Productos.objects.all().count()
            # Ventas
            context["num_ventas_total"] = Venta.objects.total_ventas_no_cerradas()
            context["monto_total_ventas"] = Venta.objects.total_ventas()
            # Ventas titulo
            context["num_ventas"] = Venta.objects.ventas_no_cerradas().count()
            context["monto_ventas"] = Venta.objects.total_ventas_dia()
            context["monto_ventas_anuladas"] = Venta.objects.total_ventas_anuladas_dia()
            # Ventas Fecha
            context["ventas_mayo"] = Venta.objects.v_mayo_2021()
            context["ventas_junio"] = Venta.objects.v_junio_2021()
        else:
            context['num_productos'] = 0
            context["num_ventas_total"] = 0
            context["monto_total_ventas"] = 0
            context["num_ventas"] = 0
            context["monto_ventas"] = 0
            context["monto_ventas_anuladas"] = 0
            context["ventas_mayo"] = 0
            context["ventas_junio"] = 0

        return context
    