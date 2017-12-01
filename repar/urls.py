from django.conf.urls import *
from django.contrib import admin
from repar.views import register
from django.contrib.auth.decorators import login_required
from repar import views
from repar import forms
from repar.forms import *
from repar.views import *
from django.conf import settings
from django.contrib.auth.views import password_reset_confirm, password_reset_complete
handler404 = 'repar.views.page_not_found'
handler500 = 'repar.views.server_error'


admin.autodiscover()

urlpatterns = [
    url(r'^repar/change/$', passwordChange, name="changePassR"),
	url(r'^$', iniciar),
    url(r'^inicio/$', inicial),
    url(r'^login/$', loguser),
    url(r'^new/$', new_reg),
    url(r'^solicitud/$', register),
    url(r'^contacto/$', sugerir),
    url(r'^salir/$', nologin),
    url(r'^tipoars/(?P<tipoar>[0-9A-Za-z]+)/$', obtener_calibres),
    url(r'^marcas/(?P<marca>[0-9A-Za-z]+)/$', obtener_modelos),
    url(r'^new/(?P<dnis>[0-9A-Za-z]+)/$', obtener_nroprontuario),
    #url(r'^new/search/$', 'repar.views.search'),
    url(r'^regis/(?P<id>[0-9A-Za-z]+)/$', editarReg),
    url(r'^seek/(?P<id>[0-9A-Za-z]+)/$', verdata),

    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm),
    url(r'^reset/done/$', password_reset_complete),
]
