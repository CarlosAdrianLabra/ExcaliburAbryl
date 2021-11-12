#
from django.urls import path
from . import views

app_name = "administracion_app"

urlpatterns = [
    path(
        'panel/', 
        views.PanelHomeView.as_view(),
        name='index',
    ),
    path(
        'panel/admin/', 
        views.PanelAdminView.as_view(),
        name='index-admin',
    ),
    path(
        'panel/admin-reporte/', 
        views.ReporteAdmin.as_view(),
        name='admin-reporte',
    ),
    path(
        'panel/admin-liquidacion/', 
        views.ReporteLiquidacion.as_view(),
        name='admin-liquidacion',
    ),
    path(
        'panel/admin-resumen-ventas/', 
        views.ReporteResumenVentas.as_view(),
        name='admin-resumen_ventas',
    ),
    path(
        'panel/admin-gastos/', 
        views.GastosListView.as_view(),
        name='admin-gastos',
    ),
    path(
        'panel/detalle-gastos/<pk>/', 
        views.GastosDetailView.as_view(),
        name='detalle-gastos',
    ),
    path(
        'panel/crear-gastos/', 
        views.GastosCreateView.as_view(),
        name='crear-gastos',
    ),
    path(
        'panel/modificar-gastos/<pk>', 
        views.GastosUpdateView.as_view(),
        name='modificar-gastos',
    ),
    path(
        'panel/8020/', 
        views.Informe8020ListView.as_view(),
        name='8020-base',
    ),
    path(
        'panel/reporte/compra_vs_vende/', 
        views.CompravsVende.as_view(),
        name='compra_vende',
    ),
    path(
        'panel/reporte/lista_pedidos/', 
        views.listaPedidos.as_view(), 
        name='comprazapato_lista_pedidos'),

    path(
        'panel/reporte/vista_pedido/<pk>',
        views.vistaZapatoUpdateView.as_view(), 
        name='vista-comprazapato'),
    
    path(
        'panel/reporte/borrar_pedido/<pk>/', 
        views.listaPedidosDeleteView.as_view(),
        name='borrar_pedido'),

]