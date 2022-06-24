from unicodedata import name
from django.urls import path
from .views import *
from . import views

app_name = "users_app"

urlpatterns = [
    path('', LoginUser.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('invocador_del_llano/', UserRegisterView.as_view(), name='user-create'),
    # Urls Administración
    path('usuarios/', views.UserListView.as_view(), name='user-lista',),
    path('usuarios/actualizar/<pk>/', UserUpdateView.as_view(), name='user-data-update'),
    # Urls Perfil del sistema
    path('usuarios/perfil/', PerfilView.as_view(), name='perfil'),
    path('usuarios/contraseña/', UpdatePasswordView.as_view(), name='user-update'),
    #
    path('redireccionando/', PaginaRedireccionar.as_view(), name='redireccionar'),
]