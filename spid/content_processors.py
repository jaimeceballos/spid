# importamos los settings del proyecto
from django.conf import settings as _settings

def settings(request):
    # los devolvemos en la variable de contexto "settings"
    return {'settings': _settings}