#encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import Group,Permission,User
from django.contrib.admin.models import LogEntry
from django.db.models import signals
import random,datetime,time
from django.core.validators import MinValueValidator,MaxValueValidator

class Registrouser(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	action=models.CharField(max_length=50)
	tablas = models.CharField(max_length=50)
	link = models.CharField(max_length=50)
	session=models.CharField(max_length=50)
	fecha=models.DateTimeField(auto_now=True)
	def __str__(self):
	  return '%s' % self.user

	class Meta:
		db_table = 'Registrouser'
		app_label = 'preventivos'

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
	ureg = models.ForeignKey('UnidadesRegionales',blank=True, null=True, on_delete=models.DO_NOTHING)
	depe = models.ForeignKey('Dependencias',blank=True, null=True, on_delete=models.DO_NOTHING)
	last_login = models.BooleanField(default=True)
	ultimo_ingreso = models.DateTimeField(blank=True,null=True)
	solicitud_cambio = models.BooleanField(default=False)
	fecha_solicitud = models.DateTimeField(blank=True,null=True)
	clave_anterior = models.CharField(max_length=128,blank=True,null=True)

	def __str__(self):
	  return "%s's profile" % self.user

	class Meta:
		db_table = 'UserProfile'
		app_label = 'preventivos'


	def user_profile(sender, instance, signal, *args, **kwargs):
		# Creates user profile
		profile, new = UserProfile.objects.get_or_create(user=instance)

	signals.post_save.connect(user_profile, sender=User)



class RefPaises(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField("Seleccione Pais :", unique=True, max_length=45 )


	def __str__(self):
	  return  u'%s' % (self.descripcion)
	  self.descripcion = self.descripcion.upper()


	class Meta:
		ordering = ["descripcion"]
		db_table = 'ref_paises'
		app_label = 'preventivos'

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefPaises, self).save(force_insert, force_update)

class RefProvincia(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField("Ingrese Provincia :", max_length=45)
	pais = models.ForeignKey(RefPaises,on_delete=models.PROTECT)


	def __str__(self):
		return  u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()


	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefProvincia, self).save(force_insert, force_update)

	class Meta:
		unique_together=('descripcion','pais',)
		db_table = 'ref_provincia'
		ordering = ["descripcion"]
		app_label = 'preventivos'

class RefDepartamentos(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField("Ingrese Departamento :", unique=True, max_length=45)
	provincia = models.ForeignKey(RefProvincia, on_delete=models.PROTECT)

	def __str__(self):
		return  u'%s' %  (self.descripcion)
		self.descripcion = self.descripcion.upper()


	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefDepartamentos, self).save(force_insert, force_update)

	class Meta:
		#unique_together=('descripcion','provincia',)
		ordering = ["descripcion"]
		db_table = 'ref_departamentos'
		app_label = 'preventivos'

class RefCiudades(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=80)
	departamento = models.ForeignKey('RefDepartamentos',blank=True, null=True, on_delete=models.PROTECT)
	provincia = models.ForeignKey('RefProvincia', blank=True,  null=True, on_delete=models.PROTECT)
	pais = models.ForeignKey('RefPaises', on_delete=models.PROTECT)
	lat= models.CharField(max_length=50,blank=True,null=True)
	longi= models.CharField(max_length=50,blank=True,null=True)

	def __str__(self):
		return  u'%s' %  (self.descripcion)
		self.descripcion = self.descripcion.upper()

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefCiudades, self).save(force_insert, force_update)

	class Meta:
		unique_together = ('pais','provincia','descripcion',)
		ordering = ["descripcion"]
		db_table = 'ref_ciudades'
		app_label = 'preventivos'

#modelo de datos de referencias de tipos de lugares en donde se cometio el hecho
class RefLugares(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=100, blank=True, unique=True)

	def __str__(self):
		return u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefLugares, self).save(force_insert, force_update)

	class Meta:
		ordering = ["descripcion"]
		db_table = 'ref_lugares'
		app_label = 'preventivos'

class RefHogares(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=100,blank=True, unique=True)

	def __str__(self):
		return u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefHogares, self).save(force_insert, force_update)

	class Meta:
		ordering = ["descripcion"]
		db_table = 'ref_hogares'
		app_label = 'preventivos'

class RefCondclimas(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=150,blank=True, unique=True)

	def __str__(self):
		return u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefCondclimas, self).save(force_insert, force_update)

	class Meta:
		ordering = ["descripcion"]
		db_table = 'ref_condclimas'
		app_label = 'preventivos'

class UnidadesRegionales(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=80)
	ciudad = models.ForeignKey('RefCiudades',on_delete=models.PROTECT)
	cabecera_envio = models.ForeignKey('Dependencias',on_delete = models.PROTECT,blank=True,null=True)

	def __str__(self):
		return u'%s' %  (self.descripcion)
		self.descripcion = self.descripcion.upper()


	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(UnidadesRegionales, self).save(force_insert, force_update)

	class Meta:
		unique_together = ('descripcion','ciudad')
		ordering = ["descripcion"]
		db_table = 'unidades_regionales'
		app_label = 'preventivos'

class Dependencias(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=80)
	unidades_regionales = models.ForeignKey('UnidadesRegionales', related_name="unidades", on_delete=models.PROTECT)
	ciudad = models.ForeignKey('RefCiudades',on_delete=models.PROTECT)


	def __str__(self):
		return u'%s - %s' % (self.id, self.descripcion)
		self.descripcion = self.descripcion.upper()

	def save(self, force_insert=False, force_update= False):
		self.descripcion = self.descripcion.upper()
		super(Dependencias, self).save(force_insert,force_update)

	class Meta:
		unique_together = ('descripcion','unidades_regionales','ciudad')
		ordering = ["descripcion"]
		db_table = 'dependencias'
		app_label = 'preventivos'


class RefPeople(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField("Involucrados - Tipos :", null=False, unique=True, max_length=150 )


	def __str__(self):
	  return  u'%s' % (self.descripcion)
	  self.descripcion = self.descripcion.upper()


	class Meta:
		ordering = ["descripcion"]
		db_table = 'ref_people'
		app_label = 'preventivos'

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefPeople, self).save(force_insert, force_update)

class RefTipoDelitos(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length = 50)

	def __str__(self):
		return u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()

	def save(self, force_insert = False, force_update = False):
		self.descripcion = self.descripcion.upper()
		super(RefTipoDelitos, self).save(force_insert,force_update)

	class Meta:
		ordering =["descripcion"]
		db_table = 'ref_tipo_delito'
		app_label = 'preventivos'

class RefDelito(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=50)
	tipo_delito = models.ForeignKey('RefTipoDelitos', on_delete=models.PROTECT)

	def __str__(self):
		return u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()

	def save(self, force_insert = False, force_update = False):
		self.descripcion = self.descripcion.upper()
		super(RefDelito, self).save(force_insert,force_update)

	class Meta:
		unique_together=('descripcion','tipo_delito')
		ordering = ["descripcion"]
		db_table = 'ref_delito'
		app_label = 'preventivos'

