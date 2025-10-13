from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import FormularioCadastro

class CadastrarUsuario(CreateView):
    form_class = FormularioCadastro
    template_name = 'usuarios/cadastrar.html'
    success_url = reverse_lazy('login') 