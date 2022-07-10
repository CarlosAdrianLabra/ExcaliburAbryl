from decimal import Decimal
from django.db import models
from django.db.models.signals import post_save, pre_save
from PIL import Image
from model_utils.models import TimeStampedModel
from django.utils import timezone
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

# Modelo de marca
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

# Modelo de color
class Color(models.Model):
    nombre = models.CharField('Color', max_length=35, blank=True)

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'
        db_table = 'Color'
        ordering = ['nombre']

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        return super(Color, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# Modelo de talla
class Talla(models.Model):
    nombre = models.CharField('Talla', max_length=10, blank=True)

    class Meta:
        verbose_name = 'Talla'
        verbose_name_plural = 'Tallas'
        db_table = 'Talla'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        return super(Talla, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# Modelo de sublinea
class Sublinea(models.Model):
    nombre = models.CharField('Sublinea', max_length=30, blank=True)

    class Meta:
        verbose_name = 'Sublinea'
        verbose_name_plural = 'Sublineas'
        db_table = 'Sublinea'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        return super(Sublinea, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# Modelo de productos
class Productos(TimeStampedModel):

    OPCIONES_ALMACEN = (
        ('1000', 'ALMACEN 1'),
        ('2000', 'ALMACEN 2'),
        ('3000', 'ALMACEN 3'),
    )

    OPCIONES_TIPO_PRODUCTO = (
        ('100', 'CALZADO'),
        ('200', 'ROPA'),
        ('300', 'ACCESORIOS'),
    )

    OPCIONES_GENERO = (
        ('', '---------'),
        ('0', 'BEBE'),
        ('1', 'CABALLERO'),
        ('2', 'DAMA'),
        ('3', 'JOVEN'),
        ('4', 'NINA'),
        ('5', 'NINO'),
        ('6', 'UNISEX'),
        ('7', 'VARIOS'),
    )

    OPCION_PROMOCIONES = (
        ('', '---------'),
        ('0', 'Sin promoción'),
        ('', ''),
        ('1', '10 %'),
        ('2', '20 %'),
        ('3', '30 %'),
        ('', ''),
        ('4', '2 x 1'),
        ('5', '3 x 2'),
        ('', ''),
        ('6', '1=10%, 2=20%'),
        ('', ''),
        ('7', '2 Adidas y obtén 10%'),
        ('', ''),
        ('8', '- $89.00'),
        ('9', '- $99.00'),
        ('10', '- $199.00'),
        ('11', '- $299.00'),
        ('', ''),
        ('12', 'Descuento establecido por tienda'),
        ('13', 'Descuento familiar'),
    )

    # Atributos necesarios
    barcode = models.CharField('Código de barras', max_length=13, blank=True, unique=True)
    barcode_exterior = models.CharField('Código de barras', max_length=15, blank=True)
    nombre = models.CharField('Nombre', max_length=30)

    # Atributos foreignkey
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    sublinea = models.ForeignKey(Sublinea, on_delete=models.CASCADE)

    # Atributos de opciones
    tipo = models.CharField('Tipo de producto', max_length=3, choices=OPCIONES_TIPO_PRODUCTO)
    almacen = models.CharField('Almacén', max_length=4, choices=OPCIONES_ALMACEN)
    genero = models.CharField('Género', max_length=1, blank=True, choices=OPCIONES_GENERO)
    promocion = models.CharField('Promociones', max_length=2, blank=True, choices=OPCION_PROMOCIONES, default='0')
    fecha_final_promocion = models.DateTimeField('Fecha final de promoción', null=True, blank=True)

    # Atributos no necesarios
    modelo = models.CharField('Modelo', max_length=25, blank=True)
    stock = models.PositiveIntegerField('Existencias', default=0)
    precio_compra = models.DecimalField('Precio de costo', max_digits=7, decimal_places=2, default=0)
    precio_venta = models.DecimalField('Precio de venta', max_digits=7, decimal_places=2, default=0)
    num_venta = models.PositiveIntegerField('Número de ventas', default=0)
    anular = models.BooleanField('Anular Producto', default=False)

    # Imagen del producto
    img = models.ImageField('Imagen', upload_to='productos', blank=True, null=True)

    # Managers
    objects = filtros()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Inventario de Productos'
        ordering = ['-id']
        db_table = 'Productos'
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Productos, self).save(*args, **kwargs)

    def __str__(self):
        return self.marca.nombre + ' - ' + self.modelo + ' - ' + self.get_genero_display()

# Modelo de movimientos (actualizaciones de inventario)
class Movimientos(TimeStampedModel):
    barcode = models.CharField('Código de barras', max_length=13)
    stock_nuevo = models.IntegerField('Cantidad de productos ingresados',  default=0)
    fecha = models.DateTimeField('Fecha y hora de actualización')
    precio_costo = models.DecimalField('Precio de costo', max_digits=7, decimal_places=2, default=0)
    total_costo = models.DecimalField('Costo total de productos ingresados', max_digits=7, decimal_places=2, default=0)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, verbose_name='Producto', related_name='movimientos_producto')

    class Meta:
        verbose_name = 'Movimientos'
        verbose_name_plural = 'Movimientos'
        ordering = ['-id']
        db_table = 'Movimientos'
    
    def __str__(self):
        return self.producto.nombre

# Funcion para optimizar el atributo IMG del modelo Productos
def optimizar_img(sender, instance, **kwargs):
    if instance.img:
        img = Image.open(instance.img.path)
        img.save(instance.img.path, quality=20, optimize=True)

post_save.connect(optimizar_img, sender=Productos)

# Funcion para registrar los cambios del modelo Productos
def movimientos_productos(sender, instance, **kwargs):
    try:
        stock_anterior = Productos.objects.get(barcode=instance.barcode)
        stock_anterior.stock = str(stock_anterior.stock)
        stock_anterior = int(stock_anterior.stock)
        #
        stock_nuevo = instance.stock
        stock_nuevo = int(stock_nuevo)
        #
        stock_ingresado = stock_nuevo - stock_anterior
        #
        precio_costo = Productos.objects.get(barcode=instance.barcode)
        costo = Decimal(stock_ingresado) * precio_costo.precio_compra
        #
        producto_modificado = Productos.objects.get(barcode=instance.barcode)
        producto_modificado.nombre = str(producto_modificado.nombre)
        costo_producto = precio_costo.precio_compra
        #
        mov = Movimientos.objects.create(
            barcode=instance.barcode,
            stock_nuevo=stock_ingresado,
            fecha=timezone.now(),
            total_costo=costo,
            producto=producto_modificado,
            precio_costo=costo_producto
        )
        mov.save()
    except Productos.DoesNotExist:
        return []
    else:
        return []

pre_save.connect(movimientos_productos, sender=Productos)

# Funcion para agregar el código de barras
def product(sender, instance, **kwargs):
    try:
        if instance.id > 0 and instance.id < 10:
            Productos.objects.filter(barcode=instance.barcode).update(
                barcode = str(instance.almacen)+str(instance.tipo)+"00000"+str(instance.id)
            )
        elif instance.id > 9 and instance.id < 100:
            Productos.objects.filter(barcode=instance.barcode).update(
                barcode = str(instance.almacen)+str(instance.tipo)+"0000"+str(instance.id)
            )
        elif instance.id > 99 and instance.id < 1000:
            Productos.objects.filter(barcode=instance.barcode).update(
                barcode = str(instance.almacen)+str(instance.tipo)+"000"+str(instance.id)
            )
        elif instance.id > 999 and instance.id < 10000:
            Productos.objects.filter(barcode=instance.barcode).update(
                barcode = str(instance.almacen)+str(instance.tipo)+"00"+str(instance.id)
            )
        elif instance.id > 9999 and instance.id < 100000:
            Productos.objects.filter(barcode=instance.barcode).update(
                barcode = str(instance.almacen)+str(instance.tipo)+"0"+str(instance.id)
            )
        elif instance.id > 99999:
            Productos.objects.filter(barcode=instance.barcode).update(
                barcode = str(instance.almacen)+str(instance.tipo)+str(instance.id)
            )

    except Productos.DoesNotExist:
        return []

post_save.connect(product, sender=Productos)

# Modelo para subir archivos
class ArchivoSubido(models.Model):

    OPCIONES_TIPO = (
        ('1', 'Marca'),
        ('2', 'Proveedor'),
        ('3', 'Accesorios'),
        ('4', 'Calzado'),
        ('5', 'Ropa'),
        ('6', 'Color'),
        ('7', 'Talla'),
        ('8', 'Sublinea')
    )

    archivo = models.FileField('Archivo', upload_to='archivos/')
    fecha = models.DateTimeField('Fecha de subida', auto_now_add=True)
    tipo = models.CharField('Tipo de archivo', max_length=2, choices=OPCIONES_TIPO, blank=True)

    class Meta:
        verbose_name = 'Archivo Subido'
        verbose_name_plural = 'Archivos Subidos'
        db_table = 'ArchivoSubido'

    def __str__(self):
        return str(self.archivo)

    def delete(self, *args, **kwargs):
        self.archivo.delete()
        super().delete(*args, **kwargs)