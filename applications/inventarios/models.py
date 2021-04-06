from django.db import models

# Create your models here.
class Productos(models.Model):
    nombreP = models.CharField('Nombre de producto', max_length=50)
    cantidadP = models.IntegerField('Cantidad')
    precioP = models.FloatField('Precio')
    marcaP = models.CharField('Marca', max_length=25, blank=True)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventario de Productos'
        ordering = ['id']
