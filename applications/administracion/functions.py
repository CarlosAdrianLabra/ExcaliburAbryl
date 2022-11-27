#
from django.db.models import Prefetch, F, FloatField, ExpressionWrapper
#
from applications.ventas.models import Venta, DetalleVenta


def detalle_resumen_ventas(date_start, date_end): # Administración - Detalle de ventas
    # Función que recupera ventas no anuladas en rango de fechas
    # y el detalle de cada venta
    
    if date_start and date_end:
        ventas = Venta.objects.ventas_en_fechas(date_start, date_end)
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
    else:
        return []

def detalle_completo(date_start, date_end, caja, tipo): # Administración - Detalle completo
    print(tipo)
    if date_start and date_end and caja and tipo:
        
        if caja == '1' and tipo == '3':
            ventas = Venta.objects.ventas_en_fechas(date_start, date_end).filter(caja='1')
        elif caja == '1':
            ventas = Venta.objects.ventas_en_fechas(date_start, date_end).filter(caja='1', type_payment=tipo)

        elif caja == '2' and tipo == '3':
            ventas = Venta.objects.ventas_en_fechas(date_start, date_end).filter(caja='2')
        elif caja == '2':
            ventas = Venta.objects.ventas_en_fechas(date_start, date_end).filter(caja='2', type_payment=tipo)

        elif caja == '3' and tipo == '3':
            ventas = Venta.objects.ventas_en_fechas(date_start, date_end)
        elif caja == '3':
            ventas = Venta.objects.ventas_en_fechas(date_start, date_end).filter(type_payment=tipo)

        consulta = ventas.prefetch_related(Prefetch('detail_sale', queryset=DetalleVenta.objects.filter(sale__id__in=ventas)))

        return consulta
    
    else: return []