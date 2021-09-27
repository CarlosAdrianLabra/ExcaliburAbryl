from applications.apartados.models import Apartados
from django import forms

class ApartadosForm(forms.Form):
    monto_pagado = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control text-right col',
                'placeholder': '100.00'
            }
        )
    )

class ApartadosUpdateForm(forms.ModelForm):

    class Meta:
        model = Apartados
        fields = ('__all__')

        widgets = {
            'barcode': forms.TextInput(attrs={'class': 'form-control col-9 ml-1 mb-3 float-left text-right'}),
            'monto_pagado': forms.TextInput(attrs={'class': 'form-control col-9 ml-1 mb-3 float-left text-right'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control col-9 ml-1 mb-3 float-left text-right'}),
            'precio_producto': forms.TextInput(attrs={'class': 'form-control col-9 ml-1 mb-3 float-left text-right'}),
        }    

    monto_actualizar = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-9 ml-1 mb-3 mt-4 float-left text-right',
                'placeholder': '100.00'
            }
        )
    )