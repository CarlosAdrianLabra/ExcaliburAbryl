from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView
)
from applications.ventas.models import Venta, DetalleVenta
from applications.inventarios.models import Productos
from applications.users.mixins import AdminPermisoMixin
#
from .forms import LiquidacionProviderForm, ResumenVentasForm
#
from .functions import detalle_resumen_ventas




class PanelHomeView(TemplateView):
    template_name = "administracion/index.html"


class PanelAdminView(AdminPermisoMixin, TemplateView):
    template_name = "administracion/administrador.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_ventas"] = Venta.objects.total_ventas_dia()
        context["total_anulaciones"] = Venta.objects.total_ventas_anuladas_dia()
        context["stok_cero"] = Productos.objects.productos_por_terminarse().count()
        context["resumen_semana"] = DetalleVenta.objects.resumen_ventas()[:7]
        return context
    

class ReporteAdmin(ListView):
    template_name = "administracion/reporte_admin.html"
    context_object_name = "resumen_ventas_mes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_ventas"] = Venta.objects.total_ventas()
        return context
    
    def get_queryset(self):
        return DetalleVenta.objects.resumen_ventas_mes()

class ReporteLiquidacion(ListView):
    template_name = "administracion/reporte_liquidacion.html"
    context_object_name = "ventas_liquidacion"
    extra_context = {'form': LiquidacionProviderForm}
    
    def get_queryset(self):
        
        lista_ventas, total_ventas = DetalleVenta.objects.resumen_ventas_proveedor(
            proveedor=self.request.GET.get("proveedor", ''),
            date_start=self.request.GET.get("date_start", ''),
            date_end=self.request.GET.get("date_end", ''),
        )
        self.extra_context.update({'total_ventas': total_ventas})
        return lista_ventas


class ReporteResumenVentas(AdminPermisoMixin, ListView):
    template_name = "administracion/resumen_ventas.html"
    context_object_name = "resumen_ventas"
    extra_context = {'form': ResumenVentasForm}
    
    def get_queryset(self):
        
        lista_ventas = detalle_resumen_ventas(
            self.request.GET.get("date_start", ''),
            self.request.GET.get("date_end", ''),
        )
        return lista_ventas