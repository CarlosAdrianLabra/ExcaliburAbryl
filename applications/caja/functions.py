#
from django.db.models import Prefetch, F, FloatField, ExpressionWrapper
#
from applications.ventas.models import Venta, DetalleVenta

def detalle_ventas_no_cerradas(): # Cierre de caja / Punto de venta - voucher
    # recuepramos arry de id de ventas no cerradas
    ventas = Venta.objects.ventas_no_cerradas()
    consulta = ventas.prefetch_related(
        Prefetch(
            'detail_sale', 
            queryset=DetalleVenta.objects.filter(sale__id__in=ventas)
            # .annotate(
            #     subtotal=ExpressionWrapper(
            #         F('price_sale')*F('count'),
            #         output_field=FloatField()
            #     )
            # )
        )
    )

    return consulta


def detalle_ventas_no_cerradas_2(): # Cierre de caja / Punto de venta - voucher
    # recuepramos arry de id de ventas no cerradas
    ventas = Venta.objects.ventas_no_cerradas_2()
    consulta = ventas.prefetch_related(
        Prefetch(
            'detail_sale', 
            queryset=DetalleVenta.objects.filter(sale__id__in=ventas)
        )
    )

    return consulta