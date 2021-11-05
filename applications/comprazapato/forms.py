from django import forms
from .models import Pedidos

class pedidosForm(forms.Form):

    monto = forms.DecimalField(
        required=False,
       
    )

    fecha_inicio = forms.DateTimeField(
        required=False,
        
    )

    fecha_final = forms.DateTimeField(
        required=False,
        
    )
