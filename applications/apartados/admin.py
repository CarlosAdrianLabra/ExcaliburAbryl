from django.contrib import admin
from .models import Apartados

# Register your models here.
class ApartadosAdmin(admin.ModelAdmin):
    list_display = (
        'barcode',
        'monto_pagado',
        'precio_producto',
        'apartado_cerrado',
        'apartado_venta'
    )

admin.site.register(Apartados, ApartadosAdmin)