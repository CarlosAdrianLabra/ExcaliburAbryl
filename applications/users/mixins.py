from django.views.generic import View
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .models import User

def check_user_role(role, user_role):

    if (role==User.ADMINISTRADOR or role==user_role):
        return True
    else:
        return False

class AlmacenPermisionMixin(LoginRequiredMixin):
    login_url=reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_user_role(request.user.role, User.ALMACEN):
            return HttpResponseRedirect(reverse('users_app:user-login'))

        return super().dispatch(request,*args,**kwargs)

class VentasPermisoMixin(LoginRequiredMixin):
    login_url=reverse_lazy('users_app:user-login')
    
    def dispatch(self, request, *args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_user_role(request.user.role, User.VENTAS):
            return HttpResponseRedirect(reverse('users_app:user-login'))

        return super().dispatch(request,*args,**kwargs)

class AdminPermisoMixin(LoginRequiredMixin):
    login_url=reverse_lazy('users_app:user-login')
    
    def dispatch(self, request, *args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_user_role(request.user.role, User.ADMINISTRADOR):
            return HttpResponseRedirect(reverse('users_app:user-login'))

        return super().dispatch(request,*args,**kwargs)
