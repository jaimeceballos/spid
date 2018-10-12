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
from django.template.context_processors import csrf
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
from django.urls import reverse
from prontuario.models import *
from prontuario.forms import *
import json

@login_required
@group_required(["prontuario"])
def home(request):
    """ Definicion que redirige al usuario al home de Prontuario"""
    values = {}
    user = request.user
    values['destino'] = "%s / %s" % (user.userprofile.depe,user.userprofile.ureg)
    values['state'] = user.groups.values_list('name', flat=True)
    values['form'] = SearchForm()
    if request.user.userprofile.depe.unidades_regionales.descripcion == "INVESTIGACIONES":
        verificar = Verificar.objects.filter(verificado = False)
        values['verificar'] = verificar
    return render(request,'./prontuario_home.html',values)

@login_required
@group_required(["prontuario"])
def nuevo_search(request):
    """
    Definicion que devuelve solamente el formulario de busqueda previa a la carga
    """
    if request.is_ajax():
        form = SearchForm()
        return render(request,'./search.html',{'form':form})
    else:
        return HttpResponseNotFound()

@login_required
@group_required(["prontuario"])
def nuevo(request):
    """
    Definicion que devuelve el formulario de carga de un nuevo prontuario
    """
    if request.is_ajax():
        values = {}
        form            = PersonasForm()
        prontuarioForm  = ProntuarioForm()
        values['form'] = form
        values['prontuarioForm'] = prontuarioForm
        return render(request,'./nuevo_prontuario.html',values)
    else:
        return HttpResponseNotFound()

@login_required
@group_required(["prontuario"])
def nuevo_procesales(request,prontuario,apellido,nombre,dni):
    """
    Definicion que devuelve el formulario de carga de un nuevo prontuario
    """
    if request.is_ajax():
        values = {}
        form            = PersonasForm()
        prontuarioForm  = ProntuarioForm()
        prontuarioForm.fields['nro'].initial = prontuario
        form.fields['apellidos'].initial = apellido
        form.fields['nombres'].initial = nombre
        form.fields['nro_doc'].initial = dni
        values['form'] = form
        values['prontuarioForm'] = prontuarioForm
        return render(request,'./nuevo_prontuario.html',values)
    else:
        return HttpResponseNotFound()


@login_required
@group_required(["prontuario"])
def search_persona(request):
    """
    Definicion que se encarga de la busqueda de personas en las diferentes bases de datos
    SPID, RRHH, ACEI, COM. PROCESALES.
    Realiza una busqueda de acuerdo a los criterios recibidos pero establece prioridades de
    bases de datos para buscar, inicialmente busca en la base de SPID, si encuentra resultados
    busca en la base de ACEI para tratar de localizar a las personas con su numero de prontuario,
    si no resuelve en ACEI y solo si la busqueda es con numero de dni busca en COM. PROCESALES.
    """
    if request.is_ajax():
        form = SearchForm(request.POST)
        parametros = {}
        if form.is_valid():
            parametros['apellido']          = form.cleaned_data['apellido']
            parametros['nombre']            = form.cleaned_data['nombre']
            parametros['fecha_nacimiento']  = form.cleaned_data['fecha_nacimiento']
            parametros['ciudad_nacimiento'] = form.cleaned_data['ciudad_nacimiento']
            parametros['pais_nacimiento']   = form.cleaned_data['pais_nacimiento']
            parametros['ciudad_nacimiento_id'] = form.cleaned_data['ciudad_nacimiento_id']
            parametros['pais_nacimiento_id']   = form.cleaned_data['pais_nacimiento_id']
            parametros['documento']         = form.cleaned_data['documento']
            parametros['alias']             = form.cleaned_data['alias']
            strParametros = str(parametros)
            try:
                resultados = SearchResults.objects.filter(id_busqueda=SearchHistory.objects.get(busqueda = strParametros).id)
            except Exception as e:
                persona_spid = buscar_persona_spid(parametros)
                persona_rrhh = buscar_persona_rrhh(parametros)
                persona_acei = buscar_persona_acei(parametros)
                persona_indice = buscar_persona_indice(
                                parametros,
                                persona_acei = persona_acei if persona_acei.count()>0 else None,
                                persona_spid = persona_spid if persona_spid.count()>0 else None,
                                persona_rrhh = persona_rrhh if len(persona_rrhh) > 0 else None
                                )
                resultados = SearchResults.objects.filter(
                             id_busqueda=preparar_resultados(
                                             request.user,
                                             strParametros,
                                             spid = persona_spid,
                                             acei = persona_acei,
                                             rrhh = persona_rrhh,
                                             prontuario = persona_indice
                                             )
                                        )
            
        ciudades_nacimiento = resultados.values('ciudad_nacimiento').distinct()
        ciudades_residencia = resultados.values('ciudad_residencia').distinct()
        paises_nacimiento = resultados.values('pais_nacimiento').distinct()
        if resultados.count():
            procesales_result = None
            persona_indice = buscar_persona_indice(parametros)
            if persona_indice and persona_indice.count() > 0:
                persona_indice = persona_indice.exclude(dni__exact='').exclude(n_c__exact='').exclude(n_p__exact='').exclude(n_p__exact='0').values_list('dni','n_c','n_p','id').distinct()
                

        elif persona_indice and persona_indice.count() > 0:
            procesales_result = None
            if persona_indice and persona_indice.count() > 0:
                persona_indice = persona_indice.exclude(dni__exact='').exclude(n_c__exact='').exclude(n_p__exact='').exclude(n_p__exact='0').values_list('dni','n_c','n_p','id').distinct()
                
            
        else:
            return HttpResponseNotFound("No hay Resultados para su busqueda.")
        
        return render(request,"./resultados_busqueda.html",{'resultados':resultados,'ver_procesales':persona_indice.count(),'procesales_result':persona_indice})
    else:
        return HttpResponseNotFound()

def to_html(query):
    html = '<table class="table"><thead><tr><th>DNI</th><th>Nombre</th><th>Prontuario</th></tr></thead><tbody>'
    for row in query:
        fila = '<tr><td>'+row[0]+'</td><td>'+row[1]+'</td><td>'+row[2]+'</td></tr>'
        html = html+fila
    html = html+'</tbody></table>'
    return html


def buscar_persona_spid(parametros):
    """ Esta definicion realiza la busqueda de la persona segun los parametros ingresados
    en la base de datos de personas del sistema SPID"""
    persona_spid = Personas.objects.all()
    if not parametros['apellido'] == "":
        persona_spid = persona_spid.filter(apellidos__icontains = parametros['apellido'])
    if not parametros['nombre'] == "":
        persona_spid = persona_spid.filter(nombres__icontains = parametros['nombre'])
    if not parametros['fecha_nacimiento'] == "":
        persona_spid = persona_spid.filter(fecha_nac = datetime.datetime.strptime(parametros['fecha_nacimiento'],'%d/%m/%Y'))
    if not parametros['ciudad_nacimiento'] == "":
        persona_spid = persona_spid.filter(Q(ciudad_nac = parametros['ciudad_nacimiento_id'])|Q(ciudad_res = parametros['ciudad_nacimiento_id']))
    if not parametros['pais_nacimiento'] == "":
        persona_spid = persona_spid.filter(pais_nac = parametros['pais_nacimiento_id'])
    if not parametros['documento'] == "":
        persona_spid = persona_spid.filter(nro_doc = parametros['documento'])
    if not parametros['alias'] == "":
        persona_spid = persona_spid.filter(alias__icontains = parametros['alias'])
    return persona_spid

