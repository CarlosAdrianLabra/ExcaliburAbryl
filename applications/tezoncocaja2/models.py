from django.db import models
from model_utils.models import TimeStampedModel
from applications.inventarios.models import Productos
from applications.ventas.models import PreciosFijos
from applications.ventas.managers import CarShopManager

# Create your models here.
class Carritotezoncocaja2(TimeStampedModel):
    """
    Modelo que representa el carrito de compras
    """
    barcode = models.CharField(max_length=13, unique=True)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, verbose_name='producto', related_name='producto_carritotezoncocaja2')
    count = models.PositiveIntegerField('Cantidad')

    objects = CarShopManager()
    
    class Meta:
        verbose_name = 'Carrito de compras'
        verbose_name_plural = 'Carrito de compras'
        ordering = ['-created']

    def __str__(self):
        return str(self.producto.nombre)

    def subtotal(self):
        cod = self.barcode
        cantidad = float(self.count)
        promocion = self.producto.promocion
        p_venta = float(self.producto.precio_venta)
        cant_x_venta = float(self.count * self.producto.precio_venta)
        

        if promocion == '0' or promocion == '7':
            return cant_x_venta

        if promocion == '1':
            return cant_x_venta - (cant_x_venta * 0.10)

        if promocion == '2':
            return cant_x_venta - (cant_x_venta * 0.20)
        
        if promocion == '3' or promocion == '13':
            return cant_x_venta - (cant_x_venta * 0.30)
        
        if promocion == '4' and self.count == 2:
            return cant_x_venta - p_venta
        elif promocion == '4':
            return cant_x_venta
        
        if promocion == '5' and self.count == 3:
            return cant_x_venta - p_venta
        elif promocion == '5':
            return cant_x_venta

        if promocion == '6' and self.count == 1:
            return cant_x_venta - (cant_x_venta * 0.10)
        elif promocion == '6' and self.count == 2:
            return cant_x_venta - (cant_x_venta * 0.20)
        elif promocion == '6':
            return cant_x_venta
        
        if promocion == '8':
            return cant_x_venta - (cantidad * 89)
        if promocion == '9':
            return cant_x_venta - (cantidad * 99)
        if promocion == '10':
            return cant_x_venta - (cantidad * 199)
        if promocion == '11':
            return cant_x_venta - (cantidad * 299)
        
        if promocion == '12':
            promo = PreciosFijos.objects.get(barcode=cod)
            promo.precio_fijo = str(promo.precio_fijo)
            promo.precio_fijo = float(promo.precio_fijo)
            
            return cant_x_venta - (cantidad * promo.precio_fijo)

class Efectivotezoncocaja2(TimeStampedModel):
    cash = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    change = models.DecimalField(max_digits=7, decimal_places=2, blank=True)

    class Meta:
        verbose_name = 'Cambio de efectivo tezonco caja 2'
        verbose_name_plural = 'Cambio de efectivo tezonco caja 2'
        ordering = ['-created']

    def __str__(self):
        return str(self.change)