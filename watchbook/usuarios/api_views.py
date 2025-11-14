from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User
from django.db.models import Q

from .models import RegistroAssistido, PerfilUsuario
from .serializers import (
    UsuarioSerializer, UsuarioCreateSerializer, PerfilUsuarioSerializer,
    RegistroAssistidoSerializer, RegistroCreateSerializer, RegistroUpdateSerializer
)


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para usuários
    
    Endpoints:
    - GET /api/usuarios/ - listar usuários (com busca ?search=nome)
    - POST /api/usuarios/ - criar usuário (cadastro)
    - GET /api/usuarios/{id}/ - detalhe de um usuário
    
    - GET /api/usuarios/me/ - dados do usuário autenticado
    - GET /api/usuarios/meu_perfil/ - perfil completo do usuário autenticado
    - GET /api/usuarios/{id}/perfil/ - perfil completo de outro usuário
    - GET /api/usuarios/{id}/registros/ - registros de um usuário
    """
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']
    
    def get_permissions(self):
        """Permite cadastro sem autenticação"""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        """Usa serializer específico para criação"""
        if self.action == 'create':
            return UsuarioCreateSerializer
        return UsuarioSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        GET /api/usuarios/me/
        retorna dados do usuário autenticado
        """
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def meu_perfil(self, request):
        """
        GET /api/usuarios/meu_perfil/
        retorna perfil completo do usuário autenticado
        """
        perfil = PerfilUsuario.objects.get(id=request.user.id)
        serializer = PerfilUsuarioSerializer(perfil)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def perfil(self, request, pk=None):
        """
        GET /api/usuarios/{id}/perfil/
        retorna perfil completo de um usuário específico
        """
        user = self.get_object()
        perfil = PerfilUsuario.objects.get(id=user.id)
        serializer = PerfilUsuarioSerializer(perfil)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def registros(self, request, pk=None):
        """
        GET /api/usuarios/{id}/registros/
        Lista registros de um usuário específico
        Query params: tipo=F (filmes) ou tipo=S (séries)
        """
        user = self.get_object()
        registros = RegistroAssistido.objects.filter(usuario=user)
        
        tipo = request.query_params.get('tipo', None)
        if tipo:
            registros = registros.filter(obra__tipo=tipo)
        
        registros = registros.order_by('-data_assistido')
        
        serializer = RegistroAssistidoSerializer(registros, many=True)
        return Response(serializer.data)


class RegistroAssistidoViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para registros assistidos
    
    Endpoints:
    - GET /api/registros/ - listar meus registros
    - POST /api/registros/ - criar novo registro
    - GET /api/registros/{id}/ - detalhe de um registro
    - PUT/PATCH /api/registros/{id}/ - atualizar registro
    - DELETE /api/registros/{id}/ - deletar registro
    - GET /api/registros/recentes/ - registros recentes do usuário
    - GET /api/registros/amigos/ - atividades dos amigos
    - GET /api/registros/estatisticas/ - estatísticas do usuário
    """
    serializer_class = RegistroAssistidoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas registros do usuário autenticado"""
        return RegistroAssistido.objects.filter(
            usuario=self.request.user
        ).select_related('obra', 'usuario').order_by('-data_assistido', '-id')
    
    def get_serializer_class(self):
        """Usa serializer específico para cada ação"""
        if self.action == 'create':
            return RegistroCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return RegistroUpdateSerializer
        return RegistroAssistidoSerializer
    
    def perform_create(self, serializer):
        """Adiciona o usuário automaticamente ao criar"""
        serializer.save(usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def recentes(self, request):
        """
        GET /api/registros/recentes/?limit=10
        Retorna os registros mais recentes do usuário
        """
        limit = int(request.query_params.get('limit', 10))
        registros = self.get_queryset()[:limit]
        serializer = self.get_serializer(registros, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def amigos(self, request):
        """
        GET /api/registros/amigos/?limit=10
        Retorna atividades recentes dos amigos
        """
        from amizade.models import Amizade
        
        amizades = Amizade.objects.filter(
            Q(de_usuario=request.user) | Q(para_usuario=request.user),
            status='ACEITO'
        )
        amigos_ids = []
        for amizade in amizades:
            if amizade.de_usuario == request.user:
                amigos_ids.append(amizade.para_usuario.id)
            else:
                amigos_ids.append(amizade.de_usuario.id)
        
        limit = int(request.query_params.get('limit', 10))
        registros = RegistroAssistido.objects.filter(
            usuario__id__in=amigos_ids
        ).select_related('obra', 'usuario').order_by('-data_assistido', '-id')[:limit]
        
        serializer = RegistroAssistidoSerializer(registros, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """
        GET /api/registros/estatisticas/
        Retorna estatísticas dos registros do usuário
        """
        perfil = PerfilUsuario.objects.get(id=request.user.id)
        return Response({
            'total_obras': perfil.total_obras,
            'total_filmes': perfil.total_filmes,
            'total_series': perfil.total_series,
            'genero_favorito': perfil.genero_favorito,
            'nota_media': perfil.nota_media,
            'total_amigos': perfil.total_amigos,
        })
