import datetime
import os

from _decimal import Decimal
from auditlog.models import LogEntry
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Q
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.utils.dateparse import parse_date
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import resolve, reverse
from xhtml2pdf import pisa

from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from pprint import pprint

from dashboards.forms import *
from dashboards.models import *

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""


@login_required
def Inicio(request, **kwargs):
    layout = 'layout/default.html'
    top_3_equipo = []
    top_4_equipo_empresa = []
    today = datetime.date.today()
    month = today.month
    year = today.year
    equipos_por_categoria = []
    equipos = Equipo.objects.all()
    partes = Parte.objects.all()
    piezas = Pieza.objects.all()
    activos  = Equipo.objects.filter(estado='Activo')
    venta  = Equipo.objects.filter(estado='Venta')
    reparacion  = Equipo.objects.filter(estado='Reparación')
    equipos = Equipo.objects.all()
    equipos_venta = Equipo.objects.filter(estado='Venta')
    equipos_venta_ultimo_mes = Equipo.objects.filter(estado='Venta',fecha_registro__month=month)
    equipos_reparacion = Equipo.objects.filter(estado='Reparación')

    for categoria in CategoriaEquipo.objects.all():
        equipos_cat = Equipo.objects.filter(categoria=categoria).order_by('-fecha_registro')
        if equipos_cat:
            equipos_por_categoria.append({'categoria':categoria,'equipos_cat':equipos_cat})


    top_3_equipo_por_marca = Marca.objects.annotate(cant_equipos = Count('equipo')).order_by('-cant_equipos')[:3]
    top_4_equipo_por_empresa = Empresa.objects.annotate(cant_equipos = Count('equipo')).order_by('-cant_equipos')[:4]

    for equipo in top_3_equipo_por_marca:
        top_3_equipo.append({'marca':equipo.nombre,'cant':equipo.cant_equipos})

    for empresa in top_4_equipo_por_empresa:
        top_4_equipo_empresa.append({'empresa':empresa.nombre,'cant':equipo.cant_equipos})

    #crecimiento mensual de registro de equipos
    cantidad_actual = Equipo.objects.filter(fecha_registro__month=month-1, fecha_registro__year=year).count()
    cantidad_actual_venta = Equipo.objects.filter(estado='Venta', fecha_registro__month=month-1, fecha_registro__year=year).count()

    mes_anterior = month - 2
    anno_anterior = year
    if mes_anterior == 0:
        mes_anterior = 12
        anno_anterior = year - 1

    previous_count = Equipo.objects.filter(fecha_registro__month=mes_anterior,fecha_registro__year=anno_anterior).count()
    previous_count_venta = Equipo.objects.filter(estado='Venta',fecha_registro__month=mes_anterior,fecha_registro__year=anno_anterior).count()
    if previous_count != 0:
        porciento_crecimiento_mensual = Decimal((cantidad_actual - previous_count) / previous_count) * 100
        porciento_crecimiento_mensual_venta = Decimal((cantidad_actual_venta - previous_count_venta) / previous_count_venta) * 100
    else:
        porciento_crecimiento_mensual = Decimal((cantidad_actual - previous_count)) * 100
        porciento_crecimiento_mensual_venta = Decimal((cantidad_actual_venta - previous_count_venta) ) * 100

    context = {
        'equipos':equipos,
        'equipos_venta':{'equipos_venta':equipos_venta,'porciento':(equipos_venta.count()/equipos.count())*100},
        'equipos_venta_ultimo_mes':equipos_venta_ultimo_mes,
        'equipos_reparacion':equipos_reparacion,
        'top_3_equipo':top_3_equipo,
        'layout':layout,
        'activos':activos,
        'reparacion':reparacion,
        'venta':venta,
        'partes':partes,
        'piezas':piezas,
        'top_4_equipo_empresa':top_4_equipo_empresa,
        'equipos_por_categoria':equipos_por_categoria,
        'porciento_crecimiento_mensual':porciento_crecimiento_mensual,
        'porciento_crecimiento_mensual_venta':porciento_crecimiento_mensual_venta
    }
    context = KTLayout.init(context)

    return render(request, "pages/dashboards/index.html", context)

def ExistePropiedadPieza(id_pieza, id_propiedad):
    if PropiedadPieza.objects.filter(pieza_id=id_pieza, propiedad_id=id_propiedad):
        return True
    else:
        return False


def ExistePropiedadInsumo(id_insumo, id_propiedad):
    if PropiedadInsumo.objects.filter(insumo_id=id_insumo, propiedad_id=id_propiedad):
        return True
    else:
        return False


def ExistePropiedadParte(id_parte, id_propiedad):
    if PropiedadParte.objects.filter(parte_id=id_parte, propiedad_id=id_propiedad):
        return True
    else:
        return False


def ExistePropiedadEquipo(id_equipo, id_propiedad):
    if PropiedadEquipo.objects.filter(equipo_id=id_equipo, propiedad_id=id_propiedad):
        return True
    else:
        return False


