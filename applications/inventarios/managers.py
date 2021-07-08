from django.db import models
from django.db.models import Q, Avg

# Filtro para almacen y tipo
class filtros(models.Manager):

    def filtros_calzado(self, **filters):

        consulta = self.filter(
            Q(barcode__icontains=filters['filtro']) | Q(nombre__icontains=filters['filtro']) | Q(marca__nombre__icontains=filters['filtro']) | Q(proveedor__nombre__icontains=filters['filtro'])
        ).filter(
            tipo='100' # 100 - CALZADO
        ).filter(
            almacen='1000' # 1000 - ALMACEN 1
        )

        return consulta
    
    def filtros_ropa(self, **filters):

        consulta = self.filter(
            Q(barcode__icontains=filters['filtro']) | Q(nombre__icontains=filters['filtro']) | Q(marca__nombre__icontains=filters['filtro']) | Q(proveedor__nombre__icontains=filters['filtro'])
        ).filter(
            tipo='200' # 200 - ROPA
        ).filter(
            almacen='1000' # 1000 - ALMACEN 1
        )

        return consulta
    
    def filtros_accesorios(self, **filters):

        consulta = self.filter(
            Q(barcode__icontains=filters['filtro']) | Q(nombre__icontains=filters['filtro']) | Q(marca__nombre__icontains=filters['filtro']) | Q(proveedor__nombre__icontains=filters['filtro'])
        ).filter(
            tipo='300' # 300 - ACCESORIOS
        ).filter(
            almacen='1000' # 1000 - ALMACEN 1
        )

        return consulta
    
    #
    # Calzado
    #

    def calzado_por_terminarse(self):
        #
        consulta = self.filter(
           stock__lt=10
        ).filter(
            tipo='100' # 100 - CALZADO
        )
        #
        return consulta

    def calzado_mas_vendido(self):
        #
        promedio = self.aggregate(Avg('num_venta'))
        consulta = self.filter(
            num_venta__gt=promedio['num_venta__avg']
        ).filter(
            tipo='100' # 100 - CALZADO
        )
        #
        return consulta
    
    def calzado_promedio(self):
        #
        producto = self.all().filter(
            tipo='100' # 100 - CALZADO
        )
        #
        if producto:
            promedio = self.filter(
                tipo='100' # 100 - CALZADO
            ).aggregate(Avg('num_venta'))

            return round(promedio['num_venta__avg'])
        #
        else:
            return 0
            
    #
    # Ropa
    #

    def ropa_por_terminarse(self):
        #
        consulta = self.filter(
           stock__lt=10
        ).filter(
            tipo='200' # 200 - ROPA
        )
        #
        return consulta

    def ropa_mas_vendida(self):
        #
        promedio = self.aggregate(Avg('num_venta'))
        consulta = self.filter(
            num_venta__gt=promedio['num_venta__avg']
        ).filter(
            tipo='200' # 200 - ROPA
        )
        #
        return consulta
    
    def ropa_promedio(self):
        #
        producto = self.all().filter(
            tipo='200' # 200 - ROPA
        )
        #
        if producto:
            promedio = self.filter(
                tipo='200' # 200 - ROPA
            ).aggregate(Avg('num_venta'))
            
            return round(promedio['num_venta__avg'])
        #
        else:
            return 0

    #
    # Accesorios
    #

    def accesorios_por_terminarse(self):
        #
        consulta = self.filter(
           stock__lt=10
        ).filter(
            tipo='300' # 300 - ACCESORIOS
        )
        #
        return consulta

    def accesorios_mas_vendidos(self):
        #
        promedio = self.aggregate(Avg('num_venta'))
        consulta = self.filter(
            num_venta__gt=promedio['num_venta__avg']
        ).filter(
            tipo='300' # 300 - ACCESORIOS
        )
        #
        return consulta
    
    def accesorios_promedio(self):
        #
        producto = self.all().filter(
            tipo='300' # 300 - ACCESORIOS
        )
        #
        if producto:
            promedio = self.filter(
                tipo='300' # 300 - ACCESORIOS
            ).aggregate(Avg('num_venta'))
            
            return round(promedio['num_venta__avg'])
        #
        else:
            return 0

    #
    # Interface Panel de Control
    #

    def productos_por_terminarse(self):
        #
        consulta = self.filter(
           stock__lt=10
        )
        if consulta:
            return consulta
        else:
            return 0
    
    #
    # Interface Códigos de Barras
    #

    def filtros_barras(self, **filters):

        consulta = self.filter(
            Q(barcode__icontains=filters['filtro']))


        return consulta