def buscar_persona_acei(parametros):
    """ Esta definicion realiza la busqueda de la persona segun los parametros ingresados
    en la base de datos ACEI del sistema Indice"""
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
    if not parametros['pais_nacimiento'] == "":
        nacion = Nationalities.objects.using('acei').get(name__icontains=parametros['pais_nacimiento']).id
        persona_acei = persona_acei.filter(nationality = nacion)
    if not parametros['ciudad_nacimiento'] == '':
        persona_acei = persona_acei.filter(place_of_birth__icontains = parametros['ciudad_nacimiento'])
    if not parametros['alias'] == "":
        persona_acei = persona_acei.filter(alias__icontains = parametros['alias'])
    return persona_acei

def buscar_persona_indice(parametros,persona_spid = None, persona_acei = None, persona_rrhh = None):
    """ Esta definicion realiza la busqueda de la persona segun los parametros ingresados
    en la base de datos chubut del sistema Comunicaciones Procesales"""
    persona_indice = Indice.objects.using('prontuario').all().exclude(dni__exact='',n_c__exact='').exclude(dni__exact='0',n_p__exact='').exclude(n_p__exact='0')
    n_c = ""
    if not parametros['nombre'] == "":
        n_c = n_c +parametros['nombre']
    if not parametros['apellido'] == "":
        n_c = parametros['apellido'] + " " + n_c
    if not parametros['nombre'] == "" or not parametros['apellido'] == "":
        persona_indice = persona_indice.filter(n_c__icontains = n_c)
    if not parametros['documento'] == "":
        persona_indice = persona_indice.filter(dni = parametros['documento'])
    documento = []
    if persona_spid and len(persona_spid) > 0:
        for registro in persona_spid.values('nro_doc').distinct():
            documento.append(registro['nro_doc'])
    if persona_rrhh and len(persona_rrhh) > 0:
        for registro in persona_rrhh:
            if registro['documento'] not in documento:
                documento.append(registro['documento'])
    if persona_acei and len(persona_acei) > 0:
        for registro in persona_acei.values('dni').distinct():
            if registro['dni'] not in documento:
                documento.append(registro['dni'])
    persona_indice = persona_indice.exclude(dni__in=documento)
    
    return persona_indice



def buscar_persona_rrhh(parametros):
    """ Esta definicion realiza la busqueda de la persona segun los parametros ingresados
    en la base de datos de personas del sistema Recursos Humanos"""

    query = "select p.id as id, p.apellido as apellido, p.nombre as nombre,"\
    " case when p.ciudad_nacimiento_id then (select descripcion from referencias.ref_ciudades where id = p.ciudad_nacimiento_id) else 'no registrado' end as ciudad_nacimiento,"\
    " case when p.ciudad_nacimiento_id then (select id from referencias.ref_ciudades where id = p.ciudad_nacimiento_id) else null end as ciudad_nacimiento_id,"\
    " case when p.ciudad_domicilio_id then (select descripcion from referencias.ref_ciudades where id = p.ciudad_domicilio_id) else 'no registrado' end as ciudad_residencia,"\
    " case when p.ciudad_domicilio_id then (select id from referencias.ref_ciudades where id = p.ciudad_domicilio_id) else null end as ciudad_residencia_id,"\
    " case when p.pais_nacimiento_id then (select descripcion from referencias.ref_paises where id = p.pais_nacimiento_id) else 'no registrado' end as pais_nacimiento,"\
    " case when p.pais_nacimiento_id then (select id from referencias.ref_paises where id = p.pais_nacimiento_id) else null end as pais_nacimiento_id,"\
    " p.documento as documento, fecha_nacimiento as fecha_nacimiento,"\
    " case when p.estado_civil_id then (select descripcion from referencias.ref_estado_civil where id = p.estado_civil_id) else 'no registrado' end as estado_civil,"\
    " case when pp.id then '1' else '0' end  as personal "\
    " FROM rrhh.personas p "\
    " left join rrhh.personal_policial pp on p.id = pp.persona_id where "
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
        ciudad_nacimiento = str(RefCiudadesRh.objects.using('referencias').get(descripcion = RefCiudades.objects.get(id = parametros['ciudad_nacimiento_id']).descripcion).id)
        if first_condition == "":
            first_condition = "(p.ciudad_nacimiento_id like '"+ciudad_nacimiento+"' or ciudad_domicilio_id like '"+ciudad_nacimiento+"') "
        else:
            and_condition = and_condition + "and (p.ciudad_nacimiento_id like '"+ciudad_nacimiento+"' or ciudad_domicilio_id like '"+ciudad_nacimiento+"') "
    if not parametros['pais_nacimiento'] == "":
        pais_nacimiento = str(RefPaisesRh.objects.using('referencias').get(descripcion = RefPaises.objects.get(id = parametros['pais_nacimiento_id']).descripcion).id)
        if first_condition == "":
            first_condition = "p.pais_nacimiento_id like '"+pais_nacimiento+"' "
        else:
            and_condition = and_condition + "and p.pais_nacimiento_id like '"+pais_nacimiento+"' "
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

