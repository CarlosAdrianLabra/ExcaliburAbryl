from django.db import models
from django.db.models.signals import post_save
from PIL import Image
from model_utils.models import TimeStampedModel
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
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.direccion = self.direccion.upper()
        self.nombre_banco = self.nombre_banco.upper()
        self.nombre_benefactor = self.nombre_benefactor.upper()
        return super(Proveedor, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# Modelo de marcas
class Marca(TimeStampedModel):

    nombre = models.CharField('Nombre', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas Registradas'
        db_table = 'Marca'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        return super(Marca, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# Modelo de productos
class Productos(TimeStampedModel):

    OPCIONES_ALMACEN = (
        ('10', 'ALMACEN 1'),
        ('20', 'ALMACEN 2'),
        ('30', 'ALMACEN 3'),
    )

    OPCIONES_TIPO_PRODUCTO = (
        ('10', 'CALZADO'),
        ('20', 'ROPA'),
    )

    OPCIONES_TALLA = (
        ('00', 'CH'),
        ('01', 'M'),
        ('02', 'G'),
    )

    OPCIONES_MEDIDA = (
        ('', '---------'),
        ('00', '21'),('01', '22'),('02', '23'),('03', '24'),('04', '25'),
        ('05', '26'),('06', '27'),('07', '28'),('08', '29'),('09', '30'),
        ('', '---------'),
        ('10', '21.5'),('11', '22.5'),('12', '23.5'),('13', '24.5'),('14', '25.5'),
        ('15', '26.5'),('16', '27.5'),('17', '28.5'),('18', '29.5'),
    )

    OPCIONES_LINEA = (
        ('00', 'ADULTO'),
        ('01', 'NIÑO'),
        ('02', 'CABALLERO'),
        ('03', 'DAMA'),
    )

    OPCIONES_COLOR = (
        ('00', 'ROJO'),
        ('01', 'AZUL'),
        ('02', 'AMARILLO'),
        ('03', 'NEGRO'),
        ('04', 'MORADO'),
        ('05', 'VERDE'),
        ('06', 'BLANCO'),
    )

    # Atributos necesarios
    barcode = models.CharField('Código de barras', max_length=13, blank=True, unique=True)
    nombre = models.CharField('Nombre', max_length=40)

    # Atributos foreignkey
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    
    # Atributos de opciones
    tipo = models.CharField('Tipo de producto', max_length=2, choices=OPCIONES_TIPO_PRODUCTO)
    almacen = models.CharField('Almacén', max_length=2, choices=OPCIONES_ALMACEN)
    talla = models.CharField('Talla', max_length=2, blank=True, choices=OPCIONES_TALLA)
    medida = models.CharField('Medida', max_length=2, blank=True, choices=OPCIONES_MEDIDA)
    linea = models.CharField('Departamento', max_length=2, blank=True, choices=OPCIONES_LINEA)
    color = models.CharField('Color', max_length=2, blank=True, choices=OPCIONES_COLOR)

    # Atributos no necesarios
    modelo = models.CharField('Modelo', max_length=3, blank=True)
    stock = models.PositiveIntegerField('Existencias', default=0)
    precio_compra = models.DecimalField('Precio de compra', max_digits=6, decimal_places=2, default=0)
    precio_venta = models.DecimalField('Precio de venta', max_digits=6, decimal_places=2, default=0)
    num_venta = models.PositiveIntegerField('Número de ventas', default=0)
    anular = models.BooleanField('Anular Producto', default=False)

    # Imagen del producto
    img = models.ImageField('Imagen', upload_to='productos', blank=True, null=True)

    # Managers
    objects = filtros()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Inventario de Productos'
        ordering = ['id']
        db_table = 'Productos'
    
    def save(self, *args, **kwargs):        
        self.barcode = self.almacen + self.tipo + self.medida + self.talla + self.modelo + self.linea + self.color
        self.nombre = self.nombre.upper()
        super(Productos, self).save(*args, **kwargs)

    def __str__(self):
        return self.marca.nombre + ' - ' + self.modelo + ' - ' + self.get_linea_display() + ' - ' + self.get_color_display()

# Funcion para optimizar el atributo IMG del modelo Productos
def optimizar_img(sender, instance, **kwargs):
    if instance.img:
        img = Image.open(instance.img.path)
        img.save(instance.img.path, quality=20, optimize=True)

post_save.connect(optimizar_img, sender=Productos)