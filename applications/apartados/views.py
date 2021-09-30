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
from applications.inventarios.models import Productos
from applications.users.models import User
from applications.ventas.models import Carrito, Venta
from .forms import ApartadosForm, ApartadosUpdateForm
from .models import Apartados
from .functions import pre_apartado, procesar_venta_apartado

# Create your views here.
class CrearApartado(FormView):
    template_name = 'apartados/index.html'
    form_class = ApartadosForm
    success_url = reverse_lazy('ventas_app:venta-index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos_pos'] = Carrito.objects.all()
        context['total_cobrar'] = Carrito.objects.total_cobrar()

        return context
    
    def form_valid(self, form):
        monto_pagado = form.cleaned_data['monto_pagado']
        
        apartado = pre_apartado(
            self=self,
            monto_pagado=monto_pagado
        )

        if apartado: 
            return HttpResponseRedirect(reverse('apartados_app:apartados_lista'))

        else:
            return HttpResponseRedirect(reverse('ventas_app:venta-index'))

class ApartadosLista(ListView):
    template_name = 'apartados/apartados_lista.html'
    model = Apartados
    context_object_name = "apartados_lista"
    

class ApartadosUpdateView(UpdateView):
    template_name = "apartados/apartados_update.html"
    form_class = ApartadosUpdateForm
    model = Apartados
    success_url=reverse_lazy('apartados_app:apartados_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apartados'] = Apartados.objects.get(id=self.kwargs['pk'])

        return context

    def form_valid(self, form):
        monto_actualizar = form.cleaned_data['monto_actualizar']

        apartados = form.save(commit=False)
        apartados.monto_pagado = float(apartados.monto_pagado) + float(monto_actualizar)
        apartados.save()

        return super(ApartadosUpdateView, self).form_valid(form)


class ApartadosProcesarVenta(View):

    def post(self, request, *args, **kwargs):
        
        procesar_venta_apartado(
            self=self,
            type_invoice=Venta.APARTADO,
            type_payment=Venta.EFECTIVO,
            user=self.request.user
        )
        
        return HttpResponseRedirect(
            reverse(
                'apartados_app:apartados_lista'
            )
        )