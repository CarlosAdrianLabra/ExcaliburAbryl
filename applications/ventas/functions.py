from django.utils import timezone
from django.db.models import Prefetch

from applications.inventarios.models import Productos

from .models import Venta, DetalleVenta, Carrito, Efectivo


def procesar_venta(self, **params_venta):
    # recupera la lista de productos en carrtio
    productos_en_car = Carrito.objects.all()
    total_de_venta = Carrito.objects.total_cobrar()
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
        for p_c in productos_en_car:
            venta_detalle = DetalleVenta(
                producto=p_c.producto,
                sale=venta,
                count=p_c.count,
                price_purchase=p_c.producto.precio_compra,
                price_sale=p_c.producto.precio_venta,
                price_subtotal=p_c.subtotal(),
                tax=0.16,
            )
            # actualizmos stok de producto en iteracion
            producto = p_c.producto
            producto.stock = producto.stock - p_c.count
            producto.num_venta = producto.num_venta + p_c.count
            #
            ventas_detalle.append(venta_detalle)
            productos_en_venta.append(producto)
            #
            venta.count = venta.count + p_c.count
            venta.amount = total_de_venta

        # for p_c in productos_en_car:
        #     venta_detalle = DetalleVenta(
        #         producto=p_c.producto,
        #         sale=venta,
        #         count=p_c.count,
        #         price_purchase=p_c.producto.precio_compra,
        #         price_sale=p_c.producto.precio_venta,
        #         tax=0.16,
        #     )
        #     # actualizmos stok de producto en iteracion
        #     producto = p_c.producto
        #     producto.stock = producto.stock - p_c.count
        #     producto.num_venta = producto.num_venta + p_c.count
        #     #
        #     ventas_detalle.append(venta_detalle)
        #     productos_en_venta.append(producto)
        #     #
        #     venta.count = venta.count + p_c.count
        #     #venta.amount = venta.amount + p_c.count*p_c.producto.precio_venta
        #     venta.amount = total_de_venta

        venta.save()
        DetalleVenta.objects.bulk_create(ventas_detalle)
        # actualizamos el stok
        Productos.objects.bulk_update(productos_en_venta, ['stock', 'num_venta'])
        # completada la venta, eliminamos productos delc arrito
        productos_en_car.delete()
        return venta
    else:
        return None
    