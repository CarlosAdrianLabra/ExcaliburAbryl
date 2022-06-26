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
        ('1', 'UN'),
        ('2', 'PZA'),
        ('', '---------'),
        ('', 'CABALLERO'),
        ('3', 'UN'),
        ('4', '10'),
        ('5', '12'),
        ('6', '14'),
        ('7', '14.5'),
        ('8', '15'),
        ('9', '15.5'),
        ('10', '16'),
        ('11', '16.5'),
        ('12', '17'),
        ('13', '17.5'),
        ('14', '18'),
        ('15', '20'),
        ('16', '22'),
        ('17', '24'),
        ('18', '26'),
        ('19', '28'),
        ('20', '30'),
        ('21', '32'),
        ('22', '34'),
        ('23', '36'),
        ('24', '38'),
        ('25', '40'),
        ('26', '42'),
        ('27', '80'),
        ('28', 'CH'),
        ('29', 'M'),
        ('30', 'G'),
        ('31', 'XG'),
        ('', '---------'),
        ('', 'DAMA'),
        ('32', 'PZA0'),
        ('33', 'UN'),
        ('34', '10'),
        ('35', '12'),
        ('36', '14'),
        ('37', '16'),
        ('38', '28'),
        ('39', '30'),
        ('40', '32'),
        ('41', '34'),
        ('42', '36'),
        ('43', '38'),
        ('44', '40'),
        ('45', '42'),
        ('46', '60'),
        ('47', '80'),
        ('48', 'XCH'),
        ('49', 'CH'),
        ('50', 'M'),
        ('51', 'G'),
        ('52', 'XG'),
        ('', '---------'),
        ('', 'JOVEN'),
        ('53', '28'),
        ('54', '30'),
        ('55', '32'),
        ('56', '34'),
        ('57', '36'),
        ('58', '38'),
        ('59', '40'),
        ('60', '42'),
        ('', '---------'),
        ('', 'NIÑA'),
        ('61', '10'),
        ('62', '12'),
        ('63', '14'),
        ('64', '16'),
        ('65', '18'),
        ('66', '18.5'),
        ('67', '19'),
        ('68', '19.5'),
        ('69', '20'),
        ('70', '20.5'),
        ('71', '21'),
        ('72', '21.5'),
        ('73', '40'),
        ('74', '60'),
        ('75', '80'),
        ('76', 'CH'),
        ('77', 'M'),
        ('78', 'G'),
        ('79', 'XG'),
        ('', '---------'),
        ('', 'NIÑO'),
        ('80', 'UN'),
        ('81', '10'),
        ('82', '12'),
        ('83', '14'),
        ('84', '16'),
        ('85', '18'),
        ('86', '28'),
        ('87', '30'),
        ('88', '32'),
        ('89', '34'),
        ('90', '36'),
        ('91', '38'),
        ('92', '40'),
        ('93', '42'),
        ('94', '44'),
        ('95', '60'),
        ('96', '80'),
        ('', '---------'),
        ('', 'UNISEX'),
        ('97', '10'),
        ('98', '12'),
        ('99', '40'),
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
        ('1', '18'),
        ('2', '18.5'),
        ('3', '19'),
        ('4', '19.5'),
        ('5', '20'),
        ('6', '20.5'),
        ('7', '21'),
        ('8', '21.5'),
        ('9', '22'),
        ('10', '22.5'),
        ('11', '23'),
        ('12', '23.5'),
        ('13', '24'),
        ('14', '24.5'),
        ('15', '25'),
        ('16', '25.5'),
        ('17', '26'),
        ('18', '26.5'),
        ('19', '27'),
        ('20', '27.5'),
        ('21', '28'),
        ('22', '28.5'),
        ('23', '29'),
        ('24', '29.5'),
        ('25', '30'),
        ('26', '30.5'),
        ('27', '31'),
        ('28', '31.5'),
        ('29', '32'),
        ('30', 'XCH'),
        ('31', 'CH'),
        ('32', 'M'),
        ('33', 'G'),
        ('34', 'XG'),
        ('', '---------'),
        ('', 'DAMA'),
        ('35', '21.5'),
        ('36', '22'),
        ('37', '22.5'),
        ('38', '23'),
        ('39', '23.5'),
        ('40', '24'),
        ('41', '24.5'),
        ('42', '25'),
        ('43', '25.5'),
        ('44', '26'),
        ('45', '26.5'),
        ('46', '27'),
        ('47', '27.5'),
        ('48', 'XCH'),
        ('49', 'CH'),
        ('50', 'M'),
        ('51', 'G'),
        ('52', 'XG'),
        ('', '---------'),
        ('', 'JOVEN'),
        ('53', '21.5'),
        ('54', '22'),
        ('55', '22.5'),
        ('56', '23'),
        ('57', '23.5'),
        ('58', '24'),
        ('59', '24.5'),
        ('60', '25'),
        ('61', '25.5'),
        ('62', '26'),
        ('63', '26.5'),
        ('64', '27'),
        ('', '---------'),
        ('', 'NIÑA'),
        ('65', '10'),
        ('66', '10.5'),
        ('67', '11'),
        ('68', '11.5'),
        ('69', '12'),
        ('70', '12.5'),
        ('71', '13'),
        ('72', '13.5'),
        ('73', '14'),
        ('74', '14.5'),
        ('75', '15'),
        ('76', '15.5'),
        ('77', '16'),
        ('78', '16.5'),
        ('79', '17'),
        ('80', '17.5'),
        ('81', '18'),
        ('82', '18.5'),
        ('83', '19'),
        ('84', '19.5'),
        ('85', '20'),
        ('86', '20.5'),
        ('87', '21'),
        ('88', '21.5'),
        ('89', '22'),
        ('', '---------'),
        ('', 'NIÑO'),
        ('90', '9'),
        ('91', '9.5'),
        ('92', '10'),
        ('93', '10.5'),
        ('94', '11'),
        ('95', '11.5'),
        ('96', '12'),
        ('97', '12.5'),
        ('98', '13'),
        ('99', '13.5'),
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
        ('1', '26'),
        ('2', '26.5'),
        ('3', '27'),
        ('4', '27.5'),
        ('5', '28'),
        ('6', '28.5'),
        ('7', '29'),
        ('8', '29.5'),
        ('9', '30'),
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
        ('0', 'ANTE'),
        ('1', 'PIEL'),
        ('2', 'PIEL/SINTETICO'),
        ('3', 'SINTETICO'),
        ('4', 'SINTETICO/TEXTIL'),
        ('5', 'TEXTIL'),
        ('6', 'TEXTIL/SINTETICO'),
    )

    OPCIONES_LINEA_ROPA = (
        ('', '---------'),
        ('0', 'SINTETICO'),
        ('1', 'TEXTIL'),
    )

    OPCIONES_LINEA_ACCESORIOS = (
        ('', '---------'),
        ('0', 'PIEL'),
        ('1', 'SINTETICO'),
        ('2', 'TEXTIL'),
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
        ('0', 'AJEDREZ/MARINO'),
        ('1', 'AJEDREZ/NEGRO'),
        ('2', 'ALERCE'),
        ('3', 'ALPISTE'),
        ('4', 'AMARILLO'),
        ('5', 'ARENA'),
        ('6', 'ARENA/GAMUZA'),
        ('7', 'ARENA/NUBUCK'),
        ('8', 'AVELLANA'),
        ('9', 'AVELLANA/NUBUCK'),
        ('10', 'AZUL'),
        ('11', 'AZUL/ANTE'),
        ('12', 'AZUL/BLANCO'),
        ('13', 'AZUL/MARINO'),
        ('14', 'AZUL/NEGRO'),
        ('15', 'AZUL/REY'),
        ('16', 'AZUL/ROJO'),
        ('17', 'AZUL/ROSA'),
        ('18', 'AZULCIELO'),
        ('19', 'AZULCIELO/CUADROS'),
        ('20', 'AZULCLARO'),
        ('21', 'AZULLTURQUEZA'),
        ('22', 'AZULMARINO'),
        ('23', 'AZULREY'),
        ('24', 'BEIGE'),
        ('25', 'BEIGE/CAMEL'),
        ('26', 'BEIGE/CHAROL'),
        ('27', 'BEIGE/NEGRO'),
        ('28', 'BLANCO'),
        ('29', 'BLANCO/ANANAS'),
        ('30', 'BLANCO/AZUL'),
        ('31', 'BLANCO/AZULCIELO'),
        ('32', 'BLANCO/AZULMARINO'),
        ('33', 'BLANCO/CHAROL'),
        ('34', 'BLANCO/CHAROL/GLITTER'),
        ('35', 'BLANCO/CORAL'),
        ('36', 'BLANCO/FIUSHA'),
        ('37', 'BLANCO/FLOR'),
        ('38', 'BLANCO/GRIS'),
        ('39', 'BLANCO/GRIS/ROJO'),
        ('40', 'BLANCO/GRIS/ROSA'),
        ('41', 'BLANCO/JASPEADO'),
        ('42', 'BLANCO/LILA'),
        ('43', 'BLANCO/LILA/ANANAS'),
        ('44', 'BLANCO/MARINO'),
        ('45', 'BLANCO/MARINO/PLATA'),
        ('46', 'BLANCO/MULTICOLOR'),
        ('47', 'BLANCO/NACAR'),
        ('48', 'BLANCO/NEGRO'),
        ('49', 'BLANCO/NEGRO/ROJO'),
        ('50', 'BLANCO/ORO'),
        ('51', 'BLANCO/PLATA'),
        ('52', 'BLANCO/ROJO'),
        ('53', 'BLANCO/ROSA'),
        ('54', 'BLANCO/VERDE'),
        ('55', 'BRANDY'),
        ('56', 'BROWN'),
        ('57', 'BUCK/ROSA'),
        ('58', 'BURGUNDY'),
        ('59', 'CABRA/ROJO'),
        ('60', 'CAFE'),
        ('61', 'CAFE/AZUL'),
        ('62', 'CAFE/BEIGE'),
        ('63', 'CAFE/BLANCO'),
        ('64', 'CAFE/CARNAZA'),
        ('65', 'CAFE/DURAZNO'),
        ('66', 'CAFE/MIEL'),
        ('67', 'CAFE/RAYAS'),
        ('68', 'CAJETA'),
        ('69', 'CAJETA/NOBUCK'),
        ('70', 'CAMEL'),
        ('71', 'CAMEL/MARINO'),
        ('72', 'CAMUFLAJE/VERDE'),
        ('73', 'CAPUCHINO/DURAZNO'),
        ('74', 'CEREZA/CHAROL'),
        ('75', 'CHAROL/ANTE/NEGRO'),
        ('76', 'CHAROL/HUESO'),
        ('77', 'CHAROL/MAQUILLAJE'),
        ('78', 'CHAROL/NEGRO'),
        ('79', 'CHAROL/NEUTRO'),
        ('80', 'CHAROL/PLATA'),
        ('81', 'CHAROL/VINO'),
        ('82', 'CHOCOLATE'),
        ('83', 'CIELO'),
        ('84', 'CLAY'),
        ('85', 'COGÑAC'),
        ('86', 'CORAL'),
        ('87', 'COÑAC'),
        ('88', 'CRISTAL/PLATA'),
        ('89', 'CUADRI/ROJO'),
        ('90', 'CUADROS/ROJO/AZUL'),
        ('91', 'CUARZO'),
        ('92', 'DIURNA'),
        ('93', 'ESCOSES'),
        ('94', 'FERRERO/GAMUZA'),
        ('95', 'FIUSHA'),
        ('96', 'FIUSHA/BLANCO'),
        ('97', 'FIUSHA/CORAL'),
        ('98', 'FIUSHA/LILA'),
        ('99', 'FIUSHA/ROSA'),
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
        ('13', 'Descuento familiar'),
    )

    # Atributos necesarios
    barcode = models.CharField('Código de barras', max_length=13, blank=True, unique=True)
    barcode_exterior = models.CharField('Código de barras', max_length=15, blank=True)
    nombre = models.CharField('Nombre', max_length=30)

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

# Modelo de movimientos (actualizaciones de inventario)
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

# Modelo para subir archivos
class ArchivoSubido(models.Model):

    OPCIONES_TIPO = (
        ('1', 'Marca'),
        ('2', 'Proveedor'),
        ('3', 'Accesorios'),
        ('4', 'Calzado'),
        ('5', 'Ropa'),
    )

    archivo = models.FileField('Archivo', upload_to='archivos/')
    fecha = models.DateTimeField('Fecha de subida', auto_now_add=True)
    tipo = models.CharField('Tipo de archivo', max_length=2, choices=OPCIONES_TIPO, blank=True)

    class Meta:
        verbose_name = 'Archivo Subido'
        verbose_name_plural = 'Archivos Subidos'
        db_table = 'ArchivoSubido'

    def __str__(self):
        return str(self.archivo)