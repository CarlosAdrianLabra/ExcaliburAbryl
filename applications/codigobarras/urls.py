from django.urls import path
from . import views

app_name = "codigobarras_app"

urlpatterns = [
    path('codigo_de_barras/',  views.codigobarrasview.as_view(), name='tabla_codigobarras'),
    path('codigo_de_barras/pdf/<pk>/',  views.BarrasPDF.as_view(), name='barraspdf'),
    # path('pdfcodigobarras/',  views.Codigobarraspdf.as_view(), name='pdfcodigobarras'),

]