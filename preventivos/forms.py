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
from preventivos.models import *
from django.core.exceptions import ValidationError
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.db.models import Q


class CambiarPassForm(forms.Form):
	pass1 = forms.CharField(required=True, widget=forms.PasswordInput(),label='Ingresar una clave nueva')
	pass2 = forms.CharField(required = True, widget=forms.PasswordInput(),label='Vuelva a Ingresar la clave')

	def clean_pass2(self):
		pass1 = self.cleaned_data['pass1']
		pass2 = self.cleaned_data['pass2']
		if pass1 != pass2:
			raise forms.ValidationError("Existe un problema con la contraseña elegida, vuelva a ingresarla.")

		return pass2

class GroupForm(forms.ModelForm):
	#name = forms.CharField(required=True)
	class Meta:
		model = Group
		exclude=('name')
		   
		groups = forms.ModelChoiceField(
		Group.objects.all(), 
		widget=admin.widgets.FilteredSelectMultiple(('groups'), False))

	def __init__(self, *args, **kwargs):
		super(GroupForm,self).__init__(*args,**kwargs)
 
	   
		self.fields["permissions"].widget = forms.SelectMultiple()
		self.fields["permissions"].queryset = Permission.objects.filter(content_type__app_label__contains='preventivos')
 



class UserForm(forms.ModelForm):
   
	class Meta:
		model = User
		exclude = ('password','last_login','is_superuser','date_joined')
		fields = ('groups','user_permissions','username','first_name','last_name','last_login','email','is_active','is_staff')
 
	def __init__(self, *args, **kwargs):
		super(UserForm,self).__init__(*args,**kwargs)
 
	   
		self.fields["user_permissions"].widget = forms.SelectMultiple()
		self.fields["user_permissions"].queryset = Permission.objects.filter(content_type__app_label__contains='preventivos')
 
		self.fields["groups"].widget = forms.SelectMultiple()
		self.fields["groups"].queryset = Group.objects.all()
 
	   
class UserProfileForm(forms.ModelForm):
  
	def __init__(self, *args, **kwargs):
		super(UserProfileForm,self).__init__(*args,**kwargs)
 
	class Meta():
	   
		model = UserProfile
		fields=('ureg','depe')

class CiudadesForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefCiudades

class DepartamentosForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefDepartamentos

class ProvinciasForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
   
	class Meta:
		model = RefProvincia


class PaisesForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefPaises

class LugaresForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefLugares

class HogaresForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefHogares

class CondclimasForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefCondclimas

class UnidadesForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	ciudad = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= RefCiudades.objects.filter(provincia__contains = RefProvincia.objects.filter(descripcion__contains = 'CHUBUT').values('id'))  )
	class Meta:
		model = UnidadesRegionales
 
class DependenciasForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	ciudad = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= RefCiudades.objects.filter(provincia__contains = RefProvincia.objects.filter(descripcion__contains = 'CHUBUT').values('id'))  )
	unidades_regionales = forms.ModelChoiceField(widget = forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= UnidadesRegionales.objects.all())

	
	class Meta:
		model = Dependencias        

class PeopleForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefPeople

class TipoDelitosForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefTipoDelitos
 
class DelitoForm(forms.ModelForm):
	descripcion = forms.CharField(required = True)
	tipo_delito = forms.ModelChoiceField(widget = forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= RefTipoDelitos.objects.all())
	class Meta:
		model = RefDelito

class JobsForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefOcupacion

class TrademarkForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefTrademark

class TiposarmasForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefTiposarmas

class SubtiposaForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefSubtiposa

class SistemadisForm(forms.ModelForm):
	#descripcion = forms.CharField(required=True)
	class Meta:
		model = RefSistemadis

class ItemForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefItems

class CategoryForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefCategory

class BarriadasForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	ciudad = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= RefCiudades.objects.filter(provincia__contains = RefProvincia.objects.filter(descripcion__contains = 'CHUBUT').values('id'))  )
   
	class Meta:
	  model = RefBarrios
	  exclude = ('deleted',)
  
class AddressForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	ciudad = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= RefCiudades.objects.filter(provincia__contains = RefProvincia.objects.filter(descripcion__contains = 'CHUBUT').values('id'))  )
   
	class Meta:
	  model = RefCalles   

class AuthoritiesForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	email = forms.EmailField()
	todo = forms.BooleanField(required=False)
	class Meta:
	   model = RefAutoridad
	   fields = ('ciudades','descripcion','email',)
 
	def __init__(self, *args, **kwargs):
		super(AuthoritiesForm,self).__init__(*args,**kwargs)

		self.fields["ciudades"].widget = CheckboxSelectMultiple()
		self.fields["ciudades"].queryset = RefCiudades.objects.filter(provincia__contains = RefProvincia.objects.filter(descripcion__contains = 'CHUBUT').values('id'))
 
class TipoJerarquiaForm(forms.ModelForm):
	descripcion = forms.CharField(required = True)
 
	class Meta:
		model = RefTipoJerarquia
 
class DivisionJerarquiaForm(forms.ModelForm):
	descripcion = forms.CharField(required = True)
 
	class Meta:
		model = RefDivisionJerarquia
 
class JerarquiasForm(forms.ModelForm):
	descripcion = forms.CharField(required = True)
 
	class Meta:
		model = RefJerarquias

class SexoForm(forms.ModelForm):
	Sexo_opciones=(
	('1','FEMENINO'),
	('2','MASCULINO'),
	)
	descripcion = forms.CharField(widget = forms.CheckboxSelectMultiple(choices = Sexo_opciones))
  
	class Meta:
		model = RefSexo

class TipodocForm(forms.ModelForm):
	Doc_opciones=(
	('1','DNI'),
	('2','LC'),
	('3','LE'),
	('4','CI'),
	('5','PAS'),
	)
	descripcion = forms.CharField(widget = forms.CheckboxSelectMultiple(choices = Doc_opciones))
  
	class Meta:
		model = RefTipoDocumento

class ActuantesForm(forms.ModelForm):
	fcio_opciones=(('1','ACTUANTE'),('2','PREVENTOR'),('3','ACT / PREV'))
	funcion = forms.CharField(initial='1',widget = forms.RadioSelect(choices = fcio_opciones))
	
	class Meta:
		model = Actuantes
		

class HorizRadioRenderer(forms.RadioSelect.renderer):
	""" this overrides widget method to put radio buttons horizontally
		instead of vertically.
	"""
	def render(self):
			"""Outputs radios"""
			return mark_safe(u'%s' % u'\n'.join([u'%s'  % force_unicode(w) for w in self]))


laburo_opciones=(('1','ESTABLE'),('2','NO ESTABLE'))

class PersonasForm(forms.ModelForm):
	pais_res = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= RefPaises.objects.all(),required= False)
	celular = forms.CharField(required= False)
	"""
	alias = forms.CharField(required= False)
	cuit = forms.CharField(required= False)
	emails=forms.CharField(required=False)
	condicionlaboral=forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=laburo_opciones,initial='1',required=False)
	"""
	def __init__(self, *args, **kwargs):
		super(PersonasForm, self).__init__(*args, **kwargs)
		# Making name required
		self.fields['nro_doc'].required = False
		#self.fields['estado_civil'].required = True
		#self.fields['ocupacion'].required = True
		self.fields['pais_res'].queryset= RefPaises.objects.all()
	class Meta:
		model = Personas
		#fields = ('estado_civil','nro_doc','ciudad_res','ocupacion')
	


class PersonalForm(forms.ModelForm):

	class Meta:
		model = Personal

class ComunidadesForm(forms.ModelForm):
	Zonas_opciones=(
	('1','Urbana'),
	('2','Sub-urbana'),
	('3','Rural'),
	)
	descripcion = forms.CharField(widget = forms.CheckboxSelectMultiple(choices = Zonas_opciones))
  
	class Meta:
		model = RefComunidades

