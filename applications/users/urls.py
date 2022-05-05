from django.urls import path
from .views import *
from . import views

app_name = "users_app"

urlpatterns = [
    path('', LoginUser.as_view(), name='user-login'),
    path('create_user/', UserRegisterView.as_view(), name='user-create'),
    path('usuarios/contraseña/', UpdatePasswordView.as_view(), name='user-update'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('user_update/<pk>/', UserUpdateView.as_view(), name='user-data-update'),
    path('usuarios/perfil/', PerfilView.as_view(), name='perfil'),
    path(
        'usuarios/', 
        views.UserListView.as_view(),
        name='user-lista',
    ),
]