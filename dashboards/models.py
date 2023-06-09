from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.db import models

from _keenthemes.settings import MEDIA_URL, STATIC_URL

class Provincia(models.Model):
    history = AuditlogHistoryField()
    nombre = models.CharField(max_length=20, verbose_name='Provincia')
    codigo = models.CharField(max_length=2, verbose_name='Código')
    sigla = models.CharField(max_length=3, verbose_name='Sigla')
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'provincia'
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'

    def __str__(self):
        return self.nombre

class Organismo(models.Model):
    history = AuditlogHistoryField()
    nombre = models.CharField(verbose_name='Nombre', max_length=50)
    codigo = models.CharField(verbose_name='Codigo', max_length=5, unique=True)
    sigla = models.CharField(verbose_name='Sigla', max_length=13)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'organismo'
        verbose_name = 'Organismo'
        verbose_name_plural = 'Organismos'

    def __str__(self):
        return self.nombre

auditlog.register(Organismo)

class Osde(models.Model):
    history = AuditlogHistoryField()
    organismo = models.ForeignKey(Organismo, verbose_name='Organismo', on_delete=models.PROTECT)
    codigo = models.CharField(verbose_name='Código', max_length=5, unique=True)
    nombre = models.CharField(verbose_name='Nombre del OSDE', max_length=50)
    sigla = models.CharField(verbose_name='Sigla', max_length=13)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'osde'
        verbose_name = 'OSDE'
        verbose_name_plural = 'OSDE'

    def __str__(self):
        return self.nombre

auditlog.register(Osde)

