from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from applications.inventarios.models import Productos, Movimientos
from django.db.models import Q, Sum, F, FloatField, IntegerField, ExpressionWrapper, Count
from django.db.models.functions import Upper

class SaleManager(models.Manager):
    """ procedimiento para modelo venta """
    fecha_hoy = datetime.now()
    mes_actual = fecha_hoy.month
    ano_actual = fecha_hoy.year
    
    #
    # Tezonco Caja 1
    #

    def ventas_no_cerradas(self): # Cierre de caja
        return self.filter(close=False,anulate=False,caja='1')
    
    def total_ventas_dia(self): # Panel de control / Cierre de caja / Administración - Ingresos por día
        consulta = self.filter(close=False,anulate=False,caja='1').aggregate(total=Sum('amount'))
        if consulta: return consulta['total']
        else: return 0
    
    def total_ventas_anuladas_dia(self): # Panel de control / Cierre de caja / Administración - Ingresos por día
        consulta = self.filter(close=False,anulate=True,caja='1').aggregate(total=Sum('amount'))
        if consulta: return consulta['total']
        else: return 0
    
    def cerrar_ventas(self):  # Administración - Cierre de caja
        consulta = self.filter(close=False,caja='1')
        # actualizmos a cerrado
        total = consulta.aggregate(total=Sum('amount'))['total']
        cerrados = consulta.update(close=True) # devuelve numero de actualizaciones

        return cerrados, total

    #
    # Tezonco Caja 2
    #

    def ventas_no_cerradas_2(self): # Cierre de caja
        return self.filter(close=False,anulate=False,caja='2')
    
    def total_ventas_dia_2(self): # Panel de control / Cierre de caja / Administración - Ingresos por día
        consulta = self.filter(close=False,anulate=False,caja='2').aggregate(total=Sum('amount'))
        if consulta: return consulta['total']
        else: return 0
    
    def total_ventas_anuladas_dia_2(self): # Panel de control / Cierre de caja / Administración - Ingresos por día
        consulta = self.filter(close=False,anulate=True,caja='2').aggregate(total=Sum('amount'))
        if consulta: return consulta['total']
        else: return 0
    
    def cerrar_ventas_2(self):  # Administración - Cierre de caja
        consulta = self.filter(close=False,caja='2')
        # actualizmos a cerrado
        total = consulta.aggregate(total=Sum('amount'))['total']
        cerrados = consulta.update(close=True) # devuelve numero de actualizaciones

        return cerrados, total

    #
    #
    #

    # EN ESPERA
    # def total_ventas_por_dia(self): # Panel de control / Administración - Ingresos por día
    #     consulta = self.filter(anulate=False,).aggregate(total=Sum('amount'))
    #     if consulta: return consulta['total']
    #     else: return 0

    def total_ventas(self): # Administración - Mensualmente
        consulta = self.filter(
                anulate=False, close=True,
                date_sale__range=[str(self.ano_actual)+"-01-01 00:00:00.100000-0500", str(self.ano_actual)+"-12-31 23:59:59.100000-0500"],
            ).aggregate(total=Sum('amount'))

        if consulta: return consulta['total']
        else: return 0
    
    def ventas_en_fechas(self, date_start, date_end): # Administración - Ventas por fecha
        return self.filter(
            anulate=False, close=True,
            date_sale__range=(str(date_start)+" 00:00:00.100000-0500", str(date_end)+" 23:59:59.100000-0500"),
        ).order_by('-date_sale')

    # FUNCIÓN REEMPLAZADA
    # def monto_total_ventas(self):
    #     #
    #     consulta = self.filter(
    #         anulate=False,
    #     ).aggregate(
    #         total=Sum('amount')
    #     )
    #     #
    #     return consulta['total']
    
    def monto_total_ventas_actual(self): # Panel de control
        #
        consulta = self.filter(
            anulate=False,
            date_sale__gte=str(self.ano_actual)+"-01-01"
        ).aggregate(
            total=Sum('amount')
        )
        #
        if consulta:
            return consulta['total']
        else:
            return 0
    
    def ventas_no_cerradas_panel(self): # Panel de control / Cierre de caja
        #
        consulta = self.filter(close=False, anulate=False)
        #
        if consulta:
            return consulta.count()
        else:
            return 0

    # FUNCIÓN REEMPLAZADA
    # def total_ventas_no_cerradas(self):
    #     #
    #     consulta = self.filter(
    #         anulate=False
    #     ).count()
    #     #
    #     return consulta

    def venta_sin_anular(self): # Panel de control
        return self.filter(anulate=False)

    def total_ventas_no_cerradas_actual(self): # Panel de control
        #
        consulta = self.filter(
            anulate=False,
            date_sale__gte=str(self.ano_actual)+"-01-01"
        )
        #
        if consulta:
            return consulta.count()
        else:
            return 0

    # FUNCIÓN REEMPLAZADA
    # def costo_total(self):
    #     #
    #     consulta = self.filter(
    #         anulate=False
    #     ).aggregate(
    #         total=Sum(F('detail_sale__price_purchase')*F('detail_sale__count'),output_field=FloatField())
    #     )
    #     return consulta['total']

    def costo_total_actual(self): # Panel de control
        #
        consulta = self.filter(
            anulate=False,
            date_sale__gte=str(self.ano_actual)+"-01-01"
        ).aggregate(
            total=Sum(F('detail_sale__price_purchase')*F('detail_sale__count'),output_field=FloatField())
        )
        if consulta:
            return consulta['total']
        else:
            return 0

    def monto_ventas_mes(self): # Panel de control
        if str(self.mes_actual) == '1':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-01-01 00:00:00.100000-0500", str(self.ano_actual)+"-01-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            if consulta:
                return consulta['total']
            else:
                return 0
        if str(self.mes_actual) == '2':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-02-01 00:00:00.100000-0500", str(self.ano_actual)+"-02-28 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            if consulta:
                return consulta['total']
            else:
                return 0
        if str(self.mes_actual) == '3':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-03-01 00:00:00.100000-0500", str(self.ano_actual)+"-03-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            if consulta:
                return consulta['total']
            else:
                return 0
        if str(self.mes_actual) == '4':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-04-01 00:00:00.100000-0500", str(self.ano_actual)+"-04-30 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            if consulta:
                return consulta['total']
            else:
                return 0
        if str(self.mes_actual) == '5':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-05-01 00:00:00.100000-0500", str(self.ano_actual)+"-05-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            if consulta:
                return consulta['total']
            else:
                return 0
        if str(self.mes_actual) == '6':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-06-01 00:00:00.100000-0500", str(self.ano_actual)+"-06-30 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            if consulta:
                return consulta['total']
            else:
                return 0
        if str(self.mes_actual) == '7':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-07-01 00:00:00.100000-0500", str(self.ano_actual)+"-07-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            if consulta:
                return consulta['total']
            else:
                return 0
        if str(self.mes_actual) == '8':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-08-01 00:00:00.100000-0500", str(self.ano_actual)+"-08-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            if consulta:
                return consulta['total']
            else:
                return 0
        if str(self.mes_actual) == '9':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-09-01 00:00:00.100000-0500", str(self.ano_actual)+"-09-30 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            if consulta:
                return consulta['total']
            else:
                return 0
        if str(self.mes_actual) == '10':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-10-01 00:00:00.100000-0500", str(self.ano_actual)+"-10-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            if consulta:
                return consulta['total']
            else:
                return 0
        if str(self.mes_actual) == '11':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-11-01 00:00:00.100000-0500", str(self.ano_actual)+"-11-30 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            if consulta:
                return consulta['total']
            else:
                return 0
        if str(self.mes_actual) == '12':
            consulta = self.filter(anulate=False).filter(date_sale__range=[str(self.ano_actual)+"-12-01 00:00:00.100000-0500", str(self.ano_actual)+"-12-31 23:59:59.100000-0500"]).aggregate(total=Sum('amount'))
            if consulta:
                return consulta['total']
            else:
                return 0

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
    fecha_hoy = datetime.now()
    mes_actual = fecha_hoy.month
    ano_actual = fecha_hoy.year
    
    # No se utiliza
    # def detalle_por_venta(self, id_venta):
    #     return self.filter(
    #         sale__id=id_venta
    #     )

    def ventas_mes_producto(self, id_prod): # Inventario - Leer Accesorios, Calzado, Ropa
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        consulta = self.filter(
            sale__anulate=False, sale__close=True,
            created__range=(start_date, end_date),
            producto__pk=id_prod,
        ).values('sale__date_sale__date', 'producto__nombre').annotate(
            cantidad_vendida=Sum('count'),
        )
        return consulta
    
    def restablecer_stok_num_ventas(self, id_venta): # Cierre de caja
        prods_en_anulados = []
        for venta_detail in self.filter(sale__id=id_venta):
            # Actualizamos producto
            venta_detail.producto.stock = venta_detail.producto.stock + venta_detail.count
            venta_detail.producto.num_venta = venta_detail.producto.num_venta - venta_detail.count
            prods_en_anulados.append(venta_detail.producto)
        Productos.objects.bulk_update(prods_en_anulados, ['stock', 'num_venta'])
        return True
    
    def resumen_ventas(self): # Administración - Ultimos 31 días
        return self.filter(
            sale__anulate=False,
            sale__close=True,
        ).values('sale__date_sale__date').annotate(
            total_vendido=Sum(F('price_subtotal'),output_field=FloatField()),
            total_ganancias=Sum(F('price_subtotal') - F('price_purchase')*F('count'),output_field=FloatField()),
            num_productos_vendidos=Sum('count'),
            precio_costo=Sum('price_purchase'),
            precio_venta=Sum('price_sale'),
        )
    
    def resumen_ventas_mes(self): # Administración - Mensualmente
        return self.filter(
            sale__anulate=False,
            sale__close=True,
        ).values('sale__date_sale__date__month', 'sale__date_sale__date__year').annotate(
            cantidad_ventas=Sum('count'),
            total_ventas=Sum(F('price_subtotal'), output_field=FloatField()),
            ganancia_total=Sum(F('price_subtotal') - F('price_purchase')*F('count'),output_field=FloatField()),
            precio_costo=Sum('price_purchase'),
            precio_venta=Sum('price_sale'),
        ).order_by('-sale__date_sale__date__month')
    
    def resumen_ventas_proveedor(self, **filters): # Administración - Liquidación de proveedores
        # recibe 3 parametros en un diccionario
        # devuelve lista de ventas en rango de fechas de un proveedor
        # y, devuelve el total de ventas en rango de fechas y de proveedor

        if filters['date_start'] and filters['date_end'] and filters['proveedor']:
            consulta = self.filter(
                anulate=False,
                sale__close=True,
                sale__date_sale__range = (
                    str(filters['date_start'])+" 00:00:00.100000-0500",
                    str(filters['date_end'])+" 23:59:59.100000-0500",
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
    
    def ganancias_totales(self): # Panel de control PENDIENTE
        costo = self.filter(anulate=False, sale__close=True).aggregate(
            total=Sum(
                F('price_subtotal') - F('count')*F('price_purchase'),
                output_field=FloatField()
            )
        )
        return costo['total']
    
    def ganancias_totales_actuales(self): # Panel de control
        costo = self.filter(sale__anulate=False, sale__date_sale__gte=str(self.ano_actual)+"-01-01").aggregate(
            total=Sum(
                F('price_subtotal') - F('count')*F('price_purchase'),
                output_field=FloatField()
            )
        )
        if costo:
            return costo['total']
        else:
            return 0

    def reporte8020_producto2(self,f1,f2): # Administración - 8020
        resultado=self.filter(
            anulate=False, sale__close=True, sale__date_sale__range=(str(f1)+" 00:00:00.100000-0500",str(f2)+" 23:59:59.100000-0500")
        ).values(
            'producto'
        ).annotate(
            nombre=Upper('producto__marca__nombre'),
            piezas=ExpressionWrapper(F('producto__num_venta'),output_field=IntegerField()),
            inventario_inicial_piezas=ExpressionWrapper(F('producto__stock')+F('producto__num_venta'),output_field=IntegerField()),
            inventario_inicial_venta=ExpressionWrapper(Sum(F('price_subtotal')-F('price_subtotal')*F('tax'))+Sum('producto__stock')*F('price_sale'),output_field=FloatField()),
            num_ventas=ExpressionWrapper(Sum('count'),FloatField()),
            total_ventas=Sum('price_subtotal'),
            total_ventas_sin_iva=Sum(F('price_subtotal')-F('price_subtotal')*F('tax')),
            participacion=ExpressionWrapper((F('num_ventas')/Sum('count')),output_field=FloatField()),
            utilidad=ExpressionWrapper(Sum((F('price_subtotal')-F('price_subtotal')*F('tax'))-(F('price_purchase')*F('count'))),output_field=FloatField()),
            participacion_utilidad=ExpressionWrapper(F('count'),output_field=FloatField()),
            costo_venta=ExpressionWrapper(F('price_purchase')*F('count'),output_field=FloatField()),
            precio_lleno_venta=ExpressionWrapper((F('price_purchase')*F('count'))*1.65,output_field=FloatField()),
            margen_marcado=ExpressionWrapper(((F('precio_lleno_venta')-F('costo_venta'))/F('precio_lleno_venta')),output_field=FloatField()),
            margen_real=ExpressionWrapper((F('total_ventas_sin_iva')-F('costo_venta'))/F('total_ventas_sin_iva'),output_field=FloatField()),
            descuentos=ExpressionWrapper(F('total_ventas_sin_iva')-F('precio_lleno_venta'),output_field=FloatField()),
            inventario=Sum('producto__stock'),
            inventario_costo=ExpressionWrapper(Sum('producto__stock')*F('price_purchase'),output_field=FloatField()),
            inventario_venta=ExpressionWrapper(Sum('producto__stock')*F('price_sale'),output_field=FloatField()),
            inventario_inicial=ExpressionWrapper(F('total_ventas_sin_iva')+F('inventario_venta'),output_field=FloatField()),
            meses_inventario_venta=ExpressionWrapper(F('total_ventas_sin_iva')/(F('inventario_venta')/1),output_field=FloatField()),
            rotacion=ExpressionWrapper(F('total_ventas_sin_iva')/F('inventario_inicial')*100,output_field=FloatField()),
            meses_inventario_piezas=ExpressionWrapper(F('num_ventas')/F('inventario'),output_field=FloatField()),
            num_modelos=Count('producto__modelo'),
            profundidad=ExpressionWrapper(F('inventario')/F('num_modelos'),FloatField())
        ).order_by('-total_ventas','producto__marca__nombre')


        return resultado

    def compra_vs_vende(self, **filters): # Administración - Compra vs vende
        if filters['fecha_inicio'] and filters['fecha_fin'] and filters['proveedor']:
            #
            # Lo que se vende
            #
            fecha_venta = self.filter(
                anulate=False,
                sale__close=True,
                sale__date_sale__range = (str(filters['fecha_inicio'])+" 00:00:00.100000-0500",str(filters['fecha_fin'])+" 23:59:59.100000-0500",),
                producto__proveedor__pk=filters['proveedor'],
            )
        
            se_vende = fecha_venta.annotate(
                sub_total=ExpressionWrapper(F('price_subtotal'),output_field=FloatField()),
                total_pagar=ExpressionWrapper(F('price_subtotal') - (F('price_purchase') * F('count')),output_field=FloatField()),
                total_costo_pagar=ExpressionWrapper(F('count') * F('price_purchase'),output_field=FloatField())
            ).order_by('-sale__date_sale')

            total_se_vende = fecha_venta.aggregate(
                total_de_venta=Sum(
                    F('price_subtotal') - (F('price_purchase') * F('count')),output_field=FloatField()
                )
            )['total_de_venta']
            
            total_costo_vendido = fecha_venta.aggregate(
                total_costo_venta=Sum(
                    F('count') * F('price_purchase'),output_field=FloatField()
                )
            )['total_costo_venta']
            
            #
            # Lo que se compra
            #
            
            fecha_compra = Movimientos.objects.filter(
                fecha__range=(str(filters['fecha_inicio'])+" 00:00:00.100000-0500",str(filters['fecha_fin'])+" 23:59:59.100000-0500",),
                producto__proveedor__pk=filters['proveedor'],
            ).order_by('-fecha')

            se_compra = fecha_compra.annotate(
                total_pagar=ExpressionWrapper(F('total_costo'),output_field=FloatField())
            )

            total_se_compra = fecha_compra.aggregate(
                total_costo=Sum(
                    F('total_costo'),output_field=FloatField()
                )
            )['total_costo']

            return se_vende, total_se_vende, total_costo_vendido, total_se_compra, se_compra
        else:
            return [], 0, 0, 0, []


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