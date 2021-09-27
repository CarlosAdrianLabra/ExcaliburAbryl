from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    View
)
from django.urls import reverse_lazy, reverse
from applications.ventas.models import Venta, DetalleVenta
from applications.administracion.models import Gastos
from applications.inventarios.models import Productos
from applications.users.mixins import AdminPermisoMixin
#
from .forms import LiquidacionProviderForm, ResumenVentasForm, CompravsVendeFormulario, GastosFormulario
#
from .functions import detalle_resumen_ventas


class PanelHomeView(TemplateView):
    template_name = "administracion/index.html"


class PanelAdminView(AdminPermisoMixin, TemplateView):
    template_name = "administracion/administrador.html"

    def get_context_data(self, **kwargs):
        menos = Productos.objects.filter(stock__lt=10)
        context = super().get_context_data(**kwargs)
        context["total_ventas"] = Venta.objects.total_ventas_dia()
        context["total_anulaciones"] = Venta.objects.total_ventas_anuladas_dia()
        if menos:
            context["stok_cero"] = Productos.objects.productos_por_terminarse().count()
        else:
            context["stok_cero"] = 0
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
    

class GastosListView(ListView):
    model = Gastos
    template_name = "administracion/lista_gastos.html"
    context_object_name = "lista_gastos"

    def get_queryset(self):
        return Gastos.objects.listar_gastos()


class GastosDetailView(DetailView):
    model = Gastos
    template_name = "administracion/detalle_gastos.html"
    context_object_name = "detalle_gastos"


class GastosCreateView(CreateView):
    model = Gastos
    form_class = GastosFormulario
    template_name = "administracion/crear_gasto.html"
    success_url=reverse_lazy('administracion_app:admin-gastos')

    def form_valid(self, form):
        try:
            return super(GastosCreateView, self).form_valid(form)
        except IntegrityError:
            return HttpResponseRedirect(reverse('administracion_app:admin-gastos'))
    

class GastosUpdateView(UpdateView):
    model = Gastos
    form_class = GastosFormulario
    template_name = "administracion/update_gasto.html"
    success_url=reverse_lazy('administracion_app:admin-gastos')
    

class Informe8020ListView(ListView):
    model = DetalleVenta
    template_name = "administracion/8020.html"
    context_object_name='informe_8020'

    def get_queryset(self):
        return DetalleVenta.objects.reporte8020_producto


# class ResultadosView(View):
#     template_name="administracion/resultados.html"
#     context_object_name='resultados'

#     def get_queryset(self):
        
#         return queryset


class CompravsVende(ListView):
    template_name = "administracion/reporte_compravsvende.html"
    context_object_name = "compra_vs_vende"
    extra_context = {'form': CompravsVendeFormulario}
    
    def get_queryset(self):
        
        consulta, total_se_vende, total_costo_vendido, total_se_compra, se_compra = DetalleVenta.objects.compra_vs_vende(
            fecha_inicio=self.request.GET.get("fecha_inicio", ''),
            fecha_fin=self.request.GET.get("fecha_fin", ''),
            proveedor=self.request.GET.get("proveedor", ''),
        )
        self.extra_context.update(
            {'total_se_vende': total_se_vende,
            'total_costo_vendido': total_costo_vendido,
            'total_se_compra': total_se_compra,
            'se_compra': se_compra
            }
        )

        return consulta