def preparar_resultados(usuario,strParametros,spid = None,acei = None,rrhh = None,prontuario = None):
    """ esta definicion prepara los resultados encontrados en las diferentes bases
    de datos para ser insertados en la tabla de resultados_busqueda, una tabla intermedia
    donde se almacenan temporalmente los resultados de busquedas hechas por el usuario."""

    # obtengo el id de la busqueda realizada
    id_busqueda = obtener_id_busqueda(strParametros,usuario)

    # si se obtuvieron resultados en la base de datos SPID 
    if spid:
        
        # booleano que indica si la persona buscada es policia 
        es_policia = False

        # comienzo a procesar la informacion dentro de los resultados de la base de datos SPID
        for registro in spid:
            # obtengo el numero de documento desde los datos almacenados en la base de datos
            documento = registro.nro_doc
            # preparo tres registros temporales uno para cada uno de las bases de datos restantes
            registro_rrhh = None
            registro_acei = None
            registro_prontuario = None
            # detecto si la persona figura como empleado policial en la base de datos SPID
            try:
                es_policia = True if registro.personal else False
            except Exception as e:
                es_policia = False

            # Realizo una busqueda de la persona actual dentro de cada una de las bases de datos restantes
            # si tengo resultados desde la base de datos de RRHH
            if rrhh:
                # genero un indice que va a apuntar a un elemento de la base de datos de RRHH
                index = None
                # Obtengo cada elemento y su indice del conjunto de resultados de RRHH
                for idx, elemento in enumerate(rrhh):
                    # si alguno de los resultados obtenidos coincide con el nro de documento de la persona que estoy procesando
                    if elemento['documento'] == str(documento):
                        # lo almaceno en el registro temporal
                        registro_rrhh = elemento
                        # guardo su indice dentro del conjunto de resultados
                        index = idx
                        # finalizo la busqueda
                        break
                # si hay un indice guardado
                if index:
                    # quito el registro apuntado del conjunto de resultados de RRHH
                    rrhh.pop(index)
            # si hay resultados desde la base de datos de ACEI
            if acei:
                try:
                    # busco en el conjunto de resultados de ACEI una persona que coincida con la actual
                    registro_acei = acei.get(dni=documento)
                    # si obtuve una persona la quito del conjunto de resultados
                    acei = acei.exclude(id = registro_acei.id)
                except ObjectDoesNotExist:
                    pass
            if prontuario:
                for reg in prontuario:
                    print("dni %s n_c %s n_p %s " % (reg.dni, reg.n_c, reg.n_p)) 
            # creo un nuevo registro de resultado de busqueda
            nuevo = SearchResults()
            # completo cada dato del registro con los obtenidos anteriormente
            nuevo.id_busqueda           = id_busqueda
            # id del registro de la persona en la base de datos SPID
            nuevo.id_spid               = registro.id 
            # id del registro de la persona en la base de datos RRHH si no se encontro queda nulo
            nuevo.id_rrhh               = registro_rrhh['id'] if registro_rrhh else None
            # id del registro de la persona en la base de datos ACEI si no se encontro queda nulo
            nuevo.id_acei               = registro_acei.id if registro_acei else None
            nuevo.id_prontuario         = registro_prontuario.id if registro_prontuario else None
            nuevo.es_policia            = es_policia
            nuevo.apellido_nombre       = registro.apellidos +" "+ registro.nombres
            nuevo.documento             = registro.nro_doc
            nuevo.ciudad_nacimiento     = registro.ciudad_nac.descripcion if registro.ciudad_nac else registro_rrhh['ciudad_nacimiento'] if registro_rrhh and registro_rrhh['ciudad_nacimiento'] else registro_acei.place_of_birth if registro_acei and registro_acei.place_of_birth else ""
            nuevo.ciudad_nacimiento_id  = registro.ciudad_nac.id if registro.ciudad_nac else None
            nuevo.ciudad_residencia     = registro.ciudad_res.descripcion if registro.ciudad_res else registro_rrhh['ciudad_residencia'] if registro_rrhh and registro_rrhh['ciudad_residencia'] else registro_acei.address_city if registro_acei and registro_acei.address_city else ""
            nuevo.ciudad_residencia_id  = registro.ciudad_res.id if registro.ciudad_res else None
            nuevo.pais_nacimiento       = registro.ciudad_nac.pais.descripcion if registro.ciudad_nac else registro_rrhh['pais_nacimiento'] if registro_rrhh and registro_rrhh['pais_nacimiento'] else registro_acei.nationality.name if registro_acei and registro_acei.nationality else None
            nuevo.pais_nacimiento_id    = registro.pais_nac.id if registro.pais_nac else None
            nuevo.fecha_nacimiento      = datetime.datetime.strftime(registro.fecha_nac,'%d/%m/%Y')
            nuevo.alias                 = registro.alias
            try:
                nuevo.prontuario_spid = Prontuario.objects.get(persona = registro).nro
            except ObjectDoesNotExist:
                nuevo.prontuario_acei = registro_acei.criminal_record_nro if registro_acei else  ""
            nuevo.usuario               = usuario
            nuevo.save()

    if rrhh:
        for elemento in rrhh:
            try:
                id = SearchResults.objects.get(id_rrhh=elemento['id'],id_busqueda= id_busqueda)
            except ObjectDoesNotExist:
                es_policia = es_policia = True if elemento['personal'] == 1 else False
                documento = elemento['documento']
                registro_spid = None
                registro_acei = None
                if spid:
                    try:
                        registro_spid = spid.get(nro_doc = documento)
                        spid = spid.exclude(id = registro_spid.id)
                    except ObjectDoesNotExist:
                        pass
                if acei:
                    try:
                        registro_acei = acei.get(dni = documento)
                        acei = acei.exclude(id = registro_acei.id)
                    except ObjectDoesNotExist:
                        pass

                prontuario = registro_acei.criminal_record_nro if registro_acei else  ""

                nuevo = SearchResults()
                nuevo.id_busqueda           = id_busqueda
                nuevo.id_spid               = registro_spid.id if registro_spid else None
                nuevo.id_rrhh               = elemento['id']
                nuevo.id_acei               = registro_acei.id if registro_acei else None
                nuevo.id_prontuario         = None
                nuevo.es_policia            = es_policia
                nuevo.apellido_nombre       = elemento['apellido'] +" "+ elemento['nombre']
                nuevo.documento             = documento
                nuevo.ciudad_nacimiento     = elemento['ciudad_nacimiento'] if elemento['ciudad_nacimiento'] else registro_spid.ciudad_nac.descripcion if registro_spid and registro_spid.ciudad_nac else registro_acei.place_of_birth if registro_acei and registro_acei.place_of_birth else ""
                nuevo.ciudad_nacimiento_id  = elemento['ciudad_nacimiento_id']
                nuevo.ciudad_residencia     = elemento['ciudad_residencia'] if elemento['ciudad_residencia'] else registro_spid.ciudad_res.descripcion if registro_spid and registro_spid.ciudad_res else registro_acei.address_city if registro_acei and registro_acei.address_city else ""
                nuevo.ciudad_residencia_id  = elemento['ciudad_residencia_id']
                nuevo.pais_nacimiento       = elemento['pais_nacimiento'] if elemento['pais_nacimiento'] else registro_spid.ciudad_nac.pais.descripcion if registro_spid and registro_spid.ciudad_nac else registro_acei.nationality if registro_acei and registro_acei.nationality else ""
                nuevo.pais_nacimiento_id    = elemento['pais_nacimiento_id']
                nuevo.fecha_nacimiento      = datetime.datetime.strftime(elemento['fecha_nacimiento'],'%d/%m/%Y') if elemento['fecha_nacimiento'] else None
                nuevo.alias                 = ""
                nuevo.prontuario_acei       = registro_acei.criminal_record_nro if registro_acei else ""
                nuevo.usuario               = usuario
                nuevo.save()

    if acei:
        for registro in acei:
            try:
                id = SearchResults.objects.get(id_acei=registro.id,id_busqueda= id_busqueda)
            except ObjectDoesNotExist:
                es_policia = False
                documento = registro.dni
                registro_spid = None
                registro_rrhh = None
                if spid:
                    try:
                        registro_spid = spid.get(nro_doc = documento)
                        spid = spid.exclude(id = registro_spid.id)
                    except ObjectDoesNotExist:
                        pass
                if rrhh:
                    index = None
                    for idx, elemento in enumerate(rrhh):
                        if elemento['documento'] == str(documento):
                            registro_rrhh = elemento
                            es_policia = True if elemento['personal'] == 1 else False
                            index = idx
                            break
                    if index:
                        rrhh.pop(index)
                nuevo = SearchResults()
                nuevo.id_busqueda           = id_busqueda
                nuevo.id_spid               = registro_spid.id if registro_spid else None
                nuevo.id_rrhh               = registro_rrhh['id'] if registro_rrhh else None
                nuevo.id_acei               = registro.id
                nuevo.id_prontuario         = None
                nuevo.es_policia            = es_policia
                nuevo.apellido_nombre       = registro.surname +" "+ registro.name_1 +" "+ registro.name_2
                nuevo.documento             = registro.dni
                nuevo.ciudad_nacimiento     = registro.place_of_birth if registro.place_of_birth else registro_spid.ciudad_nac if registro_spid and registro_spid.ciudad_nac else registro_rrhh['ciudad_nacimiento'] if registro_rrhh and registro_rrhh['ciudad_nacimiento'] else ""
                nuevo.ciudad_nacimiento_id  = None
                nuevo.ciudad_residencia     = registro.address_city if registro.address_city else registro_spid.ciudad_res if registro_spid and registro_spid.ciudad_res else registro_rrhh['ciudad_residencia'] if registro_rrhh and registro_rrhh['ciudad_nacimiento'] else ""
                nuevo.ciudad_residencia_id  = None
                nuevo.pais_nacimiento       = registro.nationality.name if registro.nationality else registro_spid.ciudad_nacimiento.pais.descripcion if registro_spid and registro_spid.ciudad_nac else registro_rrhh['pais_nacimiento'] if registro_rrhh and registro_rrhh['pais_nacimiento'] else ""
                nuevo.pais_nacimiento_id    = registro.nationality.id
                nuevo.fecha_nacimiento      = datetime.datetime.strftime(registro.date_of_birth,'%d/%m/%Y')
                nuevo.alias                 = registro.alias
                nuevo.prontuario_acei       = registro.criminal_record_nro
                nuevo.usuario               = usuario
                try:
                    nuevo.save()
                except Exception as e:
                    pass



    return id_busqueda

