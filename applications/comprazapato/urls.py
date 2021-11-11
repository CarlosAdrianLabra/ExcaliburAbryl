from django.urls import path
from .views import *
from . import views

app_name = "comprazapato_app"

urlpatterns = [
    path('comprazapato/', views.baseCompraZapato.as_view(), name='comprazapato'),
    path('comprazapato/lista_pedidos/', views.listaPedidos.as_view(), name='comprazapato_lista_pedidos'),
    path('comprazapato/update-comprazapato/<pk>', views.compraZapatoUpdateView.as_view(), name='update-comprazapato'),

]