from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^$',home_nif,name='home_nif'),
    url(r'^generar/$',generar_codigos,name='generar'),
    url(r'^descargar/$',descargar_codigos,name='descargar'),
]
