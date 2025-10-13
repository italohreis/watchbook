# catalogo/views.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Obra
from usuarios.forms import RegistroAssistidoForm

class ListarObras(LoginRequiredMixin, ListView):
    model = Obra
    context_object_name = 'lista_obras'
    template_name = 'catalogo/listar.html'
    login_url = '/'
    
    def get_queryset(self):
        return super().get_queryset().order_by('titulo')