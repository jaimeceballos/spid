 #!/usr/bin/python
#encoding:utf-8
from django.template import Context, Template, RequestContext
from django.http import HttpResponse,HttpResponseRedirect, HttpResponse,Http404, HttpResponseBadRequest
from django.shortcuts import render, render_to_response,get_object_or_404
from preventivos.models import *
from preventivos.forms import *
from django.core import serializers
from django.contrib.auth.models import Group,Permission,User
from django.contrib.admin.models import LogEntry
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.http import HttpResponse,HttpResponseRedirect, HttpResponse,Http404, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, render_to_response,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import auth
from datetime import date,timedelta
import datetime
from time import strptime
from decorators.auth import group_required
from django.contrib.auth.decorators import login_required,permission_required
from django.db import transaction,IntegrityError,connection,connections
from django.core.urlresolvers import reverse
from prontuario.models import *
from prontuario.forms import *

@login_required
@group_required(["prontuario"])
def home(request):

    return render_to_response('./prontuario_home.html',{},context_instance=RequestContext(request))

@login_required
@group_required(["prontuario"])
def nuevo_search(request):
    if request.is_ajax():
        form = SearchForm()
        return render_to_response('./search.html',{'form':form},context_instance=RequestContext(request))
    else:
        return HttpResponseNotFound()

@login_required
@group_required(["prontuario"])
def nuevo(request):
    if request.is_ajax():
        values = {}
        form            = PersonasForm()
        prontuarioForm  = ProntuarioForm()
        values['form'] = form
        values['prontuarioForm'] = prontuarioForm
        return render_to_response('./nuevo_prontuario.html',values,context_instance=RequestContext(request))
    else:
        return HttpResponseNotFound()

def search_persona(request):
    if request.is_ajax():
        form = SearchForm(request.POST)
        parametros = {}
        if form.is_valid():
            parametros['apellido']          = form.cleaned_data['apellido']
            parametros['nombre']            = form.cleaned_data['nombre']
            parametros['fecha_nacimiento']  = form.cleaned_data['fecha_nacimiento']
            parametros['ciudad_nacimiento'] = form.cleaned_data['ciudad_nacimiento_id']
            parametros['pais_nacimiento']   = form.cleaned_data['pais_nacimiento_id']
            parametros['documento']         = form.cleaned_data['documento']
            parametros['alias']             = form.cleaned_data['alias']
            persona_spid = buscar_persona_spid(parametros)
            persona_acei = buscar_persona_acei(parametros)
            persona_indice = buscar_persona_indice(parametros)
            persona_rrhh = buscar_persona_rrhh(parametros)
            if len(persona_indice) == len(Indice.objects.using('prontuario').all()):

                documento = []
                if len(persona_spid) > 0:
                    for registro in persona_spid.values('nro_doc').distinct():
                        documento.append(registro['nro_doc'])
                if len(persona_rrhh) > 0:
                    for registro in persona_rrhh:
                        if registro['documento'] not in documento:
                            documento.append(registro['documento'])
                if len(persona_acei) > 0:
                    for registro in persona_acei.values('dni').distinct():
                        if registro['dni'] not in documento:
                            documento.append(registro['dni'])
                persona_indice = persona_indice.filter(dni__in=documento)


            resultados = SearchResults.objects.filter(
                         id_busqueda=preparar_resultados(
                                         usuario = request.user,
                                         spid = persona_spid if len(persona_spid) > 0 else None,
                                         rrhh = persona_rrhh if len(persona_rrhh) > 0 else None,
                                         acei = persona_acei if len(persona_acei)>0 else None,
                                         prontuario = persona_indice if len(persona_indice)>0 else None))
            
        return render_to_response("./resultados_busqueda.html",{'resultados':resultados},context_instance=RequestContext(request))
    else:
        return HttpResponseNotFound()


def buscar_persona_spid(parametros):
    persona_spid = Personas.objects.all()
    if not parametros['apellido'] == "":
        persona_spid = persona_spid.filter(apellidos__icontains = parametros['apellido'])
    if not parametros['nombre'] == "":
        persona_spid = persona_spid.filter(nombres__icontains = parametros['nombre'])
    if not parametros['fecha_nacimiento'] == "":
        persona_spid = persona_spid.filter(fecha_nac = datetime.datetime.strptime(parametros['fecha_nacimiento'],'%d/%m/%Y'))
    if not parametros['ciudad_nacimiento'] == "":
        persona_spid = persona_spid.filter(Q(ciudad_nac = parametros['ciudad_nacimiento'])|Q(ciudad_res = parametros['ciudad_nacimiento']))
    if not parametros['pais_nacimiento'] == "":
        persona_spid = persona_spid.filter(pais_nac = parametros['pais_nacimiento'])
    if not parametros['documento'] == "":
        persona_spid = persona_spid.filter(nro_doc = parametros['documento'])
    if not parametros['alias'] == "":
        persona_spid = persona_spid.filter(alias__icontains = parametros['alias'])
    return persona_spid

