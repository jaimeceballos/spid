#encoding:utf-8
from repar.models import *
from repar.forms import *
from spid.forms import LoginForm
from django.template.context_processors import csrf
from django.template import Context, Template, RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, render_to_response,get_object_or_404
from django.core import serializers
import json as simplejson
from django.contrib.auth import authenticate, login
from decorators.auth import group_required
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.contrib import auth,messages
from django.http import Http404
from django.contrib.auth.models import Group,Permission,User
import sys, os
from datetime import date,datetime
from django.utils.dateparse import parse_datetime
import random,datetime,time
from django.contrib.auth.decorators import login_required
from django.utils.encoding import smart_text
from django.contrib.auth import logout
from io import BytesIO
from django.utils.encoding import smart_bytes, smart_text
#from reportlab.pdfgen import canvas
from django.db.models.signals  import  post_save,post_delete
from django.http import HttpResponse
from django.template import Context, loader
from django.forms.utils import ErrorList
from preventivos.models import *
from preventivos.forms import *
from django.db import connections
from collections import namedtuple

def page_not_found(request):
  state= request.session.get('state')
  destino= request.session.get('destino')
  return render(request,'./error404.html',{'state':state, 'destino': destino})

def server_error(request):
 return render(request, './500.html')

@login_required
def obtener_calibres(request,tipoar):
        data = request.POST
        calibres = RefCalibres.objects.filter(tipoar_id = tipoar)
        data = serializers.serialize("json", calibres)
        return HttpResponse(data, mimetype='application/json')

@login_required
def obtener_modelos(request,marca):
        data = request.POST
        modelos = RefModArmas.objects.filter(trademark_id = marca)
        data = serializers.serialize("json", modelos)
        return HttpResponse(data, mimetype='application/json')

def iniciar(request):
    state = ''
    name=''
    username = password = ''
    formd = []
    return render(request, './loginRepar.html', {'formd':formd,'state':state})

@login_required
def inicial(request):
  ciudades = ""
  state= request.session.get('state')
  destino= request.session.get('destino')

  return render(request,'repar.html',{'state':state, 'destino': destino})

#la funcion en donde se guardan los grupos de usuarios que son ingresados en usuarios

def loguser(request):
    state = ''
    name=''
    username = password = ''
    destino = ''
    changePass = ''
    birthday=False
    #form = DependenciasForm()
    form=''
    formpass = CambiarPassForm()

    if request.POST.get('username')=='':
         formj = ActuantesForm()
         return render(request, 'contactar.html', {'state':state,'formj':formj})
    else:
        if request.POST.get('logonea')=='Conectar':

         username = request.POST.get('username')
         password = request.POST.get('password')

         ultimo_ingreso = User.objects.get(username = username).last_login
         profile = User.objects.get(username=username).userprofile
         profile.ultimo_ingreso = ultimo_ingreso
         profile.save()
         if username.isdigit():
          user = auth.authenticate(username=username, password=password)
          if user is not None:

           if Personas.objects.get(nro_doc=username).fecha_nac.day == date.today().day and Personas.objects.get(nro_doc=username).fecha_nac.month == date.today().month:
              birthday = True




         user = auth.authenticate(username=username, password=password)
         if user is not None:
            if user.is_active:
                #fecha_login=datetime.datetime.strftime(user.last_login, "%Y-%m-%d %H:%M:%S")
                #fecha_joined=datetime.datetime.strftime(user.date_joined, "%Y-%m-%d %H:%M:%S")
                #print type(datetime.datetime.strptime(fecha_login, "%Y-%m-%d %H:%M:%S")),fecha_login,fecha_joined
                #if datetime.datetime.strptime(fecha_login, "%Y-%m-%d %H:%M:%S")!=datetime.datetime.strptime(fecha_joined, "%Y-%m-%d %H:%M:%S"):
                if user.userprofile.last_login:
                   changePass = 'si'

                auth.login(request, user)
                userp=user.userprofile
                profiles = user.userprofile
                uregs=profiles.ureg
                depes=profiles.depe


                gr=user.groups.values_list('name', flat=True)

                for varios in gr:
                  if 'admi' in varios or 'repar' in varios:
                    state = str(Group.objects.get(name=varios))

                if 'administrador' in state or 'repar' in state:
                    state = str(Group.objects.get(name=varios))
                    request.session['state']=state
                    destino='Jefatura - Repar'
                    request.session['destino']=destino
                else:
                   state="Usuario no Autorizado"
                   return render(request, 'login.html', {'state':state,'form':form})

            else:
              state="Usuario no Autorizado"
              return render(request, 'login.html', {'state':state,'form':form})
         return render(request, './repar.html', {'form':form,'state':state, 'destino': destino,'changePass':changePass,'formpass':formpass,'birthday':birthday,'ultimo_ingreso':ultimo_ingreso})

        else:
            return render(request, 'login.html', {'name':name,'form':form})



