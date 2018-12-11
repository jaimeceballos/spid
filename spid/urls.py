from django.conf.urls import *
from django.contrib import *
from spid.views import registro
from django.contrib.auth.decorators import login_required
from spid.views import *
from preventivos.views import inicial
#from repar import views
from repar.forms import *
from preventivos.forms import *
from django.contrib.auth.views import password_reset, password_reset_complete, password_reset_confirm
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

handler404 = 'preventivos.views.page_not_found'
handler500 = 'preventivos.views.server_error'
admin.autodiscover()

urlpatterns = [
    url(r'^spid/change/(?P<id>[0-9A-Za-z]+)/$', passwordChange, name="changePass"),
    url(r'^spid/$', iniciar),
    url(r'^spid/depes/(?P<depes>[0-9A-Za-z]+)/$', obtener_dependencias),
    url(r'^spid/login/$', login_user),
    url(r'^solicitud/$', registro),
    url(r'^contacto/$', contactar),
    url(r'^password/$', password_reset,{'post_reset_redirect' : '../repar/','template_name' : 'registro/password_reset_form.html'}),
    url(r'^resetpassword/$', password_reset,{'post_reset_redirect' : '../spid/','template_name' : 'registration/password_reset_form.html'}),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm),
    url(r'^reset/done/$', password_reset_complete),
    url(r'^spid/inicio/$', inicial),
    url(r'^spid/manual/$', some_view),
    url(r'^spid/help/$', help_view),
    url(r'^spid/ayudaonline/$', help_view),
    url(r'^spid/salir/$', nologin),
    url(r'^admin/config/', admin.site.urls),
    url(r'^preventivos/', include('preventivos.urls')),
    #url(r'^NIF/',include('NIF.urls')),
    url(r'^prontuario/',include('prontuario.urls')),
    url(r'^spid/dependencias_ajax/',dependencias_ajax,name='dependencias_ajax'),
    url(r'^spid/primer_ingreso/(?P<id>[0-9A-Za-z]+)/$',primer_ingreso,name='primer_ingreso'),
    url(r'^repar/', include('repar.urls')),

 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
