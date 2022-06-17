from django.db import models

# Create your models here.
class Etiqueta(models.Model):
    barcode = models.CharField('Código de barras', max_length=15, blank=True)
    nombre = models.CharField('Nombre', max_length=30)
    marca = models.CharField('Marca', max_length=30)
    modelo = models.CharField('Modelo', max_length=30)
    linea = models.CharField('Línea', max_length=25)
    sublinea = models.CharField('Sublínea', max_length=25)
    talla = models.CharField('Talla', max_length=15)
    color = models.CharField('Color', max_length=35)

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        db_table = 'Etiqueta'

    def __str__(self):
        return self.nombre