class PrimerForm(forms.ModelForm):
	unidad = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13'}), queryset= UnidadesRegionales.objects.all(), required=False)
	nro = forms.IntegerField(required=False,validators=[MinValueValidator(1),MaxValueValidator(9999)])
	anio = forms.IntegerField(required=False,validators=[MinValueValidator(2012),MaxValueValidator(2025)])

	def clean(self):
		cleaned_data = super(PrimerForm, self).clean()
		#if Preventivos.objects.filter(dependencia__exact=self.cleaned_data.get('dependencia'),nro__exact=self.cleaned_data.get('nro'),anio__exact=self.cleaned_data.get('anio')).values('nro'):
		#   raise forms.ValidationError("El Nro y Año Existentes")
	 
		#if Preventivos.objects.filter(dependencia__exact=self.cleaned_data.get('dependencia'),nro__exact=self.cleaned_data.get('nro'),anio__exact=self.cleaned_data.get('anio')).values('nro'):
		#   raise forms.ValidationError("El Nro y Año Existentes")
		if self.cleaned_data.get('fecha_denuncia') is not None:
			fecha_denuncia = self.cleaned_data.get('fecha_denuncia')
			#Obtenemos la fecha actual
			
			fecha_actual = timezone.now()
 
			if fecha_denuncia > fecha_actual:
			   raise forms.ValidationError("El Fecha de Denuncia no debe ser mayor al dia de hoy")
		else:
		  raise forms.ValidationError("Ingrese una Fecha de Denuncia menor o igual a la Fecha actual")
   
		
		if self.cleaned_data.get('unidad') is not None:
		   filtro=Dependencias.objects.filter(unidades_regionales_id__exact=self.cleaned_data.get('unidad'))
		   if self.cleaned_data.get('dependencia') not in filtro:
			  raise forms.ValidationError('La dependencia elegida no pertenece a la U.R.E seleccionada')
		  
		return self.cleaned_data
	class Meta:
		model = Preventivos
		fields = ('fecha_denuncia','caratula','dependencia')
	
	

class SegundoForm(forms.ModelForm):
	unidad = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13'}), queryset= UnidadesRegionales.objects.all(), required=False)
	nro = forms.IntegerField(required=False)
	anio = forms.IntegerField(required=False)

	def clean(self):
		cleaned_data = super(SegundoForm, self).clean()
		#if self.cleaned_data.get('actuante') is not None:
		#   if self.cleaned_data.get('preventor') is not None:
			  #if self.cleaned_data.get('actuante') == self.cleaned_data.get('preventor'):
			  #raise forms.ValidationError("Seleccione Actuante y Preventor")
		#else:
		#raise forms.ValidationError("Seleccione Actuante y Preventor diferentes")
		#if Preventivos.objects.filter(dependencia__exact=self.cleaned_data.get('dependencia'),nro__exact=self.cleaned_data.get('nro'),anio__exact=self.cleaned_data.get('anio')).values('nro'):
		#    raise forms.ValidationError("El Nro y Año Existentes")
	   
		if  self.cleaned_data.get('actuante') is None or self.cleaned_data.get('preventor') is None:
			raise forms.ValidationError("Seleccione Actuante y Preventor")
	
		return self.cleaned_data
	class Meta:
		model = Preventivos
		fields = ('actuante','preventor',)



class TerceroForm(forms.ModelForm):
	unidad = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13'}), queryset= UnidadesRegionales.objects.all(), required=False)
	nro = forms.IntegerField(required=False)
	anio = forms.IntegerField(required=False)
	def clean(self):
		cleaned_data = super(TerceroForm, self).clean()
	   
		if Preventivos.objects.filter(dependencia__exact=self.cleaned_data.get('dependencia'),nro__exact=self.cleaned_data.get('nro'),anio__exact=self.cleaned_data.get('anio')).values('nro'):
		   raise forms.ValidationError("El Nro y Año Existentes")
		
		return self.cleaned_data
		
	def __init__(self, *args, **kwargs):
		super(TerceroForm,self).__init__(*args,**kwargs)
		self.fields["autoridades"].widget = CheckboxSelectMultiple()
		self.fields["autoridades"].queryset = RefAutoridad.objects.all()
		self.fields["autoridades"].help_text='Seleccione haciendo click sobre cada de las Autoridades a Informar.-'
	class Meta:
		model =  Preventivos
		fields = ('autoridades',)


