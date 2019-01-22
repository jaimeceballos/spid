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
from django.utils.translation import ugettext as _
# Create your models here.

def upload_name(instance, filename):
    return '{}/{}'.format(instance.persona.nro_doc, filename)

class RefOcupacionEspecifica(models.Model):
    descripcion = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return  u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    class Meta:
        db_table = 'ref_ocupacion_especifica'

class FotosPersona(models.Model):
    persona        = models.ForeignKey(Personas,related_name='fotos_persona',on_delete=models.DO_NOTHING)
    tipo_foto      = models.CharField(max_length=25)
    foto           = models.ImageField(upload_to=upload_name)
    fecha          = models.DateField(auto_now=True)

    class Meta:
        db_table = 'fotos_persona'

class RefContextura(models.Model):
    descripcion     = models.CharField(max_length = 25, unique=True)

    def __str__(self):
        return  u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    class Meta:
        db_table = 'ref_contextura'

class RefTipoCabello(models.Model):
    descripcion     = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return  u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    class Meta:
        db_table = 'ref_tipo_cabello'

class Identificacion(models.Model):
    persona                     = models.ForeignKey(Personas,on_delete=models.DO_NOTHING)
    fecha_identificacion        = models.DateField()
    prontuario_local            = models.CharField(max_length=7)
    dependencia_identificacion  = models.ForeignKey(Dependencias,on_delete=models.DO_NOTHING)
    ocupacion_especifica        = models.ForeignKey(RefOcupacionEspecifica,on_delete=models.DO_NOTHING)
    altura_metros               = models.IntegerField()
    altura_centimetros          = models.IntegerField()
    contextura                  = models.ForeignKey(RefContextura,on_delete=models.DO_NOTHING)
    cutis                       = models.CharField(max_length=25)
    cabello_tipo                = models.ForeignKey(RefTipoCabello,on_delete=models.DO_NOTHING)
    cabello_color               = models.CharField(max_length=25)
    es_tenido                   = models.BooleanField(default=False)
    posee_tatuajes              = models.BooleanField(default=False)
    posee_cicatrices            = models.BooleanField(default=False)
    observaciones               = models.CharField(max_length=250)


    class Meta:
        db_table = 'identificacion'
        get_latest_by = 'id'


class Prontuario(models.Model):
    nro                 = models.CharField(max_length=7,unique=True)
    persona             = models.OneToOneField(Personas,on_delete=models.DO_NOTHING)
    identificaciones    = models.ManyToManyField(Identificacion)
    fotos               = models.ManyToManyField('FotosPersona',related_name='fotos',blank=True)
    observaciones       = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        db_table = 'prontuario'

        permissions = (
            ('can_change_prontuario_nro', _('Can change prontuario nro')),
        )

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
    country = models.ForeignKey(Countries,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'provinces'

class RecordIdentifications(models.Model):
    id = models.IntegerField(primary_key=True)
    criminal_record_nro = models.BigIntegerField(unique=True)
    dni = models.CharField(max_length=15, blank=True)
    type_dni = models.ForeignKey('TypeDnis', null=True, blank=True,on_delete=models.DO_NOTHING)
    name_1 = models.CharField(max_length=50)
    name_2 = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=100)
    nationality = models.ForeignKey(Nationalities,on_delete=models.DO_NOTHING)
    profession = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    civil_status = models.ForeignKey(CivilStatuses,on_delete=models.DO_NOTHING)
    instructed = models.BooleanField(default=None)
    e_mail = models.CharField(max_length=60, blank=True)
    telephone_number = models.CharField(max_length=20, blank=True)
    alias = models.CharField(max_length=20, blank=True)
    place_of_birth = models.CharField(max_length=100)
    province = models.ForeignKey(Provinces, null=True, blank=True,on_delete=models.DO_NOTHING)
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
    dni = models.CharField(max_length=20)
    n_c = models.CharField(max_length=100, blank=True)
    fechan = models.CharField(max_length=100)
    tipo_p = models.CharField(max_length=25)
    n_p = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    fechase = models.CharField(max_length=100)
    ob = models.CharField(max_length=500)
    fechac = models.CharField(max_length=20)
    tipo = models.CharField(max_length=150, blank=True)
    nombre_archivo = models.CharField(max_length=255, blank=True)
    identificado = models.CharField(max_length=100)
    user = models.CharField(max_length=20)
    class Meta:
        db_table = 'indice'

class RefCiudadesRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    pais_id = models.IntegerField()
    provincia_id = models.IntegerField(null=True, blank=True)
    cp = models.CharField(max_length=45, blank=True)
    class Meta:
        db_table = 'ref_ciudades'

class RefEstadoCivilRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    class Meta:
        db_table = 'ref_estado_civil'

class RefGrupoSanguineoRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    class Meta:
        db_table = 'ref_grupo_sanguineo'

class RefPaisesRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    nacionalidad = models.CharField(max_length=45)
    class Meta:
        db_table = 'ref_paises'

class RefProvinciaRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    pais_id = models.IntegerField()
    class Meta:
        db_table = 'ref_provincia'

class RefSexoRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    class Meta:
        db_table = 'ref_sexo'

class RefTipoDocumentoRh(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45)
    class Meta:
        db_table = 'ref_tipo_documento'


class SearchHistory(models.Model):
    busqueda        = models.CharField(max_length=300,null=True,blank=True)
    usuario         = models.ForeignKey(User,on_delete=models.DO_NOTHING)
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
    usuario                 = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    fecha_hora_creado       = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'resultados_busqueda'


class Verificar(models.Model):
    persona             = models.ForeignKey(Personas,on_delete=models.DO_NOTHING)
    identificacion      = models.ForeignKey(Identificacion,on_delete=models.DO_NOTHING)
    fecha               = models.DateField()
    usuario             = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    verificado          = models.BooleanField(default= False)
    verificado_dia      = models.DateField(null=True)
    verifica_usuario    = models.ForeignKey(User,null=True,blank=True,related_name="usuario_verifica",on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'prontuario_verificar'

class PreventivosPersona(models.Model):
    preventivo_id = models.IntegerField()
    preventivo_nro = models.IntegerField()
    anio = models.IntegerField()
    dependencia_id = models.IntegerField()
    dependencia = models.CharField(max_length=80)
    persona_id = models.IntegerField()
    documento = models.CharField(max_length=50)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=150)
    rol_id = models.IntegerField()
    rol = models.CharField(max_length=150)
    hecho_id = models.IntegerField()
    hecho_descripcion = models.CharField(max_length=2000, blank=True)
    class Meta:
        managed = False
        db_table = 'preventivos_persona'

class ProntuarioLog(models.Model):
    usuario     = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    fecha       = models.DateTimeField(auto_now_add=True)
    accion      = models.CharField(max_length=300)
    entidad     = models.CharField(max_length=100, default="",blank=True, null=True)
    entidad_id  = models.IntegerField(default=None,blank=True, null=True)
    accion_tipo = models.CharField(max_length = 3,default = None, blank = True, null = True)

    class Meta:
        db_table = 'prontuario_log'