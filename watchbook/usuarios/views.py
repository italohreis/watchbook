from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import FormularioCadastro, RegistroAssistidoForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from catalogo.models import Obra
from .models import RegistroAssistido
from django.views.generic import ListView
from django.shortcuts import redirect

class RegistrarObraAssistida(LoginRequiredMixin, CreateView):
    form_class = RegistroAssistidoForm
    success_url = reverse_lazy('meus-registros') 

    def form_valid(self, form):
        obra_id = self.kwargs.get('obra_id')
        obra = get_object_or_404(Obra, id=obra_id)
        
        form.instance.usuario = self.request.user
        form.instance.obra = obra
        
        return super().form_valid(form)

    def get_template_names(self):
        return []

    def form_invalid(self, form):
        return redirect(self.request.META.get('HTTP_REFERER', 'buscar-obras'))

class MeusRegistrosView(LoginRequiredMixin, ListView):
    model = RegistroAssistido
    template_name = 'usuarios/meus_registros.html'
    context_object_name = 'registros'
    login_url = '/'

    def get_queryset(self):
        queryset = RegistroAssistido.objects.filter(usuario=self.request.user).select_related('obra')
        
        # Filtrar por tipo se especificado na query string
        tipo_filtro = self.request.GET.get('tipo')
        if tipo_filtro and tipo_filtro in ['filme', 'serie']:
            queryset = queryset.filter(obra__tipo=tipo_filtro)
        
        return queryset.order_by('-data_assistido')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_atual'] = self.request.GET.get('tipo', 'todos')
        return context
    

class CadastrarUsuario(CreateView):
    form_class = FormularioCadastro
    template_name = 'usuarios/cadastrar.html'
    success_url = reverse_lazy('login') 