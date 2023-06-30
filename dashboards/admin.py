from django.contrib import admin
from django.contrib.auth.models import Permission

from dashboards.models import *

# Register your models here.
admin.site.register(Organismo)
admin.site.register(Osde)
admin.site.register(Empresa)
admin.site.register(Propiedad)
admin.site.register(Provincia)
admin.site.register(CategoriaParte)
admin.site.register(CategoriaPieza)
admin.site.register(CategoriaEquipo)
admin.site.register(Pieza)
admin.site.register(Parte)
admin.site.register(Equipo)
admin.site.register(MarcaModelo)
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(UserPerfil)
admin.site.register(Permission)
admin.site.register(Estado)