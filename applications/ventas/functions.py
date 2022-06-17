from django.contrib import messages
from django.utils import timezone
from django.db.models import Prefetch
from applications.inventarios.models import Productos
from .models import Venta, DetalleVenta, Carrito


def procesar_venta(self, **params_venta):
    # Recupera la lista de productos en carrtio
    productos_en_car = Carrito.objects.all()
    total_de_venta = Carrito.objects.total_cobrar()
    if productos_en_car.count() > 0 and Carrito.objects.filter(producto__stock__gt=0):

        sub_10:float = 0
        for p in productos_en_car:
            if p.producto.promocion=='7':
                sub_10 += float(p.producto.precio_venta * p.count) - float(p.producto.precio_venta * p.count)*float(0.10)
            else:
                sub_10 += float(p.producto.precio_venta * p.count)

        # Crea el objeto venta
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

        if sub_10 == total_de_venta:
            for p_c in productos_en_car:
                #
                subtotal = ""
                subtotal = str(p_c.subtotal())
                #
                if p_c.producto.promocion=='7':
                    venta_detalle = DetalleVenta(
                        producto=p_c.producto,
                        sale=venta,
                        count=p_c.count,
                        price_purchase=p_c.producto.precio_compra,
                        price_sale=p_c.producto.precio_venta,
                        price_subtotal=float(p_c.producto.precio_venta * p_c.count) - float(p_c.producto.precio_venta * p_c.count)*float(0.10),
                        promocion=p_c.producto.promocion,
                        discount=float(p_c.producto.precio_venta * p_c.count) - float(p_c.producto.precio_venta * p_c.count) - float(p_c.producto.precio_venta * p_c.count)*float(0.10),
                        tax=0.16,
                    )
                else:
                    venta_detalle = DetalleVenta(
                        producto=p_c.producto,
                        sale=venta,
                        count=p_c.count,
                        price_purchase=p_c.producto.precio_compra,
                        price_sale=p_c.producto.precio_venta,
                        price_subtotal=p_c.subtotal(),
                        promocion=p_c.producto.promocion,
                        discount=float(p_c.producto.precio_venta * p_c.count) - float(subtotal),
                        tax=0.16,
                    )
                # Actualizamos stock de producto en iteracion
                producto = p_c.producto
                producto.stock = producto.stock - p_c.count
                producto.num_venta = producto.num_venta + p_c.count
                #
                ventas_detalle.append(venta_detalle)
                productos_en_venta.append(producto)
                #
                venta.count = venta.count + p_c.count
                venta.amount = total_de_venta
        else:
            for p_c in productos_en_car:
                #
                subtotal = ""
                subtotal = str(p_c.subtotal())
                #
                venta_detalle = DetalleVenta(
                    producto=p_c.producto,
                    sale=venta,
                    count=p_c.count,
                    price_purchase=p_c.producto.precio_compra,
                    price_sale=p_c.producto.precio_venta,
                    price_subtotal=p_c.subtotal(),
                    promocion=p_c.producto.promocion,
                    discount=float(p_c.producto.precio_venta * p_c.count) - float(subtotal),
                    tax=0.16,
                )
                # Actualizamos stock de producto en iteracion
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
        try:
            # Actualizamos el stock
            Productos.objects.bulk_update(productos_en_venta, ['stock', 'num_venta'])
            DetalleVenta.objects.bulk_create(ventas_detalle)
            # Completada la venta, eliminamos productos del carrito
            productos_en_car.delete()
            #
            return venta

        except Exception:
            productos_en_car.delete()
            venta = Venta.objects.last()
            venta.delete()
            return messages.add_message(self.request, messages.ERROR, '¡No se logró procesar la venta. El producto no cuenta con suficientes existencias en el inventario!')

    else:
        return None