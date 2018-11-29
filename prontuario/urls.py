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

urlpatterns = [
    url(r'^$',home,name='prontuario'),
    url(r'^nuevo/$',nuevo_search,name='nuevo_prontuario'),
    url(r'^search_persona/$',search_persona,name='search_persona'),
    url(r'^search_detalle/(?P<sistema>[0-9A-Za-z]+)/(?P<id>[0-9A-Za-z]+)/$',search_detalle,name='detalle'),
    url(r'^search_procesales/(?P<id>[0-9A-Za-z]+)/(?P<dni>[0-9A-Za-z]+)/$',search_procesales,name='procesales'),
    url(r'^utilizar_prontuario/(?P<id>[0-9A-Za-z]+)/(?P<prontuario>[0-9A-Za-z]+)/$',utilizar_prontuario,name='utilizar_prontuario'),
    url(r'^cargar_nuevo/$',nuevo,name='cargar_nuevo'),
    url(r'^cargar_nuevo_procesales/(?P<prontuario>[0-9A-Za-z]+)/(?P<apellido>[A-Za-z]+)/(?P<nombre>[A-Za-z]+)/(?P<dni>[0-9A-Za-z]+)/$',nuevo_procesales,name='cargar_nuevo'),
    url(r'^cargar_nuevo_existe/(?P<id_detalle>[0-9A-Za-z]+)/$',nuevo_existe,name='cargar_nuevo_existe'),
    url(r'^nuevo_pais/(?P<tipo>[0-9A-Za-z]+)/$',nuevo_pais,name='nuevo_pais'),
    url(r'^nueva_ciudad/(?P<tipo>[0-9A-Za-z]+)/$',nueva_ciudad,name='nueva_ciudad'),
    url(r'^verificar_prontuario/(?P<n_p>[0-9A-Za-z]+)/$',verificar_prontuario,name='verificar_prontuario'),
    url(r'^nuevo/save/$',nuevo_save,name='nuevo_prontuario_save'),
    url(r'^identificacion/save/$',identificacion_save,name='identificacion_save'),
    url(r'^verificar/$',verificar,name='verificar'),
    url(r'^datos_verificar/(?P<id>[0-9A-Za-z]+)/$',datos_verificar,name='datos_verificar'),
    url(r'^cargar_padres/(?P<id>[0-9A-Za-z]+)/$',cargar_padres,name='cargar_padres'),
    url(r'^cargar_domicilios/(?P<id>[0-9A-Za-z]+)/$',cargar_domicilios,name='cargar_domicilios'),
    url(r'^cargar_fotos/(?P<id>[0-9A-Za-z]+)/$',cargar_fotos,name='cargar_fotos'),
    url(r'^verificar_existe/(?P<id>[0-9A-Za-z]+)/$',verificar_existe,name='verificar_existe'),
    url(r'^vincular/(?P<id>[0-9A-Za-z]+)/$',vincular,name='vincular'),
    url(r'^identificaciones_anteriores/(?P<id>[0-9A-Za-z]+)/$',identificaciones_anteriores,name='identificaciones_anteriores'),
    url(r'^obtener_identificacion/(?P<id>[0-9A-Za-z]+)/$',obtener_identificacion,name='obtener_identificacion'),
    url(r'^obtener_fotos/(?P<id>[0-9A-Za-z]+)/$',obtener_fotos,name='obtener_fotos'),
    url(r'^identificacion/(?P<id>[0-9A-Za-z]+)/$',identificacion,name='identificacion'),
    url(r'^resumen_persona/(?P<id>[0-9A-Za-z]+)/$',resumen_persona,name='resumen_persona'),
    url(r'^ver_identificacion/(?P<id>[0-9A-Za-z]+)/$',ver_identificacion,name='ver_identificacion'),
    url(r'^buscar/$',buscar,name='buscar'),
    url(r'^busqueda/$',busqueda,name='busqueda'),
    url(r'^obtener_miniatura/(?P<id>[0-9A-Za-z]+)/$',obtener_miniatura,name='obtener_miniatura'),
    url(r'^ver_prontuario/(?P<id>[0-9]+)/$',ver_prontuario,name='ver_prontuario'),
    url(r'^modificar_persona/(?P<id>[0-9]+)/$',modificar_persona,name='modificar_persona'),
    url(r'^persona_save/(?P<id>[0-9]+)/$',persona_save,name='persona_save'),
    url(r'^verificar_dni/(?P<id>[0-9]+)/(?P<dni>[0-9]+)/$',verificar_dni,name='verificar_dni'),
    url(r'^nuevo_elemento/(?P<tipo>[A-Za-z]+)/$',nuevo_elemento,name='nuevo_elemento'),
    url(r'^eliminar_historial/$',eliminar_historial,name='eliminar_historial'),
    url(r'^buscar_procesales/$',buscar_procesales,name='buscar_procesales'),
    url(r'^preventivos_persona/(?P<persona>[0-9]+)/$',preventivos_persona,name='preventivos_persona'),
    url(r'^imprimir_prontuario/(?P<prontuario>[0-9]+)/$',imprimir_prontuario,name='imprimir_prontuario'),
    url(r'^eliminar_domicilio/(?P<id>[0-9]+)/$',eliminar_domicilio,name='eliminar_domicilio'),
    url(r'^actividad/$',log,name='log'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