class FinForm(forms.ModelForm):
	unidad = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13'}), queryset= UnidadesRegionales.objects.all(), required=False)
	nro = forms.IntegerField(required=False)
	anio = forms.IntegerField(required=False)
   
	def clean(self):
		cleaned_data = super(FinForm, self).clean()
		if  self.cleaned_data.get('actuante') is None or self.cleaned_data.get('preventor') is None:
			raise forms.ValidationError("Seleccione Actuante y Preventor")
		#if Preventivos.objects.filter(dependencia__exact=self.cleaned_data.get('dependencia'),nro__exact=self.cleaned_data.get('nro'),anio__exact=self.cleaned_data.get('anio')).values('nro'):
		   #raise forms.ValidationError("El Nro y Año Existentes")
		return self.cleaned_data
	def __init__(self, *args, **kwargs):
		super(FinForm,self).__init__(*args,**kwargs)
		self.fields["autoridades"].widget = CheckboxSelectMultiple()
		self.fields["autoridades"].queryset = RefAutoridad.objects.all()
		self.fields["autoridades"].help_text='Seleccione haciendo click sobre cada de las Autoridades a Informar.-'
	
	class Meta:
		model = Preventivos
		fields = ('fecha_denuncia','caratula','actuante','preventor','autoridades',)

class PreventivosForm(forms.ModelForm):
	nro=forms.IntegerField(required=False)
	anio=forms.IntegerField(required=False)
	fecha_carga=forms.DateTimeField(required=False)
	fecha_autorizacion=forms.DateTimeField(required=False)
	fecha_cierre=forms.DateTimeField(required=False)
	dependencia=forms.IntegerField(required=False)
	def __init__(self, *args, **kwargs):
		super(PreventivosForm,self).__init__(*args,**kwargs)
		self.fields["autoridades"].widget = CheckboxSelectMultiple()
		self.fields["autoridades"].queryset = RefAutoridad.objects.all()
		self.fields["autoridades"].help_text='Seleccione haciendo click sobre cada de las Autoridades a Informar.-'
	
  
	class Meta:
		model = Preventivos
		fields = ('nro','anio','fecha_denuncia','caratula','actuante','preventor','autoridades',)

class HechosForm(forms.ModelForm):

	tipodelito=forms.ModelChoiceField(required=False,widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= RefTipoDelitos.objects.all())

	def __init__(self, *args, **kwargs):
		super(HechosForm, self).__init__(*args, **kwargs)
		# Making name required
		self.fields['motivo'].required = True
		self.fields['fecha_desde'].required = True
		self.fields['fecha_hasta'].required = True
   

	def clean_motivo(self):
		motivo=self.cleaned_data['motivo']
		if not motivo:
			msg = 'Ingrese el Motivo de la Denuncia del Hecho'
			raise forms.ValidationError(self.error_messages[msg])
	
		return motivo

	def clean_fecha_desde(self):    
		fecha_desde = self.cleaned_data['fecha_desde']
		if not fecha_desde: 
			 raise forms.ValidationError(self.error_messages['Ingrese las Fechas y Hora de Inicio'])
		return fecha_desde   
	def clean_fecha_hasta(self):
		fecha_desde = self.cleaned_data['fecha_desde']
		fecha_hasta = self.cleaned_data['fecha_hasta']
		if not fecha_hasta:
		   raise forms.ValidationError(self.error_messages['Ingrese las Fechas y Hora Final del Hecho'])
		else:
		   if fecha_desde > fecha_hasta:
			   raise forms.ValidationError("La Fecha y Hora Final Debe ser mayor a la de Inicio")
		
		return fecha_hasta
   
	class Meta:
		model = Hechos
		fields = ('descripcion','motivo','fecha_desde','fecha_hasta',)
		exclude = ('fecha_carga','preventivo',)