class RefOcupacion(models.Model):
	id = models.AutoField(primary_key= True)
	descripcion = models.CharField(max_length=80,unique = True)

	def __str__(self):
		return u'%s' % (self.descripcion.upper())
		

	def save(self, force_insert=False,force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefOcupacion, self).save(force_insert,force_update)

	class Meta:
		ordering = ['descripcion']
		db_table = 'ref_ocupacion'
		app_label = 'preventivos'


class RefTrademark(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=100,unique = True)

	def __str__(self):
		return u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()

	def save(self, force_insert=False,force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefTrademark, self).save(force_insert,force_update)

	class Meta:
		ordering = ['descripcion']
		db_table = 'ref_trademark'
		app_label = 'preventivos'

class RefTiposarmas(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=100,unique = True)

	def __str__(self):
		return u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()

	def save(self, force_insert=False,force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefTiposarmas, self).save(force_insert,force_update)

	class Meta:
		ordering = ['descripcion']
		db_table = 'ref_tiposarmas'
		app_label = 'preventivos'

class RefSubtiposa(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField("Ingrese Sub-Tipo :", max_length=100)
	tipo = models.ForeignKey(RefTiposarmas,related_name='tiposub',on_delete=models.PROTECT)


	def __str__(self):
		return  u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()


	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefSubtiposa, self).save(force_insert, force_update)

	class Meta:
		unique_together=('descripcion','tipo',)
		db_table = 'ref_subtiposa'
		ordering = ["descripcion"]
		app_label = 'preventivos'

class RefSistemadis(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=100,unique=True)


	def __str__(self):
		return  u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()


	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefSistemadis, self).save(force_insert, force_update)

	class Meta:
		unique_together=('descripcion',)
		db_table = 'ref_sistemadis'
		ordering = ["descripcion"]
		app_label = 'preventivos'



class RefItems(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=100,unique = True)

	def __str__(self):
		return u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()

	def save(self, force_insert=False,force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefItems, self).save(force_insert,force_update)

	class Meta:
		ordering = ['descripcion']
		db_table = 'ref_items'
		app_label = 'preventivos'

class RefCategory(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField("Ingrese Categoria :", max_length=100)
	rubro = models.ForeignKey(RefItems,related_name='rubcategory',on_delete=models.PROTECT)


	def __str__(self):
		return  u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()


	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefCategory, self).save(force_insert, force_update)

	class Meta:
		unique_together=('descripcion','rubro',)
		db_table = 'ref_category'
		ordering = ["descripcion"]
		app_label = 'preventivos'

class RefBarrios(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=100)
	ciudad = models.ForeignKey('RefCiudades',on_delete=models.PROTECT)

	def __str__(self):
		return u'%s' %  (self.descripcion)
		self.descripcion = self.descripcion.upper()


	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefBarrios, self).save(force_insert, force_update)

	class Meta:
		unique_together = ('descripcion','ciudad',)
		ordering = ["descripcion"]
		db_table = 'ref_barrios'
		app_label = 'preventivos'


class RefCalles(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=150)
	ciudad = models.ForeignKey('RefCiudades', related_name="ciucalle", on_delete=models.PROTECT)


	def __str__(self):
		return  u'%s' %  (self.descripcion)
		self.descripcion = self.descripcion.upper()

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(RefCalles, self).save(force_insert, force_update)

	class Meta:
		app_label = 'preventivos'
		unique_together = ('descripcion','ciudad',)
		ordering = ["descripcion"]
		db_table = 'ref_calles'

class RefAutoridad(models.Model):
	id = models.AutoField(primary_key = True)
	descripcion = models.CharField(max_length = 80)
	ciudades = models.ManyToManyField('RefCiudades', related_name="ciu_autori", blank = True)
	email = models.EmailField("e mail",max_length = 300)

	def __str__(self):
		return self.descripcion
		self.descripcion = self.descripcion.upper()

	def save(self, force_insert = False, force_update = False):
		self.descripcion = self.descripcion.upper()
		super(RefAutoridad, self).save(force_insert, force_update)

	class Meta:
		ordering = ['descripcion']
		db_table = 'ref_autoridad'
		app_label = 'preventivos'

class RefTipoJerarquia(models.Model):
	id = models.AutoField(primary_key = True)
	descripcion = models.CharField(max_length = 45)

	def __str__(self):
		return u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()

	class Meta:
		ordering = ['descripcion']
		db_table = 'ref_tipo_jerarquia'
		app_label = 'preventivos'

class RefDivisionJerarquia(models.Model):
	id = models.AutoField(primary_key = True)
	descripcion = models.CharField(max_length = 45)

	def __str__(self):
		return u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()

	class Meta:
		ordering = ['descripcion']
		db_table = 'ref_division_jerarquia'
		app_label = 'preventivos'

class RefJerarquias(models.Model):
	id = models.AutoField(primary_key = True)
	descripcion = models.CharField(max_length = 45)
	ref_tipo_jerarquia = models.ForeignKey('RefTipoJerarquia',on_delete = models.PROTECT)
	ref_division_jerarquia = models.ForeignKey('RefDivisionJerarquia', on_delete = models.PROTECT)

	def __str__(self):
		return u'%s' % (self.descripcion)
		self.descripcion = self.descripcion.upper()

	class Meta:
		ordering = ['descripcion']
		db_table = 'ref_jerarquias'
		app_label = 'preventivos'

class RefSexo(models.Model):
	id = models.AutoField(primary_key = True)
	Sexo_opciones=(
	('1','Femenino'),
	('2','Masculino'),
	)
	descripcion = models.CharField(max_length = 10, choices=Sexo_opciones)

	def __str__(self):
		return u'%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']
		db_table = 'ref_sexo'
		app_label = 'preventivos'

class RefEstadosciv(models.Model):
	id = models.AutoField(primary_key = True)
	civil_opciones=(
	('0','NO REGISTRA'),('1','SOLTERO'),('2','CONCUBINO'),('3','CASAD0'),('4','DIVORCIADO'),('5','VIUDO'),('6','SEPARADO'),)
	descripcion = models.CharField(max_length = 10, choices=civil_opciones)

	def __str__(self):
		return u'%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']
		db_table = 'ref_estadociv'
		app_label = 'preventivos'

class RefTipoDocumento(models.Model):
	id = models.AutoField(primary_key = True)
	Doc_opciones=(
	('1','DNI'),
	('2','LC'),
	('3','LE'),
	('4','CI'),
	('5','PAS'),
	('6','NO POSEE'),
	)
	descripcion = models.CharField(max_length = 8, choices= Doc_opciones)

	def __str__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']
		db_table = 'ref_tipodocumento'
		app_label = 'preventivos'

