from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from preventivos import views
from preventivos import forms
from preventivos.forms import *
from prontuario.views import *
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'preventivos.views.page_not_found'

urlpatterns = patterns('',
    url(r'^$','prontuario.views.home',name='prontuario'),
    url(r'^nuevo/$','prontuario.views.nuevo_search',name='nuevo_prontuario'),
    url(r'^search_persona/$','prontuario.views.search_persona',name='search_persona'),
    url(r'^search_detalle/(?P<sistema>[0-9A-Za-z]+)/(?P<id>[0-9A-Za-z]+)/$','prontuario.views.search_detalle',name='detalle'),
    url(r'^search_procesales/(?P<id>[0-9A-Za-z]+)/(?P<dni>[0-9A-Za-z]+)/$','prontuario.views.search_procesales',name='procesales'),
    url(r'^utilizar_prontuario/(?P<id>[0-9A-Za-z]+)/(?P<prontuario>[0-9A-Za-z]+)/$','prontuario.views.utilizar_prontuario',name='utilizar_prontuario'),
    url(r'^cargar_nuevo/$','prontuario.views.nuevo',name='cargar_nuevo'),
    url(r'^cargar_nuevo_existe/(?P<id_detalle>[0-9A-Za-z]+)/$','prontuario.views.nuevo_existe',name='cargar_nuevo_existe'),
    url(r'^nuevo_pais/(?P<tipo>[0-9A-Za-z]+)/$','prontuario.views.nuevo_pais',name='nuevo_pais'),
    url(r'^nueva_ciudad/(?P<tipo>[0-9A-Za-z]+)/(?P<pais>[0-9A-Za-z]+)/$','prontuario.views.nueva_ciudad',name='nueva_ciudad'),
    url(r'^verificar_prontuario/(?P<n_p>[0-9A-Za-z]+)/$','prontuario.views.verificar_prontuario',name='verificar_prontuario'),
    url(r'^nuevo/save/$','prontuario.views.nuevo_save',name='nuevo_prontuario_save'),
    url(r'^identificacion/save/$','prontuario.views.identificacion_save',name='identificacion_save'),
    url(r'^verificar/$','prontuario.views.verificar',name='verificar'),
    url(r'^datos_verificar/(?P<id>[0-9A-Za-z]+)/$','prontuario.views.datos_verificar',name='datos_verificar'),
    url(r'^cargar_padres/(?P<id>[0-9A-Za-z]+)/$','prontuario.views.cargar_padres',name='cargar_padres'),
    url(r'^cargar_domicilios/(?P<id>[0-9A-Za-z]+)/$','prontuario.views.cargar_domicilios',name='cargar_domicilios'),
    url(r'^cargar_fotos/(?P<id>[0-9A-Za-z]+)/$','prontuario.views.cargar_fotos',name='cargar_fotos'),
    url(r'^verificar_existe/(?P<id>[0-9A-Za-z]+)/$','prontuario.views.verificar_existe',name='verificar_existe'),
    url(r'^vincular/(?P<id>[0-9A-Za-z]+)/$','prontuario.views.vincular',name='vincular'),
    url(r'^identificaciones_anteriores/(?P<id>[0-9A-Za-z]+)/$','prontuario.views.identificaciones_anteriores',name='identificaciones_anteriores'),
    url(r'^obtener_identificacion/(?P<id>[0-9A-Za-z]+)/$','prontuario.views.obtener_identificacion',name='obtener_identificacion'),
    url(r'^obtener_fotos/(?P<id>[0-9A-Za-z]+)/$','prontuario.views.obtener_fotos',name='obtener_fotos'),
    url(r'^identificacion/(?P<id>[0-9A-Za-z]+)/$','prontuario.views.identificacion',name='identificacion'),
    url(r'^ver_identificacion/(?P<id>[0-9A-Za-z]+)/$','prontuario.views.ver_identificacion',name='ver_identificacion'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
