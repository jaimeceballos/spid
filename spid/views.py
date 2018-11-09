#encoding:utf-8
from preventivos.models import *
from preventivos.forms import *
from .forms import *
from django.template.context_processors import csrf
from django.template import Context, Template, RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, render_to_response,get_object_or_404
from django.core import serializers
import json as simplejson
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.contrib import auth
from django.http import Http404
import sys, os
from datetime import date
import random,datetime,time
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_text
from django.contrib.auth import logout
from io import BytesIO
from django.utils.encoding import smart_bytes, smart_text
#from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template import Context, loader
from django.forms.utils import ErrorList
from preventivos.views import obtener_cantidad_no_enviados, obtener_cantidad_no_autorizados
from prontuario.models import SearchResults, SearchHistory
from preventivos.models import Dependencias, UnidadesRegionales
import json

def some_view(request):
   full= os.path.dirname(__file__)+"/static/pdfs/"
   fullpath = os.path.join(full, 'preventivo digital SPID.pdf',)
   response = HttpResponse(file(fullpath).read())
   response['Content-Type'] = 'application/pdf'
   response['Content-disposition'] = 'attachment; filename=preventivo\ digital\ SPID.pdf'
   return response



def obtener_dependencias(request,depes):

        data = request.POST
        dependencias = Dependencias.objects.filter(unidades_regionales = depes)
        data = serializers.serialize("json", dependencias)
        return HttpResponse(data, mimetype='application/json')

def help_view(request):
    state = ''
    name=''
    username = password = ''
    destino = ''
    form = DependenciasForm()
    formd = []
    return render(request, 'musers.html', {'formd':formd,'state':state,'destino':destino,'form':form})

#Definicion que carga la pantalla de login
def iniciar(request):
    
    """Esta deficnicion es la encargada de cargar la pantalla de login y de la
    preparacion del entorno para la misma
    #Inicializacion de variables para generar el entorno
    state = ''                      #estado
    name=''                         #nombre
    username = password = ''        #usuario y password
    destino = ''                    #destino
    form = DependenciasForm()       #formulario de dependencias
    formd = []                      #arreglo formd
    #renderiza la pagina de inicio con las variables de inicializacion del entorno
    return render(request, 'index.html', {'formd':formd,'state':state,'destino':destino,'form':form})"""
    try:
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    except Exception as e:
        print(e)
    

