from django.conf.urls import *
from django.contrib import admin
from repar.views import register
from django.contrib.auth.decorators import login_required
from repar import views
from repar import forms
from repar.forms import *
from repar.views import *
from django.conf import settings
handler404 = 'repar.views.page_not_found'
handler500 = 'repar.views.server_error' 


admin.autodiscover()

urlpatterns = patterns('',url(r'^repar/change/$', 'repar.views.passwordChange', name="changePass"),
	(r'^$', 'repar.views.iniciar'),
    (r'^inicio/$', 'repar.views.inicial'),
    (r'^login/$', 'repar.views.loguser'),
    (r'^new/$', 'repar.views.new_reg'),
    (r'^solicitud/$', 'repar.views.register'),
    (r'^contacto/$', 'repar.views.sugerir'),
    (r'^salir/$', 'repar.views.nologin'),
    (r'^tipoars/(?P<tipoar>[0-9A-Za-z]+)/$', 'repar.views.obtener_calibres'),
    (r'^marcas/(?P<marca>[0-9A-Za-z]+)/$', 'repar.views.obtener_modelos'),
    (r'^new/(?P<dnis>[0-9A-Za-z]+)/$', 'repar.views.obtener_nroprontuario'),
    #(r'^new/search/$', 'repar.views.search'),
    (r'^regis/(?P<id>[0-9A-Za-z]+)/$', 'repar.views.editarReg'),
    (r'^seek/(?P<id>[0-9A-Za-z]+)/$', 'repar.views.verdata'),
    (r'^resetpassword/$', 'django.contrib.auth.views.password_reset', 
    {'post_reset_redirect' : '../repar/','template_name' : 'registration/password_reset_form.html'}),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),

)

