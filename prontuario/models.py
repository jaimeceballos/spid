# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import Group,Permission,User
from django.contrib.admin.models import LogEntry
from django.db.models import signals
import random,datetime,time
from django.core.validators import MinValueValidator,MaxValueValidator
from preventivos.models import *
from preventivos.models import RefCiudades,RefPaises
# Create your models here.

def upload_name(instance, filename):
    return '{}/{}'.format(instance.persona.nro_doc, filename)

class RefOcupacionEspecifica(models.Model):
    descripcion = models.CharField(max_length=50,unique=True)

    def __unicode__(self):
	  return  u'%s' % (self.descripcion)
	  self.descripcion = self.descripcion.upper()

    class Meta:
        db_table = 'ref_ocupacion_especifica'

class FotosPersona(models.Model):
    persona        = models.ForeignKey(Personas,related_name='fotos_persona')
    tipo_foto      = models.CharField(max_length=25)
    foto           = models.ImageField(upload_to=upload_name)
    fecha          = models.DateField(auto_now=True)

    class Meta:
        db_table = 'fotos_persona'

class RefContextura(models.Model):
    descripcion     = models.CharField(max_length = 25, unique=True)

    def __unicode__(self):
	  return  u'%s' % (self.descripcion)
	  self.descripcion = self.descripcion.upper()

    class Meta:
        db_table = 'ref_contextura'

class RefTipoCabello(models.Model):
    descripcion     = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
	  return  u'%s' % (self.descripcion)
	  self.descripcion = self.descripcion.upper()

    class Meta:
        db_table = 'ref_tipo_cabello'

class Identificacion(models.Model):
    persona                     = models.ForeignKey(Personas)
    fecha_identificacion        = models.DateField()
    prontuario_local            = models.CharField(max_length=7)
    dependencia_identificacion  = models.ForeignKey(Dependencias)
    ocupacion_especifica        = models.ForeignKey(RefOcupacionEspecifica)
    altura_metros               = models.IntegerField()
    altura_centimetros          = models.IntegerField()
    contextura                  = models.ForeignKey(RefContextura)
    cutis                       = models.CharField(max_length=25)
    cabello_tipo                = models.ForeignKey(RefTipoCabello)
    cabello_color               = models.CharField(max_length=25)
    es_tenido                   = models.BooleanField(default=False)
    posee_tatuajes              = models.BooleanField(default=False)
    posee_cicatrices            = models.BooleanField(default=False)
    observaciones               = models.CharField(max_length=250)


    class Meta:
        db_table = 'identificacion'


class Prontuario(models.Model):
    nro                 = models.CharField(max_length=7,unique=True)
    persona             = models.OneToOneField(Personas)
    identificaciones    = models.ManyToManyField(Identificacion,null=True)
    fotos               = models.ManyToManyField('FotosPersona',related_name='fotos',blank=True,null=True)
    observaciones       = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table = 'prontuario'


