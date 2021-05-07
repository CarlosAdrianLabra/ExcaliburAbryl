from django.utils import timezone
from django.db.models import Prefetch

from applications.inventarios.models import Productos

from .models import Venta, DetalleVenta, Carrito


def procesar_venta(self, **params_venta):
    # recupera la lista de productos en carrtio
    productos_en_car = Carrito.objects.all()
    if productos_en_car.count() > 0:
        
        # crea el objeto venta
        venta = Venta.objects.create(
            date_sale=timezone.now(),
            count=0,
            amount=0,
            type_invoice=params_venta['type_invoice'],
            type_payment=params_venta['type_payment'],
            user=params_venta['user'],
        )
        #
        ventas_detalle = []
        productos_en_venta = []
        for producto_car in productos_en_car:
            venta_detalle = DetalleVenta(
                producto=producto_car.producto,
                sale=venta,
                count=producto_car.count,
                price_purchase=producto_car.producto.precio_compra,
                price_sale=producto_car.producto.precio_venta,
                tax=0.16,
            )
            # actualizmos stok de producto en iteracion
            producto = producto_car.producto
            producto.stock = producto.stock - producto_car.count
            producto.num_venta = producto.num_venta + producto_car.count
            #
            ventas_detalle.append(venta_detalle)
            productos_en_venta.append(producto)
            #
            venta.count = venta.count + producto_car.count
            venta.amount = venta.amount + producto_car.count*producto_car.producto.precio_venta

        venta.save()
        DetalleVenta.objects.bulk_create(ventas_detalle)
        # actualizamos el stok
        Productos.objects.bulk_update(productos_en_venta, ['stock', 'num_venta'])
        # completada la venta, eliminamos productos delc arrito
        productos_en_car.delete()
        return venta
    else:
        return None
    