# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Userprofile(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('AuthUser', unique=True)
    ureg = models.ForeignKey('UnidadesRegionales', null=True, blank=True)
    depe = models.ForeignKey('Dependencias', null=True, blank=True)
    class Meta:
        db_table = 'UserProfile'

class Actuantes(models.Model):
    id = models.IntegerField(primary_key=True)
    funcion = models.IntegerField()
    documento = models.IntegerField()
    apeynombres = models.CharField(max_length=250L)
    jerarquia_id = models.ForeignKey('RefJerarquias')
    persona_id = models.ForeignKey('Personas')
    unidadreg_id = models.ForeignKey('UnidadesRegionales')
    dependencia_id = models.ForeignKey('Dependencias')
    class Meta:
        db_table = 'actuantes'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80L, unique=True)
    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100L)
    class Meta:
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128L)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(max_length=30L, unique=True)
    first_name = models.CharField(max_length=30L)
    last_name = models.CharField(max_length=30L)
    email = models.CharField(max_length=75L)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        db_table = 'auth_user_user_permissions'

class Dependencias(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=80L)
    unidades_regionales = models.ForeignKey('UnidadesRegionales')
    ciudad = models.ForeignKey('RefCiudades')
    class Meta:
        db_table = 'dependencias'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', null=True, blank=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200L)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100L)
    app_label = models.CharField(max_length=100L)
    model = models.CharField(max_length=100L)
    class Meta:
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=40L, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = 'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=100L)
    name = models.CharField(max_length=50L)
    class Meta:
        db_table = 'django_site'

class Personal(models.Model):
    id = models.IntegerField(primary_key=True)
    persona_id = models.ForeignKey('Personas', unique=True)
    legajo = models.CharField(max_length=6L)
    credencial = models.IntegerField()
    nro_cuenta_bco = models.CharField(max_length=20L)
    nro_seros = models.CharField(max_length=15L)
    class Meta:
        db_table = 'personal'

class Personas(models.Model):
    id = models.IntegerField(primary_key=True)
    tipo_doc = models.ForeignKey('RefTipodocumento')
    nro_doc = models.IntegerField()
    apellidos = models.CharField(max_length=100L)
    nombres = models.CharField(max_length=150L)
    fecha_nac = models.DateField()
    ciudad_nac = models.ForeignKey('RefCiudades')
    pais_nac = models.ForeignKey('RefPaises')
    ciudad_res = models.ForeignKey('RefCiudades')
    sexo_id = models.ForeignKey('RefSexo')
    ocupacion = models.ForeignKey('RefOcupacion')
    cuit = models.BigIntegerField()
    celular = models.CharField(max_length=100L)
    class Meta:
        db_table = 'personas'

class Preventivos(models.Model):
    id = models.IntegerField(primary_key=True)
    nro = models.IntegerField()
    anio = models.IntegerField()
    caratula = models.CharField(max_length=250L)
    fecha_carga = models.DateField()
    fecha_denuncia = models.DateField()
    fecha_autorizacion = models.DateField(null=True, blank=True)
    fecha_cierre = models.DateField(null=True, blank=True)
    actuante = models.ForeignKey(Actuantes)
    preventor = models.ForeignKey(Actuantes)
    dependencia = models.ForeignKey(Dependencias)
    class Meta:
        db_table = 'preventivos'

class PreventivosAutoridades(models.Model):
    id = models.IntegerField(primary_key=True)
    preventivos = models.ForeignKey(Preventivos)
    refautoridad = models.ForeignKey('RefAutoridad')
    class Meta:
        db_table = 'preventivos_autoridades'

class RefAgrupacion(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=25L, blank=True)
    class Meta:
        db_table = 'ref_agrupacion'

