from preventivos.models import *
from django.contrib.auth.models import Group,Permission,User
from django.contrib import admin

admin.autodiscover()(admin.ModelAdmin):
    list_display = ('id','descripcion',)
    list_filter  = ('descripcion',)
    search_fields = ('descripcion',)

class RefProvinciaAdmin(admin.ModelAdmin):
    list_display = ('id','descripcion','pais',)
    list_filter  = ('descripcion',)
    search_fields = ('pais',)
    raw_id_fields = ('pais',)
# 
#admin.site.register(RefCiudades)

#admin.site.register(RefPaises,RefPaisesAdmin)
#admin.site.register(RefProvincia,RefProvinciaAdmin)
