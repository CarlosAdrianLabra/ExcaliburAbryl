from applications.inventarios.models import Marca
from datetime import datetime
from django.db import models
from django.db.models.fields import CharField, FloatField, IntegerField
from django.db.models import Q, Sum, F, FloatField, ExpressionWrapper
from .managers import GastosManager
from applications.ventas.models import DetalleVenta, Venta

# Create your models here.

class Gastos(models.Model):

    # Campos del modelo gastos

    OPCIONES_MES=(
        ('01','ENERO'),
        ('02','FEBRERO'),
        ('03','MARZO'),
        ('04','ABRIL'),
        ('05','MAYO'),
        ('06','JUNIO'),
        ('07','JULIO'),
        ('08','AGOSTO'),
        ('09','SEPTIEMBRE'),
        ('10','OCTUBRE'),
        ('11','NOVIEMBRE'),
        ('12','DICIEMBRE'),
    )

    OPCIONES_ANO=(

        ('2010','2010'),
        ('2011','2011'),
        ('2012','2012'),
        ('2013','2013'),
        ('2014','2015'),
        ('2015','2014'),
        ('2016','2016'),
        ('2017','2017'),
        ('2018','2018'),
        ('2019','2019'),
        ('2020','2020'),
        ('2021','2021'),
        ('2022','2022'),
        ('2023','2023'),
        ('2024','2024'),
        ('2025','2025'),
        ('2026','2026'),
        ('2027','2027'),
        ('2028','2028'),
        ('2029','2029'),        

    )
    #valores fecha
    mes=models.CharField('Mes',max_length=2,blank=False,choices=OPCIONES_MES)
    año=models.CharField('Año',max_length=4,blank=False,choices=OPCIONES_ANO)
    fecha=models.DateField(unique=True,blank=True)

    #Gastos Bancarios
    cargosBancarios = models.FloatField('Cargos Bancarios',default=0)
    comisionTarjetaCredito= models.FloatField('Comisión de tarjeta de crédito',default=0)
    otrosBancos=models.FloatField('Otros bancos',default=0)
    #Sueldos
    salariosSueldosWeb=models.FloatField('Salarios y sueldos web',default=0)
    sueldosOficina=models.FloatField('Sueldos oficina',default=0)
    sueldosCorporativos=models.FloatField('Sueldos corporativos',default=0)
    comisionesPagadas=models.FloatField('Comisiones pagadas',default=0)
    jubilacion=models.FloatField('Jubilación',default=0)
    utilidades=models.FloatField('Utilidades',default=0)
    costosReclutamiento=models.FloatField('Costos de reclutamiento',default=0)
    imss=models.FloatField('IMSS',default=0)
    #Gastos generales
    rollosImpresora=models.FloatField('Rollos de impresora',default=0)
    tapiceria=models.FloatField('Tapicería',default=0)
    remodelacionOficina=models.FloatField('Remodelaciones de oficina',default=0)
    predial=models.FloatField('Predial',default=0)
    papeleria=models.FloatField('Papelería',default=0)
    intercomunicador=models.FloatField('Intercomunicador',default=0)
    telefonosOficina=models.FloatField('Telefonos de oficina',default=0)
    luz=models.FloatField('Luz',default=0)
    telefono=models.FloatField('Telefono',default=0)
    lentes=models.FloatField('Lentes',default=0)
    fletes=models.FloatField('Fletes',default=0)
    walmart=models.FloatField('Walmart',default=0)
    reparacionesManteminiento=models.FloatField('Reparaciones y mantenimiento',default=0)
    notas=models.FloatField('Notas',default=0)
    agua=models.FloatField('Agua',default=0)
    policia=models.FloatField('Policía',default=0)
    gastosViajes=models.FloatField('Gastos de viajes',default=0)
    amplificadorBocinas=models.FloatField('Amplificador y bocinas',default=0)
    gastosCheques=models.FloatField('Gastos cheques',default=0)
    gastosOficina=models.FloatField('Gastos oficina',default=0)
    fideicomiso=models.FloatField('Fideicomiso',default=0)
    contador=models.FloatField('Contador',default=0)
    cometra=models.FloatField('Cometra',default=0)
    paletas=models.FloatField('Paletas',default=0)
    finiquito=models.FloatField('Finiquito',default=0)
    honorariosConsultores=models.FloatField('Honorarios de consultores',default=0)
    impuestoCDMX=models.FloatField('Impuesto CDMX',default=0)
    chequesAbril=models.FloatField('Cheques Abril',default=0)
    equipoComputo=models.FloatField('Equipos de computo',default=0)
    mantenimientoComputo=models.FloatField('Mantenimiento computo',default=0)
    viaticos=models.FloatField('Viaticos',default=0)
    comidas=models.FloatField('Comidas y cenas',default=0)
    valoracionInmuebles=models.FloatField('Valoración de Inmuebles',default=0)
    imprenta=models.FloatField('Imprenta',default=0)
    comisionRentaLocal=models.FloatField('Comisión de renta de local',default=0)
    impuestos=models.FloatField('Impuestos',default=0)
    #total de gastos
    gastosTotales=models.FloatField('Gastos Totales',blank=True,null=True)
    #sub-totales
    totales_bancarios=models.FloatField('Gastos bancarios totales',blank=True,null=True)
    totales_sueldos=models.FloatField('Sueldos totales',blank=True,null=True)
    totales_generales=models.FloatField('Gastos generales totales',blank=True,null=True)
    
    objects=GastosManager()

    class Meta:

        verbose_name = 'Gastos'
        verbose_name_plural = 'Gastos'

    def save(self, *args, **kwargs):        
        
        date=self.año+'-'+self.mes+'-'+'01'
        monthdate = datetime.strptime(date,'%Y-%m-%d').date()
        self.fecha = monthdate

        total=(self.cargosBancarios+self.comisionTarjetaCredito+self.otrosBancos
                +self.salariosSueldosWeb+self.sueldosOficina+self.sueldosCorporativos+self.comisionesPagadas
                +self.jubilacion+self.utilidades+self.costosReclutamiento+self.imss
                +self.rollosImpresora+self.tapiceria+self.remodelacionOficina+self.predial
                +self.papeleria+self.intercomunicador+self.telefonosOficina+self.luz
                +self.telefono+self.lentes+self.fletes+self.walmart+self.reparacionesManteminiento
                +self.notas+self.agua+self.policia+self.gastosViajes+self.amplificadorBocinas
                +self.gastosCheques+self.gastosOficina+self.fideicomiso+self.contador
                +self.cometra+self.paletas+self.finiquito+self.honorariosConsultores
                +self.impuestoCDMX+self.chequesAbril+self.equipoComputo+self.mantenimientoComputo
                +self.viaticos+self.comidas+self.valoracionInmuebles+self.imprenta
                +self.comisionRentaLocal+self.impuestos)
        
        total_b = self.cargosBancarios+self.comisionTarjetaCredito+self.otrosBancos
        total_s = (self.salariosSueldosWeb+self.sueldosOficina+self.sueldosCorporativos+self.comisionesPagadas
                +self.jubilacion+self.utilidades+self.costosReclutamiento+self.imss)
        total_g = (self.rollosImpresora+self.tapiceria+self.remodelacionOficina+self.predial
                +self.papeleria+self.intercomunicador+self.telefonosOficina+self.luz
                +self.telefono+self.lentes+self.fletes+self.walmart+self.reparacionesManteminiento
                +self.notas+self.agua+self.policia+self.gastosViajes+self.amplificadorBocinas
                +self.gastosCheques+self.gastosOficina+self.fideicomiso+self.contador
                +self.cometra+self.paletas+self.finiquito+self.honorariosConsultores
                +self.impuestoCDMX+self.chequesAbril+self.equipoComputo+self.mantenimientoComputo
                +self.viaticos+self.comidas+self.valoracionInmuebles+self.imprenta
                +self.comisionRentaLocal+self.impuestos)
        
        self.gastosTotales=total
        #
        self.totales_bancarios=total_b
        self.totales_sueldos=total_s
        self.totales_generales=total_g

        super(Gastos, self).save(*args, **kwargs)

    def ventas_calzado(self):
        if Venta.objects.filter(detail_sale__producto__tipo='100').filter(close=True).exists():
            if self.mes == '01' or self.mes == '03' or self.mes == '05' or self.mes == '07' or self.mes == '08' or self.mes == '10' or self.mes == '12':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='100',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-31 23:59:59.100000-0500'),
                ).aggregate(total=Sum('amount'))['total']
            elif self.mes == '02':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='100',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-28 23:59:59.100000-0500'),
                ).aggregate(total=Sum('amount'))['total']
            elif self.mes == '04' or self.mes == '06' or self.mes == '09' or self.mes == '11':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='100',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-30 23:59:59.100000-0500'),
                ).aggregate(total=Sum('amount'))['total']
        else:
            consulta = 0

        return consulta
    
    def ventas_ropa(self):
        if Venta.objects.filter(detail_sale__producto__tipo='200').filter(close=True).exists():
            if self.mes == '01' or self.mes == '03' or self.mes == '05' or self.mes == '07' or self.mes == '08' or self.mes == '10' or self.mes == '12':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='200',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-31 23:59:59.100000-0500'),
                ).aggregate(total=Sum('amount'))['total']
            elif self.mes == '02':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='200',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-28 23:59:59.100000-0500'),
                ).aggregate(total=Sum('amount'))['total']
            elif self.mes == '04' or self.mes == '06' or self.mes == '09' or self.mes == '11':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='200',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-30 23:59:59.100000-0500'),
                ).aggregate(total=Sum('amount'))['total']
        else:
            consulta = 0

        return consulta
    
    def ventas_accesorios(self):
        if Venta.objects.filter(detail_sale__producto__tipo='300').filter(close=True).exists():
            if self.mes == '01' or self.mes == '03' or self.mes == '05' or self.mes == '07' or self.mes == '08' or self.mes == '10' or self.mes == '12':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='300',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-31 23:59:59.100000-0500'),
                ).aggregate(total=Sum('amount'))['total']
            elif self.mes == '02':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='300',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-28 23:59:59.100000-0500'),
                ).aggregate(total=Sum('amount'))['total']
            elif self.mes == '04' or self.mes == '06' or self.mes == '09' or self.mes == '11':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='300',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-30 23:59:59.100000-0500'),
                ).aggregate(total=Sum('amount'))['total']
        else:
            consulta = 0

        return consulta

    def total_de_ventas(self):
        consulta_c = self.ventas_calzado()
        consulta_r = self.ventas_ropa()
        consulta_a = self.ventas_accesorios()
        #
        consulta_final = consulta_c + consulta_r + consulta_a

        return consulta_final

    def descuentos_calzado(self):
        if Venta.objects.filter(detail_sale__producto__tipo='100').filter(close=True).exists():
            if self.mes == '01' or self.mes == '03' or self.mes == '05' or self.mes == '07' or self.mes == '08' or self.mes == '10' or self.mes == '12':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='100',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-31 23:59:59.100000-0500'),
                ).aggregate(total=Sum('detail_sale__discount'))['total']
            elif self.mes == '02':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='100',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-28 23:59:59.100000-0500'),
                ).aggregate(total=Sum('detail_sale__discount'))['total']
            elif self.mes == '04' or self.mes == '06' or self.mes == '09' or self.mes == '11':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='100',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-30 23:59:59.100000-0500'),
                ).aggregate(total=Sum('detail_sale__discount'))['total']
        else:
            consulta = 0

        return consulta

    def descuentos_ropa(self):
        if Venta.objects.filter(detail_sale__producto__tipo='200').filter(close=True).exists():
            if self.mes == '01' or self.mes == '03' or self.mes == '05' or self.mes == '07' or self.mes == '08' or self.mes == '10' or self.mes == '12':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='200',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-31 23:59:59.100000-0500'),
                ).aggregate(total=Sum('detail_sale__discount'))['total']
            elif self.mes == '02':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='200',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-28 23:59:59.100000-0500'),
                ).aggregate(total=Sum('detail_sale__discount'))['total']
            elif self.mes == '04' or self.mes == '06' or self.mes == '09' or self.mes == '11':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='200',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-30 23:59:59.100000-0500'),
                ).aggregate(total=Sum('detail_sale__discount'))['total']
        else:
            consulta = 0

        return consulta

    def descuentos_accesorios(self):
        if Venta.objects.filter(detail_sale__producto__tipo='300').filter(close=True).exists():
            if self.mes == '01' or self.mes == '03' or self.mes == '05' or self.mes == '07' or self.mes == '08' or self.mes == '10' or self.mes == '12':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='300',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-31 23:59:59.100000-0500'),
                ).aggregate(total=Sum('detail_sale__discount'))['total']
            elif self.mes == '02':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='300',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-28 23:59:59.100000-0500'),
                ).aggregate(total=Sum('detail_sale__discount'))['total']
            elif self.mes == '04' or self.mes == '06' or self.mes == '09' or self.mes == '11':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='300',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-30 23:59:59.100000-0500'),
                ).aggregate(total=Sum('detail_sale__discount'))['total']
        else:
            consulta = 0

        return consulta

    def total_de_descuentos(self):
        consulta_c = self.descuentos_calzado()
        consulta_r = self.descuentos_ropa()
        consulta_a = self.descuentos_accesorios()
        #
        consulta_final = consulta_c + consulta_r + consulta_a

        return consulta_final

    def venta_neta_sistema(self):
        total_de_ventas = self.total_de_ventas()
        total_de_descuentos = self.total_de_descuentos()
        #
        consulta_final = total_de_ventas - total_de_descuentos

        return consulta_final

    def costo_ventas_calzado(self):
        if Venta.objects.filter(detail_sale__producto__tipo='100').filter(close=True).exists():
            if self.mes == '01' or self.mes == '03' or self.mes == '05' or self.mes == '07' or self.mes == '08' or self.mes == '10' or self.mes == '12':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='100',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-31 23:59:59.100000-0500'),
                ).aggregate(total=Sum(F('detail_sale__price_purchase')*F('detail_sale__count'),output_field=FloatField()))['total']
            elif self.mes == '02':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='100',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-28 23:59:59.100000-0500'),
                ).aggregate(total=Sum(F('detail_sale__price_purchase')*F('detail_sale__count'),output_field=FloatField()))['total']
            elif self.mes == '04' or self.mes == '06' or self.mes == '09' or self.mes == '11':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='100',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-30 23:59:59.100000-0500'),
                ).aggregate(total=Sum(F('detail_sale__price_purchase')*F('detail_sale__count'),output_field=FloatField()))['total']
        else:
            consulta = 0

        return consulta
    
    def costo_ventas_ropa(self):
        if Venta.objects.filter(detail_sale__producto__tipo='200').filter(close=True).exists():
            if self.mes == '01' or self.mes == '03' or self.mes == '05' or self.mes == '07' or self.mes == '08' or self.mes == '10' or self.mes == '12':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='200',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-31 23:59:59.100000-0500'),
                ).aggregate(total=Sum(F('detail_sale__price_purchase')*F('detail_sale__count'),output_field=FloatField()))['total']
            elif self.mes == '02':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='200',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-28 23:59:59.100000-0500'),
                ).aggregate(total=Sum(F('detail_sale__price_purchase')*F('detail_sale__count'),output_field=FloatField()))['total']
            elif self.mes == '04' or self.mes == '06' or self.mes == '09' or self.mes == '11':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='200',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-30 23:59:59.100000-0500'),
                ).aggregate(total=Sum(F('detail_sale__price_purchase')*F('detail_sale__count'),output_field=FloatField()))['total']
        else:
            consulta = 0

        return consulta
    
    def costo_ventas_accesorios(self):
        if Venta.objects.filter(detail_sale__producto__tipo='300').filter(close=True).exists():
            if self.mes == '01' or self.mes == '03' or self.mes == '05' or self.mes == '07' or self.mes == '08' or self.mes == '10' or self.mes == '12':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='300',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-31 23:59:59.100000-0500'),
                ).aggregate(total=Sum(F('detail_sale__price_purchase')*F('detail_sale__count'),output_field=FloatField()))['total']
            elif self.mes == '02':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='300',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-28 23:59:59.100000-0500'),
                ).aggregate(total=Sum(F('detail_sale__price_purchase')*F('detail_sale__count'),output_field=FloatField()))['total']
            elif self.mes == '04' or self.mes == '06' or self.mes == '09' or self.mes == '11':
                consulta = Venta.objects.filter(detail_sale__producto__tipo='300',close=True,anulate=False,
                    date_sale__range=(self.año+'-'+self.mes+'-01 00:00:00.100000-0500', self.año+'-'+self.mes+'-30 23:59:59.100000-0500'),
                ).aggregate(total=Sum(F('detail_sale__price_purchase')*F('detail_sale__count'),output_field=FloatField()))['total']
        else:
            consulta = 0

        return consulta

    def total_de_costo_ventas(self):
        consulta_c = self.costo_ventas_calzado()
        consulta_r = self.costo_ventas_ropa()
        consulta_a = self.costo_ventas_accesorios()
        #
        consulta_final = consulta_c + consulta_r + consulta_a

        return consulta_final

    def __str__(self):
        return 'Gastos ' + str(self.id)+ ' - ' + self.mes + ' ' + self.año + ' = ' + str(self.gastosTotales) 
