from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from dashboards.views import *

app_name = 'dashboards'

urlpatterns = [
    #Nomencladores
    #Crud Marca
    path('marca/lista', lista_marca, name='lista_marca'),
    path('marca/crear', create_marca, name='create_marca'),
    path('marca/editar/<int:pk>', editar_marca, name='editar_marca'),
    path('marca/eliminar/<int:pk>', eliminar_marca, name='eliminar_marca'),

    #Crud Modelo
    path('listado_modelo/', lista_modelo, name='lista_modelo'),
    path('modelo/crear', create_modelo, name='create_modelo'),
    path('modelo/editar/<int:pk>', editar_modelo, name='editar_modelo'),
    path('modelo/eliminar/<int:pk>', eliminar_modelo, name='eliminar_modelo'),

    #Crud Propiedad
    path('listado_propiedad/', lista_propiedad, name='lista_propiedad'),
    path('propiedad/crear', create_propiedad, name='create_propiedad'),
    path('propiedad/editar/<int:pk>', editar_propiedad, name='editar_propiedad'),
    path('propiedad/eliminar/<int:pk>', eliminar_propiedad, name='eliminar_propiedad'),

    #Crud Organismo
    path('listado_organismo/', lista_organismo, name='lista_organismo'),
    path('organismo/crear', create_organismo, name='create_organismo'),
    path('organismo/editar/<int:pk>', editar_organismo, name='editar_organismo'),
    path('organismo/eliminar/<int:pk>', eliminar_organismo, name='eliminar_organismo'),

    #Crud Osde
    path('listado_osde/', lista_osde, name='lista_osde'),
    path('osde/crear', create_osde, name='create_osde'),
    path('osde/editar/<int:pk>', editar_osde, name='editar_osde'),
    path('osde/eliminar/<int:pk>', eliminar_osde, name='eliminar_osde'),

    #Crud Empresa
    path('listado_empresa/', lista_empresa, name='lista_empresa'),
    path('empresa/crear', create_empresa, name='create_empresa'),
    path('empresa/editar/<int:pk>', editar_empresa, name='editar_empresa'),
    path('empresa/eliminar/<int:pk>', eliminar_empresa, name='eliminar_empresa'),

#   #Crud CATEGORIAPIEZA
    path('categoriapieza/lista', lista_categoriapieza, name='lista_categoriapieza'),
    path('categoriapieza/crear', create_categoriapieza, name='create_categoriapieza'),
    path('categoriapieza/editar/<int:pk>', editar_categoriapieza, name='editar_categoriapieza'),
    path('categoriapieza/eliminar/<int:pk>', eliminar_categoriapieza, name='eliminar_categoriapieza'),

    #Crud CATEGORIAPARTE
    path('listado_categoriaparte/lista', lista_categoriaparte, name='lista_categoriaparte'),
    path('categoriaparte/crear', create_categoriaparte, name='create_categoriaparte'),
    path('categoriaparte/editar/<int:pk>', editar_categoriaparte, name='editar_categoriaparte'),
    path('categoriaparte/eliminar/<int:pk>', eliminar_categoriaparte, name='eliminar_categoriaparte'),

    #Crud CATEGORIAEQUIPO
    path('listado_categoriaequipo/lista', lista_categoriaequipo, name='lista_categoriaequipo'),
    path('categoriaequipo/crear', create_categoriaequipo, name='create_categoriaequipo'),
    path('categoriaequipo/editar/<int:pk>', editar_categoriaequipo, name='editar_categoriaequipo'),
    path('categoriaequipo/eliminar/<int:pk>', eliminar_categoriaequipo, name='eliminar_categoriaequipo'),

    # #Crud CATEGORIAINSUMO
    # path('categoriainsumo/lista', lista_categoriainsumo, name='lista_categoriainsumo'),
    # path('categoriainsumo/crear', create_categoriainsumo, name='create_categoriainsumo'),
    # path('categoriainsumo/editar/<int:pk>', editar_categoriainsumo, name='editar_categoriainsumo'),
    # path('categoriaequipo/eliminar/<int:pk>', eliminar_categoriaequipo, name='eliminar_categoriaequipo'),

    # Crud Equipo
    path('listado_equipo/lista', lista_equipo, name='lista_equipo'),
    path('equipo/crear', crear_equipo, name='crear_equipo'),
    path('equipo/<int:pk>/propiedad', equipo_propiedad, name='equipo_propiedad'),
    path('equipo/editar/<int:pk>', editar_equipo, name='editar_equipo'),
    path('equipo/eliminar/<int:pk>', eliminar_equipo, name='eliminar_equipo'),

    # Crud Pieza
    path('listado_pieza/lista', lista_pieza, name='lista_pieza'),
    path('pieza/crear', crear_pieza, name='crear_pieza'),
    path('pieza/<int:pk>/propiedad', pieza_propiedad, name='pieza_propiedad'),
    path('pieza/editar/<int:pk>', editar_pieza, name='editar_pieza'),
    path('pieza/eliminar/<int:pk>', eliminar_pieza, name='eliminar_pieza'),

    # Crud Parte
    path('listado_parte/lista', lista_parte, name='lista_parte'),
    path('parte/crear', crear_parte, name='crear_parte'),
    path('parte/<int:pk>/propiedad', parte_propiedad, name='parte_propiedad'),
    path('parte/editar/<int:pk>', editar_parte, name='editar_parte'),
    path('parte/eliminar/<int:pk>', eliminar_parte, name='eliminar_parte'),

    #PDF
    path('equipo/pdf/<int:pk>', ExpedienteEquipoPDFView.as_view(), name='generar_pdf_equipo'),
    path('listado_equipo/pdf', ListadoEquipoPDFView.as_view(), name='generar_pdf_listado_equipo'),

    #Perfil
    path('perfil/', perfil_usuario, name='perfil_usuario'),

    #Reporte
    path('reporte/equipo', reporte_equipo, name='reporte_equipo'),

    # path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)