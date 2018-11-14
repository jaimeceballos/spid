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
from django.utils.encoding import force_text
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


class UserCreateForm(forms.Form):
	fcio_opciones=(('1','ACTUANTE'),('2','PREVENTOR'),('3','ACT / PREV'))

	documento 				= forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control','onkeyup':'javascript:format(this);','aria-describedby':'inputError'})))
	nombre					= forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'Nombre'})))
	apellido				= forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'Apellido'})))
	fecha_nacimiento		= forms.DateField(required=True,widget=forms.DateInput(attrs=dict({'class':'form-control','placeholder':'dd/mm/aaaa'})),label="Fecha Nacimiento")
	ciudad_nacimiento		= forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'Nombre de la ciudad'})))
	ciudad_nacimiento_id    = forms.CharField(required=True,widget=forms.HiddenInput())
	estados_civiles			= forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=RefEstadosciv.objects.all().values_list('id','descripcion'))
	ciudad_residencia		= forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'Nombre de la ciudad'})))
	ciudad_residencia_id    = forms.CharField(required=True,widget=forms.HiddenInput())
	jerarquia				= forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'Jerarquía'})))
	jerarquia_id			= forms.CharField(required=True,widget=forms.HiddenInput())
	lugar_trabajo			= forms.CharField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'Dependencia'})))
	lugar_trabajo_id		= forms.CharField(required=True,widget=forms.HiddenInput())
	email					= forms.EmailField(required=True,widget=forms.TextInput(attrs=dict({'class':'form-control','placeholder':'mail@example.com'})))
	sexo 					= forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),choices=RefSexo.objects.all().values_list('id','descripcion'))
	grupos 					= forms.MultipleChoiceField(widget = forms.SelectMultiple(attrs={'class':'form-control'}), choices= Group.objects.all().values_list('id','name'))
	activo 					= forms.BooleanField()
	funcion					= forms.CharField(required=False,widget = forms.RadioSelect(choices = fcio_opciones))

class GroupForm(forms.ModelForm):
	#name = forms.CharField(required=True)
	class Meta:
		model = Group
		exclude=['name',]

		groups = forms.ModelChoiceField(
		Group.objects.all(),
		widget=admin.widgets.FilteredSelectMultiple(('groups'), False))

	def __init__(self, *args, **kwargs):
		super(GroupForm,self).__init__(*args,**kwargs)


		self.fields["permissions"].widget = forms.SelectMultiple()
		self.fields["permissions"].queryset = Permission.objects.filter(Q(content_type__app_label__contains='preventivos')|Q(content_type__app_label__contains='prontuario'))




class UserForm(forms.ModelForm):

	groups 	= forms.ModelMultipleChoiceField(widget = forms.SelectMultiple(),queryset = Group.objects.all())
	class Meta:
		model = User
		exclude = ['password','last_login','is_superuser','date_joined',]
		fields = ['groups','user_permissions','username','first_name','last_name','last_login','email','is_active','is_staff',]

	def __init__(self, *args, **kwargs):
		super(UserForm,self).__init__(*args,**kwargs)


		self.fields["user_permissions"].widget = forms.SelectMultiple()
		self.fields["user_permissions"].queryset = Permission.objects.filter(content_type__app_label__contains='preventivos')

		#self.fields["groups"].widget = forms.SelectMultiple()
		#self.fields["groups"].queryset = Group.objects.all()

class UserGroupsForm(forms.ModelForm):

	class Meta:
		model = User
		exclude = ('password','last_login','is_superuser','date_joined','user_permissions','username','first_name','last_name','last_login','email','is_active')
		fields = ('groups','is_staff')

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
		exclude = []

class DepartamentosForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefDepartamentos
		exclude = []

class ProvinciasForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)

	class Meta:
		model = RefProvincia
		exclude = []

class PaisesForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefPaises
		exclude = []

class LugaresForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefLugares
		exclude = []

class HogaresForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefHogares
		exclude = []

class CondclimasForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefCondclimas
		exclude = []

class UnidadesForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)


	def __init__(self, *args, **kwargs):
		super(UnidadesForm,self).__init__(*args,**kwargs)
		self.fields["ciudad"].widget = forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'})
		self.fields["ciudad"].queryset = RefCiudades.objects.filter(provincia__descripcion__contains = 'CHUBUT')

	class Meta:
		model = UnidadesRegionales
		exclude = []

class DependenciasForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)

	def __init__(self, *args, **kwargs):
		super(DependenciasForm,self).__init__(*args,**kwargs)
		self.fields["ciudad"].widget = forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'})
		self.fields["ciudad"].queryset = RefCiudades.objects.filter(provincia__descripcion__icontains = 'CHUBUT')
		self.fields["unidades_regionales"].widget = forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'})
		self.fields["unidades_regionales"].queryset= UnidadesRegionales.objects.all()

	class Meta:
		model = Dependencias
		exclude = []

class PeopleForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefPeople
		exclude = []

class TipoDelitosForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefTipoDelitos
		exclude = []

class DelitoForm(forms.ModelForm):
	descripcion = forms.CharField(required = True)
	tipo_delito = forms.ModelChoiceField(widget = forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= RefTipoDelitos.objects.all())
	class Meta:
		model = RefDelito
		exclude = []

class JobsForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefOcupacion
		exclude = []

class TrademarkForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefTrademark
		exclude = []

class TiposarmasForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefTiposarmas
		exclude = []

class SubtiposaForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefSubtiposa
		exclude = []

class SistemadisForm(forms.ModelForm):
	#descripcion = forms.CharField(required=True)
	class Meta:
		model = RefSistemadis
		exclude = []

class ItemForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefItems
		exclude = []

class CategoryForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)
	class Meta:
		model = RefCategory
		exclude = []

class BarriadasForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)

	def __init__(self, *args, **kwargs):
		super(BarriadasForm,self).__init__(*args,**kwargs)
		self.fields["ciudad"].widget = forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'})
		self.fields["ciudad"].queryset = RefCiudades.objects.filter(provincia__descripcion__contains = 'CHUBUT').values('id')



	class Meta:
	  model = RefBarrios
	  exclude = ('deleted',)

class AddressForm(forms.ModelForm):
	descripcion = forms.CharField(required=True)

	def __init__(self, *args, **kwargs):
		super(AddressForm,self).__init__(*args,**kwargs)
		self.fields["ciudad"].widget = forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'})
		self.fields["ciudad"].queryset = RefCiudades.objects.filter(provincia__descripcion__contains = 'CHUBUT')


	class Meta:
	  model = RefCalles
	  exclude = []

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
		self.fields["ciudades"].queryset = RefCiudades.objects.filter(provincia__descripcion__contains = 'CHUBUT')

class TipoJerarquiaForm(forms.ModelForm):
	descripcion = forms.CharField(required = True)

	class Meta:
		model = RefTipoJerarquia
		exclude = []

class DivisionJerarquiaForm(forms.ModelForm):
	descripcion = forms.CharField(required = True)

	class Meta:
		model = RefDivisionJerarquia
		exclude = []

class JerarquiasForm(forms.ModelForm):
	descripcion = forms.CharField(required = True)

	class Meta:
		model = RefJerarquias
		exclude = []

class SexoForm(forms.ModelForm):
	Sexo_opciones=(
	('1','FEMENINO'),
	('2','MASCULINO'),
	)
	descripcion = forms.CharField(widget = forms.CheckboxSelectMultiple(choices = Sexo_opciones))

	class Meta:
		model = RefSexo
		exclude = []

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
		exclude = []

class ActuantesForm(forms.ModelForm):
	fcio_opciones=(('1','ACTUANTE'),('2','PREVENTOR'),('3','ACT / PREV'))
	funcion = forms.CharField(initial='1',widget = forms.RadioSelect(choices = fcio_opciones))

	class Meta:
		model = Actuantes
		exclude = []


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
		exclude = []


class PersonalForm(forms.ModelForm):

	class Meta:
		model = Personal
		exclude = []

class ComunidadesForm(forms.ModelForm):
	Zonas_opciones=(
	('1','Urbana'),
	('2','Sub-urbana'),
	('3','Rural'),
	)
	descripcion = forms.CharField(widget = forms.CheckboxSelectMultiple(choices = Zonas_opciones))

	class Meta:
		model = RefComunidades
		exclude = []

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
	unidades_regionales = forms.ModelChoiceField(widget = forms.Select(attrs={'size':'13', 'onchange':'this.form.action=this.form.submit()'}), queryset= UnidadesRegionales.objects.all())
	dependencias = forms.Select()

	def __init__(self, *args, **kwargs):
		super(SearchPreveForm,self).__init__(*args,**kwargs)
		#self.fields["unidades_regionales"].widget = forms.Select(attrs={'size':'13', })
		#self.fields["unidades_regionales"].queryset= UnidadesRegionales.objects.exclude(descripcion__icontains='INVESTIGACION') &  UnidadesRegionales.objects.exclude(descripcion__icontains='AREA')

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
		exclude = []

