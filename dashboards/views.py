import datetime
import os
from django.utils.html import escape

from _decimal import Decimal
from auditlog.models import LogEntry
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Q
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template
from django.utils.dateparse import parse_date
from django.utils.decorators import method_decorator
from django.views.defaults import permission_denied
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
    top_3_equipo = []
    top_4_equipo_empresa = []
    today = datetime.date.today()
    month = today.month
    year = today.year
    equipos_por_categoria = []
    partes = Parte.objects.all()
    piezas = Pieza.objects.all()
    activos = Equipo.objects.filter(estado__nombre='Activo')
    venta = Equipo.objects.filter(estado__nombre='Venta')
    reparacion = Equipo.objects.filter(estado__nombre='Reparación')
    equipos = Equipo.objects.all()
    equipos_venta = Equipo.objects.filter(estado__nombre='Venta')
    equipos_venta_ultimo_mes = Equipo.objects.filter(estado__nombre='Venta', fecha_registro__month=month)
    equipos_reparacion = Equipo.objects.filter(estado__nombre='Reparación')

    for categoria in CategoriaEquipo.objects.all():
        equipos_cat = Equipo.objects.filter(categoria=categoria).order_by('-fecha_registro')
        if equipos_cat:
            equipos_por_categoria.append({'categoria': categoria, 'equipos_cat': equipos_cat})

    top_3_equipo_por_marca = Marca.objects.annotate(cant_equipos=Count('equipo')).order_by('-cant_equipos')[:3]
    top_4_equipo_por_empresa = Empresa.objects.annotate(cant_equipos=Count('equipo')).order_by('-cant_equipos')[:4]

    for equipo in top_3_equipo_por_marca:
        top_3_equipo.append({'marca': equipo.nombre, 'cant': equipo.cant_equipos})

    for empresa in top_4_equipo_por_empresa:
        top_4_equipo_empresa.append({'empresa': empresa.nombre, 'cant': equipo.cant_equipos})

    # crecimiento mensual de registro de equipos
    cantidad_actual = Equipo.objects.filter(fecha_registro__month=month - 1, fecha_registro__year=year).count()
    cantidad_actual_venta = Equipo.objects.filter(estado__nombre='Venta', fecha_registro__month=month - 1,
                                                  fecha_registro__year=year).count()

    mes_anterior = month - 2
    anno_anterior = year
    if mes_anterior == 0:
        mes_anterior = 12
        anno_anterior = year - 1

    previous_count = Equipo.objects.filter(fecha_registro__month=mes_anterior,
                                           fecha_registro__year=anno_anterior).count()
    previous_count_venta = Equipo.objects.filter(estado__nombre='Venta', fecha_registro__month=mes_anterior,
                                                 fecha_registro__year=anno_anterior).count()
    if previous_count != 0:
        porciento_crecimiento_mensual = Decimal((cantidad_actual - previous_count) / previous_count) * 100
        porciento_crecimiento_mensual_venta = Decimal(
            (cantidad_actual_venta - previous_count_venta) / previous_count_venta) * 100
    else:
        porciento_crecimiento_mensual = Decimal((cantidad_actual - previous_count)) * 100
        porciento_crecimiento_mensual_venta = Decimal((cantidad_actual_venta - previous_count_venta)) * 100
        if equipos_venta.count() == 0:
            porciento = 0
        else:
            porciento = (equipos_venta.count() / equipos.count()) * 100


    context = {
        'equipos': equipos,
        'equipos_venta': {'equipos_venta': equipos_venta, 'porciento': porciento},
        'equipos_venta_ultimo_mes': equipos_venta_ultimo_mes,
        'equipos_reparacion': equipos_reparacion,
        'top_3_equipo': top_3_equipo,
        'layout': 'layout/default.html',
        'activos': activos,
        'reparacion': reparacion,
        'venta': venta,
        'partes': partes,
        'piezas': piezas,
        'top_4_equipo_empresa': top_4_equipo_empresa,
        'equipos_por_categoria': equipos_por_categoria,
        'porciento_crecimiento_mensual': porciento_crecimiento_mensual,
        'porciento_crecimiento_mensual_venta': porciento_crecimiento_mensual_venta
    }
    context = KTLayout.init(context)

    return render(request, "pages/dashboards/index.html", context)


@login_required
def handlePopAdd(request, addForm, field):
    if request.method == "POST":
        form = addForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                newObject = form.save(commit=False)
                newObject.save()

            except:
                newObject = None

            p = request.GET.get('_popup', '')
            if p == '1':
                return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % (
                        escape(newObject._get_pk_val()), escape(newObject)))
            else:
                return HttpResponse(
                    '<script type="text/javascript">opener.returnBackAddAnotherPopup(window, "%s", "%s");</script>' % (
                        escape(newObject._get_pk_val()), escape(newObject)))

    else:
        form = addForm()

    pageContext = {'form': form, 'field': field}
    return render(request, "pages/popadd.html", pageContext)


@login_required
def addModelo(request):
    return handlePopAdd(request, ModeloModelForm, 'Modelo')


@login_required
def addMarca(request):
    return handlePopAdd(request, MarcaModelForm, 'Marca')


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
    try:
        if not request.user.groups.filter(permissions__codename='view_organismo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = Organismo.objects.all()
    dict_object_list = {}

    for element in object_list:
        url_editar = reverse("dashboards:editar_organismo", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_organismo", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Organismos',
        'crear_url': reverse('dashboards:create_organismo'),
        'nombre_tabla': 'organismo',
        'layout': 'layout/default.html',
        'breadcumb_lista': 'Organismo',
        'encabezado_pagina': 'Organismos',
    }
    KTTheme.addJavascriptFile('../assets/js/message.js')
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/list.html', context)


@login_required
def create_organismo(request):
    try:
        if not request.user.groups.filter(permissions__codename='add_organismo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = OrganismoModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_organismo'), {'layout': 'layout/default.html'})
    else:
        form = OrganismoModelForm()
        context = {
            'title_html': 'Organismo',
            'url_cancel': reverse('dashboards:lista_organismo'),
            'form': form,
            'breadcumb_lista': 'Nueva Organismo',
            'encabezado_pagina': 'Organismos',
            'layout': 'layout/default.html'
        }
    return render(request, 'pages/common/create_update.html', context)


