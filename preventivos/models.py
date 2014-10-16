#encoding:utf-8 
from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import Group,Permission,User
from django.contrib.admin.models import LogEntry
from django.db.models import signals
from django.core.validators import MinValueValidator,MaxValueValidator

class Registrouser(models.Model):
    user = models.ForeignKey(User)
    action=models.CharField(max_length=50)
    tablas = models.CharField(max_length=50)
    link = models.CharField(max_length=50)
    session=models.CharField(max_length=50)
    fecha=models.DateTimeField(auto_now=True)
    def __str__(self):  
      return '%s' % self.user  

    class Meta: 
        db_table = 'Registrouser'
       
        
   

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    ureg = models.ForeignKey('UnidadesRegionales',blank=True, null=True,)
    depe = models.ForeignKey('Dependencias',blank=True, null=True,)
    
    def __str__(self):  
      return "%s's profile" % self.user  

    class Meta: 
        db_table = 'UserProfile'
       
        
    def user_profile(sender, instance, signal, *args, **kwargs):
        # Creates user profile
        profile, new = UserProfile.objects.get_or_create(user=instance)

    signals.post_save.connect(user_profile, sender=User) 
    
   

class RefPaises(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField("Seleccione Pais :", unique=True, max_length=45L )
    

    def __unicode__(self):
      return  u'%s' % (self.descripcion)  
      self.descripcion = self.descripcion.upper()
     
    
    class Meta: 
        ordering = ["descripcion"]
        db_table = 'ref_paises'

    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefPaises, self).save(force_insert, force_update)        

class RefProvincia(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField("Ingrese Provincia :", max_length=45L)
    pais = models.ForeignKey(RefPaises,on_delete=models.PROTECT)
    

    def __unicode__(self):
        return  u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    
    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefProvincia, self).save(force_insert, force_update)

    class Meta:
        unique_together=('descripcion','pais',)
        db_table = 'ref_provincia'
        ordering = ["descripcion"]
     
class RefDepartamentos(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField("Ingrese Departamento :", unique=True, max_length=45L)
    provincia = models.ForeignKey(RefProvincia, on_delete=models.PROTECT)
       
    def __unicode__(self):
        return  u'%s' %  (self.descripcion)
        self.descripcion = self.descripcion.upper()
        
    
    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefDepartamentos, self).save(force_insert, force_update)

    class Meta:
        #unique_together=('descripcion','provincia',)
        ordering = ["descripcion"]
        db_table = 'ref_departamentos'
        
class RefCiudades(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=80L)
    departamento = models.ForeignKey('RefDepartamentos',blank=True, null=True, on_delete=models.PROTECT)
    provincia = models.ForeignKey('RefProvincia', blank=True,  null=True, on_delete=models.PROTECT)
    pais = models.ForeignKey('RefPaises', on_delete=models.PROTECT)
    lat= models.CharField(max_length=50,blank=True,null=True)
    longi= models.CharField(max_length=50,blank=True,null=True)

    def __unicode__(self):
        return  u'%s' %  (self.descripcion)
        self.descripcion = self.descripcion.upper()

    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefCiudades, self).save(force_insert, force_update)

    class Meta:
        unique_together = ('pais','provincia','departamento','descripcion',)
        ordering = ["descripcion"]
        db_table = 'ref_ciudades'

#modelo de datos de referencias de tipos de lugares en donde se cometio el hecho
class RefLugares(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100L, blank=True, unique=True)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefLugares, self).save(force_insert, force_update)
 
    class Meta:
        ordering = ["descripcion"]
        db_table = 'ref_lugares'

class RefHogares(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100L,blank=True, unique=True)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefHogares, self).save(force_insert, force_update)

    class Meta:
        ordering = ["descripcion"]
        db_table = 'ref_hogares'

class RefCondclimas(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150L,blank=True, unique=True)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefCondclimas, self).save(force_insert, force_update)        

    class Meta:
        ordering = ["descripcion"]
        db_table = 'ref_condclimas'

class UnidadesRegionales(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=80L)
    ciudad = models.ForeignKey('RefCiudades',on_delete=models.PROTECT)
     
    def __unicode__(self):
        return u'%s' %  (self.descripcion)
        self.descripcion = self.descripcion.upper()
         
 
    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(UnidadesRegionales, self).save(force_insert, force_update)
 
    class Meta:
        unique_together = ('descripcion','ciudad')
        ordering = ["descripcion"]
        db_table = 'unidades_regionales'
 
