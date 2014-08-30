from dajax.core import Dajax
from preventivos.models import RefPaises, RefProvincia, RefDepartamentos, RefCiudades
from preventivos.forms import PaisesForm, ProvinciasForm, DepartamentosForm, CiudadesForm
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def cargar_paises(request):
 dajax = Dajax()
 paises = PaisesForm.objects.all()
 out = ""
 for pais in paises:
  out = "%s %s"%(out,pais.id,pais.descripcion)
  dajax.assign
 ('#pais','innerHTML',out)
 return dajax.json() 

def cargar_provincia(request):
 dajax = Dajax()
 provincias = RefProvincia.objects.filter(id= int(request.POST['option']))
 out = ""
 print provincias
 for provincia in provincias:
  out = "%s %s"%(out,provincia.id,provincia.descripcion)
  dajax.assign('#provincia','innerHTML',out)
 return dajax.json()

def cargar_dptos(request):
 dajax = Dajax()
 dpto = RefDepartamentos.objects.filter(id= int(request.POST['option']))
 out = ""
 for depto in dpto:
  out = "%s %s"%(out,dpto.id,dpto.descripcion)
  dajax.assign
 ('#departamento','innerHTML',out)
 return dajax.json()
 
