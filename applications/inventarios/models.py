from django.db import models
from django.db.models.signals import post_save
from model_utils.models import TimeStampedModel
from PIL import Image

# Modelo de proveedores
class Proveedor(TimeStampedModel):

    nombre = models.CharField('Nombre', max_length=50,  blank=True)
    correo = models.EmailField('Correo Electrónico', blank=True)
    telefono = models.CharField('Teléfono', max_length=14, blank=True)
    direccion = models.CharField('Dirección', max_length=50, blank=True)

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

#Modelo de productos
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
        ('0', 'EXTRA CHICA'),
        ('1', 'CHICA'),
        ('2', 'MEDIANA'),
        ('3', 'GRANDE'),
        ('4', 'EXTRA GRANDE'),
        ('2', 'SLIM'),
    )

    OPCIONES_MEDIDA = (
        ('0', '21'),
        ('1', '21.5'),
        ('2', '22'),
        ('3', '22.5'),
        ('4', '23'),
        ('5', '23.5'),
        ('6', '24'),
        ('7', '24.5'),
        ('8', '25'),
        ('9', '25.5'),
        ('10', '26'),
        ('11', '26.5'),
        ('12', '27'),
        ('13', '27.5'),
        ('14', '28'),
        ('15', '28.5'),
        ('16', '29'),
        ('17', '29.5'),
        ('18', '30'),
    )

    # Atributos necesarios
    barcode = models.CharField('Código de barras', max_length=12, unique=True)
    nombre = models.CharField('Nombre', max_length=40)
    num_venta = models.PositiveIntegerField('Número de ventas', default=0)

    # Atributos de opciones
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    tipo = models.CharField('Tipo de producto', max_length=1, choices=OPCIONES_TIPO_PRODUCTO)
    almacen = models.CharField('Almacén', max_length=1, choices=OPCIONES_ALMACEN)

    # Atributos no necesarios
    stock = models.PositiveIntegerField('Existencias', default=0)
    precio_compra = models.DecimalField('Precio de compra', max_digits=8, decimal_places=2, default=0)
    precio_venta = models.DecimalField('Precio de venta', max_digits=8, decimal_places=2, default=0)
    descripcion = models.CharField('Descripción', max_length=50, blank=True)
    
    # Opciones
    talla = models.CharField('Talla', max_length=1, blank=True, choices=OPCIONES_TALLA)
    medida = models.CharField('Medida', max_length=2, blank=True, choices=OPCIONES_MEDIDA)
    anular = models.BooleanField('Anular Producto', default=False)

    # Imagen del producto
    img = models.ImageField('Imagen', upload_to='productos', blank=True, null=True)

    # Managers
    #objects = Almacen_1_Calzado()
    #objects = Almacen_1_Ropa()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Inventario de Productos'
        ordering = ['id']
        db_table = 'Productos'

    def __str__(self):
        return self.nombre

# Funcion para optimizar el atributo IMG del modelo Productos
def optimizar_img(sender, instance, **kwargs):
    if instance.img:
        img = Image.open(instance.img.path)
        img.save(instance.img.path, quality=20, optimize=True)

post_save.connect(optimizar_img, sender=Productos)
