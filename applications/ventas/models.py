from django.db import models
from django.conf import settings
from django.db.models.base import Model
from django.db.models.signals import pre_delete, post_save

from model_utils.models import TimeStampedModel

#applicaciones locales
from applications.inventarios.models import Productos
from .managers import SaleManager, SaleDetailManager, CarShopManager

# Create your models here.
class Venta(TimeStampedModel):
    """
    Modelo que representa la venta Global
    """

    #Constantes del recibo
    BOLETA = '0'
    FACTURA = '1'
    SIN_COMPROBANTE = '2'
    APARTADO = '3'
    APARTADO_ANULADO = '4'
    #Tipo pago constantes
    TARJETA = '0'
    EFECTIVO = '1'
    BONO = '2'
    OTRO = '3'

    TIPO_INVOICE_CHOICES = [
        (SIN_COMPROBANTE, 'Sin Factura'),
        (FACTURA, 'Factura'),
        (APARTADO, 'Apartado'),
        (APARTADO_ANULADO, 'Apartado. No se termino de pagar')
    ]

    TIPO_PAYMENT_CHOICES = [
        (EFECTIVO, 'Efectivo'),
        (TARJETA, 'Tarjeta'),
    ]

    date_sale = models.DateTimeField('Fecha de Venta',)
    count = models.PositiveIntegerField('Cantidad de Productos')
    amount = models.DecimalField('Monto', max_digits=10, decimal_places=2)
    type_invoice = models.CharField('TIPO', max_length=2, choices=TIPO_INVOICE_CHOICES)
    type_payment = models.CharField('TIPO PAGO', max_length=2, choices=TIPO_PAYMENT_CHOICES)
    close = models.BooleanField('Venta Cerrada en Caja', default=False,)
    anulate = models.BooleanField('Venta Anulada', default=False,)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='cajero', related_name="user_venta")

    objects = SaleManager()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return 'Num# [' + str(self.id) + '] - ' + str(self.date_sale)


class DetalleVenta(TimeStampedModel):
    """
    Modelo que representa a una venta en detalle
    """
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, verbose_name='producto', related_name='product_sale')
    sale = models.ForeignKey(Venta, on_delete=models.CASCADE, verbose_name='Codigo de Venta', related_name='detail_sale')
    count = models.PositiveIntegerField('Cantidad')
    price_purchase = models.DecimalField('Precio Compra', max_digits=10, decimal_places=2)
    price_sale = models.DecimalField('Precio Venta', max_digits=10, decimal_places=2)
    price_subtotal = models.DecimalField('Precio Subtotal', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Total de Descuento', max_digits=5, decimal_places=2, default=0)
    promocion = models.CharField('Promoción de la venta', max_length=2, blank=True)
    tax = models.DecimalField('Impuesto', max_digits=5, decimal_places=2)
    anulate = models.BooleanField(default=False)

    objects = SaleDetailManager()

    class Meta:
        verbose_name = 'Producto Vendido'
        verbose_name_plural = 'Productos vendidos'

    def __str__(self):
        return str(self.sale.id) + ' - ' + str(self.producto.nombre)


class Carrito(TimeStampedModel):
    """
    Modelo que representa el carrito de compras
    """
    barcode = models.CharField(max_length=13, unique=True)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, verbose_name='producto', related_name='product_car')
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
        
        if promocion == '3':
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


class Efectivo(TimeStampedModel):
    cash = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    change = models.DecimalField(max_digits=7, decimal_places=2, blank=True)

    class Meta:
        verbose_name = 'Cambio de efectivo'
        verbose_name_plural = 'Cambio de efectivo'
        ordering = ['-created']

    def __str__(self):
        return str(self.change)
    

class PreciosFijos(models.Model):
    barcode = models.CharField('Código de barras', max_length=13, blank=True)
    precio_fijo = models.DecimalField('Precio fijado por tienda', max_digits=7, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Precio Fijo'
        verbose_name_plural = 'Precios Fijos'

    def __str__(self):
        return str(self.precio_fijo)
