from django.db import models
from django.db.models.deletion import CASCADE
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

from applications.inventarios.models import Productos
# Create your models here.

class Codigodebarras(models.Model):
    nombre= models.CharField(max_length=200)
    barcodeimg= models.ImageField('imagenbarras', upload_to='codigodebarras/', blank=True)
    
    country_id = models.CharField(max_length=1, null=True)
    manufacturer_id = models.CharField(max_length=6, null=True)
    product_id = models.CharField(max_length=5, null=True)
    

    def __str__(self):
        return str(self.nombre)

    def save(self, *args, **kwargs):
        EAN= barcode.get_barcode_class('ean13')
        ean = EAN(f'{self.country_id}{self.manufacturer_id}{self.product_id}', writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcodeimg.save(f"{self.nombre}.png", File(buffer), save=False)
        return super().save(*args, **kwargs)

