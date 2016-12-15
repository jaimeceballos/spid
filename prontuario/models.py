from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import Group,Permission,User
from django.contrib.admin.models import LogEntry
from django.db.models import signals
import random,datetime,time
from django.core.validators import MinValueValidator,MaxValueValidat
from preventivos.models import *
# Create your models here.

def upload_name(instance, filename):
    return '{}/{}/{}'.format(prontuarios, instance.persona.documento, filename)

class RefOcupacionEspecifica(models.Model):
    descripcion = models.CharField(max_length=50)

    class Meta:
        db_table = 'ref_ocupacion_especifica'

class FotosPersona(models.Model):
    persona        = models.ForeignKey(Persona)
    tipo_foto      = models.CharField(max_length=25)
    foto           = models.ImageField(upload_to=upload_name)

    class Meta:
        db_table = 'fotos_persona'


class Identificacion(models.Model):
    persona                     = models.ForeignKey(Personas)
    fecha_identificacion        = models.DateField()
    prontuario_local            = models.CharField(max_length=7)
    dependencia_identificacion  = models.ForeignKey(Dependencias)
    ocupacion_especifica        = models.ForeignKey(RefOcupacionEspecifica)
    altura                      = models.IntegerField()
    contextura                  = models.CharField(max_length=25)
    cutis                       = models.CharField(max_length=25)
    cabello_tipo                = models.CharField(max_length=25)
    cabello_color               = models.CharField(max_length=25)
    es_tenido                   = models.BooleanField()
    posee_tatuajes              = models.BooleanField()
    posee_cicatrices            = models.BooleanField()
    observaciones               = models.CharField(max_length=250)
    fotos                       = models.ManyToManyField('FotosPersona',related_name='fotos',blank=True,null=True)

    class Meta:
        db_table = 'identificacion'


class Prontuario(models.Model):
    nro                 = models.CharField(max_length=7)
    persona             = models.OneToOneField(Personas)
    identificaciones    = models.ManyToManyField(Identificacion)
    
    class Meta:
        db_table = 'prontuario'
