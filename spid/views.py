#encoding:utf-8 
from preventivos.models import *
from preventivos.forms import *
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
#from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template import Context, loader
from django.forms.util import ErrorList


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



def iniciar(request):
    state = ''
    name=''
    username = password = ''
    destino = ''
    form = DependenciasForm()
    formd = []
    return render(request, 'index.html', {'formd':formd,'state':state,'destino':destino,'form':form})

def login_user(request):
    state = ''
    name=''
    username = password = ''
    destino = ''
    changePass = ''
    birthday=False
    form = DependenciasForm()
    formpass = CambiarPassForm()
    if request.POST.get('username')=='':
         formj = ActuantesForm()
         
         return render(request, 'correocontacto.html', {'state':state,'formj':formj})
    else:
        if request.POST.get('logonea')=='Conectar':
         username = request.POST.get('username')
         password = request.POST.get('password')
         depe = request.POST.get('dependencias')
         ureg = request.POST.get('ureg')
         if username.isdigit():
          user = auth.authenticate(username=username, password=password)
          if user is not None:
       
           if Personas.objects.get(nro_doc=username).fecha_nac.day == date.today().day and Personas.objects.get(nro_doc=username).fecha_nac.month == date.today().month:
              birthday = True
     
         if ureg and depe:
            uregi1=UnidadesRegionales.objects.get(id=ureg)
            uregis1=uregi1.id
            depen1=Dependencias.objects.get(id=depe)
            depeni1=depen1.id

         else:
            uregis1='1'
            depeni1='1'
            destino="Jefatura"

         if depe.isdigit():
            destino = Dependencias.objects.get(id = depe)
            ur=UnidadesRegionales.objects.get(id = ureg)
            destino= '%s / %s' %(destino,ur)
            user = auth.authenticate(username=username, password=password)

            if user is not None:
              if user.is_active:
                #print user.last_login,user.date_joined

                #fecha_login=datetime.datetime.strftime(user.last_login, "%Y-%m-%d %H:%M:%S")
                #fecha_joined=datetime.datetime.strftime(user.date_joined, "%Y-%m-%d %H:%M:%S")
                #print type(datetime.datetime.strptime(fecha_login, "%Y-%m-%d %H:%M:%S")),fecha_login,fecha_joined
                #if datetime.datetime.strptime(fecha_login, "%Y-%m-%d %H:%M:%S")<=datetime.datetime.strptime(fecha_joined, "%Y-%m-%d %H:%M:%S"):
                if user.get_profile().last_login:
                   changePass = 'si'
               
                auth.login(request, user)
                userp=user.get_profile()
                profiles = user.get_profile()
                uregs=profiles.ureg
                depes=profiles.depe
                uregi=UnidadesRegionales.objects.get(descripcion=uregs)
                uregis=uregi.id
                depen=Dependencias.objects.get(descripcion=depes)
                depeni=depen.id
              
              
                gr=user.groups.values_list('name', flat=True)
                for varios in gr:
                    state = str(Group.objects.get(name=varios))
                if uregis == uregis1 and depeni == depeni1:
                  for varios in gr:
                    state = str(Group.objects.get(name=varios))
                  request.session['state']=state
                  request.session['destino']=destino
                          
                  return render(request, './index1.html', {'form':form,'state':state, 'destino': destino,'changePass':changePass,'formpass':formpass,'birthday':birthday})
                else:
                  state="Dependencias seleccionadas INCONRRECTAS"
                  return render(request, 'index.html', {'state':state,'form':form})
        
              else:
                state = "Ud. es un Usuario inactivo. Comuniquese con el Administrador del Sistema"
            else:
              
               state = "Su usuario y/o password son incorrectos"
          
            return render(request, 'index.html', {'state':state,'form':form})
         else:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
              if user.is_active:
                #fecha_login=datetime.datetime.strftime(user.last_login, "%Y-%m-%d %H:%M:%S")
                #fecha_joined=datetime.datetime.strftime(user.date_joined, "%Y-%m-%d %H:%M:%S")
                #print type(datetime.datetime.strptime(fecha_login, "%Y-%m-%d %H:%M:%S")),fecha_login,fecha_joined
                #if datetime.datetime.strptime(fecha_login, "%Y-%m-%d %H:%M:%S")!=datetime.datetime.strptime(fecha_joined, "%Y-%m-%d %H:%M:%S"):
                if user.get_profile().last_login:
                   changePass = 'si'
                auth.login(request, user)
                userp=user.get_profile()
                profiles = user.get_profile()
                uregs=profiles.ureg
                depes=profiles.depe
                uregi=UnidadesRegionales.objects.get(descripcion=uregs)
                uregis=uregi.id
                depen=Dependencias.objects.get(descripcion=depes)
                depeni=depen.id

                gr=user.groups.values_list('name', flat=True)
                for varios in gr:
                    state = str(Group.objects.get(name=varios))
                if uregis == uregis1 and depeni == depeni1: 
                   for varios in gr:
                    state = str(Group.objects.get(name=varios))
                   request.session['state']=state
                   request.session['destino']=destino
                else: 

                  if state=="administrador" or state=="visita":
                     state = str(Group.objects.get(name=gr))
                     request.session['state']=state
                     destino='Jefatura'
                     request.session['destino']=destino
                  else:
                    state="Usuario no Autorizado"
                    return render(request, 'index.html', {'state':state,'form':form})
              

              
                        
              else:    
                state="Usuario no Autorizado"
                return render(request, 'index.html', {'state':state,'form':form})
            return render(request, './index1.html', {'form':form,'state':state, 'destino': destino,'changePass':changePass,'formpass':formpass,'birthday':birthday})
          
        else:
            return render(request, 'index.html', {'name':name,'form':form})

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
           subject, from_email, to = 'Solicitud de Usuario - SPID' ,request.POST.get('mail'), 'admredes@policia.chubut.gov.ar'
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
           subject, from_email, to = 'Solicitud de Información' ,request.POST.get('mail'), 'admredes@policia.chubut.gov.ar,fydsoftware@gmail.com'
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


def nologin(request):
    logout(request)
    try:
        del request.session['state']
        del request.session['destino']
        request.session.flush()
    except KeyError:
        pass
        state = "SE DESCONECTO DEL SISTEMA"
    form = DependenciasForm()      
    formd = []  
    return render(request, 'index.html', {'formd':formd,'state':state,'form':form})



def passwordChange(request):
  formpass = CambiarPassForm(request.POST)
  changePass = 'si'

  state = request.session['state']
  destino = request.session['destino']
  form = DependenciasForm()

  user = User.objects.get(username=request.user)
  #if formpass.is_valid():
  pass1 = request.POST.get('pass1')
 
  if pass1:
     user.date_joined=datetime.datetime.now()
     user.set_password(pass1)
     user.save()
     profiles = user.get_profile()
     profiles.last_login=False
     profiles.save()
     changePass = ''
  logout(request)
  try:
      del request.session['state']
      del request.session['destino']
      request.session.flush()
  except KeyError:
      pass
      state = "SE DESCONECTO DEL SISTEMA"
  form = DependenciasForm()      
  formd = []  
  print form,formd
  return render(request, 'index.html', {'formd':formd,'form':form,'state':state,})
  #return render(request, './index.html', {'formd':formd,'form':form,'state':state, 'destino': destino, 'changePass':changePass,'formpass':formpass})