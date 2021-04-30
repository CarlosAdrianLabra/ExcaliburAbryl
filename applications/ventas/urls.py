from django.urls import path
from . import views

app_name = "ventas_app"

urlpatterns = [
    path(
        'Base-ventas/',
        views.VentasView.as_view(),
        name='inicioventas',
        )
]