class RefEstudios(models.Model):
	id = models.AutoField(primary_key=True)
	Estudios_opt=(('1','PRIMARIO'),('2','SECUNDARIO'),('3','TERCIARIO'),('4','UNIVERSITARIO'),)
	descripcion = models.CharField(max_length = 13, choices= Estudios_opt)


	def __str__(self):
		return u'%s' %  (self.descripcion)
		self.descripcion = self.descripcion.upper()


	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(Estudios, self).save(force_insert, force_update)

	class Meta:
		ordering = ["descripcion"]
		db_table = 'ref_estudios'
		app_label = 'preventivos'

class Personas(models.Model):
	id = models.AutoField(primary_key = True)
	apellidos = models.CharField(max_length = 100,verbose_name='apellidos')
	nombres = models.CharField(max_length = 150,verbose_name='nombres')
	tipo_doc = models.ForeignKey('RefTipoDocumento', verbose_name='tipo documento',on_delete = models.PROTECT)
	nro_doc = models.CharField(max_length=50,unique=True)
	ciudad_nac = models.ForeignKey('RefCiudades',  blank = True, null = True,related_name='ciudad_nac', on_delete = models.PROTECT)
	pais_nac =models.ForeignKey('RefPaises',  blank = True, null = True,related_name='pais_nac', on_delete = models.PROTECT)
	ciudad_res = models.ForeignKey('RefCiudades', blank = True, null = True,related_name='ciudad_res', on_delete = models.PROTECT)
	sexo_id =  models.ForeignKey('RefSexo', on_delete = models.PROTECT)
	ocupacion = models.ForeignKey('RefOcupacion',blank = True, null = True,on_delete = models.PROTECT)
	cuit = models.CharField(max_length=11,default=0,blank = True, null = True)
	celular = models.CharField(max_length= 100,blank = True, null = True)
	fecha_nac = models.DateField()
	estado_civil=models.ForeignKey('RefEstadosciv',blank = True, null = True,on_delete = models.PROTECT)
	alias = models.CharField(max_length=150,blank = True, null = True)
	"""
	emails=models.CharField(max_length=300,blank = True, null = True)
	redsociales=models.CharField(max_length=300,blank = True, null = True)
	condicionlaboral= models.IntegerField()
	estudios=models.ForeignKey('RefEstudios',blank = True, null = True,on_delete = models.PROTECT)
	domiciliolab=models.CharField(max_length=300,blank = True, null = True)
	horariolab=models.CharField(max_length=100,blank = True, null = True)
	otrasactividades=models.CharField(max_length=500,blank = True, null = True)
	horalugaractivi=models.CharField(max_length=100,blank = True, null = True)
	"""

	def __str__(self):
		return  u'%s %s' % (self.apellidos, self.nombres)

	def save(self, force_insert = False, force_update = False):
		self.apellidos = self.apellidos.upper()
		self.nombres = self.nombres.upper()
		super(Personas, self).save(force_insert, force_update)

	class Meta:
		unique_together=('tipo_doc','nro_doc','apellidos','nombres',)
		ordering = ['apellidos']
		db_table = 'personas'
		app_label = 'preventivos'

class Actuantes(models.Model):
	id = models.AutoField(primary_key=True)
	funcion = models.IntegerField()
	documento = models.IntegerField(unique=True)
	apeynombres = models.CharField(max_length=250)
	jerarquia_id = models.ForeignKey('RefJerarquias', on_delete=models.PROTECT)
	persona_id = models.ForeignKey('Personas', on_delete=models.PROTECT)
	unidadreg_id = models.ForeignKey('UnidadesRegionales', on_delete=models.PROTECT)
	dependencia_id = models.ForeignKey('Dependencias', on_delete=models.PROTECT)

	def __str__(self):
		return u'%s ' % (self.apeynombres)

	def save(self, force_insert = False, force_update = False):
		self.documento = self.documento
		self.apeynombres = self.apeynombres.upper()
		super(Actuantes, self).save(force_insert, force_update)

	class Meta:
		ordering = ['documento']
		db_table = 'actuantes'
		app_label = 'preventivos'

class Personal(models.Model):
	id = models.AutoField(primary_key=True)
	persona_id = models.OneToOneField('Personas', unique=True,on_delete=models.PROTECT)
	legajo = models.CharField(max_length=6)
	credencial = models.IntegerField()
	nro_cuenta_bco = models.CharField(max_length=20)
	nro_seros = models.CharField(max_length=15)

	def __str__(self):
		return u'%s' % (self.id)

	class Meta:

		ordering = ['id']
		db_table = 'personal'
		app_label = 'preventivos'

class RefComunidades(models.Model):
	id = models.AutoField(primary_key = True)
	Zonas_opciones=(
	('1','Urbana'),
	('2','Sub-urbana'),
	('3','Rural'),
	('4','Costa'),
	)
	descripcion = models.CharField(max_length = 10, choices= Zonas_opciones)

	def __str__(self):
		return u'%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']
		db_table = 'ref_comunidades'
		app_label = 'preventivos'

class Preventivos(models.Model):
	id = models.AutoField(primary_key=True)
	nro = models.PositiveIntegerField(verbose_name='Nro. :',validators=[MinValueValidator(1),MaxValueValidator(9999999)])
	anio = models.PositiveIntegerField(verbose_name='Año :',validators=[MinValueValidator(2012),MaxValueValidator(2025)])
	caratula = models.CharField(max_length=250)
	fecha_carga = models.DateTimeField(default=0)
	fecha_denuncia = models.DateTimeField(default=0)
	fecha_autorizacion = models.DateTimeField(null=True)
	fecha_cierre = models.DateTimeField(null=True)
	actuante = models.ForeignKey('Actuantes', verbose_name='Actuante', related_name='Actuante', on_delete=models.PROTECT)
	preventor = models.ForeignKey('Actuantes', verbose_name='Preventor', related_name='Preventor', on_delete=models.PROTECT)
	dependencia = models.ForeignKey('Dependencias',blank=True,null=True, on_delete=models.DO_NOTHING)
	autoridades = models.ManyToManyField('RefAutoridad',blank=True)
	sendwebservice = models.IntegerField(default=0)
	reenviado = models.BooleanField(default=False)
	fecha_envio = models.DateTimeField(null=True)
	autoriza = models.CharField(max_length = 10,blank=True,null=True)
	aforo = models.IntegerField(null=True)


	def __str__(self):
		return u'%s %s %s %s' % (self.id,self.caratula,self.actuante,self.preventor)

	def save(self, force_insert = False, force_update = False):
		self.caratula=self.caratula.upper()
		super(Preventivos, self).save(force_insert, force_update)

	def has_hecho(self):
		try:
			self.hecho
			return True
		except:
			return False

	class Meta:
		ordering = ['nro','anio','dependencia']
		db_table = 'preventivos'
		app_label = 'preventivos'