#definicion para loguear un usuario
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        user = None
        error = ""
        changePass = ""
        if form.is_valid():
            usuario             = form.cleaned_data['usuario']
            password            = form.cleaned_data['password']
            dependencia         = form.cleaned_data['dependencia_id']
            unidad_regional     = form.cleaned_data['unidad_regional_id']
            try:
                user            = User.objects.get(username = usuario)
                if user.userprofile.last_login:
                    return HttpResponseRedirect('/spid/primer_ingreso/%d/' % user.id)
            except Exception as e:
                error = "El usuario no existe."
            print(user)
            if user.is_active:
                if str(user.userprofile.depe.id) == dependencia:
                    if user.userprofile.last_login:
                        changePass = 'si'                                            #si esta levantada prepara una bandera que indica que debe cambiar la contraseña
                    grupos = user.groups.values_list('name',flat=True) 
                    radio_user = True if 'Radio' in grupos else False
                    
                    if len(grupos) == 1 or (len(grupos) == 2 and "administrador" in grupos) :
                        if "prontuario" in grupos:
                            ultimo_ingreso = User.objects.get(username = usuario).last_login      #obtiene la fecha de ultimo ingreso
                            profile = User.objects.get(username=usuario).userprofile            #obtiene el perfil del usuario
                            profile.ultimo_ingreso = ultimo_ingreso                                #asigna el ultimo ingreso al perfil del usuario
                            profile.save()                                                         #guarda el valor
                            user = auth.authenticate(username=usuario, password=password)      #autentica al usuario
                            destino = "%s / %s" % (profile.depe,profile.ureg)
                            state = user.groups.values_list('name', flat=True)
                            request.session['state']=state                                #si es correcto carga en la sesion la variable estado
                            request.session['destino']=destino                            #carga en la sesion la variable destino
                            
                            if user:
                                auth.login(request, user)                                       #realiza el login del usuario
                                return HttpResponseRedirect("/prontuario/")
                            return HttpResponseRedirect("/spid/")
                                
                        else:
                            destino = "%s / %s" % (user.userprofile.depe,user.userprofile.ureg)
                            state = user.groups.values_list('name', flat=True)
                            no_enviados = False                                           #inicializa una variable de no enviados
                            #verifica si el usuario es preventor
                            if Actuantes.objects.filter(funcion__gt=1,documento=user.username):
                                no_enviados = obtener_cantidad_no_enviados(request)         #obtiene la cantidad de preventivos no enviados
                                no_autorizados = obtener_cantidad_no_autorizados(request)     #obtiene la cantidad de preventivos no autorizados
                                radio_user = False                                            #crea una variable radio user para identificar si el usuario pertenece a una radiocabecera
                            #verifica si dentro de los grupos del usuario se encuentra radio
                            if user.groups.filter(name='radio'):
                                radio_user = True                                       #pone en tru radio user
                            autorizados = 0                                               #establece un contador de preventivos autorizados en 0
                            no_autorizados = 0
                            #si es usuario de radiocabecera
                            if radio_user:
                                preventivos = ""
                                dependencias = ""
                                dependencias = Dependencias.objects.filter(ciudad = user.userprofile.depe.ciudad )
                                preventivos = Preventivos.objects.filter(dependencia__in=dependencias,fecha_autorizacion__isnull=False,fecha_envio__isnull = True)            #para esas dependencias obtiene los preventivos autorizados no enviados
                                #si hay preventivos no enviados
                                if preventivos.count() > 0:
                                    autorizados = preventivos.count()                     #obtiene la cantidad de preventivos autorizados para enviar
                            form = DependenciasForm()       #formulario de dependencias
                            formpass = CambiarPassForm()    #formulario de cambio de contraseña
                            ultimo_ingreso = User.objects.get(username = usuario).last_login      #obtiene la fecha de ultimo ingreso
                            profile = User.objects.get(username=usuario).userprofile            #obtiene el perfil del usuario
                            profile.ultimo_ingreso = ultimo_ingreso                                #asigna el ultimo ingreso al perfil del usuario
                            profile.save()                                                         #guarda el valor
                            user = auth.authenticate(username=usuario, password=password)      #autentica al usuario
                            request.session['state']=state                                #si es correcto carga en la sesion la variable estado
                            request.session['destino']=destino                            #carga en la sesion la variable destino
                            if user:
                                auth.login(request, user)
                                return render(request, './index1.html', {'form':form,'state':state, 'destino': destino,'changePass':changePass,'formpass':formpass,'no_enviados':no_enviados,'no_autorizados':no_autorizados,'ultimo_ingreso':ultimo_ingreso,'radio_user':radio_user,'autorizados':autorizados})
                            return HttpResponseRedirect("/spid/")
                    elif len(grupos) > 1 and ('prontuario' in grupos):
                        request.session['cambia_sistema'] = 'radio' in grupos or 'policia' in grupos or 'investigaciones' in grupos or 'jefes' in grupos
                        ultimo_ingreso = User.objects.get(username = usuario).last_login      #obtiene la fecha de ultimo ingreso
                        profile = User.objects.get(username=usuario).userprofile            #obtiene el perfil del usuario
                        profile.ultimo_ingreso = ultimo_ingreso                                #asigna el ultimo ingreso al perfil del usuario
                        profile.save()                                                         #guarda el valor
                        user = auth.authenticate(username=usuario, password=password)      #autentica al usuario
                        if user:
                            auth.login(request, user)                                       #realiza el login del usuario
                            return render(request,"./seleccionar_sistema.html",{'usuario':usuario})
                        return HttpResponseRedirect('/spid/')
                    else:
                        destino = "%s / %s" % (user.userprofile.depe,user.userprofile.ureg)
                        state = grupos
                        

                        form = DependenciasForm()       #formulario de dependencias
                        formpass = CambiarPassForm()    #formulario de cambio de contraseña
                        ultimo_ingreso = User.objects.get(username = usuario).last_login      #obtiene la fecha de ultimo ingreso
                        profile = User.objects.get(username=usuario).userprofile            #obtiene el perfil del usuario
                        profile.ultimo_ingreso = ultimo_ingreso                                #asigna el ultimo ingreso al perfil del usuario
                        profile.save()                                                         #guarda el valor
                        user = auth.authenticate(username=usuario, password=password)      #autentica al usuario
                        auth.login(request, user)
                        no_enviados = False                                           #inicializa una variable de no enviados
                        #verifica si el usuario es preventor
                        if Actuantes.objects.filter(funcion__gt=1,documento=user.username):
                            no_enviados = obtener_cantidad_no_enviados(request)         #obtiene la cantidad de preventivos no enviados
                            no_autorizados = obtener_cantidad_no_autorizados(request)     #obtiene la cantidad de preventivos no autorizados
                            radio_user = False                                            #crea una variable radio user para identificar si el usuario pertenece a una radiocabecera
                        #verifica si dentro de los grupos del usuario se encuentra radio
                        if user.groups.filter(name='radio'):
                            radio_user = True                                       #pone en tru radio user
                            
                            no_autorizados = 0
                        autorizados = 0                                               #establece un contador de preventivos autorizados en 0
                        #si es usuario de radiocabecera
                        if radio_user:
                            preventivos = ""
                            dependencias = ""
                            dependencias = Dependencias.objects.filter(ciudad = user.userprofile.depe.ciudad )
                            preventivos = Preventivos.objects.filter(dependencia__in=dependencias,fecha_autorizacion__isnull=False,fecha_envio__isnull = True)            #para esas dependencias obtiene los preventivos autorizados no enviados
                            #si hay preventivos no enviados
                            if preventivos.count() > 0:
                                autorizados = preventivos.count()                     #obtiene la cantidad de preventivos autorizados para enviar
                        request.session['state'] = serializers.serialize('json',user.groups.all(),fields=("name"))                                #si es correcto carga en la sesion la variable estado
                        request.session['destino'] = destino                            #carga en la sesion la variable destino
                        values = {
                        'form':form,
                        'state':state, 
                        'destino': destino,
                        'changePass':changePass,
                        'formpass':formpass,
                        'no_enviados':no_enviados,
                        'no_autorizados':no_autorizados,
                        'ultimo_ingreso':ultimo_ingreso,
                        'radio_user':radio_user,
                        'autorizados':autorizados
                        }
                        return render(request, './index1.html', values)

            else:
                return render(request,"login.html",{'form':form,'error':"Usuario Desactivado."})
        return render(request,"./login.html",{'form':form})
    return HttpResponseRedirect("/spid/")

