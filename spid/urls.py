from django.conf.urls import *
from django.contrib import *
from spid.views import registro
from django.contrib.auth.decorators import login_required
from spid import views
from preventivos import views
from repar import views
from repar.forms import *
from preventivos.forms import *
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

handler404 = 'preventivos.views.page_not_found'
handler500 = 'preventivos.views.server_error'
admin.autodiscover()

urlpatterns = patterns('',  url(r'^spid/change/$', 'spid.views.passwordChange', name="changePass"),
    (r'^spid/$', 'spid.views.iniciar'),
    (r'^spid/depes/(?P<depes>[0-9A-Za-z]+)/$', 'spid.views.obtener_dependencias'),
    (r'^spid/login/$', 'spid.views.login_user'),
    (r'^solicitud/$', 'spid.views.registro'),
    (r'^contacto/$', 'spid.views.contactar'),
    (r'^password/$', 'django.contrib.auth.views.password_reset',
    {'post_reset_redirect' : '../repar/','template_name' : 'registro/password_reset_form.html'}),
    (r'^resetpassword/$', 'django.contrib.auth.views.password_reset',
    {'post_reset_redirect' : '../spid/','template_name' : 'registration/password_reset_form.html'}),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^spid/inicio/$', 'preventivos.views.inicial'),
    (r'^spid/manual/$', 'spid.views.some_view'),
    (r'^spid/help/$', 'spid.views.help_view'),
    (r'^spid/ayudaonline/$', 'spid.views.help_view'),
    (r'^spid/salir/$', 'spid.views.nologin'),
    (r'^admin/config/', include(admin.site.urls)),
    (r'^preventivos/', include('preventivos.urls')),
    url(r'^NIF/',include('NIF.urls')),
    url(r'^prontuario/',include('prontuario.urls')),
    url(r'^spid/dependencias_ajax/','spid.views.dependencias_ajax',name='dependencias_ajax'),
    (r'^repar/', include('repar.urls')),

 ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
