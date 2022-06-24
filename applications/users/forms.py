from django import forms
from django.contrib.auth import authenticate

from bootstrap_modal_forms.forms import BSModalModelForm
from .models import User

class UserRegisterForm(forms.ModelForm):

    password1=forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña',
                'class': 'form-control',
            }
        )
    )

    password2=forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repetir Contraseña',
                'class': 'form-control',
            }
        )
    )
    
    class Meta:
        model = User
        fields = ('username','email','nombres','apellidos','role')
        widgets={
            'username':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre para iniciar sesión'
                }
            ),
            'email':forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email'
                }
            ),
            'nombres':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nombre(s)'
                }
            ),
            'apellidos':forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Apellidos'
                }
            ),
            'role':forms.Select(
                attrs={
                    'class': 'form-control',
                }
            )
        }






    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2','Las contraseñas no son iguales')

class LoginForm(forms.Form):
    username=forms.CharField(
        label='username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Usuario',
                'class': 'form-control'
            }
        )
    )
    password=forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña',
                'class': 'form-control'
            }
        )
    )

    def clean(self):
        cleaned_data=super(LoginForm,self).clean()
        username= self.cleaned_data['username']
        password=self.cleaned_data['password']

        if not authenticate(username=username,password=password):
            raise forms.ValidationError('datos de usuario incorrectos')

        return self.cleaned_data

class UpdatePasswordForm(forms.Form):
    password1=forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                #'placeholder':'Contraseña actual'
            }
        )
    )

    password2=forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                #'placeholder':'Contraseña nueva'
            }
        )
    )