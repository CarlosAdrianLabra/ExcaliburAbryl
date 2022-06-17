from django.db import models
from django.db.models import Q, Avg

# Filtro para almacen y tipo
class filtros(models.Manager):

    def filtros_calzado(self, **filters):
        consulta = self.filter(
            Q(barcode__icontains=filters['filtro']) | Q(marca__nombre__icontains=filters['filtro']) | Q(proveedor__nombre__icontains=filters['filtro']) | Q(modelo__icontains=filters['filtro'])
        ).filter(
            tipo='100' # 100 - CALZADO
        ).filter(
            almacen='1000' # 1000 - ALMACEN 1
        )

        return consulta
    
    def filtros_ropa(self, **filters):
        consulta = self.filter(
            Q(barcode__icontains=filters['filtro']) | Q(marca__nombre__icontains=filters['filtro']) | Q(proveedor__nombre__icontains=filters['filtro']) | Q(modelo__icontains=filters['filtro'])
        ).filter(
            tipo='200' # 200 - ROPA
        ).filter(
            almacen='1000' # 1000 - ALMACEN 1
        )

        return consulta
    
    def filtros_accesorios(self, **filters):
        consulta = self.filter(
            Q(barcode__icontains=filters['filtro']) | Q(marca__nombre__icontains=filters['filtro']) | Q(proveedor__nombre__icontains=filters['filtro']) | Q(modelo__icontains=filters['filtro'])
        ).filter(
            tipo='300' # 300 - ACCESORIOS
        ).filter(
            almacen='1000' # 1000 - ALMACEN 1
        )

        return consulta
    
    #
    # Calzado
    #

    # SIN USAR
    # def calzado_por_terminarse(self):
    #     consulta = self.filter(stock__lt=2).filter(
    #         tipo='100' # 100 - CALZADO
    #     )
    #     if consulta:
    #         return consulta
    #     else:
    #         return 0

    def calzado_mas_vendido(self):
        promedio = self.aggregate(Avg('num_venta'))
        if self.all():
            consulta = self.filter(num_venta__gt=promedio['num_venta__avg']).filter(
                tipo='100' # 100 - CALZADO
            )[:25]
            if promedio and consulta:
                return consulta
            else:
                return 0

        else:
            return 0

    def calzado_mas_vendido_c(self):
        promedio = self.aggregate(Avg('num_venta'))
        if self.all():
            consulta = self.filter(num_venta__gt=promedio['num_venta__avg']).filter(
                tipo='100' # 100 - CALZADO
            )
            if promedio and consulta:
                return consulta.count()
            else:
                return 0

        else:
            return 0

    # SIN USAR
    # def calzado_promedio(self):
    #     producto = self.all().filter(tipo='100')
    #     if producto:
    #         promedio = self.filter(tipo='100').aggregate(Avg('num_venta'))
    #         return round(promedio['num_venta__avg'])

    #     else:
    #         return 0
    
    def calzado_cantidad(self):
        producto = self.all().filter(tipo='100')
        if producto:
            return producto.count()
        else:
            return 0
            
    #
    # Ropa
    #

    # SIN USAR
    # def ropa_por_terminarse(self):
    #     consulta = self.filter(stock__lt=2).filter(
    #         tipo='200' # 200 - ROPA
    #     )
    #     if consulta:
    #         return consulta
    #     else:
    #         return 0

    def ropa_mas_vendida(self):
        promedio = self.aggregate(Avg('num_venta'))
        if self.all():
            consulta = self.filter(num_venta__gt=promedio['num_venta__avg']).filter(
                tipo='200' # 200 - ROPA
            )[:25]
            if promedio and consulta:
                return consulta
            else:
                return 0
        
        else:
            return 0
    
    def ropa_mas_vendida_c(self):
        promedio = self.aggregate(Avg('num_venta'))
        if self.all():
            consulta = self.filter(num_venta__gt=promedio['num_venta__avg']).filter(
                tipo='200' # 200 - ROPA
            )
            if promedio and consulta:
                return consulta.count()
            else:
                return 0
        else:
            return 0

    # SIN USAR
    # def ropa_promedio(self):
    #     producto = self.all().filter(tipo='200')
    #     if producto:
    #         promedio = self.filter(tipo='200').aggregate(Avg('num_venta'))
    #         return round(promedio['num_venta__avg'])

    #     else:
    #         return 0
        
    def ropa_cantidad(self):
        producto = self.all().filter(tipo='200')
        if producto:
            return producto.count()
        else:
            return 0

    #
    # Accesorios
    #

    # SIN USAR
    # def accesorios_por_terminarse(self):
    #     consulta = self.filter(stock__lt=2).filter(
    #         tipo='300' # 300 - ACCESORIOS
    #     )
    #     if consulta:
    #         return consulta
    #     else:
    #         return 0

    def accesorios_mas_vendidos(self):
        promedio = self.aggregate(Avg('num_venta'))
        if self.all():
            consulta = self.filter(num_venta__gt=promedio['num_venta__avg']).filter(
                tipo='300' # 300 - ACCESORIOS
            )[:25]
            if promedio and consulta:
                return consulta
            else:
                return 0

        else:
            return 0
    
    def accesorios_mas_vendidos_c(self):
        promedio = self.aggregate(Avg('num_venta'))
        if self.all():
            consulta = self.filter(num_venta__gt=promedio['num_venta__avg']).filter(
                tipo='300' # 300 - ACCESORIOS
            )
            if promedio and consulta:
                return consulta.count()
            else:
                return 0
        
        else:
            return 0

    # SIN USAR
    # def accesorios_promedio(self):
    #     producto = self.all().filter(tipo='300')
    #     if producto:
    #         promedio = self.filter(tipo='300').aggregate(Avg('num_venta'))
    #         return round(promedio['num_venta__avg'])

    #     else:
    #         return 0
    
    def accesorios_cantidad(self):
        producto = self.all().filter(tipo='300')
        if producto:
            return producto.count()
        else:
            return 0

    #
    # Interface Panel de Control
    #

    def productos_por_terminarse(self): # Administración - Ingresos_por_dia
        #
        consulta = self.filter(
           stock__lt=2
        )
        #
        if consulta:
            return consulta.count()
        else:
            return 0

    def productos_registrados(self):
        #
        consulta = self.all().count()
        #
        if consulta:
            return consulta
        else:
            return 0
    
    #
    # Interface Códigos de Barras
    #

    def filtros_para_etiqueta(self, **filters):

        consulta = self.filter(
            Q(barcode__icontains=filters['filtro']) | Q(marca__nombre__icontains=filters['filtro']) | Q(modelo__icontains=filters['filtro']) | Q(proveedor__nombre__icontains=filters['filtro'])
        ).filter(
            stock__gt=0
        )

        return consulta

    #
    # Promociones
    #

    def promociones_activas(self):
        consulta = self.all().exclude(promocion='0').order_by('-created')

        return consulta