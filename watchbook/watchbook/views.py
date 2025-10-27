# watchbook/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from usuarios.forms import FormularioLogin
from usuarios.models import RegistroAssistido
from amizade.models import Amizade 

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('inicio') 
        
        form = FormularioLogin()
        return render(request, 'usuarios/login.html', {'form': form})

    def post(self, request):
        form = FormularioLogin(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('inicio')

       
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'usuarios/login.html', {'form': form})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class Inicio(LoginRequiredMixin, TemplateView):
    template_name = 'inicio.html'
    login_url = '/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['total_obras'] = RegistroAssistido.objects.filter(usuario=user).count()
        
        # Atividades recentes dos amigos
        amizades = Amizade.objects.filter(
            Q(de_usuario=user, status='ACEITO') | 
            Q(para_usuario=user, status='ACEITO')
        )
        
        amigos_ids = []
        for amizade in amizades:
            if amizade.de_usuario == user:
                amigos_ids.append(amizade.para_usuario.id)
            else:
                amigos_ids.append(amizade.de_usuario.id)
        
        context['atividades_amigos'] = RegistroAssistido.objects.filter(
            usuario__id__in=amigos_ids
        ).select_related('usuario', 'obra').order_by('-data_assistido')[:10]
        
        context['meus_registros_recentes'] = RegistroAssistido.objects.filter(
            usuario=user
        ).select_related('obra').order_by('-data_assistido')[:5]
        
        return context