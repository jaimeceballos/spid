#encoding:utf-8
from django.forms import ModelForm, TimeField
from django import forms
from datetime import datetime
from django.contrib import admin
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import  Group,Permission,User
from django.contrib.admin import widgets
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms.widgets import CheckboxSelectMultiple,RadioSelect
from prontuario.models import *
from preventivos.models import *
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.db.models import Q

TIPO_FOTOS_CHOICES = (
        ('1','FRENTE'),
        ('2','PERFIL DERECHO'),
        ('3','PERFIL IZQUIERDO'),
        ('4','CUERPO COMPLETO'),
        ('5','OTRO'),
)

class FotosPersonaForm(forms.ModelForm):
    tipo_foto = forms.ChoiceField(choices=TIPO_FOTOS_CHOICES)
    foto      = forms.ImageField()
    class Meta:
        model = FotosPersona
        exclude = ['persona',]

class RefOcupacionEspecificaForm(forms.ModelForm):
    descripcion = forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'Descripcion'})))

    class Meta:
        model = RefOcupacionEspecifica
        exclude = []

class Prontuario2Form(forms.Form):
    nro             = forms.CharField(required=False, widget=forms.TextInput(attrs=dict({'class':'form-control ','autocomplete':'off','placeholder':'Nro. Prontuario'})))
    apellidos       = forms.CharField(required=True, widget=forms.TextInput(attrs=dict({'class':'form-control ','autocomplete':'off','placeholder':'Apellidos'})))
    nombres         = forms.CharField(required=True, widget=forms.TextInput(attrs=dict({'class':'form-control ','autocomplete':'off','placeholder':'Nombres'})))
    fecha_nac       = forms.CharField(required = True, widget=forms.TextInput(attrs=dict({'class':'form-control  verifca','placeholder':'Fecha de nacimiento','style':'text-align: center;'})))
    tipo_doc        = forms.ModelChoiceField(queryset= RefTipoDocumento.objects.all())
    nro_doc         = forms.CharField(required=True, widget=forms.TextInput(attrs=dict({'class':'form-control ','autocomplete':'off','placeholder':'Nro. Documento'})))
    pais_nac_id     = forms.CharField(required = True, widget=forms.HiddenInput())
    ciudad_nac      = forms.CharField(required = True, widget=forms.TextInput(attrs=dict({'class':'form-control  verifca','placeholder':'ciudad','style':'text-align: center;'})))
    ciudad_nac_id   = forms.CharField(required = True, widget=forms.HiddenInput())
    sexo_id         = forms.ModelChoiceField(queryset= RefSexo.objects.all())
    estado_civil    = forms.ModelChoiceField(queryset= RefEstadosciv.objects.all())
    pais_res_id     = forms.CharField(required = True, widget=forms.HiddenInput())
    ciudad_res      = forms.CharField(required = True, widget=forms.TextInput(attrs=dict({'class':'form-control  verifca','placeholder':'ciudad','style':'text-align: center;'})))
    ciudad_res_id   = forms.CharField(required = True, widget=forms.HiddenInput())
    ocupacion       = forms.ModelChoiceField(queryset= RefOcupacion.objects.all())
    alias           = forms.CharField(required=False, widget=forms.TextInput(attrs=dict({'class':'form-control ','autocomplete':'off','placeholder':'Alias'})))
    observaciones   = forms.CharField(required=False, widget=forms.TextInput(attrs=dict({'class':'form-control ','autocomplete':'off','placeholder':'Motivo de la identificacion'})))

class ProntuarioForm(forms.ModelForm):

    class Meta:
        model = Prontuario
        exclude = ['persona','identificaciones']

class SearchForm(forms.Form):
    apellido                = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','autocomplete':'off','placeholder':'Apellido','style':'text-align: center;'})))
    nombre                  = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'nombre','style':'text-align: center;'})))
    documento               = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Numero Documento','style':'text-align: center;'})))
    fecha_nacimiento        = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Fecha de nacimiento','style':'text-align: center;','title':'Solo se puede Realizar busqueda de personas mayores de 18 años.'})))
    ciudad_nacimiento       = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Ciudad','style':'text-align: center;'})))
    ciudad_nacimiento_id    = forms.CharField(required = False, widget=forms.HiddenInput())
    pais_nacimiento         = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'pais','style':'text-align: center;'})))
    pais_nacimiento_id      = forms.CharField(required = False, widget=forms.HiddenInput())
    alias                   = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Alias','style':'text-align: center;'})))

class BuscarProcesalesForm(forms.Form):
    apellido                = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Apellido','style':'text-align: center;'})))
    nombre                  = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'nombre','style':'text-align: center;'})))
    documento               = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Numero Documento','style':'text-align: center;'})))

    def clean(self):

        cleaned_data = super(BuscarProcesalesForm,self).clean()
        if cleaned_data['apellido'] == "" and cleaned_data['nombre'] == "" and cleaned_data['documento'] == "":
            raise forms.ValidationError("Debe ingresar al menos un criterio de busqueda.")
        return cleaned_data




class BuscarForm(forms.Form):
    documento               = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Numero Documento','style':'text-align: center;'})))
    nombre                  = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Nombre','style':'text-align: center;'})))
    apellido                = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Apellido','style':'text-align: center;'})))
    ciudad_nacimiento       = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Nacido en:','style':'text-align: center;'})))
    ciudad_nacimiento_id    = forms.CharField(required = False, widget=forms.HiddenInput())
    ciudad_residencia       = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Vive en:','style':'text-align: center;'})))
    ciudad_residencia_id    = forms.CharField(required = False, widget=forms.HiddenInput())
    anio_nacimiento         = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifica', 'placeholder':'Año de Nacimiento','style':'text-align:center;'})))

class IdentificacionForm(forms.ModelForm):
    prontuario_local = forms.CharField(required=False,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'Registro Local','style':'text-align: center;'})))
    ocupacion_especifica = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'form-control'}), queryset= RefOcupacionEspecifica.objects.all()  )
    altura_metros = forms.IntegerField(required=True,widget = forms.TextInput(attrs=dict({'class':'form-control','placeholder':'Mts.','style':'text-align: center;'})))
    altura_centimetros = forms.IntegerField(required=True,widget = forms.TextInput(attrs=dict({'class':'form-control','placeholder':'Cms.','style':'text-align: center;'})))
    contextura = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'form-control'}), queryset= RefContextura.objects.all()  )
    cutis = forms.CharField(required=False,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'cutis','style':'text-align: center;'})))
    cabello_tipo = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'form-control'}), queryset= RefTipoCabello.objects.all()  )
    cabello_color = forms.CharField(required=False,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'Color','style':'text-align: center;'})))
    es_tenido = forms.BooleanField(required=False)
    posee_tatuajes = forms.BooleanField(required=False)
    posee_cicatrices = forms.BooleanField(required=False)
    observaciones = forms.CharField(required=False,widget=forms.Textarea(attrs=dict({'class':'form-control','placeholder':'Observaciones','style':'text-align: center;'})))

    class Meta:
        model = Identificacion
        exclude = ['persona','fecha_identificacion','dependencia_identificacion','fotos']


class ContexturaForm(forms.ModelForm):

    descripcion = forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'descripcion','required':'required'})))

    class Meta:
        model = RefContextura
        exclude = []

class OcupacionEspecificaForm(forms.ModelForm):

    descripcion = forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'descripcion','required':'required'})))

    class Meta:
        model = RefOcupacionEspecifica
        exclude = []
