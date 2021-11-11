from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Pedidos




class pedidosForm(forms.ModelForm):

    class Meta:
        model = Pedidos
        fields = (
             '__all__'
        )
        
        widgets = {
            'monto_por_pagar': forms.NumberInput(attrs={
                'class': 'form-control mb-3'
                
            }),
            'fecha_inicio': forms.TextInput(attrs={
                    'class': 'form-control mb-3',
                    'type': 'date'
            }),
            'fecha_termino': forms.TextInput(attrs={
                    'class': 'form-control mb-3',
                    'type': 'date'
            }),
            'estado_compra':forms.Select(attrs={
                'class': 'form-control mb-3',
                
            }),
            'codigo_factura':forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'type': 'text'
            }),
            'proveedor':forms.TextInput(attrs={
                'class': 'form-control mb-3'
                
            }),
            'comentario':forms.Textarea(attrs={
                'class': 'form-control mb-3',
                
            }),

        }

    
