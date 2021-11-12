from django import forms
from applications.inventarios.models import Proveedor
from .models import Gastos
from applications.comprazapato.models import Pedidos


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


class GastosFormulario(forms.ModelForm):

    class Meta:
        model = Gastos
        fields = [
            'mes','año','fecha','cargosBancarios','comisionTarjetaCredito','otrosBancos',
            'salariosSueldosWeb','sueldosOficina','sueldosCorporativos','comisionesPagadas','jubilacion','utilidades','costosReclutamiento','imss',
            'rollosImpresora','tapiceria','remodelacionOficina','predial','papeleria','intercomunicador','telefonosOficina','luz','telefono','lentes','fletes',
            'walmart','reparacionesManteminiento','notas','agua','policia','gastosViajes','amplificadorBocinas','gastosCheques','gastosOficina','fideicomiso',
            'contador','cometra','paletas','finiquito','honorariosConsultores','impuestoCDMX','chequesAbril','equipoComputo','mantenimientoComputo',
            'viaticos','comidas','valoracionInmuebles','imprenta','comisionRentaLocal','impuestos',
        ]


class CompravsVendeFormulario(forms.Form):
    proveedor = forms.ModelChoiceField(
        required=True,
        queryset=Proveedor.objects.all(),
        widget=forms.Select(
            attrs = {
                'class': 'form-control',
            }
        )
    )
    fecha_inicio = forms.DateField(
        required=True,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control pull-right',
            },
        )
    )
    fecha_fin = forms.DateField(
        required=True,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control pull-right',
            },
        )
    )

class pedidosadminForm(forms.ModelForm):

    class Meta:
        model = Pedidos
        fields = (
             '__all__'
        )
        
        widgets = {
            'monto_por_pagar': forms.NumberInput(attrs={
                'class': 'form-control mb-3',
                'readonly':'readonly',
                
            }),
            'fecha_inicio': forms.TextInput(attrs={
                    'class': 'form-control mb-3',
                    'type': 'date',
                    'readonly':'readonly',
            }),
            'fecha_termino': forms.TextInput(attrs={
                    'class': 'form-control mb-3',
                    'type': 'date',
                    'readonly':'readonly',
            }),
            'estado_compra':forms.Select(attrs={
                'class': 'form-control mb-3',
                'readonly':'readonly',
                
            }),
            'codigo_factura':forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'type': 'text',
                'readonly':'readonly',
            }),
            'proveedor':forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'readonly':'readonly',
                
            }),
            'comentario':forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'readonly':'readonly',
                
            }),

        }