from django.db import models


class GastosManager(models.Manager):
    #Managers para gastos

    def listar_gastos(self):
        resultado=self.order_by('fecha')
        return resultado

