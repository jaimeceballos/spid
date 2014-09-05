#!/usr/bin/env python
# -*- coding: LATIN1 -*-
from django.utils.dates import MONTHS
import datetime
from datetime import datetime, date
import csv
from django.http import *
from django.contrib import *
from django.contrib.admin import *
from django.middleware import threadlocals 
#from django.contrib.auth import *
from django.conf.urls.defaults import *
from django.template import *
from django.views.generic.simple import *
from django.views.generic import list_detail
from django.views.generic import *
from django.http import Http404
from django.views.generic import *
from django.views.generic.date_based import *
from django.views.generic import date_based
from django.db import models
from django.db.models import *
from django.shortcuts import *
from django.contrib.auth.decorators import *
from django.contrib.sessions.models import Session
from django.db.models import signals
from datetime import *
# Forms
from django import forms as forms
from django.forms import ModelForm
from django.forms.models import *
from django.forms.extras import *
from django.forms.widgets import *
from django.contrib.auth.decorators import *
#Reportes
from cStringIO import StringIO

#Propios del Modelo
from preventivos.models import *
from preventivos.views import *
from preventivos.forms import *

#Render msg
def msg_render(msg):
    raw_t=''
    raw_t=msg
    t=Template(raw_t)
    c=Context({'valor':'x'})
    msgr=t.render(c)
    return msgr
def hoydia():
    ahora=datetime.datetime.now()
    hoy=ahora.date()
    return hoy
def hoyhora():
    ahora=datetime.datetime.now()
    hora=ahora.time()
    a_hora=str(hora)
    a_hora=a_hora[:8]
    return a_hora
#Signals
#Registro de LOG conforme a Procesos 
def registro_post_save(sender, instance, created, **kwargs):
    if created==True:
        accion='ADD'
    else:
        accion='CHG'
    user=threadlocals.get_current_user()
    op=instance
    opa=str(op)
    sender_l=str(sender).split('.')
    #Verificar Errores en SENDER
    try:
        tabla=str(sender_l[3])[:-2]
    except:
        tabla=str(sender)
    log_reg={}
    log_pk={}
    log_pk['valor']=''
    log_pk['pk']=''
    for f in op.__class__._meta.fields:
        valor_nuevo=getattr(op,f.name)
        log_reg[f.name]=str(valor_nuevo)
        
        if f.primary_key==True:
            log_pk['pk']=f.name
            log_pk['valor']=str(valor_nuevo)
        else:
            if f.name=='id':
                log_pk['pk']=f.name
                log_pk['valor']=str(valor_nuevo)
    hoy=hoydia()
    hora=hoyhora()
    log=Registrouser()
    #log.MALG_DMAOP=hoy
    #log.MALG_HORA=hora
    log.user=str(user)
    log.tablas=tabla
    #log.MALG_PK=log_pk['pk']
    #log.MALG_PKVAL=log_pk['valor']
    log.action=str(accion)
    log.fecha=datetime.now()
    log.save()
    return
#Registro de Proceso   
def registro_post_delete(sender, instance, **kwargs):
    user=threadlocals.get_current_user()
    op=instance
    opa=str(op)
    sender_l=str(sender).split('.')
    #Verificar Errores en SENDER
    try:
        tabla=str(sender_l[3])[:-2]
    except:
        tabla=str(sender)
    log_reg={}
    log_pk={}
    log_pk['valor']=''
    log_pk['pk']=''
    for f in op.__class__._meta.fields:
        valor_nuevo=getattr(op,f.name)
        log_reg[f.name]=str(valor_nuevo)
        
        if f.primary_key==True:
            log_pk['pk']=f.name
            log_pk['valor']=str(valor_nuevo)
        else:
            if f.name=='id':
                log_pk['pk']=f.name
                log_pk['valor']=str(valor_nuevo)
    hoy=hoydia()
    hora=hoyhora()
    log=malog()
    log.MALG_DMAOP=hoy
    log.MALG_HORA=hora
    log.MALG_USU=str(user)
    log.MALG_TABLA=tabla
    log.MALG_PK=log_pk['pk']
    log.MALG_PKVAL=log_pk['valor']
    log.MALG_ACCION='DEL'
    log.MALG_VALORES=str(log_reg)
    log.save()
    return
#Signals Definicion - aqui se definen cada una de las tablas que requieren ser logueadas
signals.post_save.connect(registro_post_save, sender=Preventivos)
signals.post_delete.connect(registro_post_delete, sender=PersInvolucradas)
signals.post_save.connect(registro_post_save, sender=User)#Este directamete registra los movimientos de la tabla de Usuarios