def nologin(request):
    logout(request)
    try:
        del request.session['state']
        del request.session['destino']
        request.session.flush()
    except KeyError:
        pass
        state = "SE DESCONECTO DEL SISTEMA"

    formd = []
    return render(request, 'login.html', {'formd':formd,'state':state})

def passwordChange(request):
  formpass = CambiarPassForm(request.POST)
  changePass = 'si'

  state = request.session['state']
  destino = request.session['destino']
  form = ''
  #DependenciasForm()

  user = User.objects.get(username=request.user)
  #if formpass.is_valid():
  pass1 = request.POST.get('pass1')

  if pass1:
     user.date_joined=datetime.datetime.now()
     user.set_password(pass1)
     user.save()
     profiles = user.userprofile
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
  #form = DependenciasForm()
  formd = []
  #print form,formd
  return render(request, 'loginRepar.html', {'formd':formd,'form':form,'state':state,})
  #return render(request, './index.html', {'formd':formd,'form':form,'state':state, 'destino': destino, 'changePass':changePass,'formpass':formpass})

def register(request):
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
           subject, from_email, to = 'Solicitud de Usuario - Repar' ,request.POST.get('mail'), 'fydsoftware@gmail.com'
           text_content = "Solicitud recibida de : %s<br><br>Nro de Dni : %s<br><br>Jerarquia : %s<br><br>Destino actual : %s<br><br> Usuarios <br><br> %s <br><br>" % (request.POST.get('name'),str(request.POST.get('docu')),jerarca,request.POST.get('destino'),request.POST.get('comment'))
           msg = EmailMultiAlternatives(subject,text_content,from_email, [to])
           msg.attach_alternative(text_content,'text/html')
           try:
               msg.send(fail_silently=True)
           except IndexError:
               pass


           cabecera = '<br><br><br>'+'Al Sr/a'+'<br>'+'ADMINISTRADOR SIREGAR'+'<br>'+'Div. Desarrollo Informático'+'<br>'+'S_____________/_______________D'+'<br><br>'
           cuerpos='Por medio de la presente, me dirijo a UD. con el fin de solicitar el ALTA de usuarios al Sistema Registración de Armas'
           usuas='Lista del Personal A/C: '+str(jerarca)+' - '+str(request.POST.get('destino'))+'<br><br>'+str(request.POST.get('comment'))+'<br><br><br><br><br><br>'
           saludo='Sin más que agregar, aprovecho la ocasión para saludarlo muy atentamente.'+'<br><br><br><br><br><br><br><br><br><br>'
           datos.append(cabecera)
           for i in datos:
             soli=soli+i

           return  render(request,'solicitaUser.html',{'name':soli,'today':today,'cuerpos':cuerpos,'usuas':usuas,'saludo':saludo,})
    else:
       formj = ActuantesForm()

       return render(request, 'contactar.html',  {'name':name,'formj':formj})