class RefModosHecho(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=80)
	delito = models.ForeignKey(RefDelito,on_delete=models.PROTECT)
	def __str__(self):
		return u'%s' % (self.descripcion)
			 # %s  ,self.delito)

	def save(self, force_insert = False, force_update = False):
		self.descripcion=self.descripcion.upper()
		super(RefModosHecho, self).save(force_insert, force_update)

	class Meta:
		unique_together=('descripcion','delito',)
		ordering = ['id']
		db_table = 'ref_modos_hecho'
		app_label = 'preventivos'

class RefMotivosHecho(models.Model):
	id = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=80, unique=True)
	def __str__(self):
		return u'%s' % unicode(self.descripcion)
	class Meta:
		ordering = ['id']
		db_table = 'ref_motivos_hecho'
		app_label = 'preventivos'



class Hechos(models.Model):
	fecha_carga=models.DateTimeField(blank=True,null=True)
	descripcion=models.CharField(max_length=2000,blank=True,null=True)
	preventivo=models.OneToOneField('Preventivos', on_delete=models.PROTECT,related_name='hecho')
	motivo=models.ForeignKey('RefMotivosHecho', null=False, on_delete=models.PROTECT)
	fecha_desde=models.DateTimeField()
	fecha_hasta=models.DateTimeField()
	fecha_esclarecido=models.DateTimeField(null=True)

	def __str__(self):
		return u'%s %s' % (self.preventivo,self.descripcion)

	def save(self, force_insert = False, force_update = False):
		#self.descripcion=self.descripcion.upper()
		super(Hechos, self).save(force_insert, force_update)

	def has_lugar(self):
		try:
			self.lugar_hecho
			return True
		except:
			return False

	class Meta:
		ordering = ['fecha_carga','preventivo',]
		db_table = 'hechos'
		app_label = 'preventivos'

class HechosDelito(models.Model):
	id = models.AutoField(primary_key=True)
	hechos = models.ForeignKey('Hechos',related_name='hechos', on_delete=models.DO_NOTHING)
	refdelito = models.ForeignKey('RefDelito',related_name='delis', on_delete=models.DO_NOTHING)
	refmodoshecho = models.ForeignKey('RefModosHecho', related_name='modus', null=True, blank=True, on_delete=models.DO_NOTHING)
	borrado = models.CharField(max_length=1,null=True, blank=True)

	def __str__(self):
		return u'%s' % (self.refdelito.descripcion)

	def save(self, force_insert = False, force_update = False):
		super(HechosDelito, self).save(force_insert)

	class Meta:
		ordering = ['id']
		db_table = 'hechos_delito'
		unique_together = ('hechos','refdelito','refmodoshecho',)
		app_label = 'preventivos'


class PersInvolucradas(models.Model):
	fcio_opciones=(('si','SI'),('no','NO'),)
	id = models.AutoField(primary_key=True)
	hechos = models.ForeignKey('Hechos',related_name='involu', on_delete=models.DO_NOTHING)
	roles = models.ForeignKey('RefPeople',related_name='rol',default=0, on_delete=models.DO_NOTHING)
	persona = models.ForeignKey('Personas',related_name='perso', on_delete=models.DO_NOTHING)
	juridica =models.CharField(max_length=2,choices=fcio_opciones,blank=True,default="no")
	razon_social = models.CharField(max_length=150,null=True,blank=True)
	menor =  models.CharField(max_length=2,choices=fcio_opciones,blank=True,default="no")
	detenido = models.CharField(max_length=2,choices=fcio_opciones,blank=True,default="si")
	tentativa = models.CharField(max_length=2,choices=fcio_opciones,blank=True,default="no")
	infraganti =models.CharField(max_length=2,choices=fcio_opciones,blank=True,default="no")
	fechahoradetencion=models.DateTimeField(null=True,blank=True)
	fechahoralibertad=models.DateTimeField(null=True,blank=True)
	cargado_prev=models.BooleanField(default=False)
	ampliacion=models.ForeignKey('Ampliacion',blank=True,null=True, on_delete=models.DO_NOTHING)
	cuit=models.ForeignKey('RefTipoDocumento', verbose_name='cuit',null=True,blank=True, on_delete=models.DO_NOTHING)
	nrocuit=models.CharField(max_length=11,default=0,unique=True)

	def __str__(self):
		return u'%s' % (self.persona)

	def save(self, force_insert = False, force_update = False):
		self.razon_social=self.razon_social.upper()
		super(PersInvolucradas, self).save(force_insert, force_update)

	class Meta:
		unique_together = ('hechos','persona','roles','cargado_prev','ampliacion',)
		ordering = ['id']
		db_table = 'persinvolucradas'
		app_label = 'preventivos'

class Padres(models.Model):
	id=models.AutoField(primary_key=True)
	persona = models.ForeignKey('Personas',related_name='padre',on_delete=models.DO_NOTHING)
	padre_nombres=models.CharField(max_length=150,null=True,blank=True,default="")
	padre_apellidos=models.CharField(max_length=100,null=True,blank=True,default="")
	padre_vive = models.BooleanField(default=True)
	madre_apellidos=models.CharField(max_length=100,null=True,blank=True,default="")
	madre_nombres=models.CharField(max_length=150,null=True,blank=True,default="")
	madre_vive=models.BooleanField(default=True)


	def __str__(self):
		return u'%s %s %s %s %s' % (self.padre_nombres,self.padre_apellidos,self.madre_nombres,self.madre_apellidos,self.persona)

	def save(self, force_insert = False, force_update = False):
		self.padre_apellidos=self.padre_apellidos.upper() if self.padre_apellidos else ""
		self.padre_nombres=self.padre_nombres.upper() if self.padre_nombres else ""
		self.madre_apellidos=self.madre_apellidos.upper() if self.madre_apellidos else ""
		self.madre_nombres=self.madre_nombres.upper() if self.madre_nombres else ""
		super(Padres, self).save(force_insert, force_update)

	class Meta:
		unique_together=('persona','padre_nombres','padre_apellidos','madre_nombres','madre_apellidos',)
		ordering = ['id']
		db_table = 'padres'
		app_label = 'preventivos'
		get_latest_by = 'id'

class Detenidos(models.Model):
	id=models.AutoField(primary_key=True)
	persona = models.ForeignKey(Personas,on_delete=models.DO_NOTHING )
	fechahoradetencion=models.DateTimeField(null=True,blank=True)
	fechahoralibertad=models.DateTimeField(null=True,blank=True)
	libertad=models.CharField(max_length=1,null=True, blank=True)
	hechos = models.ForeignKey(Hechos,on_delete=models.DO_NOTHING)
	observaciones= models.CharField(max_length=800,null=True,blank=True)
	borrado = models.CharField(max_length=1,null=True, blank=True)


	def __str__(self):
		return u'%s' % (self.persona)

	def save(self, force_insert = False, force_update = False):
		super(Detenidos, self).save(force_insert, force_update)

	class Meta:
		unique_together=('hechos','persona',)
		ordering = ['id']
		db_table = 'detenidos'
		app_label = 'preventivos'

