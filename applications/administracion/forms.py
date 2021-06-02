from django import forms

from applications.inventarios.models import Proveedor


class LiquidacionProviderForm(forms.Form):

    proveedor = forms.ModelChoiceField(
        required=True,
        queryset=Proveedor.objects.all(),
        widget=forms.Select(
            attrs = {
                'class': 'form-control',
            }
        )
    )
    date_start = forms.DateField(
        required=True,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control pull-right',
                
            },
        )
    )
    date_end = forms.DateField(
        required=True,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control pull-right',
            },
        )
    )


class ResumenVentasForm(forms.Form):
    
    date_start = forms.DateField(
        required=True,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control pull-right',
            },
        )
    )
    date_end = forms.DateField(
        required=True,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control pull-right',
            },
        )
    )
