from django.db import models
from django.db.models import Q

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
    
    def productos_en_inventario(self):
        #
        consulta = self.filter(
           stock__lt=10
        )
        #
        return consulta