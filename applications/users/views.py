from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, View, UpdateView, ListView
from django.views.generic.edit import FormView
from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm
from django.urls import reverse_lazy,reverse
from .models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class UserRegisterView(FormView):
    template_name = 'users/createUser.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):

        User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            role=form.cleaned_data['role']
        )

        return super(UserRegisterView,self).form_valid(form)

class LoginUser(FormView):
    """LoginUser definition."""
    template_name = 'users/login.html'
    form_class=LoginForm
    success_url='/panel_de_control'

    def form_valid(self, form):
        user=authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser,self).form_valid(form)

class LogoutView(View):

    def get(self,request,*args,**kargs):
        logout(request)
        return HttpResponseRedirect(
            reverse('users_app:user-login')
        )

class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name='users/update.html'
    form_class=UpdatePasswordForm
    success_url=reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self,form):
        usuario = self.request.user
        user= authenticate(
            username=usuario.username,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
        
        logout(self.request)

        return super(UpdatePasswordView, self).form_valid(form)

class UserUpdateView(UpdateView):
    model = User
    template_name = "users/updateuser.html"
    fields = ['username','email','nombres','apellidos','role','is_staff','is_active']
    success_url='/'

class UserListView(ListView):
    template_name = "users/lista.html"
    context_object_name = 'usuarios'

    def get_queryset(self):
        return User.objects.usuarios_sistema()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["usuarios"] = User.objects.usuarios_sistema()
    #     return context

class PerfilView(ListView):
    template_name = "users/perfil.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.all()
        return context