class CivilStatuses(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'civil_statuses'

class Countries(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'countries'

class Nationalities(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'nationalities'

class Provinces(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    country = models.ForeignKey(Countries)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'provinces'

class RecordIdentifications(models.Model):
    id = models.IntegerField(primary_key=True)
    criminal_record_nro = models.BigIntegerField(unique=True)
    dni = models.CharField(max_length=15, blank=True)
    type_dni = models.ForeignKey('TypeDnis', null=True, blank=True)
    name_1 = models.CharField(max_length=50)
    name_2 = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=100)
    nationality = models.ForeignKey(Nationalities)
    profession = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    civil_status = models.ForeignKey(CivilStatuses)
    instructed = models.BooleanField()
    e_mail = models.CharField(max_length=60, blank=True)
    telephone_number = models.CharField(max_length=20, blank=True)
    alias = models.CharField(max_length=20, blank=True)
    place_of_birth = models.CharField(max_length=100)
    province = models.ForeignKey(Provinces, null=True, blank=True)
    address_city = models.CharField(max_length=100, blank=True)
    address_street = models.CharField(max_length=100, blank=True)
    foreign_address = models.CharField(max_length=100, blank=True)
    father_surname = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    father_dni = models.CharField(max_length=15, blank=True)
    mother_surname = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_dni = models.CharField(max_length=15, blank=True)
    reason_for_the_identification = models.CharField(max_length=256)
    jurisdiction_id = models.IntegerField()
    user_create = models.IntegerField()
    user_update = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    sex = models.CharField(max_length=10)
    class Meta:
        db_table = 'record_identifications'

class TypeDnis(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'type_dnis'

class Indice(models.Model):
    id = models.IntegerField(primary_key=True)
    dni = models.CharField(max_length=20L)
    n_c = models.CharField(max_length=100L, blank=True)
    fechan = models.CharField(max_length=100L)
    tipo_p = models.CharField(max_length=25L)
    n_p = models.CharField(max_length=100L)
    estado = models.CharField(max_length=100L)
    fechase = models.CharField(max_length=100L)
    ob = models.CharField(max_length=500L)
    fechac = models.CharField(max_length=20L)
    tipo = models.CharField(max_length=150L, blank=True)
    nombre_archivo = models.CharField(max_length=255L, blank=True)
    identificado = models.CharField(max_length=100L)
    user = models.CharField(max_length=20L)
    class Meta:
        db_table = 'indice'

class RefCiudadesRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    pais_id = models.IntegerField()
    provincia_id = models.IntegerField(null=True, blank=True)
    cp = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'ref_ciudades'

class RefEstadoCivilRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'ref_estado_civil'

class RefGrupoSanguineoRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'ref_grupo_sanguineo'

class RefPaisesRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    nacionalidad = models.CharField(max_length=45L)
    class Meta:
        db_table = 'ref_paises'

class RefProvinciaRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    pais_id = models.IntegerField()
    class Meta:
        db_table = 'ref_provincia'

class RefSexoRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'ref_sexo'

class RefTipoDocumentoRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'ref_tipo_documento'


class SearchHistory(models.Model):
    busqueda        = models.CharField(max_length=300,null=True,blank=True)
    usuario         = models.ForeignKey(User)
    class Meta:
        db_table = 'historial_busqueda'

class SearchResults(models.Model):
    id_busqueda             = models.IntegerField()
    id_spid                 = models.IntegerField(null=True, blank=True)
    id_rrhh                 = models.IntegerField(null=True, blank=True)
    id_acei                 = models.IntegerField(null=True, blank=True)
    id_prontuario           = models.IntegerField(null=True, blank=True)
    es_policia              = models.BooleanField(default=False)
    apellido_nombre         = models.CharField(max_length = 150, null=True, blank=True)
    documento               = models.CharField(max_length = 20, null=True, blank=True)
    ciudad_nacimiento       = models.CharField(max_length = 50, null=True, blank=True)
    ciudad_nacimiento_id    = models.IntegerField(null=True, blank=True)
    ciudad_residencia       = models.CharField(max_length = 50, null=True, blank=True)
    ciudad_residencia_id    = models.IntegerField(null=True, blank=True)
    pais_nacimiento         = models.CharField(max_length = 50, null=True, blank=True)
    pais_nacimiento_id      = models.IntegerField(null=True, blank=True)
    fecha_nacimiento        = models.CharField(max_length=12,null=True, blank=True)
    alias                   = models.CharField(max_length = 50, null=True, blank=True)
    prontuario_acei         = models.CharField(max_length = 30, null=True,blank=True)
    prontuario_spid       = models.CharField(max_length = 30, null=True,blank=True)
    usuario                 = models.ForeignKey(User)
    fecha_hora_creado       = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'resultados_busqueda'


class Verificar(models.Model):
    persona             = models.ForeignKey(Personas)
    identificacion      = models.ForeignKey(Identificacion)
    fecha               = models.DateField()
    usuario             = models.ForeignKey(User)
    verificado          = models.BooleanField(default= False)
    verificado_dia      = models.DateField(null=True)
    verifica_usuario    = models.ForeignKey(User,null=True,blank=True,related_name="usuario_verifica")

    class Meta:
        db_table = 'prontuario_verificar'
