from django.db import models
from applications.ventas.models import Carrito

# Create your models here.
class Apartados(models.Model):
    barcode = models.CharField('Código de barras', max_length=15, blank=True)
    monto_pagado = models.DecimalField('Monto pagado', max_digits=10, decimal_places=2, default=0)
    fecha = models.DateTimeField('Fecha de apartado',)
    precio_producto = models.DecimalField('Monto pagado', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Producto Apartado'
        verbose_name_plural = 'Productos Apartados'

    def __str__(self):
        return self.barcode