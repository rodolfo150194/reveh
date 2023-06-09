import os
import django
from random import randint
from django.contrib.auth.models import User
from dashboards.models import Marca, Modelo, Organismo, Osde, Provincia, Empresa, CategoriaPieza, CategoriaParte, \
    CategoriaEquipo, CategoriaInsumo, Propiedad, PropiedadPieza, PropiedadParte, PropiedadEquipo, Insumo, Pieza, Parte, \
    Equipo, MarcaModelo, PropiedadInsumo

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_keenthemes.settings')
django.setup()


def create_data():
    # Crear Provincias
    provincia1 = Provincia.objects.create(nombre='Mendoza', codigo='54', sigla='MZA')
    provincia2 = Provincia.objects.create(nombre='Buenos Aires', codigo='01', sigla='BUE')
    provincia3 = Provincia.objects.create(nombre='San Juan', codigo='67', sigla='SJU')

    # Crear Organismo
    organismo1 = Organismo.objects.create(nombre='Organismo 1', codigo='O1', sigla='O1')
    organismo2 = Organismo.objects.create(nombre='Organismo 2', codigo='O2', sigla='O2')

    # Crear OSDE
    osde1 = Osde.objects.create(organismo=organismo1, codigo='OSDE1', nombre='OSDE1', sigla='OSDE1')
    osde2 = Osde.objects.create(organismo=organismo2, codigo='OSDE2', nombre='OSDE2', sigla='OSDE2')

    # Crear Empresas
    empresa1 = Empresa.objects.create(osde=osde1, provincia=provincia1, nombre='Empresa 1', reup_code='Reup 1',
                                       codigo='E1')
    empresa2 = Empresa.objects.create(osde=osde2, provincia=provincia2, nombre='Empresa 2', reup_code='Reup 2',
                                       codigo='E2')

    # Crear Marcas
    marca1 = Marca.objects.create(nombre='Marca 1')
    marca2 = Marca.objects.create(nombre='Marca 2')
    marca3 = Marca.objects.create(nombre='Marca 3')
    marca4 = Marca.objects.create(nombre='Marca 4')

    # Crear Modelos
    modelo1 = Modelo.objects.create(nombre='Modelo 1')
    modelo2 = Modelo.objects.create(nombre='Modelo 2')
    modelo3 = Modelo.objects.create(nombre='Modelo 3')
    modelo4 = Modelo.objects.create(nombre='Modelo 4')

    # Crear MarcaModelo
    marca_modelo1 = MarcaModelo.objects.create(marca=marca1, modelo=modelo1, equipo=True, parte=False, pieza=False,
                                               insumo=False)
    marca_modelo2 = MarcaModelo.objects.create(marca=marca2, modelo=modelo2, equipo=False, parte=True, pieza=False,
                                               insumo=False)
    marca_modelo3 = MarcaModelo.objects.create(marca=marca3, modelo=modelo3, equipo=False, parte=False, pieza=True,
                                               insumo=False)
    marca_modelo4 = MarcaModelo.objects.create(marca=marca4, modelo=modelo4, equipo=False, parte=False, pieza=False,
                                               insumo=True)

    # Crear Propiedades
    propiedad1 = Propiedad.objects.create(nombre='Propiedad 1')
    propiedad2 = Propiedad.objects.create(nombre='Propiedad 2')
    propiedad3 = Propiedad.objects.create(nombre='Propiedad 3')
    propiedad4 = Propiedad.objects.create(nombre='Propiedad 4')
    propiedad5 = Propiedad.objects.create(nombre='Propiedad 5')

    # Crear CategoriasPiezas
    categoria_pieza1 = CategoriaPieza.objects.create(nombre='Categoria Pieza 1')
    categoria_pieza1.propiedad.set([propiedad1, propiedad2])

    categoria_pieza2 = CategoriaPieza.objects.create(nombre='Categoria Pieza 2')
    categoria_pieza2.propiedad.set([propiedad3, propiedad4])

    # Crear CategoriasPartes
    categoria_parte1 = CategoriaParte.objects.create(nombre='Categoria Parte 1')
    categoria_parte1.propiedad.set([propiedad1, propiedad3])

    categoria_parte2 = CategoriaParte.objects.create(nombre='Categoria Parte 2')
    categoria_parte2.propiedad.set([propiedad2, propiedad4])

    # Crear CategoriasEquipos
    categoria_equipo1 = CategoriaEquipo.objects.create(nombre='Categoria Equipo 1')
    categoria_equipo1.propiedad.set([propiedad1, propiedad4])

    categoria_equipo2 = CategoriaEquipo.objects.create(nombre='Categoria Equipo 2')
    categoria_equipo2.propiedad.set([propiedad2, propiedad3])

    # Crear CategoriasInsumos
    categoria_insumo1 = CategoriaInsumo.objects.create(nombre='Categoria Insumo 1')
    categoria_insumo1.propiedad.set([propiedad3, propiedad4])

    categoria_insumo2 = CategoriaInsumo.objects.create(nombre='Categoria Insumo 2')
    categoria_insumo2.propiedad.set([propiedad1, propiedad2])

    # Crear Insumos
    insumo1 = Insumo.objects.create(categoria=categoria_insumo1, nombre='Insumo 1', marca=marca1, modelo=modelo1,
                                    descripcion='Descripcion 1')

    insumo2 = Insumo.objects.create(categoria=categoria_insumo2, nombre='Insumo 2', marca=marca2, modelo=modelo2,
                                    descripcion='Descripcion 2')

    # Crear PropiedadesInsumos
    propiedad_insumo1 = PropiedadInsumo.objects.create(insumo=insumo1, propiedad=propiedad3, valor='Valor 1')
    propiedad_insumo2 = PropiedadInsumo.objects.create(insumo=insumo1, propiedad=propiedad4, valor='Valor 2')

    propiedad_insumo3 = PropiedadInsumo.objects.create(insumo=insumo2, propiedad=propiedad1, valor='Valor 3')
    propiedad_insumo4 = PropiedadInsumo.objects.create(insumo=insumo2, propiedad=propiedad2, valor='Valor 4')

    # Crear Piezas
    pieza1 = Pieza.objects.create(categoria=categoria_pieza1, nombre='Pieza 1', marca=marca3, modelo=modelo3,
                                  descripcion='Descripcion 3')

    pieza2 = Pieza.objects.create(categoria=categoria_pieza2, nombre='Pieza 2', marca=marca4, modelo=modelo4,
                                  descripcion='Descripcion 4')

    # Crear PropiedadesPiezas
    propiedad_pieza1 = PropiedadPieza.objects.create(pieza=pieza1, propiedad=propiedad1, valor='Valor 1')
    propiedad_pieza2 = PropiedadPieza.objects.create(pieza=pieza1, propiedad=propiedad2, valor='Valor 2')

    propiedad_pieza3 = PropiedadPieza.objects.create(pieza=pieza2, propiedad=propiedad3, valor='Valor 3')
    propiedad_pieza4 = PropiedadPieza.objects.create(pieza=pieza2, propiedad=propiedad4, valor='Valor 4')

    # Crear Partes
    parte1 = Parte.objects.create(categoria=categoria_parte1, nombre='Parte 1', marca=marca2, modelo=modelo2,
                                    descripcion='Descripcion 2')

    parte2 = Parte.objects.create(categoria=categoria_parte2, nombre='Parte 2', marca=marca1, modelo=modelo1,
                                    descripcion='Descripcion 1')

    # Crear PropiedadesPartes
    propiedad_parte1 = PropiedadParte.objects.create(parte=parte1, propiedad=propiedad1, valor='Valor 1')
    propiedad_parte2 = PropiedadParte.objects.create(parte=parte1, propiedad=propiedad3, valor='Valor 2')

    propiedad_parte3 = PropiedadParte.objects.create(parte=parte2, propiedad=propiedad2, valor='Valor 3')
    propiedad_parte4 = PropiedadParte.objects.create(parte=parte2, propiedad=propiedad4, valor='Valor 4')

    # Crear Equipos
    equipo1 = Equipo.objects.create(empresa=empresa1, categoria=categoria_equipo1, nombre='Equipo 1', marca=marca4,
                                     modelo=modelo4, descripcion='Descripcion 4', estado='Activo')

    equipo2 = Equipo.objects.create(empresa=empresa2, categoria=categoria_equipo2, nombre='Equipo 2', marca=marca3,
                                     modelo=modelo3, descripcion='Descripcion 3', estado='Reparación')

    # Crear PropiedadesEquipos
    propiedad_equipo1 = PropiedadEquipo.objects.create(equipo=equipo1, propiedad=propiedad1, valor='Valor 1')
    propiedad_equipo2 = PropiedadEquipo.objects.create(equipo=equipo1, propiedad=propiedad4, valor='Valor 2')

    propiedad_equipo3 = PropiedadEquipo.objects.create(equipo=equipo2, propiedad=propiedad2, valor='Valor 3')
    propiedad_equipo4 = PropiedadEquipo.objects.create(equipo=equipo2, propiedad=propiedad3, valor='Valor 4')

    # Asignar Piezas
    equipo1.piezas.set([pieza1, pieza2])
    equipo2.piezas.set([pieza2])

    # Asignar Partes
    equipo1.partes.set([parte1])
    equipo2.partes.set([parte2])

    # Asignar Insumos
    parte1.insumo.set([insumo1])
    parte2.insumo.set([insumo2])

    # Asignar MarcaModelos a Modelos
    modelo1.marca.add(marca1)
    modelo2.marca.add(marca2)
    modelo3.marca.add(marca3)
    modelo4.marca.add(marca4)

    # Comprobar qué se ha creado
    print('Provincias', Provincia.objects.all())
    print('Organismos', Organismo.objects.all())
    print('OSDEs', Osde.objects.all())
    print('Empresas', Empresa.objects.all())
    print('Marcas', Marca.objects.all())
    print('Modelos', Modelo.objects.all())
    print('MarcaModelos', MarcaModelo.objects.all())
    print('Propiedades', Propiedad.objects.all())
    print('CategoriasPiezas', CategoriaPieza.objects.all())
    print('CategoriasPartes', CategoriaParte.objects.all())
    print('CategoriasEquipos', CategoriaEquipo.objects.all())
    print('CategoriasInsumos', CategoriaInsumo.objects.all())
    print('Insumos', Insumo.objects.all())
    print('PropiedadesInsumos', PropiedadInsumo.objects.all())
    print('Piezas', Pieza.objects.all())
    print('PropiedadesPiezas', PropiedadPieza.objects.all())
    print('Partes', Parte.objects.all())
    print('PropiedadesPartes', PropiedadParte.objects.all())
    print('Equipos', Equipo.objects.all())
    print('PropiedadesEquipos', PropiedadEquipo.objects.all())


if __name__ == '__main__':
    create_data()