class Domicilios(models.Model):
	personas = models.ForeignKey('Personas',related_name='persodom',on_delete=models.DO_NOTHING)
	ref_ciudades = models.ForeignKey(RefCiudades,blank = True, null = True,on_delete=models.DO_NOTHING)
	barrio_codigo = models.ForeignKey(RefBarrios,blank = True, null = True,on_delete=models.DO_NOTHING)
	calle = models.ForeignKey(RefCalles,related_name = 'domicilio',blank = True, null = True,on_delete=models.DO_NOTHING)
	altura = models.CharField(max_length=4,default="0",blank = True)
	entre = models.ForeignKey(RefCalles,related_name = 'interseccion', blank = True, null = True,on_delete=models.DO_NOTHING)
	fecha_desde = models.DateField(blank = True, null = True)
	fecha_hasta = models.DateField(blank = True, null = True)
	fecha_actualizacion = models.DateField(blank = True, null = True)
	tipos_domicilio = models.ForeignKey(RefHogares,blank = True, null = True,on_delete=models.DO_NOTHING)
	ref_zona = models.ForeignKey(RefComunidades,blank = True, null = True,on_delete=models.DO_NOTHING)
	departamento = models.CharField(max_length = 10,blank = True, null = True,default="")
	piso = models.CharField(max_length=4,default="0",blank = True)
	lote =models.CharField(max_length=4,default="0",blank = True)
	sector = models.CharField(max_length = 10,blank = True, null = True,default="")
	manzana = models.CharField(max_length=4,default="0",blank = True)
	calle2 = models.CharField(max_length=80,blank= True, null=True)
	
	def __str__(self):
		
		str_domicilio = "" 
		if self.barrio_codigo:
			str_domicilio = str_domicilio + self.barrio_codigo.descripcion
		if self.calle and self.entre and self.altura:
			str_domicilio = str_domicilio +  " %s %s y %s " % (self.calle,self.altura,self.entre)
		elif self.calle and self.entre and not self.altura:
			str_domicilio = str_domicilio +  " %s y %s " % (self.calle,self.entre)
		elif self.calle and self.altura and not self.entre:
			str_domicilio = str_domicilio +  " %s %s " % (self.calle,self.altura)
		elif self.calle2:
			str_domicilio = str_domicilio +  " %s " % (self.calle2.upper())
		else: 
			str_domicilio = "Sin datos especificos."
		if self.manzana and not self.manzana == '0':
			str_domicilio = str_domicilio + " Mza. %s " % self.manzana
		if self.lote and not self.lote == '0':
			str_domicilio = str_domicilio + " Lte. %s " % self.lote


		return str_domicilio
		
		

	class Meta:
		unique_together=('personas','ref_ciudades','barrio_codigo','fecha_desde','calle','altura')
		ordering = ['-fecha_desde']
		db_table = 'domicilios'
		app_label = 'preventivos'
		get_latest_by = 'id'

class Lugar(models.Model):
	calle = models.ForeignKey(RefCalles,related_name='calle_hecho',on_delete=models.PROTECT,blank=True,null = True)
	altura = models.IntegerField(default='0',blank=True,null = True)
	latitud = models.CharField(max_length=50)
	longitud = models.CharField(max_length=50)
	barrio = models.ForeignKey('RefBarrios',on_delete = models.PROTECT,blank = True, null = True)
	tipo_lugar = models.ForeignKey('RefLugares',on_delete=models.PROTECT)
	cond_climaticas = models.ManyToManyField('RefCondclimas',related_name='condiciones',blank=True)
	hecho = models.OneToOneField('Hechos', related_name='lugar_hecho',on_delete = models.PROTECT)
	lote = models.CharField(default='0',max_length = 45,blank=True,null = True)
	manzana = models.CharField(default='0',max_length = 45,blank=True,null = True)
	sector = models.CharField(default='',max_length = 45,blank=True,null = True)
	departamento = models.CharField(default='',max_length = 45,blank=True,null = True)
	piso = models.CharField(default='0',max_length = 45,blank=True,null = True)
	delito = models.ForeignKey('RefDelito',blank=True, null = True,on_delete = models.PROTECT)
	zona = models.ForeignKey('RefComunidades',on_delete = models.PROTECT)
	nro_casa = models.IntegerField(default='0',blank=True,null = True)
	edificio = models.CharField(default='',max_length = 45,blank=True,null = True)
	escalera = models.CharField(default='',max_length = 45,blank=True,null = True)
	dependencia = models.ForeignKey('Dependencias',null=True,blank=True,on_delete = models.PROTECT)

	"""def __str__(self):
		return u'%s %s %s %s' % (self.calle,self.barrio,self.tipo_lugar,self.cond_climaticas)"""
	def save(self, force_insert = False, force_update = False):
		super(Lugar, self).save(force_insert,force_update)

	class Meta:
		ordering = ['id']
		db_table = 'lugar'
		app_label = 'preventivos'

#modelo de elementos
class RefTipoelementos(models.Model):
	id=models.AutoField(primary_key=True)
	elementos=(
	('1','DENUNCIADOS'),
	('2','SECUESTRADOS'),
	('3','UTILIZADOS'), ('4','UTILIZADOS/SECUESTRADOS'),
	)
	descripcion = models.CharField(max_length = 50,choices= elementos)

	def __str__(self):
		return u'%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']
		db_table = 'reftipoelementos'
		app_label = 'preventivos'

class RefUnidadmedidas(models.Model):
	id=models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length =30)

	def __str__(self):
		return u'%s' % (self.descripcion)

	def save(self, force_insert = False, force_update = False):
		self.descripcion=self.descripcion.upper()
		super(RefUnidadmedidas, self).save(force_insert,force_update)

	class Meta:
		unique_together=('descripcion',)
		ordering = ['descripcion']
		db_table = 'refunidadmedidas'
		app_label = 'preventivos'
