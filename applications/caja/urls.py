from django.urls import path
from . import views

app_name = "caja_app"

urlpatterns = [
    path('Base-caja/',views.CajaView.as_view(),name='iniciocaja',)
]