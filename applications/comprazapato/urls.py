from django.urls import path
from .views import *
from . import views

app_name = "comprazapato_app"

urlpatterns = [
    path('comprazapato/', baseCompraZapato.as_view(), name='comprazapato'),
    path('comprazapato/lista_pedidos/', listaPedidos.as_view(), name='comprazapato_lista_pedidos'),

]