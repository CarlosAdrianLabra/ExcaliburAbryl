from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from .models import Productos

# Formulario de productos
class ProductosFormulario(BSModalModelForm):

    class Meta:
        model = Productos
        fields = ['nombreP', 'marcaP', 'modeloP', 'cantidadP', 'precioP', 'imagenP']
        exclude = ['timestamp']

        widgets = {
            'nombreP': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre',
                    'class': 'form-control mb-3'
                }
            ),
            'marcaP': forms.TextInput(
                attrs={
                    'placeholder': 'Marca',
                    'class': 'form-control mb-3'
                }
            ),
            'modeloP': forms.TextInput(
                attrs={
                    'placeholder': 'Modelo',
                    'class': 'form-control mb-3'
                }
            ),
            'cantidadP': forms.NumberInput(
                attrs={
                    'placeholder': 'Stock',
                    'class': 'form-control mb-3'
                }
            ),
            'precioP': forms.NumberInput(
                attrs={
                    'placeholder': 'Precio',
                    'class': 'form-control mb-4'
                }
            ),

        }