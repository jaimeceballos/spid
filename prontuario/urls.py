from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from preventivos import views
from preventivos import forms
from preventivos.forms import *
from prontuario.views import *
from django.conf import settings

handler404 = 'preventivos.views.page_not_found'

urlpatterns = patterns('',
    url(r'^$','prontuario.views.home',name='prontuario'),
    url(r'^nuevo/$','prontuario.views.nuevo_search',name='nuevo_prontuario'),
    url(r'^search_persona/$','prontuario.views.search_persona',name='search_persona'),

)
