from django.urls import path
from . import views


app_name = "codigobarras_app"

urlpatterns = [


path('tabla_barras/',  views.codigobarrasview.as_view(), name='tabla_codigobarras'),

path('pdfbarras/<pk>/',  views.BarrasPDF.as_view(), name='barraspdf'),



# path('pdfcodigobarras/',  views.Codigobarraspdf.as_view(), name='pdfcodigobarras'),

]