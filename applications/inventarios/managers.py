from django.db import models
from django.db.models import Q, Avg

# Filtro para almacen y tipo
class filtros(models.Manager):

    def almacen_tipo_calzado(self, filtro):

        consulta = self.filter(
            Q(barcode__icontains=filtro) | Q(nombre__icontains=filtro) | Q(marca__nombre__icontains=filtro)| Q(proveedor__nombre__icontains=filtro)
        ).filter(
            tipo='0' # 0 - CALZADO
        ).filter(
            almacen='0' # 0 - ALMACEN 1
        )

        return consulta
    
    def almacen_tipo_ropa(self, filtro):

        consulta = self.filter(
            Q(barcode__icontains=filtro) | Q(nombre__icontains=filtro) | Q(marca__nombre__icontains=filtro)| Q(proveedor__nombre__icontains=filtro)
        ).filter(
            tipo='1' # 1 - ROPA
        ).filter(
            almacen='0' # 0 - ALMACEN 1
        )

        return consulta

    # Interface Inventarios Index
    # Calzado
    def calzado_por_terminarse(self):
        #
        consulta = self.filter(
           stock__lt=10
        ).filter(
            tipo='0' # 0 - CALZADO
        )
        #
        return consulta

    def calzado_mas_vendido(self):
        #
        promedio = self.aggregate(Avg('num_venta'))
        consulta = self.filter(
            num_venta__gt=promedio['num_venta__avg']
        ).filter(
            tipo='0' # 0 - CALZADO
        )
        #
        return consulta
    
    def calzado_promedio(self):
        #
        promedio = self.filter(
            tipo='0' # 0 - CALZADO
        ).aggregate(Avg('num_venta'))

        return round(promedio['num_venta__avg'])
    
    # Ropa
    def ropa_por_terminarse(self):
        #
        consulta = self.filter(
           stock__lt=10
        ).filter(
            tipo='1' # 1 - ROPA
        )
        #
        return consulta

    def ropa_mas_vendida(self):
        #
        promedio = self.aggregate(Avg('num_venta'))
        consulta = self.filter(
            num_venta__gt=promedio['num_venta__avg']
        ).filter(
            tipo='1' # 1 - ROPA
        )
        #
        return consulta
    
    def ropa_promedio(self):
        #
        promedio = self.filter(
            tipo='1' # 1 - ROPA
        ).aggregate(Avg('num_venta'))

        return round(promedio['num_venta__avg'])