"""
class RefCategorias(models.Model):
	id=models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length =100)

	def __str__(self):
		return u'%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']
		db_table = 'refcategorias'
"""
class Elementos(models.Model):
	id=models.AutoField(primary_key=True)
	categoria=models.ForeignKey('RefCategory',on_delete=models.PROTECT)
	rubro = models.ForeignKey(RefItems,on_delete=models.PROTECT)
	tipo=models.ForeignKey('RefTipoelementos',on_delete=models.PROTECT)
	unidadmed=models.ForeignKey('RefUnidadmedidas',on_delete=models.PROTECT)
	hechos=models.ForeignKey('Hechos',related_name='eleinvolu',on_delete=models.PROTECT)
	descripcion=models.CharField(max_length=150)
	cantidad=models.IntegerField()
	fecha=models.DateTimeField(auto_now=True)
	borrado = models.CharField(max_length=1,null=True, blank=True)
	observaciones= models.CharField(max_length=800,null=True,blank=True)
	cargado_prev=models.BooleanField(default=False)
	ampliacion=models.ForeignKey('Ampliacion',blank=True,null=True,on_delete=models.DO_NOTHING)

	def __str__(self):
		return u'%s %s %s %s %s %s' % (self.id,self.categoria,self.rubro,self.descripcion, self.hechos, self.observaciones)
		self.descripcion = self.descripcion.upper()


	def save(self, force_insert = False, force_update = False):
		self.descripcion = self.descripcion.upper()
		super(Elementos, self).save(force_insert, force_update)

	class Meta:

		ordering = ['tipo','descripcion']
		db_table = 'elementos'
		app_label = 'preventivos'


class Armas(models.Model):
	id=models.AutoField(primary_key=True)
	tipos=models.ForeignKey('RefTiposarmas', on_delete=models.PROTECT)
	subtipos=models.ForeignKey('RefSubtiposa',on_delete=models.PROTECT)
	sistema_disparo=models.ForeignKey('RefSistemadis',on_delete=models.PROTECT,blank=True,null=True)
	marcas=models.ForeignKey('RefTrademark',on_delete=models.PROTECT,blank=True,null=True)
	modelo=models.CharField(max_length=100,blank=True,null=True)
	calibre=models.CharField(max_length=10,blank=True,null=True)
	nro_arma=models.CharField(max_length=50,blank=True,null=True)
	nro_doc = models.IntegerField(blank=True,null=True)
	propietario=models.CharField(max_length=100,blank=True,null=True)
	fecha_carga=models.DateTimeField(auto_now=True)

	def __str__(self):
		return u'%s' % (self.tipos)

	def save(self, force_insert = False, force_update = False):

		super(Armas, self).save(force_insert, force_update)

	class Meta:
		#unique_together=['nro_arma',]
		ordering = ['tipos','subtipos','marcas',]
		db_table = 'armas'
		app_label = 'preventivos'

class Elementosarmas(models.Model):
	id=models.AutoField(primary_key=True)
	idelemento=models.ForeignKey('Elementos',related_name='relelem',on_delete=models.DO_NOTHING)
	idarma=models.ForeignKey('Armas',on_delete=models.DO_NOTHING)

	def __str__(self):
		return u'%s' % (self.idelemento)
	def save(self, force_insert = False, force_update = False):

		super(Elementosarmas, self).save(force_insert, force_update)

	class Meta:

		ordering = ['idelemento',]
		db_table = 'elementosarmas'
		app_label = 'preventivos'

"""
#modelo de elementos automotores
class RefMarcascars(models.Model):
	id = models.AutoField(primary_key = True)
	descripcion = models.CharField(max_length = 50)

	def __str__(self):
	  return  u'%s' % (self.descripcion)
	  self.descripcion = self.descripcion.upper()


	class Meta:
		ordering = ["descripcion"]
		db_table = 'refmarcascars'
"""

class Vehiculos(models.Model):
	id = models.AutoField(primary_key = True)
	dominio=models.CharField(max_length=10,null=True,blank=True)
	anio=models.IntegerField(null=True,blank=True)
	nmotor=models.CharField(max_length=100, null=True,blank=True)
	nchasis=models.CharField(max_length=100,null=True,blank=True)
	tipov=models.CharField(max_length=20)
	modelo=models.CharField(max_length=50,null=True,blank=True)
	idmarca=models.ForeignKey('RefTrademark',on_delete=models.PROTECT,null=True,blank=True)
	fecha_carga=models.DateTimeField(auto_now=True)
	nro_doc = models.IntegerField(null=True,blank=True)
	propietario = models.CharField(max_length=100,null=True,blank=True)
	def __str__(self):
		return u'%s' % (self.dominio)

	def save(self, force_insert = False, force_update = False):
		self.dominio        = self.dominio.upper()
		self.nmotor         = self.nmotor.upper() if self.nmotor else self.nmotor
		self.nchasis        = self.nchasis.upper() if self.nchasis else self.nchasis
		self.tipov          = self.tipov.upper()
		self.modelo         = self.modelo.upper()
		self.propietario    = self.propietario.upper()
		super(Vehiculos, self).save(force_insert, force_update)


	class Meta:
		ordering = ['dominio',]
		db_table = 'vehiculos'
		app_label = 'preventivos'


class Elementoscars(models.Model):
	id=models.AutoField(primary_key=True)
	idelemento=models.ForeignKey('Elementos',on_delete=models.DO_NOTHING)
	idvehiculo=models.ForeignKey('Vehiculos',on_delete=models.DO_NOTHING)

	def save(self, force_insert = False, force_update = False):
		super(Elementoscars, self).save(force_insert, force_update)

	class Meta:

		db_table = 'elementoscars'
		app_label = 'preventivos'

class RefTipodrogas(models.Model):
	id = models.AutoField(primary_key = True)
	typedrogas=(
	('1','Marihuana'),
	('2','Cocaina'),
	('3','Inhalantes'),
	('4','Paco'),
	('5','Energizantes'),
	('6','Extasis'),('7','Otros'),
	)
	descripcion = models.CharField(max_length = 50, choices= typedrogas)

	def __str__(self):
	  return  u'%s' % (self.descripcion)
	  self.descripcion = self.descripcion.upper()


	class Meta:
		ordering = ["descripcion"]
		db_table = 'reftipodrogas'
		app_label = 'preventivos'



class Drogas(models.Model):
	id = models.AutoField(primary_key = True)
	descripcion=models.CharField(max_length=100)
	idtipo=models.ForeignKey('reftipodrogas',on_delete=models.DO_NOTHING)
	fecha_carga=models.DateTimeField(auto_now=True)
	def __str__(self):
		return u'%s' % (self.descripcion)

	def save(self, force_insert = False, force_update = False):
		super(Drogas, self).save(force_insert, force_update)

	class Meta:
		ordering = ['descripcion',]
		db_table = 'drogas'
		app_label = 'preventivos'


class Elementosdrogas(models.Model):
	id=models.AutoField(primary_key=True)
	idelemento=models.ForeignKey('Elementos',on_delete=models.DO_NOTHING)
	droga=models.ForeignKey('Drogas',on_delete=models.DO_NOTHING)

	class Meta:
		app_label = 'preventivos'

