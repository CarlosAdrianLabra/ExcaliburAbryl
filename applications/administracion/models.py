
from applications.ventas.models import DetalleVenta, Venta
from datetime import datetime,date,timedelta
from django.db import models
from django.db.models import Sum
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateField, FloatField, IntegerField
from django.db.models.fields.related import ForeignKey
from .managers import GastosManager, ResultadoManager

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
        
        self.gastosTotales=total

        super(Gastos, self).save(*args, **kwargs)

    def __str__(self):
        return 'Gastos ' + str(self.id)+ ' - ' + self.mes + ' ' + self.año + ' = ' + str(self.gastosTotales) 

class Resultado(models.Model):

    #Campos del modelo resultados

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

    #gastos=ForeignKey(Gastos,on_delete=CASCADE,verbose_name='Gasto',related_name='gastos',blank=True)
    #detalleventas=ForeignKey(DetalleVenta,on_delete=CASCADE,verbose_name='Venta',related_name='ventas')
    resultado=FloatField('Resultados del mes',default=0,blank=True)
    fecha=DateField(blank=True,null=True,unique=True)
    objects=ResultadoManager()
    gastos_mes=FloatField('Gastos del mes',default=0,blank=True)
    dias_agregados=IntegerField(default=0)
    ventas_mes=FloatField('Ventas del mes',default=0,blank=True)


    def save(self, *args, **kwargs):

        date=self.año+'-'+self.mes+'-'+'01'
        monthdate = datetime.strptime(date,'%Y-%m-%d').date()
        self.fecha = monthdate

        start_date=monthdate
        d=timedelta(days=self.dias_agregados)
        end_date=start_date+d

        consulta1=Gastos.objects.filter(
            fecha__range=(start_date,end_date)
        ).values(
            'gastosTotales'
        ).get()

        self.gastos_mes=consulta1.get('gastosTotales')

        consulta2=DetalleVenta.objects.filter(
            sale__date_sale__range=(start_date,end_date)
        ).values(
            'sale__date_sale__date__month'
        ).annotate(
            ventasmes=Sum('price_subtotal',output_field=FloatField())
        ).get()

        print (consulta2)
        ventastotal=consulta2.get('ventasmes')
        print (ventastotal) 
        self.ventas_mes=consulta2.get('ventasmes')
        self.resultado=self.ventas_mes-self.gastos_mes
        super(Resultado, self).save(*args, **kwargs)    

    def __str__(self):
        return str(self.gastos_mes) # TODO

