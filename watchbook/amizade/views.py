from django.views.generic import ListView, View
from django.shortcuts import get_object_or_404, redirect
from .models import Amizade
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404

class PaginaAmigos(LoginRequiredMixin, ListView):
    model = User
    template_name = 'amizade/amigos.html'
    context_object_name = 'resultados'

    def get_queryset(self):
        query = self.request.GET.get('q')
        
        if query:
            return User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query)
            ).exclude(pk=self.request.user.pk)
        
        return User.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')

        context['pedidos_pendentes'] = Amizade.objects.filter(
            para_usuario=self.request.user,
            status='PENDENTE'
        )
        
        # Lista de amigos aceitos (onde o usuário é remetente ou destinatário)
        amizades_aceitas = Amizade.objects.filter(
            Q(de_usuario=self.request.user, status='ACEITO') |
            Q(para_usuario=self.request.user, status='ACEITO')
        ).select_related('de_usuario', 'para_usuario')
        
        # Extrair os IDs dos amigos
        amigos_ids = []
        for amizade in amizades_aceitas:
            if amizade.de_usuario == self.request.user:
                amigos_ids.append(amizade.para_usuario.id)
            else:
                amigos_ids.append(amizade.de_usuario.id)
        
        # Buscar os objetos User dos amigos
        context['amigos'] = User.objects.filter(id__in=amigos_ids)
        
        # Para cada usuário nos resultados da busca, verificar o status da amizade
        if context['query']:
            usuarios_com_status = []
            for usuario in context['resultados']:
                amizade_enviada = Amizade.objects.filter(
                    de_usuario=self.request.user,
                    para_usuario=usuario
                ).first()
                
                amizade_recebida = Amizade.objects.filter(
                    de_usuario=usuario,
                    para_usuario=self.request.user
                ).first()
                
                # Determinar o status
                if amizade_enviada:
                    status = amizade_enviada.status
                    pedido_id = amizade_enviada.id
                elif amizade_recebida:
                    status = amizade_recebida.status
                    pedido_id = amizade_recebida.id
                else:
                    status = None
                    pedido_id = None
                
                usuarios_com_status.append({
                    'usuario': usuario,
                    'status': status,
                    'pedido_id': pedido_id
                })
            
            context['usuarios_com_status'] = usuarios_com_status
        
        return context
            
class EnviarPedidoAmizade(LoginRequiredMixin, View):

    def post(self, request, user_id):
        para_usuario = get_object_or_404(User, pk=user_id)
        de_usuario = request.user
        
        if de_usuario != para_usuario:
            Amizade.objects.get_or_create(
                de_usuario=de_usuario,
                para_usuario=para_usuario
            )
        
        return redirect('pagina-amigos')
    
class ResponderPedidoAmizade(LoginRequiredMixin, View):

    def post(self, request, pedido_id, acao):
        pedido = get_object_or_404(Amizade, pk=pedido_id)

        if pedido.para_usuario != request.user:
            raise Http404("Você não tem permissão para responder a este pedido.")

        if acao == 'aceitar':
            pedido.status = 'ACEITO'
            pedido.save()
        elif acao == 'recusar':
            pedido.delete()
        
        return redirect('pagina-amigos')


class RemoverAmizade(LoginRequiredMixin, View):

    def post(self, request, user_id):
        amigo = get_object_or_404(User, pk=user_id)
        
        amizade = Amizade.objects.filter(
            Q(de_usuario=request.user, para_usuario=amigo, status='ACEITO') |
            Q(de_usuario=amigo, para_usuario=request.user, status='ACEITO')
        ).first()
        
        if amizade:
            amizade.delete()
        
        return redirect('pagina-amigos')