class Ampliacion(models.Model):
	id                  = models.AutoField(primary_key = True)
	fecha               = models.DateTimeField(auto_now=True)
	titulo              = models.CharField(max_length=100)
	autoridades         = models.ManyToManyField('RefAutoridad',blank=True)
	descripcion         = models.CharField(max_length=2000)
	preventivo          = models.ForeignKey('Preventivos',related_name='ampli',on_delete=models.DO_NOTHING)
	fecha_autorizacion  = models.DateTimeField(null=True,blank=True)
	cierre_causa        = models.BooleanField(default=False)
	fecha_cierre        = models.DateTimeField(blank=True,null=True)
	fin_edicion         = models.BooleanField(default=False)
	sendwebservice      = models.IntegerField(default=0)

	def __str__(self):
		return u'%s' % (self.descripcion)

	def save(self, force_insert = False, force_update = False):
		super(Ampliacion,self).save(force_insert,force_update)

	class Meta:
		ordering    = ['id']
		db_table    = 'ampliacion'
		app_label = 'preventivos'

"""
class ViolenciaFliar(models.Model):
	sino_opciones=(('1','SI'),('2','NO'),)
	id=models.AutoField(primary_key=True)
	fecha = models.DateTimeField()
	fecha_carga=models.DateTimeField()
	intervencionsavd= models.IntegerField()
	intervencionotro= models.IntegerField()
	intervencioncual=models.CharField(max_length=250,blank=True,null=True)
	otrosdatosinteres=models.CharField(max_length=2000,blank=True,null=True)
	hechos = models.ForeignKey('Hechos',related_name='hechovif',blank=True,null=True)

	def __str__(self):
		return u'%s' % (self.hechos)

	def save(self, force_insert = False, force_update = False):
		super(ViolenciaFliar,self).save(force_insert,force_update)

	class Meta:
		ordering    = ['id']
		db_table    = 'violenciafliar'
		unique_together = ('fecha_carga','hechos')

class PerInvolViolenfliar(models.Model):
	id = models.AutoField(primary_key=True)
	violencia = models.ForeignKey('ViolenciaFliar',related_name='involuvif')
	roles = models.ForeignKey('RefPeople',related_name='rolvif',default=0)
	persona = models.ForeignKey('Personas',related_name='persovif')
	juridica = models.IntegerField(default=0)
	razon_social = models.CharField(max_length=250,null=True,blank=True)
	cargo = models.CharField(max_length=250,null=True,blank=True)
	pidereserva=models.IntegerField(default=0)
	composiciongrupofliar=models.CharField(max_length=200,null=True,blank=True)
	cgfconviven=models.IntegerField(default=0)
	vinculodenunciado=models.CharField(max_length=20,null=True,blank=True)
	vdconviven=models.IntegerField(default=0)
	vinculovictima=models.CharField(max_length=20,null=True,blank=True)
	teldomalternativos=models.CharField(max_length=1000,null=True,blank=True)
	teldomfliaprimaria=models.CharField(max_length=1000,null=True,blank=True)
	telconfigurasreferentes=models.CharField(max_length=1000,null=True,blank=True)
	cargado_viol=models.IntegerField(default=0)
	ampliacion=models.ForeignKey('Ampliacion',blank=True,null=True)

	def __str__(self):
		return u'%s' % (self.persona)

	def save(self, force_insert = False, force_update = False):
		#self.razon_social=self.razon_social.upper()
		super(PerInvolViolenfliar, self).save(force_insert, force_update)

	class Meta:
		unique_together = ('violencia','persona','roles','cargado_viol','ampliacion',)
		ordering = ['id']
		db_table = 'persinvolviolenfliar'

class HechoViolencia(models.Model):
	id = models.AutoField(primary_key=True)
	fecha_carga=models.DateField()
	relato=models.CharField(max_length=2000,null=True,blank=True)
	lesiones=models.CharField(max_length=500,null=True,blank=True)
	consultamedica=models.CharField(max_length=500,null=True,blank=True)
	certificadomedico=models.IntegerField(default=0)
	danios=models.CharField(max_length=500,null=True,blank=True)
	amenazas=models.IntegerField(default=0)
	tipoamenazas=models.CharField(max_length=500,null=True,blank=True)
	lugardenunciado=models.CharField(max_length=500,null=True,blank=True)
	portaarmasfuego=models.IntegerField(default=0)
	lugararmas=models.CharField(max_length=500,null=True,blank=True)
	armasregistradas=models.IntegerField(default=0)
	armasusohabitual=models.IntegerField(default=0)
	otrasarmas=models.IntegerField(default=0)
	lugarotrasarmas=models.CharField(max_length=500,null=True,blank=True)
	elementosrelacionados=models.IntegerField(default=0)
	email=models.CharField(max_length=300,null=True,blank=True)
	mjstexto=models.CharField(max_length=300,null=True,blank=True)
	mjsvoz=models.CharField(max_length=300,null=True,blank=True)
	filmacion=models.CharField(max_length=100,null=True,blank=True)
	fotografias=models.CharField(max_length=100,null=True,blank=True)
	otroselementos=models.CharField(max_length=100,null=True,blank=True)
	poseevehiculo=models.IntegerField(default=0)
	patentedominio=models.CharField(max_length=10,null=True,blank=True)
	datosvehiculo=models.CharField(max_length=200,null=True,blank=True)
	medicacion=models.IntegerField(default=0)
	medicacioncual=models.CharField(max_length=200,null=True,blank=True)
	bebidas=models.IntegerField(default=0)
	sustdroga=models.IntegerField(default=0)
	sustdrogacual=models.CharField(max_length=200,null=True,blank=True)
	antpsicologicos=models.IntegerField(default=0)
	incidiohecho=models.CharField(max_length=200,null=True,blank=True)
	primeravez=models.IntegerField(default=0)
	noprimeravez=models.CharField(max_length=200,null=True,blank=True)
	otrosterceros=models.CharField(max_length=500,null=True,blank=True)
	diadenunciado=models.CharField(max_length=500,null=True,blank=True)
	violencia = models.ForeignKey('ViolenciaFliar',related_name='hechovif')

	def __str__(self):
		return u'%s' % (self.violencia)

	def save(self, force_insert = False, force_update = False):
		self.relato=self.relato.upper()
		super(HechoViolencia, self).save(force_insert, force_update)

	class Meta:
		unique_together = ('violencia','fecha_carga',)
		ordering = ['id']
		db_table = 'hechoviolencia'

class HechosTestigos(models.Model):
	id = models.AutoField(primary_key=True)
	hechosv = models.ForeignKey('HechoViolencia',related_name='hechosv',)
	nombreape = models.CharField(max_length=200,null=True,blank=True)
	dni = models.IntegerField(default=0)
	domiciliotestigo=models.CharField(max_length=200,null=True,blank=True)
	telefonos = models.CharField(max_length=200,null=True,blank=True)
	borrado = models.CharField(max_length=1,null=True, blank=True)

	def __str__(self):
		return u'%s' % (self.nombreape)

	def save(self, force_insert = False, force_update = False):
		super(HechosTestigos, self).save(force_insert)

	class Meta:
		ordering = ['id']
		db_table = 'hechos_testigos'
		unique_together = ('hechosv','nombreape','dni',)

class HistoryDenuncias(models.Model):
	id = models.AutoField(primary_key=True)
	dependencia = models.ForeignKey('Dependencias', on_delete=models.PROTECT)
	fiscalia = models.CharField(max_length=200,null=True,blank=True)
	otrolugar=models.CharField(max_length=200,null=True,blank=True)
	tipoagresion=models.CharField(max_length=200,null=True,blank=True)
	agresor=models.CharField(max_length=200,null=True,blank=True)
	agredido=models.CharField(max_length=200,null=True,blank=True)
	resultado=models.CharField(max_length=500,null=True,blank=True)
	persona = models.ForeignKey('Personas',related_name='denunvif')

	def __str__(self):
		return u'%s' % (self.dependencia)

	def save(self, force_insert = False, force_update = False):
		super(HistoryDenuncias, self).save(force_insert)

	class Meta:
		ordering = ['id']
		db_table = 'historydenuncias'

"""
class Nacionalidad(models.Model):
	idNacionalidad=models.AutoField(primary_key=True)
	descripcion=models.CharField(max_length=100)

	def __str__(self):
	  return  u'%s' % (self.descripcion)
	  self.descripcion = self.descripcion.upper()


	class Meta:
		ordering = ["descripcion"]
		db_table = 'nacionalidad'
		app_label = 'preventivos'

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(Nacionalidad, self).save(force_insert, force_update)

