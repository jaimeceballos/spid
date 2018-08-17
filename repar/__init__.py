from datetime import datetime
from django.db import models
from django.contrib import messages
from django.dispatch import receiver
from django.dispatch import Signal
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save,post_delete
#from django.middleware import threadlocals
from repar.models import *
from django.utils.dates import MONTHS
from django.utils import timezone 
from django.utils.encoding import smart_bytes, smart_text
#import datetime
from preventivos.models import *
from datetime import datetime, date
import csv
from django.http import *
from django.contrib import *
from django.contrib.admin import *
from django.http import Http404
from django.shortcuts import *
from django.contrib.auth.decorators import *
from django.contrib.sessions.models import Session
from django.db.models import signals
from datetime import *
# Forms
from django import forms as forms
from django.forms import ModelForm
from django.forms.models import *
#from django.forms.extras import *
from django.forms.widgets import *
from django.contrib.auth.decorators import *
#Reportes
#from cStringIO import StringIO

#Propios del Modelo
from repar.models import *
#from repar.views import *
from repar.forms import *

#Render msg
def msg_render(msg):
    raw_t=''
    raw_t=msg
    t=Template(raw_t)
    c=Context({'valor':'x'})
    msgr=t.render(c)
    return msgr
def hoydia():
    ahora=timezone.now()
    hoy=ahora.date()
    return hoy
def hoyhora():
    ahora=timezone.now()
    hora=ahora.time()
    a_hora=str(hora)
    a_hora=a_hora[:8]
    return a_hora
#Signals
#Registro de LOG conforme a Procesos 
def registro_post_save(sender, instance, created, **kwargs):
    #print created
    if created==True:
        accion='AGREGAR'
    else:
        accion='MODIFICAR'
    
    user=threadlocals.get_current_user()
    op=instance
    opa=str(op)
    sender_l=str(sender).split('.')

    #Verificar Errores en SENDER
    try:
        tabla=str(sender_l[3])[:-2]
    except:
        tabla=str(sender)
    if tabla=='mode':
       tabla="Tabla User"
       user = User.objects.get(username=opa)
       
    log_reg={}
    log_pk={}
    log_pk['valor']=''
    log_pk['pk']=''
    #print op.__class__._meta.fields
    for f in op.__class__._meta.fields:
        if 'username' in f.name:
           valor_nuevo=getattr(op,'username')
        else:
           valor_nuevo=getattr(op,f.name)
        #print valor_nuevo
        #log_reg[f.name]=str(valor_nuevo)
        #valor=str(valor_nuevo)
        #if len(valor)<=48:
        #  ref=valor
        #else:
        #  ref=user
        ref=user.username
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
    log.user=user
    log.tablas=tabla.replace('class','')
    #log.MALG_PK=log_pk['pk']
    log.link='Id Nro: '+str(log_pk['valor'])
    log.session='Usuario : '+str(ref)
    log.action=str(accion)
    log.fecha=timezone.now()
    log.save()
    return
#Registro de Proceso   
def registro_post_delete(sender, instance, **kwargs):
    user=threadlocals.get_current_user()
    op=instance
    opa=str(op)
    sender_l=str(sender).split('.')
    accion="BORRADO"
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
        if 'username' in f.name:
           valor_nuevo=getattr(op,'username')
        else:
           valor_nuevo=getattr(op,f.name)
        #log_reg[f.name]=str(valor_nuevo)
        #valor=str(valor_nuevo)
        #if len(valor)<=48:
        #  ref=valor
        #else:
        #  ref=user
        ref=user.username
        if f.primary_key==True:
            log_pk['pk']=f.name
            log_pk['valor']=str(valor_nuevo)
        else:
            if f.name=='id':
                log_pk['pk']=f.name
                log_pk['valor']=str(valor_nuevo)
    
    
    """hoy=hoydia()
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
    log.save()"""
    hoy=hoydia()
    hora=hoyhora()
    log=Registrouser()
    #log.MALG_DMAOP=hoy
    #log.MALG_HORA=hora
    log.user=user
    log.tablas=tabla.replace('class','')
    #log.MALG_PK=log_pk['pk']
    log.link='Id Nro: '+str(log_pk['valor'])
    log.session='Usuario : '+str(ref)
    log.action=str(accion)
    log.fecha=timezone.now()
    log.save()
    return

#Signals Definicion - aqui se definen cada una de las tablas que requieren ser logueadas
signals.post_save.connect(registro_post_save, sender=Repardata)
signals.post_save.connect(registro_post_save, sender=Historyrepar)
signals.post_save.connect(registro_post_save, sender=RefModArmas)

#Signals postdelete
signals.post_delete.connect(registro_post_delete, sender=Repardata)
signals.post_delete.connect(registro_post_delete, sender=Historyrepar)
signals.post_delete.connect(registro_post_delete, sender=RefModArmas)
#signals.post_delete.connect(registro_post_delete, sender=User)#Este directamete registra los movimientos de la tabla de Usuarios


# Listener Signals
@receiver([user_logged_in, user_logged_out], sender=User)

def log_user_activity(sender, **kwargs):
    signal = kwargs.get('signal', None)
    user = kwargs.get('user', None)
    request = kwargs.get('request', None)
    session_key = request.session.session_key
   
    
    if signal == user_logged_in:
        action = "login"
       
        messages.info(request, "Bienvenido")
    elif signal == user_logged_out:
        action = "logout"
       
        messages.info(request, 'Hasta la proxima')
    if signal == post_save:
        action = "Grabar"
    elif signal == post_delete:
        action = "Eliminar/Borrar"
    
    users=User.objects.get(username=user)
    log_entry = Registrouser(user=users, action=action, tablas='user',
                       link=request.path, session=session_key, fecha=timezone.now())
    log_entry.save()

# Listener Signals
@receiver([post_save, post_delete], sender=Repardata, weak=False)
def send_update(sender, **kwargs):
    #print kwargs.get('user')
    signal = kwargs.get('signal', None)
    user = kwargs.get('instance')
    obj=kwargs['instance']
    ntabla="Repardata id_nro :"+str(obj)
    if signal == post_save:
        action = "Grabar"
    elif signal == post_delete:
        action = "Eliminar/Borrar"
     
    #print user
    #users=User.objects.get(username=user)
    #print users
    #log_entry = Registrouser(user=users, action=action, tabla=ntabla,
                     #  link=request.path,  fecha=datetime.now())
    #log_entry.save()