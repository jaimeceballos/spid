#encoding:utf-8
from preventivos.models import *
from preventivos.forms import *
from .forms import *
from django.core.context_processors import csrf
from django.template import Context, Template, RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, render_to_response,get_object_or_404
from django.core import serializers
from django.utils import simplejson
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
from django.utils.encoding import smart_str, smart_unicode
#from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template import Context, loader
from django.forms.util import ErrorList
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
    form = LoginForm()

    return render_to_response('./login.html',{'form':form},context_instance= RequestContext(request))

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
                if user.get_profile().last_login:
                    return HttpResponseRedirect('/spid/primer_ingreso/%d/' % user.id)
            except Exception as e:
                error = "El usuario no existe."
            if user.is_active:
                if str(user.get_profile().depe.id) == dependencia:
                    if user.get_profile().last_login:
                        changePass = 'si'                                            #si esta levantada prepara una bandera que indica que debe cambiar la contraseña
                    grupos = user.groups.values_list('name', flat=True)

                    if len(grupos) == 1 or (len(grupos) == 2 and "administrador" in grupos) :
                        if "prontuario" in grupos:
                            ultimo_ingreso = User.objects.get(username = usuario).last_login      #obtiene la fecha de ultimo ingreso
                            profile = User.objects.get(username=usuario).get_profile()            #obtiene el perfil del usuario
                            profile.ultimo_ingreso = ultimo_ingreso                                #asigna el ultimo ingreso al perfil del usuario
                            profile.save()                                                         #guarda el valor
                            user = auth.authenticate(username=usuario, password=password)      #autentica al usuario
                            auth.login(request, user)                                       #realiza el login del usuario
                            destino = "%s / %s" % (profile.depe,profile.ureg)
                            state = user.groups.values_list('name', flat=True)
                            request.session['state']=state                                #si es correcto carga en la sesion la variable estado
                            request.session['destino']=destino                            #carga en la sesion la variable destino
                            return HttpResponseRedirect("/prontuario/")
                        else:
                            destino = "%s / %s" % (user.get_profile().depe,user.get_profile().ureg)
                            state = grupos
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
                                dependencias = Dependencias.objects.filter(ciudad = user.get_profile().depe.ciudad )
                                preventivos = Preventivos.objects.filter(dependencia__in=dependencias,fecha_autorizacion__isnull=False,fecha_envio__isnull = True)            #para esas dependencias obtiene los preventivos autorizados no enviados
                                #si hay preventivos no enviados
                                if preventivos.count() > 0:
                                    autorizados = preventivos.count()                     #obtiene la cantidad de preventivos autorizados para enviar
                            form = DependenciasForm()       #formulario de dependencias
                            formpass = CambiarPassForm()    #formulario de cambio de contraseña
                            ultimo_ingreso = User.objects.get(username = usuario).last_login      #obtiene la fecha de ultimo ingreso
                            profile = User.objects.get(username=usuario).get_profile()            #obtiene el perfil del usuario
                            profile.ultimo_ingreso = ultimo_ingreso                                #asigna el ultimo ingreso al perfil del usuario
                            profile.save()                                                         #guarda el valor
                            user = auth.authenticate(username=usuario, password=password)      #autentica al usuario
                            auth.login(request, user)
                            request.session['state']=state                                #si es correcto carga en la sesion la variable estado
                            request.session['destino']=destino                            #carga en la sesion la variable destino
                            return render(request, './index1.html', {'form':form,'state':state, 'destino': destino,'changePass':changePass,'formpass':formpass,'no_enviados':no_enviados,'no_autorizados':no_autorizados,'ultimo_ingreso':ultimo_ingreso,'radio_user':radio_user,'autorizados':autorizados})
                    elif len(grupos) > 1 and ('prontuario' in grupos):
                        request.session['cambia_sistema'] = 'radio' in grupos or 'policia' in grupos or 'investigaciones' in grupos or 'jefes' in grupos
                        ultimo_ingreso = User.objects.get(username = usuario).last_login      #obtiene la fecha de ultimo ingreso
                        profile = User.objects.get(username=usuario).get_profile()            #obtiene el perfil del usuario
                        profile.ultimo_ingreso = ultimo_ingreso                                #asigna el ultimo ingreso al perfil del usuario
                        profile.save()                                                         #guarda el valor
                        user = auth.authenticate(username=usuario, password=password)      #autentica al usuario
                        auth.login(request, user)                                       #realiza el login del usuario
                        return render_to_response("./seleccionar_sistema.html",{'usuario':usuario},context_instance=RequestContext(request))
                    else:
                        destino = "%s / %s" % (user.get_profile().depe,user.get_profile().ureg)
                        state = grupos
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
                            dependencias = Dependencias.objects.filter(ciudad = user.get_profile().depe.ciudad )
                            preventivos = Preventivos.objects.filter(dependencia__in=dependencias,fecha_autorizacion__isnull=False,fecha_envio__isnull = True)            #para esas dependencias obtiene los preventivos autorizados no enviados
                            #si hay preventivos no enviados
                            if preventivos.count() > 0:
                                autorizados = preventivos.count()                     #obtiene la cantidad de preventivos autorizados para enviar
                        form = DependenciasForm()       #formulario de dependencias
                        formpass = CambiarPassForm()    #formulario de cambio de contraseña
                        ultimo_ingreso = User.objects.get(username = usuario).last_login      #obtiene la fecha de ultimo ingreso
                        profile = User.objects.get(username=usuario).get_profile()            #obtiene el perfil del usuario
                        profile.ultimo_ingreso = ultimo_ingreso                                #asigna el ultimo ingreso al perfil del usuario
                        profile.save()                                                         #guarda el valor
                        user = auth.authenticate(username=usuario, password=password)      #autentica al usuario
                        auth.login(request, user)
                        request.session['state']=state                                #si es correcto carga en la sesion la variable estado
                        request.session['destino']=destino                            #carga en la sesion la variable destino
                        return render(request, './index1.html', {'form':form,'state':state, 'destino': destino,'changePass':changePass,'formpass':formpass,'no_enviados':no_enviados,'no_autorizados':no_autorizados,'ultimo_ingreso':ultimo_ingreso,'radio_user':radio_user,'autorizados':autorizados})


        return render_to_response("./login.html",{'form':form},context_instance=RequestContext(request))
    return HttpResponseRedirect("/spid/")

    """error = ""
    state = []                      #estado
    name=''                         #nombre
    username = password = ''        #usuario y contraseña
    destino = ''                    #destino
    changePass = ''                 #bandera de cambio de password
    birthday=False                  #bandera de cumpleaños
    form = DependenciasForm()       #formulario de dependencias
    formpass = CambiarPassForm()    #formulario de cambio de contraseña
    if request.POST.get('logonea')=='Conectar':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            depe = request.POST.get('dependencias')
            ureg = request.POST.get('ureg')
            ultimo_ingreso = User.objects.get(username = username).last_login      #obtiene la fecha de ultimo ingreso
            profile = User.objects.get(username=username).get_profile()            #obtiene el perfil del usuario
            profile.ultimo_ingreso = ultimo_ingreso                                #asigna el ultimo ingreso al perfil del usuario
            profile.save()                                                         #guarda el valor
        except Exception as e:
            error = "Acceso incorrecto al sistema."

    return render_to_response('index.html', {'name':error,'form':form},context_instance = RequestContext(request))"""


    """ esta definicion realiza el logueo del usuario y las verificaciones
    necesarias para saber que tipo de usuario es el que se esta logueando
    tambien prepara el entorno correspondiente para cada tipo de usuario
    #Definicion e incializacion de variables
    state = []                      #estado
    name=''                         #nombre
    username = password = ''        #usuario y contraseña
    destino = ''                    #destino
    changePass = ''                 #bandera de cambio de password
    birthday=False                  #bandera de cumpleaños
    form = DependenciasForm()       #formulario de dependencias
    formpass = CambiarPassForm()    #formulario de cambio de contraseña

    #Comienzo de la logica
    #si el boton presionado fue conectar
    if request.POST.get('logonea')=='Conectar':
     try:

         username = request.POST.get('username')                                #obtiene el nombre de usuario
         password = request.POST.get('password')                                #obtiene la contraseña
         depe = request.POST.get('dependencias')                                #obtiene la dependencia
         ureg = request.POST.get('ureg')                                        #obtiene la unidad regional
         ultimo_ingreso = User.objects.get(username = username).last_login      #obtiene la fecha de ultimo ingreso
         profile = User.objects.get(username=username).get_profile()            #obtiene el perfil del usuario
         profile.ultimo_ingreso = ultimo_ingreso                                #asigna el ultimo ingreso al perfil del usuario
         profile.save()                                                         #guarda el valor
         #si el nombre de usuario es numerico
         if username.isdigit():
          user = auth.authenticate(username=username, password=password)        #autentica el usuario
          #si la autenticacion es valida
          if user is not None:
           #Verifica si es el cumpleaños del usuario
           if Personas.objects.get(nro_doc=username).fecha_nac.day == date.today().day and Personas.objects.get(nro_doc=username).fecha_nac.month == date.today().month:
              birthday = True                                                   #asigna true a la bandera de cumpleaños

         #si se obtuvo unidad regional y dependencia
         if ureg and depe:
            uregi1=UnidadesRegionales.objects.get(id=ureg)                      #obtiene la unidad regional
            uregis1=uregi1.id                                                   #obtiene el id de la unidad regional
            depen1=Dependencias.objects.get(id=depe)                            #obtiene la dependencia
            depeni1=depen1.id                                                   #obtiene el id de la dependencia

         #si no se obtuvo la dependencia y unidad regional
         else:
            uregis1='1'                                                         #a la variable de id de unidad regional le asigna 1
            depeni1='1'                                                         #a la variable de id de dependencia le asigna 1
            destino="Jefatura"                                                  #al destino le asigna "jefatura"

         #si depe es numerico
         if depe.isdigit():
            destino = Dependencias.objects.get(id = depe)                       #obtiene en destino la dependencia
            ur=UnidadesRegionales.objects.get(id = ureg)                        #obtiene en ur la unidad regional
            destino= '%s / %s' %(destino,ur)                                    #prepara una cadena con la dependencia y unidad regional
            user = auth.authenticate(username=username, password=password)      #autentica al usuario

            #si se pudo autenticar
            if user is not None:
              #y el usuario esta activo
              if user.is_active:
                #verifica si en el perfil esta levantada la bandera que indica primer inicio de sesion
                if user.get_profile().last_login:
                   changePass = 'si'                                            #si esta levantada prepara una bandera que indica que debe cambiar la contraseña

                auth.login(request, user)                                       #realiza el login del usuario
                userp=user.get_profile()                                        #obtiene el perfil
                profiles = user.get_profile()                                   #obtiene el perfil
                uregs=profiles.ureg                                             #obtiene la unidad regional del usuario
                depes=profiles.depe                                             #obtiene la dependencia del usuario
                uregi=UnidadesRegionales.objects.get(descripcion=uregs)         #crea una instancia de la unidad regional
                uregis=uregi.id                                                 #obtiene el id de la unidad regional
                depen=Dependencias.objects.get(descripcion=depes)               #crea una instancia de la dependencia
                depeni=depen.id                                                 #obtiene el id de la dependencia


                gr=user.groups.values_list('name', flat=True)                   #obtiene los grupos que tiene asignado el usuario
                #para cada grupo
                for varios in gr:
                    state.append(str(Group.objects.get(name=varios)))           #agrega el grupo a la variable de estado

                #Verifica que el usuario se este logueando en su dependencia destino
                if uregis == uregis1 and depeni == depeni1:
                  request.session['state']=state                                #si es correcto carga en la sesion la variable estado
                  request.session['destino']=destino                            #carga en la sesion la variable destino
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

                  #si es usuario de radiocabecera
                  if radio_user:
                      preventivos = ""
                      dependencias = ""

                      dependencias = Dependencias.objects.filter(ciudad = user.get_profile().depe.ciudad )
                      preventivos = Preventivos.objects.filter(dependencia__in=dependencias,fecha_autorizacion__isnull=False,fecha_envio__isnull = True)            #para esas dependencias obtiene los preventivos autorizados no enviados
                      #si hay preventivos no enviados
                      if preventivos.count() > 0:
                          autorizados = preventivos.count()                     #obtiene la cantidad de preventivos autorizados para enviar

                  #Renderiza el template index1 logueo correcto, con todas las variables de entorno inicializadas
                  if 'prontuario' in gr:
                      if 'policia' in gr or 'jefes' in gr or 'radio' in gr or 'investigaciones' in gr:
                          return render_to_response('./seleccionar_sistema.html',{'form':form,'state':state, 'destino': destino,'changePass':changePass,'formpass':formpass,'birthday':birthday,'no_enviados':no_enviados,'no_autorizados':no_autorizados,'ultimo_ingreso':ultimo_ingreso,'radio_user':radio_user,'autorizados':autorizados},context_instance = RequestContext(request))
                      else:
                          return HttpResponseRedirect('/prontuario/')
                  return render(request, './index1.html', {'form':form,'state':state, 'destino': destino,'changePass':changePass,'formpass':formpass,'birthday':birthday,'no_enviados':no_enviados,'no_autorizados':no_autorizados,'ultimo_ingreso':ultimo_ingreso,'radio_user':radio_user,'autorizados':autorizados})

                #si el usuario intenta loguearse en una dependencia que no corresponde a su destino actual
                else:
                  state="Dependencias seleccionadas INCORRECTAS"               #se indica que las dependencia es incorrecta

                  return render(request, 'index.html', {'state':state,'form':form})

              #si el usuario no esta activo
              else:
                state = "Su Usuario fue desactivado. Comuniquese con el Administrador del Sistema" #se indica que el usuario no esta activo
            #si la autenticacion no es correcta
            else:

               state = "Su usuario y/o password son incorrectos"                #se indica que el usuario o contraseña son incorrectos

            return render(request, 'index.html', {'state':state,'form':form})


     except Exception as e:
         error = "Usuario o Contraseña Incorrecta"
         return render(request, 'index.html', {'name':error,'form':form})
    else:
        state="Usuario no Autorizado"
        return render(request, 'index.html', {'state':state,'form':form})"""

