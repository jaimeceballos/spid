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
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.db.models import Q


class RefOcupacionEspecificaForm(forms.ModelForm):
    descripcion = forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'Descripcion'})))

    class Meta:
        model = RefOcupacionEspecifica

class ProntuarioForm(forms.ModelForm):

    class Meta:
        model = Prontuario

class SearchForm(forms.Form):
    apellido                = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Apellido','style':'text-align: center;'})))
    nombre                  = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'nombre','style':'text-align: center;'})))
    documento               = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Numero Documento','style':'text-align: center;'})))
    fecha_nacimiento        = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Fecha de nacimiento','style':'text-align: center;','title':'Solo se puede Realizar busqueda de personas mayores de 18 años.'})))
    ciudad_nacimiento       = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Ciudad','style':'text-align: center;'})))
    ciudad_nacimiento_id    = forms.CharField(required = False, widget=forms.HiddenInput())
    pais_nacimiento         = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'pais','style':'text-align: center;'})))
    pais_nacimiento_id      = forms.CharField(required = False, widget=forms.HiddenInput())
    alias                   = forms.CharField(required = False, widget=forms.TextInput(attrs=dict({'class':'form-control input-lg verifca','placeholder':'Alias','style':'text-align: center;'})))
