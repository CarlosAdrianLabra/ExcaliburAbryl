from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    ArchivoSubido,
    Proveedor,
    Marca,
    Productos,
    Movimientos,
    Color,
    Talla,
    Sublinea
)
from .resources import ProductosRecursos

# class ProveedorAdmin(admin.ModelAdmin):
#     list_display = (
#         'nombre',
#         'direccion',
#         'correo',
#         'telefono',
#         'nombre_benefactor',
#         'nombre_banco',
#         'clabe'
#     )
# admin.site.register(Proveedor, ProveedorAdmin)

# class MarcaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = (
#         'id',
#         'nombre',
#     )
# admin.site.register(Marca, MarcaAdmin)

# class ColorAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'nombre',
#     )
# admin.site.register(Color, ColorAdmin)

# class TallaAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'nombre',
#     )
# admin.site.register(Talla, TallaAdmin)

# class SublineaAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'nombre',
#     )
# admin.site.register(Sublinea, SublineaAdmin)

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
        'id',
        'barcode',
        'marca',
        'modelo',
        'stock',
        'precio_compra',
        'precio_venta',
        'tipo',
    )
    resource_class = ProductosRecursos
    exclude = ('id',)
    list_filter = ('tipo', )

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

# admin.site.register(Movimientos)
admin.site.register(ArchivoSubido)