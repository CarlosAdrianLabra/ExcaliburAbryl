from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

# Create your views here.

class PaginaInicio(TemplateView):
    template_name = 'inicio.html'
    
