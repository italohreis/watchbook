from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Amizade
from .serializers import AmizadeSerializer, AmizadeCreateSerializer


class AmizadeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para amizades
    
    Endpoints:
    - GET /api/amizades/ - listar minhas amizades
    - POST /api/amizades/ - enviar solicitação de amizade
    - GET /api/amizades/{id}/ - detalhe de uma amizade
    - DELETE /api/amizades/{id}/ - deletar amizade
    
    - POST /api/amizades/{id}/aceitar/ - aceitar solicitação
    - POST /api/amizades/{id}/rejeitar/ - rejeitar solicitação
    - GET /api/amizades/pendentes/ - solicitações pendentes recebidas
    - GET /api/amizades/aceitas/ - amizades aceitas
    """
    serializer_class = AmizadeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna amizades relacionadas ao usuário autenticado"""
        user = self.request.user
        return Amizade.objects.filter(
            Q(de_usuario=user) | Q(para_usuario=user)
        ).select_related('de_usuario', 'para_usuario').order_by('-data_criacao')
    
    def get_serializer_class(self):
        """Usa serializer específico para criação"""
        if self.action == 'create':
            return AmizadeCreateSerializer
        return AmizadeSerializer
    
    def destroy(self, request, *args, **kwargs):
        """Permite deletar apenas amizades que envolvem o usuário"""
        amizade = self.get_object()
        user = request.user
        
        if amizade.de_usuario != user and amizade.para_usuario != user:
            return Response(
                {'erro': 'Você não pode deletar esta amizade.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def aceitar(self, request, pk=None):
        """
        POST /api/amizades/{id}/aceitar/
        Aceita uma solicitação de amizade
        """
        amizade = self.get_object()
        
        # Apenas o destinatário pode aceitar
        if amizade.para_usuario != request.user:
            return Response(
                {'erro': 'Você não pode aceitar esta solicitação.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if amizade.status == 'ACEITO':
            return Response(
                {'erro': 'Esta solicitação já foi aceita.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        amizade.status = 'ACEITO'
        amizade.save()
        
        serializer = AmizadeSerializer(amizade)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def rejeitar(self, request, pk=None):
        """
        POST /api/amizades/{id}/rejeitar/
        Rejeita/deleta uma solicitação de amizade
        """
        amizade = self.get_object()
        
        # Apenas o destinatário pode rejeitar
        if amizade.para_usuario != request.user:
            return Response(
                {'erro': 'Você não pode rejeitar esta solicitação.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        amizade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """
        GET /api/amizades/pendentes/
        Lista solicitações pendentes recebidas
        """
        pendentes = Amizade.objects.filter(
            para_usuario=request.user,
            status='PENDENTE'
        ).select_related('de_usuario', 'para_usuario').order_by('-data_criacao')
        
        serializer = AmizadeSerializer(pendentes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def aceitas(self, request):
        """
        GET /api/amizades/aceitas/
        Lista amizades aceitas
        """
        user = request.user
        aceitas = Amizade.objects.filter(
            Q(de_usuario=user) | Q(para_usuario=user),
            status='ACEITO'
        ).select_related('de_usuario', 'para_usuario').order_by('-data_criacao')
        
        serializer = AmizadeSerializer(aceitas, many=True)
        return Response(serializer.data)
