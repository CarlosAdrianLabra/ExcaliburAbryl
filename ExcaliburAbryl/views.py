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
        # Actualiza ls fecha de promociones
        fecha_hoy = datetime.now()
        fecha_hoy = str(fecha_hoy)
        # 
        if Productos.objects.filter(fecha_final_promocion__lte=fecha_hoy):
            Productos.objects.filter(fecha_final_promocion__lte=fecha_hoy).update(
                promocion='0'
            )
        # Etiquetas inicio de página
        context["num_ventas"] = Venta.objects.ventas_no_cerradas_panel()
        context["monto_ventas"] = Venta.objects.total_ventas_dia()
        context["monto_ventas_mes"] = Venta.objects.monto_ventas_mes()
        context["monto_ventas_anuladas"] = Venta.objects.total_ventas_anuladas_dia()
        # Tabla 1
        context["monto_total_ventas"] = Venta.objects.monto_total_ventas_actual()
        # Monto ventas
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
        # Valores al final de tabla
        context['costo_total'] = Venta.objects.costo_total_actual()
        context["ganancias_totales"] = DetalleVenta.objects.ganancias_totales_actuales()
        # Tabla 2
        context["num_ventas_total"] = Venta.objects.total_ventas_no_cerradas_actual()
        # Numero ventas
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
        # Etiquetas final de página
        context['num_productos'] = Productos.objects.productos_registrados()
        context['productos_por_terminarse'] = Productos.objects.productos_por_terminarse()
        #
        return context
    