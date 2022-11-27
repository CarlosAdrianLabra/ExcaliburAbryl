from django import forms

class EfectivoFormTezoncoCaja2(forms.Form):
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