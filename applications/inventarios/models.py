from django.db import models
from django.db.models.signals import post_save
from model_utils.models import TimeStampedModel
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from PIL import Image
from .managers import filtros

# Modelo de proveedores
class Proveedor(TimeStampedModel):

    nombre = models.CharField('Nombre', max_length=50, blank=True)
    correo = models.EmailField('Correo Electrónico', blank=True)
    telefono = models.CharField('Teléfono', max_length=14, blank=True)
    direccion = models.CharField('Dirección', max_length=50, blank=True)
    clabe = models.CharField('Clabe interbancaria', max_length=18, blank=True)
    nombre_banco = models.CharField('Nombre de banco', max_length=40, blank=True)
    nombre_benefactor = models.CharField('Nombre del beneficiario', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores Registrados'
        db_table = 'Proveedor'

    def __str__(self):
        return self.nombre

# Modelo de marcas
class Marca(TimeStampedModel):

    nombre = models.CharField('Nombre', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas Registradas'
        db_table = 'Marca'

    def __str__(self):
        return self.nombre

# Modelo de productos
class Productos(TimeStampedModel):

    OPCIONES_ALMACEN = (
        ('0', 'ALMACEN 1'),
        ('1', 'ALMACEN 2'),
        ('2', 'ALMACEN 3'),
    )

    OPCIONES_TIPO_PRODUCTO = (
        ('0', 'CALZADO'),
        ('1', 'ROPA'),
    )

    OPCIONES_TALLA = (
        ('0', 'CH'),
        ('1', 'M'),
        ('2', 'G'),
    )

    OPCIONES_MEDIDA = (
        ('', '---------'),
        ('0', '21'),('1', '22'),('2', '23'),('3', '24'),('4', '25'),
        ('5', '26'),('6', '27'),('7', '28'),('8', '29'),('9', '30'),
        ('', '---------'),
        ('10', '21.5'),('11', '22.5'),('12', '23.5'),('13', '24.5'),('14', '25.5'),
        ('15', '26.5'),('16', '27.5'),('17', '28.5'),('18', '29.5'),
    )

    OPCIONES_LINEA = (
        ('0', 'ADULTO'),
        ('1', 'NIÑO'),
        ('2', 'CABALLERO'),
        ('3', 'DAMA'),
    )

    OPCIONES_COLOR = (
        ('0', 'ROJO'),
        ('1', 'AZUL'),
        ('2', 'AMARILLO'),
        ('3', 'NEGRO'),
        ('4', 'MORADO'),
        ('5', 'VERDE'),
        ('6', 'BLANCO'),
    )

    # Atributos necesarios
    barcode = models.PositiveIntegerField('Código de barras', unique=True)
    nombre = models.CharField('Nombre', max_length=40)

    # Atributos foreignkey
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    
    # Atributos de opciones
    tipo = models.CharField('Tipo de producto', max_length=1, choices=OPCIONES_TIPO_PRODUCTO)
    almacen = models.CharField('Almacén', max_length=1, choices=OPCIONES_ALMACEN)
    talla = models.CharField('Talla', max_length=1, blank=True, choices=OPCIONES_TALLA)
    medida = models.CharField('Medida', max_length=2, blank=True, choices=OPCIONES_MEDIDA)
    linea = models.CharField('Departamento', max_length=1, blank=True, choices=OPCIONES_LINEA)
    color = models.CharField('Color', max_length=2, blank=True, choices=OPCIONES_COLOR)

    # Atributos no necesarios
    modelo = models.CharField('Modelo', max_length=6, blank=True)
    stock = models.PositiveIntegerField('Existencias', default=0)
    precio_compra = models.DecimalField('Precio de compra', max_digits=6, decimal_places=2, default=0)
    precio_venta = models.DecimalField('Precio de venta', max_digits=6, decimal_places=2, default=0)
    num_venta = models.PositiveIntegerField('Número de ventas', default=0)
    anular = models.BooleanField('Anular Producto', default=False)

    # Imagen del producto
    img = models.ImageField('Imagen', upload_to='productos', blank=True, null=True)
    
    # Imagen del codigo de barras
    barcodeimg= models.ImageField('imagenbarras', upload_to='codigodebarras/', blank=True)

    # Managers
    objects = filtros()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Inventario de Productos'
        ordering = ['id']
        db_table = 'Productos'

    def __str__(self):
        return self.marca.nombre + ' - ' + self.modelo + ' - ' + self.get_linea_display() + ' - ' + self.get_color_display()

    def save(self, *args, **kwargs):
        EAN= barcode.get_barcode_class('ean13')
        ean = EAN('123456789012', writer=ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcodeimg.save(f"{self.nombre}.png", File(buffer), save=False)
        return super().save(*args, **kwargs)

# Funcion para optimizar el atributo IMG del modelo Productos
def optimizar_img(sender, instance, **kwargs):
    if instance.img:
        img = Image.open(instance.img.path)
        img.save(instance.img.path, quality=20, optimize=True)

post_save.connect(optimizar_img, sender=Productos)
