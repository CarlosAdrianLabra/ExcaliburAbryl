from django import forms

# Import model
from .models import Productos

# Create your forms here.
class NProductos(forms.ModelForm):

    class Meta:
        model = Productos
        fields = ('__all__')
