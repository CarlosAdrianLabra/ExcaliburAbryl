from applications.inventarios.models import Productos
from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    View,
)
from applications.inventarios.models import Productos
from applications.utils import render_to_pdf
from django.http import JsonResponse, HttpResponse

# Create your views here.


class codigobarrasview(ListView):
    template_name = "codigobarras/Tabla_barras.html"
    paginate_by = '10'
    context_object_name = 'Barras'
    model= Productos

    def get_queryset(self):

        queryset = Productos.objects.filtros_barras(
            filtro = self.request.GET.get("filtro", ''),
        )
        return queryset

class BarrasPDF(View):

    def get(self, request, *args, **kwargs):
        productos = Productos.objects.get(barcode=self.kwargs['pk'])
        data = {
            'productos': productos
        }
        pdf = render_to_pdf('codigobarras/codigobarraspdf.html', data)

        return HttpResponse(pdf, content_type='application/pdf')