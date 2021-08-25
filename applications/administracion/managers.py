from django.db import models
from django.db.models import Q, Sum, F, ExpressionWrapper
from django.db.models.fields import FloatField

class GastosManager(models.Manager):
    #Managers para gastos

    def listar_gastos(self):
        resultado=self.order_by('fecha')
        return resultado

class ResultadoManager(models.Manager):

    def listar_resultados(self):
        
        consulta=self.filter(
            ventas__sale__anulate=False,
            ventas__sale__close=True,
            ventas__sale__date_sale__range=('2021-01-01','2021-12-31'),
            gastos__fecha__range=['2021-01-01','2021-12-31'],
        ).values(
            'ingresos','gasto'
        ).annotate(
            totalventas=Sum('ingresos__price_subtotal'),
            totalgastos=Sum('gasto__gastosTotales'),
            resultado=ExpressionWrapper(F(Sum('ingresos__price_subtotal'))-F(Sum('gasto__gastosTotales')),output_field=FloatField())
        )
        return consulta