###################################################
####                Crud Organismo             ####
###################################################
@login_required()
def lista_organismo(request, **kwargs):
    object_list = Organismo.objects.all()
    crear_url = reverse('dashboards:create_organismo')
    title_html = 'Organismos'
    dict_object_list = {}
    variables_filtro = ['nombre']
    layout = 'layout/default.html'

    for element in object_list:
        url_editar = reverse("dashboards:editar_organismo", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_organismo", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar':url_eliminar}


    context = {
        'dict_object_list': dict_object_list,
        'title_html': title_html,
        'crear_url': crear_url,
        'variables_filtro': variables_filtro,
        'nombre_tabla': 'organismo',
        'layout':layout,
        'breadcumb_lista': 'Organismo',
        'encabezado_pagina': 'Organismos',
    }
    KTTheme.addJavascriptFile('../assets/js/message.js')
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/list.html', context)


@login_required
def create_organismo(request):
    title_html = 'Organismo'
    url_cancel = reverse('dashboards:lista_organismo')
    layout = 'layout/default.html'

    if request.POST:
        form = OrganismoModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_organismo'),{'layout':layout})
    else:
        form = OrganismoModelForm()
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Nueva Organismo',
            'encabezado_pagina': 'Organismos',
            'layout':layout
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_organismo(request, pk):

    title_html = 'Organismo'
    url_cancel = reverse('dashboards:lista_organismo')
    layout = 'layout/default.html'
    object_pk = get_object_or_404(Organismo, pk=pk)
    if request.POST:
        form = OrganismoModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_organismo'),{'layout':layout})
    else:
        form = OrganismoModelForm(instance=object_pk)
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Editar Organismo [ '+ object_pk.nombre+' ]',
            'encabezado_pagina': 'Organismos',
            'object_pk': object_pk,
            'layout': layout
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_organismo(request, pk):
    url_cancel = reverse('dashboards:lista_organismo')
    title_html = 'Organismo'
    layout = 'layout/default.html'
    object = get_object_or_404(Organismo, pk=pk)
    if request.POST:
        object = get_object_or_404(Organismo, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_organismo'), {'layout':layout})
    context = {
        'title_html': title_html,
        'url_cancel': url_cancel,
        'breadcumb_lista': 'Eliminar Organismo [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Organismos',
        'object': object,
        'layout': layout
    }
    return render(request, 'pages/common/delete.html', context)

###################################################
####                Crud Osde                  ####
###################################################
@login_required()
def lista_osde(request, **kwargs):
    object_list = Osde.objects.all()
    crear_url = reverse('dashboards:create_osde')
    title_html = 'Osde'
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_osde", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_osde", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar':url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': title_html,
        'crear_url': crear_url,
        'variables_filtro': variables_filtro,
        'nombre_tabla': 'osde',
        'breadcumb_lista': 'Osde',
        'encabezado_pagina': 'Osde',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/message.js')
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/list.html', context)


@login_required
def create_osde(request):
    title_html = 'Osde'
    url_cancel = reverse('dashboards:lista_osde')
    layout = 'layout/default.html'

    if request.POST:
        form = OsdeModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_osde'),{'layout':layout})
    else:
        form = OsdeModelForm()
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Nueva Osde',
            'encabezado_pagina': 'Osde',
            'layout':layout
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_osde(request, pk):

    title_html = 'Osde'
    url_cancel = reverse('dashboards:lista_osde')
    layout = 'layout/default.html'
    object_pk = get_object_or_404(Osde, pk=pk)
    if request.POST:
        form = OsdeModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_osde'),{'layout':layout})
    else:
        form = OsdeModelForm(instance=object_pk)
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Editar Osde [ '+ object_pk.nombre+' ]',
            'encabezado_pagina': 'Osde',
            'object_pk': object_pk,
            'layout': layout
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_osde(request, pk):
    url_cancel = reverse('dashboards:lista_osde')
    title_html = 'Osde'
    layout = 'layout/default.html'
    object = get_object_or_404(Osde, pk=pk)
    if request.POST:
        object = get_object_or_404(Osde, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_osde'), {'layout':layout})
    context = {
        'title_html': title_html,
        'url_cancel': url_cancel,
        'breadcumb_lista': 'Eliminar Osde [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Osde',
        'object': object,
        'layout': layout
    }
    return render(request, 'pages/common/delete.html', context)

###################################################
####                Crud Empresa               ####
###################################################
@login_required()
def lista_empresa(request, **kwargs):
    object_list = Empresa.objects.all()
    crear_url = reverse('dashboards:create_empresa')
    title_html = 'Empresa'
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_empresa", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_empresa", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar':url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': title_html,
        'crear_url': crear_url,
        'variables_filtro': variables_filtro,
        'nombre_tabla': 'empresa',
        'breadcumb_lista': 'Empresa',
        'encabezado_pagina': 'Empresas',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/message.js')
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/list.html', context)


@login_required
def create_empresa(request):
    title_html = 'Empresa'
    url_cancel = reverse('dashboards:lista_empresa')
    layout = 'layout/default.html'

    if request.POST:
        form = EmpresaModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_empresa'),{'layout':layout})
    else:
        form = EmpresaModelForm()
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Nueva Empresa',
            'encabezado_pagina': 'Empresa',
            'layout':layout
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_empresa(request, pk):

    title_html = 'Empresa'
    url_cancel = reverse('dashboards:lista_empresa')
    layout = 'layout/default.html'
    object_pk = get_object_or_404(Empresa, pk=pk)
    if request.POST:
        form = EmpresaModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_empresa'),{'layout':layout})
    else:
        form = EmpresaModelForm(instance=object_pk)
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Editar Empresa [ '+ object_pk.nombre+' ]',
            'encabezado_pagina': 'Empresa',
            'object_pk': object_pk,
            'layout': layout
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_empresa(request, pk):
    url_cancel = reverse('dashboards:lista_empresa')
    title_html = 'Empresa'
    layout = 'layout/default.html'
    object = get_object_or_404(Empresa, pk=pk)
    if request.POST:
        object = get_object_or_404(Empresa, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_empresa'), {'layout':layout})
    context = {
        'title_html': title_html,
        'url_cancel': url_cancel,
        'breadcumb_lista': 'Eliminar Empresa [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Empresa',
        'object': object,
        'layout': layout
    }
    return render(request, 'pages/common/delete.html', context)

###################################################
####                Crud CategoriaPieza        ####
###################################################
@login_required()
def lista_categoriapieza(request, **kwargs):
    object_list = CategoriaPieza.objects.all()
    crear_url = reverse('dashboards:create_categoriapieza')
    title_html = 'Categoria Pieza'
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_categoriapieza", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_categoriapieza", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar':url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': title_html,
        'crear_url': crear_url,
        'variables_filtro': variables_filtro,
        'nombre_tabla': 'categoriapieza',
        'breadcumb_lista': 'Categoria Pieza',
        'encabezado_pagina': 'Categoria Piezas',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/message.js')
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/list.html', context)


@login_required
def create_categoriapieza(request):
    title_html = 'Categoria Parte'
    url_cancel = reverse('dashboards:lista_categoriapieza')
    layout = 'layout/default.html'

    if request.POST:
        form = CategoriaPiezaModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_categoriapieza'),{'layout':layout})
    else:
        form = CategoriaPiezaModelForm()
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Nueva Categoria Pieza',
            'encabezado_pagina': 'Categoria Pieza',
            'layout':layout
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_categoriapieza(request, pk):

    title_html = 'Empresa'
    url_cancel = reverse('dashboards:lista_categoriapieza')
    layout = 'layout/default.html'
    object_pk = get_object_or_404(Empresa, pk=pk)
    if request.POST:
        form = CategoriaPiezaModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_categoriapieza'),{'layout':layout})
    else:
        form = CategoriaPiezaModelForm(instance=object_pk)
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Editar Categoria Pieza [ '+ object_pk.nombre+' ]',
            'encabezado_pagina': 'Categoria Pieza',
            'object_pk': object_pk,
            'layout': layout
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_categoriapieza(request, pk):
    url_cancel = reverse('dashboards:lista_categoriapieza')
    title_html = 'Categoria Pieza'
    layout = 'layout/default.html'
    object = get_object_or_404(CategoriaPieza, pk=pk)
    if request.POST:
        object = get_object_or_404(CategoriaPieza, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_categoriapieza'), {'layout':layout})
    context = {
        'title_html': title_html,
        'url_cancel': url_cancel,
        'breadcumb_lista': 'Eliminar Categoria Pieza [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Categoria Piezas',
        'object': object,
        'layout': layout
    }
    return render(request, 'pages/common/delete.html', context)

###################################################
####                Crud CategoriaParte        ####
###################################################
@login_required()
def lista_categoriaparte(request, **kwargs):
    object_list = CategoriaParte.objects.all()
    crear_url = reverse('dashboards:create_categoriaparte')
    title_html = 'Categoria Parte'
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_categoriaparte", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_categoriaparte", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar':url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': title_html,
        'crear_url': crear_url,
        'variables_filtro': variables_filtro,
        'nombre_tabla': 'categoriaparte',
        'breadcumb_lista': 'Categoria Parte',
        'encabezado_pagina': 'Categoria Partes',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/message.js')
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/list.html', context)


@login_required
def create_categoriaparte(request):
    title_html = 'Categoria Parte'
    url_cancel = reverse('dashboards:lista_categoriaparte')
    layout = 'layout/default.html'

    if request.POST:
        form = CategoriaParteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_categoriaparte'),{'layout':layout})
    else:
        form = CategoriaParteModelForm()
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Nueva Categoria Parte',
            'encabezado_pagina': 'Categoria Parte',
            'layout':layout
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_categoriaparte(request, pk):

    title_html = 'Categoria Parte'
    url_cancel = reverse('dashboards:lista_categoriaparte')
    layout = 'layout/default.html'
    object_pk = get_object_or_404(CategoriaParte, pk=pk)
    if request.POST:
        form = CategoriaParteModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_categoriaparte'),{'layout':layout})
    else:
        form = CategoriaParteModelForm(instance=object_pk)
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Editar Categoria Parte [ '+ object_pk.nombre+' ]',
            'encabezado_pagina': 'Categoria Parte',
            'object_pk': object_pk,
            'layout': layout
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_categoriaparte(request, pk):
    url_cancel = reverse('dashboards:lista_categoriaparte')
    title_html = 'Categoria Parte'
    layout = 'layout/default.html'
    object = get_object_or_404(CategoriaParte, pk=pk)
    if request.POST:
        object = get_object_or_404(CategoriaParte, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_categoriaparte'), {'layout':layout})
    context = {
        'title_html': title_html,
        'url_cancel': url_cancel,
        'breadcumb_lista': 'Eliminar Categoria Parte [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Categoria Partes',
        'object': object,
        'layout': layout
    }
    return render(request, 'pages/common/delete.html', context)

###################################################
####                Crud Categoria Equipo        ####
###################################################
@login_required()
def lista_categoriaequipo(request, **kwargs):
    object_list = CategoriaEquipo.objects.all()
    crear_url = reverse('dashboards:create_categoriaequipo')
    title_html = 'Categoria Equipo'
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_categoriaequipo", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_categoriaequipo", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar':url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': title_html,
        'crear_url': crear_url,
        'variables_filtro': variables_filtro,
        'nombre_tabla': 'categoriaequipo',
        'breadcumb_lista': 'Categoria Equipo',
        'encabezado_pagina': 'Categoria Equipo',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/message.js')
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/list.html', context)


@login_required
def create_categoriaequipo(request):
    title_html = 'Categoria Equipo'
    url_cancel = reverse('dashboards:lista_categoriaequipo')
    layout = 'layout/default.html'

    if request.POST:
        form = CategoriaEquipoModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_categoriaequipo'),{'layout':layout})
    else:
        form = CategoriaEquipoModelForm()
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Nueva Categoria Equipo',
            'encabezado_pagina': 'Categoria Equipo',
            'layout':layout
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_categoriaequipo(request, pk):

    title_html = 'Categoria Equipo'
    url_cancel = reverse('dashboards:lista_categoriaequipo')
    layout = 'layout/default.html'
    object_pk = get_object_or_404(CategoriaEquipo, pk=pk)
    if request.POST:
        form = CategoriaEquipoModelForm(request.POST, request.FILES, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_categoriaequipo'),{'layout':layout})
    else:
        form = CategoriaEquipoModelForm(instance=object_pk)
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Editar Categoria Equipo [ '+ object_pk.nombre+' ]',
            'encabezado_pagina': 'Categoria Equipo',
            'object_pk': object_pk,
            'layout': layout
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_categoriaequipo(request, pk):
    url_cancel = reverse('dashboards:lista_categoriaequipo')
    title_html = 'Categoria Equipo'
    layout = 'layout/default.html'
    object = get_object_or_404(CategoriaEquipo, pk=pk)
    if request.POST:
        object = get_object_or_404(CategoriaEquipo, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_categoriaequipo'), {'layout':layout})
    context = {
        'title_html': title_html,
        'url_cancel': url_cancel,
        'breadcumb_lista': 'Eliminar Categoria Equipo [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Categoria Equipos',
        'object': object,
        'layout': layout
    }
    return render(request, 'pages/common/delete.html', context)

###################################################
####                Crud Marca                 ####
###################################################
@login_required()
def lista_marca(request, **kwargs):
    object_list = Marca.objects.all()
    crear_url = reverse('dashboards:create_marca')
    title_html = 'Marcas'
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_marca", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_marca", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar':url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': title_html,
        'crear_url': crear_url,
        'variables_filtro': variables_filtro,
        'nombre_tabla': 'marca',
        'breadcumb_lista': 'Marca',
        'encabezado_pagina': 'Marcas',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/message.js')
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/list.html', context)


@login_required
def create_marca(request):
    title_html = 'Marca'
    url_cancel = reverse('dashboards:lista_marca')
    layout = 'layout/default.html'

    if request.POST:
        form = MarcaModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_marca'),{'layout':layout})
    else:
        form = MarcaModelForm()
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Nueva Marca',
            'encabezado_pagina': 'Marcas',
            'layout':layout
        }
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_marca(request, pk):

    title_html = 'Marca'
    url_cancel = reverse('dashboards:lista_marca')
    layout = 'layout/default.html'
    object_pk = get_object_or_404(Marca, pk=pk)
    if request.POST:
        form = MarcaModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_marca'),{'layout':layout})
    else:
        form = MarcaModelForm(instance=object_pk)
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Editar Marca [ '+ object_pk.nombre+' ]',
            'encabezado_pagina': 'Marcas',
            'object_pk': object_pk,
            'layout': layout
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_marca(request, pk):
    url_cancel = reverse('dashboards:lista_marca')
    title_html = 'Marca'
    layout = 'layout/default.html'
    object = get_object_or_404(Marca, pk=pk)
    if request.POST:
        object = get_object_or_404(Marca, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_marca'), {'layout':layout})
    context = {
        'title_html': title_html,
        'url_cancel': url_cancel,
        'breadcumb_lista': 'Eliminar Marca [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Marcas',
        'object': object,
        'layout': layout
    }
    return render(request, 'pages/common/delete.html', context)

###################################################
####                Crud Modelo                 ###
###################################################
@login_required()
def lista_modelo(request, **kwargs):
    object_list = Modelo.objects.all()
    crear_url = reverse('dashboards:create_modelo')
    title_html = 'Modelos'
    nombre_tabla = 'modelo'
    dict_object_list = {}

    for element in object_list:
        url_editar = reverse("dashboards:editar_modelo", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_modelo", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar':url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': title_html,
        'crear_url': crear_url,
        'nombre_tabla': nombre_tabla,
        'breadcumb_lista': 'Modelos',
        'encabezado_pagina': 'Modelos',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    KTTheme.addJavascriptFile('../assets/js/messaje.js')
    return render(request, 'pages/common/list.html', context)

@login_required
def create_modelo(request):
    title_html = 'Modelo'
    url_cancel = reverse('dashboards:lista_modelo')
    layout = 'layout/default.html'

    if request.POST:
        form = ModeloModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_modelo'),{'layout':layout})
    else:
        form = ModeloModelForm()
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Nueva Modelo',
            'encabezado_pagina': 'Modelos',
            'layout':layout
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_modelo(request, pk):

    title_html = 'Modelo'
    url_cancel = reverse('dashboards:lista_modelo')
    layout = 'layout/default.html'
    object_pk = get_object_or_404(Modelo, pk=pk)
    if request.POST:
        form = ModeloModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_modelo'),{'layout':layout})
    else:
        form = ModeloModelForm(instance=object_pk)
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Editar Modelo [ '+ object_pk.nombre+' ]',
            'encabezado_pagina': 'Modelos',
            'object_pk': object_pk,
            'layout': layout
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_modelo(request, pk):
    url_cancel = reverse('dashboards:lista_modelo')
    title_html = 'Marca'
    layout = 'layout/default.html'
    object = get_object_or_404(Modelo, pk=pk)
    if request.POST:
        object = get_object_or_404(Modelo, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_modelo'), {'layout':layout})
    context = {
        'title_html': title_html,
        'url_cancel': url_cancel,
        'breadcumb_lista': 'Eliminar Modelo [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Modelos',
        'object': object,
        'layout': layout
    }
    return render(request, 'pages/common/delete.html', context)

###################################################
####                Crud Propiedad             ####
###################################################
@login_required()
def lista_propiedad(request, **kwargs):
    object_list = Propiedad.objects.all()
    crear_url = reverse('dashboards:create_propiedad')
    title_html = 'Propiedades'
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_propiedad", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_propiedad", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar':url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': title_html,
        'crear_url': crear_url,
        'variables_filtro': variables_filtro,
        'nombre_tabla': 'propiedad',
        'breadcumb_lista': 'Propiedad',
        'encabezado_pagina': 'Propiedades',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/message.js')
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/list.html', context)


@login_required
def create_propiedad(request):
    title_html = 'Propiedad'
    url_cancel = reverse('dashboards:lista_propiedad')
    layout = 'layout/default.html'

    if request.POST:
        form = PropiedadModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_propiedad'),{'layout':layout})
    else:
        form = PropiedadModelForm()
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Nueva Propiedad',
            'encabezado_pagina': 'Propiedades',
            'layout':layout
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_propiedad(request, pk):

    title_html = 'Propiedad'
    url_cancel = reverse('dashboards:lista_propiedad')
    layout = 'layout/default.html'
    object_pk = get_object_or_404(Propiedad, pk=pk)
    if request.POST:
        form = PropiedadModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_propiedad'),{'layout':layout})
    else:
        form = PropiedadModelForm(instance=object_pk)
        context = {
            'title_html': title_html,
            'url_cancel': url_cancel,
            'form': form,
            'breadcumb_lista': 'Editar Propiedad [ '+ object_pk.nombre+' ]',
            'encabezado_pagina': 'Propiedades',
            'object_pk': object_pk,
            'layout': layout
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_propiedad(request, pk):
    url_cancel = reverse('dashboards:lista_propiedad')
    title_html = 'Propiedad'
    layout = 'layout/default.html'
    object = get_object_or_404(Propiedad, pk=pk)
    if request.POST:
        object = get_object_or_404(Propiedad, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_propiedad'), {'layout':layout})
    context = {
        'title_html': title_html,
        'url_cancel': url_cancel,
        'breadcumb_lista': 'Eliminar Propiedad [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Propiedades',
        'object': object,
        'layout': layout
    }
    return render(request, 'pages/common/delete.html', context)

###################################################
####                Crud Pieza                 ###
###################################################

@login_required()
def lista_pieza(request, **kwargs):
    object_list = Pieza.objects.all()
    crear_url = reverse('dashboards:crear_pieza')
    title_html = 'Piezas'
    dict_object_list = {}
    variables_filtro = ['marca', 'modelo', 'empresa', 'organismo', 'osde', 'estado']

    for element in object_list:
        url_editar = reverse("dashboards:editar_pieza", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_pieza", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar,'url_eliminar':url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': title_html,
        'crear_url': crear_url,
        'variables_filtro': variables_filtro,
        'nombre_tabla': 'pieza',
        'breadcumb_lista': 'Piezas',
        'encabezado_pagina': 'Piezas',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    KTTheme.addJavascriptFile('../assets/js/message.js')
    return render(request, 'pages/equipo/list.html', context)

@login_required
def crear_pieza(request):
    title_html = 'Pieza'
    layout = 'layout/default.html'
    url_cancel = reverse('dashboards:lista_pieza')
    if request.POST:
        form = PiezaModelForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                # guardo el modelo pieza
                pieza = form.save()
                # lleno el modelo propiedadpieza con las propiedades que estan asociadas a la pieza
                categoria = CategoriaPieza.objects.get(id=form.cleaned_data['categoria'].id)
                for i in categoria.propiedad.all():
                    propiedad_pieza = PropiedadPieza()
                    propiedad_pieza.pieza_id = pieza.id
                    propiedad_pieza.propiedad_id = i.id
                    propiedad_pieza.save()
                # si no existe la relacion la creo y si existe actualizo los campos boleanos en este caso marco que pertenece a una pieza
                mm, created = MarcaModelo.objects.get_or_create(marca=form.cleaned_data['marca'],
                                                                modelo=form.cleaned_data['modelo'])
                mm.pieza = True
                mm.save()
                messages.success(request,'El elemento ha sido creado satisfactoriamente')
                return HttpResponseRedirect(reverse('dashboards:pieza_propiedad', args=[pieza.id]),{'layout':layout})
    else:
        form = PiezaModelForm()

    return render(request, 'pages/equipo/create_update_equipo.html',
                  {'title_html': title_html,
            'url_cancel': url_cancel,
            'breadcumb_lista': 'Crear Pieza',
            'encabezado_pagina': 'Pieza',
            'form':form,
            'object': object,
            'layout': layout}
                  )

@login_required
def editar_pieza(request, pk):
    title_html = 'Equipo'
    layout = 'layout/default.html'
    url_cancel = reverse('dashboards:lista_pieza')
    categoria_vieja = Pieza.objects.get(id=pk).categoria
    object_pk = get_object_or_404(Pieza, pk=pk)
    if request.POST:
        form = PiezaModelForm(request.POST, request.FILES, instance=object_pk)
        if form.is_valid():
            with transaction.atomic():
                pieza = form.save()

                categoria = CategoriaPieza.objects.get(id=form.cleaned_data['categoria'].id)
                if categoria_vieja.nombre != categoria.nombre:
                    pieza.propiedadpieza_set.all().delete()
                    for i in categoria.propiedad.all():
                        propiedad_pieza = PropiedadPieza()
                        propiedad_pieza.pieza_id = pieza.id
                        propiedad_pieza.propiedad_id = i.id
                        propiedad_pieza.save()
                else:
                    for ppa in pieza.propiedadpieza_set.all():
                        if CategoriaPieza.objects.filter(propiedad=ppa.propiedad, id=categoria.id).first() is None:
                            ppieza = PropiedadPieza.objects.filter(propiedad=ppa.propiedad, pieza=pieza).first()
                            ppieza.delete()

                    for i in categoria.propiedad.all():
                        if ExistePropiedadPieza(pieza.id, i.id) == False:
                            propiedad_pieza = PropiedadPieza()
                            propiedad_pieza.pieza_id = pieza.id
                            propiedad_pieza.propiedad_id = i.id
                            propiedad_pieza.save()
                mm, created = MarcaModelo.objects.get_or_create(marca=form.cleaned_data['marca'],
                                                                modelo=form.cleaned_data['modelo'])
                mm.pieza = True
                mm.save()
                messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
                # if request.GET.get('popup'):
                #     return HttpResponseRedirect(reverse('expediente:equipo_propiedad', args=[object_pk.id]) + 'popup=1')
                # else:
                return HttpResponseRedirect(reverse('dashboards:pieza_propiedad', args=[object_pk.id]),{'layout':layout})

    else:
        form = ParteModelForm(instance=object_pk)
        # form_modelo = ModeloModelForm()
        # form_marca = MarcaModelForm()
    return render(request, 'pages/equipo/create_update_equipo.html',
                  {'form': form, 'object_pk': object_pk, 'url_cancel': url_cancel, 'title_html': title_html,
                    'layout':layout,'nombre_tabla': 'equipo',
                    'breadcumb_lista': 'Editar Equipo ['+object_pk.nombre+']',
                    'encabezado_pagina': 'Equipos',
                   })

@login_required
def eliminar_pieza(request, pk):
    url_cancel = reverse('dashboards:lista_pieza')
    layout = 'layout/default.html'
    title_html = 'Pieza'
    object = get_object_or_404(Pieza, pk=pk)
    if request.POST:
        object = get_object_or_404(Pieza, pk=pk)
        object.propiedadpieza_set.all().delete()
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_pieza'))

    context = {
        'title_html': title_html,
        'url_cancel': url_cancel,
        'breadcumb_lista': 'Eliminar Pieza [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Pieza',
        'object': object,
        'layout': layout
    }
    return render(request, 'pages/common/delete.html', context)

@login_required
def pieza_propiedad(request, pk):
    title_html = 'Pieza'
    layout = 'layout/default.html'
    url_cancel = reverse("dashboards:editar_pieza", args=[pk])
    pieza = get_object_or_404(Pieza, pk=pk)
    propiedades = pieza.propiedadpieza_set.all()
    propiedades_nombres = pieza.propiedades.all()

    PropiedadPiezaFormSet = modelformset_factory(PropiedadPieza, form=PropiedadPiezaModelForm,
                                                  extra=propiedades.count(), max_num=propiedades.count())
    if request.POST:
        formset = PropiedadPiezaFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                pp = PropiedadPieza.objects.get(pieza=pieza, propiedad=form.cleaned_data['propiedad'])
                pp.valor = form.cleaned_data['valor']
                pp.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_pieza'),{'layout':layout})
    else:
        formset = PropiedadPiezaFormSet(queryset=propiedades)
        if propiedades.count() > 0:
            KTTheme.addJavascriptFile('js/propiedad_nombre.js')
            return render(request, 'pages/equipo/equipo_propiedad.html', {'formset': formset,
                                                                    'url_cancel': url_cancel,
                                                                    'propiedades': propiedades,
                                                                    'pieza': pieza,
                                                                    'title_html': title_html,
                                                                        'layout':layout,
                                                                          'breadcumb_lista': 'Establecer Valor a Pieza',
                                                                          'encabezado_pagina': 'Pieza',
                                                                    'propiedades_nombres': propiedades_nombres
                                                                    })
        else:
            return HttpResponseRedirect(reverse('dashboards:lista_pieza'),{'layout':layout})


###################################################
####                Crud Parte                  ###
###################################################

@login_required()
def lista_parte(request, **kwargs):
    object_list = Parte.objects.all()
    crear_url = reverse('dashboards:crear_parte')
    title_html = 'Parte'
    dict_object_list = {}
    variables_filtro = ['marca', 'modelo', 'empresa', 'organismo', 'osde', 'estado']

    for element in object_list:
        url_editar = reverse("dashboards:editar_parte", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_parte", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar,'url_eliminar':url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': title_html,
        'crear_url': crear_url,
        'variables_filtro': variables_filtro,
        'nombre_tabla': 'parte',
        'breadcumb_lista': 'Parte',
        'encabezado_pagina': 'Partes',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    KTTheme.addJavascriptFile('../assets/js/message.js')
    return render(request, 'pages/equipo/list.html', context)

@login_required
def crear_parte(request):
    title_html = 'Parte'
    layout = 'layout/default.html'
    url_cancel = reverse('dashboards:lista_parte')
    if request.POST:
        form = ParteModelForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                # guardo el modelo pieza
                parte = form.save()
                # lleno el modelo propiedadpieza con las propiedades que estan asociadas a la pieza
                categoria = CategoriaParte.objects.get(id=form.cleaned_data['categoria'].id)
                for i in categoria.propiedad.all():
                    propiedad_parte = PropiedadParte()
                    propiedad_parte.parte_id = parte.id
                    propiedad_parte.propiedad_id = i.id
                    propiedad_parte.save()
                # si no existe la relacion la creo y si existe actualizo los campos boleanos en este caso marco que pertenece a una pieza
                mm, created = MarcaModelo.objects.get_or_create(marca=form.cleaned_data['marca'],
                                                                modelo=form.cleaned_data['modelo'])
                mm.parte = True
                mm.save()
                messages.success(request,'El elemento ha sido creado satisfactoriamente')
                return HttpResponseRedirect(reverse('dashboards:parte_propiedad', args=[parte.id]),{'layout':layout})
    else:
        form = ParteModelForm()

    return render(request, 'pages/equipo/create_update_equipo.html',
                  {'title_html': title_html,
            'url_cancel': url_cancel,
            'breadcumb_lista': 'Crear Parte',
            'encabezado_pagina': 'Parte',
            'form':form,
            'object': object,
            'layout': layout}
                  )

@login_required
def editar_parte(request, pk):
    title_html = 'Equipo'
    layout = 'layout/default.html'
    url_cancel = reverse('dashboards:lista_parte')
    categoria_vieja = Parte.objects.get(id=pk).categoria
    object_pk = get_object_or_404(Parte, pk=pk)
    if request.POST:
        form = ParteModelForm(request.POST, request.FILES, instance=object_pk)
        if form.is_valid():
            with transaction.atomic():
                parte = form.save()

                categoria = CategoriaParte.objects.get(id=form.cleaned_data['categoria'].id)
                if categoria_vieja.nombre != categoria.nombre:
                    parte.propiedadparte_set.all().delete()
                    for i in categoria.propiedad.all():
                        propiedad_parte = PropiedadParte()
                        propiedad_parte.pieza_id = parte.id
                        propiedad_parte.propiedad_id = i.id
                        propiedad_parte.save()
                else:
                    for ppa in parte.propiedadparte_set.all():
                        if CategoriaParte.objects.filter(propiedad=ppa.propiedad, id=categoria.id).first() is None:
                            pparte = PropiedadParte.objects.filter(propiedad=ppa.propiedad, parte=parte).first()
                            pparte.delete()

                    for i in categoria.propiedad.all():
                        if ExistePropiedadParte(parte.id, i.id) == False:
                            propiedad_parte = PropiedadParte()
                            propiedad_parte.parte_id = parte.id
                            propiedad_parte.propiedad_id = i.id
                            propiedad_parte.save()
                mm, created = MarcaModelo.objects.get_or_create(marca=form.cleaned_data['marca'],
                                                                modelo=form.cleaned_data['modelo'])
                mm.parte = True
                mm.save()
                messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
                # if request.GET.get('popup'):
                #     return HttpResponseRedirect(reverse('expediente:equipo_propiedad', args=[object_pk.id]) + 'popup=1')
                # else:
                return HttpResponseRedirect(reverse('dashboards:parte_propiedad', args=[object_pk.id]),{'layout':layout})

    else:
        form = ParteModelForm(instance=object_pk)
        # form_modelo = ModeloModelForm()
        # form_marca = MarcaModelForm()
    return render(request, 'pages/equipo/create_update_equipo.html',
                  {'form': form, 'object_pk': object_pk, 'url_cancel': url_cancel, 'title_html': title_html,
                    'layout':layout,'nombre_tabla': 'equipo',
                    'breadcumb_lista': 'Editar Equipo ['+object_pk.nombre+']',
                    'encabezado_pagina': 'Equipos',
                   })

@login_required
def eliminar_parte(request, pk):
    url_cancel = reverse('dashboards:lista_parte')
    layout = 'layout/default.html'
    title_html = 'Parte'
    object = get_object_or_404(Parte, pk=pk)
    if request.POST:
        object = get_object_or_404(Parte, pk=pk)
        object.propiedadparte_set.all().delete()
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_parte'))

    context = {
        'title_html': title_html,
        'url_cancel': url_cancel,
        'breadcumb_lista': 'Eliminar Parte [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Parte',
        'object': object,
        'layout': layout
    }
    return render(request, 'pages/common/delete.html', context)

@login_required
def parte_propiedad(request, pk):
    title_html = 'Parte'
    layout = 'layout/default.html'
    url_cancel = reverse("dashboards:editar_parte", args=[pk])
    parte = get_object_or_404(Parte, pk=pk)
    propiedades = parte.propiedadparte_set.all()
    propiedades_nombres = parte.propiedades.all()

    PropiedadParteFormSet = modelformset_factory(PropiedadParte, form=PropiedadParteModelForm,
                                                  extra=propiedades.count(), max_num=propiedades.count())
    if request.POST:
        formset = PropiedadParteFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                pp = PropiedadParte.objects.get(parte=parte, propiedad=form.cleaned_data['propiedad'])
                pp.valor = form.cleaned_data['valor']
                pp.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_parte'),{'layout':layout})
    else:
        formset = PropiedadParteFormSet(queryset=propiedades)
        if propiedades.count() > 0:
            KTTheme.addJavascriptFile('js/propiedad_nombre.js')
            return render(request, 'pages/equipo/equipo_propiedad.html', {'formset': formset,
                                                                    'url_cancel': url_cancel,
                                                                    'propiedades': propiedades,
                                                                    'pieza': parte,
                                                                    'title_html': title_html,
                                                                        'layout':layout,
                                                                          'breadcumb_lista': 'Establecer Valor a Parte',
                                                                          'encabezado_pagina': 'Parte',
                                                                    'propiedades_nombres': propiedades_nombres
                                                                    })
        else:
            return HttpResponseRedirect(reverse('dashboards:lista_parte'),{'layout':layout})


###################################################
####                Crud Equipo                 ###
###################################################

@login_required()
def lista_equipo(request, **kwargs):
    object_list = Equipo.objects.all()
    crear_url = reverse('dashboards:crear_equipo')
    title_html = 'Vehïculos'
    dict_object_list = {}
    variables_filtro = ['marca', 'modelo', 'empresa', 'organismo', 'osde', 'estado']

    for element in object_list:
        url_editar = reverse("dashboards:editar_equipo", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_equipo", args=[element.pk])
        url_pdf = reverse("dashboards:generar_pdf_equipo", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar,'url_eliminar':url_eliminar,'url_pdf':url_pdf}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': title_html,
        'crear_url': crear_url,
        'variables_filtro': variables_filtro,
        'nombre_tabla': 'equipo',
        'breadcumb_lista': 'Vehïculos',
        'encabezado_pagina': 'Vehïculos',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    KTTheme.addJavascriptFile('../assets/js/message.js')
    return render(request, 'pages/equipo/list.html', context)

@login_required
def crear_equipo(request):
    title_html = 'Vehïculo'
    layout = 'layout/default.html'
    url_cancel = reverse('dashboards:lista_equipo')
    if request.POST:
        form = EquipoModelForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                # guardo el modelo pieza
                equipo = form.save()
                # lleno el modelo propiedadpieza con las propiedades que estan asociadas a la pieza
                categoria = CategoriaEquipo.objects.get(id=form.cleaned_data['categoria'].id)
                for i in categoria.propiedad.all():
                    propiedad_equipo = PropiedadEquipo()
                    propiedad_equipo.equipo_id = equipo.id
                    propiedad_equipo.propiedad_id = i.id
                    propiedad_equipo.save()
                # si no existe la relacion la creo y si existe actualizo los campos boleanos en este caso marco que pertenece a una pieza
                mm, created = MarcaModelo.objects.get_or_create(marca=form.cleaned_data['marca'],
                                                                modelo=form.cleaned_data['modelo'])
                mm.equipo = True
                mm.save()
                messages.success(request,'El elemento ha sido creado satisfactoriamente')
                return HttpResponseRedirect(reverse('dashboards:equipo_propiedad', args=[equipo.id]),{'layout':layout})
    else:
        form = EquipoModelForm()

    return render(request, 'pages/equipo/create_update_equipo.html',
                  {'title_html': title_html,
            'url_cancel': url_cancel,
            'breadcumb_lista': 'Crear Vehïculo',
            'encabezado_pagina': 'Vehïculo',
            'form':form,
            'object': object,
            'layout': layout}
                  )

@login_required
def editar_equipo(request, pk):
    title_html = 'Vehïculo'
    layout = 'layout/default.html'
    url_cancel = reverse('dashboards:lista_equipo')
    categoria_vieja = Equipo.objects.get(id=pk).categoria
    object_pk = get_object_or_404(Equipo, pk=pk)
    if request.POST:
        form = EquipoModelForm(request.POST, request.FILES, instance=object_pk)
        if form.is_valid():
            with transaction.atomic():
                equipo = form.save()

                categoria = CategoriaEquipo.objects.get(id=form.cleaned_data['categoria'].id)
                if categoria_vieja.nombre != categoria.nombre:
                    equipo.propiedadequipo_set.all().delete()
                    for i in categoria.propiedad.all():
                        propiedad_equipo = PropiedadEquipo()
                        propiedad_equipo.equipo_id = equipo.id
                        propiedad_equipo.propiedad_id = i.id
                        propiedad_equipo.save()
                else:
                    for ppa in equipo.propiedadequipo_set.all():
                        if CategoriaEquipo.objects.filter(propiedad=ppa.propiedad, id=categoria.id).first() is None:
                            pequipo = PropiedadEquipo.objects.filter(propiedad=ppa.propiedad, equipo=equipo).first()
                            pequipo.delete()

                    for i in categoria.propiedad.all():
                        if ExistePropiedadEquipo(equipo.id, i.id) == False:
                            propiedad_equipo = PropiedadEquipo()
                            propiedad_equipo.equipo_id = equipo.id
                            propiedad_equipo.propiedad_id = i.id
                            propiedad_equipo.save()
                mm, created = MarcaModelo.objects.get_or_create(marca=form.cleaned_data['marca'],
                                                                modelo=form.cleaned_data['modelo'])
                mm.equipo = True
                mm.save()
                messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
                # if request.GET.get('popup'):
                #     return HttpResponseRedirect(reverse('expediente:equipo_propiedad', args=[object_pk.id]) + 'popup=1')
                # else:
                return HttpResponseRedirect(reverse('dashboards:equipo_propiedad', args=[object_pk.id]),{'layout':layout})

    else:
        form = EquipoModelForm(instance=object_pk)
        # form_modelo = ModeloModelForm()
        # form_marca = MarcaModelForm()
    return render(request, 'pages/equipo/create_update_equipo.html',
                  {'form': form, 'object_pk': object_pk, 'url_cancel': url_cancel, 'title_html': title_html,
                    'layout':layout,'nombre_tabla': 'equipo',
                    'breadcumb_lista': 'Editar Vehïculo ['+object_pk.nombre+']',
                    'encabezado_pagina': 'Vehïculos',
                   })

@login_required
def eliminar_equipo(request, pk):
    url_cancel = reverse('dashboards:lista_equipo')
    layout = 'layout/default.html'
    title_html = 'Vehïculo'
    object = get_object_or_404(Equipo, pk=pk)
    if request.POST:
        object = get_object_or_404(Equipo, pk=pk)
        object.propiedadequipo_set.all().delete()
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_equipo'))

    context = {
        'title_html': title_html,
        'url_cancel': url_cancel,
        'breadcumb_lista': 'Eliminar Vehïculo [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Vehïculo',
        'object': object,
        'layout': layout
    }
    return render(request, 'pages/common/delete.html', context)

@login_required
def equipo_propiedad(request, pk):
    title_html = 'Equipo'
    layout = 'layout/default.html'
    url_cancel = reverse("dashboards:editar_equipo", args=[pk])
    equipo = get_object_or_404(Equipo, pk=pk)
    propiedades = equipo.propiedadequipo_set.all()
    propiedades_nombres = equipo.propiedades.all()

    PropiedadEquipoFormSet = modelformset_factory(PropiedadEquipo, form=PropiedadEquipoModelForm,
                                                  extra=propiedades.count(), max_num=propiedades.count())
    if request.POST:
        formset = PropiedadEquipoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                pp = PropiedadEquipo.objects.get(equipo=equipo, propiedad=form.cleaned_data['propiedad'])
                pp.valor = form.cleaned_data['valor']
                pp.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_equipo'),{'layout':layout})
    else:
        formset = PropiedadEquipoFormSet(queryset=propiedades)
        if propiedades.count() > 0:
            KTTheme.addJavascriptFile('js/propiedad_nombre.js')
            return render(request, 'pages/equipo/equipo_propiedad.html', {'formset': formset,
                                                                    'url_cancel': url_cancel,
                                                                    'propiedades': propiedades,
                                                                    'equipo': equipo,
                                                                    'title_html': title_html,
                                                                        'layout':layout,
                                                                          'breadcumb_lista': 'Establecer Valor a Propiedades',
                                                                          'encabezado_pagina': 'Equipo',
                                                                    'propiedades_nombres': propiedades_nombres
                                                                    })
        else:
            return HttpResponseRedirect(reverse('dashboards:lista_equipo'),{'layout':layout})

# @login_required
class ExpedienteEquipoPDFView(View):
    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL
        sRoot = settings.STATICFILES_DIRS
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        if not os.path.isfile(path):
            raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('pages/equipo/equipo_pdf.html')
            equipo = Equipo.objects.get(pk=self.kwargs['pk'])
            context = {
                'BASE_DIR': str(settings.BASE_DIR),
                'equipo': equipo,
                'icon': '{}{}'.format(settings.STATIC_URL, 'assets/media/empty.jpg'),
                'bootstrap': '{}{}'.format(settings.STATIC_URL, 'assets/css/style.bundle.css'),
            }

            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename = "Expediente #.pdf"'
            response['Content-Disposition'] = 'attachment; filename = "Expediente #' + str(
                equipo.id) + '-' + equipo.categoria.nombre + '-' + equipo.modelo.nombre + '-' + equipo.marca.nombre + '.pdf"'

            pisaStatus = pisa.CreatePDF(html, dest=response,
                                        # link_callback=self.link_callback
                                        )

            if pisaStatus.err:
                return HttpResponse('Error' + html)
            return response
        except Exception as e:
            return str(e)
        return HttpResponseRedirect(reverse_lazy('dashboard:lista_equipo'))


# @login_required
class ListadoEquipoPDFView(View):
    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL
        sRoot = settings.STATICFILES_DIRS
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        if not os.path.isfile(path):
            raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('pages/equipo/listado_equipo_pdf.html')
            equipo = Equipo.objects.all()
            context = {
                'BASE_DIR': str(settings.BASE_DIR),
                'equipo': equipo,
                'icon': '{}{}'.format(settings.STATIC_URL, 'assets/media/empty.jpg'),
                'bootstrap': '{}{}'.format(settings.STATIC_URL, 'assets/css/style.bundle.css'),
            }

            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename = "Expediente #.pdf"'
            response['Content-Disposition'] = 'attachment; filename = "Listado de equipos.pdf"'

            pisaStatus = pisa.CreatePDF(html, dest=response,
                                        # link_callback=self.link_callback
                                        )

            if pisaStatus.err:
                return HttpResponse('Error' + html)
            return response
        except Exception as e:
            return str(e)
        return HttpResponseRedirect(reverse_lazy('dashboard:lista_equipo'))



@login_required
def perfil_usuario(request):
    layout = 'layout/default.html'

    # acciones2 = LogEntry.changes
    acciones = LogEntry.objects.filter(actor_id=request.user.id).order_by('-timestamp')[:8]

    context = {
        'title_html': 'Perfil',
        'acciones':acciones
    }
    context = KTLayout.init(context)

    return render(request, "pages/auth/perfil.html", context)


@login_required()
def reporte_equipo(request):
    layout = 'layout/default.html'
    empresa = Empresa.objects.all()
    marca = Marca.objects.all()
    modelo = Modelo.objects.all()

    context = {
        'title_html': 'Reporte',
        'nombre_tabla': 'reporte',
        'layout': layout,
        'empresa': empresa,
        'marca': marca,
        'modelo': modelo,
        'breadcumb_lista': 'Reporte',
        'encabezado_pagina': 'Reportes',
        'title_html': 'Reporte'
    }

    if request.POST:
        marca_query =request.POST['marca']
        modelo_query =request.POST['modelo']
        estado_query =request.POST['estado']
        empresa_query =request.POST['empresa']
        fecha_range = request.POST.get('fecha_registro', '')

        q=Q()

        if marca_query:
            q &= Q(marca__nombre__icontains=marca_query)
        if modelo_query:
            q &= Q(modelo__nombre__icontains=modelo_query)
        if estado_query:
            q &= Q(estado__icontains=estado_query)
        if fecha_range:
            fecha_inicio, fecha_fin = fecha_range.split(' - ')
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%m/%d/%Y').strftime('%Y-%m-%d')
            fecha_fin = datetime.datetime.strptime(fecha_fin, '%m/%d/%Y').strftime('%Y-%m-%d')
            q &= Q(fecha_registro__range=(fecha_inicio, fecha_fin))

        if q:
            equipos = Equipo.objects.filter(q)
        else:
            equipos = Equipo.objects.all()
        context['consulta'] = equipos

        context = KTLayout.init(context)
        KTTheme.addJavascriptFile('../assets/js/forms.js')
        KTTheme.addJavascriptFile('../assets/js/kt_table.js')
        return render(request, "pages/equipo/reporte_equipo.html", context)

    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/forms.js',)
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, "pages/equipo/reporte_equipo.html", context)