class Dependencias(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=80)
    unidades_regionales = models.ForeignKey('UnidadesRegionales', related_name="unidades", on_delete=models.PROTECT)
    ciudad = models.ForeignKey('RefCiudades',on_delete=models.PROTECT)
   
 
    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()
 
    def save(self, force_insert=False, force_update= False):
        self.descripcion = self.descripcion.upper()
        super(Dependencias, self).save(force_insert,force_update)
 
    class Meta:
        unique_together = ('descripcion','unidades_regionales','ciudad')
        ordering = ["descripcion"]
        db_table = 'dependencias'


class RefPeople(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField("Involucrados - Tipos :", null=False, unique=True, max_length=150L )
    

    def __unicode__(self):
      return  u'%s' % (self.descripcion)  
      self.descripcion = self.descripcion.upper()
     
    
    class Meta: 
        ordering = ["descripcion"]
        db_table = 'ref_people'

    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefPeople, self).save(force_insert, force_update)   

class RefTipoDelitos(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length = 50)
 
    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()
 
    def save(self, force_insert = False, force_update = False):
        self.descripcion = self.descripcion.upper()
        super(RefTipoDelitos, self).save(force_insert,force_update)
 
    class Meta:
        ordering =["descripcion"]
        db_table = 'ref_tipo_delito'
 
class RefDelito(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    tipo_delito = models.ForeignKey('RefTipoDelitos', on_delete=models.PROTECT)
 
    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()
 
    def save(self, force_insert = False, force_update = False):
        self.descripcion = self.descripcion.upper()
        super(RefDelito, self).save(force_insert,force_update)
 
    class Meta:
        unique_together=('descripcion','tipo_delito')
        ordering = ["descripcion"]
        db_table = 'ref_delito'

class RefOcupacion(models.Model):
    id = models.AutoField(primary_key= True)
    descripcion = models.CharField(max_length=80,unique = True)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    def save(self, force_insert=False,force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefOcupacion, self).save(force_insert,force_update)

    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_ocupacion'


class RefTrademark(models.Model):
    id = models.AutoField(primary_key=True)        
    descripcion = models.CharField(max_length=100,unique = True)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    def save(self, force_insert=False,force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefTrademark, self).save(force_insert,force_update)

    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_trademark'   

class RefTiposarmas(models.Model):
    id = models.AutoField(primary_key=True)        
    descripcion = models.CharField(max_length=100,unique = True)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    def save(self, force_insert=False,force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefTiposarmas, self).save(force_insert,force_update)

    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_tiposarmas'    

class RefSubtiposa(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField("Ingrese Sub-Tipo :", max_length=100L)
    tipo = models.ForeignKey(RefTiposarmas,related_name='tiposub',on_delete=models.PROTECT)
    

    def __unicode__(self):
        return  u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    
    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefSubtiposa, self).save(force_insert, force_update)

    class Meta:
        unique_together=('descripcion','tipo',)
        db_table = 'ref_subtiposa'
        ordering = ["descripcion"]

class RefSistemadis(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100,unique=True)
    

    def __unicode__(self):
        return  u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    
    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefSistemadis, self).save(force_insert, force_update)

    class Meta:
        unique_together=('descripcion',)
        db_table = 'ref_sistemadis'
        ordering = ["descripcion"]



class RefItems(models.Model):
    id = models.AutoField(primary_key=True)        
    descripcion = models.CharField(max_length=100L,unique = True)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    def save(self, force_insert=False,force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefItems, self).save(force_insert,force_update)

    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_items'    

class RefCategory(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField("Ingrese Categoria :", max_length=100L)
    rubro = models.ForeignKey(RefItems,related_name='rubcategory',on_delete=models.PROTECT)
    

    def __unicode__(self):
        return  u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()

    
    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefCategory, self).save(force_insert, force_update)

    class Meta:
        unique_together=('descripcion','rubro',)
        db_table = 'ref_category'
        ordering = ["descripcion"]

class RefBarrios(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100L)
    ciudad = models.ForeignKey('RefCiudades',on_delete=models.PROTECT)
   
    def __unicode__(self):
        return u'%s' %  (self.descripcion)
        self.descripcion = self.descripcion.upper()
         
 
    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefBarrios, self).save(force_insert, force_update)
 
    class Meta:
        unique_together = ('descripcion','ciudad',)
        ordering = ["descripcion"]
        db_table = 'ref_barrios'
       
      