def obtener_id_busqueda(strParametros,usuario):
    """definicion que guarda el la parametrizacion de la busqueda realizada por
    el usuario para poder identificar si se realizo dos veces y buscar los resultados
    directamente en la tabla de resultados_busqueda para agilizar los tiempos de busqueda"""

    historial = SearchHistory()
    historial.busqueda = strParametros
    historial.usuario = usuario
    try:
        historial.save()
    except Exception as e:
        pass

    return historial.id

@login_required
@group_required(["prontuario"])
def search_detalle(request,sistema,id):
    """definicion que obtiene detalles de la persona seleccionada"""

    if request.is_ajax():
        resultado = {}
        if sistema == "SPID":
            persona = Personas.objects.get(id = id)
            padres = persona.padre.all()
            resultado['nombre']             = persona.apellidos +", "+ persona.nombres
            resultado['sexo']               = persona.sexo_id.descripcion.lower()
            resultado['dni']                = persona.nro_doc
            resultado['lugar_nacimiento']   = persona.ciudad_nac.descripcion+" - "+persona.ciudad_nac.pais.descripcion if persona.ciudad_nac else ""
            resultado['lugar_residencia']   = persona.ciudad_res.descripcion+" - "+persona.ciudad_res.pais.descripcion if persona.ciudad_res else ""
            resultado['ocupacion']          = persona.ocupacion.descripcion
            resultado['fecha_nacimiento']   = persona.fecha_nac
            resultado['estado_civil']       = persona.estado_civil.descripcion
            resultado['alias']              = persona.alias if not persona.alias == "" and not persona.alias == None else "No registra"
            try:
                resultado['padre']              = padres[0].padre_apellidos+", "+padres[0].padre_nombres
                resultado['madre']              = padres[0].madre_apellidos+", "+padres[0].madre_nombres
            except IndexError:
                resultado['padre']              = "No registrado"
                resultado['madre']              = "No registrado"
        if sistema == "INDICE":
            persona     = RecordIdentifications.objects.using('acei').get(id = id)
            resultado['nombre']             = persona.surname +", "+ persona.name_1+" "+persona.name_2
            resultado['sexo']               = persona.sex
            resultado['dni']                = persona.dni
            resultado['lugar_nacimiento']   = persona.place_of_birth
            resultado['lugar_residencia']   = persona.address_city
            resultado['ocupacion']          = persona.profession
            resultado['fecha_nacimiento']   = persona.date_of_birth
            resultado['estado_civil']       = persona.civil_status.name
            resultado['alias']              = persona.alias if not persona.alias == "" and not persona.alias == None else "No registra"
            resultado['padre']              = persona.father_surname+", "+persona.father_name if not persona.father_surname == "" and not persona.father_surname == None else "No registrado"
            resultado['madre']             = persona.mother_surname+", "+persona.mother_name if not persona.mother_surname == "" and not persona.mother_surname == None else "No Registrado"
        if sistema == "RRHH":
            persona =  buscar_detalle_persona_rrhh(id)[0]
            resultado['nombre']             = persona['nombre']
            resultado['sexo']               = persona['sexo'].lower()
            resultado['dni']                = persona['documento']
            resultado['lugar_nacimiento']   = persona['lugar_nacimiento'] if not persona['lugar_nacimiento'] == None else ""
            resultado['lugar_residencia']   = persona['lugar_residencia'] if not persona['lugar_residencia'] == None else ""
            resultado['ocupacion']          = "No registrado"
            resultado['fecha_nacimiento']   = persona['fecha_nacimiento']
            resultado['estado_civil']       = persona['estado_civil']
            resultado['alias']              = "No registrado"
            resultado['padre']              = persona['padre'] if not persona['padre'] == None else "No registrado"
            resultado['madre']              = persona['madre'] if not persona['madre'] == None else "No registrado"
        return render(request,'./detalle_persona.html',{'resultado':resultado})
    else:
        return HttpResponseBadRequest()


def buscar_detalle_persona_rrhh(id):
    """definicion que realiza la busqueda de detalles de la persona en el sistema
    de recursos humanos"""

    query = "select CONCAT(p.apellido,', ',p.nombre) as nombre, "\
    "case when p.sexo_id then (select descripcion from referencias.ref_sexo where p.sexo_id = id) else 'Sin descripcion' end as sexo, "\
    "case when p.ciudad_nacimiento_id then (select CONCAT(cn.descripcion,', ',pn.descripcion) from referencias.ref_ciudades cn join referencias.ref_paises pn on cn.pais_id = pn.id where cn.id = p.ciudad_nacimiento_id) else 'No registrado' end as lugar_nacimiento, "\
    "p.fecha_nacimiento, p.documento, "\
    "case when p.estado_civil_id then ( select descripcion from referencias.ref_estado_civil where p.estado_civil_id = id) else 'No registrado' end as estado_civil, "\
    "case when p.ciudad_domicilio_id then (select CONCAT(cr.descripcion,', ',pr.descripcion) from referencias.ref_ciudades cr join referencias.ref_paises pr on cr.pais_id = pr.id where cr.id = p.ciudad_domicilio_id) else 'No registrado' end as lugar_residencia, "\
    "(select CONCAT(padre.apellido,', ',padre.nombre) from rrhh.grupo_familiar gf join rrhh.personas padre on gf.familiar_id = padre.id "\
    "where gf.persona_id = p.id and gf.tipo_parentezco_id = 3 and padre.sexo_id = 2) as padre, "\
    "(select CONCAT(madre.apellido,', ',madre.nombre) from rrhh.grupo_familiar gf2 join rrhh.personas madre on gf2.familiar_id = madre.id "\
    "where gf2.persona_id = p.id and gf2.tipo_parentezco_id = 3 and madre.sexo_id = 1) as madre "\
    "from rrhh.personas p where p.id = %s" % id


    """query = "select CONCAT(p.apellido,', ',p.nombre) as nombre, s.descripcion as sexo, "\
    "CONCAT(cn.descripcion,', ',pn.descripcion) as lugar_nacimiento, p.fecha_nacimiento, "\
    "p.documento, ec.descripcion as estado_civil, CONCAT(cr.descripcion,', ',pr.descripcion) as lugar_residencia, "\
    "(select CONCAT(padre.apellido,', ',padre.nombre) from rrhh.grupo_familiar gf join rrhh.personas padre on gf.familiar_id = padre.id "\
    "where gf.persona_id = p.id and gf.tipo_parentezco_id = 3 and padre.sexo_id = 2) as padre, "\
    "(select CONCAT(madre.apellido,', ',madre.nombre) from rrhh.grupo_familiar gf2 join rrhh.personas madre on gf2.familiar_id = madre.id "\
    "where gf2.persona_id = p.id and gf2.tipo_parentezco_id = 3 and madre.sexo_id = 1) as madre "\
    "from rrhh.personas p join referencias.ref_sexo s on p.sexo_id = s.id left join referencias.ref_ciudades cn on p.ciudad_nacimiento_id = cn.id "\
    "left join referencias.ref_paises pn on p.pais_nacimiento_id = pn.id join referencias.ref_estado_civil ec on p.estado_civil_id = ec.id "\
    "left join referencias.ref_ciudades cr on p.ciudad_domicilio_id = cr.id left join referencias.ref_paises pr on cr.pais_id = pr.id "\
    "where p.id = %s" % id"""
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

