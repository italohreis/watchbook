from django.urls import reverse_lazy
from .forms import FormularioCadastro, RegistroAssistidoForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from catalogo.models import Obra
from .models import RegistroAssistido, PerfilUsuario
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.shortcuts import redirect
from django.contrib import messages

class RegistrarObraAssistida(LoginRequiredMixin, CreateView):
    form_class = RegistroAssistidoForm
    success_url = reverse_lazy('meus-registros') 

    def form_valid(self, form):
        obra_id = self.kwargs.get('obra_id')
        obra = get_object_or_404(Obra, id=obra_id)
        usuario = self.request.user

        # Verifica se já existe registro dessa obra para este usuário
        if RegistroAssistido.objects.filter(usuario=usuario, obra=obra).exists():
            messages.warning(self.request, 'Você já marcou esta obra como assistida.')
            return redirect(self.request.META.get('HTTP_REFERER', 'buscar-obras'))

        form.instance.usuario = usuario
        form.instance.obra = obra

        messages.success(self.request, 'Registro salvo com sucesso!')
        return super().form_valid(form)

    def get_template_names(self):
        return []

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível salvar. Verifique os campos e tente novamente.')
        return redirect(self.request.META.get('HTTP_REFERER', 'buscar-obras'))
    
class EditarRegistroAssistido(LoginRequiredMixin, UpdateView):
    model = RegistroAssistido
    form_class = RegistroAssistidoForm
    success_url = reverse_lazy('meus-registros')
    login_url = '/'

    def get_queryset(self):
        # Garante que o usuário só pode editar seus próprios registros
        return RegistroAssistido.objects.filter(usuario=self.request.user)
    
    def get_template_names(self):
        # Não renderiza template, apenas processa o POST
        return []
    
    def form_invalid(self, form):
        # Em caso de erro, redireciona de volta
        return redirect(self.request.META.get('HTTP_REFERER', 'meus-registros'))

class ExcluirRegistroAssistido(LoginRequiredMixin, DeleteView):
    model = RegistroAssistido
    success_url = reverse_lazy('meus-registros')
    login_url = '/'

    def get_queryset(self):
        # Garante que o usuário só pode excluir seus próprios registros
        return RegistroAssistido.objects.filter(usuario=self.request.user)
    
    def get_template_names(self):
        # Não renderiza template de confirmação, apenas processa o POST
        return []
    
    def get(self, request, *args, **kwargs):
        # Redireciona GET para a página de registros (evita acesso direto)
        return redirect('meus-registros')

class MeusRegistros(LoginRequiredMixin, ListView):
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


class PerfilUsuarioView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/perfil.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user_id = self.kwargs.get('user_id')
        if user_id:
            perfil = get_object_or_404(PerfilUsuario, pk=user_id)
            is_own_profile = False
        else:
            perfil = PerfilUsuario.objects.get(pk=self.request.user.pk)
            is_own_profile = True
        
        context['perfil_usuario'] = perfil
        context['is_own_profile'] = is_own_profile
        
        context['total_obras'] = perfil.total_obras
        context['total_filmes'] = perfil.total_filmes
        context['total_series'] = perfil.total_series
        context['genero_favorito'] = perfil.genero_favorito
        context['nota_media'] = perfil.nota_media
        context['total_amigos'] = perfil.total_amigos
        
        context['registros_recentes'] = perfil.get_registros_recentes(limit=5)
        
        if not is_own_profile:
            usuario_logado = PerfilUsuario.objects.get(pk=self.request.user.pk)
            context['sao_amigos'] = usuario_logado.sao_amigos(perfil)
        else:
            context['sao_amigos'] = False
            
        return context


class RegistrosUsuario(LoginRequiredMixin, ListView):
    """View para visualizar todos os registros de um usuário específico"""
    model = RegistroAssistido
    template_name = 'usuarios/registros_usuario.html'
    context_object_name = 'registros'
    login_url = '/'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        usuario = get_object_or_404(PerfilUsuario, pk=user_id)
        
        queryset = RegistroAssistido.objects.filter(
            usuario=usuario
        ).select_related('obra')
        
        # Filtrar por tipo se especificado
        tipo_filtro = self.request.GET.get('tipo')
        if tipo_filtro and tipo_filtro in ['filme', 'serie']:
            queryset = queryset.filter(obra__tipo=tipo_filtro)
        
        return queryset.order_by('-data_assistido', '-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
        usuario = get_object_or_404(PerfilUsuario, pk=user_id)
        
        context['usuario_perfil'] = usuario
        context['is_own_profile'] = usuario.id == self.request.user.id
        context['tipo_atual'] = self.request.GET.get('tipo', 'todos')
        
        # Verificar se são amigos
        if not context['is_own_profile']:
            usuario_logado = PerfilUsuario.objects.get(pk=self.request.user.pk)
            context['sao_amigos'] = usuario_logado.sao_amigos(usuario)
        
        return context
 