class RefCalles(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150L)
    ciudad = models.ForeignKey('RefCiudades', related_name="ciucalle", on_delete=models.PROTECT)
    
    
    def __unicode__(self):
        return  u'%s' %  (self.descripcion)
        self.descripcion = self.descripcion.upper()

    def save(self, force_insert=False, force_update=False):
        self.descripcion = self.descripcion.upper()
        super(RefCalles, self).save(force_insert, force_update)

    class Meta:
        unique_together = ('descripcion','ciudad',)
        ordering = ["descripcion"]
        db_table = 'ref_calles'

class RefAutoridad(models.Model):
    id = models.AutoField(primary_key = True)
    descripcion = models.CharField(max_length = 80)
    ciudades = models.ManyToManyField('RefCiudades', related_name="ciu_autori", blank = True, null = True)
    email = models.EmailField("e mail")
 
    def __unicode__(self):
        return self.descripcion
        self.descripcion = self.descripcion.upper()
 
    def save(self, force_insert = False, force_update = False):
        self.descripcion = self.descripcion.upper()
        super(RefAutoridad, self).save(force_insert, force_update)
 
    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_autoridad'
 
class RefTipoJerarquia(models.Model):
    id = models.AutoField(primary_key = True)
    descripcion = models.CharField(max_length = 45)
 
    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()
 
    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_tipo_jerarquia'
 
class RefDivisionJerarquia(models.Model):
    id = models.AutoField(primary_key = True)
    descripcion = models.CharField(max_length = 45)
 
    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()
 
    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_division_jerarquia'
 
class RefJerarquias(models.Model):
    id = models.AutoField(primary_key = True)
    descripcion = models.CharField(max_length = 45)
    ref_tipo_jerarquia = models.ForeignKey('RefTipoJerarquia',on_delete = models.PROTECT)
    ref_division_jerarquia = models.ForeignKey('RefDivisionJerarquia', on_delete = models.PROTECT)
 
    def __unicode__(self):
        return u'%s' % (self.descripcion)
        self.descripcion = self.descripcion.upper()
 
    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_jerarquias'

class RefSexo(models.Model):
    id = models.AutoField(primary_key = True)
    Sexo_opciones=(
    ('1','Femenino'),
    ('2','Masculino'),
    )
    descripcion = models.CharField(max_length = 10, choices=Sexo_opciones)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
  
    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_sexo'

class RefEstadosciv(models.Model):
    id = models.AutoField(primary_key = True)
    civil_opciones=(
    ('0','NO REGISTRA'),('1','SOLTERO'),('2','CONCUBINO'),('3','CASAD0'),('4','DIVORCIADO'),('5','VIUDO'),('6','SEPARADO'),)
    descripcion = models.CharField(max_length = 10, choices=civil_opciones)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
  
    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_estadociv'        

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

    def __unicode__(self):
        return u'%s' % (self.descripcion)
 
    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_tipodocumento'


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
    

    def __unicode__(self):
        return u'%s %s' % (self.apellidos, self.nombres)
        self.apellidos = self.descripcion.upper()
        self.nombres = self.nombres.upper()
 
    def save(self, force_insert = False, force_update = False):
        self.apellidos = self.apellidos.upper()
        self.nombres = self.nombres.upper()
        super(Personas, self).save(force_insert, force_update)    

    class Meta:
        unique_together=('tipo_doc','nro_doc','apellidos','nombres',)
        ordering = ['apellidos']
        db_table = 'personas'

class Actuantes(models.Model):
    id = models.AutoField(primary_key=True)
    funcion = models.IntegerField()
    documento = models.IntegerField(max_length=8, unique=True)
    apeynombres = models.CharField(max_length=250)
    jerarquia_id = models.ForeignKey('RefJerarquias', on_delete=models.PROTECT)
    persona_id = models.ForeignKey('Personas', on_delete=models.PROTECT)
    unidadreg_id = models.ForeignKey('UnidadesRegionales', on_delete=models.PROTECT)
    dependencia_id = models.ForeignKey('Dependencias', on_delete=models.PROTECT)

    def __unicode__(self):
        return u'%s ' % (self.apeynombres)
    
    def save(self, force_insert = False, force_update = False):
        self.documento = self.documento
        self.apeynombres = self.apeynombres.upper()
        super(Actuantes, self).save(force_insert, force_update)
  
    class Meta:
        ordering = ['documento']
        db_table = 'actuantes'