class Empresa(models.Model):
    history = AuditlogHistoryField()
    osde = models.ForeignKey(Osde, verbose_name='Osde', on_delete=models.PROTECT,null=True,blank=True)
    provincia = models.ForeignKey(Provincia, verbose_name='Provincia', on_delete=models.PROTECT,null=True,blank=True)
    nombre = models.CharField("Nombre comercial", max_length=200)
    reup_code = models.CharField("Código REEUP", max_length=120, null=True, blank=False)
    codigo = models.CharField(verbose_name='Código', max_length=5)
    activa = models.BooleanField(verbose_name='Activa', default=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'empresa'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']

auditlog.register(Empresa)


# Create your models here.

# Create your models here.
class Marca(models.Model):
    history = AuditlogHistoryField()
    nombre = models.CharField(max_length=50, verbose_name='Marca', unique=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'marca'
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

auditlog.register(Marca)

class Modelo(models.Model):
    history = AuditlogHistoryField()
    nombre = models.CharField(max_length=50, verbose_name='Modelo', unique=True)
    marca = models.ManyToManyField(Marca, verbose_name='Marca', blank=True, through='MarcaModelo')
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'modelo'
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

auditlog.register(Modelo)

class MarcaModelo(models.Model):
    history = AuditlogHistoryField()
    marca = models.ForeignKey(Marca, verbose_name='Marca', on_delete=models.PROTECT)
    modelo = models.ForeignKey(Modelo, verbose_name='Modelo', on_delete=models.PROTECT)
    equipo = models.BooleanField(verbose_name='Equipo', default=False)
    parte = models.BooleanField(verbose_name='Parte', default=False)
    pieza = models.BooleanField(verbose_name='Pieza', default=False)
    insumo = models.BooleanField(verbose_name='Insumo', default=False)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'marca_modelo'
        verbose_name = 'Marca Modelo'
        verbose_name_plural = 'Marcas Modelos'
        ordering = ['marca', 'modelo']

    def __str__(self):
        return self.marca.nombre + ' - ' + self.modelo.nombre

auditlog.register(MarcaModelo)


class Propiedad(models.Model):
    history = AuditlogHistoryField()
    nombre = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'propiedad'
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

auditlog.register(Propiedad)

class CategoriaPieza(models.Model):
    history = AuditlogHistoryField()
    nombre = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    propiedad = models.ManyToManyField(Propiedad, verbose_name='Propiedad', blank=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'categoria_pieza'
        verbose_name = 'Categoría Pieza'
        verbose_name_plural = 'Categorías Piezas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

auditlog.register(CategoriaPieza)

class CategoriaParte(models.Model):
    history = AuditlogHistoryField()
    nombre = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    propiedad = models.ManyToManyField(Propiedad, verbose_name='Propiedad', blank=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'categoria_parte'
        verbose_name = 'Categoría Parte'
        verbose_name_plural = 'Categorías Partes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

auditlog.register(CategoriaParte)

class CategoriaEquipo(models.Model):
    history = AuditlogHistoryField()
    nombre = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    propiedad = models.ManyToManyField(Propiedad, verbose_name='Propiedad', blank=True)
    foto = models.ImageField(upload_to='CategoriaEquipo/', null=True, blank=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'categoria_equipo'
        verbose_name = 'Categoría Equipo'
        verbose_name_plural = 'Categorías Equipos'
        ordering = ['nombre']


    def __str__(self):
        return self.nombre

    def get_foto(self):
        if self.foto:
            return '{}{}'.format(MEDIA_URL, self.foto)
        else:
            return '{}{}'.format(STATIC_URL, 'media/empty.jpg')

auditlog.register(CategoriaEquipo)

class CategoriaInsumo(models.Model):
    history = AuditlogHistoryField()
    nombre = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    propiedad = models.ManyToManyField(Propiedad, verbose_name='Propiedad', blank=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'categoria_insumo'
        verbose_name = 'Categoría Insumo'
        verbose_name_plural = 'Categorías Insumos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


auditlog.register(CategoriaInsumo)


class Insumo(models.Model):
    history = AuditlogHistoryField()
    categoria = models.ForeignKey(CategoriaInsumo, verbose_name='Categoria', on_delete=models.PROTECT)
    nombre = models.CharField(verbose_name='Nombre', max_length=50)
    marca = models.ForeignKey(Marca, verbose_name='Marca', on_delete=models.PROTECT)
    modelo = models.ForeignKey(Modelo, verbose_name='Modelo', on_delete=models.PROTECT)
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    propiedades = models.ManyToManyField(Propiedad, verbose_name='Propiedad', blank=True, through='PropiedadInsumo')
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'insumo'
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return self.nombre

auditlog.register(Insumo)

class PropiedadInsumo(models.Model):
    history = AuditlogHistoryField()
    insumo = models.ForeignKey(Insumo, verbose_name='Insumo', on_delete=models.PROTECT)
    propiedad = models.ForeignKey(Propiedad, verbose_name='Propiedad', on_delete=models.PROTECT)
    valor = models.CharField(verbose_name='Valor', max_length=100, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'propiedad_insumo'
        verbose_name = 'Propiedad Insumo'
        verbose_name_plural = 'Propiedades Insumos'
        unique_together = (('insumo', 'propiedad'),)

    def __str__(self):
        return self.insumo.nombre + ' - ' + self.propiedad.nombre

auditlog.register(PropiedadInsumo)

class Pieza(models.Model):
    history = AuditlogHistoryField()
    categoria = models.ForeignKey(CategoriaPieza, verbose_name='Categoria Pieza', on_delete=models.PROTECT)
    nombre = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    marca = models.ForeignKey(Marca, verbose_name='Marca', on_delete=models.PROTECT)
    modelo = models.ForeignKey(Modelo, verbose_name='Modelo', on_delete=models.PROTECT, null=True, blank=True)
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    propiedades = models.ManyToManyField(Propiedad, verbose_name='Propiedad', blank=True, through='PropiedadPieza')
    insumo = models.ManyToManyField(Insumo, verbose_name='Insumo', blank=True)
    foto = models.ImageField(upload_to='Pieza/', null=True, blank=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'pieza'
        verbose_name = 'Pieza'
        verbose_name_plural = 'Piezas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def get_foto(self):
        if self.foto:
            return '{}{}'.format(MEDIA_URL, self.foto)
        else:
            return '{}{}'.format(STATIC_URL, 'assets/media/empty.jpg')

auditlog.register(Pieza)

class PropiedadPieza(models.Model):
    history = AuditlogHistoryField()
    pieza = models.ForeignKey(Pieza, verbose_name='Pieza', on_delete=models.PROTECT)
    propiedad = models.ForeignKey(Propiedad, verbose_name='Propiedad', on_delete=models.PROTECT)
    valor = models.CharField(verbose_name='Valor', max_length=100, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'propiedad_pieza'
        verbose_name = 'Propiedad Pieza'
        verbose_name_plural = 'Propiedades Piezas'
        # unique_together = (('propiedad', 'pieza'),)

    def __str__(self):
        return self.propiedad.nombre + ' - ' + self.pieza.nombre

auditlog.register(PropiedadPieza)

class Parte(models.Model):
    history = AuditlogHistoryField()
    categoria = models.ForeignKey(CategoriaParte, verbose_name='Categoría', on_delete=models.PROTECT)
    nombre = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    marca = models.ForeignKey(Marca, verbose_name='Marca', on_delete=models.PROTECT)
    modelo = models.ForeignKey(Modelo, verbose_name='Modelo', on_delete=models.PROTECT, null=True, blank=True)
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    propiedades = models.ManyToManyField(Propiedad, verbose_name='Propiedad', blank=True, through='PropiedadParte')
    piezas = models.ManyToManyField(Pieza, verbose_name='Pieza', blank=True)
    insumo = models.ManyToManyField(Insumo, verbose_name='Insumo', blank=True)
    foto = models.ImageField(upload_to='Parte/', null=True, blank=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'parte'
        verbose_name = 'Parte'
        verbose_name_plural = 'Partes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def get_foto(self):
        if self.foto:
            return '{}{}'.format(MEDIA_URL, self.foto)
        else:
            return '{}{}'.format(STATIC_URL, 'assets/media/empty.jpg')

auditlog.register(Parte)

class PropiedadParte(models.Model):
    history = AuditlogHistoryField()
    parte = models.ForeignKey(Parte, verbose_name='Parte', on_delete=models.PROTECT)
    propiedad = models.ForeignKey(Propiedad, verbose_name='Propiedad', on_delete=models.PROTECT)
    valor = models.CharField(verbose_name='Valor', max_length=100, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'propiedad_parte'
        verbose_name = 'Propiedad Parte'
        verbose_name_plural = 'Propiedades Partes'
        # unique_together = (('propiedad', 'parte'),)

    def __str__(self):
        return self.propiedad.nombre + ' - ' + self.parte.nombre

auditlog.register(PropiedadParte)

class Equipo(models.Model):
    ESTADO_CHOICES = (
        ('Activo', 'Activo'),
        ('Reparación', 'Reparación'),
        ('Venta', 'Venta'),
    )
    history = AuditlogHistoryField()
    empresa = models.ForeignKey(Empresa, verbose_name='Empresa', on_delete=models.PROTECT)
    categoria = models.ForeignKey(CategoriaEquipo, verbose_name='Categoria', on_delete=models.PROTECT)
    nombre = models.CharField(verbose_name='Nombre', max_length=50)
    marca = models.ForeignKey(Marca, verbose_name='Marca', on_delete=models.PROTECT)
    modelo = models.ForeignKey(Modelo, verbose_name='Modelo', on_delete=models.PROTECT)
    chapa = models.CharField(verbose_name='Chapa', max_length=7, null=True, blank=True, unique=True)
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    propiedades = models.ManyToManyField(Propiedad, verbose_name='Propiedad', blank=True, through='PropiedadEquipo')
    partes = models.ManyToManyField(Parte, verbose_name='Parte', blank=True)
    estado = models.CharField(max_length=11, choices=ESTADO_CHOICES)
    foto = models.ImageField(upload_to='Equipo/', null=True, blank=True)
    fecha_registro = models.DateField(auto_now_add=True,null=True,blank=True)

    class Meta:
        db_table = 'equipo'
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return self.marca.nombre +' - '+ self.modelo.nombre

    def get_foto(self):
        if self.foto:
            return '{}{}'.format(MEDIA_URL, self.foto)
        else:
            return '{}{}'.format(STATIC_URL, 'media/empty.jpg')

    # def clean(self):
    #     self.chapa = self.chapa.upper()
    #
    #     if not self.chapa[0].isalpha():
    #         raise ValidationError("El primer caracter de la chapa debe ser una letra")
    #
    #     if not self.chapa[1:].isdigit():
    #         raise ValidationError("Los siguientes 6 caracteres deben ser dígitos")

auditlog.register(Equipo)

class PropiedadEquipo(models.Model):
    history = AuditlogHistoryField()
    equipo = models.ForeignKey(Equipo, verbose_name='Equipo', on_delete=models.PROTECT)
    propiedad = models.ForeignKey(Propiedad, verbose_name='Propiedad', on_delete=models.PROTECT)
    valor = models.CharField(verbose_name='Valor', max_length=100, blank=True, null=True)
    fecha_registro = models.DateField(auto_now_add=True, null=True, blank=True)


    class Meta:
        db_table = 'propiedad_equipo'
        verbose_name = 'Propiedad Equipo'
        verbose_name_plural = 'Propiedades Equipos'
        # unique_together = (('equipo', 'propiedad'),)

    def __str__(self):
        return self.equipo.nombre + ' - ' + self.propiedad.nombre



auditlog.register(PropiedadEquipo)