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
