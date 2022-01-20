from datetime import datetime, timedelta, date
from applications.inventarios.views import producto_calzado
from django.shortcuts import render
from django.views.generic import TemplateView
from applications.inventarios.models import Productos
from applications.ventas.models import Venta, DetalleVenta

# Create your views here.
class PanelControlInicio(TemplateView):
    template_name = 'panel_control_inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta = Venta.objects.filter()
        producto = Productos.objects.filter(stock__lt=10)
        #
        fecha_hoy = datetime.now()
        fecha_hoy = str(fecha_hoy)
        #
        if Productos.objects.filter(fecha_final_promocion__lte=fecha_hoy):
            Productos.objects.filter(fecha_final_promocion__lte=fecha_hoy).update(
                promocion='0'
            )
        #
        if producto:
            context['productos_por_terminarse'] = Productos.objects.productos_por_terminarse().count()
        else:
            context['productos_por_terminarse'] = 0
        if venta and Venta.objects.filter(anulate=False):
            # Inventario
            context['num_productos'] = Productos.objects.all().count()
            # Ventas
            context["num_ventas_total"] = Venta.objects.total_ventas_no_cerradas()
            context["monto_total_ventas"] = Venta.objects.monto_total_ventas()
            context["ganancias_totales"] = DetalleVenta.objects.ganancias_totales()
            # Ventas titulo
            context["num_ventas"] = Venta.objects.ventas_no_cerradas().count()
            context["monto_ventas"] = Venta.objects.total_ventas_dia()
            context["monto_ventas_anuladas"] = Venta.objects.total_ventas_anuladas_dia()
            #
            context['costo_total'] = Venta.objects.costo_total()
            # Ventas Fecha
            context["ventas_enero"] = Venta.objects.v_enero()
            context["ventas_febrero"] = Venta.objects.v_febrero()
            context["ventas_marzo"] = Venta.objects.v_marzo()
            context["ventas_abril"] = Venta.objects.v_abril()
            context["ventas_mayo"] = Venta.objects.v_mayo()
            context["ventas_junio"] = Venta.objects.v_junio()
            context["ventas_julio"] = Venta.objects.v_julio()
            context["ventas_agosto"] = Venta.objects.v_agosto()
            context["ventas_septiembre"] = Venta.objects.v_septiembre()
            context["ventas_octubre"] = Venta.objects.v_octubre()
            context["ventas_noviembre"] = Venta.objects.v_noviembre()
            context["ventas_diciembre"] = Venta.objects.v_diciembre()
            #
            context["ventas_enero2"] = Venta.objects.m_enero()
            context["ventas_febrero2"] = Venta.objects.m_febrero()
            context["ventas_marzo2"] = Venta.objects.m_marzo()
            context["ventas_abril2"] = Venta.objects.m_abril()
            context["ventas_mayo2"] = Venta.objects.m_mayo()
            context["ventas_junio2"] = Venta.objects.m_junio()
            context["ventas_julio2"] = Venta.objects.m_julio()
            context["ventas_agosto2"] = Venta.objects.m_agosto()
            context["ventas_septiembre2"] = Venta.objects.m_septiembre()
            context["ventas_octubre2"] = Venta.objects.m_octubre()
            context["ventas_noviembre2"] = Venta.objects.m_noviembre()
            context["ventas_diciembre2"] = Venta.objects.m_diciembre()
            #
            context["monto_ventas_mes"] = Venta.objects.monto_ventas_mes()
        else:
            context['num_productos'] = 0
            #
            context["num_ventas_total"] = 0
            context["monto_total_ventas"] = 0
            context["ganancias_totales"] = 0
            #
            context["num_ventas"] = 0
            context["monto_ventas"] = 0
            context["monto_ventas_anuladas"] = 0
            #
            context["ventas_enero"] = 0
            context["ventas_febrero"] = 0
            context["ventas_marzo"] = 0
            context["ventas_abril"] = 0
            context["ventas_mayo"] = 0
            context["ventas_junio"] = 0
            context["ventas_julio"] = 0
            context["ventas_agosto"] = 0
            context["ventas_septiembre"] = 0
            context["ventas_octubre"] = 0
            context["ventas_noviembre"] = 0
            context["ventas_diciembre"] = 0
            #
            context["ventas_enero2"] = 0
            context["ventas_febrero2"] = 0
            context["ventas_marzo2"] = 0
            context["ventas_abril2"] = 0
            context["ventas_mayo2"] = 0
            context["ventas_junio2"] = 0
            context["ventas_julio2"] = 0
            context["ventas_agosto2"] = 0
            context["ventas_septiembre2"] = 0
            context["ventas_octubre2"] = 0
            context["ventas_noviembre2"] = 0
            context["ventas_diciembre2"] = 0
            #
            context["monto_ventas_mes"] = 0

        return context
    