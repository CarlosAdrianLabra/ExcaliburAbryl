from django.contrib import admin
from django.urls import path

# Import views
from . import views

app_name = "inventarios_app"

urlpatterns = [
    path('registrar-nuevo-producto/', views.NuevoProducto.as_view(), name='rnp'),
]