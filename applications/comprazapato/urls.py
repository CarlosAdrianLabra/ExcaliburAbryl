from django.urls import path
from .views import *
from . import views

app_name = "comprazapato_app"

urlpatterns = [
    path('compra_de_zapato/', views.baseCompraZapato.as_view(), name='comprazapato'),
    path('compra_de_zapato/lista_pedidos/', views.listaPedidos.as_view(), name='comprazapato_lista_pedidos'),
    path('compra_de_zapato/actualizar_pedido/<pk>', views.compraZapatoUpdateView.as_view(), name='update-comprazapato'),

]