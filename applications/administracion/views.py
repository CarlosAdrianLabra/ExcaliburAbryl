from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    View
)
from django.urls import reverse_lazy
from applications.ventas.models import Venta, DetalleVenta
from applications.administracion.models import Gastos
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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     #
    #     context["ventas_calzado"] = Venta.objects.ventas_calzado()
    #     context["ventas_ropa"] = Venta.objects.ventas_ropa()
    #     context["ventas_accesorios"] = Venta.objects.ventas_accesorios()
    #     context["total_de_ventas"] = Venta.objects.total_de_ventas()
    #     #
    #     context["descuentos_calzado"] = Venta.objects.descuentos_calzado()
    #     context["descuentos_ropa"] = Venta.objects.descuentos_ropa()
    #     context["descuentos_accesorios"] = Venta.objects.descuentos_accesorios()
    #     context["total_de_descuentos"] = Venta.objects.total_de_descuentos()
    #     #
    #     context["venta_neta_sistema"] = Venta.objects.venta_neta_sistema()
    #     #
    #     context["costo_ventas_calzado"] = Venta.objects.costo_ventas_calzado()
    #     context["costo_ventas_ropa"] = Venta.objects.costo_ventas_ropa()
    #     context["costo_ventas_accesorios"] = Venta.objects.costo_ventas_accesorios()
    #     context["total_de_costo_ventas"] = Venta.objects.total_de_costo_ventas()
    #     #
    #     return context


class GastosCreateView(CreateView):
    model = Gastos
    template_name = "administracion/crear_gasto.html"
    success_url=reverse_lazy('administracion_app:admin-gastos')
    fields=[
        'mes',
        'año',
        'cargosBancarios',
        'comisionTarjetaCredito',
        'otrosBancos',
        'salariosSueldosWeb',
        'sueldosOficina',
        'sueldosCorporativos',
        'comisionesPagadas',
        'jubilacion',
        'utilidades',
        'costosReclutamiento',
        'imss',
        'rollosImpresora',
        'tapiceria',
        'remodelacionOficina',
        'predial',
        'papeleria',
        'intercomunicador',
        'telefonosOficina',
        'luz',
        'telefono',
        'lentes',
        'fletes',
        'walmart',
        'reparacionesManteminiento',
        'notas',
        'agua',
        'policia',
        'gastosViajes',
        'amplificadorBocinas',
        'gastosCheques',
        'gastosOficina',
        'fideicomiso',
        'contador',
        'cometra',
        'paletas',
        'finiquito',
        'honorariosConsultores',
        'impuestoCDMX',
        'chequesAbril',
        'equipoComputo',
        'mantenimientoComputo',
        'viaticos',
        'comidas',
        'valoracionInmuebles',
        'imprenta',
        'comisionRentaLocal',
        'impuestos',
    ]


class GastosUpdateView(UpdateView):
    model = Gastos
    template_name = "administracion/update_gasto.html"
    fields=[
        'mes',
        'año',
        'cargosBancarios',
        'comisionTarjetaCredito',
        'otrosBancos',
        'salariosSueldosWeb',
        'sueldosOficina',
        'sueldosCorporativos',
        'comisionesPagadas',
        'jubilacion',
        'utilidades',
        'costosReclutamiento',
        'imss',
        'rollosImpresora',
        'tapiceria',
        'remodelacionOficina',
        'predial',
        'papeleria',
        'intercomunicador',
        'telefonosOficina',
        'luz',
        'telefono',
        'lentes',
        'fletes',
        'walmart',
        'reparacionesManteminiento',
        'notas',
        'agua',
        'policia',
        'gastosViajes',
        'amplificadorBocinas',
        'gastosCheques',
        'gastosOficina',
        'fideicomiso',
        'contador',
        'cometra',
        'paletas',
        'finiquito',
        'honorariosConsultores',
        'impuestoCDMX',
        'chequesAbril',
        'equipoComputo',
        'mantenimientoComputo',
        'viaticos',
        'comidas',
        'valoracionInmuebles',
        'imprenta',
        'comisionRentaLocal',
        'impuestos',
    ]
    success_url=reverse_lazy('administracion_app:admin-gastos')
    

class Informe8020ListView(ListView):
    model = DetalleVenta
    template_name = "administracion/8020.html"
    context_object_name='informe_8020'

    def get_queryset(self):
        return DetalleVenta.objects.reporte8020_producto

class ResultadosView(View):
    template_name="administracion/resultados.html"
    context_object_name='resultados'

    def get_queryset(self):
        
        return queryset