class RefModosHechoForm(forms.ModelForm):
	delito=forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= RefDelito.objects.all())
	class Meta:
		model = Hechos
		fields = ('descripcion','delito')

class RefMotivosHechoForm(forms.ModelForm):
	class Meta:
		model = Hechos
		fields = ('descripcion',)

class SearchPreveForm(forms.Form):
	nro=forms.IntegerField(required=False)
	anio=forms.IntegerField(required=False)
	fecha_carga=forms.DateTimeField(required=False)
	caratula=forms.CharField(required=False)
	unidades_regionales=forms.ModelChoiceField(widget = forms.Select(attrs={'size':'13', }), required=False, queryset= UnidadesRegionales.objects.exclude(descripcion__icontains='INVESTIGACION') &  UnidadesRegionales.objects.exclude(descripcion__icontains='AREA'))
	#unidades_regionales = forms.ModelChoiceField(widget = forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= UnidadesRegionales.objects.filter(Q(descripcion__startswith="OPERA") | Q(descripcion__startswith="UNIDAD")))
	dependencias = forms.Select()
	
	
	
	"""
	class Meta:
		model = Preventivos
		fields = ('nro','anio','fecha_carga','caratula',)"""

class HechoForm(forms.ModelForm):

	#tipodelito=forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= RefTipoDelitos.objects.all())

	def __init__(self, *args, **kwargs):
		super(HechoForm, self).__init__(*args, **kwargs)
		# Making name required
		self.fields['motivo'].required = True
		self.fields['fecha_desde'].required = True
		self.fields['fecha_hasta'].required = True
   

	def clean_motivo(self):
		motivo=self.cleaned_data['motivo']
		if not motivo:
			msg = 'Ingrese el Motivo de la Denuncia del Hecho'
			raise forms.ValidationError(self.error_messages[msg])
	
		return motivo
	def clean_fecha_desde(self):    
		fecha_desde = self.cleaned_data['fecha_desde']
		if not fecha_desde: 
			 raise forms.ValidationError(self.error_messages['Ingrese las Fechas y Hora de Inicio'])
		return fecha_desde   
	def clean_fecha_hasta(self):
		cleaned_data = super(HechoForm, self).clean()
		fecha_desde = self.cleaned_data['fecha_desde']
		fecha_hasta = self.cleaned_data['fecha_hasta']
		if not fecha_hasta:
		   raise forms.ValidationError(self.error_messages['Ingrese las Fechas y Hora Final del Hecho'])
		else:
		   if fecha_desde > fecha_hasta:
			   raise forms.ValidationError("La Fecha y Hora Final Debe ser mayor a la de Inicio")
		
		return fecha_hasta
   
	class Meta:
		model = Hechos
		fields = ('descripcion','motivo','fecha_desde','fecha_hasta',)
		exclude = ('fecha_carga','preventivo','delito','tipodelito',)

class HechosDelitoForm(forms.ModelForm):

	class Meta:
		model = HechosDelito


class PersInvolucradasForm(forms.ModelForm):
	roles=forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13'}), queryset= RefPeople.objects.all(),initial=1)

	class Meta:
		model = PersInvolucradas
		exclude = ('persona','hechos')
		widgets = {
			'roles': forms.Select(attrs={'initial':1}),
		 
		}
	   
class DomiciliosForm(forms.ModelForm):
 
	class Meta:
		model = Domicilios
		exclude = ('personas','ref_ciudades',)

