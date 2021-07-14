#
from django.db.models import Prefetch, F, FloatField, ExpressionWrapper
#
from applications.ventas.models import Venta, DetalleVenta

def detalle_ventas_no_cerradas():
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
    