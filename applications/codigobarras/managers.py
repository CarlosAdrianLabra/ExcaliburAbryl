from django.db import models
from django.db.models import Q, Avg



class filtros(models.Manager):

    def filtros_barras(self, **filters):

        consulta = self.filter(
            Q(barcode__icontains=filters['filtro']))


        return consulta