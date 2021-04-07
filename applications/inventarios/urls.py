from django.contrib import admin
from django.urls import path

# Import views
from . import views

app_name = "inventarios"

urlpatterns = [
    path('registrar-nuevo-producto/', views.NuevoProducto.as_view(), name='registro_producto'),
    path('inventario/', views.PaginaPrincipal.as_view(), name='principal'),
]