from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from applications.inventarios.models import Productos, Movimientos, ArchivoSubido
from django.db.models import Sum, F, FloatField, IntegerField, ExpressionWrapper, Count, Case, When
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
            precio_costo=Sum(F('price_purchase')*F('count'),output_field=FloatField()),
            precio_venta=Sum(F('price_sale')*F('count'),output_field=FloatField()),
            descuento=Sum('discount'),
        )
    
    def resumen_ventas_mes(self): # Administración - Mensualmente
        return self.filter(
            sale__anulate=False,
            sale__close=True,
        ).values('sale__date_sale__date__month', 'sale__date_sale__date__year').annotate(
            cantidad_ventas=Sum('count'),
            total_ventas=Sum(F('price_subtotal'), output_field=FloatField()),
            ganancia_total=Sum(F('price_subtotal') - F('price_purchase')*F('count'),output_field=FloatField()),
            precio_costo=Sum(F('price_purchase')*F('count'),output_field=FloatField()),
            precio_venta=Sum(F('price_sale')*F('count'),output_field=FloatField()),
            descuento=Sum('discount'),
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
                    F('price_subtotal') - (F('price_purchase')*F('count')),
                    output_field=FloatField()
                )
            ).order_by('sale__date_sale')

            total_ventas = consulta.aggregate(
                total_venta=Sum(
                    F('price_subtotal') - (F('price_purchase')*F('count')),
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
        marcas, suma_ventas_con_iva, suma_ventas_sin_iva, suma_piezas, suma_utilidad, modelos = [], [], [], [], [], []
        dic, total_stock, total_utilidad, modelo = {}, {}, {}, {}
        consulta = self.filter(anulate=False, sale__close=True, sale__date_sale__range=(str(f1)+" 00:00:00.100000-0500",str(f2)+" 23:59:59.100000-0500"))

        # Filtrado de marcas
        for venta in consulta:
            if venta.producto.marca not in marcas: marcas.append(venta.producto.marca)
        
        # Total de ventas con/sin iva, piezas vendidas, utilidad
        for i, marca in enumerate(marcas):
            suma = self.filter(anulate=False, sale__close=True,sale__date_sale__range=(str(f1)+" 00:00:00.100000-0500",str(f2)+" 23:59:59.100000-0500"),producto__marca=marca
                ).aggregate(
                    total_ventas_con_iva=Sum(F('price_subtotal'),output_field=FloatField()),
                    total_ventas_sin_iva=Sum(F('price_subtotal')/1.16),
                    piezas=ExpressionWrapper(Sum(F('producto__num_venta'))/Count('producto__num_venta'),output_field=FloatField()),
                    utilidad=Sum(F('price_subtotal')/1.16,output_field=FloatField())-Sum(F('price_purchase'),output_field=FloatField()),
                )
            suma_ventas_con_iva.append(suma['total_ventas_con_iva'])
            suma_ventas_sin_iva.append(suma['total_ventas_sin_iva'])
            suma_piezas.append(suma['piezas'])
            suma_utilidad.append(suma['utilidad'])
        
        total_ventas_civa:float = sum(suma_ventas_con_iva)
        total_ventas_siva:float = sum(suma_ventas_sin_iva)
        total_piezas:float = sum(suma_piezas)
        total_utilidad:float = sum(suma_utilidad)

        total_modelos,suma_stock_actual,suma_inv_venta = 0,0,0
        # Inventario de Productos - inicial en piezas, precio venta, precio costo
        for i, marca in enumerate(marcas):
            consulta_filtrada = Productos.objects.filter(marca=marca).aggregate(
                total_stock = Sum(F('stock')+F('num_venta'),output_field=IntegerField()),
                total_precio_venta = Sum(F('precio_venta')*F('stock'),output_field=FloatField()),
                stock_actual = Sum(F('stock'),output_field=IntegerField()),
                precio_costo_actual = Sum(F('precio_compra')*F('stock'),output_field=FloatField()),
            )

            total_stock[i] = consulta_filtrada['total_stock'],consulta_filtrada['total_precio_venta'],consulta_filtrada['stock_actual'],consulta_filtrada['precio_costo_actual']

            # Contadores para sacar sumas totales
            suma_stock_actual += consulta_filtrada['stock_actual']
            suma_inv_venta += consulta_filtrada['total_precio_venta']
        
        suma_modelos = 0
        # Numero de modelos
        for i, marca in enumerate(marcas):
            consulta_filtrada = Productos.objects.filter(marca=marca)
            for cf in consulta_filtrada:
                if cf.modelo not in modelos:
                    modelos.append(cf.modelo)
                    total_modelos += modelos.count(cf.modelo)
            
            modelo[i] = str(total_modelos)

            # Contadores para sacar sumas totales
            suma_modelos += total_modelos

        suma_inv_ini_venta,suma_costo_venta,suma_lleno,suma_descuentos = 0,0,0,0
        # Agrupando todos los valores en un diccionario
        for i, marca in enumerate(marcas):
            consulta_filtrada = self.filter(
                anulate=False, sale__close=True,
                sale__date_sale__range=(str(f1)+" 00:00:00.100000-0500",str(f2)+" 23:59:59.100000-0500"),
                producto__marca=marca
                ).values('producto').annotate(
                    piezas=ExpressionWrapper(F('producto__num_venta'),output_field=IntegerField()),
                    venta_con_iva=Sum(F('price_subtotal'),output_field=FloatField()),
                    venta_sin_iva=Sum(F('price_subtotal')/1.16,output_field=FloatField()),
                    participacion=ExpressionWrapper(Sum(F('price_subtotal'))/total_ventas_siva, output_field=FloatField()),
                    total_precio_venta=ExpressionWrapper(Sum(F('price_sale')*F('producto__num_venta'),output_field=FloatField())/Count('price_subtotal'),output_field=FloatField()),
                    utilidad=Sum(F('price_subtotal')/1.16,output_field=FloatField())-Sum(F('price_purchase'),output_field=FloatField()),
                    costo_venta=Sum(F('price_purchase'),output_field=FloatField()),
                    precio_lleno_venta=Sum(F('price_purchase')*1.65,output_field=FloatField()),
                    margen_marcado=(Sum(F('price_purchase')*1.65,output_field=FloatField())-Sum(F('price_purchase'),output_field=FloatField()))/Sum(F('price_purchase')*1.65,output_field=FloatField()),
                    margen_real=(Sum(F('price_subtotal')/1.16,output_field=FloatField())-Sum(F('price_purchase'),output_field=FloatField()))/Sum(F('price_subtotal')/1.16,output_field=FloatField()),
                    descuentos=Sum(F('price_subtotal')/1.16,output_field=FloatField())-Sum(F('price_purchase')*1.65,output_field=FloatField()),
                )
            inv_iniclal_precio_venta=consulta_filtrada[0]['total_precio_venta']+total_stock[i][1]
            participacion_utilidad=consulta_filtrada[0]['utilidad']/total_utilidad
            rotacion=consulta_filtrada[0]['venta_sin_iva']/inv_iniclal_precio_venta
            meses_invetario_venta=total_stock[i][1]/(consulta_filtrada[0]['venta_sin_iva']/1)
            meses_inventario_piezas=total_stock[i][2]/(consulta_filtrada[0]['piezas']/1)
            profundidad_inventario=float(total_stock[i][2])/float(modelo[i][0])

            dic[i] = str(marca),consulta_filtrada[0]['piezas'],consulta_filtrada[0]['venta_con_iva'],consulta_filtrada[0]['venta_sin_iva'],consulta_filtrada[0]['participacion'],total_stock[i][0],inv_iniclal_precio_venta,consulta_filtrada[0]['utilidad'],participacion_utilidad,consulta_filtrada[0]['costo_venta'],consulta_filtrada[0]['precio_lleno_venta'],consulta_filtrada[0]['margen_marcado'],consulta_filtrada[0]['margen_real'],consulta_filtrada[0]['descuentos'],total_stock[i][2],total_stock[i][3],total_stock[i][1],rotacion,meses_invetario_venta,meses_inventario_piezas,modelo[i][0],profundidad_inventario

            # Contadores para sacar sumas totales
            suma_inv_ini_venta += inv_iniclal_precio_venta
            suma_costo_venta += consulta_filtrada[0]['costo_venta']
            suma_lleno += consulta_filtrada[0]['precio_lleno_venta']
            suma_descuentos += consulta_filtrada[0]['descuentos']
        
        # TOTALES
        total_inv_ini_venta = suma_inv_ini_venta
        total_costo_venta = suma_costo_venta
        total_lleno_venta = suma_lleno
        total_descuentos = suma_descuentos
        total_inv_piezas = suma_stock_actual
        total_inv_venta = suma_inv_venta
        totat_modelos = suma_modelos

        try:
            total_margen_mercado = (total_lleno_venta-total_costo_venta)/total_lleno_venta
            total_margen_real = (float(total_ventas_siva)-total_costo_venta)/float(total_ventas_siva)
            total_rotacion = float(total_ventas_siva)/total_inv_ini_venta
            total_meses_inv = total_inv_venta/(float(total_ventas_siva)/1)
            total_prof_inv = total_inv_piezas/totat_modelos
        except ZeroDivisionError:
            total_margen_mercado = 0
            total_margen_real = 0
            total_rotacion = 0
            total_meses_inv = 0
            total_prof_inv = 0

        # for key, value in dic.items(): print(key, value)
        return dic,total_piezas,total_ventas_civa,total_ventas_siva,total_inv_ini_venta,total_utilidad,total_costo_venta,total_lleno_venta,total_margen_mercado,total_margen_real,total_descuentos,total_inv_piezas,total_inv_venta,total_rotacion,total_meses_inv,totat_modelos,total_prof_inv
    
    def totales_8020(self,f1,f2):
        dict_total = {}
        total_piezas = int(self.reporte8020_producto2(f1,f2)[1])
        total_venta_civa = self.reporte8020_producto2(f1,f2)[2]
        total_venta_siva = self.reporte8020_producto2(f1,f2)[3]
        total_inv_ini_venta = self.reporte8020_producto2(f1,f2)[4]
        total_utilidad = self.reporte8020_producto2(f1,f2)[5]
        total_costo_venta = self.reporte8020_producto2(f1,f2)[6]
        total_lleno_venta = self.reporte8020_producto2(f1,f2)[7]
        total_margen_mercado = self.reporte8020_producto2(f1,f2)[8]
        total_margen_real = self.reporte8020_producto2(f1,f2)[9]
        total_descuentos = self.reporte8020_producto2(f1,f2)[10]
        total_inv_piezas = self.reporte8020_producto2(f1,f2)[11]
        total_inv_venta = self.reporte8020_producto2(f1,f2)[12]
        total_rotacion = self.reporte8020_producto2(f1,f2)[13]
        total_meses_inv = self.reporte8020_producto2(f1,f2)[14]
        total_modelos =  self.reporte8020_producto2(f1,f2)[15]
        total_prof_inv = self.reporte8020_producto2(f1,f2)[16]

        dict_total[0] = total_piezas,total_venta_civa,total_venta_siva,total_inv_ini_venta,total_utilidad,total_costo_venta,total_lleno_venta,total_margen_mercado,total_margen_real,total_descuentos,total_inv_piezas,total_inv_venta,total_rotacion,total_meses_inv,total_modelos,total_prof_inv

        return dict_total

    def compra_vs_vende(self, **filters): # Administración - Compra vs vende
        if filters['fecha_inicio'] and filters['fecha_fin'] and filters['proveedor'] and filters['archivo']:
            productos = Movimientos.objects.all()
            productos.delete()

            #
            # Lo que se vende
            #

            fecha_venta = self.filter(
                anulate=False,sale__close=True,
                sale__date_sale__range = (str(filters['fecha_inicio'])+" 00:00:00.100000-0500",str(filters['fecha_fin'])+" 23:59:59.100000-0500",),
                producto__proveedor__pk=filters['proveedor'],
            )
        
            se_vende = fecha_venta.annotate(
                sub_total=ExpressionWrapper(F('price_subtotal'),output_field=FloatField()),
                total_pagar=ExpressionWrapper(F('price_subtotal') - (F('price_purchase') * F('count')),output_field=FloatField()),
                total_costo_pagar=ExpressionWrapper(F('count') * F('price_purchase'),output_field=FloatField())
            ).order_by('-sale__date_sale')

            total_se_vende = fecha_venta.aggregate(total_de_venta=Sum(F('price_subtotal') - (F('price_purchase') * F('count')),output_field=FloatField()))['total_de_venta']
            total_costo_vendido = fecha_venta.aggregate(total_costo_venta=Sum(F('count') * F('price_purchase'),output_field=FloatField()))['total_costo_venta']
            
            #
            # Lo que se compra
            #

            archivo = filters['archivo']
            file = ArchivoSubido.objects.get(id=archivo)
            
            fecha_archivo = file.fecha
            total_pcosto_stock, total_pcosto_stock_2 = [], []
            total_pventa_stock, total_pventa_stock_2 = [], []
            lista_stock, lista_stock_2 = [], []
            t_pcosto, t_pcosto_2 = 0, 0
            t_pventa, t_pventa_2 = 0, 0
            stock, stock_2 = 0, 0
            dic_archivo = {}
            dic_ventas = {}
            dic_ventas_stock = {}
            dic_ventas_date = {}
            with open(f'/webapps/excalibur/ExcaliburAbryl/media/{file}', "r") as archivo:
                renglon_archivo = archivo.readlines()
                lista = []
                for i, renglon in enumerate(renglon_archivo[1:]):
                    r = renglon.strip()
                    dic_archivo[i] = r
                
                for i in dic_archivo:
                    archivo = str(dic_archivo[i]).split(',')
                    total_pcosto_stock.append(float(archivo[7])*float(archivo[6]))
                    total_pventa_stock.append(float(archivo[8])*float(archivo[6]))
                    lista_stock.append(int(archivo[6]))

                t_pcosto = sum(total_pcosto_stock)
                t_pventa = sum(total_pventa_stock)
                stock = sum(lista_stock)
                
                for n, i in enumerate(fecha_venta):
                    dic_ventas[n] = str(i.producto.marca)+','+str(i.producto.modelo)+','+str(i.producto.get_genero_display())+','+str(i.producto.sublinea)+','+str(i.producto.color)+','+str(i.producto.talla)+','+str(i.producto.stock)+','+str(i.producto.precio_compra)+','+str(i.producto.precio_venta)+','+str(i.producto.proveedor)
                    dic_ventas_stock[n] = str(i.count)
                    dic_ventas_date[n] = str(i.sale.date_sale)
                
                sc = 1
                for n, i in enumerate(dic_ventas):
                    for j in dic_archivo:
                        vent = str(dic_ventas[i]).split(',')
                        archivo = str(dic_archivo[j]).split(',')
                        ventas = str(vent[0])+','+str(vent[1])+','+str(vent[2])+','+str(vent[3])+','+str(vent[4])+','+str(vent[5])+','+str(vent[7])+','+str(vent[8])+','+str(vent[9])
                        archiv = str(archivo[0])+','+str(archivo[1])+','+str(archivo[2])+','+str(archivo[3])+','+str(archivo[4])+','+str(archivo[5])+','+str(archivo[7])+','+str(archivo[8])+','+str(archivo[9])
                        
                        if ventas == archiv:
                            total_pcosto_stock_2.append(float(archivo[7])*float(archivo[6]))
                            total_pventa_stock_2.append(float(archivo[8])*float(archivo[6]))
                            lista_stock_2.append(int(archivo[6]))
                            sc = dic_ventas_stock[n]
                            lista.append(Movimientos(
                                marca=archivo[0],modelo=archivo[1],linea=archivo[2],sublinea=archivo[3],
                                color=archivo[4],talla=archivo[5],stock=archivo[6],precio_costo=archivo[7],precio_venta=archivo[8],
                                proveedor=archivo[9],stock_comprado=sc,fecha_venta=dic_ventas_date[n]
                                )
                            )
                            break
                
                t_pcosto_2 = sum(total_pcosto_stock_2)
                t_pventa_2 = sum(total_pventa_stock_2)
                stock_2 = sum(lista_stock_2)

                for j in dic_archivo:
                    
                    archivo = str(dic_archivo[j]).split(',')

                    lista.append(Movimientos(
                        marca=archivo[0],modelo=archivo[1],linea=archivo[2],sublinea=archivo[3],
                        color=archivo[4],talla=archivo[5],stock=archivo[6],precio_costo=archivo[7],precio_venta=archivo[8],
                        proveedor=archivo[9],stock_comprado=0
                        )
                    )

                if len(lista) > 0:
                    Movimientos.objects.bulk_create(lista)

            stock_comprado = Movimientos.objects.order_by('fecha_venta', 'marca')

            # fecha_compra = Movimientos.objects.filter(
            #     fecha__range=(str(filters['fecha_inicio'])+" 00:00:00.100000-0500",str(filters['fecha_fin'])+" 23:59:59.100000-0500",),
            #     producto__proveedor__pk=filters['proveedor'],
            # ).order_by('-fecha')

            # se_compra = fecha_compra.annotate(total_pagar=ExpressionWrapper(F('total_costo'),output_field=FloatField()))
            # total_se_compra = fecha_compra.aggregate(total_costo=Sum(F('total_costo'),output_field=FloatField()))['total_costo']

            return se_vende, total_se_vende, total_costo_vendido, stock_comprado, fecha_archivo, t_pcosto, t_pcosto_2, t_pventa, t_pventa_2, stock, stock_2
            
        else:
            return [], 0, 0, [], [], 0, 0, 0, 0, 0, 0

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