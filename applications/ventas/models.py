from django.db import models
from django.conf import settings
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
    #Tipo pago constantes
    TARJETA = '0'
    EFECTIVO = '1'
    BONO = '2'
    OTRO = '3'

    TIPO_INVOICE_CHOICES = [
        (SIN_COMPROBANTE, 'Sin Factura'),
        (FACTURA, 'Factura'),
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
    close = models.BooleanField('Venta Anulada', default=False,)
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
    price_purchase = models.DecimalField('Precio Compra', max_digits=10, decimal_places=3)
    price_sale = models.DecimalField('Precio Venta', max_digits=10, decimal_places=2)
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


class Efectivo(TimeStampedModel):
    cash = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    change = models.DecimalField(max_digits=7, decimal_places=2, blank=True)

    class Meta:
        verbose_name = 'Cambio de efectivo'
        verbose_name_plural = 'Cambio de efectivo'
        ordering = ['-created']

    def __str__(self):
        return str(self.change)