class Personal(models.Model):
    id = models.AutoField(primary_key=True)
    persona_id = models.OneToOneField('Personas', unique=True,on_delete=models.PROTECT)
    legajo = models.CharField(max_length=6)
    credencial = models.IntegerField()
    nro_cuenta_bco = models.CharField(max_length=20)
    nro_seros = models.CharField(max_length=15)

    def __unicode__(self):
        return u'%s' % (self.id)
    
    class Meta:

        ordering = ['id']
        db_table = 'personal'

class RefComunidades(models.Model):
    id = models.AutoField(primary_key = True)
    Zonas_opciones=(
    ('1','Urbana'),
    ('2','Sub-urbana'),
    ('3','Rural'),
    ('4','Costa'),
    )
    descripcion = models.CharField(max_length = 10, choices= Zonas_opciones)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
 
    class Meta:
        ordering = ['descripcion']
        db_table = 'ref_comunidades'

class Preventivos(models.Model):
    id = models.AutoField(primary_key=True)
    nro = models.PositiveIntegerField(verbose_name='Nro. :',validators=[MinValueValidator(1),MaxValueValidator(9999999)])
    anio = models.PositiveIntegerField(verbose_name='Año :',validators=[MinValueValidator(2012),MaxValueValidator(2025)])
    caratula = models.CharField(max_length=250)
    fecha_carga = models.DateField()
    fecha_denuncia = models.DateField()
    fecha_autorizacion = models.DateField(null=True)
    fecha_cierre = models.DateField(null=True)
    actuante = models.ForeignKey('Actuantes', verbose_name='Actuante', related_name='Actuante', on_delete=models.PROTECT)
    preventor = models.ForeignKey('Actuantes', verbose_name='Preventor', related_name='Preventor', on_delete=models.PROTECT)
    dependencia = models.ForeignKey('Dependencias',blank=True,null=True)
    autoridades = models.ManyToManyField('RefAutoridad',blank=True,null=True)

  
    def __unicode__(self):
        return u'%s' % (self.id)
    
    def save(self, force_insert = False, force_update = False):
        self.caratula=self.caratula.upper()
        super(Preventivos, self).save(force_insert, force_update)
  
   

    class Meta:
        ordering = ['nro','anio','dependencia']
        db_table = 'preventivos'

class RefModosHecho(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=80)
    delito = models.ForeignKey(RefDelito,on_delete=models.PROTECT)
    def __unicode__(self):
        return u'%s' % (self.descripcion)
             # %s  ,self.delito)

    def save(self, force_insert = False, force_update = False):
        self.descripcion=self.descripcion.upper()
        super(RefModosHecho, self).save(force_insert, force_update)

    class Meta:
        unique_together=('descripcion','delito',)
        ordering = ['id']
        db_table = 'ref_modos_hecho'

class RefMotivosHecho(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=80, unique=True)
    def __unicode__(self):
        return u'%s' % unicode(self.descripcion)
    class Meta:
        ordering = ['id']
        db_table = 'ref_motivos_hecho'



class Hechos(models.Model):
    fecha_carga=models.DateField(blank=True,null=True)
    descripcion=models.CharField(max_length=2000,blank=True,null=True)
    preventivo=models.ForeignKey('Preventivos', unique=True, on_delete=models.PROTECT,related_name='hecho')
    motivo=models.ForeignKey('RefMotivosHecho', null=False, on_delete=models.PROTECT)
    fecha_desde=models.DateTimeField()
    fecha_hasta=models.DateTimeField()
    fecha_esclarecido=models.DateField(null=True)
   
    def __unicode__(self):
        return u'%s' % (self.descripcion)
  
    def save(self, force_insert = False, force_update = False):
        #self.descripcion=self.descripcion.upper()
        super(Hechos, self).save(force_insert, force_update)

    class Meta:
        ordering = ['fecha_carga','preventivo',]
        db_table = 'hechos'

