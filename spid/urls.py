from django.conf.urls import *
from django.contrib import admin
from spid.views import registro
from django.contrib.auth.decorators import login_required
from spid import views
from preventivos import views
from preventivos.forms import *
from django.conf import settings


handler404 = 'preventivos.views.page_not_found'
handler500 = 'preventivos.views.server_error' 

admin.autodiscover()

urlpatterns = patterns('',  url(r'^$', 'spid.views.passwordChange', name="changePass"),
    (r'^spid/$', 'spid.views.iniciar'),
    (r'^spid/depes/(?P<depes>[0-9A-Za-z]+)/$', 'spid.views.obtener_dependencias'),
    (r'^spid/login/$', 'spid.views.login_user'),
    (r'^solicitud/$', 'spid.views.registro'),
     (r'^contacto/$', 'spid.views.contactar'),
    (r'^resetpassword/$', 'django.contrib.auth.views.password_reset', 
    {'post_reset_redirect' : '../spid/','template_name' : 'registration/password_reset_form.html'}),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^spid/inicio/$', 'preventivos.views.inicial'),
    (r'^spid/manual/$', 'spid.views.some_view'),
    (r'^spid/inicio/$', 'preventivos.views.inicial'),
    (r'^spid/salir/$', 'spid.views.nologin'),
    (r'^admin/config/', include(admin.site.urls)),
    (r'^preventivos/', include('preventivos.urls')),
    (r'^','preventivos.views.page_not_found'),
 )
s.nlugares'),
    (r'^preventivos/ciudades/$','preventivos.views.ciudades'),
    (r'^preventivos/actuantes/ure/(?P<ure>[0-9A-Za-z]+)/$', 'preventivos.views.obtener_dependencias'),
    (r'^preventivos/user/ure/(?P<ure>[0-9A-Za-z]+)/$', 'preventivos.views.obtener_dependencias'),
    (r'^preventivos/ciudades/(?P<pais>[0-9A-Za-z]+)/$', 'preventivos.views.obtener_provincia'),
    (r'^preventivos/ciudades/editar/(?P<idciu>[0-9A-Za-z]+)/$', 'preventivos.views.ciudad'),
    (r'^preventivos/ciudades/dpto/(?P<prvi>[0-9A-Za-z]+)/$', 'preventivos.views.obtener_departa'),
    (r'^preventivos/paises/$', 'preventivos.views.pais'),
    (r'^preventivos/newpais/$', 'preventivos.views.npais'),
    (r'^preventivos/provincias/$', 'preventivos.views.provincias'),
    (r'^preventivos/departamentos/$','preventivos.views.departamentos'),
    (r'^preventivos/paises/(?P<idlista>[0-9A-Za-z]+)/$', 'preventivos.views.paise'),
    (r'^preventivos/provincias/(?P<idpcia>[0-9A-Za-z]+)/$', 'preventivos.views.provi'),
    (r'^preventivos/departamentos/(?P<iddepto>[0-9A-Za-z]+)/$', 'preventivos.views.depto'),
    (r'^preventivos/unidades/$', 'preventivos.views.unidades'),
    (r'^preventivos/unidades/(?P<idUnidad>[0-9A-Za-z]+)/$', 'preventivos.views.unidad'),
    (r'^preventivos/dependencias/$','preventivos.views.dependencias'),
    (r'^preventivos/dependencias/(?P<idDepe>[0-9A-Za-z]+)/$', 'preventivos.views.dependencia'),
    (r'^preventivos/peopleenv/$','preventivos.views.personasi'),
    (r'^preventivos/peopleenv/(?P<idple>[0-9A-Za-z]+)/$', 'preventivos.views.npersonasi'),
    (r'^preventivos/typedelitos/$', 'preventivos.views.tipodelitos'),
    (r'^preventivos/typedelitos/(?P<idtipo>[0-9A-Za-z]+)/$', 'preventivos.views.tipodelito'),
    (r'^preventivos/delitos/$', 'preventivos.views.delitos'),
    (r'^preventivos/delitos/(?P<idelito>[0-9A-Za-z]+)/$', 'preventivos.views.delito'),
    (r'^spid/inicio/$', 'preventivos.views.inicial'),
    (r'^preventivos/jobs/$', 'preventivos.views.jobs'),
    (r'^preventivos/jobs/(?P<idjob>[0-9A-Za-z]+)/$', 'preventivos.views.jobselected'),
    (r'^preventivos/items/$', 'preventivos.views.rubros'),
    (r'^preventivos/items/(?P<idrub>[0-9A-Za-z]+)/$', 'preventivos.views.itemselec'),
    (r'^preventivos/category/$', 'preventivos.views.categorias'),
    (r'^preventivos/category/(?P<idcat>[0-9A-Za-z]+)/$', 'preventivos.views.catselect'),
    (r'^preventivos/newrubro/$', 'preventivos.views.nrubros'),
    (r'^preventivos/barrios/$', 'preventivos.views.barrios'),
    (r'^preventivos/barrios/(?P<idbar>[0-9A-Za-z]+)/$', 'preventivos.views.nbarrios'),
    #(r'^preventivos/barrios/ids/(?P<idci>[0-9A-Za-z]+)/$', 'preventivos.views.obtener_calles'),
    (r'^preventivos/address/$', 'preventivos.views.calles'),
    (r'^preventivos/address/(?P<idadrs>[0-9A-Za-z]+)/$', 'preventivos.views.ncalles'),
    (r'^preventivos/authorities/$', 'preventivos.views.autoridades'),
    (r'^preventivos/authorities/(?P<idaut>[0-9A-Za-z]+)/$', 'preventivos.views.autoridad'),
  # (r'^preventivos/manual/$', 'preventivos.views.descarga'),
    (r'^preventivos/actuantes/$', 'preventivos.views.actuantes'),
    (r'^preventivos/actuantes/(?P<idact>[0-9A-Za-z]+)/$','preventivos.views.oficiales'),
    (r'^preventivos/user/(?P<iduser>[0-9A-Za-z]+)/$','preventivos.views.usuarios'),
    (r'^spid/inicio/$', 'preventivos.views.inicial'),
    (r'^spid/salir/$', 'spid.views.nologin'),
    (r'^admin/', include(admin.site.urls)),
    (r'^preventivos/groupusers/$', 'preventivos.views.grupos'),
    (r'^preventivos/newgroup/$', 'preventivos.views.ngrupos'),
    (r'^preventivos/groupusers/(?P<idgr>[0-9A-Za-z]+)/$', 'preventivos.views.grupusers'),
    (r'^preventivos/persona/$', 'preventivos.views.personas'),
    (r'^preventivos/persona/ver/(?P<idper>[0-9A-Za-z]+)/$', 'preventivos.views.persona'),
    (r'^preventivos/persona/(?P<pais>[0-9A-Za-z]+)/$', 'preventivos.views.obtener_ciudades'),
    (r'^preventivos/nuevo/$',PreventivoWizard.as_view([("caratula", PreventivoForm1),
        ("preventor_actuante", PreventivoForm2),
        ("autoridades_inf", PreventivoForm3),("confirmacion",PreventivoForm)])),
  
 )