def primer_ingreso(request,id):
    form = CambiarPassForm()
    usuario = User.objects.get(id = id)
    state = "R" if "repar" in usuario.groups.values_list('name', flat=True) else ""
    return render(request,'./primer_ingreso.html',{'form':form,'state':state,'usuario':usuario.id})


def dependencias_ajax(request):
    if request.is_ajax():
        q = request.GET.get('term','')

        dependencias = Dependencias.objects.filter(descripcion__icontains = q)[:20]
        results = []
        for dependencia in dependencias:
            dependencia_json = {}
            dependencia_json['id'] = dependencia.id
            dependencia_json['label'] =  dependencia.descripcion + ' - ' + dependencia.unidades_regionales.descripcion
            dependencia_json['value'] = dependencia.descripcion + ' - ' + dependencia.unidades_regionales.descripcion
            dependencia_json['unidad_regional_id']  = dependencia.unidades_regionales.id
            results.append(dependencia_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data,mimetype)

def registro(request):
    info_enviado = False
    name=""
    docu=""
    jerarca=""
    destino=""
    mail=""
    comment=""
    formulario=""
    today = datetime.datetime.now()
    datos=[]
    soli=''
    if request.POST.get('envia')=='Enviar':
           jerarca=RefJerarquias.objects.get(id=request.POST.get('jerarca'))

           info_enviado= True
           subject, from_email, to = 'Solicitud de Usuario - SPID' ,request.POST.get('mail'), 'divsistemasjp@policia.chubut.gov.ar'
           text_content = "Solicitud recibida de : %s<br><br>Nro de Dni : %s<br><br>Jerarquia : %s<br><br>Destino actual : %s<br><br> Usuarios <br><br> %s <br><br>" % (request.POST.get('name'),str(request.POST.get('docu')),jerarca,request.POST.get('destino'),request.POST.get('comment'))
           msg = EmailMultiAlternatives(subject,text_content,from_email, [to])
           msg.attach_alternative(text_content,'text/html')
           try:
               msg.send(fail_silently=True)
           except IndexError:
               pass


           cabecera = '<br><br><br>'+'Al Sr :............................'+'<br>'+'ADMINISTRADOR SPID'+'<br>'+'S____________/_____________D'+'<br><br>'
           cuerpos='Por medio de la presente, me dirijo a UD. con el fin de solicitar el ALTA de usuarios al Sistema SPID'
           usuas='Lista del Personal A/C: '+str(jerarca)+' - '+str(request.POST.get('destino'))+'<br><br>'+str(request.POST.get('comment'))+'<br><br><br><br><br><br>'
           saludo='Sin más que agregar, aprovecho la ocasión para saludarlo muy atentamente.'+'<br><br><br><br><br><br><br><br><br><br>'
           datos.append(cabecera)
           for i in datos:
             soli=soli+i

           return  render(request,'solicitud.html',{'name':soli,'today':today,'cuerpos':cuerpos,'usuas':usuas,'saludo':saludo,})
    else:
       formj = ActuantesForm()

       return render(request, 'correocontacto.html',  {'name':name,'formj':formj})