class HechosDelito(models.Model):
    id = models.AutoField(primary_key=True)
    hechos = models.ForeignKey('Hechos',related_name='hechos',)
    refdelito = models.ForeignKey('RefDelito',related_name='delis',)
    refmodoshecho = models.ForeignKey('RefModosHecho', related_name='modus', null=True, blank=True)
    borrado = models.CharField(max_length=1,null=True, blank=True)

    def __unicode__(self):
        return u'%s' % (self.refdelito.descripcion)
        
    def save(self, force_insert = False, force_update = False):
        super(HechosDelito, self).save(force_insert)

    class Meta:
        ordering = ['id']
        db_table = 'hechos_delito'
        unique_together = ('hechos','refdelito','refmodoshecho',)


class PersInvolucradas(models.Model):
    fcio_opciones=(('si','SI'),('no','NO'),)
    id = models.AutoField(primary_key=True)
    hechos = models.ForeignKey('Hechos',related_name='involu')
    roles = models.ForeignKey('RefPeople',related_name='rol')
    persona = models.ForeignKey('Personas',related_name='perso')
    juridica =models.CharField(max_length=2,choices=fcio_opciones,blank=True,default="no")
    razon_social = models.CharField(max_length=150,null=True,blank=True)
    menor =  models.CharField(max_length=2,choices=fcio_opciones,blank=True,default="no")
    detenido = models.CharField(max_length=2,choices=fcio_opciones,blank=True,default="no")
    infraganti =models.CharField(max_length=2,choices=fcio_opciones,blank=True,default="no")
    fechahoradetencion=models.DateTimeField(null=True,blank=True)
    fechahoralibertad=models.DateTimeField(null=True,blank=True)
    cargado_prev=models.BooleanField(default=False)
    ampliacion=models.ForeignKey('Ampliacion',blank=True,null=True)

    def __unicode__(self):
        return u'%s' % (self.persona)
        
    def save(self, force_insert = False, force_update = False):
        self.razon_social=self.razon_social.upper()
        super(PersInvolucradas, self).save(force_insert, force_update)

    class Meta:
        unique_together = ('hechos','persona','roles','cargado_prev','ampliacion',)
        ordering = ['id']
        db_table = 'persinvolucradas'

class Padres(models.Model):
    id=models.AutoField(primary_key=True)
    persona = models.ForeignKey('Personas',related_name='padre')
    padre_nombres=models.CharField(max_length=150,null=True,blank=True,default="")
    padre_apellidos=models.CharField(max_length=100,null=True,blank=True,default="")
    madre_apellidos=models.CharField(max_length=100,null=True,blank=True,default="")
    madre_nombres=models.CharField(max_length=150,null=True,blank=True,default="")
    
    def __unicode__(self):
        return u'%s' % (self.persona)
        
    def save(self, force_insert = False, force_update = False):
        self.padre_apellidos=self.padre_apellidos.upper()
        self.padre_nombres=self.padre_nombres.upper()
        self.madre_apellidos=self.madre_apellidos.upper()
        self.madre_nombres=self.madre_nombres.upper()
        super(Padres, self).save(force_insert, force_update)

    class Meta:
        unique_together=('persona','padre_nombres','padre_apellidos','madre_nombres','madre_apellidos',)
        ordering = ['id']
        db_table = 'padres'

class Detenidos(models.Model):
    id=models.AutoField(primary_key=True)
    persona = models.ForeignKey(Personas)
    fechahoradetencion=models.DateTimeField(null=True,blank=True)
    fechahoralibertad=models.DateTimeField(null=True,blank=True)
    hechos = models.ForeignKey(Hechos)
    observaciones= models.CharField(max_length=800,null=True,blank=True)
    borrado = models.CharField(max_length=1,null=True, blank=True)


    def __unicode__(self):
        return u'%s' % (self.persona)
        
    def save(self, force_insert = False, force_update = False):
        super(Detenidos, self).save(force_insert, force_update)

    class Meta:
        unique_together=('hechos','persona',)
        ordering = ['id']
        db_table = 'detenidos'

