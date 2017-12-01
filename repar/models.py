#encoding:utf-8
from __future__ import unicode_literals
from django.db import models
import datetime
from django.utils import timezone
from django.forms import ModelForm
from django.contrib.auth.models import Group,Permission,User
from django.contrib.admin.models import LogEntry
from django.db.models import signals
import random,datetime,time
from django.core.validators import MinValueValidator,MaxValueValidator

class RefTipoDocumento(models.Model):
    id = models.AutoField(primary_key = True)
    Doc_opciones=(
    ('1','DNI'),
    ('2','LC'),
    ('3','LE'),
    ('4','CI'),
    ('5','PAS'),
    ('6','NO POSEE'),
    ('7','CUIT'),
    ('8','CUIL'),
    )
    descripcion = models.CharField(max_length = 8, choices= Doc_opciones)

    def __unicode__(self):
        return u'%s' % (self.descripcion)

    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_tipodocumento'
        app_label = "repar"


class RefTiposarmas(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100,unique = True)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    def save(self, force_insert=False,force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefTiposarmas, self).save(force_insert,force_update)

    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_tiposarmas'
        app_label = "repar"

class RefTrademark(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100,unique = True)
    codidar = models.IntegerField()

    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    def save(self, force_insert=False,force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefTrademark, self).save(force_insert,force_update)

    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_trademark'
        app_label = "repar"


class RefCalibres(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=15L)
    tipoar = models.ForeignKey('RefTiposarmas',on_delete=models.PROTECT)


    def __unicode__(self):
        return  u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()


    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefCalibres, self).save(force_insert, force_update)

    class Meta:
        unique_together=('descripcion','tipoar',)
        db_table = 'ref_calibres'
        ordering = ["descripcion"]
        app_label = "repar"

class RefModArmas(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField("Modelo :", max_length=15L)
    trademark = models.ForeignKey('RefTrademark',on_delete=models.PROTECT)


    def __unicode__(self):
        return  u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()


    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefModArmas, self).save(force_insert, force_update)

    class Meta:
        unique_together=('descripcion','trademark',)
        db_table = 'ref_modarmas'
        ordering = ["descripcion"]
        app_label = "repar"

class Repardata(models.Model):
    id = models.AutoField(primary_key=True)
    nro = models.IntegerField()
    anio = models.IntegerField()
    fecha_reg = models.DateTimeField(default=0)
    tipoar = models.ForeignKey('RefTiposarmas', on_delete=models.PROTECT)
    calibre = models.ForeignKey('RefCalibres',on_delete=models.PROTECT)
    marca=models.ForeignKey('RefTrademark',on_delete=models.PROTECT,related_name="marca")
    modelo=models.ForeignKey('RefModArmas',on_delete=models.PROTECT,related_name="mode")
    nro_arma = models.CharField(max_length=50)
    apellidos_pro = models.CharField(max_length=100)
    nombres_pro = models.CharField(max_length=100)
    tipodoc = models.ForeignKey('RefTipoDocumento', on_delete=models.PROTECT)
    nrodoc_pro = models.IntegerField(max_length=8)
    domicilio_pro = models.CharField(max_length=200)
    nro_prontuario = models.CharField(max_length=50)
    seccion = models.CharField(max_length=50)
    #id_prontuario = models.ForeingKey("")
    fecha_transf = models.DateTimeField(null=True)
    observaciones = models.CharField(max_length=2000)

    def __unicode__(self):
        return u'%s %s %s ' % (self.apellidos_pro,self.nombres_pro,self.nrodoc_pro)
        self.nrodoc_pro = self.nrodoc_pro
        self.apellidos_pro = self.apellidos_pro.upper()
        self.nombres_pro = self.nombres_pro.upper()
        self.fecha_reg = timezone.now()

    def save(self, force_insert = False, force_update = False):
        super(Repardata, self).save(force_insert, force_update)

    class Meta:
        unique_together=('nro_arma','tipoar','marca','nrodoc_pro')
        ordering = ['nro','anio']
        db_table = 'repardata'
        app_label = "repar"

class Historyrepar(models.Model):
    id = models.AutoField(primary_key=True)
    fechamov = models.DateTimeField(default=0)
    apellidos_pro = models.CharField(max_length=100)
    nombres_pro = models.CharField(max_length=100)
    tipodoc = models.ForeignKey('RefTipoDocumento', on_delete=models.PROTECT)
    nrodoc_pro = models.IntegerField(max_length=8)
    domicilio_pro = models.CharField(max_length=200)
    reparid = models.ForeignKey('Repardata', on_delete=models.PROTECT,related_name='movis')
    observaciones = models.CharField(max_length=2000)
    
    def __unicode__(self):
        return u'%s %s %s %s' % (self.apellidos_pro,self.nombres_pro,self.nrodoc_pro,self.reparid)
        self.nrodoc_pro = self.nrodoc_pro
        self.apellidos_pro = self.apellidos_pro.upper()
        self.nombres_pro = self.nombres_pro.upper()
        self.fechamov = timezone.now()

    def save(self, force_insert = False, force_update = False):
        super(Historyrepar, self).save(force_insert, force_update)

    class Meta:
        ordering = ['-fechamov']
        db_table = 'historyrepar'
        app_label = "repar"

class Indice(models.Model):
    id_documento = models.AutoField(primary_key=True)
    dni = models.CharField(max_length=20)
    n_c = models.CharField(max_length=100)
    fechan =  models.CharField(max_length=100)
    tipo_p =  models.CharField(max_length=25)
    n_p =  models.CharField(max_length=100)
    estado =  models.CharField(max_length=100)
    fechase =  models.CharField(max_length=100)
    ob =  models.CharField(max_length=500)
    fechac =  models.CharField(max_length=20)
    tipo =  models.CharField(max_length=150)
    nombre_archivo =  models.CharField(max_length=255)
    identificado =  models.CharField(max_length=100)
    user =  models.CharField(max_length=20)
    cargado =  models.CharField(max_length=100)

    class Meta:
       managed = False
       db_table = 'indice'
       app_label = "repar"