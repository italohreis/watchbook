# watchbook/views.py
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from usuarios.forms import FormularioLogin 

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('buscar-obras') 
        
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
                return redirect('buscar-obras')

       
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'usuarios/login.html', {'form': form})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')