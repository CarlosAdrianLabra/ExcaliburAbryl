from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Proveedor,
    Marca,
    Productos,
    Movimientos
)
from .resources import ProductosRecursos

class ProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'direccion',
        'correo',
        'telefono',
        'nombre_benefactor',
        'nombre_banco',
        'clabe'
    )
admin.site.register(Proveedor, ProveedorAdmin)

class MarcaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
    )
admin.site.register(Marca, MarcaAdmin)

# class ProductosAdmin(admin.ModelAdmin):
#     list_display = (
#         'barcode',
#         'nombre',
#         'stock',
#         'precio_compra',
#         'precio_venta',
#         'tipo',
#         'almacen',
#     )
# admin.site.register(Productos, ProductosAdmin)

class ProductosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'barcode',
        'nombre',
        'stock',
        'precio_compra',
        'precio_venta',
        'tipo',
        'almacen',
    )
    resource_class = ProductosRecursos

admin.site.register(Productos, ProductosAdmin)

# @admin.register(Productos)
# class ProductosAdmin2(ImportExportModelAdmin):
#     list_display = (
#         'barcode',
#         'nombre',
#         'stock',
#         'precio_compra',
#         'precio_venta',
#         'tipo',
#         'almacen',
#     )

admin.site.register(Movimientos)