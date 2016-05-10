from django.conf.urls import include, url
from .views import *

urlpatterns = [
    url(r'^$',home_nif,name='home_nif'),
]
