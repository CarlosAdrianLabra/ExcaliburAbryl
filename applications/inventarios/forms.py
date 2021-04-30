from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import (
    Productos,
    Marca
)

""" **************************************** REGISTROS **************************************** """

# Formulario registros
class MarcaFormulario(BSModalModelForm):

    class Meta:
        model = Marca
        fields = ('__all__')

        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control mb-3'}
            ),
        }

""" **************************************** ALMACEN 1 **************************************** """

# Formulario calzado
class CalzadoFormulario(BSModalModelForm):

    class Meta:
        model = Productos
        fields = ['barcode','nombre', 'marca', 'medida', 'stock', 'precio_venta', 'precio_compra', 'almacen', 'tipo', 'proveedor', 'img',]
        exclude = ['timestamp']

        widgets = {
            'barcode': forms.NumberInput(
                attrs={'class': 'form-control mb-3'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control mb-3'}
            ),
            'marca': forms.Select(
                attrs={'class': 'form-control mb-3'}
            ),
            'medida': forms.Select(
                attrs={'class': 'form-control mb-3'}
            ),
            'stock': forms.NumberInput(
                attrs={'class': 'form-control mb-3'}
            ),
            'precio_venta': forms.NumberInput(
                attrs={'class': 'form-control mb-3'}
            ),
            'precio_compra': forms.NumberInput(
                attrs={'class': 'form-control mb-3'}
            ),
            'almacen': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'value': '0', # 0 = ALMACEN 1
                }
            ),
            'tipo': forms.TextInput(
                attrs={
                    'class': 'form-control mb-4',
                    'value': '0', # 0 = CALZADO
                }
            ),
            'proveedor': forms.Select(
                attrs={'class': 'form-control mb-3',}
            ),
        }

# Formulario Ropa
class RopaFormulario(BSModalModelForm):

    class Meta:
        model = Productos
        fields = ['barcode','nombre', 'marca', 'talla', 'stock', 'precio_venta', 'precio_compra', 'almacen', 'tipo', 'proveedor', 'img',]
        exclude = ['timestamp']

        widgets = {
            'barcode': forms.NumberInput(
                attrs={'class': 'form-control mb-3'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'form-control mb-3'}
            ),
            'marca': forms.Select(
                attrs={'class': 'form-control mb-3'}
            ),
            'talla': forms.Select(
                attrs={'class': 'form-control mb-3'}
            ),
            'stock': forms.NumberInput(
                attrs={'class': 'form-control mb-3'}
            ),
            'precio_venta': forms.NumberInput(
                attrs={'class': 'form-control mb-3'}
            ),
            'precio_compra': forms.NumberInput(
                attrs={'class': 'form-control mb-3'}
            ),
            'almacen': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'value': '0', # 0 = ALMACEN 1
                }
            ),
            'tipo': forms.TextInput(
                attrs={
                    'class': 'form-control mb-4',
                    'value': '1', # 1 = ROPA
                }
            ),
            'proveedor': forms.Select(
                attrs={'class': 'form-control mb-3',}
            ),
        }