"""ExcaliburAbryl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

# Import views
from . import views

name_app = 'abryl'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel_de_control/', views.PanelControlInicio.as_view(), name='panel_de_control'),

    #URLS - APPLICATIONS.INVENTARIOS
    re_path('', include('applications.inventarios.urls')),
    #URLS - APPLICATIONS.VENTAS
    re_path('', include('applications.ventas.urls')),
    #URLS - APPLICATIONS.CAJA
    re_path('', include('applications.caja.urls')),
    #URLS - APPLICATIONS.CODIGOBARRAS
    re_path('', include('applications.codigobarras.urls')),
    #URLS - APPLICATIONS.USERS
    re_path('', include('applications.users.urls')),
    #URLS - APPLICATIONS.ADMINISTRACIÓN
    re_path('', include('applications.administracion.urls')),
    #URLS - APPLICATIONS.APARTADOS
    re_path('', include('applications.apartados.urls')),
    #URLS - APPLICATIONS.COMPRAZAPATO
    re_path('', include('applications.comprazapato.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
