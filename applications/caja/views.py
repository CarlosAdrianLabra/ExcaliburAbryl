from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    TemplateView,
    UpdateView,
    DeleteView,
    )
# Create your views here.
class CajaView(TemplateView):
    template_name = "caja/base_caja.html"