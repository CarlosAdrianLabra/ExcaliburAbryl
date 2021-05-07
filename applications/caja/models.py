from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel

#applicaciones locales
from applications.inventarios.models import Productos
# Create your models here.



class CerrarCaja(TimeStampedModel):
    """
    Representa los cierres de caja
    """
    date_close = models.DateTimeField('Fecha de Cierre',)
    count = models.PositiveIntegerField('Cantidad de ventas',)
    amount = models.DecimalField('Monto total en ventas', max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='cajero', related_name="close_user")

    class Meta:
        verbose_name = 'Cierre Caja'
        verbose_name_plural = 'Cierres de Caja'

    def __str__(self):
        return str(self.user) + ' - ' + str(self.date_close)