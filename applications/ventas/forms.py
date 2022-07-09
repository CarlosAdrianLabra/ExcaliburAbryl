from django import forms
from applications.inventarios.models import Marca
from .models import Venta
from applications.inventarios.models import Productos, Sublinea

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
    
    def clean_barcode(self):
        barcode = self.cleaned_data['barcode']
        
        if Productos.objects.filter(barcode = barcode):
            return barcode
        else:
            raise forms.ValidationError('Error XD')
            
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

class EfectivoForm(forms.Form):
    cash = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-12 text-right',
                'value': '0'
            }
        )
    )
    change = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-12 text-right',
                'style': 'display:None;',
                'value': '0'
            }
        )
    )

class PromocionesForm(forms.Form):
    genero = forms.ChoiceField(
        required=False,
        choices=Productos.OPCIONES_GENERO,
        widget=forms.Select(
            attrs = {
                'class': 'form-control col-9 ml-1 mb-3 float-left',
            }
        )
    )
    sublinea = forms.ModelChoiceField(
        required=False,
        queryset=Sublinea.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control col-9 ml-1 mb-3 float-left',
            }
        )
    )
    marca = forms.ModelChoiceField(
        required=False,
        queryset=Marca.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control col-9 ml-1 mb-3 float-left',
            }
        )
    )
    modelo = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-9 ml-1 mb-3 float-left',
            }
        )
    )
    precio_asignado = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-9 ml-1 mb-3 float-left text-right',
                'placeholder': '99.00'
            }
        )
    )
    barcode = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-9 ml-1 mb-3 float-left text-right',
                'placeholder': 'Ingresar código de barras del producto'
            }
        )
    )
    barcode_solo = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control col-9 ml-1 mb-3 float-left text-right',
                'placeholder': 'Ingresar código de barras del producto'
            }
        )
    )
    promocion = forms.ChoiceField(
        required=True,
        choices=Productos.OPCION_PROMOCIONES,
        widget=forms.Select(
            attrs = {
                'class': 'form-control col-12 ml-1 mb-3',
            }
        )
    )
    fecha_final_promocion = forms.DateField(
        required=True,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control col-12 ml-1 mb-3',
                
            },
        )
    )