@login_required
@group_required(["prontuario"])
def search_procesales(request,id,dni):
    """Esta definicion busca una persona por dni en la base de datos del sistema
    de comunicaciones Procesales"""
    if request.is_ajax():
        resultado = Indice.objects.using('prontuario').filter(dni = dni)
        if resultado.count() > 0:
            return render(request,"./listado_procesales.html",{'resultado':resultado,'id':id})
        else:
            return HttpResponseNotFound("No se encontraron resultados")
    else:
        return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def utilizar_prontuario(request,id,prontuario):
    """esta definicion obtiene el numero de prontuario y lo utiliza temporalmente
    en la persona encontrada en la tabla de resultados_busqueda"""
    if request.is_ajax():
        detalle = SearchResults.objects.get(id = id)
        detalle.prontuario_spid = prontuario
        try:
            detalle.save()
            return HttpResponse("ok")
        except Exception as e:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def nuevo_pais(request,tipo):
    """definicion que sirve para crear un nuevo pais"""

    if request.is_ajax():
        if request.method == 'POST':
            form = PaisesForm(request.POST)
            if form.is_valid():
                pais = RefPaises()
                pais.descripcion = form.cleaned_data['descripcion'].upper()
                try:
                    pais.save()
                except Exception as e:
                    return HttpResponseBadRequest()
                paises = RefPaises.objects.all()
                data = serializers.serialize("json", paises)
                return HttpResponse(data, content_type='application/json')
        else:
            form = PaisesForm()
            return render(request,"./nuevo_pais.html",{'form':form,'tipo':tipo})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def nueva_ciudad(request,tipo,pais):
    """definicion que sirve para generar una nueva ciudad"""

    if request.is_ajax:
        pais = RefPaises.objects.get(id = pais)
        if request.method == "POST":
            form = CiudadesForm(request.POST)
            if form.is_valid():
                ciudad = RefCiudades()
                ciudad.pais = form.cleaned_data['pais']
                ciudad.descripcion = form.cleaned_data['descripcion']
                try:
                    ciudad.save()
                except Exception as e:
                    return HttpResponseBadRequest()
                ciudades = RefCiudades.objects.filter(pais=pais)
                data = serializers.serialize("json",ciudades)
                return HttpResponse(data,content_type="application/json")
        else:
            form = CiudadesForm(initial={'pais':pais})
            return render(request,"./nuevo_ciudad.html",{'form':form,'tipo':tipo,'pais':pais})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def verificar_prontuario(request,n_p):
    """definicion que verifica si el numero de prontuario ingresado existe en la
    base de datos de comunicaciones procesales"""

    if request.is_ajax():
        prontuarios = Indice.objects.using('prontuario').filter(n_p = n_p)
        if prontuarios.count() > 0:
            return render(request,"./listado_procesales.html",{'resultado':prontuarios,'id':0})
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def nuevo_save(request):
    """ definicion que guarda un nuevo prontuario y habilita la cracion de una
    nueva identificacion"""

    if request.is_ajax():
        if request.method == 'POST':
            print("ingresa")
            validacion = False
            id = request.POST['persona_id']
            if id == "":
                persona = Personas()
                form = PersonasForm(request.POST)
            else:
                persona = Personas.objects.get(id=id)
                form = PersonasForm(request.POST,instance=persona)
            prontuarioForm = ProntuarioForm(request.POST)
            if request.user.userprofile.depe.unidades_regionales.descripcion == "INVESTIGACIONES":
                validacion = form.is_valid() and prontuarioForm.is_valid()
            else:
                validacion = form.is_valid()
                
            if validacion:
                prontuario = Prontuario()
                persona.apellidos       = form.cleaned_data['apellidos']
                persona.nombres         = form.cleaned_data['nombres']
                persona.fecha_nac       = form.cleaned_data['fecha_nac']
                persona.tipo_doc        = form.cleaned_data['tipo_doc']
                persona.nro_doc         = form.cleaned_data['nro_doc']
                persona.ciudad_nac      = form.cleaned_data['ciudad_nac']
                persona.pais_nac        = form.cleaned_data['pais_nac']
                persona.ciudad_res      = form.cleaned_data['ciudad_res']
                persona.sexo_id         = form.cleaned_data['sexo_id']
                persona.ocupacion       = form.cleaned_data['ocupacion']
                persona.estado_civil    = form.cleaned_data['estado_civil']
                try:
                    persona.save()
                    if request.user.userprofile.depe.unidades_regionales.descripcion == "INVESTIGACIONES":
                        prontuario.nro = prontuarioForm.cleaned_data['nro']
                        prontuario.persona = persona
                        prontuario.observaciones = prontuarioForm.cleaned_data['observaciones']
                        if not prontuario.observaciones =='':
                            prontuario.observaciones = prontuario.observaciones.upper()
                        try:
                            print("------ SAVE DE PRONTUARIO ------")
                            prontuario.save()
                        except Exception as e:
                            print("excepcion save prontuario")
                            print(e)
                    form = IdentificacionForm()
                    existe = False
                    return HttpResponseRedirect('/prontuario/ver_prontuario/%s/' % persona.id) #render(request,"./nueva_identificacion.html",{'persona':persona,'prontuario':prontuario,'form':form,'existe':existe})
                except Exception as e:
                    print("excepcion save")
                    print(e)
                    return HttpResponseBadRequest()

    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def identificacion(request,id):
    if request.is_ajax:
        persona = Personas.objects.get(id=id)
        #prontuario = Prontuario.objects.get(persona=persona)
        form = IdentificacionForm()
        existe = True
        return render(request,"./nueva_identificacion.html",{'persona':persona,'form':form,'existe':existe})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def resumen_persona(request,id):
    if request.is_ajax:
        persona = Personas.objects.get(id=id)
        #prontuario = Prontuario.objects.get(persona=persona)
        return HttpResponseRedirect('/prontuario/ver_prontuario/%s/' % persona.id)
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def nuevo_existe(request,id_detalle):
    """definicion que genera un nuevo prontuario a partir de una persona existente
    en la base de datos de personas del sistema SPID, y habilita la carga de una
    nueva identificacion"""

    if request.is_ajax:
        detalle = SearchResults.objects.get(id = id_detalle)
        prontuario_nro = detalle.prontuario_acei if detalle.prontuario_acei else detalle.prontuario_spid if detalle.prontuario_spid else ""
        if detalle.id_spid:
            persona = Personas.objects.get(id = detalle.id_spid)
            if not prontuario_nro == "" and request.user.userprofile.depe.unidades_regionales.descripcion == 'INVESTIGACIONES':
                prontuario,create = Prontuario.objects.get_or_create(
                                        nro = prontuario_nro,
                                        persona = persona
                                    )
                form = IdentificacionForm()
                return render(request,"./nueva_identificacion.html",{'persona':persona,'prontuario':prontuario,'form':form,'existe':True})
            form = PersonasForm(
                                initial={
                                    'nombres':persona.nombres,
                                    'apellidos' : persona.apellidos,
                                    'fecha_nac' : persona.fecha_nac,
                                    'tipo_doc' : persona.tipo_doc,
                                    'nro_doc' : persona.nro_doc,
                                    'pais_nac' : persona.pais_nac,
                                    'ciudad_nac' : persona.ciudad_nac,
                                    'sexo_id' : persona.sexo_id,
                                    'estado_civil' : persona.estado_civil,
                                    'ciudad_res' : persona.ciudad_res,
                                    'pais_res' : persona.ciudad_res.pais,
                                    'ocupacion' : persona.ocupacion

                                    }
                                )
            if request.user.userprofile.depe.unidades_regionales.descripcion == 'INVESTIGACIONES':
                prontuarioForm  = ProntuarioForm(initial={'nro':prontuario_nro})
            else:
                prontuarioForm = ProntuarioForm()
            return render(request,'./nuevo_prontuario.html',{'form':form,'prontuarioForm':prontuarioForm,'persona':persona.id})
        else:
            prontuarioForm = ProntuarioForm()
            if not prontuario_nro == "" and request.user.userprofile.depe.unidades_regionales.descripcion == 'INVESTIGACIONES':
                prontuarioForm = ProntuarioForm(initial={'nro':prontuario_nro})
            apellido = detalle.apellido_nombre.split(" ")[0]
            nombres = detalle.apellido_nombre.split(" ")[1] if len(detalle.apellido_nombre.split(" ")) == 2 else detalle.apellido_nombre.split(" ")[1]+" "+detalle.apellido_nombre.split(" ")[2]
            form = PersonasForm(
                                initial={
                                    'nombres':nombres,
                                    'apellidos' : apellido,
                                    'fecha_nac' : detalle.fecha_nacimiento,
                                    'nro_doc'   : detalle.documento,

                                    }
                                )
            return render(request,'./nuevo_prontuario.html',{'form':form,'prontuarioForm':prontuarioForm})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def identificacion_save(request):
    """"Definicion para guardar una nueva identificacion de una persona"""
    if request.is_ajax():
        if request.method == "POST":
            form = IdentificacionForm(request.POST)
            if form.is_valid():
                identificacion = Identificacion()

                identificacion.persona                      = Personas.objects.get(id = request.POST['persona'])
                identificacion.fecha_identificacion         = datetime.datetime.now()
                identificacion.prontuario_local             = form.cleaned_data['prontuario_local'] if not request.user.userprofile.depe.unidades_regionales.descripcion == "INVESTIGACIONES" else request.POST['prontuario']
                identificacion.dependencia_identificacion   = request.user.userprofile.depe
                identificacion.ocupacion_especifica         = form.cleaned_data['ocupacion_especifica']
                identificacion.altura_metros                = form.cleaned_data['altura_metros']
                identificacion.altura_centimetros           = form.cleaned_data['altura_centimetros']
                identificacion.contextura                   = form.cleaned_data['contextura']
                identificacion.cutis                        = form.cleaned_data['cutis']
                identificacion.cabello_tipo                 = form.cleaned_data['cabello_tipo']
                identificacion.cabello_color                = form.cleaned_data['cabello_color']
                identificacion.es_tenido                    = form.cleaned_data['es_tenido']
                identificacion.posee_tatuajes               = form.cleaned_data['posee_tatuajes']
                identificacion.posee_cicatrices             = form.cleaned_data['posee_cicatrices']
                identificacion.observaciones                = form.cleaned_data['observaciones']
                try:
                    identificacion.save()
                    if request.user.userprofile.depe.unidades_regionales.descripcion == "INVESTIGACIONES":
                        prontuario = Prontuario.objects.get(id=request.POST['prontuario'])
                        prontuario.identificaciones.add(identificacion)
                    else:
                        verificar = Verificar()
                        verificar.persona = identificacion.persona
                        verificar.identificacion = identificacion
                        verificar.usuario = request.user
                        verificar.fecha = datetime.datetime.now()
                        verificar.save()
                        prontuario = Prontuario()
                except Exception as e:
                    return HttpResponseBadRequest()
                return HttpResponseRedirect("/prontuario/resumen_persona/%s/" % identificacion.persona.id) #render(request,"./nueva_identificacion.html",{'persona':identificacion.persona,'prontuario':prontuario,'identificacion':identificacion,'existe':True})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def verificar(request):
    if request.is_ajax():
        verificar = Verificar.objects.filter(verificado = False)
        return render(request,"./verificar.html",{'verificar':verificar})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def datos_verificar(request,id):
    if request.is_ajax():
        verificar = Verificar.objects.get(id=id)
        persona = Personas.objects.get(id = verificar.persona.id)
        identificacion = Identificacion.objects.get(id=verificar.identificacion.id)
        padres = persona.padre.all()
        domicilios = persona.persodom.all().order_by('-id')
        fotos = persona.fotos_persona.filter(tipo_foto = '1') | persona.fotos_persona.filter(tipo_foto='4')

        values = {
            'verificar':verificar,
            'identificacion':identificacion,
            'persona':persona,
            'padres':padres[0] if padres.count()>0 else None,
            'domicilios':domicilios[0] if domicilios.count() > 0 else None,
            'fotos':fotos,
            'form':ProntuarioForm(),
        }
        return render(request,"./detalle_verificar.html",values)
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def cargar_padres(request,id):
    if request.is_ajax():
        if request.method == 'POST':
            form = PadresForm(request.POST)
            persona = Personas.objects.get(id=id)
            if form.is_valid():
                padres = Padres()
                try:
                    padres = Padres.objects.get(persona = persona)
                except Exception as e:
                    pass
                padres.padre_nombres = form.cleaned_data['padre_nombres']
                padres.padre_apellidos = form.cleaned_data['padre_apellidos']
                padres.madre_nombres = form.cleaned_data['madre_nombres']
                padres.madre_apellidos = form.cleaned_data['madre_apellidos']
                padres.persona = persona
                try:
                    padres.save()
                except Exception as e:
                    return HttpResponseBadRequest()
                return HttpResponse("ok")
        else:
            persona = Personas.objects.get(id=id)
            form = ""
            try:
                padres = Padres.objects.get(persona=persona)
                form = PadresForm(instance = padres)
            except ObjectDoesNotExist:
                form = PadresForm()
            return render(request,"./padres.html",{'form':form,'id':id,'persona':persona})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def cargar_domicilios(request,id):
    if request.is_ajax():
        persona = Personas.objects.get(id=id)
        if request.method =="POST":
            form = DomicilioProntuarioForm(request.POST)
            domicilio_vigente = Domicilios.objects.filter(personas=persona,fecha_hasta__isnull= True)
            if domicilio_vigente.count() > 0:
                for domicilio in domicilio_vigente:
                    domicilio.fecha_hasta = domicilio.fecha_actualizacion = datetime.datetime.now()
                    domicilio.save()
            if form.is_valid():
                domicilio = Domicilios()
                domicilio.ref_ciudades                                  = form.cleaned_data['ref_ciudades']
                domicilio.barrio_codigo                                 = form.cleaned_data['barrio_codigo']
                domicilio.calle                                         = form.cleaned_data['calle']
                domicilio.altura                                        = form.cleaned_data['altura']
                domicilio.entre                                         = form.cleaned_data['entre']
                domicilio.fecha_desde = domicilio.fecha_actualizacion   = datetime.datetime.now()
                domicilio.tipos_domicilio                               = form.cleaned_data['tipos_domicilio']
                domicilio.ref_zona                                      = form.cleaned_data['ref_zona']
                domicilio.departamento                                  = form.cleaned_data['departamento']
                domicilio.piso                                          = form.cleaned_data['piso']
                domicilio.lote                                          = form.cleaned_data['lote']
                domicilio.sector                                        = form.cleaned_data['sector']
                domicilio.manzana                                       = form.cleaned_data['manzana']
                domicilio.calle2                                        = form.cleaned_data['calle2']
                domicilio.personas                                      = persona
                try:
                    domicilio.save()
                    return HttpResponseRedirect("/prontuario/resumen_persona/%s/" % persona.id)
                except Exception as e:
                    return HttpResponseBadRequest()
        domicilios = Domicilios.objects.filter(personas=persona)
        paises = RefPaises.objects.all()
        form = DomicilioProntuarioForm()
        return render(request,"./domicilios.html",{'domicilios':domicilios,'form':form,'id':id,'paises':paises})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def cargar_fotos(request,id):
    print ("VIENE")
    if request.is_ajax():
        persona = Personas.objects.get(id=id)
        if request.method=="POST":
            form = FotosPersonaForm(request.POST, request.FILES)
            if form.is_valid():
                foto = FotosPersona()
                foto.persona = persona
                foto.tipo_foto = form.cleaned_data['tipo_foto']
                foto.foto = form.cleaned_data['foto']
                try:
                    foto.save()
                    try:
                        prontuario = Prontuario.objects.get(persona = persona)
                        prontuario.fotos.add(foto)
                    except Exception as e:
                        print (e)
                except Exception as e:
                    return HttpResponseBadRequest()
        fotos = FotosPersona.objects.filter(persona = persona)
        print (fotos)
        form = FotosPersonaForm()
        return render(request,"./fotos.html",{'fotos':fotos,'form':form,'id':id})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def verificar_existe(request,id):
    if request.is_ajax():
        persona = Personas.objects.get(id = id)
        documento = persona.nro_doc
        prontuario = ""
        try:
            prontuario = RecordIdentifications.objects.using('acei').get(dni = documento).criminal_record_nro
        except Exception as e:
            try:
                prontuario = Indice.objects.using('prontuario').get(dni = documento).n_p
            except Exception as e:
                return HttpResponseNotFound()

        return HttpResponse(prontuario)
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def vincular(request,id):
    if request.is_ajax():
        identificacion = Identificacion.objects.get(id = id)                        # obtengo la identificacion a vincular con un prontuario
        if request.method == 'POST':
            form = None
            prontuario=None
            try:
                prontuario = Prontuario.objects.get(persona = identificacion.persona) # trato de obtener un prontuario que coincida con la persona
            except ObjectDoesNotExist:                                                # si la persona no esta prontuariada
                form = ProntuarioForm(request.POST)                                   # obtengo los datos recibidos por POST

            if form and form.is_valid():                                              # si se inicializo un form y es valido
                prontuario = Prontuario()                                             # creo un nuevo prontuario
                prontuario.nro = form.cleaned_data['nro']                             # asigno el numero recibido del usuario
                prontuario.persona = identificacion.persona                           # asigno la persona identificada al prontuario
            try:
                if not prontuario.id:                                                 # si la instancia de prontuario es nueva y no existia en la BD
                    prontuario.save()                                                 # guardo la nueva instancia en la BD
                prontuario.identificaciones.add(identificacion)                       # asigno la identificacion al prontuario
                fotos = FotosPersona.objects.filter(persona = identificacion.persona) # busco si existen fotos asociadas a la persona
                if fotos.count() > 0:                                                   # en el caso que existan
                    for foto in fotos:
                        try:
                            prontuario.fotos.add(foto)                                    # las agrego al prontuario
                        except Exception as e:
                            print (e)

                verificar = Verificar.objects.get(identificacion = identificacion)
                verificar.verificado = True                                           # marco la identificacion como verificada
                verificar.verificado_dia = datetime.datetime.now()
                verificar.verifica_usuario = request.user
                verificar.save()
                return HttpResponse("ok")                                             # devuelvo "ok" para notificar que la operacion termino correctamente
            except Exception as e:
                print ("Excepcion en vincular %s" % e)
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def identificaciones_anteriores(request,id):
    if request.is_ajax():
        identificaciones = Identificacion.objects.filter(persona=id).order_by("-id")
        if identificaciones.count() > 0:
            data = serializers.serialize("json", identificaciones)
            return HttpResponse(data, content_type='application/json')
        return HttpResponseNotFound()
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def obtener_identificacion(request,id):
    if request.is_ajax():
        identificacion = Identificacion.objects.get(id=id)
        return render(request,"./identificacion.html",{'identificacion':identificacion})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def obtener_fotos(request,id):
    if request.is_ajax():
        fotos = FotosPersona.objects.filter(persona = id)
        return render(request,"./galeria.html",{"fotos":fotos})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def ver_identificacion(request,id):
    if request.is_ajax:
        identificacion = Identificacion.objects.get(id=id)
        foto = FotosPersona.objects.filter(persona = identificacion.persona,tipo_foto = "1")[0] if FotosPersona.objects.filter(persona = identificacion.persona,tipo_foto = "1").count() > 0 else None
        return render(request,"./ver_identificacion.html",{'identificacion':identificacion,'foto':foto})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def buscar(request):
    if request.is_ajax:
        form = BuscarForm()
        return render(request,"./busqueda.html",{'form':form})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def busqueda(request):
    if request.user.is_authenticated:
        if request.is_ajax:
            if request.method == "POST":
                form = BuscarForm(request.POST)
                if form.is_valid():
                    apellido = form.cleaned_data['apellido']
                    nombre = form.cleaned_data['nombre']
                    documento = form.cleaned_data['documento']
                    lugar_nacimiento = form.cleaned_data['ciudad_nacimiento_id']
                    lugar_residencia = form.cleaned_data['ciudad_residencia_id']
                    anio_nacimiento = form.cleaned_data['anio_nacimiento']
                    if not documento =="":
                        personas = Personas.objects.filter(nro_doc = documento)
                    else:
                        personas = Personas.objects.all().order_by('id')
                        if not apellido == "":
                            personas = personas.filter(apellidos__icontains = apellido)
                        if not nombre == "":
                            personas = personas.filter(nombres__icontains = nombre)
                        if not lugar_nacimiento == "":
                            personas = personas.filter(ciudad_nac = lugar_nacimiento)
                        if not lugar_residencia == "":
                            personas = personas.filter(ciudad_res = lugar_residencia)
                        if not anio_nacimiento == "":
                            personas = personas.filter(fecha_nac__year = anio_nacimiento )
                    resultados = Prontuario.objects.filter(persona__in = personas)
                    data = serializers.serialize("json", resultados)
                    return HttpResponse(data, content_type='application/json')
        return HttpResponseBadRequest()
    return HttpResponseRedirect("/")

