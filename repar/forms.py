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
from repar.models import *
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.widgets import TextInput
from django.db.models import Q

Doc_opciones=(
    ('1','DNI'),
    ('2','LC'),
    ('3','LE'),
    ('4','CI'),
    ('5','PAS'),
    ('6','NO POSEE'),
    ('7','CUIT'),
    ('8','CUIL'),
    )
class RepardataForm(forms.ModelForm):
    apellidos_pro = forms.CharField(widget=forms.TextInput(attrs=dict({'class':'form-control','size': 100,'autocomplete':'off','placeholder':'Apellidos/Propietario'})))
    nombres_pro = forms.CharField(widget=forms.TextInput(attrs=dict({'class':'form-control','size': 100,'autocomplete':'off','placeholder':'Nombres/Propietario'})))
    domicilio_pro = forms.CharField(required=False,widget=forms.TextInput(attrs=dict({'class':'form-control','autocomplete':'off','placeholder':'Domicilio actual'})))
    nrodoc_pro = forms.IntegerField(max_value=99999999,widget=TextInput(attrs=dict({'class':'form-control','size': 6}))) 
    nro_arma = forms.CharField(widget=TextInput(attrs=dict({'class':'form-control','size':150}))) 
    nro_prontuario = forms.CharField(required=False,widget=forms.TextInput(attrs=dict({'class':'form-control','autocomplete':'off'})))
    seccion = forms.CharField(required=False,widget=forms.TextInput(attrs=dict({'class':'form-control','autocomplete':'off'})))    
    observaciones = forms.CharField(required=False,max_length=2000,widget=forms.Textarea(attrs=dict({'class':'form-control','rows':3,'col':80})))
    marca=forms.ModelChoiceField(widget = forms.Select(attrs={'class':'form-control' }), queryset= RefTrademark.objects.filter(codidar__exact=9))
    nro = forms.IntegerField(required=False,validators=[MinValueValidator(1),MaxValueValidator(99999)])
    anio = forms.IntegerField(required=False,validators=[MinValueValidator(2016),MaxValueValidator(2025)])
    fecha_transf=forms.DateTimeField(required=False)
    fecha_reg=forms.DateTimeField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(RepardataForm,self).__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super(RepardataForm, self).clean()
        nro_arma = cleaned_data.get("nro_arma")
        nrodoc_pro = cleaned_data.get("nrodoc_pro")
        tipoar= cleaned_data.get("tipoar")
        marca = cleaned_data.get("marca")
        if Repardata.objects.filter(nro_arma=nro_arma, nrodoc_pro=nrodoc_pro, tipoar=tipoar, marca=marca).count() > 0:
            raise forms.ValidationError('Error registro de arma ya existente')
       
        if self.cleaned_data.get('tipoar') is not None:
           filtrot=RefCalibres.objects.filter(tipoar__exact=self.cleaned_data.get('tipoar'))
           if self.cleaned_data.get('calibre') not in filtrot:
              raise forms.ValidationError('El calibre seleccionado no pertenece al tipo de Arma seleccionado')
        
        if self.cleaned_data.get('marca') is not None:
           filtrom=RefModArmas.objects.filter(trademark__exact=self.cleaned_data.get('marca'))
           if self.cleaned_data.get('modelo') not in filtrom:
              raise forms.ValidationError('El modelo seleccionado no pertenece a la Marca de Arma seleccionada')

        return self.cleaned_data

    class Meta:
        model = Repardata
        #exclude = ('id_prontuario')
        field_args = {
        "nrodoc_pro" : {"error_messages" : {"required" : "Es obligatorio","max_length" : "Hasta 8 digitos"}}
        }

class RefModArmasForm(forms.ModelForm):
  descripcion = forms.CharField(required=True)
  trademark = forms.ModelChoiceField(required=True,widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= RefTrademark.objects.filter(codidar__exact=9))

  class Meta:
    model = RefModArmas   



class TrademarkForm(forms.ModelForm):
  descripcion = forms.CharField(required=True)
  class Meta:
    model = RefTrademark

class RefCalibresForm(forms.ModelForm):
  descripcion = forms.CharField(required=True)
  tipoar = forms.ModelChoiceField(required=True,widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= RefTiposarmas.objects.all())

  class Meta:
    model = RefCalibres

class RefTiposarmasForm(forms.ModelForm):
  descripcion = forms.CharField(required=True)
  class Meta:
    model = RefTiposarmas

class HistoryreparForm(forms.ModelForm):
    apellidos_pro = forms.CharField(widget=forms.TextInput(attrs=dict({'class':'form-control','size': 100,'autocomplete':'off'})))
    nombres_pro = forms.CharField(widget=forms.TextInput(attrs=dict({'class':'form-control','size': 100,'autocomplete':'off'})))
    domicilio_pro = forms.CharField(required=False,widget=forms.TextInput(attrs=dict({'class':'form-control','autocomplete':'off','size':150})))
    nrodoc_pro = forms.IntegerField(max_value=99999999,widget=TextInput(attrs=dict({'class':'form-control','size': 6}))) 
    observaciones = forms.CharField(required=False,max_length=500,widget=forms.TextInput(attrs=dict({'class':'form-control','autocomplete':'off'})))
    fechamov=forms.DateTimeField(required=False)
    

    def __init__(self, *args, **kwargs):
        super(HistoryreparForm,self).__init__(*args, **kwargs)
        
    class Meta:
        model = Historyrepar
        exclude = ('reparid')
        field_args = {
        "nrodoc_pro" : {"error_messages" : {"required" : "Es obligatorio","max_length" : "Hasta 8 digitos"}}
        }
