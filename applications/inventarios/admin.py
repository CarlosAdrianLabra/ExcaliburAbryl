from django.contrib import admin
from .models import Productos

# Register your models here.

class ProductosAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombreP',
        'cantidadP',
        'precioP',
        'marcaP',
    )

admin.site.register(Productos, ProductosAdmin)