class DetenidosForm(forms.ModelForm):

	def clean_fechahoradetencion(self):    
		fechahoradetencion = self.cleaned_data['fechahoradetencion']
		if not fechahoradetencion: 
			 raise forms.ValidationError(self.error_messages['Ingrese las Fechas y Hora de Ingreso'])
		return fechahoradetencion 
		
	def clean_fechahoralibertad(self):
		cleaned_data = super(DetenidosForm, self).clean()
		fechahoradetencion = self.cleaned_data['fechahoradetencion']
		fechahoralibertad = self.cleaned_data['fechahoralibertad']

		if not fechahoralibertad:
		   raise forms.ValidationError(self.error_messages['Ingrese las Fechas y Hora de Egreso'])
		else:
		   if fechahoradetencion > fechahoralibertad:
			   raise forms.ValidationError("La Fecha y Hora de Egreso Debe ser mayor a la de Ingreso")
		
		return fechahoralibertad

	class Meta:
		model = Detenidos
		exclude = ('persona',)

class PadresForm(forms.ModelForm):
 
	class Meta:
		model = Padres
		exclude = ('persona',)


class LugarForm(forms.ModelForm):
	nuevo_barrio = forms.CharField(required=False)
	callen = forms.CharField(widget=forms.HiddenInput())
	def clean_nuevo_barrio(self):
		cleaned_data = super(LugarForm, self).clean()
		nbarrio = self.cleaned_data['nuevo_barrio']
		if not self.cleaned_data.has_key('barrio'):
			if not nbarrio:
				raise forms.ValidationError('Debe indicar el nombre del Barrio')
		return nbarrio

	def __init__(self, *args, **kwargs):
		super(LugarForm,self).__init__(*args,**kwargs)
		self.fields["cond_climaticas"].widget = CheckboxSelectMultiple()
		self.fields["cond_climaticas"].queryset = RefCondclimas.objects.all()
		self.fields["cond_climaticas"].help_text='Seleccione haciendo click sobre cada de las Autoridades a Informar.-'

	class Meta:
		model = Lugar
		exclude = ('hecho','delito')

class ElementosForm(forms.ModelForm):

	class Meta:
		model = Elementos
		exclude = ('hechos',)

class UnidadMedidasForm(forms.ModelForm):

	class Meta:
		model = RefUnidadmedidas

class ArmasForm(forms.ModelForm):
	nueva_marca = forms.CharField(required=False)

	def clean_nueva_marca(self):
		cleaned_data = super(ArmasForm,self).clean()
		nueva_marca = self.cleaned_data['nueva_marca']
		if not self.cleaned_data.has_key('marcas'):
			if not nueva_marca:
				raise forms.ValidationError('Debe indicar una marca')
		return nueva_marca
	class Meta:
		model = Armas

class VehiculosForm(forms.ModelForm):

	nueva_marcav = forms.CharField(required=False)

	def clean_nueva_marca(self):
		cleaned_data = super(VehiculosForm,self).clean()
		nueva_marcav = self.cleaned_data['nueva_marcav']
		if not self.cleaned_data.has_key('idmarca'):
			if not nueva_marcav:
				raise forms.ValidationError('Debe indicar una marca')
		return nueva_marcav

	class Meta:
		model = Vehiculos

class MapaForm(forms.Form):
	ciudades = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13',}), required=False, queryset= RefCiudades.objects.filter(provincia__contains = RefProvincia.objects.filter(descripcion__contains = 'CHUBUT').values('id'))  )
	ureg= forms.ModelChoiceField(widget = forms.Select(attrs={'size':'13', }), required=False, queryset= UnidadesRegionales.objects.exclude(descripcion__icontains='INVESTIGACION') &  UnidadesRegionales.objects.exclude(descripcion__icontains='AREA'))
	depe = forms.Select()
	ciu = forms.BooleanField(required=False,initial=False)
	depes=forms.BooleanField(required=False,initial=False)
	delito=forms.ModelChoiceField(widget = forms.Select(attrs={'size':'13',}),queryset = RefDelito.objects.all(), initial=RefDelito.objects.get(id=1),required=False)
	
	"""def __init__(self, *args, **kwargs):
		super(MapaForm,self).__init__(*args,**kwargs)
		self.fields["delito"].widget = CheckboxSelectMultiple()
		self.fields["delito"].queryset = RefDelito.objects.all()
		self.fields["delito"].help_text='Seleccione haciendo click sobre cada uno de los Delitos'"""
	
	def clean(self):
		cleaned_data = super(MapaForm,self).clean()
		if not self.cleaned_data.get['ciudades']:
		   raise forms.ValidationError('Debe indicar una Ciudad ')
			   
		return cleaned_data