def contactar(request):
    info_enviado = False
    name=""
    docu=""
    jerarca=""
    destino=""
    mail=""
    comment=""
    formulario=""
    today = datetime.datetime.now()
    datos=[]
    soli=''

    if request.POST.get('envia')=='Enviar':

           info_enviado= True
           subject, from_email, to = 'Solicitud de Información' ,request.POST.get('mail'), 'fydsoftware@gmail.com'
           text_content = "Solicitud recibida de : %s<br><br> Comentario : %s <br><br>" % (request.POST.get('name'),request.POST.get('comment'))
           msg = EmailMultiAlternatives(subject,text_content,from_email, [to])
           msg.attach_alternative(text_content,'text/html')
           #agregar email jaime para que reciba premios
           dire=[]
           dire.append(to)
           direcciones=[]
           for dire in dire:
              direcciones.append(dire)
              direcciones.append('jaimeceballos82@gmail.com')

           for cantdir in direcciones:

             try:
               msg = EmailMultiAlternatives(subject,text_content,from_email, [cantdir])
               msg.attach_alternative(text_content,'text/html')
               msg.send(fail_silently=True)
             except IndexError:
               pass
          
           return render(request,'solicitar.html',  {'name':name})
    else:
       return render(request, 'contacto.html',  {'name':name})

def inicial(request):
    
    ciudades = ""
    state= request.session.get('state')
    destino= request.session.get('destino')
    form = DependenciasForm()
    return render(request,'./index1.html',{'form':form, 'state':state, 'destino': destino})


def verificar_grupo(grupo,usuario):
    if grupo != "":
        group = Group.objects.get(name=grupo)
        return True if group in usuario.groups.all() else False
    return False

def nologin(request):
    usuario = request.user
    logout(request)
    if verificar_grupo("prontuario",usuario):
        for resultado in SearchResults.objects.filter(usuario = usuario):
            resultado.delete()

        for busqueda in SearchHistory.objects.filter(usuario = usuario):
            busqueda.delete()
    try:
        del request.session['state']
        del request.session['destino']
        request.session.flush()
    except KeyError:
        pass
        state = "SE DESCONECTO DEL SISTEMA"
    form = DependenciasForm()
    formd = []
    return HttpResponseRedirect('/spid/')



def passwordChange(request,id):
  formpass = CambiarPassForm(request.POST)
  changePass = 'si'


  form = DependenciasForm()

  user = User.objects.get(id=id)
  #if formpass.is_valid():
  pass1 = request.POST.get('pass1')

  if pass1:
     user.date_joined=datetime.datetime.now()
     user.set_password(pass1)
     user.save()
     profiles = user.userprofile
     profiles.last_login=False
     if profiles.solicitud_cambio:                                              #si el cambio de contraseña es por un pedido de reinicio
         profiles.solicitud_cambio = False                                      #cambio la bandera de solicitud de cambio
         profiles.fecha_solicitud = None                                        #blanqueo la fecha de solicitud de reinicio
         profiles.clave_anterior = None                                         #blanqueo la clave anterior
     profiles.save()
     changePass = ''
  logout(request)
  try:
      state = request.session['state']
      destino = request.session['destino']
      del request.session['state']
      del request.session['destino']
      request.session.flush()
  except KeyError:
      pass
      state = "SE DESCONECTO DEL SISTEMA"
  form = DependenciasForm()
  formd = []
  
  return HttpResponseRedirect("/spid/")
  #return render(request, './index.html', {'formd':formd,'form':form,'state':state, 'destino': destino, 'changePass':changePass,'formpass':formpass})