class Domicilios(models.Model):
    personas = models.ForeignKey('Personas',related_name='persodom')
    ref_ciudades = models.ForeignKey(RefCiudades,blank = True, null = True)
    barrio_codigo = models.ForeignKey(RefBarrios,blank = True, null = True)
    calle = models.ForeignKey(RefCalles,related_name = 'domicilio',blank = True, null = True)
    altura = models.CharField(max_length=4,default="0",blank = True)
    entre = models.ForeignKey(RefCalles,related_name = 'interseccion', blank = True, null = True)
    fecha_desde = models.DateField(blank = True, null = True)
    fecha_hasta = models.DateField(blank = True, null = True)
    fecha_actualizacion = models.DateField(blank = True, null = True)
    tipos_domicilio = models.ForeignKey(RefHogares,blank = True, null = True)
    ref_zona = models.ForeignKey(RefComunidades,blank = True, null = True)
    departamento = models.CharField(max_length = 10,blank = True, null = True,default="")
    piso = models.CharField(max_length=4,default="0",blank = True)
    lote =models.CharField(max_length=4,default="0",blank = True)
    sector = models.CharField(max_length = 10,blank = True, null = True,default="")
    manzana = models.CharField(max_length=4,default="0",blank = True)
    
    def __unicode__(self):
        return u'%s %s %s %s' % (self.personas,self.barrio_codigo,self.calle,self.altura)

    class Meta:
        unique_together=('personas','ref_ciudades','barrio_codigo','fecha_desde','calle','altura')
        ordering = ['-fecha_desde']
        db_table = 'domicilios'

class Lugar(models.Model):
    calle = models.ForeignKey(RefCalles,related_name='calle_hecho',on_delete=models.PROTECT,blank=True,null = True)
    altura = models.IntegerField(default='',blank=True,null = True)
    latitud = models.CharField(max_length=50)
    longitud = models.CharField(max_length=50)
    barrio = models.ForeignKey('RefBarrios',on_delete = models.PROTECT,blank = True, null = True)
    tipo_lugar = models.ForeignKey('RefLugares',on_delete=models.PROTECT)
    cond_climaticas = models.ManyToManyField('RefCondclimas',related_name='condiciones',blank=True,null=True)
    hecho = models.ForeignKey('Hechos', unique=True,related_name='lugar_hecho',on_delete = models.PROTECT)
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


    def save(self, force_insert = False, force_update = False):
        super(Lugar, self).save(force_insert,force_update)

    class Meta:
        ordering = ['id']
        db_table = 'lugar'

#modelo de elementos 
class RefTipoelementos(models.Model):
    id=models.AutoField(primary_key=True)
    elementos=(
    ('1','DENUNCIADOS'),
    ('2','SECUESTRADOS'),
    ('3','UTILIZADOS'), ('4','UTILIZADOS/SECUESTRADOS'),
    )
    descripcion = models.CharField(max_length = 50,choices= elementos)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
 
    class Meta:
        ordering = ['descripcion']
        db_table = 'reftipoelementos'

class RefUnidadmedidas(models.Model):
    id=models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length =30)

    def __unicode__(self):
        return u'%s' % (self.descripcion)
    
    def save(self, force_insert = False, force_update = False):
        self.descripcion=self.descripcion.upper()
        super(RefUnidadmedidas, self).save(force_insert,force_update)

    class Meta:
        unique_together=('descripcion',)
        ordering = ['descripcion']
        db_table = 'refunidadmedidas'
