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

class AdminPermisoMixin(LoginRequiredMixin):
    login_url=reverse_lazy('users_app:user-login')
    
    def dispatch(self, request, *args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_user_role(request.user.role, User.ADMINISTRADOR):
            pagina_anterior = request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
            return HttpResponseRedirect(reverse('users_app:redireccionar'), {"pagina":pagina_anterior})

        return super().dispatch(request,*args,**kwargs)

class InventarioPermisionMixin(LoginRequiredMixin):
    login_url=reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_user_role(request.user.role, User.INVENTARIO):
            pagina_anterior = request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
            return HttpResponseRedirect(reverse('users_app:redireccionar'), {"pagina":pagina_anterior})

        return super().dispatch(request,*args,**kwargs)

class PuntodeventaPermisoMixin(LoginRequiredMixin):
    login_url=reverse_lazy('users_app:user-login')
    
    def dispatch(self, request, *args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_user_role(request.user.role, User.PUNTODEVENTA):
            pagina_anterior = request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
            return HttpResponseRedirect(reverse('users_app:redireccionar'), {"pagina":pagina_anterior})

        return super().dispatch(request,*args,**kwargs)

class CodigodebarrasPermisoMixin(LoginRequiredMixin):
    login_url=reverse_lazy('users_app:user-login')
    
    def dispatch(self, request, *args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_user_role(request.user.role, User.CODIGODEBARRAS):
            pagina_anterior = request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
            return HttpResponseRedirect(reverse('users_app:redireccionar'), {"pagina":pagina_anterior})

        return super().dispatch(request,*args,**kwargs)

class PromocionesPermisoMixin(LoginRequiredMixin):
    login_url=reverse_lazy('users_app:user-login')
    
    def dispatch(self, request, *args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_user_role(request.user.role, User.PROMOCIONES):
            pagina_anterior = request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
            return HttpResponseRedirect(reverse('users_app:redireccionar'), {"pagina":pagina_anterior})

        return super().dispatch(request,*args,**kwargs)

class CompradezapatoPermisoMixin(LoginRequiredMixin):
    login_url=reverse_lazy('users_app:user-login')
    
    def dispatch(self, request, *args,**kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_user_role(request.user.role, User.COMPRADEZAPATO):
            pagina_anterior = request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')
            return HttpResponseRedirect(reverse('users_app:redireccionar'), {"pagina":pagina_anterior})

        return super().dispatch(request,*args,**kwargs)