class Provincia(models.Model):
	idProvincia=models.AutoField(primary_key=True)
	descripcion=models.CharField(max_length=100)

	def __str__(self):
	  return  u'%s' % (self.descripcion)
	  self.descripcion = self.descripcion.upper()


	class Meta:
		ordering = ["descripcion"]
		db_table = 'provincias'
		app_label = 'preventivos'

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(Provincia, self).save(force_insert, force_update)

class Localidad(models.Model):
	idLocalidad=models.AutoField(primary_key=True)
	idProvincia=models.IntegerField()
	descripcion=models.CharField(max_length=100)

	def __str__(self):
	  return  u'%s' % (self.descripcion)
	  self.descripcion = self.descripcion.upper()


	class Meta:
		ordering = ["descripcion"]
		db_table = 'Localidad'
		app_label = 'preventivos'

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(Localidad, self).save(force_insert, force_update)

class Calles(models.Model):
	idCalle=models.AutoField(primary_key=True)
	idLocalidad=models.IntegerField()
	descripcion=models.CharField(max_length=100)

	def __str__(self):
	  return  u'%s' % (self.descripcion)
	  self.descripcion = self.descripcion.upper()


	class Meta:
		ordering = ["descripcion"]
		db_table = 'calles'
		app_label = 'preventivos'

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(Calles, self).save(force_insert, force_update)

class Comisarias(models.Model):
	idorganismo=models.AutoField(primary_key=True)
	idLocalidad=models.IntegerField()
	descripcion=models.CharField(max_length=100)

	def __str__(self):
	  return  u'%s' % (self.idorganismo)
	  self.descripcion = self.descripcion.upper()


	class Meta:
		ordering = ["descripcion"]
		db_table = 'comisarias'
		app_label = 'preventivos'

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(Comisarias, self).save(force_insert, force_update)

class Barrio(models.Model):
	idBarrio=models.AutoField(primary_key=True)
	idLocalidad=models.IntegerField()
	descripcion=models.CharField(max_length=100)

	def __str__(self):
	  return  u'%s %s' % (self.idBarrio,self.descripcion)
	  self.descripcion = self.descripcion.upper()


	class Meta:
		ordering = ["descripcion"]
		db_table = 'barrio'
		app_label = 'preventivos'

	def save(self, force_insert=False, force_update=False):
		self.descripcion = self.descripcion.upper()
		super(Barrio, self).save(force_insert, force_update)

class Estadocivil(models.Model):
	idEstadoCivil = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length = 15)

	def __str__(self):
		return u'%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']
		db_table = 'Estadocivil'
		app_label = 'preventivos'

class Tipodocumentos(models.Model):
	idtipodocumento=models.CharField(primary_key=True,max_length=5)
	descripcion = models.CharField(max_length = 11)

	def __str__(self):
		return u'%s' % (self.iddoc)

	class Meta:
		ordering = ['descripcion']
		db_table = 'Tipodocumentos'
		app_label = 'preventivos'

class RolPersonas(models.Model):
	idRolPersonas=models.CharField(primary_key=True,max_length=5)
	descripcion = models.CharField(max_length = 45)

	def __str__(self):
		return u'%s' % (self.idRolPersonas)

	class Meta:
		ordering = ['descripcion']
		db_table = 'rolpersonas'
		app_label = 'preventivos'

class TipoOcupacion(models.Model):
	idtipoocupacion=models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length = 45)

	def __str__(self):
		return u'%s' % (self.idtipoocupacion)

	class Meta:
		ordering = ['descripcion']
		db_table = 'tipocupacion'
		app_label = 'preventivos'

class EnvioPreJudicial(models.Model):
	id = models.AutoField(primary_key=True)
	fecha_autorizacion = models.DateTimeField(null=True)
	fecha_envio=models.DateTimeField(auto_now=True)
	preventivo = models.ForeignKey('Preventivos',on_delete=models.DO_NOTHING)
	user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
	enviado=models.IntegerField(default=0)
	dependencia = models.ForeignKey('Dependencias',null=True,blank=True,on_delete=models.DO_NOTHING)

	def __str__(self):
		return u'%s' % (self.fecha_envio)

	class Meta:
		ordering = ['fecha_envio']
		db_table = 'envioprejudicial'
		app_label = 'preventivos'

class EnvioAmpJudicial(models.Model):
	id = models.AutoField(primary_key=True)
	fecha_envio=models.DateTimeField(auto_now=True)
	fecha_autorizacion  = models.DateTimeField(null=True,blank=True)
	ampliacion=models.ForeignKey('Ampliacion',blank=True,null=True,on_delete=models.DO_NOTHING)
	user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
	enviado=models.IntegerField(default=0)

	def __str__(self):
		return u'%s' % (self.fecha)

	class Meta:
		ordering = ['fecha_envio']
		db_table = 'envioampjudicial'
		app_label = 'preventivos'

class CambiarContrasenia(models.Model):
	motivo 				= models.CharField(max_length=20)
	detalle_motivo 		= models.CharField(max_length=100)
	usuario_que_cambia 	= models.CharField(max_length=12)
	usuario 			= models.CharField(max_length=12)
	fecha_cambio		= models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'reset_passwords'
		app_label = 'preventivos'

class Errores(models.Model):
	usuario 			= models.ForeignKey(User,on_delete=models.DO_NOTHING)
	descripcion 		= models.CharField(max_length=150)
	fecha 				= models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'errores'
		app_label = 'preventivos'
