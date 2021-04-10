from django.db import models

# Create your models here.
class Productos(models.Model):
    nombreP = models.CharField('Nombre de producto', max_length=50)
    modeloP = models.CharField('Modelo', max_length=30, blank=True)
    cantidadP = models.IntegerField('Cantidad')
    precioP = models.FloatField('Precio')
    marcaP = models.CharField('Marca', max_length=25, blank=True)
    imagenP = models.ImageField('Imagen', upload_to='productos', blank=True, null=True)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventario de Productos'
        ordering = ['id']