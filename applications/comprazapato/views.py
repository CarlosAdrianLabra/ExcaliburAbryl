from django.shortcuts import render
from django.views.generic import TemplateView, FormView, ListView, CreateView,UpdateView

from applications.comprazapato.forms import pedidosForm
from applications.comprazapato.models import Pedidos
from django.urls import reverse_lazy, reverse
# Create your views here.





class baseCompraZapato(CreateView):
    template_name = "comprazapato/index_comprazapato.html"
    form_class = pedidosForm
    success_url = reverse_lazy('comprazapato_app:comprazapato_lista_pedidos')


class listaPedidos(ListView):
    template_name = 'comprazapato/lista_pedidos.html'
    model = Pedidos
    context_object_name = "lista_pedidos"

class compraZapatoUpdateView(UpdateView):
    model = Pedidos
    form_class = pedidosForm
    template_name = "comprazapato/update_comprazapato.html"
    success_url=reverse_lazy('comprazapato_app:comprazapato_lista_pedidos')