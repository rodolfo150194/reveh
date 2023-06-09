from django import forms
from django.forms import Textarea

from dashboards.models import *

class OrganismoModelForm(forms.ModelForm):

    class Meta:
        model = Organismo
        fields = '__all__'
        widgets = {
            'fecha_registro' : forms.HiddenInput()
        }

class OsdeModelForm(forms.ModelForm):
    class Meta:
        model = Osde
        fields = '__all__'
        # widgets = {
        #     'nombre' : forms.TextInput(attrs={'class':'form-control-solid'})
        # }

class EmpresaModelForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'
        # widgets = {
        #     'nombre' : forms.TextInput(attrs={'class':'form-control-solid'})
        # }

class MarcaModelForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = '__all__'
        # widgets = {
        #     'nombre' : forms.TextInput(attrs={'class':'form-control-solid'})
        # }


class ModeloModelForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields = ['nombre']

        # widgets = {
        #     'marca': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple', 'id':'marcas'}),
        # }


class MarcaModeloModelForm(forms.ModelForm):
    class Meta:
        model = MarcaModelo
        fields = ['marca','modelo']


        widgets = {
            'marca': forms.Select(attrs={'class': 'select2'}),
            'modelo': forms.Select(attrs={'class': 'select2'}),
        }



class PropiedadModelForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = ['nombre']


class CategoriaInsumoModelForm(forms.ModelForm):
    class Meta:
        model = CategoriaInsumo
        fields = '__all__'

        widgets = {
            'propiedad': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'}),
        }

class CategoriaPiezaModelForm(forms.ModelForm):
    class Meta:
        model = CategoriaPieza
        fields = '__all__'

        widgets = {
            'propiedad': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'}),
        }


class CategoriaParteModelForm(forms.ModelForm):
    class Meta:
        model = CategoriaParte
        fields = '__all__'

        widgets = {
            'propiedad': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'}),
        }


class CategoriaEquipoModelForm(forms.ModelForm):
    class Meta:
        model = CategoriaEquipo
        fields = '__all__'

        widgets = {
            'propiedad': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'}),
        }


class InsumoModelForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = '__all__'

        widgets = {
            'categoria': forms.Select(attrs={'class': 'select2 ', 'required': 'required'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': Textarea(
                attrs={
                    'class': 'form-control', 'rows': 3, 'cols': 2
                }
            ),
            # 'marca': SelectWithPop,
            'marca': forms.Select(attrs={'class': 'select2 ', 'required': 'required'}),
            'modelo': forms.Select(attrs={'class': 'select2 ', 'required': 'required'}),

            'propiedades': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'})
            # 'modelo': forms.Select(attrs={'class': 'select2 '})
        }


class PropiedadInsumoModelForm(forms.ModelForm):
    class Meta:
        model = PropiedadInsumo
        fields = '__all__'

        widgets = {
            'insumo': forms.HiddenInput(attrs={'class': 'form-control d-none'}),
            'propiedad': forms.HiddenInput(attrs={'class': 'form-control', }),
            'valor': forms.TextInput(attrs={'class': 'form-control valor'}),
        }


class PiezaModelForm(forms.ModelForm):
    class Meta:
        model = Pieza
        fields = '__all__'

        widgets = {
            'categoria': forms.Select(attrs={'class': 'select2 ', 'required': 'required'}),
            'insumo': forms.SelectMultiple(attrs={'class': 'select2 ', 'multiple': 'multiple'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': Textarea(
                attrs={
                    'class': 'form-control', 'rows': 3, 'cols': 2
                }
            ),
            # 'marca': SelectWithPop,
            'modelo': forms.Select(attrs={'class': 'select2 ', 'required': 'required'}),
            'marca': forms.Select(attrs={'class': 'select2 ', 'required': 'required'}),
            'propiedades': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'})
            # 'modelo': forms.Select(attrs={'class': 'select2 '})
        }


class PropiedadPiezaModelForm(forms.ModelForm):
    class Meta:
        model = PropiedadPieza
        fields = '__all__'

        widgets = {
            'pieza': forms.HiddenInput(attrs={'class': 'form-control d-none'}),
            'propiedad': forms.HiddenInput(attrs={'class': 'form-control', }),
            'valor': forms.TextInput(attrs={'class': 'form-control valor'}),
        }


class ParteModelForm(forms.ModelForm):
    class Meta:
        model = Parte
        fields = '__all__'

        widgets = {
            'categoria': forms.Select(attrs={'class': 'select2 ', 'required': 'required'}),
            'insumo': forms.SelectMultiple(attrs={'class': 'select2 ', 'multiple': 'multiple'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': Textarea(
                attrs={
                    'class': 'form-control', 'rows': 3, 'cols': 2
                }
            ),
            'marca': forms.Select(attrs={'class': 'select2 ', 'required': 'required'}),
            'modelo': forms.Select(attrs={'class': 'select2 ', 'required': 'required'}),
            'piezas': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'}),
            'propiedades': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'})
            # 'piezas': SelectMultipleWithPop
        }


class PropiedadParteModelForm(forms.ModelForm):
    class Meta:
        model = PropiedadParte
        fields = '__all__'

        widgets = {
            'parte': forms.HiddenInput(attrs={'class': 'form-control d-none'}),
            'propiedad': forms.HiddenInput(attrs={'class': 'form-control', }),
            'valor': forms.TextInput(attrs={'class': 'form-control valor'}),
        }


class EquipoModelForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = '__all__'

        widgets = {
            'categoria': forms.Select(attrs={'class': 'select2 ', 'required': 'required'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': Textarea(
                attrs={
                    'class': 'form-control', 'rows': 3, 'cols': 2
                }
            ),
            'marca': forms.Select(attrs={'class': 'select2 ', 'required': 'required'}),
            'modelo': forms.Select(attrs={'class': 'select2 ', 'required': 'required'}),
            'partes': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'}),
            'propiedades': forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'})
            # 'partes': SelectMultipleWithPop
        }


class PropiedadEquipoModelForm(forms.ModelForm):
    class Meta:
        model = PropiedadEquipo
        fields = '__all__'

        widgets = {
            'equipo': forms.HiddenInput(attrs={'class': 'form-control d-none'}),
            'propiedad': forms.HiddenInput(attrs={'class': 'form-control'}),
            'valor': forms.TextInput(attrs={'class': 'form-control valor'}),
        }