def primer_ingreso(request,id):
    form = CambiarPassForm()
    usuario = User.objects.get(id = id)
    state = "R" if "repar" in usuario.groups.values_list('name', flat=True) else ""
    return render_to_response('./primer_ingreso.html',{'form':form,'state':state,'usuario':usuario.id},context_instance = RequestContext(request))


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
           """
           cabecera = '<br><br><br>'+'Al Sr :............................'+'<br>'+'ADMINISTRADOR SPID'+'<br>'+'S____________/_____________D'+'<br><br>'
           cuerpos='Por medio de la presente, me dirijo a UD. con el fin de solicitar el ALTA de usuarios al Sistema SPID'
           usuas='Lista del Personal A/C: '+str(request.POST.get('jerarca'))+' - '+str(request.POST.get('destino'))+'<br><br>'+str(request.POST.get('comment'))+'<br><br><br><br><br><br>'
           saludo='Sin más que agregar, aprovecho la ocasión para saludarlo muy atentamente.'+'<br><br><br><br><br><br><br><br><br><br>'
           datos.append(cabecera)
           for i in datos:
             soli=soli+i

           return  render(request,'solicitud.html',{'name':soli,'today':today,'cuerpos':cuerpos,'usuas':usuas,'saludo':saludo,})"""
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
     profiles = user.get_profile()
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
  #print form,formd
  return HttpResponseRedirect("/spid/")
  #return render(request, './index.html', {'formd':formd,'form':form,'state':state, 'destino': destino, 'changePass':changePass,'formpass':formpass})
