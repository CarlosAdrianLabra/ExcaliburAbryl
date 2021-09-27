from django.utils import timezone
from django.db.models import Prefetch

from applications.inventarios.models import Productos
from applications.ventas.models import Venta, DetalleVenta, Carrito
from .models import Apartados

def pre_apartado(self, **params_apartado):
    productos_pos = Carrito.objects.all()
    total_venta = Carrito.objects.total_cobrar()

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