class RefArmas(models.Model):
    id = models.IntegerField(primary_key=True)
    marca = models.CharField(max_length=80L, blank=True)
    modelo = models.CharField(max_length=90L, blank=True)
    tipo = models.CharField(max_length=90L, blank=True)
    calibre = models.CharField(max_length=90L, blank=True)
    class Meta:
        db_table = 'ref_armas'

class RefAutoridad(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=80L)
    email = models.CharField(max_length=75L)
    class Meta:
        db_table = 'ref_autoridad'

class RefAutoridadCiudades(models.Model):
    id = models.IntegerField(primary_key=True)
    refautoridad = models.ForeignKey(RefAutoridad)
    refciudades = models.ForeignKey('RefCiudades')
    class Meta:
        db_table = 'ref_autoridad_ciudades'

class RefBarrios(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=100L)
    ciudad = models.ForeignKey('RefCiudades')
    class Meta:
        db_table = 'ref_barrios'

class RefCalles(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=150L)
    ciudad = models.ForeignKey('RefCiudades')
    class Meta:
        db_table = 'ref_calles'

class RefCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=100L)
    rubro = models.ForeignKey('RefItems')
    class Meta:
        db_table = 'ref_category'

class RefCiudades(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=80L)
    departamento = models.ForeignKey('RefDepartamentos', null=True, blank=True)
    provincia = models.ForeignKey('RefProvincia', null=True, blank=True)
    pais = models.ForeignKey('RefPaises')
    class Meta:
        db_table = 'ref_ciudades'

class RefComunidades(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=10L)
    class Meta:
        db_table = 'ref_comunidades'

class RefCondclimas(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=150L, unique=True)
    class Meta:
        db_table = 'ref_condclimas'

class RefDelito(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50L)
    tipo_delito = models.ForeignKey('RefTipoDelito')
    class Meta:
        db_table = 'ref_delito'

class RefDepartamentos(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L, unique=True)
    provincia = models.ForeignKey('RefProvincia')
    class Meta:
        db_table = 'ref_departamentos'

class RefDivisionJerarquia(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'ref_division_jerarquia'

class RefEstadoCivil(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'ref_estado_civil'

class RefGrupoSanguineo(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'ref_grupo_sanguineo'

class RefHogares(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=100L, unique=True)
    class Meta:
        db_table = 'ref_hogares'

class RefItems(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=100L, unique=True)
    class Meta:
        db_table = 'ref_items'

class RefJerarquias(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    ref_tipo_jerarquia = models.ForeignKey('RefTipoJerarquia')
    ref_division_jerarquia = models.ForeignKey(RefDivisionJerarquia)
    class Meta:
        db_table = 'ref_jerarquias'

class RefLugares(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=100L, unique=True)
    class Meta:
        db_table = 'ref_lugares'

class RefModosHecho(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=80L, unique=True)
    class Meta:
        db_table = 'ref_modos_hecho'

class RefMotivosHecho(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=80L, unique=True)
    class Meta:
        db_table = 'ref_motivos_hecho'

class RefOcupacion(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=80L, unique=True)
    class Meta:
        db_table = 'ref_ocupacion'

class RefPaises(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L, unique=True)
    class Meta:
        db_table = 'ref_paises'

class RefPeople(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=150L, unique=True)
    class Meta:
        db_table = 'ref_people'

class RefProvincia(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    pais = models.ForeignKey(RefPaises)
    class Meta:
        db_table = 'ref_provincia'

class RefSexo(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=10L)
    class Meta:
        db_table = 'ref_sexo'

class RefTipoDelito(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50L)
    class Meta:
        db_table = 'ref_tipo_delito'

class RefTipoJerarquia(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=45L)
    class Meta:
        db_table = 'ref_tipo_jerarquia'

class RefTipodocumento(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=4L)
    class Meta:
        db_table = 'ref_tipodocumento'

class UnidadesRegionales(models.Model):
    id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=80L)
    ciudad = models.ForeignKey(RefCiudades)
    class Meta:
        db_table = 'unidades_regionales'