def sugerir(request):
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
              #direcciones.append('jaimeceballos82@gmail.com')

           for cantdir in direcciones:

             try:
               msg = EmailMultiAlternatives(subject,text_content,from_email, [cantdir])
               msg.attach_alternative(text_content,'text/html')
               msg.send(fail_silently=True)
             except IndexError:
               pass
           """
           cabecera = '<br><br><br>'+'Al Sr :............................'+'<br>'+'ADMINISTRADOR SIREGAR'+'<br>'+'Div. Desarrollo Informático'+'<br>'+'S____________/_____________D'+'<br><br>'
           cuerpos='Por medio de la presente, me dirijo a UD. con el fin de solicitar el ALTA de usuarios al Sistema SIREGAR'
           usuas='Lista del Personal A/C: '+str(request.POST.get('jerarca'))+' - '+str(request.POST.get('destino'))+'<br><br>'+str(request.POST.get('comment'))+'<br><br><br><br><br><br>'
           saludo='Sin más que agregar, aprovecho la ocasión para saludarlo muy atentamente.'+'<br><br><br><br><br><br><br><br><br><br>'
           datos.append(cabecera)
           for i in datos:
             soli=soli+i

           return  render(request,'solicitaUser.html',{'name':soli,'today':today,'cuerpos':cuerpos,'usuas':usuas,'saludo':saludo,})"""
           return render(request,'solicitaUser.html',  {'name':name})
    else:
       return render(request, 'sugiere.html',  {'name':name})

@login_required
@group_required(["repar"])
def new_reg(request):
  errors=[]
  state= request.session.get('state')
  destino= request.session.get('destino')
  modelos=''
  clean=False
  result=''
  formrep = RepardataForm()
  formr = Repardata.objects.all()
  form = RefModArmasForm()
  lista = Repardata.objects.all()
  formark = TrademarkForm()
  #n_c='ROSAS%'
  #datos=myconsul(n_c)
  #print (datos)
  if request.POST.get('grabarm')=="Grabar":
        formark=TrademarkForm(request.POST, request.FILES)
        form=RefModArmas()
        descripcion = request.POST.get('descripcionm')
        trademark=request.POST.get('trademark')

        if descripcion!='' and trademark!='':
            form.descripcion=descripcion
            form.trademark_id=trademark
            try:
              form.save()
            except DatabaseError:
              return HttpResponseRedirect('.')

            formrep = RepardataForm(request.POST)
            formrep.fields['modelo'].queryset = RefModArmas.objects.filter(trademark=request.POST.get('marca'))
            form = RefModArmasForm()
            lista = Repardata.objects.all()
            formark = TrademarkForm()

            values={'formark':formark,'form':form,'formrep':formrep,'clean':clean,'errors': errors,'lista':lista,'state':state, 'destino': destino,'modelos':modelos}
            return render_to_response('new_reg.html',values,context_instance=RequestContext(request))
  else:
    if request.POST.get('grabarepar')=="Guardar":
        formrep=RepardataForm(request.POST, request.FILES)
        rep=Repardata()

        if formrep.errors.has_key('__all__'):
           clean=True
        if formrep.is_valid():

          rep.tipoar = formrep.cleaned_data['tipoar']
          rep.calibre = formrep.cleaned_data['calibre']
          rep.marca = formrep.cleaned_data['marca']
          rep.modelo = formrep.cleaned_data['modelo']
          rep.nro_arma = formrep.cleaned_data['nro_arma']
          rep.apellidos_pro = formrep.cleaned_data['apellidos_pro'].upper()
          rep.nombres_pro = formrep.cleaned_data['nombres_pro'].upper()
          rep.domicilio_pro = formrep.cleaned_data['domicilio_pro'].upper()
          rep.tipodoc = formrep.cleaned_data['tipodoc']
          rep.nrodoc_pro = formrep.cleaned_data['nrodoc_pro']
          rep.nro_prontuario = formrep.cleaned_data['nro_prontuario']
          rep.seccion = formrep.cleaned_data['seccion']
          rep.observaciones = formrep.cleaned_data['observaciones']
          numeracion= Repardata.objects.filter(anio__exact=date.today().year).values('nro')
          if len(numeracion)==0:
             nro=1
          else:
             nro=numeracion[len(numeracion)-1]['nro']+1

          rep.fecha_reg=datetime.datetime.now()
          rep.nro=nro
          rep.anio=date.today().year
          try:
           rep.save()
          except KeyError:
           clean=True

        errors = formrep.errors
        formrep = RepardataForm()
        form = RefModArmasForm()
        lista = Repardata.objects.all()
        formark = TrademarkForm()
        values={'formark':formark,'form':form,'formrep':formrep,'clean':clean,'errors': errors,'lista':lista,'state':state, 'destino': destino,'modelos':modelos}
        return render_to_response('new_reg.html',values,context_instance=RequestContext(request))


  return render_to_response('new_reg.html', {'result':result,'formark':formark,'form':form,'formrep':formrep,'clean':clean,'errors': errors,'lista':lista,'state':state, 'destino': destino,'modelos':modelos},context_instance=RequestContext(request))

