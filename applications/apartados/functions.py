from django.utils import timezone
from django.db.models import Prefetch

from applications.inventarios.models import Productos
from applications.ventas.models import Venta, DetalleVenta, Carrito
from .models import Apartados

def pre_apartado(self, **params_apartado):
    productos_pos = Carrito.objects.all()

    if productos_pos.count() > 0 and Carrito.objects.filter(producto__stock__gt=0):

        detalle_apartados = []
        productos_apartado = []

        for pre_apart in productos_pos:
            detalle_apartado = Apartados(
                barcode = pre_apart.producto.barcode,
                monto_pagado = params_apartado['monto_pagado'],
                fecha=timezone.now(),
                precio_producto=pre_apart.producto.precio_venta
            )
            producto = pre_apart.producto
            producto.stock = producto.stock - pre_apart.count

        detalle_apartados.append(detalle_apartado)
        productos_apartado.append(producto)

        Apartados.objects.bulk_create(detalle_apartados)
        Productos.objects.bulk_update(productos_apartado, ['stock'])

        productos_pos.delete()

        return detalle_apartado

    else:
        return None


def procesar_venta_apartado(self, **params_apartado):
    # recupera la lista de productos en carrito
    productos_en_car = Carrito.objects.all()

    # crea el objeto venta
    venta = Venta.objects.create(
        date_sale=timezone.now(),
        count=0,
        amount=0,
        type_invoice=params_apartado['type_invoice'],
        type_payment=params_apartado['type_payment'],
        user=params_apartado['user'],
    )
    #
    ventas_detalle = []
    productos_en_venta = []

    for p_c in productos_en_car:
        #
        venta_detalle = DetalleVenta(
            producto=p_c.producto,
            sale=venta,
            count=p_c.count,
            price_purchase=p_c.producto.precio_compra,
            price_sale=p_c.producto.precio_venta,
            price_subtotal=p_c.producto.precio_venta,
            promocion='0',
            discount='0',
            tax=0.16,
        )
        # actualizamos la venta del inventario
        producto = p_c.producto
        producto.num_venta = producto.num_venta + p_c.count
        #
        ventas_detalle.append(venta_detalle)
        productos_en_venta.append(producto)
        #
        venta.count = venta.count + p_c.count
        venta.amount = p_c.producto.precio_venta

        venta.save()

        DetalleVenta.objects.bulk_create(ventas_detalle)
        # actualizamos la venta
        Productos.objects.bulk_update(productos_en_venta, ['num_venta'])
        # completada la venta, eliminamos productos del carrito
        productos_en_car.delete()
        Apartados.objects.filter(apartado_cerrado=True, apartado_venta=False).update(apartado_venta=True)

        return venta


def cancelar_venta_apartado(self, **params_apartado):
    # recupera la lista de productos en carrito
    productos_en_car = Carrito.objects.all()

    # crea el objeto venta
    venta = Venta.objects.create(
        date_sale=timezone.now(),
        count=0,
        amount=0,
        type_invoice=params_apartado['type_invoice'],
        type_payment=params_apartado['type_payment'],
        user=params_apartado['user'],
    )
    #
    ventas_detalle = []
    productos_en_venta = []

    for p_c in productos_en_car:
        #
        venta_detalle = DetalleVenta(
            producto=p_c.producto,
            sale=venta,
            count=p_c.count,
            price_purchase=p_c.producto.precio_compra,
            price_sale=p_c.producto.precio_venta,
            price_subtotal=params_apartado['monto_pagado'],
            promocion='0',
            discount='0',
            tax=0.16,
        )
        # actualizamos la venta del inventario
        producto = p_c.producto
        producto.num_venta = producto.num_venta + p_c.count
        #
        ventas_detalle.append(venta_detalle)
        productos_en_venta.append(producto)
        #
        venta.count = venta.count + p_c.count
        venta.amount = params_apartado['monto_pagado']

        venta.save()

        DetalleVenta.objects.bulk_create(ventas_detalle)
        # actualizamos la venta
        Productos.objects.bulk_update(productos_en_venta, ['num_venta'])
        # completada la venta, eliminamos productos del carrito
        productos_en_car.delete()
        Apartados.objects.filter(apartado_cerrado=False, apartado_venta=False).update(apartado_cerrado=True, apartado_venta=True)

        return venta