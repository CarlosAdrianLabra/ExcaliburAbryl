from datetime import datetime, timedelta
#from decimal import Decimal
#from django.db.models.fields import DecimalField
from django.utils import timezone
from django.db import models
#from django.views.generic import detail

from applications.inventarios.models import Productos

from django.db.models import Q, Sum, F, FloatField, ExpressionWrapper
from django.db.models.functions import Upper

class SaleManager(models.Manager):
    """ procedimiento para modelo venta """
    fecha_hoy = datetime.now()
    mes_actual = fecha_hoy.month
    ano_actual = fecha_hoy.year
    
    def ventas_no_cerradas(self):
        # creamos rango de fecha
        return self.filter(
            close=False,
            anulate=False
        )
    
    def total_ventas_dia(self):
        consulta = self.filter(
            close=False,
            anulate=False
        ).aggregate(
            total=Sum('amount')
        )
        if consulta['total']:
            return consulta['total']
        else:
            return 0
    
    def total_ventas_anuladas_dia(self):
        consulta = self.filter(
            close=False,
            anulate=True,
            
        ).aggregate(
            total=Sum('amount')
        )
        if consulta['total']:
            return consulta['total']
        else:
            return 0
    
    def cerrar_ventas(self):
        consulta = self.filter(
            close=False,
        )
        # actualizmos a cerrado
        total = consulta.aggregate(
            total=Sum('amount')
        )['total']
        cerrados = consulta.update(close=True) # devuelve numero de actualizciones

        return cerrados, total
    
    def total_ventas(self):
        return self.filter(
            anulate=False,
        ).aggregate(
            total=Sum('amount')
        )['total']
    
    def ventas_en_fechas(self, date_start, date_end):
        return self.filter(
            anulate=False,
            date_sale__range=(date_start, date_end),
        ).order_by('-date_sale')

    def monto_total_ventas(self):
        #
        consulta = self.filter(
            anulate=False,
        ).aggregate(
            total=Sum('amount')
        )
        #
        return consulta['total']

    def total_ventas_no_cerradas(self):
        #
        consulta = self.filter(
            anulate=False
        ).count()
        #
        return consulta

    def costo_total(self):
        #
        consulta = self.filter(
            anulate=False
        ).aggregate(
            #total=Sum('detail_sale__producto__precio_compra')
            total=Sum(F('detail_sale__price_purchase')*F('detail_sale__count'),output_field=FloatField())
        )
        return consulta['total']

    def monto_ventas_mes(self):
        if str(self.mes_actual) == '1':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-01-01 00:00:00.100000-0500", str(self.ano_actual)+"-01-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            return consulta['total']
        if str(self.mes_actual) == '2':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-02-01 00:00:00.100000-0500", str(self.ano_actual)+"-02-28 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            return consulta['total']
        if str(self.mes_actual) == '3':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-03-01 00:00:00.100000-0500", str(self.ano_actual)+"-03-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            return consulta['total']
        if str(self.mes_actual) == '4':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-04-01 00:00:00.100000-0500", str(self.ano_actual)+"-04-30 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            return consulta['total']
        if str(self.mes_actual) == '5':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-05-01 00:00:00.100000-0500", str(self.ano_actual)+"-05-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            return consulta['total']
        if str(self.mes_actual) == '6':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-06-01 00:00:00.100000-0500", str(self.ano_actual)+"-06-30 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            return consulta['total']
        if str(self.mes_actual) == '7':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-07-01 00:00:00.100000-0500", str(self.ano_actual)+"-07-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            return consulta['total']
        if str(self.mes_actual) == '8':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-08-01 00:00:00.100000-0500", str(self.ano_actual)+"-08-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            return consulta['total']
        if str(self.mes_actual) == '9':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-09-01 00:00:00.100000-0500", str(self.ano_actual)+"-09-30 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            return consulta['total']
        if str(self.mes_actual) == '10':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-10-01 00:00:00.100000-0500", str(self.ano_actual)+"-10-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            return consulta['total']
        if str(self.mes_actual) == '11':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-11-01 00:00:00.100000-0500", str(self.ano_actual)+"-11-30 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            return consulta['total']
        if str(self.mes_actual) == '12':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-12-01 00:00:00.100000-0500", str(self.ano_actual)+"-12-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            return consulta['total']

    def v_enero(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-01-01 00:00:00.100000-0500", str(self.ano_actual)+"-01-31 23:59:59.100000-0500"]).count()
        return consulta
    def m_enero(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-01-01 00:00:00.100000-0500", str(self.ano_actual)+"-01-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
        return consulta['total']
    
    def v_febrero(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-02-01 00:00:00.100000-0500", str(self.ano_actual)+"-02-28 23:59:59.100000-0500"]).count()
        return consulta
    def m_febrero(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-02-01 00:00:00.100000-0500", str(self.ano_actual)+"-02-28 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
        return consulta['total']
    
    def v_marzo(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-03-01 00:00:00.100000-0500", str(self.ano_actual)+"-03-31 23:59:59.100000-0500"]).count()
        return consulta
    def m_marzo(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-03-01 00:00:00.100000-0500", str(self.ano_actual)+"-03-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
        return consulta['total']
    
    def v_abril(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-04-01 00:00:00.100000-0500", str(self.ano_actual)+"-04-30 23:59:59.100000-0500"]).count()
        return consulta
    def m_abril(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-04-01 00:00:00.100000-0500", str(self.ano_actual)+"-04-30 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
        return consulta['total']
    
    def v_mayo(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-05-01 00:00:00.100000-0500", str(self.ano_actual)+"-05-31 23:59:59.100000-0500"]).count()
        return consulta
    def m_mayo(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-05-01 00:00:00.100000-0500", str(self.ano_actual)+"-05-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
        return consulta['total']
    
    def v_junio(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-06-01 00:00:00.100000-0500", str(self.ano_actual)+"-06-30 23:59:59.100000-0500"]).count()
        return consulta
    def m_junio(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-06-01 00:00:00.100000-0500", str(self.ano_actual)+"-06-30 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
        return consulta['total']
    
    def v_julio(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-07-01 00:00:00.100000-0500", str(self.ano_actual)+"-07-31 23:59:59.100000-0500"]).count()
        return consulta
    def m_julio(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-07-01 00:00:00.100000-0500", str(self.ano_actual)+"-07-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
        return consulta['total']
    
    def v_agosto(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-08-01 00:00:00.100000-0500", str(self.ano_actual)+"-08-31 23:59:59.100000-0500"]).count()
        return consulta
    def m_agosto(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-08-01 00:00:00.100000-0500", str(self.ano_actual)+"-08-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
        return consulta['total']
    
    def v_septiembre(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-09-01 00:00:00.100000-0500", str(self.ano_actual)+"-09-30 23:59:59.100000-0500"]).count()
        return consulta
    def m_septiembre(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-09-01 00:00:00.100000-0500", str(self.ano_actual)+"-09-30 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
        return consulta['total']
    
    def v_octubre(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-10-01 00:00:00.100000-0500", str(self.ano_actual)+"-10-31 23:59:59.100000-0500"]).count()
        return consulta
    def m_octubre(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-10-01 00:00:00.100000-0500", str(self.ano_actual)+"-10-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
        return consulta['total']
    
    def v_noviembre(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-11-01 00:00:00.100000-0500", str(self.ano_actual)+"-11-30 23:59:59.100000-0500"]).count()
        return consulta
    def m_noviembre(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-11-01 00:00:00.100000-0500", str(self.ano_actual)+"-11-30 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
        return consulta['total']
    
    def v_diciembre(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-12-01 00:00:00.100000-0500", str(self.ano_actual)+"-12-31 23:59:59.100000-0500"]).count()
        return consulta
    def m_diciembre(self):
        consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-12-01 00:00:00.100000-0500", str(self.ano_actual)+"-12-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
        return consulta['total']

class SaleDetailManager(models.Manager):
    """ procedimiento modelo product """
    
    def detalle_por_venta(self, id_venta):
        return self.filter(
            sale__id=id_venta
        )

    def ventas_mes_producto(self, id_prod):
        # creamos rango de fecha
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        consulta = self.filter(
            sale__anulate=False,
            created__range=(start_date, end_date),
            producto__pk=id_prod,
        ).values('sale__date_sale__date', 'producto__nombre').annotate(
            cantidad_vendida=Sum('count'),
        )
        return consulta
    
    def restablecer_stok_num_ventas(self, id_venta):
        prods_en_anulados = []
        for venta_detail in self.filter(sale__id=id_venta):
            #actualizmos producto
            venta_detail.producto.stock = venta_detail.producto.stock + venta_detail.count
            venta_detail.producto.num_venta = venta_detail.producto.num_venta - venta_detail.count
            prods_en_anulados.append(venta_detail.producto)
        Productos.objects.bulk_update(prods_en_anulados, ['stock', 'num_venta'])
        return True
    
    def resumen_ventas(self):
        return self.filter(
            sale__anulate=False,
            sale__close=True,
        ).values('sale__date_sale__date').annotate(
            total_vendido=Sum(
                F('price_subtotal'),
                # F('price_sale')*F('count'),
                output_field=FloatField()
            ),
            total_ganancias=Sum(
                F('price_subtotal') - F('price_purchase')*F('count'),
                # F('price_sale')*F('count') - F('price_purchase')*F('count'),
                output_field=FloatField()
            ),
            num_ventas=Sum('count'),
        )
    
    def resumen_ventas_mes(self):
        #
        return self.filter(
            sale__anulate=False
        ).values('sale__date_sale__date__month', 'sale__date_sale__date__year').annotate(
            cantidad_ventas=Sum('count'),
            total_ventas=Sum(F('price_subtotal'), output_field=FloatField()),
            # total_ventas=Sum(F('price_sale')*F('count'), output_field=FloatField()),
            ganancia_total=Sum(
                F('price_subtotal') - F('price_purchase')*F('count'),output_field=FloatField()
                # F('price_sale')*F('count') - F('price_purchase')*F('count'),output_field=FloatField()
            )
        ).order_by('-sale__date_sale__date__month')
    
    def resumen_ventas_proveedor(self, **filters):
        # recibe 3 parametros en un diccionario
        # devuelve lista de ventas en rango de fechas de un proveedor
        # y, devuelve el total de ventas en rango de fechas y de proveedor

        if filters['date_start'] and filters['date_end'] and filters['proveedor']:
            consulta = self.filter(
                anulate=False,
                sale__close=True,
                sale__date_sale__range = (
                    filters['date_start'],
                    filters['date_end'],
                ),
                producto__proveedor__pk=filters['proveedor'],
            )
            
            lista_ventas = consulta.annotate(
                sub_total=ExpressionWrapper(
                    F('price_subtotal'),
                    # F('price_purchase')*F('count'),
                    output_field=FloatField()
                ),
                total_pagar=ExpressionWrapper(
                    F('price_subtotal') - F('price_purchase'),
                    output_field=FloatField()
                )
            ).order_by('sale__date_sale')

            total_ventas = consulta.aggregate(
                total_venta=Sum(
                    F('price_subtotal') - F('price_purchase'),
                    # F('price_purchase')*F('count'),
                    output_field=FloatField()
                )
            )['total_venta']

            return lista_ventas, total_ventas
        else:
            return [], 0
    
    def ganancias_totales(self):
        costo = self.filter(anulate=False, sale__close=True).aggregate(
            total=Sum(
                F('price_subtotal') - F('count')*F('price_purchase'),
                output_field=FloatField()
            )
        )
        return costo['total']

    def reporte8020_producto(self):
        resultado=self.filter(
            anulate=False, sale__close=True
        ).values(
            'producto'
        ).annotate(
            nombre=Upper('producto__nombre'),
            modelo=Upper('producto__modelo'),
            color=Upper('producto__color'),
            num_ventas=Sum('count'),
            total_ventas=Sum('price_subtotal')
        ).order_by('-total_ventas')
        return resultado

class CarShopManager(models.Manager):
    """ procedimiento modelo Carrito de compras """
    
    def total_cobrar(self):
        
        total = 0
        promo_10 = 0
        if self.filter(producto__promocion='7'):
            np = self.filter(producto__promocion='7').count()
        else:
            np = 0

        if np >= 2 and self.filter(producto__promocion='7'):
            for productos in self.filter(producto__promocion='7'):
                promo_10 += (float(productos.subtotal()) * 0.10)
        if self.filter(producto__promocion='7'):
            for productos in self.all():
                total += float(productos.subtotal())
        else:
            for productos in self.all():
                total += float(productos.subtotal())

        return total - promo_10

        # consulta = self.aggregate(
        #     total=Sum(
        #         F('count')*F('producto__precio_venta'),
        #         output_field=FloatField()
        #     ),
        # )
        # if consulta['total']:
        #     return consulta['total']
        # else:
        #     return 0