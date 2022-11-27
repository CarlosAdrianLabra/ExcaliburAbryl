from django.db import models
from model_utils.models import TimeStampedModel
from django.utils import timezone
from django.db import IntegrityError
from django.db.models.signals import post_save, pre_save
from applications.inventarios.models import Productos
from .managers import CarShopManager

# Create your models here.
class Apartados(models.Model):
    barcode = models.CharField('Código de barras', max_length=15, blank=True)
    monto_pagado = models.DecimalField('Monto pagado', max_digits=8, decimal_places=2, default=0)
    fecha = models.DateTimeField('Fecha de apartado',)
    precio_producto = models.DecimalField('Precio del producto', max_digits=8, decimal_places=2, default=0)
    cambio = models.DecimalField('Cambio', max_digits=8, decimal_places=2, default=0)
    apartado_cerrado = models.BooleanField('Apartado pagado', default=False)
    apartado_venta = models.BooleanField('Apartado venta realizada', default=False)
    
    class Meta:
        verbose_name = 'Producto Apartado'
        verbose_name_plural = 'Productos Apartados'

    def __str__(self):
        return self.barcode

# Funcion para completar la venta
def completar_venta(sender, instance, **kwargs):

    try:
        precio_actualizado = instance.monto_pagado
        precio_a_pagar = instance.precio_producto

        if precio_actualizado >= precio_a_pagar:
            Apartados.objects.filter(id=instance.pk).update(apartado_cerrado=True)
            CarritoApartados.objects.create(
                barcode=instance.barcode,
                producto=Productos.objects.get(barcode=instance.barcode),
                count='1'
            )

    except IntegrityError:
        return []

post_save.connect(completar_venta, sender=Apartados)

class CarritoApartados(TimeStampedModel):
    barcode = models.CharField(max_length=13, unique=True)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, verbose_name='producto', related_name='product_car_apartados')
    count = models.PositiveIntegerField('Cantidad')

    objects = CarShopManager()
    
    class Meta:
        verbose_name = 'Carrito de apartados'
        verbose_name_plural = 'Carrito de apartados'
        ordering = ['-created']

    def __str__(self):
        return str(self.producto.nombre)

    def subtotal(self):
        cant_x_venta = float(self.count * self.producto.precio_venta)

        return cant_x_venta