@login_required
@group_required(["prontuario"])
def obtener_miniatura(request,id):
    prontuario = Prontuario.objects.get(id=id)
    foto = prontuario.fotos.filter(tipo_foto=1)
    if len(foto) > 0:
        foto = '/media/'+str(foto[0].foto)
    else:
        foto = '/static/prontuario/images/avatar.png'
    return render(request,"./miniatura.html",{'prontuario':prontuario,'foto':foto})

@login_required
@group_required(["prontuario"])
def ver_prontuario(request,id):
    #if request.is_ajax():
        values = {}
        persona = Personas.objects.get(id=id)
        try:
            values['prontuario'] = persona.prontuario
        except Exception as e:
            values['prontuario'] = None
        try:
            values['fotos'] = values['prontuario'].fotos.all()
        except Exception as e:
            values['fotos'] = None
        try:
            values['identificacion'] = persona.identificacion_set.latest(field_name = 'id')
        except Exception as e:
            values['identificacion'] = None
        values['domicilios'] = persona.persodom.all()[:2]
        values['padres'] = persona.padre.all()
        if values['padres'].count() > 0:
            values['padres'] = persona.padre.all()[0]
        values['preventivos'] = PreventivosPersona.objects.filter(documento = persona.nro_doc)
        values['persona'] = persona
        return render(request,"./prontuario.html",values)
    #return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def modificar_persona(request,id):
    if request.is_ajax():
        persona = Personas.objects.get(id=id)
        form    = PersonasForm(instance = persona)
        return render(request,"./modificar_persona.html",{'persona':persona,'form':form})
    return HttpResponseBadRequest()

