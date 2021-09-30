from django.db import models
from django.utils import timezone
from django.db import IntegrityError
from django.db.models.signals import post_save, pre_save
from applications.inventarios.models import Productos
from applications.ventas.models import Venta, Carrito, DetalleVenta
from applications.users.models import User

# Create your models here.
class Apartados(models.Model):
    barcode = models.CharField('Código de barras', max_length=15, blank=True)
    monto_pagado = models.DecimalField('Monto pagado', max_digits=10, decimal_places=2, default=0)
    fecha = models.DateTimeField('Fecha de apartado',)
    precio_producto = models.DecimalField('Precio del producto', max_digits=10, decimal_places=2, default=0)
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

        if precio_actualizado == precio_a_pagar:
            Apartados.objects.filter(id=instance.pk).update(apartado_cerrado=True)
            Carrito.objects.create(
                barcode=instance.barcode,
                producto=Productos.objects.get(barcode=instance.barcode),
                count='1'
            )

    except IntegrityError:
        pass

post_save.connect(completar_venta, sender=Apartados)