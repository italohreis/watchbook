# catalogo/views.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Obra

class ListarObras(LoginRequiredMixin, ListView):
    model = Obra
    context_object_name = 'lista_obras'
    template_name = 'catalogo/listar.html'
    login_url = '/'