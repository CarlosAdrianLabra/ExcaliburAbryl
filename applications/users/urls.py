from django.urls import path
from .views import *
from . import views

app_name = "users_app"

urlpatterns = [
    path('create_user/', UserRegisterView.as_view(), name='user-create'),
    path('login/', LoginUser.as_view(), name='user-login'),
    path('update/', UpdatePasswordView.as_view(), name='user-update'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('user_update/<pk>/', UserUpdateView.as_view(), name='user-data-update'),
    path(
        'users/lista/', 
        views.UserListView.as_view(),
        name='user-lista',
    ),
]