def persona_save(request,id):
    if request.is_ajax():
        if request.method == "POST":
            persona = Personas.objects.get(id=id)
            form = PersonasForm(request.POST,instance=persona)
            if form.is_valid():
                persona.tipo_doc    = form.cleaned_data['tipo_doc']
                persona.nro_doc     = form.cleaned_data['nro_doc']
                persona.apellidos   = form.cleaned_data['apellidos']
                persona.nombres     = form.cleaned_data['nombres']
                persona.sexo_id     = form.cleaned_data['sexo_id']
                persona.fecha_nac   = form.cleaned_data['fecha_nac']
                persona.ocupacion   = form.cleaned_data['ocupacion']
                persona.save()
                return HttpResponse("La persona se modifico correctamente.")
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def verificar_dni(request,id,dni):
    if request.is_ajax():
        response_data = {}
        persona = Personas.objects.get(id=id)
        parametros = {}
        parametros['apellido']          = ""
        parametros['nombre']            = ""
        parametros['fecha_nacimiento']  = ""
        parametros['ciudad_nacimiento'] = ""
        parametros['pais_nacimiento']   = ""
        parametros['ciudad_nacimiento_id'] = ""
        parametros['pais_nacimiento_id']   = ""
        parametros['documento']         = dni
        parametros['alias']             = ""
        persona_spid = buscar_persona_spid(parametros)
        persona_rrhh = buscar_persona_rrhh(parametros)
        persona_acei = buscar_persona_acei(parametros)
        if len(persona_spid) > 0:
            if not persona.id == persona_spid[0].id:
                response_data['error'] = 1
                response_data['error_message'] = '%s, %s' %(persona_spid[0].apellidos,persona_spid[0].nombres)
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        if len(persona_rrhh) > 0:
            if not persona.apellidos == persona_rrhh[0]['apellido'] and not persona.nombres == persona_rrhh[0]['nombre']:
                response_data['error'] = 1
                response_data['error_message'] = '%s, %s' %(persona_rrhh[0]['apellido'],persona_rrhh[0]['nombre'])
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        if len(persona_acei) > 0:
            if not persona.apellidos == persona_acei[0].surname and not persona.nombres == "%s %s"  %(persona_acei[0].name_1,persona_acei[0].name_2):
                response_data['error'] = 1
                response_data['error_message'] = '%s, %s %s' %(persona_acei[0].surname,persona_acei[0].name_1,persona_acei[0].name_2)
                return HttpResponse(json.dumps(response_data), content_type="application/json")

        response_data['error'] = 2
        response_data['error_message'] = "se puede modificar."
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def nuevo_elemento(request,tipo):
    if request.is_ajax():
        form = None
        elemento = None
        if request.method == 'POST':
            elemento = RefOcupacionEspecifica() if tipo == 'ocupacion' else RefContextura() if tipo == 'contextura' else RefPaises()if tipo == "pais" else RefCiudades()
            form = OcupacionEspecificaForm(request.POST) if tipo == 'ocupacion' else ContexturaForm(request.POST) if tipo == 'contextura' else PaisesForm(request.POST) if tipo == "pais" else CiudadesForm(request.POST)
            if form.is_valid():
                if tipo == "ciudad":
                    elemento.pais = form.cleaned_data['pais']
                elemento.descripcion = form.cleaned_data['descripcion'].upper()
                elemento.save()
                return HttpResponse(json.dumps({'tipo':tipo,'id':elemento.id,'descripcion':elemento.descripcion}),content_type="application/json")
        else:
            if tipo == "ocupacion":
                form = OcupacionEspecificaForm()
            if tipo == "contextura":
                form = ContexturaForm()
            if tipo == "pais":
                form = PaisesForm()
            if tipo == "ciudad":
                form = CiudadesForm()
                print (form)
            return render(request,"./nuevo_elemento.html",{'form':form,'tipo':tipo})
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def eliminar_historial(request):
    if request.is_ajax():
        usuario = request.user
        historial = SearchHistory.objects.filter(usuario = usuario)
        resultados = SearchResults.objects.filter(usuario = usuario)
        if historial.count() > 0:
            for registro in historial:
                registro.delete()
            for resultado in resultados:
                resultado.delete()
        return HttpResponse("Accion realizada con exito.")
    return HttpResponseBadRequest()

