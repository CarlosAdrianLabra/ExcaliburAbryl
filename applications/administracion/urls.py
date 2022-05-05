#
from django.urls import path
from . import views

app_name = "administracion_app"

urlpatterns = [
    path(
        'administracion/', 
        views.PanelHomeView.as_view(),
        name='index',
    ),
    path(
        'administracion/ingresos_por_dia/', 
        views.PanelAdminView.as_view(),
        name='index-admin',
    ),
    path(
        'administracion/reportes/ventas_por_mes/', 
        views.ReporteAdmin.as_view(),
        name='admin-reporte',
    ),
    path(
        'administracion/reportes/liquidacion/', 
        views.ReporteLiquidacion.as_view(),
        name='admin-liquidacion',
    ),
    path(
        'administracion/reportes/ventas_por_fecha/', 
        views.ReporteResumenVentas.as_view(),
        name='admin-resumen_ventas',
    ),
    path(
        'administracion/gastos/lista_de_gastos/', 
        views.GastosListView.as_view(),
        name='admin-gastos',
    ),
    path(
        'administracion/gastos/detalle_de_gastos/<pk>/', 
        views.GastosDetailView.as_view(),
        name='detalle-gastos',
    ),
    path(
        'administracion/gastos/registrar_gastos/', 
        views.GastosCreateView.as_view(),
        name='crear-gastos',
    ),
    path(
        'administracion/gastos/editar_gastos/<pk>', 
        views.GastosUpdateView.as_view(),
        name='modificar-gastos',
    ),
    path(
        'administracion/reportes/8020/', 
        views.Informe8020ListView.as_view(),
        name='8020-base',
    ),
    path(
        'administracion/reportes/compra_vs_vende/', 
        views.CompravsVende.as_view(),
        name='compra_vende',
    ),
    path(
        'administracion/reportes/lista_de_pedidos/', 
        views.listaPedidos.as_view(), 
        name='comprazapato_lista_pedidos'),

    path(
        'administracion/reportes/detalle_de_pedido/<pk>',
        views.vistaZapatoUpdateView.as_view(), 
        name='vista-comprazapato'),
    
    path(
        'administracion/reportes/eliminar_pedido/<pk>/', 
        views.listaPedidosDeleteView.as_view(),
        name='borrar_pedido'),

]