def buscar_persona_acei(parametros):
    persona_acei = RecordIdentifications.objects.using('acei').all()
    if not parametros['apellido'] == "":
        persona_acei = persona_acei.filter(surname__icontains = parametros['apellido'])
    if not parametros['nombre'] == "":
        nombre1 = parametros['nombre']
        nombre2 ="%"
        if len(parametros['nombre'].split(' ')) > 1:
            nombre1 = parametros['nombre'].split(' ')[0]
            nombre2 = parametros['nombre'].split(' ')[len(parametros['nombre'].split(' ')) - 1]
        persona_acei = persona_acei.filter(Q(name_1__icontains = nombre1)|Q(name_2__icontains = nombre2))
    if not parametros['fecha_nacimiento'] == "":
        persona_acei = persona_acei.filter(date_of_birth = datetime.datetime.strptime(parametros['fecha_nacimiento'],'%d/%m/%Y'))
    if not parametros['documento'] == "":
        persona_acei = persona_acei.filter(dni = parametros['documento'])
    return persona_acei

def buscar_persona_indice(parametros):
    filtro_aplicado = False
    persona_indice = Indice.objects.using('prontuario').all()
    n_c = ""
    if not parametros['nombre'] == "":
        n_c = n_c +parametros['nombre']
    if not parametros['apellido'] == "":
        n_c = parametros['apellido'] + " " + n_c
    if not parametros['nombre'] == "" or not parametros['apellido'] == "":
        persona_indice = persona_indice.filter(n_c__icontains = n_c)
        filtro_aplicado = True
    if not parametros['documento'] == "":
        persona_indice = persona_indice.filter(dni = parametros['documento'])
        filtro_aplicado = True
    return persona_indice

def buscar_persona_rrhh(parametros):
    query = "select p.id as id, p.apellido as apellido, p.nombre as nombre, c.descripcion as ciudad_nacimiento,"\
    " c.id as ciudad_nacimiento_id, cd.descripcion as ciudad_residencia, cd.id as ciudad_residencia_id, "\
    "pn.descripcion as pais_nacimiento,pn.id as pais_nacimiento_id, documento as documento, fecha_nacimiento as fecha_nacimiento, ec.descripcion as estado_civil "\
    "FROM personas.personas p "\
    "join referencias.ref_ciudades c on p.ciudad_nacimiento_id = c.id "\
    "join referencias.ref_ciudades cd on p.ciudad_domicilio_id = cd.id "\
    "join referencias.ref_paises pn on p.pais_nacimiento_id = pn.id "\
    "join referencias.ref_estado_civil ec on p.estado_civil_id = ec.id where "
    first_condition = ""
    and_condition = ""
    if not parametros['apellido'] == "":
        if first_condition == "":
            first_condition = "p.apellido like '"+parametros['apellido']+"%%' "
        else:
            and_condition = and_condition + "and p.apellido like '"+parametros['apellido']+"%%' "
    if not parametros['nombre'] == "":
        if first_condition == "":
            first_condition = "p.nombre '"+parametros['nombre']+"%%' "
        else:
            and_condition = and_condition + "and p.nombre like '"+parametros['nombre']+"%%' "
    if not parametros['fecha_nacimiento'] == "":
        if first_condition == "":
            first_condition = "p.fecha_nacimiento like STR_TO_DATE('"+parametros['fecha_nacimiento']+"','%%d/%%m/%%Y') "
        else:
            and_condition = and_condition + "and p.fecha_nacimiento like STR_TO_DATE('"+parametros['fecha_nacimiento']+"','%%d/%%m/%%Y') "
    if not parametros['ciudad_nacimiento'] == "":
        ciudad_nacimiento = RefCiudadesRh.objects.using('referencias').get(descripcion = RefCiudades.objects.get(id = parametros['ciudad_nacimiento']).descripcion).id
        if first_condition == "":
            first_condition = "p.ciudad_nacimiento_id like '"+parametros['ciudad_nacimiento']+"' and ciudad_domicilio_id like '"+parametros['ciudad_nacimiento']+"' "
        else:
            and_condition = and_condition + "and p.ciudad_nacimiento_id like '"+parametros['ciudad_nacimiento']+"' and ciudad_domicilio_id like '"+parametros['ciudad_nacimiento']+"' "
    if not parametros['pais_nacimiento'] == "":
        pais_nacimiento = RefPaisesRh.objects.using('referencias').get(descripcion = RefPaises.objects.get(id = parametros['pais_nacimiento']).descripcion).id
        if first_condition == "":
            first_condition = "p.pais_nacimiento_id like '"+parametros['pais_nacimiento']+"' "
        else:
            and_condition = and_condition + "and p.pais_nacimiento_id like '"+parametros['pais_nacimiento']+"' "
    if not parametros['documento'] == "":
        if first_condition == "":
            first_condition = "p.documento like '"+parametros['documento']+"' "
        else:
            and_condition = and_condition + "and p.documento like '"+parametros['documento']+"' "
    if not first_condition == "":
        query = query +first_condition
        if not and_condition == "":
            query = query +and_condition
    try:
        cursor = connections['rrhh'].cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
		    for row in cursor.fetchall()
        ]
    except Exception as e:
        return []

