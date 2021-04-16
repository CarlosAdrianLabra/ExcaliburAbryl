from django.urls import path
from . import views

urlpatterns = [
    # Index produccion
    path('inventario/', views.IndexProductos.as_view(), name='index_productos'),

    # URLs para acciones CRUD
    path('crear_productos/', views.ProductosCrearVista.as_view(), name='crear_productos'),
    path('actualizar_productos/<int:pk>', views.ProductosActualizarVista.as_view(), name='actualizar_productos'),
    path('eliminar_productos/<int:pk>', views.ProductosEliminarVista.as_view(), name='eliminar_productos'),
    path('ver_productos/<int:pk>', views.ProductosLeerVista.as_view(), name='leer_productos'),

    # URL para llamar la FUNCION producto
    path('producto/', views.producto, name='producto'),
]