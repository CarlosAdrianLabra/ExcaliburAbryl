from django.urls import path
from . import views

urlpatterns = [
    # Index marcas
    path('marca/',  views.IndexMarca.as_view(), name='index_marca'),
    # URLs para acciones CUD
    path('crear_marca/',  views.CrearMarcaVista.as_view(), name='crear_marca'),
    path('actualizar_marca/',  views.ActualizarMarcaVista.as_view(), name='actualizar_marca'),
    path('eliminar_marca/',  views.EliminarMarcaVista.as_view(), name='eliminar_marca'),

    # Index proveedores
    path('proveedor/',  views.IndexProveedor.as_view(), name='index_proveedor'),
    # URLs para acciones CUD
    path('crear_proveedor/',  views.CrearProveedorVista.as_view(), name='crear_proveedor'),
    path('actualizar_proveedor/',  views.ActualizarProveedorVista.as_view(), name='actualizar_proveedor'),
    path('eliminar_proveedor/',  views.EliminarProveedorVista.as_view(), name='eliminar_proveedor'),

    # Index inventarios
    path('inventario/',  views.IndexInventario.as_view(), name='index_inventario'),
    
    # Index calzado
    path('almacen_1/productos/calzado/', views.IndexCalzado.as_view(), name='index_calzado'),
    # URLs para acciones CRUD
    path('crear_producto_calzado/', views.CrearCalzadoVista.as_view(), name='crear_calzado'),
    path('actualizar_calzado/<int:pk>', views.ActualizarCalzadoVista.as_view(), name='actualizar_calzado'),
    path('eliminar_calzado/<int:pk>', views.EliminarCalzadoVista.as_view(), name='eliminar_calzado'),
    path('ver_calzado/<int:pk>', views.LeerCalzadoVista.as_view(), name='leer_calzado'),
    # URL para FUNCION producto_calzado
    path('producto_calzado/', views.producto_calzado, name='producto_calzado'),

    # Index ropa
    path('almacen_1/productos/ropa/', views.IndexRopa.as_view(), name='index_ropa'),
    # URLs para acciones CRUD
    path('crear_ropa/', views.CrearRopaVista.as_view(), name='crear_ropa'),
    path('actualizar_ropa/<int:pk>', views.ActualizarRopaVista.as_view(), name='actualizar_ropa'),
    path('eliminar_ropa/<int:pk>', views.EliminarRopaVista.as_view(), name='eliminar_ropa'),
    path('ver_ropa/<int:pk>', views.LeerRopaVista.as_view(), name='leer_ropa'),
    # URL para FUNCION producto_calzado
    path('producto_ropa/', views.producto_ropa, name='producto_ropa'),
]