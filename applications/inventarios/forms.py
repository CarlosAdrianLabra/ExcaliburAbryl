from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import Productos

# Formulario calzado
class CalzadoFormulario(BSModalModelForm):

    class Meta:
        model = Productos
        exclude = ['num_venta', 'talla', 'anular']

        widgets = {
            'barcode': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': 'TENIS ADVANTAGE, TENIS STAN SMITH'
                }
            ),
            'marca': forms.Select(attrs={'class': 'form-control mb-3'}),
            'medida': forms.Select(attrs={'class': 'form-control mb-3'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'almacen': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'value': '10', # 10 = ALMACEN 1
                }
            ),
            'tipo': forms.TextInput(
                attrs={
                    'class': 'form-control mb-4',
                    'value': '10', # 10 = CALZADO
                }
            ),
            'proveedor': forms.Select(attrs={'class': 'form-control mb-3',}),
            'linea': forms.Select(attrs={'class': 'form-control mb-3',}),
            'color': forms.Select(attrs={'class': 'form-control mb-3',}),
            'modelo': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': '3 DIGITOS'
                }
            ),
        }

# Formulario Ropa
class RopaFormulario(BSModalModelForm):

    class Meta:
        model = Productos
        exclude = ['num_venta', 'medida', 'anular']

        widgets = {
            'barcode': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'PLAYERA, PANTALON ESCOLAR'
                }
            ),
            'marca': forms.Select(attrs={'class': 'form-control mb-3'}),
            'talla': forms.Select(attrs={'class': 'form-control mb-3'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'almacen': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'value': '10', # 10 = ALMACEN 1
                }
            ),
            'tipo': forms.TextInput(
                attrs={
                    'class': 'form-control mb-4',
                    'value': '20', # 20 = ROPA
                }
            ),
            'proveedor': forms.Select(attrs={'class': 'form-control mb-3',}),
            'linea': forms.Select(attrs={'class': 'form-control mb-3',}),
            'color': forms.Select(attrs={'class': 'form-control mb-3',}),
            'modelo': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': '3 DIGITOS'
                }
            ),
        }