class AmpliacionForm(forms.ModelForm):
	
	class Meta:
		model   = Ampliacion
		exclude = ('preventivo','fecha_autorizacion',)

	def __init__(self, *args, **kwargs):
		super(AmpliacionForm,self).__init__(*args,**kwargs)
		self.fields["autoridades"].widget = CheckboxSelectMultiple()
		self.fields["autoridades"].queryset = RefAutoridad.objects.all()
		self.fields["autoridades"].help_text='Seleccione haciendo click sobre cada de las Autoridades a Informar.-'
		self.fields["titulo"].widget.attrs = {'size':80,}
		self.fields["descripcion"].widget = forms.Textarea(attrs={'cols': 80, 'rows': 20})

"""
nuevo=(('1','SI'),('0','NO'),)
class ViolenciaFliarForm(forms.ModelForm):
	fecha = forms.DateTimeField(required=False)
	fecha_carga = forms.DateTimeField(required=False)
	intervencionsavd=forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer), choices=nuevo,initial='0',)
	intervencionotro=forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer), choices=nuevo,initial='0',)
	#hechos=forms.IntegerField(required=False)
	class Meta:
		model = ViolenciaFliar
		exclude = ('hechos','fecha','fecha_carga',)   
	def __init__(self, *args, **kwargs):
		super(ViolenciaFliarForm,self).__init__(*args, **kwargs)
		self.fields["intervencioncual"].widget.attrs = {'size':42,}


class PerInvolViolenfliarForm(forms.ModelForm):
	roles=forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13'}), queryset= RefPeople.objects.filter(descripcion__in=['DENUNCIANTE','DENUNCIADO','VICTIMA']))
	cgfconviven=forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer), choices=nuevo,initial='0',required=False)
	vdconviven=forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer), choices=nuevo,initial='0',required=False)
	pidereserva= forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer), choices=nuevo,initial='0',required=False)
	juridica = forms.ChoiceField(widget=forms.RadioSelect(renderer=HorizRadioRenderer),choices=nuevo,initial='0',required=False)
	razon_social = forms.CharField(widget=forms.TextInput(attrs={'size':'60'}),required=False)
	cargo = forms.CharField(widget=forms.TextInput(attrs={'size':'60'}),required=False)
	cargado_viol = forms.IntegerField(required=False)
	teldomalternativos = forms.CharField(widget=forms.TextInput(attrs={'size':'120'}),required=False)
	teldomfliaprimaria = forms.CharField(widget=forms.TextInput(attrs={'size':'120'}),required=False)
	telconfigurasreferentes = forms.CharField(widget=forms.TextInput(attrs={'size':'120'}),required=False)
	class Meta:
		model = PerInvolViolenfliar
		exclude = ('persona','violencia')
		widgets = {
			'roles': forms.Select(attrs={'initial':1}),
			'composiciongrupofliar' : forms.TextInput(attrs={'size':50,}),
			'vinculodenunciado' : forms.TextInput(attrs={'size':50,}),
			'vinculovictima' : forms.TextInput(attrs={'size':60,}),
			'teldomalternativos' : forms.TextInput(attrs={'size':120}),
			'teldomfliaprimaria': forms.TextInput(attrs={'size':120}),
			'telconfigurasreferentes': forms.TextInput(attrs={'size':120}),
			
		}

	def __init__(self, *args, **kwargs):
		super(PerInvolViolenfliarForm,self).__init__(*args, **kwargs)
"""