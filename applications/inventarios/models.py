from decimal import Decimal
from django.db import models
from django.db.models.signals import post_save, pre_save
from PIL import Image
from model_utils.models import TimeStampedModel
from django.utils import timezone
from .managers import filtros

# Modelo de proveedores
class Proveedor(TimeStampedModel):

    nombre = models.CharField('Nombre', max_length=50, blank=True)
    correo = models.EmailField('Correo Electrónico', blank=True)
    telefono = models.CharField('Teléfono', max_length=14, blank=True)
    direccion = models.CharField('Dirección', max_length=50, blank=True)
    clabe = models.CharField('Clabe interbancaria', max_length=18, blank=True)
    nombre_banco = models.CharField('Nombre de banco', max_length=40, blank=True)
    nombre_benefactor = models.CharField('Nombre del beneficiario', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores Registrados'
        db_table = 'Proveedor'
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.direccion = self.direccion.upper()
        self.nombre_banco = self.nombre_banco.upper()
        self.nombre_benefactor = self.nombre_benefactor.upper()
        return super(Proveedor, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# Modelo de marcas
class Marca(TimeStampedModel):

    nombre = models.CharField('Nombre', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas Registradas'
        db_table = 'Marca'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        return super(Marca, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# Modelo de productos
class Productos(TimeStampedModel):

    OPCIONES_ALMACEN = (
        ('1000', 'ALMACEN 1'),
        ('2000', 'ALMACEN 2'),
        ('3000', 'ALMACEN 3'),
    )

    OPCIONES_TIPO_PRODUCTO = (
        ('100', 'CALZADO'),
        ('200', 'ROPA'),
        ('300', 'ACCESORIOS'),
    )

    OPCIONES_TALLA = (
        ('', '---------'),
        ('', 'BEBE'),
        ('001', 'UN'),
        ('002', 'PZA'),
        ('', '---------'),
        ('', 'CABALLERO'),
        ('003', 'UN'),
        ('004', '10'),
        ('005', '12'),
        ('006', '14'),
        ('007', '14.5'),
        ('008', '15'),
        ('009', '15.5'),
        ('010', '16'),
        ('011', '16.5'),
        ('012', '17'),
        ('013', '17.5'),
        ('014', '18'),
        ('015', '20'),
        ('016', '22'),
        ('017', '24'),
        ('018', '26'),
        ('019', '28'),
        ('020', '30'),
        ('021', '32'),
        ('022', '34'),
        ('023', '36'),
        ('024', '38'),
        ('025', '40'),
        ('026', '42'),
        ('027', '80'),
        ('028', 'CH'),
        ('029', 'M'),
        ('030', 'G'),
        ('031', 'XG'),
        ('', '---------'),
        ('', 'DAMA'),
        ('032', 'PZA0'),
        ('033', 'UN'),
        ('034', '10'),
        ('035', '12'),
        ('036', '14'),
        ('037', '16'),
        ('038', '28'),
        ('039', '30'),
        ('040', '32'),
        ('041', '34'),
        ('042', '36'),
        ('043', '38'),
        ('044', '40'),
        ('045', '42'),
        ('046', '60'),
        ('047', '80'),
        ('048', 'XCH'),
        ('049', 'CH'),
        ('050', 'M'),
        ('051', 'G'),
        ('052', 'XG'),
        ('', '---------'),
        ('', 'JOVEN'),
        ('053', '28'),
        ('054', '30'),
        ('055', '32'),
        ('056', '34'),
        ('057', '36'),
        ('058', '38'),
        ('059', '40'),
        ('060', '42'),
        ('', '---------'),
        ('', 'NIÑA'),
        ('061', '10'),
        ('062', '12'),
        ('063', '14'),
        ('064', '16'),
        ('065', '18'),
        ('066', '18.5'),
        ('067', '19'),
        ('068', '19.5'),
        ('069', '20'),
        ('070', '20.5'),
        ('071', '21'),
        ('072', '21.5'),
        ('073', '40'),
        ('074', '60'),
        ('075', '80'),
        ('076', 'CH'),
        ('077', 'M'),
        ('078', 'G'),
        ('079', 'XG'),
        ('', '---------'),
        ('', 'NIÑO'),
        ('080', 'UN'),
        ('081', '10'),
        ('082', '12'),
        ('083', '14'),
        ('084', '16'),
        ('085', '18'),
        ('086', '28'),
        ('087', '30'),
        ('088', '32'),
        ('089', '34'),
        ('090', '36'),
        ('091', '38'),
        ('092', '40'),
        ('093', '42'),
        ('094', '44'),
        ('095', '60'),
        ('096', '80'),
        ('', '---------'),
        ('', 'UNISEX'),
        ('097', '10'),
        ('098', '12'),
        ('099', '40'),
        ('100', '60'),
        ('101', '80'),
        ('', '---------'),
        ('', 'VARIOS'),
        ('102', 'PZA0'),
        ('103', 'UN'),
        ('104', '10'),
        ('105', '12'),
        ('106', '14'),
        ('107', '16'),
        ('108', '18'),
        ('109', '32'),
        ('110', '34'),
        ('111', '36'),
        ('112', '38'),
        ('113', '40'),
        ('114', '42'),
        ('115', '60'),
        ('116', '80'),
        ('117', 'XCH'),
        ('118', 'CH'),
        ('119', 'M'),
        ('120', 'G'),
        ('121', 'XG'),
    )

    OPCIONES_MEDIDA = (
        ('', '---------'),
        ('', 'CABALLERO'),
        ('001', '18'),
        ('002', '18.5'),
        ('003', '19'),
        ('004', '19.5'),
        ('005', '20'),
        ('006', '20.5'),
        ('007', '21'),
        ('008', '21.5'),
        ('009', '22'),
        ('010', '22.5'),
        ('011', '23'),
        ('012', '23.5'),
        ('013', '24'),
        ('014', '24.5'),
        ('015', '25'),
        ('016', '25.5'),
        ('017', '26'),
        ('018', '26.5'),
        ('019', '27'),
        ('020', '27.5'),
        ('021', '28'),
        ('022', '28.5'),
        ('023', '29'),
        ('024', '29.5'),
        ('025', '30'),
        ('026', '30.5'),
        ('027', '31'),
        ('028', '31.5'),
        ('029', '32'),
        ('030', 'XCH'),
        ('031', 'CH'),
        ('032', 'M'),
        ('033', 'G'),
        ('034', 'XG'),
        ('', '---------'),
        ('', 'DAMA'),
        ('035', '21.5'),
        ('036', '22'),
        ('037', '22.5'),
        ('038', '23'),
        ('039', '23.5'),
        ('040', '24'),
        ('041', '24.5'),
        ('042', '25'),
        ('043', '25.5'),
        ('044', '26'),
        ('045', '26.5'),
        ('046', '27'),
        ('047', '27.5'),
        ('048', 'XCH'),
        ('049', 'CH'),
        ('050', 'M'),
        ('051', 'G'),
        ('052', 'XG'),
        ('', '---------'),
        ('', 'JOVEN'),
        ('053', '21.5'),
        ('054', '22'),
        ('055', '22.5'),
        ('056', '23'),
        ('057', '23.5'),
        ('058', '24'),
        ('059', '24.5'),
        ('060', '25'),
        ('061', '25.5'),
        ('062', '26'),
        ('063', '26.5'),
        ('064', '27'),
        ('', '---------'),
        ('', 'NIÑA'),
        ('065', '10'),
        ('066', '10.5'),
        ('067', '11'),
        ('068', '11.5'),
        ('069', '12'),
        ('070', '12.5'),
        ('071', '13'),
        ('072', '13.5'),
        ('073', '14'),
        ('074', '14.5'),
        ('075', '15'),
        ('076', '15.5'),
        ('077', '16'),
        ('078', '16.5'),
        ('079', '17'),
        ('080', '17.5'),
        ('081', '18'),
        ('082', '18.5'),
        ('083', '19'),
        ('084', '19.5'),
        ('085', '20'),
        ('086', '20.5'),
        ('087', '21'),
        ('088', '21.5'),
        ('089', '22'),
        ('', '---------'),
        ('', 'NIÑO'),
        ('090', '9'),
        ('091', '9.5'),
        ('092', '10'),
        ('093', '10.5'),
        ('094', '11'),
        ('095', '11.5'),
        ('096', '12'),
        ('097', '12.5'),
        ('098', '13'),
        ('099', '13.5'),
        ('100', '14'),
        ('101', '14.5'),
        ('102', '15'),
        ('103', '15.5'),
        ('104', '16'),
        ('105', '16.5'),
        ('106', '17'),
        ('107', '17.5'),
        ('108', '18'),
        ('109', '18.5'),
        ('110', '19'),
        ('111', '19.5'),
        ('112', '20'),
        ('113', '20.5'),
        ('114', '21'),
        ('115', '21.5'),
        ('116', '22'),
        ('117', '22.5'),
        ('118', '23'),
        ('119', '23.5'),
        ('120', '24'),
        ('121', '24.5'),
        ('122', '25'),
        ('123', '25.5'),
        ('124', '26'),
        ('125', '26.5'),
        ('126', '27'),
        ('127', '27.5'),
        ('128', '28'),
        ('129', '28.5'),
        ('130', '29'),
        ('131', '29.5'),
        ('132', '30'),
        ('133', '30.5'),
        ('134', '31'),
        ('135', '31.5'),
        ('136', '32'),
        ('137', 'XCH'),
        ('138', 'CH'),
        ('139', 'M'),
        ('140', 'G'),
        ('141', 'XG'),
        ('', '---------'),
        ('', 'UNISEX'),
        ('142', 'PZA'),
        ('143', '17'),
        ('144', '17.5'),
        ('145', '18'),
        ('146', '18.5'),
        ('147', '19'),
        ('148', '19.5'),
        ('149', '20'),
        ('150', '20.5'),
        ('151', '21'),
        ('152', '21.5'),
        ('153', '22'),
        ('154', '22.5'),
        ('155', '23'),
        ('156', '23.5'),
        ('157', '24'),
        ('158', '24.5'),
        ('159', '25'),
        ('160', '25.5'),
        ('161', '26'),
        ('162', '26.5'),
        ('163', '27'),
        ('164', '27.5'),
        ('165', '28'),
        ('166', '28.5'),
        ('167', '29'),
        ('168', '29.5'),
        ('169', '30'),
        ('', '---------'),
        ('', 'VARIOS'),
        ('170', '18'),
        ('171', '18.5'),
        ('172', '19'),
        ('173', '19.5'),
        ('174', '20'),
        ('175', '20.5'),
        ('176', '21'),
        ('177', '21.5'),
        ('178', '22'),
        ('179', '22.5'),
        ('180', '23'),
        ('181', '23.5'),
        ('182', '24'),
        ('183', '24.5'),
        ('184', '26'),
        ('185', '26.5'),
        ('186', '27'),
        ('187', '27.5'),
        ('188', '28'),
        ('189', '28.5'),
        ('190', '29'),
        ('191', '29.5'),
        ('192', '30'),
    )

    OPCIONES_PIEZA = (
        ('', '---------'),
        ('', 'CABALLERO'),
        ('01', '26'),
        ('02', '26.5'),
        ('03', '27'),
        ('04', '27.5'),
        ('05', '28'),
        ('06', '28.5'),
        ('07', '29'),
        ('08', '29.5'),
        ('09', '30'),
        ('10', 'XCH'),
        ('11', 'CH'),
        ('12', 'M'),
        ('13', 'G'),
        ('14', 'XG'),
        ('', '---------'),
        ('', 'DAMA'),
        ('15', 'PZA'),
        ('16', '21'),
        ('17', '22'),
        ('18', '23'),
        ('19', '24'),
        ('20', '25'),
        ('21', 'XCH'),
        ('22', 'CH'),
        ('23', 'M'),
        ('24', 'G'),
        ('25', 'XG'),
        ('', '---------'),
        ('', 'NIÑO'),
        ('26', '15'),
        ('27', '15.5'),
        ('28', '16'),
        ('29', '16.5'),
        ('30', '17'),
        ('31', '17.5'),
        ('32', '18'),
        ('33', '18.5'),
        ('34', '19'),
        ('35', '19.5'),
        ('36', '20'),
        ('37', '20.5'),
        ('38', '21'),
        ('39', '21.5'),
        ('', '---------'),
        ('', 'UNISEX'),
        ('40', 'PZA'),
        ('', '---------'),
        ('', 'VARIOS'),
        ('41', 'PZA'),
    )

    OPCIONES_LINEA_CALZADO = (
        ('', '---------'),
        ('00', 'ANTE'),
        ('01', 'PIEL'),
        ('02', 'PIEL/SINTETICO'),
        ('03', 'SINTETICO'),
        ('04', 'SINTETICO/TEXTIL'),
        ('05', 'TEXTIL'),
        ('06', 'TEXTIL/SINTETICO'),
    )

    OPCIONES_LINEA_ROPA = (
        ('', '---------'),
        ('00', 'SINTETICO'),
        ('01', 'TEXTIL'),
    )

    OPCIONES_LINEA_ACCESORIOS = (
        ('', '---------'),
        ('00', 'PIEL'),
        ('01', 'SINTETICO'),
        ('02', 'TEXTIL'),
    )

    OPCIONES_GENERO = (
        ('', '---------'),
        ('0', 'BEBE'),
        ('1', 'CABALLERO'),
        ('2', 'DAMA'),
        ('3', 'JOVEN'),
        ('4', 'NIÑA'),
        ('5', 'NIÑO'),
        ('6', 'UNISEX'),
        ('7', 'VARIOS'),
    )

    OPCIONES_COLOR = (
        ('000', 'AJEDREZ/MARINO'),
        ('001', 'AJEDREZ/NEGRO'),
        ('002', 'ALERCE'),
        ('003', 'ALPISTE'),
        ('004', 'AMARILLO'),
        ('005', 'ARENA'),
        ('006', 'ARENA/GAMUZA'),
        ('007', 'ARENA/NUBUCK'),
        ('008', 'AVELLANA'),
        ('009', 'AVELLANA/NUBUCK'),
        ('010', 'AZUL'),
        ('011', 'AZUL/ANTE'),
        ('012', 'AZUL/BLANCO'),
        ('013', 'AZUL/MARINO'),
        ('014', 'AZUL/NEGRO'),
        ('015', 'AZUL/REY'),
        ('016', 'AZUL/ROJO'),
        ('017', 'AZUL/ROSA'),
        ('018', 'AZULCIELO'),
        ('019', 'AZULCIELO/CUADROS'),
        ('020', 'AZULCLARO'),
        ('021', 'AZULLTURQUEZA'),
        ('022', 'AZULMARINO'),
        ('023', 'AZULREY'),
        ('024', 'BEIGE'),
        ('025', 'BEIGE/CAMEL'),
        ('026', 'BEIGE/CHAROL'),
        ('027', 'BEIGE/NEGRO'),
        ('028', 'BLANCO'),
        ('029', 'BLANCO/ANANAS'),
        ('030', 'BLANCO/AZUL'),
        ('031', 'BLANCO/AZULCIELO'),
        ('032', 'BLANCO/AZULMARINO'),
        ('033', 'BLANCO/CHAROL'),
        ('034', 'BLANCO/CHAROL/GLITTER'),
        ('035', 'BLANCO/CORAL'),
        ('036', 'BLANCO/FIUSHA'),
        ('037', 'BLANCO/FLOR'),
        ('038', 'BLANCO/GRIS'),
        ('039', 'BLANCO/GRIS/ROJO'),
        ('040', 'BLANCO/GRIS/ROSA'),
        ('041', 'BLANCO/JASPEADO'),
        ('042', 'BLANCO/LILA'),
        ('043', 'BLANCO/LILA/ANANAS'),
        ('044', 'BLANCO/MARINO'),
        ('045', 'BLANCO/MARINO/PLATA'),
        ('046', 'BLANCO/MULTICOLOR'),
        ('047', 'BLANCO/NACAR'),
        ('048', 'BLANCO/NEGRO'),
        ('049', 'BLANCO/NEGRO/ROJO'),
        ('050', 'BLANCO/ORO'),
        ('051', 'BLANCO/PLATA'),
        ('052', 'BLANCO/ROJO'),
        ('053', 'BLANCO/ROSA'),
        ('054', 'BLANCO/VERDE'),
        ('055', 'BRANDY'),
        ('056', 'BROWN'),
        ('057', 'BUCK/ROSA'),
        ('058', 'BURGUNDY'),
        ('059', 'CABRA/ROJO'),
        ('060', 'CAFE'),
        ('061', 'CAFE/AZUL'),
        ('062', 'CAFE/BEIGE'),
        ('063', 'CAFE/BLANCO'),
        ('064', 'CAFE/CARNAZA'),
        ('065', 'CAFE/DURAZNO'),
        ('066', 'CAFE/MIEL'),
        ('067', 'CAFE/RAYAS'),
        ('068', 'CAJETA'),
        ('069', 'CAJETA/NOBUCK'),
        ('070', 'CAMEL'),
        ('071', 'CAMEL/MARINO'),
        ('072', 'CAMUFLAJE/VERDE'),
        ('073', 'CAPUCHINO/DURAZNO'),
        ('074', 'CEREZA/CHAROL'),
        ('075', 'CHAROL/ANTE/NEGRO'),
        ('076', 'CHAROL/HUESO'),
        ('077', 'CHAROL/MAQUILLAJE'),
        ('078', 'CHAROL/NEGRO'),
        ('079', 'CHAROL/NEUTRO'),
        ('080', 'CHAROL/PLATA'),
        ('081', 'CHAROL/VINO'),
        ('082', 'CHOCOLATE'),
        ('083', 'CIELO'),
        ('084', 'CLAY'),
        ('085', 'COGÑAC'),
        ('086', 'CORAL'),
        ('087', 'COÑAC'),
        ('088', 'CRISTAL/PLATA'),
        ('089', 'CUADRI/ROJO'),
        ('090', 'CUADROS/ROJO/AZUL'),
        ('091', 'CUARZO'),
        ('092', 'DIURNA'),
        ('093', 'ESCOSES'),
        ('094', 'FERRERO/GAMUZA'),
        ('095', 'FIUSHA'),
        ('096', 'FIUSHA/BLANCO'),
        ('097', 'FIUSHA/CORAL'),
        ('098', 'FIUSHA/LILA'),
        ('099', 'FIUSHA/ROSA'),
        ('100', 'GLITTER/NEGRO'),
        ('101', 'GLITTER/PLATA'),
        ('102', 'GRIS'),
        ('103', 'GRIS/CORAL'),
        ('104', 'GRIS/FIUSHA'),
        ('105', 'GRIS/LILA'),
        ('106', 'GRIS/NEGRO'),
        ('107', 'GRIS/NUBUCK'),
        ('108', 'GRIS/OXFORD'),
        ('109', 'GRIS/PERLA'),
        ('110', 'GRIS/ROJO'),
        ('111', 'GRIS/ROSA'),
        ('112', 'HUESO/CHAROL'),
        ('113', 'JAVA/GAMUZA'),
        ('114', 'LADRILLO'),
        ('115', 'LATTE'),
        ('116', 'LATTE/ORO'),
        ('117', 'LAVANDA'),
        ('118', 'LILA'),
        ('119', 'LILA/AZUL'),
        ('120', 'LILA/BLANCO/MENTA'),
        ('121', 'LILA/GRIS'),
        ('122', 'LILA/MENTA'),
        ('123', 'LILA/MORADO'),
        ('124', 'LILA/SALMON'),
        ('125', 'LIMON/ROSA'),
        ('126', 'MADERA'),
        ('127', 'MADERA/DURAZNO'),
        ('128', 'MAQUILLAJE'),
        ('129', 'MAQUILLAJE/BLANCO'),
        ('130', 'MAQUILLAJE/BUCK'),
        ('131', 'MAQUILLAJE/CAMEL'),
        ('132', 'MAQUILLAJE/CHAROL'),
        ('133', 'MARFIL'),
        ('134', 'MARINO'),
        ('135', 'MARINO/AQUA'),
        ('136', 'MARINO/BLANCO'),
        ('137', 'MARINO/CAMEL'),
        ('138', 'MARINO/CORAL'),
        ('139', 'MARINO/DURAZNO'),
        ('140', 'MARINO/FIUSHA'),
        ('141', 'MARINO/GRIS'),
        ('142', 'MARINO/GRIS/BLANCO'),
        ('143', 'MARINO/LIMON'),
        ('144', 'MARINO/MEZCLILLA'),
        ('145', 'MARINO/NARANJA'),
        ('146', 'MARINO/NEON'),
        ('147', 'MARINO/NOBUCK'),
        ('148', 'MARINO/PLATA'),
        ('149', 'MARINO/REY'),
        ('150', 'MARINO/ROJO'),
        ('151', 'MARINO/ROSA'),
        ('152', 'MARINO/TURQUEZA'),
        ('153', 'MARRON/CAMUFLAJE'),
        ('154', 'MELLE/DURAZNO'),
        ('155', 'MELLE/ORPEL'),
        ('156', 'MERCURIO'),
        ('157', 'MERCURIO/GLITTER'),
        ('158', 'MERLOT/CHAROL'),
        ('159', 'METALICA'),
        ('160', 'MEZCLILLA'),
        ('161', 'MEZCLILLA/ROJO'),
        ('162', 'MIEL'),
        ('163', 'MIEL/DURAZNO'),
        ('164', 'MIEL/NUBUCK'),
        ('165', 'MIGA/CHAROL'),
        ('166', 'MILITAR'),
        ('167', 'MILLENIAL'),
        ('168', 'MOKA'),
        ('169', 'MOKA/NOBUCK'),
        ('170', 'MOMJEANS/AZUL'),
        ('171', 'MORADO'),
        ('172', 'MORADO/FIUSHA'),
        ('173', 'MORADO/NEON'),
        ('174', 'MOSTAZA/AMBAR'),
        ('175', 'MULTICOLOR'),
        ('176', 'MUSGO'),
        ('177', 'NAVY'),
        ('178', 'NAVY/NOBUCK'),
        ('179', 'NEBRASKA/ROSA'),
        ('180', 'NEGRO'),
        ('181', 'NEGRO/AMBAR'),
        ('182', 'NEGRO/AQUA'),
        ('183', 'NEGRO/ARCOIRIS'),
        ('184', 'NEGRO/AZUL'),
        ('185', 'NEGRO/BLANCO'),
        ('186', 'NEGRO/BUCK'),
        ('187', 'NEGRO/CABRA'),
        ('188', 'NEGRO/CAFE'),
        ('189', 'NEGRO/CANELA'),
        ('190', 'NEGRO/CHAROL'),
        ('191', 'NEGRO/CORAL'),
        ('192', 'NEGRO/CRAZY'),
        ('193', 'NEGRO/DURAZNO'),
        ('194', 'NEGRO/FIUSHA'),
        ('195', 'NEGRO/GAMUZA'),
        ('196', 'NEGRO/GRIS'),
        ('197', 'NEGRO/JASPEADO'),
        ('198', 'NEGRO/MENTA'),
        ('199', 'NEGRO/MORADO'),
        ('200', 'NEGRO/NARANJA'),
        ('201', 'NEGRO/NEON'),
        ('202', 'NEGRO/NOBUCK'),
        ('203', 'NEGRO/ORO'),
        ('204', 'NEGRO/ORPEL'),
        ('205', 'NEGRO/OXFORD'),
        ('206', 'NEGRO/PLATA'),
        ('207', 'NEGRO/RAYAS'),
        ('208', 'NEGRO/REFLEX'),
        ('209', 'NEGRO/REY'),
        ('210', 'NEGRO/ROJO'),
        ('211', 'NEGRO/ROJO/BLANCO'),
        ('212', 'NEGRO/ROJO/GRIS'),
        ('213', 'NEGRO/ROSA'),
        ('214', 'NEGRO/VERDE'),
        ('215', 'NEGRO/VINO'),
        ('216', 'NOBUCK/AZUL'),
        ('217', 'NUBUCK/ORO'),
        ('218', 'NUDE'),
        ('219', 'NUEZ'),
        ('220', 'NUTTY'),
        ('221', 'OCRE'),
        ('222', 'OLIVO'),
        ('223', 'OPORTO'),
        ('224', 'ORO'),
        ('225', 'ORO/AMBAR'),
        ('226', 'ORO/CHAROL'),
        ('227', 'ORO/INGLES'),
        ('228', 'ORO/OSTION'),
        ('229', 'ORO/ROSADO'),
        ('230', 'ORQUIDEA'),
        ('231', 'OXFORD'),
        ('232', 'OXFORD/CORAL'),
        ('233', 'OXFORD/NARANJA'),
        ('234', 'OXFORD/NEGRO'),
        ('235', 'OXFORD/NEGRO/ORO'),
        ('236', 'OXFORD/ORO'),
        ('237', 'OXFORD/ROJO'),
        ('238', 'OXFORD/ROSA'),
        ('239', 'PALODEROSA'),
        ('240', 'PALOMITAS'),
        ('241', 'PATADEGALLO'),
        ('242', 'PATHE/NOBUCK'),
        ('243', 'PERLA'),
        ('244', 'PERLA/CHAROL'),
        ('245', 'PETALO'),
        ('246', 'PLATA'),
        ('247', 'PLATA/GLITTER'),
        ('248', 'PLATINA'),
        ('249', 'PRINCIPESGALES'),
        ('250', 'RATO/DURAZNO'),
        ('251', 'RAYAS/LILA'),
        ('252', 'REY'),
        ('253', 'REY/LIMON'),
        ('254', 'REY/MARINO'),
        ('255', 'REY/NEGRO'),
        ('256', 'REY/RAYAS'),
        ('257', 'ROJO'),
        ('258', 'ROJO/AZUL'),
        ('259', 'ROJO/BLANCO'),
        ('260', 'ROJO/CHAROL'),
        ('261', 'ROJO/DURAZNO'),
        ('262', 'ROJO/NEGRO'),
        ('263', 'ROSA'),
        ('264', 'ROSA/AZUL'),
        ('265', 'ROSA/BLANCO'),
        ('266', 'ROSA/CHAROL'),
        ('267', 'ROSA/CORAL'),
        ('268', 'ROSA/FIUSHA'),
        ('269', 'ROSA/GRIS'),
        ('270', 'ROSA/LILA'),
        ('271', 'ROSA/METALICO'),
        ('272', 'ROSA/MORADO'),
        ('273', 'ROSA/MULTICOLOR'),
        ('274', 'ROSA/NEGRO'),
        ('275', 'ROSA/PASTEL'),
        ('276', 'SALMON'),
        ('277', 'SHEDRON'),
        ('278', 'TABACO'),
        ('279', 'TABACO/ANTE'),
        ('280', 'TABACO/NOBUCK'),
        ('281', 'TAN'),
        ('282', 'TANG/CABRA'),
        ('283', 'TAUPE'),
        ('284', 'TECNICA'),
        ('285', 'TIEDYE'),
        ('286', 'TOPO/GAMUZA'),
        ('287', 'TURQUEZA'),
        ('288', 'TURQUEZA/BLANCO'),
        ('289', 'VARIOS'),
        ('290', 'VERDE'),
        ('291', 'VINO'),
        ('292', 'VINO/CHAROL'),
        ('293', 'VINO/DURAZNO'),
        ('294', 'VINO/NEGRO'),
        ('295', 'VINO/ROJO'),
        ('296', 'VIOLETA'),
        ('297', 'VIOLETA/MORADO'),
        ('298', 'WHISKY'),
        ('299', 'ZANAHORIA'),
    )

    OPCION_PROMOCIONES = (
        ('', '---------'),
        ('0', 'Sin promoción'),
        ('', ''),
        ('1', '10 %'),
        ('2', '20 %'),
        ('3', '30 %'),
        ('', ''),
        ('4', '2 x 1'),
        ('5', '3 x 2'),
        ('', ''),
        ('6', '1=10%, 2=20%'),
        ('', ''),
        ('7', '2 Adidas y obtén 10%'),
        ('', ''),
        ('8', '- $89.00'),
        ('9', '- $99.00'),
        ('10', '- $199.00'),
        ('11', '- $299.00'),
        ('', ''),
        ('12', 'Descuento establecido por tienda'),
    )

    # Atributos necesarios
    barcode = models.CharField('Código de barras', max_length=13, blank=True, unique=True)
    barcode_exterior = models.CharField('Código de barras', max_length=15, blank=True)
    nombre = models.CharField('Nombre', max_length=40)

    # Atributos foreignkey
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    
    # Atributos de opciones
    tipo = models.CharField('Tipo de producto', max_length=3, choices=OPCIONES_TIPO_PRODUCTO)
    almacen = models.CharField('Almacén', max_length=4, choices=OPCIONES_ALMACEN)
    talla = models.CharField('Talla', max_length=3, blank=True, choices=OPCIONES_TALLA)
    medida = models.CharField('Medida', max_length=3, blank=True, choices=OPCIONES_MEDIDA)
    pieza = models.CharField('Pieza', max_length=2, blank=True, choices=OPCIONES_PIEZA)
    linea_a = models.CharField('Línea de accesorios', max_length=2, blank=True, choices=OPCIONES_LINEA_ACCESORIOS)
    linea_c = models.CharField('Línea de calzado', max_length=2, blank=True, choices=OPCIONES_LINEA_CALZADO)
    linea_r = models.CharField('Línea de ropa', max_length=2, blank=True, choices=OPCIONES_LINEA_ROPA)
    color = models.CharField('Color', max_length=3, blank=True, choices=OPCIONES_COLOR)
    genero = models.CharField('Género', max_length=1, blank=True, choices=OPCIONES_GENERO)
    promocion = models.CharField('Promociones', max_length=2, blank=True, choices=OPCION_PROMOCIONES, default='0')
    fecha_final_promocion = models.DateTimeField('Fecha final de promoción', null=True, blank=True)

    # Atributos no necesarios
    modelo = models.CharField('Modelo', max_length=25, blank=True)
    stock = models.PositiveIntegerField('Existencias', default=0)
    precio_compra = models.DecimalField('Precio de compra', max_digits=7, decimal_places=2, default=0)
    precio_venta = models.DecimalField('Precio de venta', max_digits=7, decimal_places=2, default=0)
    num_venta = models.PositiveIntegerField('Número de ventas', default=0)
    anular = models.BooleanField('Anular Producto', default=False)

    # Imagen del producto
    img = models.ImageField('Imagen', upload_to='productos', blank=True, null=True)

    # Managers
    objects = filtros()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Inventario de Productos'
        ordering = ['-id']
        db_table = 'Productos'
    
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Productos, self).save(*args, **kwargs)

    def __str__(self):
        return self.marca.nombre + ' - ' + self.modelo + ' - ' + self.get_genero_display()

class Movimientos(TimeStampedModel):
    barcode = models.CharField('Código de barras', max_length=13)
    stock_nuevo = models.IntegerField('Cantidad de productos ingresados',  default=0)
    fecha = models.DateTimeField('Fecha y hora de actualización')
    precio_costo = models.DecimalField('Precio de costo', max_digits=7, decimal_places=2, default=0)
    total_costo = models.DecimalField('Costo total de productos ingresados', max_digits=7, decimal_places=2, default=0)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, verbose_name='Producto', related_name='movimientos_producto')

    class Meta:
        verbose_name = 'Movimientos'
        verbose_name_plural = 'Movimientos'
        ordering = ['-id']
        db_table = 'Movimientos'
    
    def __str__(self):
        return self.producto.nombre

# Funcion para optimizar el atributo IMG del modelo Productos
def optimizar_img(sender, instance, **kwargs):
    if instance.img:
        img = Image.open(instance.img.path)
        img.save(instance.img.path, quality=20, optimize=True)

post_save.connect(optimizar_img, sender=Productos)

# Funcion para registrar los cambios del modelo Productos
def movimientos_productos(sender, instance, **kwargs):
    try:
        stock_anterior = Productos.objects.get(barcode=instance.barcode)
        stock_anterior.stock = str(stock_anterior.stock)
        stock_anterior = int(stock_anterior.stock)
        #
        stock_nuevo = instance.stock
        stock_nuevo = int(stock_nuevo)
        #
        stock_ingresado = stock_nuevo - stock_anterior
        #
        precio_costo = Productos.objects.get(barcode=instance.barcode)
        costo = Decimal(stock_ingresado) * precio_costo.precio_compra
        #
        producto_modificado = Productos.objects.get(barcode=instance.barcode)
        producto_modificado.nombre = str(producto_modificado.nombre)
        costo_producto = precio_costo.precio_compra
        #
        mov = Movimientos.objects.create(
            barcode=instance.barcode,
            stock_nuevo=stock_ingresado,
            fecha=timezone.now(),
            total_costo=costo,
            producto=producto_modificado,
            precio_costo=costo_producto
        )
        mov.save()
    except Productos.DoesNotExist:
        return []
    else:
        return []

pre_save.connect(movimientos_productos, sender=Productos)

# Funcion para agregar el código de barras
def product(sender, instance, **kwargs):
    try:
        if instance.id > 0 and instance.id < 10:
            Productos.objects.filter(barcode=instance.barcode).update(
                barcode = str(instance.almacen)+str(instance.tipo)+"00000"+str(instance.id)
            )
        elif instance.id > 9 and instance.id < 100:
            Productos.objects.filter(barcode=instance.barcode).update(
                barcode = str(instance.almacen)+str(instance.tipo)+"0000"+str(instance.id)
            )
        elif instance.id > 99 and instance.id < 1000:
            Productos.objects.filter(barcode=instance.barcode).update(
                barcode = str(instance.almacen)+str(instance.tipo)+"000"+str(instance.id)
            )
        elif instance.id > 999 and instance.id < 10000:
            Productos.objects.filter(barcode=instance.barcode).update(
                barcode = str(instance.almacen)+str(instance.tipo)+"00"+str(instance.id)
            )
        elif instance.id > 9999 and instance.id < 100000:
            Productos.objects.filter(barcode=instance.barcode).update(
                barcode = str(instance.almacen)+str(instance.tipo)+"0"+str(instance.id)
            )
        elif instance.id > 99999:
            Productos.objects.filter(barcode=instance.barcode).update(
                barcode = str(instance.almacen)+str(instance.tipo)+str(instance.id)
            )

    except Productos.DoesNotExist:
        return []

post_save.connect(product, sender=Productos)