def preparar_resultados(usuario,spid = None,acei = None,rrhh = None,prontuario = None):
    id_busqueda = obtener_id_busqueda()
    if spid:
        for registro in spid:
            nuevo = SearchResults()
            nuevo.id_busqueda           = id_busqueda
            nuevo.base                  = 'SPID'
            nuevo.id_original           = registro.id
            nuevo.apellido_nombre       = registro.apellidos +" "+ registro.nombres
            nuevo.documento             = registro.nro_doc
            nuevo.ciudad_nacimiento     = registro.ciudad_nac.descripcion
            nuevo.ciudad_nacimiento_id  = registro.ciudad_nac.id
            nuevo.ciudad_residencia     = registro.ciudad_res.descripcion
            nuevo.ciudad_residencia_id  = registro.ciudad_res.id
            nuevo.pais_nacimiento       = registro.pais_nac.descripcion
            nuevo.pais_nacimiento_id    = registro.pais_nac.id
            nuevo.fecha_nacimiento      = registro.fecha_nac
            nuevo.alias                 = registro.alias
            nuevo.prontuario            = ""
            nuevo.usuario               = usuario
            nuevo.save()

    if acei :
        for registro in acei:
            nuevo = SearchResults()
            nuevo.id_busqueda           = id_busqueda
            nuevo.base                  = 'ACEI'
            nuevo.id_original           = registro.id
            nuevo.apellido_nombre       = registro.surname +" "+ registro.name_1 +" "+ registro.name_2
            nuevo.documento             = registro.dni
            nuevo.ciudad_nacimiento     = registro.place_of_birth
            nuevo.ciudad_nacimiento_id  = None
            nuevo.ciudad_residencia     = ""
            nuevo.ciudad_residencia_id  = None
            nuevo.pais_nacimiento       = registro.nationality.name
            nuevo.pais_nacimiento_id    = registro.nationality.id
            nuevo.fecha_nacimiento      = registro.date_of_birth
            nuevo.alias                 = registro.alias
            nuevo.prontuario            = registro.criminal_record_nro
            nuevo.usuario               = usuario
            nuevo.save()
    if rrhh:
        for registro in rrhh:
            nuevo = SearchResults()
            nuevo.id_busqueda           = id_busqueda
            nuevo.base                  = 'RRHH'
            nuevo.id_original           = registro['id']
            nuevo.apellido_nombre       = registro['apellido'] +" "+ registro['nombre']
            nuevo.documento             = registro['documento']
            nuevo.ciudad_nacimiento     = registro['ciudad_nacimiento']
            nuevo.ciudad_nacimiento_id  = registro['ciudad_nacimiento_id']
            nuevo.ciudad_residencia     = registro['ciudad_residencia']
            nuevo.ciudad_residencia_id  = registro['ciudad_residencia_id']
            nuevo.pais_nacimiento       = registro['pais_nacimiento']
            nuevo.pais_nacimiento_id    = registro['pais_nacimiento_id']
            nuevo.fecha_nacimiento      = registro['fecha_nacimiento']
            nuevo.alias                 = ""
            nuevo.prontuario            = ""
            nuevo.usuario               = usuario
            nuevo.save()
    if prontuario:
        for registro in prontuario:
            nuevo = SearchResults()
            nuevo.id_busqueda           = id_busqueda
            nuevo.base                  = 'PRONTUARIO'
            nuevo.id_original           = registro.id
            nuevo.apellido_nombre       = registro.n_c
            nuevo.documento             = registro.dni
            nuevo.ciudad_nacimiento     = ""
            nuevo.ciudad_nacimiento_id  = None
            nuevo.ciudad_residencia     = ""
            nuevo.ciudad_residencia_id  = None
            nuevo.pais_nacimiento       = ""
            nuevo.pais_nacimiento_id    = None
            nuevo.fecha_nacimiento      = ""
            nuevo.alias                 = ""
            nuevo.prontuario            = registro.n_p+" "+registro.tipo_p
            nuevo.usuario               = usuario
            nuevo.save()

    return id_busqueda

def obtener_id_busqueda():
    time = datetime.datetime.now()
    return (time.hour * 3600)+(time.minute * 60)+time.second
