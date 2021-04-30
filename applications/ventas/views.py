from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    View,
    UpdateView,
    DeleteView,
    ListView,
    TemplateView,
)
from django.views.generic.edit import (
    FormView
)
#applicaciones locales
from applications.inventarios.models import Productos
from .models import Venta, DetalleVenta, Carrito
#from .forms import VentaForm, VentaVoucherForm
#from .functions import procesar_venta
# Create your views here.



class VentasView(TemplateView):
    template_name = "ventas/base_ventas.html"