"""
class RefCategorias(models.Model):
    id=models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length =100)

    def __unicode__(self):
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
    fecha=models.DateField(auto_now=True)
    borrado = models.CharField(max_length=1,null=True, blank=True)
    observaciones= models.CharField(max_length=800,null=True,blank=True)
    cargado_prev=models.BooleanField(default=False)
    ampliacion=models.ForeignKey('Ampliacion',blank=True,null=True)
    
    def __unicode__(self):
        return u'%s %s %s' % (self.id,self.descripcion, self.hechos)
        self.descripcion = self.descripcion.upper()
       
 
    def save(self, force_insert = False, force_update = False):
        self.descripcion = self.descripcion.upper()
        super(Elementos, self).save(force_insert, force_update)    

    class Meta:

        ordering = ['tipo','descripcion']
        db_table = 'elementos'


class Armas(models.Model):
    id=models.AutoField(primary_key=True)
    tipos=models.ForeignKey('RefTiposarmas', on_delete=models.PROTECT)
    subtipos=models.ForeignKey('RefSubtiposa',on_delete=models.PROTECT)
    sistema_disparo=models.ForeignKey('RefSistemadis',on_delete=models.PROTECT,blank=True,null=True)
    marcas=models.ForeignKey('RefTrademark',on_delete=models.PROTECT,blank=True,null=True)
    modelo=models.CharField(max_length=100,blank=True,null=True)
    calibre=models.CharField(max_length=10,blank=True,null=True)
    nro_arma=models.CharField(max_length=50,blank=True,null=True)
    nro_doc = models.IntegerField(max_length=8,blank=True,null=True)
    propietario=models.CharField(max_length=100,blank=True,null=True)
    fecha_carga=models.DateField(auto_now=True)

    def __unicode__(self):
        return u'%s' % (self.tipos)
  
    def save(self, force_insert = False, force_update = False):
       
        super(Armas, self).save(force_insert, force_update)

    class Meta:
        #unique_together=['nro_arma',]
        ordering = ['tipos','subtipos','marcas',]
        db_table = 'armas'

class Elementosarmas(models.Model):
    id=models.AutoField(primary_key=True)
    idelemento=models.ForeignKey('Elementos',related_name='relelem')
    idarma=models.ForeignKey('Armas')

    def __unicode__(self):
        return u'%s' % (self.idelemento)
    def save(self, force_insert = False, force_update = False):
       
        super(Elementosarmas, self).save(force_insert, force_update)

    class Meta:
       
        ordering = ['idelemento',]
        db_table = 'elementosarmas'

"""
#modelo de elementos automotores
class RefMarcascars(models.Model):
    id = models.AutoField(primary_key = True)
    descripcion = models.CharField(max_length = 50)
 
    def __unicode__(self):
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
    fecha_carga=models.DateField(auto_now=True)
    nro_doc = models.IntegerField(max_length=8,null=True,blank=True)
    propietario = models.CharField(max_length=100,null=True,blank=True)
    def __unicode__(self):
        return u'%s' % (self.dominio)
  
    def save(self, force_insert = False, force_update = False):
        self.dominio        = self.dominio.upper()
        self.nmotor         = self.nmotor.upper()
        self.nchasis        = self.nchasis.upper()
        self.tipov          = self.tipov.upper()
        self.modelo         = self.modelo.upper()
        self.propietario    = self.propietario.upper()
        super(Vehiculos, self).save(force_insert, force_update)
        

    class Meta:
        ordering = ['dominio',]
        db_table = 'vehiculos'


class Elementoscars(models.Model):
    id=models.AutoField(primary_key=True)
    idelemento=models.ForeignKey('Elementos')
    idvehiculo=models.ForeignKey('Vehiculos')

    def save(self, force_insert = False, force_update = False):
        super(Elementoscars, self).save(force_insert, force_update)

    class Meta:

        db_table = 'elementoscars'

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
   
    def __unicode__(self):
      return  u'%s' % (self.descripcion)  
      self.descripcion = self.descripcion.upper()
     
    
    class Meta: 
        ordering = ["descripcion"]
        db_table = 'reftipodrogas'



class Drogas(models.Model):
    id = models.AutoField(primary_key = True)
    descripcion=models.CharField(max_length=100)
    idtipo=models.ForeignKey('reftipodrogas')
    fecha_carga=models.DateField(auto_now=True)
    def __unicode__(self):
        return u'%s' % (self.descripcion)
  
    def save(self, force_insert = False, force_update = False):
        super(Drogas, self).save(force_insert, force_update)

    class Meta:
        ordering = ['descripcion',]
        db_table = 'drogas'


class Elementosdrogas(models.Model):
    id=models.AutoField(primary_key=True)
    idelemento=models.ForeignKey('Elementos')
    droga=models.ForeignKey('Drogas')

class Ampliacion(models.Model):
    id                  = models.AutoField(primary_key = True)
    fecha               = models.DateField(auto_now=True)
    titulo              = models.CharField(max_length=100)
    autoridades         = models.ManyToManyField('RefAutoridad',null=True,blank=True)
    descripcion         = models.CharField(max_length=2000)
    preventivo          = models.ForeignKey('Preventivos',related_name='ampli')
    fecha_autorizacion  = models.DateField(null=True,blank=True)
    cierre_causa        = models.BooleanField(default=False)
    fecha_cierre        = models.DateField(blank=True,null=True)
    fin_edicion         = models.BooleanField(default=False)

    def save(self, force_insert = False, force_update = False):
        super(Ampliacion,self).save(force_insert,force_update)

    class Meta:
        ordering    = ['id']
        db_table    = 'ampliacion'