from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    View,
    DeleteView
)
from django.urls import reverse_lazy, reverse
from applications.ventas.models import Venta, DetalleVenta
from applications.administracion.models import Gastos
from applications.inventarios.models import Movimientos
from applications.comprazapato.models import Pedidos
from applications.users.mixins import AdminPermisoMixin
from applications.comprazapato.forms import pedidosForm
#
from .forms import LiquidacionProviderForm, ResumenVentasForm, CompravsVendeFormulario, GastosFormulario, pedidosadminForm, DetalleCompletoForm
#
from .functions import detalle_resumen_ventas, detalle_completo


class PanelHomeView(AdminPermisoMixin, TemplateView):
    template_name = "administracion/index.html"

# Reportes de ventas - Ultimos 31 días
class PanelAdminView(AdminPermisoMixin, TemplateView):
    template_name = "administracion/administrador.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["total_ventas"] = Venta.objects.total_ventas_por_dia()
        # context["total_anulaciones"] = Venta.objects.total_ventas_anuladas_dia()
        # context["stok_cero"] = Productos.objects.productos_por_terminarse()
        context["resumen_semana"] = DetalleVenta.objects.resumen_ventas()[:31]
        return context

# Reportes de ventas - Mensualmente
class ReporteAdmin(AdminPermisoMixin, ListView):
    template_name = "administracion/reporte_admin.html"
    context_object_name = "resumen_ventas_mes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_ventas"] = Venta.objects.total_ventas()
        return context
    
    def get_queryset(self):
        return DetalleVenta.objects.resumen_ventas_mes()

# Reportes de ventas - Detalle de ventas
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

# Reportes de ventas - Detalle completo
class ReporteDetalleCompleto(AdminPermisoMixin, ListView):
    template_name = "administracion/detalle_completo.html"
    context_object_name = "detalle_completo"
    extra_context = {'form': DetalleCompletoForm}
    
    def get_queryset(self):
        
        lista_ventas = detalle_completo(
            self.request.GET.get("date_start", ''),
            self.request.GET.get("date_end", ''),
            self.request.GET.get("caja", ''),
            self.request.GET.get("tipo", ''),
        )
        return lista_ventas


class ReporteLiquidacion(AdminPermisoMixin, ListView):
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


class GastosListView(AdminPermisoMixin, ListView):
    model = Gastos
    template_name = "administracion/lista_gastos.html"
    context_object_name = "lista_gastos"

    def get_queryset(self):
        return Gastos.objects.listar_gastos()


class GastosDetailView(AdminPermisoMixin, DetailView):
    model = Gastos
    template_name = "administracion/detalle_gastos.html"
    context_object_name = "detalle_gastos"


class GastosCreateView(AdminPermisoMixin, CreateView):
    model = Gastos
    form_class = GastosFormulario
    template_name = "administracion/crear_gasto.html"
    success_url=reverse_lazy('administracion_app:admin-gastos')

    def form_valid(self, form):
        try:
            return super(GastosCreateView, self).form_valid(form)
        except IntegrityError:
            return HttpResponseRedirect(reverse('administracion_app:admin-gastos'))
    

class GastosUpdateView(AdminPermisoMixin, UpdateView):
    model = Gastos
    form_class = GastosFormulario
    template_name = "administracion/update_gasto.html"
    success_url=reverse_lazy('administracion_app:admin-gastos')
    

class Informe8020ListView(AdminPermisoMixin, ListView):
    model = DetalleVenta
    template_name = "administracion/8020.html"
    context_object_name='informe_8020'

    def get_queryset(self):
        f1 = self.request.GET.get("fecha1",'')
        f2 = self.request.GET.get("fecha2",'')
        if f1 and f2:
            return DetalleVenta.objects.reporte8020_producto2(f1,f2)
        else:
            return []


class CompravsVende(AdminPermisoMixin, ListView):
    template_name = "administracion/reporte_compravsvende.html"
    context_object_name = "compra_vs_vende"
    paginate_by = 25
    extra_context = {'form': CompravsVendeFormulario}
    
    def get_queryset(self):
        fecha_inicio = self.request.GET.get("fecha_inicio",''),
        fecha_fin = self.request.GET.get("fecha_fin",''),
        consulta, total_se_vende, total_costo_vendido, stock_comprado, fecha_archivo = DetalleVenta.objects.compra_vs_vende(
            fecha_inicio=self.request.GET.get("fecha_inicio", ''),
            fecha_fin=self.request.GET.get("fecha_fin", ''),
            proveedor=self.request.GET.get("proveedor", ''),
            archivo=self.request.GET.get("archivo", ''),
        )
        self.extra_context.update(
            {'total_se_vende': total_se_vende,
            'total_costo_vendido': total_costo_vendido,
            'stock_comprado': stock_comprado,
            'fecha_archivo': fecha_archivo,
            'fecha_inicio': fecha_inicio[0],
            'fecha_fin': fecha_fin[0],
            }
        )

        return consulta

class listaPedidos(AdminPermisoMixin, ListView):
    template_name = 'administracion/lista_pedidos.html'
    model = Pedidos
    context_object_name = "lista_pedidos"

class vistaZapatoUpdateView(AdminPermisoMixin, UpdateView):
    model = Pedidos
    form_class = pedidosadminForm
    template_name = "administracion/vista_pedidos.html"
    success_url=reverse_lazy('administracion_app:vista-comprazapato')

class listaPedidosDeleteView(AdminPermisoMixin, DeleteView):
    template_name = "administracion/vista_pedidos_delete.html"
    model = Pedidos
    success_url = reverse_lazy('administracion_app:comprazapato_lista_pedidos')