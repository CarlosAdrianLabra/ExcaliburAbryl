from django.db import models

class CarShopManager(models.Manager):
    """ procedimiento modelo Carrito de compras """
    
    def total_cobrar(self):
        
        total = 0
        promo_10 = 0
        productos_10 = self.filter(producto__promocion='7')
        #
        if productos_10:
            np = productos_10.count()
        else:
            np = 0

        if np >= 2 and productos_10:
            for productos in productos_10:
                promo_10 += (float(productos.subtotal()) * 0.10)
        if productos_10:
            for productos in self.all():
                total += float(productos.subtotal())
        else:
            for productos in self.all():
                total += float(productos.subtotal())

        return total - promo_10