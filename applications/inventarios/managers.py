from django.db import models
from django.db.models import Q, Avg

# Filtro para almacen y tipo
class filtros(models.Manager):

    def almacen_tipo_calzado(self, filtro):

        consulta = self.filter(
            Q(barcode__icontains=filtro) | Q(nombre__icontains=filtro) | Q(marca__nombre__icontains=filtro) | Q(proveedor__nombre__icontains=filtro) | Q(modelo__icontains=filtro)
        ).filter(
            tipo='10' # 10 - CALZADO
        ).filter(
            almacen='10' # 10 - ALMACEN 1
        )

        return consulta
    
    def almacen_tipo_ropa(self, filtro):

        consulta = self.filter(
            Q(barcode__icontains=filtro) | Q(nombre__icontains=filtro) | Q(marca__nombre__icontains=filtro) | Q(proveedor__nombre__icontains=filtro) | Q(modelo__icontains=filtro)
        ).filter(
            tipo='20' # 20 - ROPA
        ).filter(
            almacen='10' # 10 - ALMACEN 1
        )

        return consulta

    # Interface Inventarios Index
    # Calzado
    def calzado_por_terminarse(self):
        #
        consulta = self.filter(
           stock__lt=10
        ).filter(
            tipo='10' # 10 - CALZADO
        )
        #
        return consulta

    def calzado_mas_vendido(self):
        #
        promedio = self.aggregate(Avg('num_venta'))
        consulta = self.filter(
            num_venta__gt=promedio['num_venta__avg']
        ).filter(
            tipo='10' # 10 - CALZADO
        )
        #
        return consulta
    
    def calzado_promedio(self):
        #
        producto = self.all().filter(
            tipo='10' # 10 - CALZADO
        )
        #
        if producto:
            promedio = self.filter(
                tipo='10' # 10 - CALZADO
            ).aggregate(Avg('num_venta'))

            return round(promedio['num_venta__avg'])
        #
        else:
            return 0
    
    # Ropa
    def ropa_por_terminarse(self):
        #
        consulta = self.filter(
           stock__lt=10
        ).filter(
            tipo='20' # 20 - ROPA
        )
        #
        return consulta

    def ropa_mas_vendida(self):
        #
        promedio = self.aggregate(Avg('num_venta'))
        consulta = self.filter(
            num_venta__gt=promedio['num_venta__avg']
        ).filter(
            tipo='20' # 20 - ROPA
        )
        #
        return consulta
    
    def ropa_promedio(self):
        #
        producto = self.all().filter(
            tipo='20' # 20 - ROPA
        )
        #
        if producto:
            promedio = self.filter(
                tipo='20' # 20 - ROPA
            ).aggregate(Avg('num_venta'))
            
            return round(promedio['num_venta__avg'])
        #
        else:
            return 0