from django.db import models
from django.db.models.fields import CharField
from django.utils import timezone
# Create your models here.

class Pedidos(models.Model):
    OPCIONES_ESTADO = (
        ('1', 'Sin revisar'),
        ('2', 'Revisado'),
        ('3', 'Defectuoso'),
    )
    fecha_inicio = models.DateTimeField('Fecha de compra')
    fecha_termino = models.DateTimeField('Fecha de Pago')
    monto_por_pagar = models.DecimalField('Monto por pagar', max_digits=10, decimal_places=2, default=0)
    estado_compra = models.CharField('Estado de compra', max_length=1, choices=OPCIONES_ESTADO, default=1)
    codigo_factura = models.CharField('Codigo de factura', max_length=20, blank=True)
    proveedor = models.CharField('Proveedor', max_length=50, blank=True)
    comentario = models.TextField('Comentario', blank=True, max_length=500)
    

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return str(self.id) + ' ' + str(self.fecha_inicio) + ' ' + str(self.fecha_termino)