def myconsul(self):
    cursor = connections['prontuario'].cursor()
    #print("select n_c,dni,n_p from indice.indice where n_c like %s",[self])
    dicto={}
    elementos=[]
    #try:
    #cursor.execute("select n_c,dni,tipo_p,n_p from indice.indice where n_c like %s",[self] )
    curso = Indice.objects.using('prontuario').get(dni='14282289')
    #print (curso.n_c)
    #for row in cursor:
    dicto={'Apellidos y Nombres :':curso.n_c,'Nro Documento :':curso.dni,'Seccion :':curso.tipo_p,'Nro Prontuario :':curso.n_p}
    #elementos.append(dicto)
    #finally:
    #cursor.close()
    return dicto

@login_required
@group_required(['repar'])
def obtener_nroprontuario(request,dnis):
    data = request.POST
    cursor = connections['prontuario'].cursor()
    dicto=''
    curso=''
    curso = Indice.objects.using('prontuario').filter(dni__contains=dnis)
    if curso:
       indice_fields = (
        'n_c',
        'tipo_p',
        'n_p'
        )
    data = serializers.serialize('json', curso)

    cursor.close()

    return HttpResponse(data, mimetype='application/json')


@login_required
@group_required(['repar'])
def editarReg(request, id):
  errors=[]
  state= request.session.get('state')
  destino= request.session.get('destino')
  modelos=''
  clean=False
  cleana=False
  result=''
  historial=''
  if request.method=='POST':
      result = Repardata.objects.get(id=id)
      formrep=RepardataForm(request.POST)

      if formrep.errors.has_key('__all__'):
           clean=True

      if formrep.is_valid():

         result.tipoar = formrep.cleaned_data['tipoar']
         result.calibre = formrep.cleaned_data['calibre']
         result.marca = formrep.cleaned_data['marca']
         result.modelo = formrep.cleaned_data['modelo']
         result.nro_arma = formrep.cleaned_data['nro_arma']
         result.apellidos_pro = formrep.cleaned_data['apellidos_pro'].upper()
         result.nombres_pro = formrep.cleaned_data['nombres_pro'].upper()
         result.domicilio_pro = formrep.cleaned_data['domicilio_pro'].upper()
         result.tipodoc = formrep.cleaned_data['tipodoc']
         result.nrodoc_pro = formrep.cleaned_data['nrodoc_pro']
         result.nro_prontuario = formrep.cleaned_data['nro_prontuario']
         result.seccion = formrep.cleaned_data['seccion']
         result.observaciones = formrep.cleaned_data['observaciones']
      else:
         result.calibre = formrep.cleaned_data['calibre']
         result.modelo = formrep.cleaned_data['modelo']
         result.apellidos_pro = formrep.cleaned_data['apellidos_pro'].upper()
         result.nombres_pro = formrep.cleaned_data['nombres_pro'].upper()
         result.domicilio_pro = formrep.cleaned_data['domicilio_pro'].upper()
         result.tipodoc = formrep.cleaned_data['tipodoc']
         result.nro_prontuario = formrep.cleaned_data['nro_prontuario']
         result.seccion = formrep.cleaned_data['seccion']
         result.observaciones = formrep.cleaned_data['observaciones']

      result.save()


      errors = formrep.errors
      formrep = RepardataForm()
      form = RefModArmasForm()
      lista = Repardata.objects.all()
      formark = TrademarkForm()
      values={'historial':historial,'clean':clean,'result':result,'formark':formark,'form':form,'formrep':formrep,'cleana':cleana,'errors': errors,'lista':lista,'state':state, 'destino': destino,'modelos':modelos}
      return render_to_response('new_reg.html',values,context_instance=RequestContext(request))

  else:
      result = Repardata.objects.get(id=id)
      formrep = RepardataForm(instance=result)

  form = RefModArmasForm()
  formrep.fields['calibre'].queryset=RefCalibres.objects.filter(tipoar=result.tipoar_id)
  formrep.fields['calibre'].initial=result.calibre
  formrep.fields['modelo'].queryset=RefModArmas.objects.filter(trademark=result.marca_id)
  formrep.fields['modelo'].initial=result.modelo
  lista = Repardata.objects.all()
  formark = TrademarkForm()
  values={'historial':historial,'result':result,'formark':formark,'form':form,'formrep':formrep,'clean':clean,'errors': errors,'lista':lista,'state':state, 'destino': destino,'modelos':modelos}
  return render_to_response('new_reg.html',values,context_instance=RequestContext(request))


