from django.urls import path
from . import views

app_name = "codigobarras_app"

urlpatterns = [
    path('codigo_de_barras/',  views.codigobarrasview.as_view(), name='codigo_de_barras_index'),
    # path('codigo_de_barras/pdf/<pk>/',  views.BarrasPDF.as_view(), name='barraspdf'),
    path('codigo_de_barras/agregar_uno/<pk>/',  views.AgregarUnoVista.as_view(), name='agregar_uno'),
    path('codigo_de_barras/pdf/lista_filtrada/',  views.ProductosFiltradosPDFVista.as_view(), name='productos_filtrados'),
    path('codigo_de_barras/pdf/lista_filtrada/eliminar_todo', views.EliminarEtiquetaVista.as_view(),name='productos_filtrados_eliminados',),
    # path('codigo_de_barras/agregar_todos/',  views.AgregarTodosVista.as_view(), name='agregar_todos'),
]