@login_required
def editar_organismo(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_organismo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_pk = get_object_or_404(Organismo, pk=pk)
    if request.POST:
        form = OrganismoModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_organismo'), {'layout': 'layout/default.html'})
    else:
        form = OrganismoModelForm(instance=object_pk)
        context = {
            'title_html': 'Organismo',
            'url_cancel': reverse('dashboards:lista_organismo'),
            'form': form,
            'breadcumb_lista': 'Editar Organismo [ ' + object_pk.nombre + ' ]',
            'encabezado_pagina': 'Organismos',
            'object_pk': object_pk,
            'layout': 'layout/default.html'
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_organismo(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_organismo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(Organismo, pk=pk)
    if request.POST:
        object = get_object_or_404(Organismo, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_organismo'), {'layout': 'layout/default.html'})
    context = {
        'title_html': 'Organismo',
        'url_cancel': reverse('dashboards:lista_organismo'),
        'breadcumb_lista': 'Eliminar Organismo [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Organismos',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


###################################################
####                Crud Osde                  ####
###################################################
@login_required()
def lista_osde(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_osde'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = Osde.objects.all()
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_osde", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_osde", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Osde',
        'crear_url': reverse('dashboards:create_osde'),
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
    try:
        if not request.user.groups.filter(permissions__codename='add_osde'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = OsdeModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_osde'), {'layout': 'layout/default.html'})
    else:
        form = OsdeModelForm()
        context = {
            'title_html': 'Osde',
            'url_cancel': reverse('dashboards:lista_osde'),
            'form': form,
            'breadcumb_lista': 'Nueva Osde',
            'encabezado_pagina': 'Osde',
            'layout': 'layout/default.html'
        }
    return render(request, 'pages/common/create_update.html', context)


@login_required
def editar_osde(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_osde'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_pk = get_object_or_404(Osde, pk=pk)
    if request.POST:
        form = OsdeModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_osde'), {'layout': 'layout/default.html'})
    else:
        form = OsdeModelForm(instance=object_pk)
        context = {
            'title_html': 'Osde',
            'url_cancel': reverse('dashboards:lista_osde'),
            'form': form,
            'breadcumb_lista': 'Editar Osde [ ' + object_pk.nombre + ' ]',
            'encabezado_pagina': 'Osde',
            'object_pk': object_pk,
            'layout': 'layout/default.html'
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_osde(request, pk):
    try:
        if not request.user.hgroups.filter(permissions__codename='delete_osde'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(Osde, pk=pk)
    if request.POST:
        object = get_object_or_404(Osde, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_osde'), {'layout': 'layout/default.html'})
    context = {
        'title_html': 'Osde',
        'url_cancel': reverse('dashboards:lista_osde'),
        'breadcumb_lista': 'Eliminar Osde [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Osde',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


###################################################
####                Crud Empresa               ####
###################################################
@login_required()
def lista_empresa(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_empresa'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = Empresa.objects.all()
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_empresa", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_empresa", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Empresa',
        'crear_url': reverse('dashboards:create_empresa'),
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
    try:
        if not request.user.groups.filter(permissions__codename='add_empresa'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = EmpresaModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_empresa'), {'layout': 'layout/default.html'})
    else:
        form = EmpresaModelForm()
        context = {
            'title_html': 'Empresa',
            'url_cancel': reverse('dashboards:lista_empresa'),
            'form': form,
            'breadcumb_lista': 'Nueva Empresa',
            'encabezado_pagina': 'Empresa',
            'layout': 'layout/default.html'
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_empresa(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_empresa'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_pk = get_object_or_404(Empresa, pk=pk)
    if request.POST:
        form = EmpresaModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_empresa'), {'layout': 'layout/default.html'})
    else:
        form = EmpresaModelForm(instance=object_pk)
        context = {
            'title_html': 'Empresa',
            'url_cancel': reverse('dashboards:lista_empresa'),
            'form': form,
            'breadcumb_lista': 'Editar Empresa [ ' + object_pk.nombre + ' ]',
            'encabezado_pagina': 'Empresa',
            'object_pk': object_pk,
            'layout': 'layout/default.html'
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_empresa(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_empresa'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(Empresa, pk=pk)
    if request.POST:
        object = get_object_or_404(Empresa, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_empresa'), {'layout': 'layout/default.html'})
    context = {
        'title_html': 'Empresa',
        'url_cancel': reverse('dashboards:lista_empresa'),
        'breadcumb_lista': 'Eliminar Empresa [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Empresa',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


###################################################
####                Crud CategoriaPieza        ####
###################################################
@login_required()
def lista_categoriapieza(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_categoriapieza'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = CategoriaPieza.objects.all()
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_categoriapieza", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_categoriapieza", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Categoria Pieza',
        'crear_url': reverse('dashboards:create_categoriapieza'),
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
    try:
        if not request.user.groups.filter(permissions__codename='add_categoriapieza'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = CategoriaPiezaModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_categoriapieza'), {'layout': 'layout/default.html'})
    else:
        form = CategoriaPiezaModelForm()
        context = {
            'title_html': 'Categoria Pieza',
            'url_cancel': reverse('dashboards:lista_categoriapieza'),
            'form': form,
            'breadcumb_lista': 'Nueva Categoria Pieza',
            'encabezado_pagina': 'Categoria Pieza',
            'layout': 'layout/default.html'
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_categoriapieza(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_categoriapieza'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_pk = get_object_or_404(CategoriaPieza, pk=pk)
    if request.POST:
        form = CategoriaPiezaModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_categoriapieza'), {'layout': 'layout/default.html'})
    else:
        form = CategoriaPiezaModelForm(instance=object_pk)
        context = {
            'title_html': 'Categoria Pieza',
            'url_cancel': reverse('dashboards:lista_categoriapieza'),
            'form': form,
            'breadcumb_lista': 'Editar Categoria Pieza [ ' + object_pk.nombre + ' ]',
            'encabezado_pagina': 'Categoria Pieza',
            'object_pk': object_pk,
            'layout': 'layout/default.html'
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_categoriapieza(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_categoriapieza'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(CategoriaPieza, pk=pk)
    if request.POST:
        object = get_object_or_404(CategoriaPieza, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_categoriapieza'), {'layout': 'layout/default.html'})
    context = {
        'title_html': 'Categoria Pieza',
        'url_cancel': reverse('dashboards:lista_categoriapieza'),
        'breadcumb_lista': 'Eliminar Categoria Pieza [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Categoria Piezas',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


###################################################
####                Crud CategoriaParte        ####
###################################################
@login_required()
def lista_categoriaparte(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_categoriaparte'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = CategoriaParte.objects.all()
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_categoriaparte", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_categoriaparte", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Categoria Parte',
        'crear_url': reverse('dashboards:create_categoriaparte'),
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
    try:
        if not request.user.groups.filter(permissions__codename='add_categoriaparte'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = CategoriaParteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_categoriaparte'), {'layout': 'layout/default.html'})
    else:
        form = CategoriaParteModelForm()
        context = {
            'title_html': 'Categoria Parte',
            'url_cancel': reverse('dashboards:lista_categoriaparte'),
            'form': form,
            'breadcumb_lista': 'Nueva Categoria Parte',
            'encabezado_pagina': 'Categoria Parte',
            'layout': 'layout/default.html'
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_categoriaparte(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_categoriaparte'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_pk = get_object_or_404(CategoriaParte, pk=pk)
    if request.POST:
        form = CategoriaParteModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_categoriaparte'), {'layout': 'layout/default.html'})
    else:
        form = CategoriaParteModelForm(instance=object_pk)
        context = {
            'title_html': 'Categoria Parte',
            'url_cancel': reverse('dashboards:lista_categoriaparte'),
            'form': form,
            'breadcumb_lista': 'Editar Categoria Parte [ ' + object_pk.nombre + ' ]',
            'encabezado_pagina': 'Categoria Parte',
            'object_pk': object_pk,
            'layout': 'layout/default.html'
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_categoriaparte(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_categoriaparte'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(CategoriaParte, pk=pk)
    if request.POST:
        object = get_object_or_404(CategoriaParte, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_categoriaparte'), {'layout': 'layout/default.html'})
    context = {
        'title_html': 'Categoria Parte',
        'url_cancel': reverse('dashboards:lista_categoriaparte'),
        'breadcumb_lista': 'Eliminar Categoria Parte [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Categoria Partes',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


###################################################
####                Crud Categoria Equipo        ####
###################################################
@login_required()
def lista_categoriaequipo(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_categoriaequipo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = CategoriaEquipo.objects.all()

    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_categoriaequipo", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_categoriaequipo", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Categoria Equipo',
        'crear_url': reverse('dashboards:create_categoriaequipo'),
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
    try:
        if not request.user.groups.filter(permissions__codename='add_categoriaequipo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = CategoriaEquipoModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_categoriaequipo'), {'layout': 'layout/default.html'})
    else:
        form = CategoriaEquipoModelForm()
        context = {
            'title_html': 'Categoria Equipo',
            'url_cancel': reverse('dashboards:lista_categoriaequipo'),
            'form': form,
            'breadcumb_lista': 'Nueva Categoria Equipo',
            'encabezado_pagina': 'Categoria Equipo',
            'layout': 'layout/default.html'
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_categoriaequipo(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_categoriaequipo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_pk = get_object_or_404(CategoriaEquipo, pk=pk)
    if request.POST:
        form = CategoriaEquipoModelForm(request.POST, request.FILES, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_categoriaequipo'), {'layout': 'layout/default.html'})
    else:
        form = CategoriaEquipoModelForm(instance=object_pk)
        context = {
            'title_html': 'Categoria Equipo',
            'url_cancel': reverse('dashboards:lista_categoriaequipo'),
            'form': form,
            'breadcumb_lista': 'Editar Categoria Equipo [ ' + object_pk.nombre + ' ]',
            'encabezado_pagina': 'Categoria Equipo',
            'object_pk': object_pk,
            'layout': 'layout/default.html'
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_categoriaequipo(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_categoriaequipo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(CategoriaEquipo, pk=pk)
    if request.POST:
        object = get_object_or_404(CategoriaEquipo, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_categoriaequipo'), {'layout': 'layout/default.html'})
    context = {
        'title_html': 'Categoria Equipo',
        'url_cancel': reverse('dashboards:lista_categoriaequipo'),
        'breadcumb_lista': 'Eliminar Categoria Equipo [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Categoria Equipos',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


###################################################
####                Crud Marca                 ####
###################################################
@login_required()
def lista_marca(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_marca'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = Marca.objects.all()
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_marca", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_marca", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Marcas',
        'crear_url': reverse('dashboards:create_marca'),
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
    try:
        if not request.user.groups.filter(permissions__codename='add_marca'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = MarcaModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_marca'), {'layout': 'layout/default.html'})
    else:
        form = MarcaModelForm()
        context = {
            'title_html': 'Marca',
            'url_cancel': reverse('dashboards:lista_marca'),
            'form': form,
            'breadcumb_lista': 'Nueva Marca',
            'encabezado_pagina': 'Marcas',
            'layout': 'layout/default.html'
        }
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_marca(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='add_marca'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_pk = get_object_or_404(Marca, pk=pk)
    if request.POST:
        form = MarcaModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_marca'), {'layout': 'layout/default.html'})
    else:
        form = MarcaModelForm(instance=object_pk)
        context = {
            'title_html': 'Marca',
            'url_cancel': reverse('dashboards:lista_marca'),
            'form': form,
            'breadcumb_lista': 'Editar Marca [ ' + object_pk.nombre + ' ]',
            'encabezado_pagina': 'Marcas',
            'object_pk': object_pk,
            'layout': 'layout/default.html'
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_marca(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_marca'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(Marca, pk=pk)
    if request.POST:
        object = get_object_or_404(Marca, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_marca'), {'layout': 'layout/default.html'})
    context = {
        'title_html': 'Marca',
        'url_cancel': reverse('dashboards:lista_marca'),
        'breadcumb_lista': 'Eliminar Marca [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Marcas',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


###################################################
####                Crud Modelo                 ###
###################################################
@login_required()
def lista_modelo(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_modelo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = Modelo.objects.all()
    nombre_tabla = 'modelo'
    dict_object_list = {}

    for element in object_list:
        url_editar = reverse("dashboards:editar_modelo", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_modelo", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Modelos',
        'crear_url': reverse('dashboards:create_modelo'),
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
    try:
        if not request.user.groups.filter(permissions__codename='add_modelo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = ModeloModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_modelo'), {'layout': 'layout/default.html'})
    else:
        form = ModeloModelForm()
        context = {
            'title_html': 'Modelo',
            'url_cancel': reverse('dashboards:lista_modelo'),
            'form': form,
            'breadcumb_lista': 'Nueva Modelo',
            'encabezado_pagina': 'Modelos',
            'layout': 'layout/default.html'
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_modelo(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_modelo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_pk = get_object_or_404(Modelo, pk=pk)
    if request.POST:
        form = ModeloModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_modelo'), {'layout': 'layout/default.html'})
    else:
        form = ModeloModelForm(instance=object_pk)
        context = {
            'title_html': 'Modelo',
            'url_cancel': reverse('dashboards:lista_modelo'),
            'form': form,
            'breadcumb_lista': 'Editar Modelo [ ' + object_pk.nombre + ' ]',
            'encabezado_pagina': 'Modelos',
            'object_pk': object_pk,
            'layout': 'layout/default.html'
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_modelo(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_modelo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(Modelo, pk=pk)
    if request.POST:
        object = get_object_or_404(Modelo, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_modelo'), {'layout': 'layout/default.html'})
    context = {
        'title_html': 'Marca',
        'url_cancel': reverse('dashboards:lista_modelo'),
        'breadcumb_lista': 'Eliminar Modelo [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Modelos',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


###################################################
####                Crud Propiedad             ####
###################################################
@login_required()
def lista_propiedad(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_propiedad'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = Propiedad.objects.all()
    dict_object_list = {}
    variables_filtro = ['nombre']

    for element in object_list:
        url_editar = reverse("dashboards:editar_propiedad", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_propiedad", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Propiedades',
        'crear_url': reverse('dashboards:create_propiedad'),
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
    try:
        if not request.user.groups.filter(permissions__codename='add_propiedad'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = PropiedadModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido creado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_propiedad'), {'layout': 'layout/default.html'})
    else:
        form = PropiedadModelForm()
        context = {
            'title_html': 'Propiedad',
            'url_cancel': reverse('dashboards:lista_propiedad'),
            'form': form,
            'breadcumb_lista': 'Nueva Propiedad',
            'encabezado_pagina': 'Propiedades',
            'layout': 'layout/default.html'
        }
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def editar_propiedad(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_propiedad'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_pk = get_object_or_404(Propiedad, pk=pk)
    if request.POST:
        form = PropiedadModelForm(request.POST, instance=object_pk)
        if form.is_valid():
            form.save()
            messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
            return HttpResponseRedirect(reverse('dashboards:lista_propiedad'), {'layout': 'layout/default.html'})
    else:
        form = PropiedadModelForm(instance=object_pk)
        context = {
            'title_html': 'Propiedad',
            'url_cancel': reverse('dashboards:lista_propiedad'),
            'form': form,
            'breadcumb_lista': 'Editar Propiedad [ ' + object_pk.nombre + ' ]',
            'encabezado_pagina': 'Propiedades',
            'object_pk': object_pk,
            'layout': 'layout/default.html'
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_propiedad(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_propiedad'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(Propiedad, pk=pk)
    if request.POST:
        object = get_object_or_404(Propiedad, pk=pk)
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_propiedad'), {'layout': 'layout/default.html'})
    context = {
        'title_html': 'Propiedad',
        'url_cancel': reverse('dashboards:lista_propiedad'),
        'breadcumb_lista': 'Eliminar Propiedad [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Propiedades',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


###################################################
####                Crud Pieza                 ###
###################################################

@login_required()
def lista_pieza(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_pieza'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = Pieza.objects.all()
    dict_object_list = {}

    for element in object_list:
        url_editar = reverse("dashboards:editar_pieza", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_pieza", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Piezas',
        'crear_url': reverse('dashboards:crear_pieza'),
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
    try:
        if not request.user.groups.filter(permissions__codename='add_pieza'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = PiezaModelForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                # guardo el modelo pieza
                pieza = form.save()

                # lleno el modelo propiedadpieza con las propiedades que estan asociadas a la pieza
                categoria = CategoriaPieza.objects.get(id=form.cleaned_data['categoria'].id)
                for i in categoria.propiedad.all():
                    propiedad_pieza, created = PropiedadPieza.objects.get_or_create(propiedad_id=i.id,
                                                                                    pieza_id=pieza.id)

                    # si no existe la relacion la creo y si existe actualizo los campos boleanos en este caso marco que pertenece a una pieza
                mm, created = MarcaModelo.objects.get_or_create(marca=form.cleaned_data['marca'],
                                                                modelo=form.cleaned_data['modelo'])
                mm.pieza = True
                mm.save()
                messages.success(request, 'El elemento ha sido creado satisfactoriamente')
                return HttpResponseRedirect(reverse('dashboards:pieza_propiedad', args=[pieza.id]),
                                            {'layout': 'layout/default.html'})
    else:
        form = PiezaModelForm()

    return render(request, 'pages/equipo/wizzard/create_pieza.html',
                  {'title_html': 'Pieza',
                   'url_cancel': reverse('dashboards:lista_pieza'),
                   'breadcumb_lista': 'Crear Pieza',
                   'encabezado_pagina': 'Pieza',
                   'form': form,
                   'object': object,
                   'layout': 'layout/default.html'}
                  )


@login_required
def editar_pieza(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_pieza'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    equipo_get = request.GET.get('equipo_id')
    parte_get = request.GET.get('parte_id')

    if equipo_get:
        url_cancel = reverse('dashboards:pieza_propiedad', args=[pk]) + '?equipo_id=' + equipo_get+'&parte_id='+parte_get
        url_finalizar = reverse('dashboards:llenar_datos_parte_equipo',args=[equipo_get])+'?equipo_id='+equipo_get
    else:
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
                if equipo_get:
                    return HttpResponseRedirect(reverse('dashboards:pieza_propiedad', args=[object_pk.id])+'?equipo_id='+equipo_get+'&parte_id='+parte_get,
                                            {'layout': 'layout/default.html'})
                else:
                    return HttpResponseRedirect(reverse('dashboards:pieza_propiedad', args=[object_pk.id]),
                                                {'layout': 'layout/default.html'})

    else:
        form = ParteModelForm(instance=object_pk)
    return render(request, 'pages/equipo/wizzard/create_pieza.html',
                  {'form': form, 'object_pk': object_pk, 'url_cancel': url_cancel,
                   'title_html': 'Pieza',
                   'layout': 'layout/default.html', 'nombre_tabla': 'pieza',
                   'breadcumb_lista': 'Editar Pieza [' + object_pk.nombre + ']',
                   'encabezado_pagina': 'Piezas',
                   })


@login_required
def eliminar_pieza(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_pieza'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(Pieza, pk=pk)
    if request.POST:
        object = get_object_or_404(Pieza, pk=pk)
        object.propiedadpieza_set.all().delete()
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_pieza'))

    context = {
        'title_html': 'Pieza',
        'url_cancel': reverse('dashboards:lista_pieza'),
        'breadcumb_lista': 'Eliminar Pieza [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Pieza',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


@login_required
def pieza_propiedad(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_pieza'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    equipo_get = request.GET.get('equipo_id')
    parte_get = request.GET.get('parte_id')
    if equipo_get:
        url_cancel = reverse('dashboards:editar_pieza', args=[pk]) + '?equipo_id=' + equipo_get+'&parte_id='+parte_get
        url_finalizar = reverse('dashboards:lista_equipo')
    else:
        url_cancel = reverse('dashboards:editar_pieza', args=[pk])
        url_finalizar = None

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
            if equipo_get:
                return HttpResponseRedirect(reverse('dashboards:llenar_datos_pieza_parte', args=[int(parte_get)])+ '?equipo_id=' + equipo_get+'&parte_id='+parte_get,
                                        {'layout': 'layout/default.html'})
            else:
                return HttpResponseRedirect(reverse('dashboards:lista_pieza'),
                                            {'layout': 'layout/default.html'})
    else:
        formset = PropiedadPiezaFormSet(queryset=propiedades)
        if propiedades.count() > 0:
            KTTheme.addJavascriptFile('js/propiedad_nombre.js')
            return render(request, 'pages/equipo/wizzard/propiedades.html', {'formset': formset,
                                                                             'url_cancel': url_cancel,
                                                                             'url_finalizar': url_finalizar,
                                                                             'pieza': pieza,
                                                                             'title_html': 'Pieza',
                                                                             'layout': 'layout/default.html',
                                                                             'breadcumb_lista': 'Establecer Valor a Pieza',
                                                                             'encabezado_pagina': 'Pieza',
                                                                             'propiedades_nombres': propiedades_nombres
                                                                             })
        else:
            return HttpResponseRedirect(reverse('dashboards:lista_pieza'), {'layout': 'layout/default.html'})


###################################################
####                Crud Parte                  ###
###################################################

@login_required()
def lista_parte(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_parte'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = Parte.objects.all()
    dict_object_list = {}

    for element in object_list:
        url_editar = reverse("dashboards:editar_parte", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_parte", args=[element.pk])
        url_propiedades = reverse("dashboards:parte_propiedad", args=[element.pk])
        url_piezas = reverse("dashboards:llenar_datos_pieza_parte", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar,'url_propiedades':url_propiedades, 'url_piezas':url_piezas}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Parte',
        'crear_url': reverse('dashboards:crear_parte'),
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
    try:
        if not request.user.groups.filter(permissions__codename='add_parte'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = ParteModelForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                # guardo el modelo pieza
                parte = form.save()
                # lleno el modelo propiedadpieza con las propiedades que estan asociadas a la pieza
                categoria = CategoriaParte.objects.get(id=form.cleaned_data['categoria'].id)
                for i in categoria.propiedad.all():
                    propiedad_parte, created = PropiedadParte.objects.get_or_create(propiedad_id=i.id,
                                                                                    parte_id=parte.id)

                if CategoriaPartexPiezas.objects.filter(categoriaparte=categoria).count() > 0:
                    cat_parte_pieza = CategoriaPartexPiezas.objects.get(categoriaparte=categoria)
                    for c in cat_parte_pieza.parte.all():
                        parte.piezas.add(c)
                # si no existe la relacion la creo y si existe actualizo los campos boleanos en este caso marco que pertenece a una pieza
                mm, created = MarcaModelo.objects.get_or_create(marca=form.cleaned_data['marca'],
                                                                modelo=form.cleaned_data['modelo'])
                mm.parte = True
                mm.save()
                messages.success(request, 'El elemento ha sido creado satisfactoriamente')
                return HttpResponseRedirect(reverse('dashboards:parte_propiedad', args=[parte.id]),
                                            {'layout': 'layout/default.html'})
    else:
        form = ParteModelForm()

    return render(request, 'pages/equipo/wizzard/create_parte.html',
                  {'title_html': 'Parte',
                   'url_cancel': reverse('dashboards:lista_parte'),
                   'breadcumb_lista': 'Nueva Parte',
                   'encabezado_pagina': 'Nueva Parte',
                   'form': form,
                   'object': object,
                   'layout': 'layout/default.html'}
                  )


@login_required
def editar_parte(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_parte'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    equipo_get = request.GET.get('equipo_id')
    if equipo_get:
        url_cancel = reverse('dashboards:llenar_datos_parte_equipo', args=[int(equipo_get)])
        url_finalizar = reverse('dashboards:lista_equipo')
    else:
        url_cancel = reverse('dashboards:lista_parte')
        url_finalizar = None

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
                        propiedad_parte, created = PropiedadParte.objects.get_or_create(parte_id=parte.id,
                                                                                        propiedad_id=i.id)

                    for j in form.cleaned_data['propiedades']:
                        propiedad_parte, created = PropiedadParte.objects.get_or_create(propiedad_id=j.id,
                                                                                        parte_id=parte.id)

                else:
                    for ppa in parte.propiedadparte_set.all():
                        if CategoriaParte.objects.filter(propiedad=ppa.propiedad, id=categoria.id).first() is None:
                            pparte = PropiedadParte.objects.filter(propiedad=ppa.propiedad, parte=parte).first()
                            pparte.delete()

                    for i in categoria.propiedad.all():
                        propiedad_parte, created = PropiedadParte.objects.get_or_create(parte_id=parte.id,
                                                                                        propiedad_id=i.id)

                    for j in form.cleaned_data['propiedades']:
                        propiedad_parte, created = PropiedadParte.objects.get_or_create(propiedad_id=j.id,
                                                                                        parte_id=parte.id)

                if CategoriaPartexPiezas.objects.filter(categoriaparte=categoria).count() > 0:
                    cat_parte_pieza = CategoriaPartexPiezas.objects.filter(categoriaparte=categoria).first()
                    for c in cat_parte_pieza.pieza.all():
                        parte.piezas.add(c)

                mm, created = MarcaModelo.objects.get_or_create(marca=form.cleaned_data['marca'],
                                                                modelo=form.cleaned_data['modelo'])
                mm.parte = True
                mm.save()
                messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.nombre)
                # if request.GET.get('popup'):
                #     return HttpResponseRedirect(reverse('expediente:equipo_propiedad', args=[object_pk.id]) + 'popup=1')
                # else:
                return HttpResponseRedirect(
                    reverse('dashboards:parte_propiedad', args=[object_pk.id]) + '?equipo_id=' + equipo_get,
                    {'layout': 'layout/default.html'})

    else:
        form = ParteModelForm(instance=object_pk)
    return render(request, 'pages/equipo/wizzard/create_parte.html',
                  {'form': form, 'object_pk': object_pk,
                   'url_cancel': url_cancel,
                   'url_finalizar': url_finalizar,
                   'title_html': 'Parte',
                   'layout': 'layout/default.html', 'nombre_tabla': 'equipo',
                   'breadcumb_lista': 'Editar [' + object_pk.nombre + ']',
                   'encabezado_pagina': 'Equipos',
                   })


@login_required
def eliminar_parte(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_parte'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(Parte, pk=pk)
    if request.POST:
        object = get_object_or_404(Parte, pk=pk)
        object.propiedadparte_set.all().delete()
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_parte'))

    context = {
        'title_html': 'Parte',
        'url_cancel': reverse('dashboards:lista_parte'),
        'breadcumb_lista': 'Eliminar [ ' + object.nombre + ' ]',
        'encabezado_pagina': 'Parte',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


@login_required
def parte_propiedad(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_parte'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    equipo_get = request.GET.get('equipo_id')
    if equipo_get:
        url_cancel = reverse('dashboards:editar_parte', args=[pk]) + '?equipo_id=' + equipo_get
        url_finalizar = reverse('dashboards:llenar_datos_parte_equipo',args=[equipo_get])
    else:
        url_cancel = reverse('dashboards:editar_parte', args=[pk])
        url_finalizar = None

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
            if equipo_get:
                return HttpResponseRedirect(
                    reverse('dashboards:llenar_datos_pieza_parte', args=[parte.id]) + '?equipo_id=' + equipo_get+'&parte_id='+str(parte.id),
                    {'layout': 'layout/default.html'})
            else:
                return HttpResponseRedirect(reverse('dashboards:lista_parte'),{'layout': 'layout/default.html'})
    else:
        formset = PropiedadParteFormSet(queryset=propiedades)
        if propiedades.count() > 0:
            return render(request, 'pages/equipo/wizzard/propiedades.html', {'formset': formset,
                                                                             'url_cancel': url_cancel,
                                                                             'url_finalizar': url_finalizar,
                                                                             'propiedades': propiedades,
                                                                             'parte': parte,
                                                                             'title_html': 'Parte',
                                                                             'layout': 'layout/default.html',
                                                                             'breadcumb_lista': 'Establecer Valor a propiedades de la Parte ['+parte.nombre+']',
                                                                             'encabezado_pagina': 'Parte',
                                                                             })
        else:
            return HttpResponseRedirect(reverse('dashboards:lista_parte'), {'layout': 'layout/default.html'})


###################################################
####                Crud Equipo                 ###
###################################################

@login_required()
def lista_equipo(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_equipo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.user.groups.filter(name='Tramitador'):
        object_list = Equipo.objects.filter(user=request.user)
    else:
        object_list = Equipo.objects.filter()

    dict_object_list = {}

    for element in object_list:
        url_editar = reverse("dashboards:editar_equipo", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_equipo", args=[element.pk])
        url_pdf = reverse("dashboards:generar_pdf_equipo", args=[element.pk])
        url_detalle = reverse("dashboards:detalle_equipo", args=[element.pk])
        url_propiedades = reverse("dashboards:equipo_propiedad", args=[element.pk])
        url_partes = reverse("dashboards:llenar_datos_parte_equipo", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar, 'url_pdf': url_pdf,
                                     'url_detalle': url_detalle,'url_propiedades':url_propiedades,'url_partes':url_partes}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Vehículos',
        'crear_url': reverse('dashboards:crear_equipo'),
        'nombre_tabla': 'equipo',
        'breadcumb_lista': 'Vehículos',
        'encabezado_pagina': 'Vehículos',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    KTTheme.addJavascriptFile('../assets/js/message.js')

    return render(request, 'pages/equipo/list.html', context)


@login_required
def crear_equipo(request):
    try:
        if not request.user.groups.filter(permissions__codename='add_equipo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = EquipoModelForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                # guardo el modelo pieza
                equipo = form.save(commit=False)
                equipo.user = request.user
                equipo.save()
                img = None
                fotos = request.FILES.getlist('fotos')
                for f in fotos:
                    img = Imagen.objects.create(
                        imagen=f,
                    )
                    equipo.fotos.add(img)

                # lleno el modelo propiedadpieza con las propiedades que estan asociadas a la pieza
                categoria = CategoriaEquipo.objects.get(id=form.cleaned_data['categoria'].id)
                for i in categoria.propiedad.all():
                    propiedad_equipo, created = PropiedadEquipo.objects.get_or_create(propiedad_id=i.id,
                                                                                      equipo_id=equipo.id)
                for j in form.cleaned_data['propiedades']:
                    propiedad_equipo, created = PropiedadEquipo.objects.get_or_create(propiedad_id=j.id,
                                                                                      equipo_id=equipo.id)

                # obtengo la categoria en la tabla donde se configura cuales piezsa pertenecen a un equipo para agregarle las pieza una vez creado el mismo
                if CategoriaEquipoxPartes.objects.filter(categoriaequipo=categoria).count() > 0:
                    cat_equipo_parte = CategoriaEquipoxPartes.objects.get(categoriaequipo=categoria)
                    for c in cat_equipo_parte.parte.all():
                        equipo.partes.add(c)

                # si no existe la relacion la creo y si existe actualizo los campos boleanos en este caso marco que pertenece a una pieza
                mm, created = MarcaModelo.objects.get_or_create(marca=form.cleaned_data['marca'],
                                                                modelo=form.cleaned_data['modelo'])
                mm.equipo = True
                mm.save()
                messages.success(request, 'El elemento ha sido creado satisfactoriamente')
                return HttpResponseRedirect(reverse('dashboards:equipo_propiedad', args=[equipo.id]),
                                            {'layout': 'layout/default.html'})
    else:
        form = EquipoModelForm()

    KTTheme.addJavascriptFile('../assets/js/RelatedObjectLookups.js')
    KTTheme.addJavascriptFile('../assets/js/forms.js')
    return render(request, 'pages/equipo/wizzard/create_equipo.html',
                  {'title_html': 'Vehículo',
                   'url_cancel': reverse('dashboards:lista_equipo'),
                   'breadcumb_lista': 'Nuevo Vehículo',
                   'encabezado_pagina': 'Nuevo Vehículo',
                   'form': form,
                   'object': object,
                   'layout': 'layout/default.html'}
                  )


@login_required
def editar_equipo(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_equipo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    categoria_vieja = Equipo.objects.get(id=pk).categoria
    object_pk = get_object_or_404(Equipo, pk=pk)
    if request.POST:
        form = EquipoModelForm(request.POST, request.FILES, instance=object_pk)
        if form.is_valid():
            with transaction.atomic():
                equipo = form.save()
                equipo.fotos.all().delete()
                img = None
                fotos = request.FILES.getlist('fotos')
                for f in fotos:
                    img = Imagen.objects.create(
                        imagen=f,
                    )
                    equipo.fotos.add(img)

                categoria = CategoriaEquipo.objects.get(id=form.cleaned_data['categoria'].id)
                if categoria_vieja.nombre != categoria.nombre:
                    equipo.propiedadequipo_set.all().delete()
                    for i in categoria.propiedad.all():
                        propiedad_equipo, created = PropiedadEquipo.objects.get_or_create(propiedad_id=i.id,
                                                                                          equipo_id=equipo.id)

                    for j in form.cleaned_data['propiedades']:
                        propiedad_equipo, created = PropiedadEquipo.objects.get_or_create(propiedad_id=j.id,
                                                                                          equipo_id=equipo.id)

                else:
                    for ppa in equipo.propiedadequipo_set.all():
                        if CategoriaEquipo.objects.filter(propiedad=ppa.propiedad, id=categoria.id).first() is None:
                            pparte = PropiedadEquipo.objects.filter(propiedad=ppa.propiedad, equipo=equipo).first()
                            pparte.delete()

                    for i in categoria.propiedad.all():
                        propiedad_equipo, created = PropiedadEquipo.objects.get_or_create(propiedad_id=i.id,
                                                                                          equipo_id=equipo.id)

                    for j in form.cleaned_data['propiedades']:
                        propiedad_equipo, created = PropiedadEquipo.objects.get_or_create(propiedad_id=j.id,
                                                                                          equipo_id=equipo.id)

                mm, created = MarcaModelo.objects.get_or_create(marca=form.cleaned_data['marca'],
                                                                modelo=form.cleaned_data['modelo'])
                mm.equipo = True
                mm.save()
                messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.codigo)
                # if request.GET.get('popup'):
                #     return HttpResponseRedirect(reverse('expediente:equipo_propiedad', args=[object_pk.id]) + 'popup=1')
                # else:
                return HttpResponseRedirect(reverse('dashboards:equipo_propiedad', args=[object_pk.id]),
                                            {'layout': 'layout/default.html'})

    else:
        form = EquipoModelForm(instance=object_pk)
    return render(request, 'pages/equipo/wizzard/create_equipo.html',
                  {'form': form, 'object_pk': object_pk, 'url_cancel': reverse('dashboards:lista_equipo'),
                   'title_html': 'Vehículo',
                   'layout': 'layout/default.html', 'nombre_tabla': 'equipo',
                   'breadcumb_lista': 'Editar Vehículo [' + object_pk.marca.nombre + ' - ' + object_pk.modelo.nombre + ']',
                   'encabezado_pagina': 'Vehículos',
                   })


@login_required
def eliminar_equipo(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_equipo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(Equipo, pk=pk)
    if request.POST:
        object = get_object_or_404(Equipo, pk=pk)
        object.propiedadequipo_set.all().delete()
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.codigo)
        return HttpResponseRedirect(reverse('dashboards:lista_equipo'))

    context = {
        'title_html': 'Vehículo',
        'url_cancel': reverse('dashboards:lista_equipo'),
        'breadcumb_lista': 'Eliminar Vehículos [ ' + object.codigo + ' ]',
        'encabezado_pagina': 'Vehículos',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


@login_required
def equipo_propiedad(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_equipo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

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
            return HttpResponseRedirect(reverse('dashboards:llenar_datos_parte_equipo', args=[equipo.id]),
                                        {'layout': 'layout/default.html'})
    else:
        formset = PropiedadEquipoFormSet(queryset=propiedades)
        if propiedades.count() > 0:
            return render(request, 'pages/equipo/wizzard/propiedades.html', {'formset': formset,
                                                                             'url_cancel': reverse(
                                                                                 "dashboards:editar_equipo", args=[pk]),
                                                                             'propiedades': propiedades,
                                                                             'equipo': equipo,
                                                                             'title_html': 'Vehículo',
                                                                             'layout': 'layout/default.html',
                                                                             'breadcumb_lista': 'Establecer Valor a Propiedades',
                                                                             'encabezado_pagina': 'Vehículo',
                                                                             })
        else:
            return HttpResponseRedirect(reverse('dashboards:llenar_datos_parte_equipo'),
                                        {'layout': 'layout/default.html'})


@login_required
def detalle_equipo(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='view_equipo'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    equipo = Equipo.objects.get(pk=pk)

    context = {
        'equipo': equipo,
        'title_html': 'Detalle de Vehículo',
        'layout': 'layout/default.html',
        'breadcumb_lista': 'Detalle de ['+equipo.marca.nombre+' - '+equipo.modelo.nombre+']',
        'encabezado_pagina': 'Vehículo',
    }

    return render(request, 'pages/equipo/detalle_equipo.html', context)


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
    try:
        if not request.user.groups.filter(permissions__codename='view_userperfil'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    acciones = LogEntry.objects.filter(actor_id=request.user.id).order_by('-timestamp')[:8]
    perfil = request.user.userperfil
    equipos = Equipo.objects.filter(user=perfil.user)

    context = {
        'title_html': 'Perfil',
        'acciones': acciones,
        'perfil': perfil,
        'equipos': equipos,
        'breadcumb_lista': 'Perfil'
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
        marca_query = request.POST['marca']
        modelo_query = request.POST['modelo']
        estado_query = request.POST['estado']
        empresa_query = request.POST['empresa']
        fecha_range = request.POST.get('fecha_registro', '')

        q = Q()

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
    KTTheme.addJavascriptFile('../assets/js/forms.js', )
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, "pages/equipo/reporte_equipo.html", context)


@login_required()
def error(request):
    return render(request, 'pages/auth/error.html', {'title': 'Permisos'})


# Pruebasss de configuracion de los equipos partes y piezas
# configurar las partes para cada equipo
@login_required()
def lista_equipoxparte(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_categoriaequipoxpartes'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = CategoriaEquipoxPartes.objects.all()

    dict_object_list = {}

    for element in object_list:
        url_editar = reverse("dashboards:editar_equipoxparte", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_equipoxparte", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Configuraciones Vehículo',
        'crear_url': reverse('dashboards:create_equipoxparte'),
        'nombre_tabla': 'equipoxparte',
        'breadcumb_lista': 'Configuraciones Vehículo',
        'encabezado_pagina': 'Configuraciones Vehículo',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/message.js')
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/list.html', context)


@login_required
def create_equipoxparte(request):
    try:
        if not request.user.groups.filter(permissions__codename='add_categoriaequipoxpartes'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = EquipoxParteModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido configurado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_equipoxparte'), {'layout': 'layout/default.html'})
    else:
        form = EquipoxParteModelForm()
        context = {
            'title_html': 'Configuracion de Vehículo',
            'url_cancel': reverse('dashboards:lista_equipoxparte'),
            'form': form,
            'breadcumb_lista': 'Crear Configuracion de Vehículo',
            'encabezado_pagina': 'Configurar Vehículo',
            'layout': 'layout/default.html'
        }
    return render(request, 'pages/common/create_update.html', context)


@login_required
def editar_equipoxparte(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_categoriaequipoxpartes'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_pk = get_object_or_404(CategoriaEquipoxPartes, pk=pk)
    if request.POST:
        form = EquipoxParteModelForm(request.POST, request.FILES, instance=object_pk)
        if form.is_valid():
            with transaction.atomic():
                cat = form.save()
                equipo = Equipo.objects.filter(categoria=cat.categoriaequipo)
                nombre_equipos = []
                usuarios = []
                for e in equipo:
                    e.partes.clear()
                    nombre_equipos.append(e.marca.nombre+' - '+e.modelo.nombre)
                    usuarios.append(e.user)
                    for p in cat.parte.all():
                        e.partes.add(p)


                asunto = 'Se configuro nuevamente la categoria ['+object_pk.categoriaequipo.nombre+']'
                mensaje = 'Sufrieron cambios en las partes los sigueintes equipo['.join(nombre_equipos)+']'

                notificacion = Notificacion.objects.create(asunto=asunto,mensaje=mensaje)
                for u in usuarios:
                    u.notificaciones.add(notificacion)

                messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.categoriaequipo.nombre)
                return HttpResponseRedirect(reverse('dashboards:lista_equipoxparte'), {'layout': 'layout/default.html'})
    else:
        form = EquipoxParteModelForm(instance=object_pk)
        context = {
            'title_html': 'Editar Configuracion Vehículo',
            'url_cancel': reverse('dashboards:lista_equipoxparte'),
            'form': form,
            'breadcumb_lista': 'Editar Configuracion Vehículo [ ' + object_pk.categoriaequipo.nombre + ' ]',
            'encabezado_pagina': 'Configurar Vehículo',
            'object_pk': object_pk,
            'layout': 'layout/default.html'
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_equipoxparte(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_categoriaequipoxpartes'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(CategoriaEquipoxPartes, pk=pk)
    if request.POST:
        object = get_object_or_404(CategoriaEquipoxPartes, pk=pk)
        object.parte.delete()
        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.categoriaequipo.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_equipoxparte'), {'layout': 'layout/default.html'})
    context = {
        'title_html': 'Eliminar Configuracion de Vehículo',
        'url_cancel': reverse('dashboards:lista_equipoxparte'),
        'breadcumb_lista': 'Eliminar Configuracion de Vehículo [ ' + object.categoriaequipo.nombre + ' ]',
        'encabezado_pagina': 'Configuracion de Vehículo',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)


# configurando las piezas para cada parte
@login_required()
def lista_partexpieza(request, **kwargs):
    try:
        if not request.user.groups.filter(permissions__codename='view_categoriapartexpiezas'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_list = CategoriaPartexPiezas.objects.all()

    dict_object_list = {}

    for element in object_list:
        url_editar = reverse("dashboards:editar_partexpieza", args=[element.pk])
        url_eliminar = reverse("dashboards:eliminar_partexpieza", args=[element.pk])
        dict_object_list[element] = {'url_editar': url_editar, 'url_eliminar': url_eliminar}

    context = {
        'dict_object_list': dict_object_list,
        'title_html': 'Configuraciones Partes',
        'crear_url': reverse('dashboards:create_partexpieza'),
        'nombre_tabla': 'equipoxparte',
        'breadcumb_lista': 'Configuraciones Partes',
        'encabezado_pagina': 'Configuraciones Partes',
    }
    context = KTLayout.init(context)
    KTTheme.addJavascriptFile('../assets/js/message.js')
    KTTheme.addJavascriptFile('../assets/js/kt_table.js')
    return render(request, 'pages/common/list.html', context)


@login_required
def create_partexpieza(request):
    try:
        if not request.user.groups.filter(permissions__codename='add_categoriapartexpiezas'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    if request.POST:
        form = PartexPiezaModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'El elemento ha sido configurado satisfactoriamente')
            return HttpResponseRedirect(reverse('dashboards:lista_partexpieza'), {'layout': 'layout/default.html'})
    else:
        form = PartexPiezaModelForm()
        context = {
            'title_html': 'Configuracion de Partes',
            'url_cancel': reverse('dashboards:lista_partexpieza'),
            'form': form,
            'breadcumb_lista': 'Crear Configuracion de Partes',
            'encabezado_pagina': 'Configurar Partes',
            'layout': 'layout/default.html'
        }
    return render(request, 'pages/common/create_update.html', context)


@login_required
def editar_partexpieza(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_categoriapartexpiezas'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_pk = get_object_or_404(CategoriaPartexPiezas, pk=pk)
    if request.POST:
        form = PartexPiezaModelForm(request.POST, request.FILES, instance=object_pk)
        if form.is_valid():

            with transaction.atomic():
                cat = form.save()
                parte = Parte.objects.filter(categoria=cat.categoriaparte)
                nombre_parte = []
                usuarios = []
                for e in parte:
                    e.piezas.clear()
                    nombre_parte.append(e.marca.nombre + ' - ' + e.modelo.nombre)
                    usuarios.append(e.user)
                    for p in cat.pieza.all():
                        e.piezas.add(p)


                asunto = 'Se configuro nuevamente la categoria ['+object_pk.categoriaequipo.nombre+']'
                mensaje = 'Sufrieron cambios en las partes los sigueintes equipo['.join(nombre_parte)+']'

                notificacion = Notificacion.objects.create(asunto=asunto,mensaje=mensaje)
                for u in usuarios:
                    u.notificaciones.add(notificacion)


                messages.success(request, '%s ha sido actualizado satisfactoriamente' % object_pk.categoriaparte.nombre)
                return HttpResponseRedirect(reverse('dashboards:lista_partexpieza'), {'layout': 'layout/default.html'})
    else:
        form = PartexPiezaModelForm(instance=object_pk)
        context = {
            'title_html': 'Editar Configuracion Partes',
            'url_cancel': reverse('dashboards:lista_partexpieza'),
            'form': form,
            'breadcumb_lista': 'Editar Configuracion Partes [ ' + object_pk.categoriaparte.nombre + ' ]',
            'encabezado_pagina': 'Configurar Partes',
            'object_pk': object_pk,
            'layout': 'layout/default.html'
        }
    # if request.path == reverse("marca_crear_popup"):
    #     return render(request, 'add/popadd.html', {'form': form, 'url_cancel': url_cancel})
    return render(request, 'pages/common/create_update.html',
                  context)


@login_required
def eliminar_partexpieza(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='delete_categoriapartexpiezas'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object = get_object_or_404(CategoriaPartexPiezas, pk=pk)
    if request.POST:
        object = get_object_or_404(CategoriaPartexPiezas, pk=pk)

        object.delete()

        messages.success(request, '%s ha sido eliminado satisfactoriamente' % object.categoriaparte.nombre)
        return HttpResponseRedirect(reverse('dashboards:lista_partexpieza'), {'layout': 'layout/default.html'})
    context = {
        'title_html': 'Eliminar Configuracion de Partes',
        'url_cancel': reverse('dashboards:lista_partexpieza'),
        'breadcumb_lista': 'Eliminar Configuracion de Partes [ ' + object.categoriaparte.nombre + ' ]',
        'encabezado_pagina': 'Configuracion de Partes',
        'object': object,
        'layout': 'layout/default.html'
    }
    return render(request, 'pages/common/delete.html', context)



def llenar_datos_parte_equipo(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_parte'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    object_pk = Equipo.objects.get(id=pk)
    objetos = object_pk.partes.all()

    equipo_get = request.GET.get('equipo_id')
    KTTheme.addJavascriptFile('../assets/js/message.js')
    return render(request, 'pages/equipo/wizzard/partes_del_equipo.html',
                  {'object_pk': object_pk, 'url_cancel': reverse('dashboards:equipo_propiedad', args=[object_pk.id])+'?equipo_id='+str(object_pk.id),
                   'title_html': 'Partes de [' + object_pk.marca.nombre + ' - ' + object_pk.modelo.nombre + ']',
                   'layout': 'layout/default.html', 'objetos': objetos,
                   'breadcumb_lista': 'Partes de [' + object_pk.marca.nombre + ' - ' + object_pk.modelo.nombre + ']',
                   'encabezado_pagina': 'Equipos',
                   })


def llenar_datos_pieza_parte(request, pk):
    try:
        if not request.user.groups.filter(permissions__codename='change_pieza'):
            raise PermissionDenied
    except PermissionDenied:
        return redirect('dashboards:error')

    equipo_get = request.GET.get('equipo_id')
    parte_get = request.GET.get('parte_id')
    if equipo_get:
        url_cancel = reverse('dashboards:parte_propiedad', args=[pk]) + '?equipo_id=' + equipo_get
    else:
        url_cancel = reverse('dashboards:parte_propiedad', args=[pk])

    equipo = Equipo.objects.get(id=int(equipo_get))
    parte = Parte.objects.get(id=pk)
    objetos = parte.piezas.all()

    url_finalizar = reverse('dashboards:llenar_datos_parte_equipo', args=[equipo_get]) + '?equipo_id=' + equipo_get

    KTTheme.addJavascriptFile('../assets/js/message.js')
    return render(request, 'pages/equipo/wizzard/piezas_de_las_partes.html',
                  {'object_pk': parte, 'url_cancel': url_cancel,
                   'title_html': 'Parte',
                   'url_finalizar': url_finalizar,
                   'equipo':equipo,
                   'parte_get':parte_get,
                   'layout': 'layout/default.html', 'objetos': objetos,
                   'breadcumb_lista': 'Piezas de [' + parte.nombre+ ']',
                   'encabezado_pagina': 'Equipos',
                   })