@login_required
@group_required(["prontuario"])
def buscar_procesales(request):
    if request.is_ajax():
        form = BuscarProcesalesForm()
        if request.method =='POST':
            form = BuscarProcesalesForm(request.POST)
            if form.is_valid():
                n_c = "%s %s"  % (form.cleaned_data['apellido'],form.cleaned_data['nombre'])
                dni = form.cleaned_data['documento']
                resultados = Indice.objects.using('prontuario').all()
                if not n_c == "" and dni =="":
                    resultados = resultados.filter(n_c__icontains = n_c)
                if not dni == "" and n_c == "":
                    resultados = resultados.filter(dni=dni)
                if not dni == "" and not n_c == "" :
                    resultados = resultados.filter(dni=dni,n_c__icontains=n_c)
                print (resultados.count())
                if resultados.count() > 0:
                    return render(request,"./listado_procesales.html",{'resultado':resultados,'id':0,'cambia':True})
                else:
                    return HttpResponseNotFound()
        return render(request,"buscar_procesales.html",{'form':form})
    return HttpResponseBadRequest()


def preventivos_persona(request,persona):
    resultados = PreventivosPersona.objects.filter(documento = persona)
    return render(request,"./preventivos_persona.html",{'resultados':resultados})


def imprimir_prontuario(request,prontuario):
    prontuario = get_object_or_404(Prontuario,id=prontuario)

    return render(request,"impresion.html",{'prontuario':prontuario})