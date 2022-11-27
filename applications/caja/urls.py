from django.urls import path
from . import views

app_name = "caja_app"

urlpatterns = [
    path(
        'cierre-caja/index/', 
        views.ReporteCierreCajaView.as_view(),
        name='caja-index',
    ),
    path(
        'cierre-caja/cerrar/', 
        views.ProcesoCerrarCajaView.as_view(),
        name='caja-cerrar',
    ),
    path('punto_de_venta/caja/2/cierre_de_caja/', views.ReporteCierreCaja2View.as_view(),name='caja2-index',),
    path('punto_de_venta/caja/2/cierre_de_caja/cerrar/', views.ProcesoCerrarCaja2View.as_view(),name='caja2-cerrar',),
]