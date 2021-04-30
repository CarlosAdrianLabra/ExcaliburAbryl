from django.contrib import admin
from .models import (
    Proveedor,
    Marca,
    Productos
)

class ProveedorAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'direccion',
        'correo',
        'telefono',
    )
admin.site.register(Proveedor, ProveedorAdmin)

class MarcaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
    )
admin.site.register(Marca, MarcaAdmin)

class ProductosAdmin(admin.ModelAdmin):
    list_display = (
        'barcode',
        'nombre',
        'stock',
        'precio_compra',
        'precio_venta',
        'tipo',
        'almacen',
    )
admin.site.register(Productos, ProductosAdmin)