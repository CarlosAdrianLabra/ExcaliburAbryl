from django.urls import path
from . import views

app_name = "apartados_app"

urlpatterns = [
    path(
        'apartados/',views.CrearApartado.as_view(),name='crear_apartado',
    ),
    path(
        'apartados/lista/',views.ApartadosLista.as_view(),name='apartados_lista',
    ),
    path(
        'apartados/actualizar/<pk>',views.ApartadosUpdateView.as_view(),name='apartados_actualizar',
    ),
    path(
        'apartados/procesar_venta/',views.ApartadosProcesarVenta.as_view(),name='apartados_procesar_venta',
    ),
    path(
        'apartados/cancelar_venta/<pk>',views.ApartadosCancelarVenta.as_view(),name='apartados_cancelar_venta',
    ),
]