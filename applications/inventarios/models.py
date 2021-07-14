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
        ('1000', 'ALMACEN 1'),
        ('2000', 'ALMACEN 2'),
        ('3000', 'ALMACEN 3'),
    )

    OPCIONES_TIPO_PRODUCTO = (
        ('100', 'CALZADO'),
        ('200', 'ROPA'),
        ('300', 'ACCESORIOS'),
    )

    OPCIONES_TALLA = (
        ('', '---------'),
        ('00', 'XCH'),
        ('01', 'CH'),
        ('02', 'M'),
        ('03', 'G'),
        ('04', 'XG'),
        ('', '---------'),
        ('', 'CABALLERO'),
        ('12', '28'),('13', '30'),('14', '32'),('15', '34'),('16', '36'),('17', '38'),('18', '40'),
        ('', '---------'),
        ('', 'DAMA'),
        ('05', '0'),('06', '3'),('07', '5'),('08', '7'),('09', '11'),('10', '13'),('11', '15'),
        ('', '---------'),
        ('', 'NIÑO/A'),
        ('', 'Pendiente ...'),
    )

    OPCIONES_MEDIDA = (
        ('', '---------'),
        ('', 'CABALLERO'),
        ('00', '25'),('01', '26'),('02', '27'),('03', '28'),('04', '29'),('05', '30'),('06', '31'),
        ('', '---------'),
        ('', 'DAMA'),
        ('07', '22'),('08', '23'),('09', '24'),('10', '25'),('11', '26'),('12', '27'),
        ('', '---------'),
        ('', 'JOVEN'),
        ('13', '22'),('14', '23'),('15', '24'),('16', '25'),('17', '26'),
        ('', '---------'),
        ('', 'NIÑO/A'),
        ('18', '9'),('19', '9.5'),('20', '10'),('21', '10.5'),('22', '11'),('23', '11.5'),('24', '12'),('25', '12.5'),
        ('26', '13'),('27', '13.5'),('28', '14'),('29', '14.5'),('30', '15'),('31', '15.5'),('32', '16'),('33', '16.5'),('34', '17'),('35', '17.5'),
        ('36', '18'),('37', '18.5'),('38', '19'),('39', '19.5'),('40', '20'),('41', '20.5'),('42', '21'),('43', '21.5')
    )

    OPCIONES_LINEA_CALZADO = (
        ('', '---------'),
        ('00', 'BOTA'),
        ('01', 'BOTÍN'),
        ('02', 'CHOCLO'),
        ('03', 'ESCOLAR'),
        ('04', 'FLATS'),
        ('05', 'PANTUFLA'),
        ('06', 'SANDALIA'),
        ('07', 'TENIS'),
        ('08', 'ZAPATILLA'),
    )

    OPCIONES_LINEA_ROPA = (
        ('', '---------'),
        ('00', 'BABERO'),
        ('01', 'PANTALON'),
    )

    OPCIONES_LINEA_ACCESORIOS = (
        ('', '---------'),
        ('00', 'LIMPIEZA'),
        ('01', 'MOCHILA'),
    )

    OPCIONES_GENERO = (
        ('', '---------'),
        ('1', 'CABALLERO'),
        ('2', 'DAMA'),
        ('3', 'JOVEN'),
        ('4', 'NIÑO/A'),
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
    )

    # Atributos necesarios
    barcode = models.CharField('Código de barras', max_length=13, blank=True, unique=True)
    nombre = models.CharField('Nombre', max_length=40)

    # Atributos foreignkey
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    
    # Atributos de opciones
    tipo = models.CharField('Tipo de producto', max_length=3, choices=OPCIONES_TIPO_PRODUCTO)
    almacen = models.CharField('Almacén', max_length=4, choices=OPCIONES_ALMACEN)
    talla = models.CharField('Talla', max_length=2, blank=True, choices=OPCIONES_TALLA)
    medida = models.CharField('Medida', max_length=2, blank=True, choices=OPCIONES_MEDIDA)
    linea_a = models.CharField('Línea de accesorios', max_length=2, blank=True, choices=OPCIONES_LINEA_ACCESORIOS)
    linea_c = models.CharField('Línea de calzado', max_length=2, blank=True, choices=OPCIONES_LINEA_CALZADO)
    linea_r = models.CharField('Línea de ropa', max_length=2, blank=True, choices=OPCIONES_LINEA_ROPA)
    color = models.CharField('Color', max_length=2, blank=True, choices=OPCIONES_COLOR)
    genero = models.CharField('Color', max_length=1, blank=True, choices=OPCIONES_GENERO)
    promocion = models.CharField('Promociones', max_length=2, blank=True, choices=OPCION_PROMOCIONES)

    # Atributos no necesarios
    modelo = models.CharField('Modelo', max_length=15, blank=True)
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
        ordering = ['-id']
        db_table = 'Productos'
    
    def save(self, *args, **kwargs):        
        self.barcode = self.almacen + self.tipo + self.medida + self.talla + self.linea_c + self.linea_r + self.linea_a + self.color
        self.nombre = self.nombre.upper()
        super(Productos, self).save(*args, **kwargs)

    def __str__(self):
        return self.marca.nombre + ' - ' + self.modelo + ' - ' + self.get_color_display()

# Funcion para optimizar el atributo IMG del modelo Productos
def optimizar_img(sender, instance, **kwargs):
    if instance.img:
        img = Image.open(instance.img.path)
        img.save(instance.img.path, quality=20, optimize=True)

post_save.connect(optimizar_img, sender=Productos)