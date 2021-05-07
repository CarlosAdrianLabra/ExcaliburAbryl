from django import forms
from .models import Venta

class VentaForm(forms.Form):
    barcode= forms.CharField(
        required = True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Código de barras',
                'class': 'form-control col-4',
            }
        )
    )
    count = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs= {
                'value': '1',
                'class': 'form-control text-center col-2',
            }
        )
    )

    def clean_count(self):
        count = self.cleaned_data['count']
        if count < 1:
            raise forms.ValidationError('Ingrese una cantidad mayor a cero')
        
        return count


class VentaVoucherForm(forms.Form):

    type_payment = forms.ChoiceField(
        required=False,
        choices=Venta.TIPO_PAYMENT_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'form-control',
            }
        )
    )
    type_invoice = forms.ChoiceField(
        required=False,
        choices=Venta.TIPO_INVOICE_CHOICES,
        widget=forms.Select(
            attrs = {
                'class': 'form-control',
            }
        )
    )