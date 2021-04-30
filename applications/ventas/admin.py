from django.contrib import admin
from .models import Venta, DetalleVenta
# Register your models here.

class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'date_sale',
        'count',
        'amount',
        'user',
        'close',
        'anulate',
    )
    list_filter = ('type_invoice', 'type_payment', 'anulate', 'user', )


class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = (
        'producto',
        'sale',
        'count',
        'anulate',
    )
    search_fields = ('product__name',)


admin.site.register(Venta, VentaAdmin)
#
admin.site.register(DetalleVenta, DetalleVentaAdmin)
