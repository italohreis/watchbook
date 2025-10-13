# catalogo/views.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Obra
from usuarios.forms import RegistroAssistidoForm
from .consts import TIPOS

class ListarObras(LoginRequiredMixin, ListView):
    model = Obra
    context_object_name = 'lista_obras'
    template_name = 'catalogo/listar.html'
    login_url = '/'
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('titulo')
        
        # Filtrar por tipo se especificado na query string
        tipo_filtro = self.request.GET.get('tipo')
        if tipo_filtro and tipo_filtro in dict(TIPOS).keys(): 
            queryset = queryset.filter(tipo=tipo_filtro)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_registro'] = RegistroAssistidoForm()
        context['tipo_atual'] = self.request.GET.get('tipo', 'todos')
        return context