@login_required
@group_required(["repar"])
def verdata(request,id):
  errors=[]
  state= request.session.get('state')
  destino= request.session.get('destino')
  modelos=''
  clean=False
  formrep = RepardataForm()
  formr = Repardata.objects.all()
  form = RefModArmasForm()
  lista = Repardata.objects.all()
  formark = TrademarkForm()
  formt = HistoryreparForm()
  result=''
  historial = ''
  if (id!='0'):
    result = Repardata.objects.get(id=id)
    if result.fecha_transf:
      historial = Repardata.objects.get(id=id).movis.all()

    formrep = RepardataForm(instance=result)
    formt = HistoryreparForm()
    if request.POST.get('grabart')=="Grabar":
       result = Repardata.objects.get(id=id)
       formrep=RepardataForm(request.POST)
       history = Historyrepar()
       formt = HistoryreparForm(request.POST,request.FILES)


       if formt.is_valid():
         #genero un registro en historyrepar
         history.apellidos_pro = result.apellidos_pro.upper()
         history.nombres_pro = result.nombres_pro.upper()
         history.domicilio_pro = result.domicilio_pro.upper()
         history.tipodoc = result.tipodoc
         history.nrodoc_pro = result.nrodoc_pro
         history.observaciones = result.observaciones
         history.fechamov=datetime.datetime.now()
         history.reparid=result
         history.save()
         result.apellidos_pro = formt.cleaned_data['apellidos_pro'].upper()
         result.nombres_pro = formt.cleaned_data['nombres_pro'].upper()
         result.domicilio_pro = formt.cleaned_data['domicilio_pro'].upper()
         result.tipodoc = formt.cleaned_data['tipodoc']
         result.nrodoc_pro = formt.cleaned_data['nrodoc_pro']
         result.id_prontuario = request.POST.get('prontuario')
         result.seccion = request.POST.get('seccion')
         result.observaciones = formt.cleaned_data['observaciones']
         result.fecha_transf = datetime.datetime.now()
         result.save()


  return render_to_response('verdatos.html', {'historial':historial,'formt':formt,'result':result,'formark':formark,'form':form,'formrep':formrep,'clean':clean,'errors': errors,'lista':lista,'state':state, 'destino': destino,'modelos':modelos},context_instance=RequestContext(request))
