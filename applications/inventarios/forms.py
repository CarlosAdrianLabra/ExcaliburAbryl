from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import Productos

# Formulario calzado
class CalzadoFormulario(BSModalModelForm):

    class Meta:
        model = Productos
        exclude = ['num_venta', 'talla', 'pieza', 'anular', 'linea_r', 'linea_a']

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
                    'value': '1000', # 1000 = ALMACEN 1
                }
            ),
            'tipo': forms.TextInput(
                attrs={
                    'class': 'form-control mb-4',
                    'value': '100', # 100 = CALZADO
                }
            ),
            'proveedor': forms.Select(attrs={'class': 'form-control mb-3',}),
            'linea_c': forms.Select(attrs={'class': 'form-control mb-3',}),
            'color': forms.Select(attrs={'class': 'form-control mb-3',}),
            'modelo': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': '15 DIGITOS'
                }
            ),
            'genero': forms.Select(attrs={'class': 'form-control mb-3',}),
            'promocion': forms.Select(attrs={'class': 'form-control mb-3',}),
            'barcode_exterior': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': '15 DIGITOS'
                }
            ),
        }

# Formulario Ropa
class RopaFormulario(BSModalModelForm):

    class Meta:
        model = Productos
        exclude = ['num_venta', 'medida', 'pieza', 'anular', 'linea_c', 'linea_a']

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
                    'value': '1000', # 1000 = ALMACEN 1
                }
            ),
            'tipo': forms.TextInput(
                attrs={
                    'class': 'form-control mb-4',
                    'value': '200', # 200 = ROPA
                }
            ),
            'proveedor': forms.Select(attrs={'class': 'form-control mb-3',}),
            'linea_r': forms.Select(attrs={'class': 'form-control mb-3',}),
            'color': forms.Select(attrs={'class': 'form-control mb-3',}),
            'modelo': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': '15 DIGITOS'
                }
            ),
            'genero': forms.Select(attrs={'class': 'form-control mb-3',}),
            'promocion': forms.Select(attrs={'class': 'form-control mb-3',}),
            'barcode_exterior': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': '15 DIGITOS'
                }
            ),
        }

# Formulario Accesorios
class AccesoriosFormulario(BSModalModelForm):

    class Meta:
        model = Productos
        exclude = ['num_venta', 'medida', 'talla', 'anular', 'linea_c', 'linea_r']

        widgets = {
            'barcode': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'MOCHILA, ARTÍCULO DE LIMPIEZA'
                }
            ),
            'marca': forms.Select(attrs={'class': 'form-control mb-3'}),
            'pieza': forms.Select(attrs={'class': 'form-control mb-3'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'almacen': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'value': '1000', # 1000 = ALMACEN 1
                }
            ),
            'tipo': forms.TextInput(
                attrs={
                    'class': 'form-control mb-4',
                    'value': '300', # 300 = ACCESORIOS
                }
            ),
            'proveedor': forms.Select(attrs={'class': 'form-control mb-3',}),
            'linea_a': forms.Select(attrs={'class': 'form-control mb-3',}),
            'color': forms.Select(attrs={'class': 'form-control mb-3',}),
            'modelo': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': '15 DIGITOS'
                }
            ),
            'genero': forms.Select(attrs={'class': 'form-control mb-3',}),
            'promocion': forms.Select(attrs={'class': 'form-control mb-3',}),
            'barcode_exterior': forms.TextInput(
                attrs={
                    'class': 'form-control mb-3',
                    'placeholder': '15 DIGITOS'
                }
            ),
        }