nuevo=(('si','SI'),('no','NO'),)
class PersInvolucradasForm(forms.ModelForm):
	roles=forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13'}), queryset= RefPeople.objects.all(),initial=5)
	detenido=forms.ChoiceField(widget=forms.Select(attrs={'size':'13'}), required=False,choices=nuevo,initial='si',)
	#juridica=forms.ChoiceField(widget=forms.Select(attrs={'size':'13'}), required=False,choices=nuevo,initial='si',)
	nrocuit = forms.CharField(required= False)

	def __init__(self, *args, **kwargs):
		super(PersInvolucradasForm,self).__init__(*args,**kwargs)
		self.fields["cuit"].widget = forms.Select(attrs={'size':'13'})
		self.fields["cuit"].queryset= RefTipoDocumento.objects.filter(descripcion__contains='CUI')
		self.fields["cuit"].initial = 8


	class Meta:
		model = PersInvolucradas
		exclude = ('persona','hechos')
		widgets = {
			'roles': forms.Select(attrs={'initial':5}),
		    'cuit': forms.Select(attrs={'initial':8}),
		}

class DomiciliosForm(forms.ModelForm):

	class Meta:
		model = Domicilios
		exclude = ('personas','ref_ciudades',)

class DomicilioProntuarioForm(forms.ModelForm):

	class Meta:
		model = Domicilios
		exclude = ['personas',]


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
	altura=forms.IntegerField(initial=0,required=False)
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
		exclude = []

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
		exclude = []

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
		exclude = []

class MapaForm(forms.Form):

	ciudades = forms.ModelChoiceField(widget=forms.Select(attrs={'size':'13',}), required=False, queryset= RefCiudades.objects.all())
	ureg= forms.ModelChoiceField(widget = forms.Select(attrs={'size':'13', }), required=False, queryset= UnidadesRegionales.objects.all())
	depe = forms.Select()
	ciu = forms.BooleanField(required=False,initial=False)
	depes=forms.BooleanField(required=False,initial=False)
	delito=forms.ModelChoiceField(widget = forms.Select(attrs={'size':'13',}),queryset = RefDelito.objects.all(),required=False)


	def __init__(self, *args, **kwargs):
		super(MapaForm,self).__init__(*args,**kwargs)
		self.fields["ciudades"].widget = forms.Select(attrs={'size':'13'})
		self.fields["ciudades"].queryset= RefCiudades.objects.filter(provincia__descripcion__icontains = 'CHUBUT')#RefCiudades.objects.filter(provincia__contains = RefProvincia.objects.filter(descripcion__contains = 'CHUBUT').values('id'))
		self.fields["ureg"].widget = forms.Select(attrs={'size':'13', })
		self.fields["ureg"].queryset= UnidadesRegionales.objects.exclude(descripcion__icontains='INVESTIGACION') &  UnidadesRegionales.objects.exclude(descripcion__icontains='AREA')
		self.fields["delito"].widget = forms.Select(attrs={'size':'13',})
		self.fields["delito"].queryset = RefDelito.objects.all()
		self.fields["delito"].initial=RefDelito.objects.get(id=1)

	def clean(self):
		cleaned_data = super(MapaForm,self).clean()
		if not self.cleaned_data.get['ciudades']:
		   raise forms.ValidationError('Debe indicar una Ciudad ')

		return cleaned_data

class AmpliacionForm(forms.ModelForm):

	class Meta:
		model   = Ampliacion
		exclude = ('preventivo','fecha_autorizacion','sendwebservice')

	def __init__(self, *args, **kwargs):
		super(AmpliacionForm,self).__init__(*args,**kwargs)
		self.fields["autoridades"].widget = CheckboxSelectMultiple()
		self.fields["autoridades"].queryset = RefAutoridad.objects.all()
		self.fields["autoridades"].help_text='Seleccione haciendo click sobre cada de las Autoridades a Informar.-'
		self.fields["titulo"].widget.attrs = {'size':80,}
		self.fields["descripcion"].widget = forms.Textarea(attrs={'cols': 80, 'rows': 20})

class CambiarContraseniaForm(forms.ModelForm):
	MOTIVO_CHOICES = (
		('1','ORDEN SUPERIOR'),
		('2','SOLICITUD DEL USUARIO'),
	)
	motivo 	= forms.ChoiceField(widget=forms.Select(attrs=dict({'class':'form-control'})),choices = MOTIVO_CHOICES,required=True)
	detalle_motivo = forms.CharField(widget=forms.Textarea(attrs=dict({'class':'form-control'})))
	class Meta:
		model = CambiarContrasenia
		exclude = ('usuario', 'usuario_que_cambia','fecha')

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
