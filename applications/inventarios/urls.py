from django.contrib import admin
from django.urls import path

# Import views
from . import views

app_name = "inventarios"

urlpatterns = [
    path('inventario/', views.PaginaPrincipal.as_view(), name='inventario_inicio'),
    path('registrar-productos/', views.RegistrarProductos.as_view(), name='registrar_productos'),
    path('inventario-productos/', views.InventarioProductos.as_view(), name='inventario_productos'),
    path('visualizar-producto/<pk>/', views.VisualizarProductos.as_view(), name='visualizar_productos'),
    path('inventario-administrar-productos/', views.AdministrarProductos.as_view(), name='administrar_productos'),
    path('actualizar-productos/<pk>/', views.ActualizarProductos.as_view(), name='actualizar_productos'),
    path('eliminar-productos/<pk>/', views.EliminarProductos.as_view(), name='eliminar_productos'),
    
]